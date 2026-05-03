"""Circular replay buffer for off-policy reinforcement learning.

Stores (obs, action, reward, next_obs, done) transitions collected during
environment interaction. The ``done`` flag encodes *only* genuine terminations
(``terminated=True``); episode truncations are intentionally stored as ``done=0``
so that the value-function bootstrap is not masked on time-limit boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch


@dataclass
class Batch:
    """A mini-batch of transitions sampled from the replay buffer.

    All tensors are float32 with shapes:

    - ``obs``:      ``(B, obs_dim)``
    - ``action``:   ``(B, action_dim)``
    - ``reward``:   ``(B,)``
    - ``next_obs``: ``(B, obs_dim)``
    - ``done``:     ``(B,)``  — 1.0 only on genuine termination, 0.0 on truncation
    """

    obs: torch.Tensor
    action: torch.Tensor
    reward: torch.Tensor
    next_obs: torch.Tensor
    done: torch.Tensor


class ReplayBuffer:
    """Fixed-capacity circular experience replay buffer.

    Transitions are stored as numpy arrays (CPU). Sampling returns a
    :class:`Batch` of float32 ``torch.Tensor`` objects on CPU; move to the
    correct device inside the training loop.

    Args:
        obs_dim: Dimensionality of the observation space.
        action_dim: Dimensionality of the action space.
        buffer_size: Maximum number of transitions to store.
    """

    def __init__(self, obs_dim: int, action_dim: int, buffer_size: int) -> None:
        self._obs_dim = obs_dim
        self._action_dim = action_dim
        self._buffer_size = buffer_size

        self._obs = np.zeros((buffer_size, obs_dim), dtype=np.float32)
        self._action = np.zeros((buffer_size, action_dim), dtype=np.float32)
        self._reward = np.zeros(buffer_size, dtype=np.float32)
        self._next_obs = np.zeros((buffer_size, obs_dim), dtype=np.float32)
        self._done = np.zeros(buffer_size, dtype=np.float32)

        self._ptr = 0      # next write position
        self._size = 0     # current fill level

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def add(
        self,
        obs: np.ndarray,
        action: np.ndarray,
        reward: float,
        next_obs: np.ndarray,
        terminated: bool,
        truncated: bool,  # noqa: ARG002 — accepted but ignored by design
    ) -> None:
        """Store a single transition.

        ``truncated`` is accepted for API compatibility with the Gymnasium step
        return, but it is intentionally ignored: only genuine ``terminated``
        episodes set ``done=1``. This preserves correct value-function
        bootstrapping for time-limited environments.

        Args:
            obs: Current observation.
            action: Action taken.
            reward: Immediate reward received.
            next_obs: Observation after taking the action.
            terminated: True if the episode ended due to a terminal state.
            truncated: True if the episode ended due to a time limit (ignored).
        """
        self._obs[self._ptr] = obs
        self._action[self._ptr] = action
        self._reward[self._ptr] = reward
        self._next_obs[self._ptr] = next_obs
        self._done[self._ptr] = float(terminated)  # truncation intentionally excluded

        self._ptr = (self._ptr + 1) % self._buffer_size
        self._size = min(self._size + 1, self._buffer_size)

    def sample(self, batch_size: int) -> Batch:
        """Sample a uniformly random mini-batch of transitions.

        Args:
            batch_size: Number of transitions to sample.

        Returns:
            A :class:`Batch` of float32 tensors on CPU.

        Raises:
            ValueError: If the buffer contains fewer transitions than ``batch_size``.
        """
        if self._size < batch_size:
            msg = f"Buffer has {self._size} transitions, cannot sample {batch_size}."
            raise ValueError(msg)

        idx = np.random.randint(0, self._size, size=batch_size)
        return Batch(
            obs=torch.tensor(self._obs[idx]),
            action=torch.tensor(self._action[idx]),
            reward=torch.tensor(self._reward[idx]),
            next_obs=torch.tensor(self._next_obs[idx]),
            done=torch.tensor(self._done[idx]),
        )

    def __len__(self) -> int:  # noqa: D105
        return self._size
