"""Unit tests for all model and module classes in the RL template."""

from __future__ import annotations

import torch
import pytest

from {{cookiecutter.repo_name}}.models.actor import DeterministicActor, StochasticActor
from {{cookiecutter.repo_name}}.models.critic import TwinCritic
from {{cookiecutter.repo_name}}.models.ppo_agent import PPOAgentContinuous, PPOAgentDiscrete
from {{cookiecutter.repo_name}}.models.qnetwork import QNetwork
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
# StochasticActor (SAC)
# ---------------------------------------------------------------------------

class TestStochasticActor:
    def test_output_shapes(self, stochastic_actor: StochasticActor) -> None:
        """get_action() must return (action, log_prob, mean) with correct shapes."""
        obs = torch.randn(BATCH, OBS_DIM)
        action, log_prob, mean = stochastic_actor.get_action(obs)
        assert action.shape == (BATCH, ACTION_DIM)
        assert log_prob.shape == (BATCH,)
        assert mean.shape == (BATCH, ACTION_DIM)

    def test_actions_bounded(self, stochastic_actor: StochasticActor) -> None:
        """tanh squashing must keep all action values strictly within (-1, 1)."""
        obs = torch.randn(128, OBS_DIM)
        action, _, _ = stochastic_actor.get_action(obs)
        assert action.abs().max().item() < 1.0

    def test_log_prob_finite(self, stochastic_actor: StochasticActor) -> None:
        """Log probabilities must be finite — the tanh correction prevents -inf."""
        obs = torch.randn(256, OBS_DIM)
        _, log_prob, _ = stochastic_actor.get_action(obs)
        assert torch.isfinite(log_prob).all(), "log_prob contains non-finite values"

    def test_act_deterministic_bounded(self, stochastic_actor: StochasticActor) -> None:
        """act_deterministic() must return tanh(mean) in (-1, 1)."""
        obs = torch.randn(BATCH, OBS_DIM)
        action = stochastic_actor.act_deterministic(obs)
        assert action.shape == (BATCH, ACTION_DIM)
        assert action.abs().max().item() < 1.0

    def test_stochasticity(self, stochastic_actor: StochasticActor) -> None:
        """Two forward passes on the same obs must produce different actions."""
        obs = torch.randn(BATCH, OBS_DIM)
        a1, _, _ = stochastic_actor.get_action(obs)
        a2, _, _ = stochastic_actor.get_action(obs)
        assert not torch.allclose(a1, a2), "Stochastic actor returned identical actions twice"


# ---------------------------------------------------------------------------
# DeterministicActor (TD3)
# ---------------------------------------------------------------------------

class TestDeterministicActor:
    def test_output_shape(self, deterministic_actor: DeterministicActor) -> None:
        """forward() must return action of shape (B, action_dim)."""
        obs = torch.randn(BATCH, OBS_DIM)
        action = deterministic_actor(obs)
        assert action.shape == (BATCH, ACTION_DIM)

    def test_actions_bounded(self, deterministic_actor: DeterministicActor) -> None:
        """tanh output must be in (-1, 1)."""
        obs = torch.randn(128, OBS_DIM)
        action = deterministic_actor(obs)
        assert action.abs().max().item() < 1.0

    def test_deterministic(self, deterministic_actor: DeterministicActor) -> None:
        """Two forward passes on the same obs must return identical actions."""
        deterministic_actor.eval()
        obs = torch.randn(BATCH, OBS_DIM)
        with torch.no_grad():
            a1 = deterministic_actor(obs)
            a2 = deterministic_actor(obs)
        assert torch.allclose(a1, a2)


# ---------------------------------------------------------------------------
# TwinCritic
# ---------------------------------------------------------------------------

