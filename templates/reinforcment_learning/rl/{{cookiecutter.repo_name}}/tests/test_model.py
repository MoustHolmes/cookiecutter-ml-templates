"""Unit tests for all model and module classes in the RL template."""

from __future__ import annotations

import torch

from {{cookiecutter.repo_name}}.models.mlp import MLP
from {{cookiecutter.repo_name}}.models.actor import DeterministicActor, StochasticActor
from {{cookiecutter.repo_name}}.models.critic import TwinCritic
from {{cookiecutter.repo_name}}.sac_module import SACModule
from {{cookiecutter.repo_name}}.td3_module import TD3Module
from {{cookiecutter.repo_name}}.ppo_module import PPOModule
from {{cookiecutter.repo_name}}.dqn_module import DQNModule

BATCH = 16
OBS_DIM = 3         # Pendulum-v1
ACTION_DIM = 1      # Pendulum-v1
CARTPOLE_OBS = 4
CARTPOLE_ACT = 2


# ---------------------------------------------------------------------------
# MLP (shared backbone)
# ---------------------------------------------------------------------------

class TestMLP:
    def test_output_shape(self) -> None:
        net = MLP(input_dim=8, output_dim=4, hidden_dim=64, num_layers=2)
        assert net(torch.randn(BATCH, 8)).shape == (BATCH, 4)

    def test_orthogonal_init(self) -> None:
        net = MLP(4, 2, hidden_dim=32, num_layers=2, orthogonal_init=True)
        assert net(torch.randn(BATCH, 4)).shape == (BATCH, 2)

    def test_tanh_activation(self) -> None:
        net = MLP(4, 2, hidden_dim=32, num_layers=2, activation="tanh")
        assert net(torch.randn(BATCH, 4)).shape == (BATCH, 2)


# ---------------------------------------------------------------------------
# StochasticActor (SAC) — forward() returns (mean, log_std) only
# ---------------------------------------------------------------------------

class TestStochasticActor:
    def test_forward_shapes(self, stochastic_actor: StochasticActor) -> None:
        """forward() returns raw (mean, log_std) — no squashing, no log-prob."""
        obs = torch.randn(BATCH, OBS_DIM)
        mean, log_std = stochastic_actor(obs)
        assert mean.shape == (BATCH, ACTION_DIM)
        assert log_std.shape == (BATCH, ACTION_DIM)

    def test_stochastic_via_module(self, sac_module: SACModule) -> None:
        """_sample_action() on SACModule produces different actions each call."""
        obs = torch.randn(BATCH, OBS_DIM)
        a1, _, _ = sac_module._sample_action(obs)
        a2, _, _ = sac_module._sample_action(obs)
        assert not torch.allclose(a1, a2)


# ---------------------------------------------------------------------------
# DeterministicActor (TD3) — thin MLP subclass, output is pre-tanh
# ---------------------------------------------------------------------------

class TestDeterministicActor:
    def test_output_shape(self, deterministic_actor: DeterministicActor) -> None:
        obs = torch.randn(BATCH, OBS_DIM)
        assert deterministic_actor(obs).shape == (BATCH, ACTION_DIM)

    def test_deterministic(self, deterministic_actor: DeterministicActor) -> None:
        deterministic_actor.eval()
        obs = torch.randn(BATCH, OBS_DIM)
        with torch.no_grad():
            assert torch.allclose(deterministic_actor(obs), deterministic_actor(obs))


# ---------------------------------------------------------------------------
# TwinCritic — forward() returns (q1, q2); no min_q method
# ---------------------------------------------------------------------------

class TestTwinCritic:
    def test_output_shapes(self, twin_critic: TwinCritic) -> None:
        obs = torch.randn(BATCH, OBS_DIM)
        action = torch.randn(BATCH, ACTION_DIM)
        q1, q2 = twin_critic(obs, action)
        assert q1.shape == (BATCH, 1)
        assert q2.shape == (BATCH, 1)

    def test_independent_networks(self, twin_critic: TwinCritic) -> None:
        obs = torch.randn(BATCH, OBS_DIM)
        action = torch.randn(BATCH, ACTION_DIM)
        q1, q2 = twin_critic(obs, action)
        assert not torch.allclose(q1, q2)


# ---------------------------------------------------------------------------
# SACModule — reparameterization + tanh + log-prob live here
# ---------------------------------------------------------------------------

