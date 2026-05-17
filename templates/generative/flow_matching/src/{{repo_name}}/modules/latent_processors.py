from __future__ import annotations

from abc import ABC, abstractmethod

import lightning as L
import torch
import torch.nn as nn


class LatentProcessor(ABC):
    """Interface for encoding inputs to and decoding outputs from a latent space."""

    @abstractmethod
    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """Encode input tensor to latent representation."""
        ...

    @abstractmethod
    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """Decode latent tensor back to data space."""
        ...


class AutoencoderWrapper(nn.Module, LatentProcessor):
    """Wraps a VAE to provide the LatentProcessor encode/decode interface.

    Optionally loads weights from a checkpoint and freezes the autoencoder
    so its parameters don't update during flow matching training.

    Args:
        autoencoder: A SpatialVAE or compatible model with .encoder and .decoder attributes.
        checkpoint_path: Path to a Lightning checkpoint. Empty string means no loading.
        freeze: Whether to freeze the autoencoder parameters. Defaults to True.
    """

    def __init__(
        self,
        autoencoder: L.LightningModule,
        checkpoint_path: str = "",
        freeze: bool = True,
    ) -> None:
        super().__init__()
        self.autoencoder = autoencoder

        if checkpoint_path:
            checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
            state_dict = checkpoint.get("state_dict", checkpoint)
            self.autoencoder.load_state_dict(state_dict)

        if freeze:
            for param in self.autoencoder.parameters():
                param.requires_grad_(False)
            self.autoencoder.eval()

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """Encode input to the VAE's mean latent, scaled by the autoencoder's scale_factor.

        Args:
            x: Input tensor of shape (B, C, H, W).

        Returns:
            Scaled latent tensor of shape (B, latent_channels, H', W').
        """
        mu, _ = self.autoencoder.encoder(x)
        scale_factor = getattr(self.autoencoder, "scale_factor", torch.tensor(1.0))
        return mu * scale_factor

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """Decode a scaled latent tensor back to data space.

        Args:
            z: Scaled latent tensor of shape (B, latent_channels, H', W').

        Returns:
            Reconstructed tensor of shape (B, C, H, W).
        """
        scale_factor = getattr(self.autoencoder, "scale_factor", torch.tensor(1.0))
        return self.autoencoder.decoder(z / scale_factor)