class TestTwinCritic:
    def test_output_shapes(self, twin_critic: TwinCritic) -> None:
        """forward() must return two Q-values each of shape (B, 1)."""
        obs = torch.randn(BATCH, OBS_DIM)
        action = torch.randn(BATCH, ACTION_DIM)
        q1, q2 = twin_critic(obs, action)
        assert q1.shape == (BATCH, 1)
        assert q2.shape == (BATCH, 1)

    def test_min_q_is_elementwise_min(self, twin_critic: TwinCritic) -> None:
        """min_q() must equal element-wise torch.min(q1, q2)."""
        obs = torch.randn(BATCH, OBS_DIM)
        action = torch.randn(BATCH, ACTION_DIM)
        q1, q2 = twin_critic(obs, action)
        min_q = twin_critic.min_q(obs, action)
        assert torch.allclose(min_q, torch.min(q1, q2))

    def test_independent_networks(self, twin_critic: TwinCritic) -> None:
        """The two Q-networks must produce different outputs (they are independent)."""
        obs = torch.randn(BATCH, OBS_DIM)
        action = torch.randn(BATCH, ACTION_DIM)
        q1, q2 = twin_critic(obs, action)
        assert not torch.allclose(q1, q2), "Twin critics produced identical outputs"


# ---------------------------------------------------------------------------
# SACModule
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
# TD3Module
# ---------------------------------------------------------------------------

class TestTD3Module:
    def test_automatic_optimization_disabled(self, td3_module: TD3Module) -> None:
        assert td3_module.automatic_optimization is False

    def test_configure_optimizers_returns_two(self, td3_module: TD3Module) -> None:
        opts = td3_module.configure_optimizers()
        assert len(opts) == 2

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
# PPOAgentDiscrete
# ---------------------------------------------------------------------------

class TestPPOAgentDiscrete:
    def test_get_action_and_value_shapes(self, ppo_agent_discrete: PPOAgentDiscrete) -> None:
        """Sampling: action (B,), log_prob (B,), entropy (B,), value (B, 1)."""
        obs = torch.randn(BATCH, CARTPOLE_OBS)
        action, log_prob, entropy, value = ppo_agent_discrete.get_action_and_value(obs)
        assert action.shape == (BATCH,)
        assert log_prob.shape == (BATCH,)
        assert entropy.shape == (BATCH,)
        assert value.shape == (BATCH, 1)

    def test_evaluate_given_action(self, ppo_agent_discrete: PPOAgentDiscrete) -> None:
        """When action is provided, log_prob/entropy must match that action."""
        obs = torch.randn(BATCH, CARTPOLE_OBS)
        given_action = torch.zeros(BATCH, dtype=torch.long)
        _, log_prob, entropy, value = ppo_agent_discrete.get_action_and_value(obs, given_action)
        assert log_prob.shape == (BATCH,)
        assert entropy.shape == (BATCH,)

    def test_act_deterministic_shape(self, ppo_agent_discrete: PPOAgentDiscrete) -> None:
        """act_deterministic() must return argmax action of shape (B,)."""
        obs = torch.randn(BATCH, CARTPOLE_OBS)
        action = ppo_agent_discrete.act_deterministic(obs)
        assert action.shape == (BATCH,)

    def test_act_deterministic_valid_action(self, ppo_agent_discrete: PPOAgentDiscrete) -> None:
        """Deterministic action must be a valid action index."""
        obs = torch.randn(BATCH, CARTPOLE_OBS)
        action = ppo_agent_discrete.act_deterministic(obs)
        assert (action >= 0).all() and (action < CARTPOLE_ACT).all()

    def test_get_value_shape(self, ppo_agent_discrete: PPOAgentDiscrete) -> None:
        obs = torch.randn(BATCH, CARTPOLE_OBS)
        value = ppo_agent_discrete.get_value(obs)
        assert value.shape == (BATCH, 1)

    def test_log_prob_finite(self, ppo_agent_discrete: PPOAgentDiscrete) -> None:
        obs = torch.randn(BATCH, CARTPOLE_OBS)
        _, log_prob, _, _ = ppo_agent_discrete.get_action_and_value(obs)
        assert torch.isfinite(log_prob).all()


# ---------------------------------------------------------------------------
# PPOAgentContinuous
# ---------------------------------------------------------------------------

