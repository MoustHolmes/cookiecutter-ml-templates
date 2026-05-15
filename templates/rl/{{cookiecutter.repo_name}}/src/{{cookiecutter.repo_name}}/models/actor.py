"""Actor network architectures for SAC (stochastic) and TD3 (deterministic)."""

from __future__ import annotations

import torch.nn as nn

from .mlp import MLP


class StochasticActor(nn.Module):
    """Gaussian actor for SAC: backbone MLP with separate mean and log-std heads.

    ``forward`` returns raw network outputs ``(mean, log_std)``.  All
    reparameterization, tanh squashing, log-prob computation, and action
    rescaling are handled by the calling :class:`SACModule`.

    Args:
        obs_dim: Observation dimensionality.
        action_dim: Action dimensionality.
        hidden_dim: Hidden layer width passed to the backbone MLP.
        num_layers: Number of hidden layers in the backbone MLP.
    """

    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        hidden_dim: int = 256,
        num_layers: int = 2,
    ) -> None:
        super().__init__()
        self.backbone = MLP(obs_dim, hidden_dim, hidden_dim, num_layers)
        self.mean_head = nn.Linear(hidden_dim, action_dim)
        self.log_std_head = nn.Linear(hidden_dim, action_dim)

    def forward(self, obs):
        """Return ``(mean, log_std)`` — unclamped network outputs."""
        features = self.backbone(obs)
        return self.mean_head(features), self.log_std_head(features)


class DeterministicActor(MLP):
    """Deterministic actor for TD3: maps observations to pre-tanh actions.

    A thin subclass of :class:`MLP` that preserves semantic parameter names
    (``obs_dim``/``action_dim``) used by environment configs for injection.
    Tanh squashing and action rescaling are applied by :class:`TD3Module`.

    Args:
        obs_dim: Observation dimensionality.
        action_dim: Action dimensionality.
        hidden_dim: Hidden layer width.
        num_layers: Number of hidden layers.
    """

    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        hidden_dim: int = 256,
        num_layers: int = 2,
    ) -> None:
        super().__init__(obs_dim, action_dim, hidden_dim, num_layers)
