"""Proximal Policy Optimization (PPO) and RPO as a PyTorch Lightning module.

PPO collects on-policy rollouts from a vectorized environment, computes
Generalized Advantage Estimation (GAE), and runs multiple epochs of
minibatch gradient updates per collected batch.

RPO (Robust Policy Optimization) is identical to PPO for continuous actions
but adds a uniform perturbation to the action mean when computing log-probs
during the gradient update, improving robustness. Enable it by setting
``rpo_alpha > 0`` in the agent config.

Ported from CleanRL (https://github.com/vwxyzjn/cleanrl).
"""

from __future__ import annotations

from functools import partial
from typing import Any

import torch
import torch.nn as nn
import lightning as L
from torch.optim import Adam


class PPOModule(L.LightningModule):
    """PPO/RPO LightningModule.

    The training loop here is unconventional: the ``RolloutDataModule``
    returns a dummy single-item dataloader so Lightning fires
    ``training_step`` once per epoch.  That single call owns the entire
    PPO round: collect rollouts → GAE → update_epochs × minibatches.

    Args:
        agent: PPOAgentDiscrete or PPOAgentContinuous instance.
        num_steps: Rollout length per environment per PPO update.
        num_envs: Number of parallel environments (must match RolloutDataModule).
        gamma: Discount factor.
        gae_lambda: GAE lambda for advantage estimation.
        num_minibatches: Number of minibatches per update epoch.
        update_epochs: Number of gradient epochs per PPO update.
        clip_coef: PPO clipping coefficient ε.
        ent_coef: Entropy bonus coefficient.
        vf_coef: Value-function loss coefficient.
        max_grad_norm: Gradient clipping max norm.
        norm_adv: Whether to normalise advantages per minibatch.
        clip_vloss: Whether to apply clipped value loss (as in CleanRL).
        target_kl: Early-stop update epoch if approx KL exceeds this.
        anneal_lr: Linearly decay learning rate to 0 over total_timesteps.
        total_timesteps: Used only when anneal_lr=True.
        optimizer: Partial optimizer factory (default Adam lr=3e-4, eps=1e-5).
    """

    automatic_optimization = False

    def __init__(
        self,
        agent: nn.Module,
        num_steps: int = 2048,
        num_envs: int = 1,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        num_minibatches: int = 32,
        update_epochs: int = 10,
        clip_coef: float = 0.2,
        ent_coef: float = 0.0,
        vf_coef: float = 0.5,
        max_grad_norm: float = 0.5,
        norm_adv: bool = True,
        clip_vloss: bool = True,
        target_kl: float | None = None,
        anneal_lr: bool = True,
        total_timesteps: int = 1_000_000,
        optimizer=None,
    ) -> None:
        super().__init__()
        self.automatic_optimization = False
        self.save_hyperparameters(logger=False, ignore=["agent"])
        self.agent = agent

        _opt = optimizer or partial(Adam, lr=3e-4, eps=1e-5)
        self.hparams.optimizer = _opt
        self._init_lr: float = getattr(_opt, "keywords", {}).get("lr", 3e-4)

        # Rollout buffers — allocated in setup() once we know the shapes
        self._obs: torch.Tensor | None = None
        self._actions: torch.Tensor | None = None
        self._log_probs: torch.Tensor | None = None
        self._rewards: torch.Tensor | None = None
        self._dones: torch.Tensor | None = None
        self._values: torch.Tensor | None = None
        self._next_obs: torch.Tensor | None = None
        self._next_done: torch.Tensor | None = None

        self._global_step: int = 0

    # ------------------------------------------------------------------
    # Lightning lifecycle
    # ------------------------------------------------------------------

    def setup(self, stage: str) -> None:
        if stage != "fit":
            return
        dm = self.trainer.datamodule
        obs_shape = dm.obs_shape
        act_shape = dm.act_shape
        n = self.hparams.num_steps
        e = self.hparams.num_envs

        # Rollout buffers live on CPU during collection; moved to device once before GAE.
        # This avoids num_steps × num_envs tiny GPU slice assignments and lets the GPU
        # run a clean uninterrupted block during GAE + update epochs.
        self._obs = torch.zeros(n, e, *obs_shape)
        self._actions = torch.zeros(n, e, *act_shape)
        self._log_probs = torch.zeros(n, e)
        self._rewards = torch.zeros(n, e)
        self._dones = torch.zeros(n, e)
        self._values = torch.zeros(n, e)

        obs_np, _ = dm.envs.reset()
        self._next_obs = torch.from_numpy(obs_np.astype("float32")).to(self.device)
        self._next_done = torch.zeros(e, device=self.device)

    def configure_optimizers(self) -> list[torch.optim.Optimizer]:
        return [self.hparams.optimizer(self.agent.parameters())]

    # ------------------------------------------------------------------
    # Training step — orchestrates one full PPO round
    # ------------------------------------------------------------------

    def training_step(self, batch: Any, batch_idx: int) -> None:  # noqa: ARG002
        opt = self.optimizers()
        dm = self.trainer.datamodule

        ep_rewards, ep_lengths = self._collect_rollout(dm.envs)
        dm.episode_rewards.extend(ep_rewards)
        dm.episode_lengths.extend(ep_lengths)

        flat = self._compute_gae()
        metrics = self._run_update_epochs(opt, flat)
        self._anneal_lr(opt)
        self._log_metrics(metrics, dm)

    # ------------------------------------------------------------------
    # PPO phases
    # ------------------------------------------------------------------

    def _collect_rollout(
        self, envs
    ) -> tuple[list[float], list[int]]:
        """Collect num_steps transitions from envs into the rollout buffers.

        Returns lists of completed episode (rewards, lengths) observed during
        this rollout so the caller can append them to the datamodule's tracking
        lists.

        Takes ``envs`` explicitly rather than reaching into the datamodule so
        that this method can be unit-tested with a mock environment.
        """
        hp = self.hparams
        ep_rewards: list[float] = []
        ep_lengths: list[int] = []

        self.agent.eval()
        with torch.no_grad():
            for step in range(hp.num_steps):
                # Store to CPU buffers — one batch GPU transfer happens before GAE
                self._obs[step] = self._next_obs.cpu()
                self._dones[step] = self._next_done.cpu()

                action, log_prob, _, value = self.agent.get_action_and_value(self._next_obs)
                self._actions[step] = action.cpu()
                self._log_probs[step] = log_prob.cpu()
                self._values[step] = value.squeeze(-1).cpu()

                action_np = action.cpu().numpy()
                obs_np, reward_np, term_np, trunc_np, infos = envs.step(action_np)
                # from_numpy avoids a data copy; astype ensures float32 contiguity
                self._rewards[step] = torch.from_numpy(reward_np.astype("float32"))
                done_np = (term_np | trunc_np).astype("float32")
                self._next_obs = torch.from_numpy(obs_np.astype("float32")).to(self.device)
                self._next_done = torch.from_numpy(done_np).to(self.device)

                self._global_step += hp.num_envs

                if "final_info" in infos:
                    for info in infos["final_info"]:
                        if info is not None and "episode" in info:
                            ep_rewards.append(float(info["episode"]["r"]))
                            ep_lengths.append(int(info["episode"]["l"]))

        return ep_rewards, ep_lengths

    def _compute_gae(self) -> dict[str, torch.Tensor]:
        """Compute GAE advantages and returns; flatten buffers to (T*N, ...).

        Global backward pass over the full (T, N) rollout — not per-episode.
        Returns a flat dict of tensors ready for minibatch sampling.
        """
        hp = self.hparams
        dev = self.device

        # Single batch transfer from CPU rollout buffers → device.
        # All subsequent GAE and update-epoch work stays on device.
        rewards = self._rewards.to(dev)
        dones = self._dones.to(dev)
        values = self._values.to(dev)

        with torch.no_grad():
            next_value = self.agent.get_value(self._next_obs).squeeze(-1)
            advantages = torch.zeros_like(rewards)
            last_gae = 0.0
            for t in reversed(range(hp.num_steps)):
                if t == hp.num_steps - 1:
                    next_non_terminal = 1.0 - self._next_done.float()
                    next_vals = next_value
                else:
                    next_non_terminal = 1.0 - dones[t + 1].float()
                    next_vals = values[t + 1]
                delta = rewards[t] + hp.gamma * next_vals * next_non_terminal - values[t]
                last_gae = delta + hp.gamma * hp.gae_lambda * next_non_terminal * last_gae
                advantages[t] = last_gae
            returns = advantages + values

        batch_size = hp.num_steps * hp.num_envs
        obs_d = self._obs.to(dev)
        return {
            "obs": obs_d.reshape(batch_size, *obs_d.shape[2:]),
            "actions": self._actions.to(dev).reshape(batch_size, *self._actions.shape[2:]),
            "log_probs": self._log_probs.to(dev).reshape(batch_size),
            "advantages": advantages.reshape(batch_size),
            "returns": returns.reshape(batch_size),
            "values": values.reshape(batch_size),
        }

    def _run_update_epochs(
        self, opt, flat: dict[str, torch.Tensor]
    ) -> dict[str, Any]:
        """Run update_epochs × num_minibatches gradient updates.

        Returns a metrics dict with the last values of pg_loss, vf_loss,
        entropy, approx_kl, clip_frac, and explained_variance.
        """
        hp = self.hparams
        b_obs = flat["obs"]
        b_actions = flat["actions"]
        b_log_probs = flat["log_probs"]
        b_advantages = flat["advantages"]
        b_returns = flat["returns"]
        b_values = flat["values"]

        batch_size = b_obs.shape[0]
        minibatch_size = batch_size // hp.num_minibatches
        b_inds = torch.arange(batch_size, device=self.device)
        clip_fracs: list[float] = []
        # Initialise to avoid "possibly unbound" errors when update_epochs=0
        pg_loss = vf_loss = entropy_loss = approx_kl = torch.zeros(1, device=self.device)

        self.agent.train()
        for _ in range(hp.update_epochs):
            shuffled = b_inds[torch.randperm(batch_size, device=self.device)]
            for start in range(0, batch_size, minibatch_size):
                mb_inds = shuffled[start: start + minibatch_size]

                mb_obs = b_obs[mb_inds]
                mb_act = b_actions[mb_inds]
                mb_adv = b_advantages[mb_inds]
                mb_ret = b_returns[mb_inds]
                mb_val = b_values[mb_inds]
                mb_old_lp = b_log_probs[mb_inds]

                # Discrete actions arrive as (B, 1) — squeeze for distribution
                if mb_act.ndim > 1 and mb_act.shape[-1] == 1:
                    mb_act = mb_act.squeeze(-1)

                _, new_log_prob, entropy, new_value = self.agent.get_action_and_value(
                    mb_obs, mb_act
                )
                new_value = new_value.squeeze(-1)

                log_ratio = new_log_prob - mb_old_lp
                ratio = log_ratio.exp()

                with torch.no_grad():
                    approx_kl = ((ratio - 1) - log_ratio).mean()
                    clip_fracs.append(
                        ((ratio - 1.0).abs() > hp.clip_coef).float().mean().item()
                    )

                adv = mb_adv
                if hp.norm_adv:
                    adv = (adv - adv.mean()) / (adv.std() + 1e-8)

                pg_loss1 = -adv * ratio
                pg_loss2 = -adv * ratio.clamp(1 - hp.clip_coef, 1 + hp.clip_coef)
                pg_loss = torch.max(pg_loss1, pg_loss2).mean()

                if hp.clip_vloss:
                    v_clipped = mb_val + (new_value - mb_val).clamp(-hp.clip_coef, hp.clip_coef)
                    vf_loss = 0.5 * torch.max(
                        (new_value - mb_ret) ** 2,
                        (v_clipped - mb_ret) ** 2,
                    ).mean()
                else:
                    vf_loss = 0.5 * ((new_value - mb_ret) ** 2).mean()

                entropy_loss = entropy.mean()
                loss = pg_loss - hp.ent_coef * entropy_loss + hp.vf_coef * vf_loss

                opt.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.agent.parameters(), hp.max_grad_norm)
                opt.step()

            if hp.target_kl is not None and approx_kl > hp.target_kl:
                break

        with torch.no_grad():
            y_pred = b_values.cpu().numpy()
            y_true = b_returns.cpu().numpy()
            var_y = float(y_true.var())
            explained_var = float("nan") if var_y == 0 else 1.0 - float((y_true - y_pred).var()) / var_y

        return {
            "pg_loss": pg_loss,
            "vf_loss": vf_loss,
            "entropy": entropy_loss,
            "approx_kl": approx_kl,
            "clip_frac": float(sum(clip_fracs) / len(clip_fracs)) if clip_fracs else 0.0,
            "explained_variance": explained_var,
        }

    def _anneal_lr(self, opt) -> None:
        if self.hparams.anneal_lr:
            frac = 1.0 - self._global_step / self.hparams.total_timesteps
            for pg in opt.param_groups:
                pg["lr"] = frac * self._init_lr

    def _log_metrics(self, metrics: dict[str, Any], dm) -> None:
        self.log("train/policy_loss", metrics["pg_loss"], prog_bar=False, on_step=False, on_epoch=True)
        self.log("train/value_loss", metrics["vf_loss"], prog_bar=False, on_step=False, on_epoch=True)
        self.log("train/entropy", metrics["entropy"], prog_bar=False, on_step=False, on_epoch=True)
        self.log("train/approx_kl", metrics["approx_kl"], prog_bar=False, on_step=False, on_epoch=True)
        self.log("train/clip_frac", metrics["clip_frac"], on_step=False, on_epoch=True)
        self.log("train/explained_variance", metrics["explained_variance"], on_step=False, on_epoch=True)
        self.log("train/global_step", float(self._global_step), prog_bar=True, on_step=False, on_epoch=True)

        if dm.episode_rewards:
            self.log("train/episode_reward", dm.episode_rewards[-1], prog_bar=True, on_epoch=True)
            self.log("train/episode_length", float(dm.episode_lengths[-1]), on_epoch=True)

    # ------------------------------------------------------------------
    # Unified eval interface for callbacks
    # ------------------------------------------------------------------

    def act_deterministic(self, obs: torch.Tensor) -> torch.Tensor:
        """Return deterministic action for callbacks and evaluation."""
        return self.agent.act_deterministic(obs)
