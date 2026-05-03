"""Twin Q-network (critic) shared by SAC and TD3.

Using two independent critics and taking their minimum for Bellman targets
prevents the Q-value overestimation bias inherent in single-network
actor-critic methods.
"""

from __future__ import annotations

import torch
import torch.nn as nn


def _build_q_network(obs_dim: int, action_dim: int, hidden_dim: int, num_layers: int) -> nn.Sequential:
    """Build a Q-network MLP taking ``cat(obs, action)`` as input.

    Args:
        obs_dim: Observation dimensionality.
        action_dim: Action dimensionality.
        hidden_dim: Width of each hidden layer.
        num_layers: Number of hidden layers.

    Returns:
        An ``nn.Sequential`` that outputs a scalar Q-value per sample.
    """
    input_dim = obs_dim + action_dim
    layers: list[nn.Module] = [nn.Linear(input_dim, hidden_dim), nn.ReLU()]
    for _ in range(num_layers - 1):
        layers += [nn.Linear(hidden_dim, hidden_dim), nn.ReLU()]
    layers.append(nn.Linear(hidden_dim, 1))
    return nn.Sequential(*layers)


class TwinCritic(nn.Module):
    """Twin Q-network used as the critic in both SAC and TD3.

    Maintains two **independent** Q-networks (``q1``, ``q2``) with identical
    architectures.  The minimum of their outputs is used when computing
    Bellman targets to reduce overestimation bias (Clipped Double-Q Learning).

    Args:
        obs_dim: Dimensionality of the observation space.
        action_dim: Dimensionality of the action space.
        hidden_dim: Width of each hidden MLP layer.
        num_layers: Number of hidden MLP layers per Q-network.
    """

    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        hidden_dim: int = 256,
        num_layers: int = 2,
    ) -> None:
        super().__init__()
        self.q1_net = _build_q_network(obs_dim, action_dim, hidden_dim, num_layers)
        self.q2_net = _build_q_network(obs_dim, action_dim, hidden_dim, num_layers)

    def forward(
        self, obs: torch.Tensor, action: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute Q-values from both networks.

        Args:
            obs: Observation tensor of shape ``(B, obs_dim)``.
            action: Action tensor of shape ``(B, action_dim)``.

        Returns:
            Tuple ``(q1, q2)`` each of shape ``(B, 1)``.
        """
        x = torch.cat([obs, action], dim=-1)
        return self.q1_net(x), self.q2_net(x)

    def min_q(self, obs: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
        """Element-wise minimum of the two Q-values.

        Used in Bellman target computation to penalise overoptimism.

        Args:
            obs: Observation tensor of shape ``(B, obs_dim)``.
            action: Action tensor of shape ``(B, action_dim)``.

        Returns:
            Tensor of shape ``(B, 1)`` containing ``min(q1, q2)``.
        """
        q1, q2 = self.forward(obs, action)
        return torch.min(q1, q2)
