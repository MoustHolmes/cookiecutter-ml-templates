"""Soft Actor-Critic (SAC) implemented as a PyTorch Lightning module.

SAC is an off-policy, maximum-entropy actor-critic algorithm for continuous
action spaces.  It jointly maximises expected cumulative reward *and* policy
entropy, which encourages exploration and prevents premature convergence.

Key algorithmic features implemented here:

- **Twin critics** — two independent Q-networks; Bellman targets use their
  minimum to suppress overestimation bias (Clipped Double-Q Learning).
- **Reparameterization trick** — actions are sampled as ``tanh(μ + σε)``
  with a correction term in the log-prob for the tanh squashing.
- **Automatic temperature tuning** — the entropy coefficient ``α`` is adapted
  online via dual gradient descent to match a target entropy.
- **Polyak averaging** — a frozen target critic tracks the online critic.

Lightning integration notes:

- ``automatic_optimization = False`` — three optimizers (critic, actor, alpha)
  are managed manually so that their update order can be controlled.
- The dataloader is driven by :class:`~{{cookiecutter.repo_name}}.data.env_datamodule.RLDataModule`.
  Each ``training_step`` first collects new environment experience, then
  performs gradient updates.
"""

from __future__ import annotations

import copy
from functools import partial

import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as L
from torch.optim import Adam

from {{cookiecutter.repo_name}}.data.replay_buffer import Batch


