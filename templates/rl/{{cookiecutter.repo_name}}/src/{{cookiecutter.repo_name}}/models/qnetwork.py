"""Q-network for DQN.

Ported from CleanRL (https://github.com/vwxyzjn/cleanrl). Uses the same
120→84 hidden architecture from the original DQN paper.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class QNetwork(nn.Module):
    """Q-value network mapping observations to per-action Q-values.

    Args:
        obs_dim: Observation dimensionality.
        n_actions: Number of discrete actions.
    """

    def __init__(self, obs_dim: int, n_actions: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(obs_dim, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, n_actions),
        )

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """Return Q-values for all actions.

        Args:
            obs: ``(B, obs_dim)``

        Returns:
            ``(B, n_actions)`` Q-values.
        """
        return self.network(obs)
