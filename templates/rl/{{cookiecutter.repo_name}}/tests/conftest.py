"""Shared pytest fixtures for the RL template test suite."""

from __future__ import annotations

from functools import partial
from pathlib import Path

import pytest
import numpy as np
import torch
from hydra import compose, initialize_config_dir
from hydra.core.global_hydra import GlobalHydra
from omegaconf import DictConfig
from torch.optim import Adam

from {{cookiecutter.repo_name}}.data.replay_buffer import ReplayBuffer
from {{cookiecutter.repo_name}}.data.env_datamodule import RLDataModule
from {{cookiecutter.repo_name}}.data.rollout_datamodule import RolloutDataModule
from {{cookiecutter.repo_name}}.models.mlp import MLP
from {{cookiecutter.repo_name}}.models.actor import DeterministicActor, StochasticActor
from {{cookiecutter.repo_name}}.models.critic import TwinCritic
from {{cookiecutter.repo_name}}.sac_module import SACModule
from {{cookiecutter.repo_name}}.td3_module import TD3Module
from {{cookiecutter.repo_name}}.ppo_module import PPOModule
from {{cookiecutter.repo_name}}.dqn_module import DQNModule

# ---------------------------------------------------------------------------
# Hydra config fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def cfg_train() -> DictConfig:
    """Load the default training configuration (SAC + Pendulum)."""
    GlobalHydra.instance().clear()
    config_dir = str(Path(__file__).parent.parent / "configs")
    with initialize_config_dir(config_dir=config_dir, version_base=None):
        cfg = compose(config_name="train_config", return_hydra_config=True)
    return cfg


@pytest.fixture(scope="function")
def cfg_train_debug() -> DictConfig:
    """Load the training configuration with the debug experiment overrides."""
    GlobalHydra.instance().clear()
    config_dir = str(Path(__file__).parent.parent / "configs")
    with initialize_config_dir(config_dir=config_dir, version_base=None):
        cfg = compose(
            config_name="train_config",
            return_hydra_config=True,
            overrides=["experiment=debug"],
        )
    return cfg


# ---------------------------------------------------------------------------
# Dimensions — all fixtures use these so changes propagate automatically
# ---------------------------------------------------------------------------

PENDULUM_OBS_DIM = 3
PENDULUM_ACTION_DIM = 1
CARTPOLE_OBS_DIM = 4
CARTPOLE_N_ACTIONS = 2

OBS_DIM = PENDULUM_OBS_DIM
ACTION_DIM = PENDULUM_ACTION_DIM


# ---------------------------------------------------------------------------
# Replay buffer fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def small_replay_buffer() -> ReplayBuffer:
    return ReplayBuffer(obs_dim=OBS_DIM, action_dim=ACTION_DIM, buffer_size=1000)


@pytest.fixture()
def filled_replay_buffer() -> ReplayBuffer:
    buf = ReplayBuffer(obs_dim=OBS_DIM, action_dim=ACTION_DIM, buffer_size=1000)
    for _ in range(200):
        buf.add(
            obs=np.random.randn(OBS_DIM).astype(np.float32),
            action=np.random.randn(ACTION_DIM).astype(np.float32),
            reward=float(np.random.randn()),
            next_obs=np.random.randn(OBS_DIM).astype(np.float32),
            terminated=False,
            truncated=False,
        )
    return buf


# ---------------------------------------------------------------------------
# Environment fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def pendulum_datamodule() -> RLDataModule:
    dm = RLDataModule(
        env_id="Pendulum-v1", buffer_size=2000, batch_size=32,
        num_workers=0, seed=0, normalize_obs=False, reward_scale=1.0,
        num_batches_per_epoch=2,
    )
    dm.setup()
    return dm


@pytest.fixture()
def cartpole_rollout_datamodule() -> RolloutDataModule:
    dm = RolloutDataModule(env_id="CartPole-v1", num_envs=2, seed=0)
    dm.setup("fit")
    return dm


# ---------------------------------------------------------------------------
# SAC / TD3 model fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def stochastic_actor() -> StochasticActor:
    return StochasticActor(obs_dim=OBS_DIM, action_dim=ACTION_DIM, hidden_dim=64, num_layers=2)