class TestPPOAgentContinuous:
    def test_get_action_and_value_shapes(self, ppo_agent_continuous: PPOAgentContinuous) -> None:
        """action (B, action_dim), log_prob (B,), entropy (B,), value (B, 1)."""
        obs = torch.randn(BATCH, OBS_DIM)
        action, log_prob, entropy, value = ppo_agent_continuous.get_action_and_value(obs)
        assert action.shape == (BATCH, ACTION_DIM)
        assert log_prob.shape == (BATCH,)
        assert entropy.shape == (BATCH,)
        assert value.shape == (BATCH, 1)

    def test_evaluate_given_action(self, ppo_agent_continuous: PPOAgentContinuous) -> None:
        obs = torch.randn(BATCH, OBS_DIM)
        given_action = torch.randn(BATCH, ACTION_DIM)
        _, log_prob, entropy, _ = ppo_agent_continuous.get_action_and_value(obs, given_action)
        assert log_prob.shape == (BATCH,)

    def test_rpo_perturbation_is_stochastic(self) -> None:
        """With rpo_alpha > 0, two evaluations of the same action get different log_probs."""
        agent = PPOAgentContinuous(obs_dim=OBS_DIM, action_dim=ACTION_DIM, rpo_alpha=0.5)
        obs = torch.randn(BATCH, OBS_DIM)
        action = torch.randn(BATCH, ACTION_DIM)
        _, lp1, _, _ = agent.get_action_and_value(obs, action)
        _, lp2, _, _ = agent.get_action_and_value(obs, action)
        assert not torch.allclose(lp1, lp2)

    def test_act_deterministic_shape(self, ppo_agent_continuous: PPOAgentContinuous) -> None:
        obs = torch.randn(BATCH, OBS_DIM)
        action = ppo_agent_continuous.act_deterministic(obs)
        assert action.shape == (BATCH, ACTION_DIM)

    def test_get_value_shape(self, ppo_agent_continuous: PPOAgentContinuous) -> None:
        obs = torch.randn(BATCH, OBS_DIM)
        value = ppo_agent_continuous.get_value(obs)
        assert value.shape == (BATCH, 1)


# ---------------------------------------------------------------------------
# QNetwork
# ---------------------------------------------------------------------------

class TestQNetwork:
    def test_output_shape(self, qnetwork: QNetwork) -> None:
        """forward() must return Q-values of shape (B, n_actions)."""
        obs = torch.randn(BATCH, CARTPOLE_OBS)
        q = qnetwork(obs)
        assert q.shape == (BATCH, CARTPOLE_ACT)

    def test_outputs_differ_across_obs(self, qnetwork: QNetwork) -> None:
        """Different observations must produce different Q-value estimates."""
        obs1 = torch.randn(BATCH, CARTPOLE_OBS)
        obs2 = torch.randn(BATCH, CARTPOLE_OBS)
        q1 = qnetwork(obs1)
        q2 = qnetwork(obs2)
        assert not torch.allclose(q1, q2)


# ---------------------------------------------------------------------------
# PPOModule (unit tests using manually-initialised buffers)
# ---------------------------------------------------------------------------

class TestPPOModule:
    def test_automatic_optimization_disabled(self, ppo_module_bare: PPOModule) -> None:
        assert ppo_module_bare.automatic_optimization is False

    def test_configure_optimizers_returns_one(self, ppo_module_bare: PPOModule) -> None:
        opts = ppo_module_bare.configure_optimizers()
        assert len(opts) == 1
        assert isinstance(opts[0], torch.optim.Optimizer)

    def test_compute_gae_output_keys(self, ppo_module_bare: PPOModule) -> None:
        flat = ppo_module_bare._compute_gae()
        for key in ("obs", "actions", "log_probs", "advantages", "returns", "values"):
            assert key in flat, f"_compute_gae missing key '{key}'"

    def test_compute_gae_shapes(self, ppo_module_bare: PPOModule) -> None:
        flat = ppo_module_bare._compute_gae()
        batch_size = 16 * 2  # num_steps * num_envs
        assert flat["obs"].shape == (batch_size, CARTPOLE_OBS)
        assert flat["actions"].shape == (batch_size,)   # discrete: 1-D
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

    def test_act_deterministic_shape(self, ppo_module_bare: PPOModule) -> None:
        obs = torch.randn(1, CARTPOLE_OBS)
        action = ppo_module_bare.act_deterministic(obs)
        assert action.shape == (1,)


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
