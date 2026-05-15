"""On-policy rollout datamodule for PPO/RPO using vectorized environments."""

from __future__ import annotations

import gymnasium as gym
import numpy as np
import torch
import lightning as L
from torch.utils.data import DataLoader, TensorDataset


def _make_env(env_id: str, seed: int):
    def thunk():
        env = gym.make(env_id)
        env = gym.wrappers.RecordEpisodeStatistics(env)
        env.action_space.seed(seed)
        return env
    return thunk


class RolloutDataModule(L.LightningDataModule):
    """Vectorized environment datamodule for on-policy algorithms (PPO/RPO).

    Creates a ``SyncVectorEnv`` with ``num_envs`` parallel environments.
    Exposes ``obs_shape``, ``act_shape``, and ``is_continuous`` so
    ``PPOModule.setup()`` can pre-allocate rollout buffers.

    The train dataloader returns a single dummy item per epoch — one call to
    ``training_step`` owns the complete PPO rollout + update round.

    Args:
        env_id: Gymnasium environment ID (e.g. ``"CartPole-v1"``).
        num_envs: Number of parallel environments.
        seed: Base random seed; env ``i`` gets ``seed + i``.
    """

    # Accumulated episode stats (mirroring RLDataModule interface)
    episode_rewards: list[float]
    episode_lengths: list[int]

    def __init__(self, env_id: str, num_envs: int = 4, seed: int = 42) -> None:
        super().__init__()
        self.save_hyperparameters()
        self.envs: gym.vector.SyncVectorEnv | None = None

        self.episode_rewards: list[float] = []
        self.episode_lengths: list[int] = []

        # Filled in setup()
        self.obs_shape: tuple[int, ...] = ()
        self.act_shape: tuple[int, ...] = ()
        self.is_continuous: bool = False

    def setup(self, stage: str) -> None:
        if stage != "fit" or self.envs is not None:
            return

        hp = self.hparams
        self.envs = gym.vector.SyncVectorEnv(
            [_make_env(hp.env_id, hp.seed + i) for i in range(hp.num_envs)]
        )

        self.obs_shape = self.envs.single_observation_space.shape
        act_space = self.envs.single_action_space

        if isinstance(act_space, gym.spaces.Discrete):
            self.is_continuous = False
            self.act_shape = ()  # scalar integer actions
        else:
            self.is_continuous = True
            self.act_shape = act_space.shape

    def train_dataloader(self) -> DataLoader:
        # One dummy item per epoch — PPOModule.training_step owns the full round
        return DataLoader(TensorDataset(torch.zeros(1)), batch_size=1)

    def on_before_batch_transfer(self, batch, dataloader_idx):
        # Capture episode stats from the vectorized env's RecordEpisodeStatistics
        if self.envs is None:
            return batch
        # Episodes are tracked via the wrapper's info dict during stepping in PPOModule
        return batch

    def teardown(self, stage: str) -> None:
        if self.envs is not None:
            self.envs.close()
            self.envs = None
