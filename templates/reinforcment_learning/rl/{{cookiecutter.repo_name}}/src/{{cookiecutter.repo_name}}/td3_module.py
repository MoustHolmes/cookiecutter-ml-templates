"""Twin Delayed DDPG (TD3) implemented as a PyTorch Lightning module.

TD3 addresses the overestimation bias of DDPG with three key additions:

1. **Clipped Double-Q Learning** — two critics; Bellman targets use ``min(Q₁, Q₂)``.
2. **Target Policy Smoothing** — small clipped noise is added to target actions
   during critic updates, regularising the value function.
3. **Delayed Policy Updates** — the actor and target networks update every
   ``policy_delay`` critic steps.

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


class TD3Module(L.LightningModule):
    """Twin Delayed DDPG (TD3) LightningModule.

    Args:
        actor: Deterministic actor network — maps obs to pre-tanh actions.
        critic: :class:`~{{cookiecutter.repo_name}}.models.critic.TwinCritic`.
        action_scale: ``(high - low) / 2`` for the action space (from env config).
        action_bias: ``(high + low) / 2`` for the action space (from env config).
        gamma: Discount factor.
        tau: Polyak averaging coefficient for target networks.
        batch_size: Mini-batch size for gradient updates.
        learning_starts: Random-action warm-up steps before first update.
        collect_steps_per_update: Environment steps per ``training_step`` call.
        gradient_steps: Gradient update iterations per ``training_step`` call.
        policy_delay: Actor + targets updated every N critic gradient steps.
        exploration_noise: Std of noise added to actions during collection.
        target_noise: Std of smoothing noise added to target actions.
        target_noise_clip: Clip range for target smoothing noise.
        actor_optimizer: Partial optimizer factory for the actor.
        critic_optimizer: Partial optimizer factory for the critic.
    """

    def __init__(
        self,
        actor,
        critic,
        action_scale: float = 1.0,
        action_bias: float = 0.0,
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
        self.actor_target = copy.deepcopy(actor)
        self.critic_target = copy.deepcopy(critic)
        for p in list(self.actor_target.parameters()) + list(self.critic_target.parameters()):
            p.requires_grad = False

        # Environment action space scaling (from env config, not model architecture)
        self.register_buffer("_action_scale", torch.tensor(action_scale, dtype=torch.float32))
        self.register_buffer("_action_bias", torch.tensor(action_bias, dtype=torch.float32))

        self.hparams.actor_optimizer = actor_optimizer or partial(Adam, lr=3e-4)
        self.hparams.critic_optimizer = critic_optimizer or partial(Adam, lr=3e-4)

        self._total_env_steps: int = 0
        self._critic_update_count: int = 0

    # ------------------------------------------------------------------
    # Lightning lifecycle
    # ------------------------------------------------------------------

    def setup(self, stage: str) -> None:
        if stage == "fit":
            dm = self.trainer.datamodule
            n_prefill = max(self.hparams.learning_starts, self.hparams.batch_size) - len(dm.replay_buffer)
            if n_prefill > 0:
                dm.collect_experience(n_steps=n_prefill, policy_fn=None)
                self._total_env_steps += n_prefill

    def configure_optimizers(self) -> list[torch.optim.Optimizer]:
        critic_opt = self.hparams.critic_optimizer(self.critic.parameters())
        actor_opt = self.hparams.actor_optimizer(self.actor.parameters())
        return [critic_opt, actor_opt]

    # ------------------------------------------------------------------
    # Training step
    # ------------------------------------------------------------------

    def training_step(self, batch: Batch, batch_idx: int) -> None:  # noqa: ARG002
        critic_opt, actor_opt = self.optimizers()
        dm = self.trainer.datamodule

        # ---- 1. Collect experience with noisy deterministic policy ----
        if self._total_env_steps < self.hparams.learning_starts:
            policy_fn = None
        else:
            noise_std = self.hparams.exploration_noise
            lo = self._action_bias - self._action_scale
            hi = self._action_bias + self._action_scale

            def policy_fn(obs: torch.Tensor) -> torch.Tensor:
                raw = self.actor(obs.to(self.device))
                action = torch.tanh(raw) * self._action_scale + self._action_bias
                noise = torch.randn_like(action) * noise_std
                return (action + noise).clamp(lo, hi)

        dm.collect_experience(self.hparams.collect_steps_per_update, policy_fn)
        self._total_env_steps += self.hparams.collect_steps_per_update

        # ---- 2. Warm-up guard -----------------------------------------
        if len(dm.replay_buffer) < self.hparams.learning_starts:
            return

        # ---- 3. Gradient updates --------------------------------------
        for _ in range(self.hparams.gradient_steps):
            b = dm.replay_buffer.sample(self.hparams.batch_size)
            b = Batch(
                obs=b.obs.to(self.device), action=b.action.to(self.device),
                reward=b.reward.to(self.device), next_obs=b.next_obs.to(self.device),
                done=b.done.to(self.device),
            )

            critic_loss = self._update_critic(b, critic_opt)
            self._critic_update_count += 1

            actor_loss = None
            if self._critic_update_count % self.hparams.policy_delay == 0:
                actor_loss = self._update_actor(b, actor_opt)
                self._soft_update_targets()

        # ---- 4. Logging -----------------------------------------------
        self.log("train/critic_loss", critic_loss, prog_bar=False, on_step=True)
        if actor_loss is not None:
            self.log("train/actor_loss", actor_loss, prog_bar=False, on_step=True)
        self.log("train/total_env_steps", float(self._total_env_steps), prog_bar=True)
        if dm.episode_rewards:
            self.log("train/episode_reward", dm.episode_rewards[-1], prog_bar=True)
            self.log("train/episode_length", float(dm.episode_lengths[-1]))

    # ------------------------------------------------------------------
    # TD3 algorithm
    # ------------------------------------------------------------------

    def _update_critic(self, b: Batch, critic_opt: torch.optim.Optimizer) -> torch.Tensor:
        """Twin-critic update with target policy smoothing.

        Bellman target::

            ã = clip(tanh(π_target(s')) + clip(ε, -c, c), lo, hi)
            y = r + γ(1-done) · min(Q₁_target, Q₂_target)(s', ã)
        """
        with torch.no_grad():
            noise = (
                torch.randn_like(b.action) * self.hparams.target_noise
            ).clamp(-self.hparams.target_noise_clip, self.hparams.target_noise_clip)
            lo = self._action_bias - self._action_scale
            hi = self._action_bias + self._action_scale
            next_action = (
                torch.tanh(self.actor_target(b.next_obs)) * self._action_scale + self._action_bias + noise
            ).clamp(lo, hi)

            q1_t, q2_t = self.critic_target(b.next_obs, next_action)
            backup = b.reward + self.hparams.gamma * (1.0 - b.done) * torch.min(q1_t, q2_t).squeeze(-1)

        q1, q2 = self.critic(b.obs, b.action)
        critic_loss = F.mse_loss(q1.squeeze(-1), backup) + F.mse_loss(q2.squeeze(-1), backup)

        critic_opt.zero_grad()
        self.manual_backward(critic_loss)
        critic_opt.step()
        return critic_loss

    def _update_actor(self, b: Batch, actor_opt: torch.optim.Optimizer) -> torch.Tensor:
        """Deterministic policy gradient.

        Actor objective::

            min_θ  -Q₁(s, tanh(π_θ(s)) · scale + bias)

        Only Q₁ is used (not the min) to avoid pessimism in the actor objective.
        """
        action = torch.tanh(self.actor(b.obs)) * self._action_scale + self._action_bias
        q1, _ = self.critic(b.obs, action)
        actor_loss = -q1.mean()

        actor_opt.zero_grad()
        self.manual_backward(actor_loss)
        actor_opt.step()
        return actor_loss

    def act_deterministic(self, obs: torch.Tensor) -> torch.Tensor:
        """Deterministic action for callbacks and evaluation."""
        return torch.tanh(self.actor(obs)) * self._action_scale + self._action_bias

    def _soft_update_targets(self) -> None:
        tau = self.hparams.tau
        for online, target in zip(self.actor.parameters(), self.actor_target.parameters()):
            target.data.mul_(1.0 - tau).add_(online.data, alpha=tau)
        for online, target in zip(self.critic.parameters(), self.critic_target.parameters()):
            target.data.mul_(1.0 - tau).add_(online.data, alpha=tau)