@pytest.fixture()
def deterministic_actor() -> DeterministicActor:
    return DeterministicActor(obs_dim=OBS_DIM, action_dim=ACTION_DIM, hidden_dim=64, num_layers=2)


@pytest.fixture()
def twin_critic() -> TwinCritic:
    return TwinCritic(obs_dim=OBS_DIM, action_dim=ACTION_DIM, hidden_dim=64, num_layers=2)


@pytest.fixture()
def sac_module(stochastic_actor, twin_critic) -> SACModule:
    return SACModule(
        actor=stochastic_actor,
        critic=twin_critic,
        action_scale=2.0,
        action_bias=0.0,
        gamma=0.99,
        tau=0.005,
        batch_size=32,
        learning_starts=50,
        target_entropy=-1.0,
        actor_optimizer=partial(Adam, lr=3e-4),
        critic_optimizer=partial(Adam, lr=3e-4),
        alpha_optimizer=partial(Adam, lr=3e-4),
    )


@pytest.fixture()
def td3_module(deterministic_actor, twin_critic) -> TD3Module:
    return TD3Module(
        actor=deterministic_actor,
        critic=twin_critic,
        action_scale=2.0,
        action_bias=0.0,
        gamma=0.99,
        tau=0.005,
        batch_size=32,
        learning_starts=50,
        policy_delay=2,
        actor_optimizer=partial(Adam, lr=3e-4),
        critic_optimizer=partial(Adam, lr=3e-4),
    )


# ---------------------------------------------------------------------------
# PPO fixtures
# ---------------------------------------------------------------------------

_PPO_NUM_STEPS = 16
_PPO_NUM_ENVS = 2


@pytest.fixture()
def ppo_actor_discrete() -> MLP:
    return MLP(
        CARTPOLE_OBS_DIM, CARTPOLE_N_ACTIONS, hidden_dim=64, num_layers=2,
        activation="tanh", orthogonal_init=True, output_std=0.01,
    )


@pytest.fixture()
def ppo_critic() -> MLP:
    return MLP(
        CARTPOLE_OBS_DIM, 1, hidden_dim=64, num_layers=2,
        activation="tanh", orthogonal_init=True, output_std=1.0,
    )


@pytest.fixture()
def ppo_module_bare(ppo_actor_discrete, ppo_critic) -> PPOModule:
    """PPOModule with rollout buffers pre-allocated (no Lightning trainer needed)."""
    module = PPOModule(
        actor=ppo_actor_discrete,
        critic=ppo_critic,
        discrete=True,
        num_steps=_PPO_NUM_STEPS,
        num_envs=_PPO_NUM_ENVS,
        gamma=0.99,
        gae_lambda=0.95,
        num_minibatches=2,
        update_epochs=2,
        anneal_lr=False,
    )
    n, e = _PPO_NUM_STEPS, _PPO_NUM_ENVS
    module._obs = torch.zeros(n, e, CARTPOLE_OBS_DIM)
    module._actions = torch.zeros(n, e)
    module._log_probs = torch.zeros(n, e)
    module._rewards = torch.randn(n, e)
    module._dones = torch.zeros(n, e)
    module._values = torch.randn(n, e)
    module._next_obs = torch.zeros(e, CARTPOLE_OBS_DIM)
    module._next_done = torch.zeros(e)
    return module


# ---------------------------------------------------------------------------
# DQN fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def dqn_q_network() -> MLP:
    return MLP(CARTPOLE_OBS_DIM, CARTPOLE_N_ACTIONS, hidden_dim=64, num_layers=2)


@pytest.fixture()
def dqn_module(dqn_q_network) -> DQNModule:
    return DQNModule(
        q_network=dqn_q_network,
        gamma=0.99,
        tau=1.0,
        batch_size=32,
        learning_starts=50,
        train_frequency=1,
        target_network_frequency=50,
        start_epsilon=1.0,
        end_epsilon=0.05,
        exploration_fraction=0.5,
        total_timesteps=500,
        optimizer=partial(Adam, lr=1e-3),
    )
