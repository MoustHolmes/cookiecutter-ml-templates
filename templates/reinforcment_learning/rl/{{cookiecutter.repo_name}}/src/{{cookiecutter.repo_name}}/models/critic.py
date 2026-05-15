"""Twin Q-network (critic) shared by SAC and TD3."""

from __future__ import annotations

import torch
import torch.nn as nn

from .mlp import MLP


class TwinCritic(nn.Module):
    """Twin Q-network: two independent Q-networks with identical MLP architectures.

    ``forward`` returns ``(q1, q2)`` — the calling module decides how to
    combine them (e.g. Clipped Double-Q uses ``torch.min(q1, q2)`` for
    Bellman targets).

    Args:
        obs_dim: Dimensionality of the observation space.
        action_dim: Dimensionality of the action space.
        hidden_dim: Width of each hidden MLP layer.
        num_layers: Number of hidden layers per Q-network.
    """

    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        hidden_dim: int = 256,
        num_layers: int = 2,
    ) -> None:
        super().__init__()
        self.q1_net = MLP(obs_dim + action_dim, 1, hidden_dim, num_layers)
        self.q2_net = MLP(obs_dim + action_dim, 1, hidden_dim, num_layers)

    def forward(
        self, obs: torch.Tensor, action: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Return ``(q1, q2)`` each of shape ``(B, 1)``."""
        x = torch.cat([obs, action], dim=-1)
        return self.q1_net(x), self.q2_net(x)