class TestSACModule:
    def test_automatic_optimization_disabled(self, sac_module: SACModule) -> None:
        assert sac_module.automatic_optimization is False

    def test_alpha_positive(self, sac_module: SACModule) -> None:
        assert sac_module.alpha.item() > 0

    def test_configure_optimizers_returns_three(self, sac_module: SACModule) -> None:
        opts = sac_module.configure_optimizers()
        assert len(opts) == 3
        for opt in opts:
            assert isinstance(opt, torch.optim.Optimizer)

    def test_sample_action_shapes(self, sac_module: SACModule) -> None:
        obs = torch.randn(BATCH, OBS_DIM)
        action, log_prob, mean = sac_module._sample_action(obs)
        assert action.shape == (BATCH, ACTION_DIM)
        assert log_prob.shape == (BATCH,)
        assert mean.shape == (BATCH, ACTION_DIM)

    def test_sample_action_bounded(self, sac_module: SACModule) -> None:
        """tanh * action_scale=2.0 → actions strictly within (-2, 2)."""
        obs = torch.randn(128, OBS_DIM)
        action, _, _ = sac_module._sample_action(obs)
        assert action.abs().max().item() < 2.0

    def test_log_prob_finite(self, sac_module: SACModule) -> None:
        obs = torch.randn(256, OBS_DIM)
        _, log_prob, _ = sac_module._sample_action(obs)
        assert torch.isfinite(log_prob).all()

    def test_sample_action_stochastic(self, sac_module: SACModule) -> None:
        obs = torch.randn(BATCH, OBS_DIM)
        a1, _, _ = sac_module._sample_action(obs)
        a2, _, _ = sac_module._sample_action(obs)
        assert not torch.allclose(a1, a2)

    def test_act_deterministic_shape(self, sac_module: SACModule) -> None:
        obs = torch.randn(BATCH, OBS_DIM)
        assert sac_module.act_deterministic(obs).shape == (BATCH, ACTION_DIM)

    def test_soft_update_does_not_fully_match(self, sac_module: SACModule) -> None:
        for p in sac_module.critic.parameters():
            p.data += 1.0
        sac_module._soft_update_target()
        for online, target in zip(
            sac_module.critic.parameters(), sac_module.critic_target.parameters()
        ):
            assert not torch.allclose(online, target)

    def test_target_critic_frozen(self, sac_module: SACModule) -> None:
        for p in sac_module.critic_target.parameters():
            assert not p.requires_grad


# ---------------------------------------------------------------------------
# TD3Module — tanh squashing and action rescaling live here
# ---------------------------------------------------------------------------

class TestTD3Module:
    def test_automatic_optimization_disabled(self, td3_module: TD3Module) -> None:
        assert td3_module.automatic_optimization is False

    def test_configure_optimizers_returns_two(self, td3_module: TD3Module) -> None:
        assert len(td3_module.configure_optimizers()) == 2

    def test_act_deterministic_shape(self, td3_module: TD3Module) -> None:
        assert td3_module.act_deterministic(torch.randn(BATCH, OBS_DIM)).shape == (BATCH, ACTION_DIM)

    def test_act_deterministic_bounded(self, td3_module: TD3Module) -> None:
        """tanh * action_scale=2.0 → strictly within (-2, 2)."""
        action = td3_module.act_deterministic(torch.randn(128, OBS_DIM))
        assert action.abs().max().item() < 2.0

    def test_target_networks_frozen(self, td3_module: TD3Module) -> None:
        for p in td3_module.actor_target.parameters():
            assert not p.requires_grad
        for p in td3_module.critic_target.parameters():
            assert not p.requires_grad

    def test_soft_update_targets(self, td3_module: TD3Module) -> None:
        for p in list(td3_module.actor.parameters()) + list(td3_module.critic.parameters()):
            p.data += 1.0
        td3_module._soft_update_targets()
        for online, target in zip(
            td3_module.actor.parameters(), td3_module.actor_target.parameters()
        ):
            assert not torch.allclose(online, target)


# ---------------------------------------------------------------------------
# PPOModule — _get_action_and_value() and distributions live here
# ---------------------------------------------------------------------------

