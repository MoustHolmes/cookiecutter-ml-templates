"""Soft Actor-Critic (SAC) implemented as a PyTorch Lightning module.

SAC is an off-policy, maximum-entropy actor-critic algorithm for continuous
action spaces.  It jointly maximises expected cumulative reward *and* policy
entropy, which encourages exploration and prevents premature convergence.

Key algorithmic features implemented here:

- **Twin critics** — two independent Q-networks; Bellman targets use their
  minimum to suppress overestimation bias.
- **Reparameterization trick** — actions are sampled as ``tanh(μ + σε)`` so
  that gradients flow through the stochastic sampling step.
- **Automatic temperature tuning** — the entropy coefficient ``α`` is adapted
  online via dual gradient descent to match a target entropy.
- **Polyak averaging** — a frozen target critic is maintained by slowly
  tracking the online critic weights (``τ`` smoothing).
- **Correct truncation semantics** — truncated episodes do *not* mask the
  value bootstrap (stored ``done=0``); only genuine terminations do.

Lightning integration notes:

- ``automatic_optimization = False`` — three optimizers (critic, actor, alpha)
  are managed manually so that their update frequencies can be controlled.
- The dataloader is driven by :class:`~{{cookiecutter.repo_name}}.data.env_datamodule.RLDataModule`
  which yields :class:`~{{cookiecutter.repo_name}}.data.replay_buffer.Batch` objects from the
  replay buffer.  Each ``training_step`` first calls back into the datamodule
  to collect new environment experience, then performs gradient updates.
"""

from __future__ import annotations

import copy
from functools import partial
from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as L
from torch.optim import Adam

from {{cookiecutter.repo_name}}.data.replay_buffer import Batch
from {{cookiecutter.repo_name}}.models.actor import StochasticActor
from {{cookiecutter.repo_name}}.models.critic import TwinCritic


