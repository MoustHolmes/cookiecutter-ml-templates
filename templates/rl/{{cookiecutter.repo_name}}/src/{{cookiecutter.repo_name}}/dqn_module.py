"""Deep Q-Network (DQN) implemented as a PyTorch Lightning module.

Off-policy algorithm for discrete action spaces.  Uses a target network and
ε-greedy exploration with linear decay.

Ported from CleanRL (https://github.com/vwxyzjn/cleanrl).
"""

from __future__ import annotations

import copy
import random
from functools import partial

import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as L
from torch.optim import Adam

from {{cookiecutter.repo_name}}.data.replay_buffer import Batch
from {{cookiecutter.repo_name}}.models.qnetwork import QNetwork


class DQNModule(L.LightningModule):
    """DQN LightningModule.

    Works with :class:`~{{cookiecutter.repo_name}}.data.env_datamodule.RLDataModule`
    (same as SAC/TD3).  ``training_step`` is called once per sampled batch;
    it collects one env step, then optionally runs a gradient update and/or a
    target-network update based on the step counters.

    Args:
        q_network: QNetwork instance.
        gamma: Discount factor.
        tau: Soft-update coefficient for target network (1.0 = hard update).
        batch_size: Mini-batch size for gradient updates.
        learning_starts: Random-action warm-up steps before first gradient update.
        train_frequency: Gradient update every N env steps.
        target_network_frequency: Target network update every N env steps.
        start_epsilon: Initial exploration rate.
        end_epsilon: Final exploration rate.
        exploration_fraction: Fraction of total_timesteps over which epsilon decays.
        total_timesteps: Used for epsilon and LR scheduling.
        optimizer: Partial optimizer factory.
    """

    automatic_optimization = False

    def __init__(
        self,
        q_network: QNetwork,
        gamma: float = 0.99,
        tau: float = 1.0,
        batch_size: int = 128,
        learning_starts: int = 10_000,
        train_frequency: int = 10,
        target_network_frequency: int = 500,
        start_epsilon: float = 1.0,
        end_epsilon: float = 0.05,
        exploration_fraction: float = 0.5,
        total_timesteps: int = 500_000,
        optimizer=None,
    ) -> None:
        super().__init__()
        self.automatic_optimization = False
        self.save_hyperparameters(logger=False, ignore=["q_network"])

        self.q_network = q_network

        # Target network: frozen copy, updated periodically
        self.q_target = copy.deepcopy(q_network)
        for p in self.q_target.parameters():
            p.requires_grad = False

        self.hparams.optimizer = optimizer or partial(Adam, lr=1e-4)
        self._total_env_steps: int = 0

    # ------------------------------------------------------------------
    # Lightning lifecycle
    # ------------------------------------------------------------------

    def setup(self, stage: str) -> None:
        """Pre-fill the replay buffer with random transitions."""
        if stage == "fit":
            dm = self.trainer.datamodule
            n_prefill = max(self.hparams.learning_starts, self.hparams.batch_size) - len(dm.replay_buffer)
            if n_prefill > 0:
                dm.collect_experience(n_steps=n_prefill, policy_fn=None)
                self._total_env_steps += n_prefill

    def configure_optimizers(self) -> list[torch.optim.Optimizer]:
        return [self.hparams.optimizer(self.q_network.parameters())]

    # ------------------------------------------------------------------
    # Training step
    # ------------------------------------------------------------------

    def training_step(self, batch: Batch, batch_idx: int) -> None:  # noqa: ARG002
        opt = self.optimizers()
        dm = self.trainer.datamodule
        hp = self.hparams

        # ---- 1. ε-greedy action collection ----------------------------
        epsilon = self._linear_schedule(
            hp.start_epsilon,
            hp.end_epsilon,
            hp.exploration_fraction * hp.total_timesteps,
            self._total_env_steps,
        )

        if random.random() < epsilon:
            policy_fn = None  # random action via RLDataModule
        else:
            def policy_fn(obs: torch.Tensor) -> torch.Tensor:
                q_vals = self.q_network(obs.to(self.device))
                return q_vals.argmax(dim=1).float()

        dm.collect_experience(n_steps=1, policy_fn=policy_fn)
        self._total_env_steps += 1

        # ---- 2. Warm-up guard -----------------------------------------
        if self._total_env_steps < hp.learning_starts:
            self.log("train/epsilon", epsilon, prog_bar=True, on_step=True)
            return

        # ---- 3. Gradient update (every train_frequency steps) ---------
        if self._total_env_steps % hp.train_frequency == 0:
            ub = dm.replay_buffer.sample(hp.batch_size)
            ub = Batch(
                obs=ub.obs.to(self.device),
                action=ub.action.to(self.device),
                reward=ub.reward.to(self.device),
                next_obs=ub.next_obs.to(self.device),
                done=ub.done.to(self.device),
            )

            with torch.no_grad():
                target_max = self.q_target(ub.next_obs).max(dim=1).values
                td_target = ub.reward + hp.gamma * target_max * (1.0 - ub.done)

            # Actions stored as float — cast to long for gather
            actions_long = ub.action.long()
            if actions_long.ndim == 1:
                actions_long = actions_long.unsqueeze(1)
            q_val = self.q_network(ub.obs).gather(1, actions_long).squeeze(1)
            loss = F.mse_loss(q_val, td_target)

            opt.zero_grad()
            self.manual_backward(loss)
            opt.step()

            self.log("train/td_loss", loss, prog_bar=False, on_step=True)
            self.log("train/q_values", q_val.mean(), on_step=True)

        # ---- 4. Target network update ---------------------------------
        if self._total_env_steps % hp.target_network_frequency == 0:
            tau = hp.tau
            for q_p, t_p in zip(self.q_network.parameters(), self.q_target.parameters()):
                t_p.data.copy_(tau * q_p.data + (1.0 - tau) * t_p.data)

        # ---- 5. Logging -----------------------------------------------
        self.log("train/epsilon", epsilon, prog_bar=True, on_step=True)
        self.log("train/total_env_steps", float(self._total_env_steps), prog_bar=True)

        if dm.episode_rewards:
            self.log("train/episode_reward", dm.episode_rewards[-1], prog_bar=True)
            self.log("train/episode_length", float(dm.episode_lengths[-1]))

    # ------------------------------------------------------------------
    # Unified eval interface for callbacks
    # ------------------------------------------------------------------

    def act_deterministic(self, obs: torch.Tensor) -> torch.Tensor:
        """Return greedy action (argmax Q) for callbacks and evaluation."""
        return self.q_network(obs).argmax(dim=-1, keepdim=True).float()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _linear_schedule(start: float, end: float, duration: float, t: int) -> float:
        slope = (end - start) / duration
        return max(slope * t + start, end)