class SACModule(L.LightningModule):
    """Soft Actor-Critic (SAC) LightningModule.

    Args:
        actor: :class:`~{{cookiecutter.repo_name}}.models.actor.StochasticActor` — backbone + mean/log-std heads.
        critic: :class:`~{{cookiecutter.repo_name}}.models.critic.TwinCritic` — two Q-networks.
        action_scale: ``(high - low) / 2`` for the action space (from env config).
        action_bias: ``(high + low) / 2`` for the action space (from env config).
        log_std_min: Lower clamp for log std during action sampling.
        log_std_max: Upper clamp for log std during action sampling.
        gamma: Discount factor.
        tau: Polyak averaging coefficient for the target critic.
        batch_size: Mini-batch size for gradient updates.
        learning_starts: Random-action warm-up steps before first update.
        collect_steps_per_update: Environment steps per ``training_step`` call.
        gradient_steps: Gradient update iterations per ``training_step`` call.
        init_alpha: Initial temperature value.
        target_entropy: Target entropy for auto-tuning. ``None`` → ``-action_dim``.
        actor_optimizer: Partial optimizer factory for the actor.
        critic_optimizer: Partial optimizer factory for the critic.
        alpha_optimizer: Partial optimizer factory for ``log_alpha``.
    """

    def __init__(
        self,
        actor: nn.Module,
        critic: nn.Module,
        action_scale: float = 1.0,
        action_bias: float = 0.0,
        log_std_min: float = -5.0,
        log_std_max: float = 2.0,
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
        self.automatic_optimization = False
        self.save_hyperparameters(logger=False, ignore=["actor", "critic"])

        self.actor = actor
        self.critic = critic
        self.critic_target = copy.deepcopy(critic)
        for p in self.critic_target.parameters():
            p.requires_grad = False

        self.log_alpha = nn.Parameter(torch.tensor(float(init_alpha)).log())

        # Environment action space scaling (from env config, not model architecture)
        self.register_buffer("_action_scale", torch.tensor(action_scale, dtype=torch.float32))
        self.register_buffer("_action_bias", torch.tensor(action_bias, dtype=torch.float32))

        self.hparams.actor_optimizer = actor_optimizer or partial(Adam, lr=3e-4)
        self.hparams.critic_optimizer = critic_optimizer or partial(Adam, lr=3e-4)
        self.hparams.alpha_optimizer = alpha_optimizer or partial(Adam, lr=3e-4)

        self._total_env_steps: int = 0

    @property
    def alpha(self) -> torch.Tensor:
        return self.log_alpha.exp()

    # ------------------------------------------------------------------
    # Lightning lifecycle
    # ------------------------------------------------------------------

    def setup(self, stage: str) -> None:
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
        critic_opt = self.hparams.critic_optimizer(self.critic.parameters())
        actor_opt = self.hparams.actor_optimizer(self.actor.parameters())
        alpha_opt = self.hparams.alpha_optimizer([self.log_alpha])
        return [critic_opt, actor_opt, alpha_opt]

    # ------------------------------------------------------------------
    # Training step
    # ------------------------------------------------------------------

    def training_step(self, batch: Batch, batch_idx: int) -> None:  # noqa: ARG002
        critic_opt, actor_opt, alpha_opt = self.optimizers()
        dm = self.trainer.datamodule

        # ---- 1. Collect experience -------------------------------------
        if self._total_env_steps < self.hparams.learning_starts:
            policy_fn = None
        else:
            def policy_fn(obs: torch.Tensor) -> torch.Tensor:
                action, _, _ = self._sample_action(obs.to(self.device))
                return action

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
            actor_loss, alpha_loss = self._update_actor_and_alpha(b, actor_opt, alpha_opt)

        # ---- 4. Soft-update target critic -----------------------------
        self._soft_update_target()

        # ---- 5. Logging -----------------------------------------------
        self.log("train/critic_loss", critic_loss, prog_bar=False, on_step=True)
        self.log("train/actor_loss", actor_loss, prog_bar=False, on_step=True)
        self.log("train/alpha_loss", alpha_loss, prog_bar=False, on_step=True)
        self.log("train/alpha", self.alpha.item(), prog_bar=True, on_step=True)
        self.log("train/total_env_steps", float(self._total_env_steps), prog_bar=True)
        if dm.episode_rewards:
            self.log("train/episode_reward", dm.episode_rewards[-1], prog_bar=True)
            self.log("train/episode_length", float(dm.episode_lengths[-1]))

    # ------------------------------------------------------------------
    # SAC algorithm
    # ------------------------------------------------------------------

    def _sample_action(
        self, obs: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Reparameterized action sample with tanh squashing and log-prob.

        SAC action sampling::

            mean, log_std = actor(obs)
            z = mean + std * ε,   ε ~ N(0, I)
            action = tanh(z) * scale + bias

        Log-prob under the squashed Gaussian (tanh correction)::

            log π(a|s) = Σ [log N(z; mean, std) - log(scale · (1 - tanh²(z)))]

        Returns:
            ``(action, log_prob, mean_action)``
        """
        mean, log_std = self.actor(obs)
        log_std = log_std.clamp(self.hparams.log_std_min, self.hparams.log_std_max)
        std = log_std.exp()

        eps = torch.randn_like(mean)
        z = mean + std * eps

        action = torch.tanh(z) * self._action_scale + self._action_bias

        log_prob_gaussian = -0.5 * (((z - mean) / (std + 1e-8)) ** 2 + 2 * log_std + 1.8378770664)
        log_det = (torch.log(self._action_scale) + torch.log(1.0 - torch.tanh(z) ** 2 + 1e-7)).sum(dim=-1)
        log_prob = log_prob_gaussian.sum(dim=-1) - log_det

        mean_action = torch.tanh(mean) * self._action_scale + self._action_bias
        return action, log_prob, mean_action

    def _update_critic(self, b: Batch, critic_opt: torch.optim.Optimizer) -> torch.Tensor:
        """Twin-critic Bellman update.

        Target::

            y = r + γ(1-done) · [min(Q₁_target, Q₂_target)(s', a') - α · log π(a'|s')]
        """
        with torch.no_grad():
            next_action, next_log_prob, _ = self._sample_action(b.next_obs)
            q1_t, q2_t = self.critic_target(b.next_obs, next_action)
            q_target = torch.min(q1_t, q2_t).squeeze(-1)
            backup = b.reward + self.hparams.gamma * (1.0 - b.done) * (
                q_target - self.alpha.detach() * next_log_prob
            )

        q1, q2 = self.critic(b.obs, b.action)
        critic_loss = F.mse_loss(q1.squeeze(-1), backup) + F.mse_loss(q2.squeeze(-1), backup)

        critic_opt.zero_grad()
        self.manual_backward(critic_loss)
        critic_opt.step()
        return critic_loss

    def _update_actor_and_alpha(
        self,
        b: Batch,
        actor_opt: torch.optim.Optimizer,
        alpha_opt: torch.optim.Optimizer,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Actor and temperature update.

        Actor objective::

            min_θ  α · log π(a|s) - min(Q₁, Q₂)(s, a)

        Temperature (dual gradient descent)::

            min_α  -α · (log π(a|s) + H_target)
        """
        action, log_prob, _ = self._sample_action(b.obs)
        q1, q2 = self.critic(b.obs, action)
        q_value = torch.min(q1, q2).squeeze(-1)

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
        """Deterministic (mean) action for callbacks and evaluation."""
        mean, _ = self.actor(obs)
        return torch.tanh(mean) * self._action_scale + self._action_bias

    def _soft_update_target(self) -> None:
        tau = self.hparams.tau
        for online, target in zip(self.critic.parameters(), self.critic_target.parameters()):
            target.data.mul_(1.0 - tau).add_(online.data, alpha=tau)