class SACModule(L.LightningModule):
    """Soft Actor-Critic (SAC) LightningModule.

    Args:
        actor: Stochastic actor network (:class:`~{{cookiecutter.repo_name}}.models.actor.StochasticActor`).
        critic: Twin Q-network (:class:`~{{cookiecutter.repo_name}}.models.critic.TwinCritic`).
        gamma: Discount factor (``γ``).
        tau: Polyak averaging coefficient for target network updates.
        batch_size: Mini-batch size for gradient updates (also used when
            sampling directly from the buffer inside ``training_step``).
        learning_starts: Number of environment steps collected with random
            actions before any gradient updates are performed.
        collect_steps_per_update: Environment steps collected per
            ``training_step`` call.
        gradient_steps: Gradient update iterations per ``training_step`` call.
        init_alpha: Initial temperature value.  The learnable parameter is
            ``log_alpha``; ``alpha = exp(log_alpha) > 0`` is always guaranteed.
        target_entropy: Target entropy for automatic temperature tuning.
            ``None`` → auto-set to ``-action_dim`` at ``on_train_start``.
        actor_optimizer: Partial optimizer factory for the actor.
        critic_optimizer: Partial optimizer factory for the critic.
        alpha_optimizer: Partial optimizer factory for ``log_alpha``.
    """

    def __init__(
        self,
        actor: StochasticActor,
        critic: TwinCritic,
        gamma: float = 0.99,
        tau: float = 0.005,
        batch_size: int = 256,
        learning_starts: int = 1000,
        collect_steps_per_update: int = 1,
        gradient_steps: int = 1,
        init_alpha: float = 1.0,
        target_entropy: float | None = None,
        actor_optimizer=None,
        critic_optimizer=None,
        alpha_optimizer=None,
    ) -> None:
        super().__init__()
        self.automatic_optimization = False  # Three optimizers — managed manually
        self.save_hyperparameters(logger=False, ignore=["actor", "critic"])

        self.actor = actor
        self.critic = critic

        # Target critic: frozen copy updated via Polyak averaging
        self.critic_target = copy.deepcopy(critic)
        for param in self.critic_target.parameters():
            param.requires_grad = False

        # Learnable log-temperature (guarantees alpha > 0 via exp())
        self.log_alpha = nn.Parameter(torch.tensor(float(init_alpha)).log())

        # Store optimizer factories (Hydra partial instantiation or defaults)
        self.hparams.actor_optimizer = actor_optimizer or partial(Adam, lr=3e-4)
        self.hparams.critic_optimizer = critic_optimizer or partial(Adam, lr=3e-4)
        self.hparams.alpha_optimizer = alpha_optimizer or partial(Adam, lr=3e-4)

        self._total_env_steps: int = 0

    @property
    def alpha(self) -> torch.Tensor:
        """Current temperature value (always > 0)."""
        return self.log_alpha.exp()

    # ------------------------------------------------------------------
    # Lightning lifecycle
    # ------------------------------------------------------------------

    def setup(self, stage: str) -> None:
        """Pre-fill the replay buffer before the training loop creates the dataloader iterator.

        ``on_train_start`` is called *after* Lightning's ``fit_loop.setup_data()`` eagerly
        creates the dataloader iterator (which immediately tries to sample from the buffer).
        ``setup()`` is called earlier — before the loop starts — so the buffer is ready in time.
        """
        if stage == "fit":
            if self.hparams.target_entropy is None:
                action_dim = self.actor.mean_head.out_features
                self.hparams.target_entropy = -float(action_dim)

            dm = self.trainer.datamodule
            n_prefill = max(self.hparams.learning_starts, self.hparams.batch_size) - len(dm.replay_buffer)
            if n_prefill > 0:
                dm.collect_experience(n_steps=n_prefill, policy_fn=None)
                self._total_env_steps += n_prefill

    def configure_optimizers(self) -> list[torch.optim.Optimizer]:
        """Return [critic_opt, actor_opt, alpha_opt]."""
        critic_opt = self.hparams.critic_optimizer(self.critic.parameters())
        actor_opt = self.hparams.actor_optimizer(self.actor.parameters())
        alpha_opt = self.hparams.alpha_optimizer([self.log_alpha])
        return [critic_opt, actor_opt, alpha_opt]

    # ------------------------------------------------------------------
    # Training step
    # ------------------------------------------------------------------

    def training_step(self, batch: Batch, batch_idx: int) -> None:  # noqa: ARG002
        """One SAC training step.

        1. Collect environment experience (calls back into the datamodule).
        2. Skip gradient updates during warm-up (``learning_starts`` steps).
        3. Run ``gradient_steps`` update iterations.
        4. Soft-update the target critic.
        5. Log metrics.

        Args:
            batch: A :class:`~{{cookiecutter.repo_name}}.data.replay_buffer.Batch` from the
                replay buffer dataloader.  Its values are *not* used for the
                gradient update — we re-sample from the buffer inside the loop
                to support ``gradient_steps > 1``.
            batch_idx: Batch index (unused).
        """
        critic_opt, actor_opt, alpha_opt = self.optimizers()
        dm = self.trainer.datamodule

        # ---- Step 1: collect experience --------------------------------
        if self._total_env_steps < self.hparams.learning_starts:
            policy_fn = None  # random actions during warm-up
        else:
            def policy_fn(obs: torch.Tensor) -> torch.Tensor:
                action, _, _ = self.actor.get_action(obs.to(self.device))
                return action

        dm.collect_experience(self.hparams.collect_steps_per_update, policy_fn)
        self._total_env_steps += self.hparams.collect_steps_per_update

        # ---- Step 2: warm-up guard ------------------------------------
        if len(dm.replay_buffer) < self.hparams.learning_starts:
            return

        # ---- Step 3: gradient updates ----------------------------------
        for _ in range(self.hparams.gradient_steps):
            update_batch = dm.replay_buffer.sample(self.hparams.batch_size)
            update_batch = Batch(
                obs=update_batch.obs.to(self.device),
                action=update_batch.action.to(self.device),
                reward=update_batch.reward.to(self.device),
                next_obs=update_batch.next_obs.to(self.device),
                done=update_batch.done.to(self.device),
            )

            critic_loss = self._update_critic(update_batch, critic_opt)
            actor_loss, alpha_loss = self._update_actor_and_alpha(
                update_batch, actor_opt, alpha_opt
            )

        # ---- Step 4: soft-update target networks -----------------------
        self._soft_update_target()

        # ---- Step 5: logging ------------------------------------------
        self.log("train/critic_loss", critic_loss, prog_bar=False, on_step=True)
        self.log("train/actor_loss", actor_loss, prog_bar=False, on_step=True)
        self.log("train/alpha_loss", alpha_loss, prog_bar=False, on_step=True)
        self.log("train/alpha", self.alpha.item(), prog_bar=True, on_step=True)
        self.log("train/total_env_steps", float(self._total_env_steps), prog_bar=True)

        if dm.episode_rewards:
            self.log("train/episode_reward", dm.episode_rewards[-1], prog_bar=True)
            self.log("train/episode_length", float(dm.episode_lengths[-1]))

    # ------------------------------------------------------------------
    # SAC update steps
    # ------------------------------------------------------------------

    def _update_critic(
        self,
        batch: Batch,
        critic_opt: torch.optim.Optimizer,
    ) -> torch.Tensor:
        """Compute and apply the twin-critic (Q-network) loss.

        Bellman target::

            y = r + γ · (1 - done) · [min_Q_target(s', a') - α · log_π(a'|s')]

        where ``a'`` is freshly sampled from the current policy at ``next_obs``.

        Args:
            batch: Mini-batch of transitions on the correct device.
            critic_opt: Optimizer for the twin critic.

        Returns:
            Scalar critic loss tensor.
        """
        with torch.no_grad():
            next_action, next_log_prob, _ = self.actor.get_action(batch.next_obs)
            q_target = self.critic_target.min_q(batch.next_obs, next_action).squeeze(-1)
            backup = batch.reward + self.hparams.gamma * (1.0 - batch.done) * (
                q_target - self.alpha.detach() * next_log_prob
            )

        q1, q2 = self.critic(batch.obs, batch.action)
        critic_loss = F.mse_loss(q1.squeeze(-1), backup) + F.mse_loss(q2.squeeze(-1), backup)

        critic_opt.zero_grad()
        self.manual_backward(critic_loss)
        critic_opt.step()
        return critic_loss

    def _update_actor_and_alpha(
        self,
        batch: Batch,
        actor_opt: torch.optim.Optimizer,
        alpha_opt: torch.optim.Optimizer,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute and apply actor and temperature losses.

        Actor objective::

            min_θ  α · log_π(a|s) - min_Q(s, a)

        Temperature (dual gradient descent)::

            min_α  -α · (log_π(a|s) + H_target)

        Args:
            batch: Mini-batch of transitions on the correct device.
            actor_opt: Optimizer for the actor.
            alpha_opt: Optimizer for ``log_alpha``.

        Returns:
            Tuple ``(actor_loss, alpha_loss)``.
        """
        action, log_prob, _ = self.actor.get_action(batch.obs)
        q_value = self.critic.min_q(batch.obs, action).squeeze(-1)

        actor_loss = (self.alpha.detach() * log_prob - q_value).mean()
        actor_opt.zero_grad()
        self.manual_backward(actor_loss)
        actor_opt.step()

        alpha_loss = -(self.log_alpha * (log_prob.detach() + self.hparams.target_entropy)).mean()
        alpha_opt.zero_grad()
        self.manual_backward(alpha_loss)
        alpha_opt.step()

        return actor_loss, alpha_loss

    def act_deterministic(self, obs: torch.Tensor) -> torch.Tensor:
        """Return the deterministic (mean) action for callbacks and evaluation."""
        return self.actor.act_deterministic(obs)

    def _soft_update_target(self) -> None:
        """Polyak averaging: ``target ← τ · online + (1 - τ) · target``."""
        tau = self.hparams.tau
        for online, target in zip(
            self.critic.parameters(), self.critic_target.parameters()
        ):
            target.data.mul_(1.0 - tau).add_(online.data, alpha=tau)
