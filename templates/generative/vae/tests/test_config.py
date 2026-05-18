"""Tests for configuration setup and instantiation."""

import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig
import pytest


def test_train_config(cfg_train: DictConfig) -> None:
    """Tests the training configuration provided by the `cfg_train` pytest fixture."""
    assert cfg_train
    assert cfg_train.data
    assert cfg_train.model
    assert cfg_train.trainer

    HydraConfig().set_config(cfg_train)

    data_module = hydra.utils.instantiate(cfg_train.data)
    assert data_module is not None

    model = hydra.utils.instantiate(cfg_train.model)
    assert model is not None

    trainer = hydra.utils.instantiate(cfg_train.trainer)
    assert trainer is not None


def test_train_config_debug(cfg_train_debug: DictConfig) -> None:
    """Tests the training configuration with debug overrides."""
    assert cfg_train_debug
    assert cfg_train_debug.data
    assert cfg_train_debug.model
    assert cfg_train_debug.trainer

    HydraConfig().set_config(cfg_train_debug)

    data_module = hydra.utils.instantiate(cfg_train_debug.data)
    assert data_module is not None

    model = hydra.utils.instantiate(cfg_train_debug.model)
    assert model is not None

    trainer = hydra.utils.instantiate(cfg_train_debug.trainer)
    assert trainer is not None


def test_config_has_required_fields(cfg_train: DictConfig) -> None:
    """Tests that the configuration has all required fields."""
    assert "data" in cfg_train
    assert "model" in cfg_train
    assert "trainer" in cfg_train
    assert "task_name" in cfg_train

    assert "_target_" in cfg_train.data
    assert "_target_" in cfg_train.model
    assert "_target_" in cfg_train.trainer


def test_model_components(cfg_train: DictConfig) -> None:
    """Tests that model configuration has all required VAE components."""
    assert "encoder" in cfg_train.model
    assert "decoder" in cfg_train.model
    assert "optimizer" in cfg_train.model
    assert "latent_dim" in cfg_train.model

    assert "_target_" in cfg_train.model.encoder
    assert "_target_" in cfg_train.model.decoder
    assert "_target_" in cfg_train.model.optimizer


def test_instantiate_all_components(cfg_train: DictConfig) -> None:
    """Tests that all configuration components can be instantiated without errors."""
    HydraConfig().set_config(cfg_train)

    data_module = hydra.utils.instantiate(cfg_train.data)
    assert data_module is not None
    assert hasattr(data_module, "prepare_data")
    assert hasattr(data_module, "setup")
    assert hasattr(data_module, "train_dataloader")

    model = hydra.utils.instantiate(cfg_train.model)
    assert model is not None
    assert hasattr(model, "training_step")
    assert hasattr(model, "validation_step")
    assert hasattr(model, "configure_optimizers")
    assert hasattr(model, "generate")

    trainer = hydra.utils.instantiate(cfg_train.trainer)
    assert trainer is not None
    assert hasattr(trainer, "fit")
