"""Tests for Hydra configuration loading and component instantiation."""

from __future__ import annotations

import hydra
import pytest
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig


def test_train_config_loads(cfg_train: DictConfig) -> None:
    """Default config must contain agent, env, and trainer sections."""
    assert cfg_train is not None
    assert cfg_train.agent is not None
    assert cfg_train.env is not None
    assert cfg_train.trainer is not None


def test_config_has_required_targets(cfg_train: DictConfig) -> None:
    """All instantiable config nodes must have a _target_ field."""
    assert "_target_" in cfg_train.agent
    assert "_target_" in cfg_train.env
    assert "_target_" in cfg_train.trainer


def test_agent_has_actor_and_critic(cfg_train: DictConfig) -> None:
    """SAC agent config must have nested actor and critic sub-configs."""
    assert "actor" in cfg_train.agent
    assert "critic" in cfg_train.agent
    assert "_target_" in cfg_train.agent.actor
    assert "_target_" in cfg_train.agent.critic


def test_instantiate_env(cfg_train: DictConfig) -> None:
    """RLDataModule must instantiate without errors."""
    HydraConfig().set_config(cfg_train)
    dm = hydra.utils.instantiate(cfg_train.env)
    assert dm is not None


def test_instantiate_agent(cfg_train: DictConfig) -> None:
    """SACModule must instantiate without errors."""
    HydraConfig().set_config(cfg_train)
    agent = hydra.utils.instantiate(cfg_train.agent)
    assert agent is not None
    assert agent.automatic_optimization is False


def test_instantiate_trainer(cfg_train: DictConfig) -> None:
    """Trainer must instantiate without errors."""
    HydraConfig().set_config(cfg_train)
    trainer = hydra.utils.instantiate(cfg_train.trainer)
    assert trainer is not None


def test_debug_config_has_fast_dev_run(cfg_train_debug: DictConfig) -> None:
    """Debug experiment must set fast_dev_run=True."""
    assert cfg_train_debug.trainer.fast_dev_run is True


def test_debug_config_small_buffer(cfg_train_debug: DictConfig) -> None:
    """Debug experiment must use a small replay buffer."""
    assert cfg_train_debug.env.buffer_size <= 5000
