"""Twin Delayed DDPG (TD3) implemented as a PyTorch Lightning module.

TD3 addresses the overestimation bias of DDPG with three key additions:

1. **Clipped Double-Q Learning** — two independent critics; Bellman targets
   use their minimum.
2. **Target Policy Smoothing** — small clipped noise is added to target
   actions during critic updates, regularising the value function across
   neighbouring actions.
3. **Delayed Policy Updates** — the actor and target networks are updated
   less frequently than the critics (every ``policy_delay`` critic steps),
   reducing variance in policy gradient estimates.

Lightning integration follows the same pattern as :class:`~{{cookiecutter.repo_name}}.sac_module.SACModule`:
``automatic_optimization=False`` with manual management of two optimizers.
"""

from __future__ import annotations

import copy
from functools import partial

import torch
import torch.nn.functional as F
import lightning as L
from torch.optim import Adam

from {{cookiecutter.repo_name}}.data.replay_buffer import Batch
from {{cookiecutter.repo_name}}.models.actor import DeterministicActor
from {{cookiecutter.repo_name}}.models.critic import TwinCritic


class TD3Module(L.LightningModule):
    """Twin Delayed DDPG (TD3) LightningModule.

    Args:
        actor: Deterministic actor network (:class:`~{{cookiecutter.repo_name}}.models.actor.DeterministicActor`).
        critic: Twin Q-network (:class:`~{{cookiecutter.repo_name}}.models.critic.TwinCritic`).
        gamma: Discount factor (``γ``).
        tau: Polyak averaging coefficient for target network updates.
        batch_size: Mini-batch size for gradient updates.
        learning_starts: Random-action warm-up steps before first update.
        collect_steps_per_update: Environment steps per ``training_step`` call.
        gradient_steps: Gradient update iterations per ``training_step`` call.
        policy_delay: Actor + target networks updated every ``policy_delay``
            critic gradient steps.
        exploration_noise: Std of Gaussian noise added to actions during
            environment collection (promotes exploration).
        target_noise: Std of smoothing noise added to target policy actions
            during critic updates (prevents sharp Q-function peaks).
        target_noise_clip: Symmetric clip applied to the target noise.
        actor_optimizer: Partial optimizer factory for the actor.
        critic_optimizer: Partial optimizer factory for the critic.
    """

    def __init__(
        self,
        actor: DeterministicActor,
        critic: TwinCritic,
        gamma: float = 0.99,
        tau: float = 0.005,
        batch_size: int = 256,
        learning_starts: int = 1000,
        collect_steps_per_update: int = 1,
        gradient_steps: int = 1,
        policy_delay: int = 2,
        exploration_noise: float = 0.1,
        target_noise: float = 0.2,
        target_noise_clip: float = 0.5,
        actor_optimizer=None,
        critic_optimizer=None,
    ) -> None:
        super().__init__()
        self.automatic_optimization = False
        self.save_hyperparameters(logger=False, ignore=["actor", "critic"])

        self.actor = actor
        self.critic = critic

        # Frozen target copies updated via Polyak averaging
        self.actor_target = copy.deepcopy(actor)
        self.critic_target = copy.deepcopy(critic)
        for param in list(self.actor_target.parameters()) + list(self.critic_target.parameters()):
            param.requires_grad = False

        self.hparams.actor_optimizer = actor_optimizer or partial(Adam, lr=3e-4)
        self.hparams.critic_optimizer = critic_optimizer or partial(Adam, lr=3e-4)

        self._total_env_steps: int = 0
        self._critic_update_count: int = 0  # tracks when to update actor

    # ------------------------------------------------------------------
    # Lightning lifecycle
    # ------------------------------------------------------------------

    def setup(self, stage: str) -> None:
        """Pre-fill the replay buffer before the training loop creates the dataloader iterator."""
        if stage == "fit":
            dm = self.trainer.datamodule
            n_prefill = max(self.hparams.learning_starts, self.hparams.batch_size) - len(dm.replay_buffer)
            if n_prefill > 0:
                dm.collect_experience(n_steps=n_prefill, policy_fn=None)
                self._total_env_steps += n_prefill

    def configure_optimizers(self) -> list[torch.optim.Optimizer]:
        """Return [critic_opt, actor_opt]."""
        critic_opt = self.hparams.critic_optimizer(self.critic.parameters())
        actor_opt = self.hparams.actor_optimizer(self.actor.parameters())
        return [critic_opt, actor_opt]

    # ------------------------------------------------------------------
    # Training step
    # ------------------------------------------------------------------

    def training_step(self, batch: Batch, batch_idx: int) -> None:  # noqa: ARG002
        """One TD3 training step.

        1. Collect environment experience with noisy deterministic policy.
        2. Skip gradient updates during warm-up.
        3. Run ``gradient_steps`` critic updates; update actor every
           ``policy_delay`` critic updates.
        4. Log metrics.

        Args:
            batch: A :class:`~{{cookiecutter.repo_name}}.data.replay_buffer.Batch` from the
                replay buffer dataloader (values not directly used — we
                re-sample for ``gradient_steps > 1``).
            batch_idx: Batch index (unused).
        """
        critic_opt, actor_opt = self.optimizers()
        dm = self.trainer.datamodule

        # ---- Step 1: collect experience --------------------------------
        if self._total_env_steps < self.hparams.learning_starts:
            policy_fn = None
        else:
            noise_std = self.hparams.exploration_noise

            def policy_fn(obs: torch.Tensor) -> torch.Tensor:
                action = self.actor(obs.to(self.device))
                noise = torch.randn_like(action) * noise_std * self.actor.action_scale
                lo = self.actor.action_bias - self.actor.action_scale
                hi = self.actor.action_bias + self.actor.action_scale
                return (action + noise).clamp(lo, hi)

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
            self._critic_update_count += 1

            # Delayed actor + target updates
            actor_loss = None
            if self._critic_update_count % self.hparams.policy_delay == 0:
                actor_loss = self._update_actor(update_batch, actor_opt)
                self._soft_update_targets()

        # ---- Step 4: logging ------------------------------------------
        self.log("train/critic_loss", critic_loss, prog_bar=False, on_step=True)
        if actor_loss is not None:
            self.log("train/actor_loss", actor_loss, prog_bar=False, on_step=True)
        self.log("train/total_env_steps", float(self._total_env_steps), prog_bar=True)

        if dm.episode_rewards:
            self.log("train/episode_reward", dm.episode_rewards[-1], prog_bar=True)
            self.log("train/episode_length", float(dm.episode_lengths[-1]))

    # ------------------------------------------------------------------
    # TD3 update steps
    # ------------------------------------------------------------------

    def _update_critic(
        self,
        batch: Batch,
        critic_opt: torch.optim.Optimizer,
    ) -> torch.Tensor:
        """Compute and apply the twin-critic loss with target policy smoothing.

        Bellman target::

            ã = clip(π_target(s') + clip(ε, -c, c), -1, 1),  ε ~ N(0, σ)
            y = r + γ · (1 - done) · min_Q_target(s', ã)

        Args:
            batch: Mini-batch of transitions on the correct device.
            critic_opt: Optimizer for the twin critic.

        Returns:
            Scalar critic loss tensor.
        """
        with torch.no_grad():
            noise = (
                torch.randn_like(batch.action) * self.hparams.target_noise
            ).clamp(-self.hparams.target_noise_clip, self.hparams.target_noise_clip) * self.actor_target.action_scale
            lo = self.actor_target.action_bias - self.actor_target.action_scale
            hi = self.actor_target.action_bias + self.actor_target.action_scale
            next_action = (self.actor_target(batch.next_obs) + noise).clamp(lo, hi)

            q_target = self.critic_target.min_q(batch.next_obs, next_action).squeeze(-1)
            backup = batch.reward + self.hparams.gamma * (1.0 - batch.done) * q_target

        q1, q2 = self.critic(batch.obs, batch.action)
        critic_loss = F.mse_loss(q1.squeeze(-1), backup) + F.mse_loss(q2.squeeze(-1), backup)

        critic_opt.zero_grad()
        self.manual_backward(critic_loss)
        critic_opt.step()
        return critic_loss

    def _update_actor(
        self,
        batch: Batch,
        actor_opt: torch.optim.Optimizer,
    ) -> torch.Tensor:
        """Compute and apply the deterministic policy gradient loss.

        Actor objective::

            min_θ  -Q1(s, π_θ(s))

        Only ``q1`` is used for the policy gradient (not the minimum) to avoid
        introducing pessimism bias into the actor objective.

        Args:
            batch: Mini-batch of transitions on the correct device.
            actor_opt: Optimizer for the actor.

        Returns:
            Scalar actor loss tensor.
        """
        action = self.actor(batch.obs)
        q1, _ = self.critic(batch.obs, action)
        actor_loss = -q1.mean()

        actor_opt.zero_grad()
        self.manual_backward(actor_loss)
        actor_opt.step()
        return actor_loss

    def act_deterministic(self, obs: torch.Tensor) -> torch.Tensor:
        """Return the deterministic action for callbacks and evaluation."""
        return self.actor.act_deterministic(obs)

    def _soft_update_targets(self) -> None:
        """Polyak averaging for both actor and critic target networks."""
        tau = self.hparams.tau
        for online, target in zip(self.actor.parameters(), self.actor_target.parameters()):
            target.data.mul_(1.0 - tau).add_(online.data, alpha=tau)
        for online, target in zip(self.critic.parameters(), self.critic_target.parameters()):
            target.data.mul_(1.0 - tau).add_(online.data, alpha=tau)
