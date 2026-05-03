"""Hydra entry point for RL training.

Run with::

    python src/{{cookiecutter.repo_name}}/train.py                    # SAC on Pendulum-v1
    python src/{{cookiecutter.repo_name}}/train.py agent=td3           # TD3 on Pendulum-v1
    python src/{{cookiecutter.repo_name}}/train.py +experiment=debug   # fast sanity-check
    python src/{{cookiecutter.repo_name}}/train.py +experiment=lunar_lander
"""

from __future__ import annotations

from pathlib import Path

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig

config_path = str(Path(__file__).resolve().parent.parent.parent / "configs")


@hydra.main(config_path=config_path, config_name="train_config", version_base="1.2")
def train(cfg: DictConfig) -> None:
    """Instantiate all components and run the training loop.

    Args:
        cfg: Hydra-composed configuration dict.
    """
    # 1. Environment + replay buffer
    datamodule = instantiate(cfg.env)

    # 2. Agent (SACModule or TD3Module with nested actor/critic)
    agent = instantiate(cfg.agent)

    # 3. Logger
    logger = instantiate(cfg.logger) if cfg.get("logger") else None
    if logger is not None:
        logger.log_hyperparams(cfg)

    # 4. Callbacks
    callbacks = (
        [instantiate(cb) for _, cb in cfg.callbacks.items()]
        if cfg.get("callbacks")
        else []
    )

    # 5. Trainer
    trainer = instantiate(cfg.trainer, logger=logger, callbacks=callbacks)

    # 6. Train
    trainer.fit(agent, datamodule)


if __name__ == "__main__":
    train()
