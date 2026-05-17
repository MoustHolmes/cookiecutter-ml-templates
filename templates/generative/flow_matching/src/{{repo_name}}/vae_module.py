from typing import Any, Callable

import lightning as L
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam, Optimizer

import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as L
from torch.optim import Adam

class SpatialEncoder(nn.Module):
    def __init__(
            self,
            in_channels: int = 1,
            latent_channels: int = 4
        ):
        super().__init__()
        # MNIST is 28x28.
        # Layer 1: 28x28 -> 14x14
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.SiLU() # SiLU (Swish) is standard for LFM/Diffusion
        )
        # Layer 2: 14x14 -> 7x7
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.SiLU()
        )
        # No flattening! We keep the 7x7 grid.
        # We project to 2 * latent_channels (for Mean and LogVar)
        self.conv_out = nn.Conv2d(64, 2 * latent_channels, kernel_size=3, padding=1)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        # Output shape: [B, 2*latent_channels, 7, 7]
        mu_logvar = self.conv_out(x)
        mu, log_var = torch.chunk(mu_logvar, 2, dim=1)
        return mu, log_var

class SpatialDecoder(nn.Module):
    def __init__(
            self,
            out_channels: int = 1,
            latent_channels: int = 4
        ):
        super().__init__()

        self.conv_in = nn.Sequential(
            nn.Conv2d(latent_channels, 64, kernel_size=3, padding=1),
            nn.SiLU()
        )

        # Layer 1 Upsample: 7x7 -> 14x14
        self.up1 = nn.Sequential(
            nn.Upsample(scale_factor=2, mode='nearest'),
            nn.Conv2d(64, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.SiLU()
        )

        # Layer 2 Upsample: 14x14 -> 28x28
        self.up2 = nn.Sequential(
            nn.Upsample(scale_factor=2, mode='nearest'),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.SiLU()
        )

        self.final = nn.Conv2d(32, out_channels, kernel_size=3, padding=1)

    def forward(self, z):
        x = self.conv_in(z)
        x = self.up1(x)
        x = self.up2(x)
        return self.final(x) # No Tanh/Sigmoid here if using MSE with logits, or add Tanh if input is -1 to 1

class SpatialVAE(L.LightningModule):
    def __init__(
            self,
            in_channels: int = 1,
            latent_channels: int = 4,
            kl_weight: float = 0.00025,
            lr: float = 1e-3
        ):
        super().__init__()
        self.save_hyperparameters()
        self.encoder = SpatialEncoder(in_channels, latent_channels)
        self.decoder = SpatialDecoder(in_channels, latent_channels)
        self.lr = lr

        self.kl_weight = kl_weight

        # Important: Scale factor for Latent Flow Matching
        # This acts like the "scale" parameter in Wan2.2
        self.register_buffer('scale_factor', torch.tensor(1.0))

    def forward(self, x):
        mu, log_var = self.encoder(x)
        z = self.reparameterize(mu, log_var)
        recon = self.decoder(z)
        return recon, mu, log_var

    def reparameterize(self, mu, log_var):
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def model_step(self, batch):
        x, _ = batch
        recon, mu, log_var = self(x)
        # Reconstruction Loss
        recon_loss = F.mse_loss(recon, x)
        # KL Divergence
        kld_loss = torch.mean(-0.5 * torch.sum(1 + log_var - mu ** 2 - log_var.exp(), dim=[1, 2, 3]))

        loss = recon_loss + self.kl_weight * kld_loss

        return {"loss": loss, "recon_loss": recon_loss, "kld_loss": kld_loss}

    def training_step(self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> torch.Tensor:
        losses = self.model_step(batch)
        self.log_dict({f"train/{k}": v for k, v in losses.items()}, on_step=True, on_epoch=True, prog_bar=True)
        return losses["loss"]

    def validation_step(self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> None:
        losses = self.model_step(batch)
        self.log_dict({f"val/{k}": v for k, v in losses.items()}, on_step=False, on_epoch=True, prog_bar=True)

    def test_step(self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> None:
        losses = self.model_step(batch)
        self.log_dict({f"test/{k}": v for k, v in losses.items()}, on_step=False, on_epoch=True, prog_bar=True)

    def configure_optimizers(self):
        return Adam(self.parameters(), lr=self.lr)

    @torch.no_grad()
    def calculate_latent_stats(self, dataloader):
        """mimics Wan2.2 scale calculation"""
        all_mus = []
        for batch in dataloader:
            x, _ = batch
            x = x.to(self.device)
            mu, _ = self.encoder(x)
            all_mus.append(mu)

        all_mus = torch.cat(all_mus, dim=0)
        std = all_mus.std()
        # In Wan/SD, they scale latents so they have approx unit variance
        self.scale_factor = 1.0 / std
        print(f"Calculated Scale Factor: {self.scale_factor}")
