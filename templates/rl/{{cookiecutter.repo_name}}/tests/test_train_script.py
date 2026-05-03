"""End-to-end integration tests for the training script."""

from __future__ import annotations

from pathlib import Path

import pytest
from hydra import compose, initialize_config_dir
from hydra.core.global_hydra import GlobalHydra
from hydra.utils import instantiate


def _fit(overrides: list[str], tmp_path) -> None:
    GlobalHydra.instance().clear()
    config_dir = str(Path(__file__).parent.parent / "configs")
    with initialize_config_dir(config_dir=config_dir, version_base=None):
        cfg = compose(config_name="train_config", overrides=overrides)
    datamodule = instantiate(cfg.env)
    agent = instantiate(cfg.agent)
    callbacks = (
        [instantiate(cb) for _, cb in cfg.callbacks.items()]
        if cfg.get("callbacks")
        else []
    )
    trainer = instantiate(cfg.trainer, logger=False, callbacks=callbacks)
    trainer.fit(agent, datamodule)


def test_sac_fast_dev_run(tmp_path) -> None:
    """SAC + Pendulum fast_dev_run must complete without errors."""
    _fit(["experiment=debug"], tmp_path)


def test_ppo_cartpole_fast_dev_run(tmp_path) -> None:
    """PPO discrete + CartPole debug run must complete without errors."""
    _fit(
        [
            "agent=ppo_discrete",
            "env=cartpole",
            "experiment=ppo_debug",
        ],
        tmp_path,
    )


def test_dqn_cartpole_fast_dev_run(tmp_path) -> None:
    """DQN + CartPole debug run must complete without errors."""
    _fit(
        [
            "agent=dqn",
            "env=cartpole_replay",
            "experiment=dqn_debug",
        ],
        tmp_path,
    )
