"""Convolutional encoder for the VAE."""

from __future__ import annotations

import torch
import torch.nn as nn


class Encoder(nn.Module):
    """Maps images to (mu, log_var) in a flat latent space.

    Two stride-2 conv layers downsample the spatial dims by 4x, then two
    linear projections produce the mean and log-variance of the posterior.

    Args:
        in_channels: 1 for grayscale (MNIST), 3 for RGB (CIFAR-10).
        image_size: (height, width) of the input — used to compute the flat dim.
        latent_dim: Dimension of the latent vector z.
        hidden_channels: Width of the convolutional feature maps.
    """

    def __init__(
        self,
        in_channels: int,
        image_size: tuple[int, int],
        latent_dim: int,
        hidden_channels: int = 64,
    ) -> None:
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.SiLU(),
            nn.Conv2d(32, hidden_channels, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(hidden_channels),
            nn.SiLU(),
        )
        h, w = image_size[0] // 4, image_size[1] // 4
        flat_dim = hidden_channels * h * w
        self.fc_mu = nn.Linear(flat_dim, latent_dim)
        self.fc_log_var = nn.Linear(flat_dim, latent_dim)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Return (mu, log_var) tensors of shape (B, latent_dim)."""
        x = self.conv(x).flatten(1)
        return self.fc_mu(x), self.fc_log_var(x)