class TestPPOModule:
    def test_automatic_optimization_disabled(self, ppo_module_bare: PPOModule) -> None:
        assert ppo_module_bare.automatic_optimization is False

    def test_configure_optimizers_returns_one(self, ppo_module_bare: PPOModule) -> None:
        opts = ppo_module_bare.configure_optimizers()
        assert len(opts) == 1
        assert isinstance(opts[0], torch.optim.Optimizer)

    def test_get_action_and_value_shapes(self, ppo_module_bare: PPOModule) -> None:
        obs = torch.randn(BATCH, CARTPOLE_OBS)
        action, log_prob, entropy, value = ppo_module_bare._get_action_and_value(obs)
        assert action.shape == (BATCH,)
        assert log_prob.shape == (BATCH,)
        assert entropy.shape == (BATCH,)
        assert value.shape == (BATCH, 1)

    def test_evaluate_given_action(self, ppo_module_bare: PPOModule) -> None:
        obs = torch.randn(BATCH, CARTPOLE_OBS)
        given_action = torch.zeros(BATCH, dtype=torch.long)
        _, log_prob, entropy, _ = ppo_module_bare._get_action_and_value(obs, given_action)
        assert log_prob.shape == (BATCH,)
        assert entropy.shape == (BATCH,)

    def test_get_value_shape(self, ppo_module_bare: PPOModule) -> None:
        assert ppo_module_bare._get_value(torch.randn(BATCH, CARTPOLE_OBS)).shape == (BATCH, 1)

    def test_log_prob_finite(self, ppo_module_bare: PPOModule) -> None:
        _, log_prob, _, _ = ppo_module_bare._get_action_and_value(torch.randn(BATCH, CARTPOLE_OBS))
        assert torch.isfinite(log_prob).all()

    def test_act_deterministic_shape(self, ppo_module_bare: PPOModule) -> None:
        assert ppo_module_bare.act_deterministic(torch.randn(1, CARTPOLE_OBS)).shape == (1,)

    def test_act_deterministic_valid_action(self, ppo_module_bare: PPOModule) -> None:
        action = ppo_module_bare.act_deterministic(torch.randn(BATCH, CARTPOLE_OBS))
        assert (action >= 0).all() and (action < CARTPOLE_ACT).all()

    def test_compute_gae_output_keys(self, ppo_module_bare: PPOModule) -> None:
        flat = ppo_module_bare._compute_gae()
        for key in ("obs", "actions", "log_probs", "advantages", "returns", "values"):
            assert key in flat, f"_compute_gae missing key '{key}'"

    def test_compute_gae_shapes(self, ppo_module_bare: PPOModule) -> None:
        flat = ppo_module_bare._compute_gae()
        batch_size = 16 * 2  # num_steps * num_envs
        assert flat["obs"].shape == (batch_size, CARTPOLE_OBS)
        assert flat["actions"].shape == (batch_size,)
        assert flat["advantages"].shape == (batch_size,)
        assert flat["returns"].shape == (batch_size,)
        assert flat["values"].shape == (batch_size,)

    def test_compute_gae_advantages_finite(self, ppo_module_bare: PPOModule) -> None:
        flat = ppo_module_bare._compute_gae()
        assert torch.isfinite(flat["advantages"]).all()
        assert torch.isfinite(flat["returns"]).all()

    def test_run_update_epochs_metric_keys(self, ppo_module_bare: PPOModule) -> None:
        flat = ppo_module_bare._compute_gae()
        opt = ppo_module_bare.configure_optimizers()[0]
        metrics = ppo_module_bare._run_update_epochs(opt, flat)
        for key in ("pg_loss", "vf_loss", "entropy", "approx_kl", "clip_frac", "explained_variance"):
            assert key in metrics, f"_run_update_epochs missing metric '{key}'"

    def test_run_update_epochs_losses_finite(self, ppo_module_bare: PPOModule) -> None:
        flat = ppo_module_bare._compute_gae()
        opt = ppo_module_bare.configure_optimizers()[0]
        metrics = ppo_module_bare._run_update_epochs(opt, flat)
        assert torch.isfinite(torch.as_tensor(metrics["pg_loss"].item()))
        assert torch.isfinite(torch.as_tensor(metrics["vf_loss"].item()))


# ---------------------------------------------------------------------------
# DQNModule
# ---------------------------------------------------------------------------

class TestDQNModule:
    def test_automatic_optimization_disabled(self, dqn_module: DQNModule) -> None:
        assert dqn_module.automatic_optimization is False

    def test_configure_optimizers_returns_one(self, dqn_module: DQNModule) -> None:
        opts = dqn_module.configure_optimizers()
        assert len(opts) == 1
        assert isinstance(opts[0], torch.optim.Optimizer)

    def test_act_deterministic_shape(self, dqn_module: DQNModule) -> None:
        obs = torch.randn(1, CARTPOLE_OBS)
        action = dqn_module.act_deterministic(obs)
        assert action.shape == (1, 1)   # (B, 1) float for buffer compatibility
