"""Actor network architectures for SAC (stochastic) and TD3 (deterministic)."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def _build_mlp(input_dim: int, hidden_dim: int, num_layers: int, output_dim: int) -> nn.Sequential:
    layers: list[nn.Module] = [nn.Linear(input_dim, hidden_dim), nn.ReLU()]
    for _ in range(num_layers - 1):
        layers += [nn.Linear(hidden_dim, hidden_dim), nn.ReLU()]
    layers.append(nn.Linear(hidden_dim, output_dim))
    return nn.Sequential(*layers)


class StochasticActor(nn.Module):
    """Stochastic Gaussian actor for SAC with tanh squashing and action rescaling.

    Args:
        obs_dim: Observation dimensionality.
        action_dim: Action dimensionality.
        hidden_dim: Hidden layer width.
        num_layers: Number of hidden layers.
        log_std_min: Lower clamp for log std.
        log_std_max: Upper clamp for log std.
        action_scale: (high - low) / 2 for the action space.
        action_bias: (high + low) / 2 for the action space.
    """

    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        hidden_dim: int = 256,
        num_layers: int = 2,
        log_std_min: float = -5.0,
        log_std_max: float = 2.0,
        action_scale: float = 1.0,
        action_bias: float = 0.0,
    ) -> None:
        super().__init__()
        self._log_std_min = log_std_min
        self._log_std_max = log_std_max

        self.backbone = _build_mlp(obs_dim, hidden_dim, num_layers - 1, hidden_dim)
        self.mean_head = nn.Linear(hidden_dim, action_dim)
        self.log_std_head = nn.Linear(hidden_dim, action_dim)

        self.register_buffer("action_scale", torch.tensor(action_scale, dtype=torch.float32))
        self.register_buffer("action_bias", torch.tensor(action_bias, dtype=torch.float32))

    def get_action(self, obs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Sample action via reparameterization and compute log prob.

        Args:
            obs: ``(B, obs_dim)``

        Returns:
            ``(action, log_prob, mean)`` where action is rescaled to the env's
            action range, log_prob is ``(B,)``, and mean is the deterministic
            greedy action (also rescaled).
        """
        x = self.backbone(obs)
        mean = self.mean_head(x)
        log_std = self.log_std_head(x).clamp(self._log_std_min, self._log_std_max)
        std = log_std.exp()

        # Reparameterization
        eps = torch.randn_like(mean)
        z = mean + std * eps

        action = torch.tanh(z) * self.action_scale + self.action_bias

        # Log-prob of z under N(mean, std)
        log_prob_gaussian = -0.5 * (((z - mean) / (std + 1e-8)) ** 2 + 2 * log_std + 1.8378770664)

        # Correction for tanh squashing + scale: subtract log|det(∂action/∂z)|
        # ∂action/∂z = scale * (1 - tanh²(z)), so log det = sum(log(scale * (1 - tanh²(z))))
        log_det = (torch.log(self.action_scale) + torch.log(1.0 - torch.tanh(z) ** 2 + 1e-7)).sum(dim=-1)
        log_prob = log_prob_gaussian.sum(dim=-1) - log_det

        mean_action = torch.tanh(mean) * self.action_scale + self.action_bias
        return action, log_prob, mean_action

    def act_deterministic(self, obs: torch.Tensor) -> torch.Tensor:
        """Return deterministic (mean) action for evaluation.

        Args:
            obs: ``(B, obs_dim)``

        Returns:
            ``tanh(mean) * scale + bias`` with shape ``(B, action_dim)``.
        """
        x = self.backbone(obs)
        mean = self.mean_head(x)
        return torch.tanh(mean) * self.action_scale + self.action_bias


class DeterministicActor(nn.Module):
    """Deterministic actor for TD3 with action rescaling.

    Args:
        obs_dim: Observation dimensionality.
        action_dim: Action dimensionality.
        hidden_dim: Hidden layer width.
        num_layers: Number of hidden layers.
        action_scale: (high - low) / 2 for the action space.
        action_bias: (high + low) / 2 for the action space.
    """

    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        hidden_dim: int = 256,
        num_layers: int = 2,
        action_scale: float = 1.0,
        action_bias: float = 0.0,
    ) -> None:
        super().__init__()
        self.net = _build_mlp(obs_dim, hidden_dim, num_layers, action_dim)

        self.register_buffer("action_scale", torch.tensor(action_scale, dtype=torch.float32))
        self.register_buffer("action_bias", torch.tensor(action_bias, dtype=torch.float32))

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """Compute rescaled deterministic action.

        Args:
            obs: ``(B, obs_dim)``

        Returns:
            Action in ``[bias - scale, bias + scale]`` with shape ``(B, action_dim)``.
        """
        return torch.tanh(self.net(obs)) * self.action_scale + self.action_bias

    def act_deterministic(self, obs: torch.Tensor) -> torch.Tensor:
        return self.forward(obs)
