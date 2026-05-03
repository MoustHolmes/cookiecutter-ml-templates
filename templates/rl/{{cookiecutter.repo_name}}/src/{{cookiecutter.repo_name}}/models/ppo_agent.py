"""PPO agent networks for discrete and continuous action spaces.

Ported from CleanRL (https://github.com/vwxyzjn/cleanrl) with orthogonal
weight initialisation as described in the original PPO paper.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical
from torch.distributions.normal import Normal


def layer_init(layer: nn.Linear, std: float = np.sqrt(2), bias_const: float = 0.0) -> nn.Linear:
    """Orthogonal weight init used by CleanRL's PPO agents."""
    nn.init.orthogonal_(layer.weight, std)
    nn.init.constant_(layer.bias, bias_const)
    return layer


def _critic(obs_dim: int, hidden_dim: int = 64) -> nn.Sequential:
    return nn.Sequential(
        layer_init(nn.Linear(obs_dim, hidden_dim)),
        nn.Tanh(),
        layer_init(nn.Linear(hidden_dim, hidden_dim)),
        nn.Tanh(),
        layer_init(nn.Linear(hidden_dim, 1), std=1.0),
    )


class PPOAgentDiscrete(nn.Module):
    """PPO agent for discrete action spaces (e.g. CartPole).

    Args:
        obs_dim: Observation dimensionality.
        n_actions: Number of discrete actions.
        hidden_dim: Hidden layer width (default 64 matching CleanRL).
    """

    def __init__(self, obs_dim: int, n_actions: int, hidden_dim: int = 64) -> None:
        super().__init__()
        self.critic = _critic(obs_dim, hidden_dim)
        self.actor = nn.Sequential(
            layer_init(nn.Linear(obs_dim, hidden_dim)),
            nn.Tanh(),
            layer_init(nn.Linear(hidden_dim, hidden_dim)),
            nn.Tanh(),
            layer_init(nn.Linear(hidden_dim, n_actions), std=0.01),
        )

    def get_value(self, obs: torch.Tensor) -> torch.Tensor:
        return self.critic(obs)

    def get_action_and_value(
        self, obs: torch.Tensor, action: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """Sample or evaluate action under Categorical policy.

        Args:
            obs: ``(B, obs_dim)``
            action: If provided, evaluate log-prob/entropy for this action.

        Returns:
            ``(action, log_prob, entropy, value)`` all shape ``(B,)`` except
            action which is ``(B,)`` integer indices.
        """
        logits = self.actor(obs)
        probs = Categorical(logits=logits)
        if action is None:
            action = probs.sample()
        return action, probs.log_prob(action), probs.entropy(), self.critic(obs)

    def act_deterministic(self, obs: torch.Tensor) -> torch.Tensor:
        """Return argmax action for callbacks/evaluation."""
        return self.actor(obs).argmax(dim=-1)


class PPOAgentContinuous(nn.Module):
    """PPO agent for continuous action spaces (e.g. Pendulum, HalfCheetah).

    Also supports RPO (Robust Policy Optimization) when ``rpo_alpha > 0``:
    during policy-gradient computation a uniform perturbation is added to the
    action mean, as in the original RPO paper.

    Args:
        obs_dim: Observation dimensionality.
        action_dim: Action dimensionality.
        hidden_dim: Hidden layer width (default 64 matching CleanRL).
        rpo_alpha: Perturbation half-width for RPO; 0 disables it (pure PPO).
    """

    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        hidden_dim: int = 64,
        rpo_alpha: float = 0.0,
    ) -> None:
        super().__init__()
        self.rpo_alpha = rpo_alpha
        self.critic = _critic(obs_dim, hidden_dim)
        self.actor_mean = nn.Sequential(
            layer_init(nn.Linear(obs_dim, hidden_dim)),
            nn.Tanh(),
            layer_init(nn.Linear(hidden_dim, hidden_dim)),
            nn.Tanh(),
            layer_init(nn.Linear(hidden_dim, action_dim), std=0.01),
        )
        self.actor_logstd = nn.Parameter(torch.zeros(1, action_dim))

    def get_value(self, obs: torch.Tensor) -> torch.Tensor:
        return self.critic(obs)

    def get_action_and_value(
        self, obs: torch.Tensor, action: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """Sample or evaluate action under diagonal Normal policy.

        Args:
            obs: ``(B, obs_dim)``
            action: If provided, evaluate log-prob/entropy (RPO perturbation
                    is applied to the mean before evaluation when rpo_alpha > 0).

        Returns:
            ``(action, log_prob, entropy, value)`` with log_prob/entropy summed
            over the action dimensions.
        """
        action_mean = self.actor_mean(obs)
        action_logstd = self.actor_logstd.expand_as(action_mean)
        action_std = torch.exp(action_logstd)
        probs = Normal(action_mean, action_std)

        if action is None:
            action = probs.sample()
        elif self.rpo_alpha > 0:
            # RPO: add uniform noise to mean before computing log-prob
            z = torch.empty_like(action_mean).uniform_(-self.rpo_alpha, self.rpo_alpha)
            action_mean = action_mean + z
            probs = Normal(action_mean, action_std)

        return action, probs.log_prob(action).sum(1), probs.entropy().sum(1), self.critic(obs)

    def act_deterministic(self, obs: torch.Tensor) -> torch.Tensor:
        """Return mean action for callbacks/evaluation."""
        return self.actor_mean(obs)
