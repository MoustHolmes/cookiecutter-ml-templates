"""Convolutional decoder for the VAE."""

from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn


class Decoder(nn.Module):
    """Maps a latent vector z back to image space.

    A linear projection expands z to the spatial shape expected by two
    nearest-neighbour upsample + conv blocks that mirror the encoder.

    Args:
        out_channels: 1 for grayscale (MNIST), 3 for RGB (CIFAR-10).
        image_size: (height, width) of the target output — must match encoder.
        latent_dim: Dimension of the latent vector z.
        hidden_channels: Width of the convolutional feature maps.
        output_activation: Optional activation applied to the final output.
            Use nn.Sigmoid for [0, 1] pixel data, nn.Tanh for [-1, 1].
            None means no activation (unbounded output).
    """

    def __init__(
        self,
        out_channels: int,
        image_size: tuple[int, int],
        latent_dim: int,
        hidden_channels: int = 64,
        output_activation: Optional[nn.Module] = None,
    ) -> None:
        super().__init__()
        self.h = image_size[0] // 4
        self.w = image_size[1] // 4
        self.hidden_channels = hidden_channels
        flat_dim = hidden_channels * self.h * self.w

        self.fc = nn.Linear(latent_dim, flat_dim)
        self.deconv = nn.Sequential(
            nn.Upsample(scale_factor=2, mode="nearest"),
            nn.Conv2d(hidden_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.SiLU(),
            nn.Upsample(scale_factor=2, mode="nearest"),
            nn.Conv2d(32, out_channels, kernel_size=3, padding=1),
        )
        self.output_activation = output_activation

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        """Return reconstructed image of shape (B, out_channels, H, W)."""
        x = self.fc(z).view(z.shape[0], self.hidden_channels, self.h, self.w)
        x = self.deconv(x)
        if self.output_activation is not None:
            x = self.output_activation(x)
        return x
