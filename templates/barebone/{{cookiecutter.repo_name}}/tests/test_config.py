"""Tests for configuration setup and instantiation."""

import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig
import pytest


def test_train_config(cfg_train: DictConfig) -> None:
    """Tests the training configuration provided by the `cfg_train` pytest fixture.

    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    assert cfg_train
    assert cfg_train.data
    assert cfg_train.model
    assert cfg_train.trainer

    HydraConfig().set_config(cfg_train)

    # Test that we can instantiate the data module
    data_module = hydra.utils.instantiate(cfg_train.data)
    assert data_module is not None

    # Test that we can instantiate the model
    model = hydra.utils.instantiate(cfg_train.model)
    assert model is not None

    # Test that we can instantiate the trainer
    trainer = hydra.utils.instantiate(cfg_train.trainer)
    assert trainer is not None


def test_config_has_required_fields(cfg_train: DictConfig) -> None:
    """Tests that the configuration has all required fields.

    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    # Check top-level fields
    assert "data" in cfg_train
    assert "model" in cfg_train
    assert "trainer" in cfg_train
    assert "task_name" in cfg_train

    # Check data config has _target_
    assert "_target_" in cfg_train.data

    # Check model config has _target_
    assert "_target_" in cfg_train.model

    # Check trainer config has _target_
    assert "_target_" in cfg_train.trainer
