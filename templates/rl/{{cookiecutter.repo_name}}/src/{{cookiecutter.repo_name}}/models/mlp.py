"""Shared MLP backbone used across all RL model architectures."""

from __future__ import annotations

import math

import torch
import torch.nn as nn

_ACTIVATIONS: dict[str, type[nn.Module]] = {
    "relu": nn.ReLU,
    "tanh": nn.Tanh,
    "elu": nn.ELU,
    "leaky_relu": nn.LeakyReLU,
    "gelu": nn.GELU,
}


class MLP(nn.Module):
    """Fully-connected network with configurable depth, width, and activation.

    Architecture: ``[Linear(in→h) + Act] × num_layers`` followed by
    ``Linear(h→out)`` and an optional output activation.

    Args:
        input_dim: Input feature dimensionality.
        output_dim: Output feature dimensionality.
        hidden_dim: Width of each hidden layer.
        num_layers: Number of hidden (Linear + activation) blocks.
        activation: Hidden-layer activation — one of ``"relu"``, ``"tanh"``,
            ``"elu"``, ``"leaky_relu"``, ``"gelu"``.
        output_activation: Optional activation applied after the final linear.
        orthogonal_init: Initialise all weights with orthogonal matrices
            (CleanRL PPO convention).
        hidden_std: Orthogonal init gain for hidden layers (default √2).
        output_std: Orthogonal init gain for the output layer; override to
            e.g. 0.01 for policy heads.
    """

    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        hidden_dim: int = 256,
        num_layers: int = 2,
        activation: str = "relu",
        output_activation: str | None = None,
        orthogonal_init: bool = False,
        hidden_std: float = math.sqrt(2),
        output_std: float = 1.0,
    ) -> None:
        super().__init__()
        act_cls = _ACTIVATIONS[activation]

        layers: list[nn.Module] = []
        in_dim = input_dim
        for _ in range(num_layers):
            linear = nn.Linear(in_dim, hidden_dim)
            if orthogonal_init:
                nn.init.orthogonal_(linear.weight, hidden_std)
                nn.init.constant_(linear.bias, 0.0)
            layers.append(linear)
            layers.append(act_cls())
            in_dim = hidden_dim

        out_linear = nn.Linear(in_dim, output_dim)
        if orthogonal_init:
            nn.init.orthogonal_(out_linear.weight, output_std)
            nn.init.constant_(out_linear.bias, 0.0)
        layers.append(out_linear)

        if output_activation is not None:
            layers.append(_ACTIVATIONS[output_activation]())

        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
