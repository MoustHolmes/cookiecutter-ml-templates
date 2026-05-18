"""VAE LightningModule — ELBO loss, reparameterisation trick, optional β-VAE."""

from __future__ import annotations

from typing import Callable, Optional

import lightning as L
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class VAEModule(L.LightningModule):
    """Training wrapper for a Variational Autoencoder.

    Implements the ELBO objective:
        loss = recon_loss + beta * kl_loss

    When kl_warmup_epochs > 0 (β-VAE mode), beta is linearly annealed from 0
    to its target value over the first kl_warmup_epochs epochs.

    Args:
        encoder: Maps x → (mu, log_var).
        decoder: Maps z → x_recon.
        optimizer: Partial optimizer constructor (use _partial_: true in Hydra).
        latent_dim: Dimension of z — used by generate().
        beta: KL weight. 1.0 = standard VAE; >1 = β-VAE.
        kl_warmup_epochs: Linearly ramp beta from 0 over this many epochs.
            Set to 0 to disable annealing.
        lr_scheduler: Optional partial LR scheduler constructor.
    """

    def __init__(
        self,
        encoder: nn.Module,
        decoder: nn.Module,
        optimizer: Callable,
        latent_dim: int,
        beta: float = 1.0,
        kl_warmup_epochs: int = 0,
        lr_scheduler: Optional[Callable] = None,
    ) -> None:
        super().__init__()
        self.save_hyperparameters(logger=False, ignore=["encoder", "decoder"])
        self.encoder = encoder
        self.decoder = decoder
        self._current_beta = 0.0 if kl_warmup_epochs > 0 else beta

    def reparameterize(self, mu: Tensor, log_var: Tensor) -> Tensor:
        std = torch.exp(0.5 * log_var)
        return mu + std * torch.randn_like(std)

    def model_step(self, batch: tuple) -> dict[str, Tensor]:
        x, _ = batch
        mu, log_var = self.encoder(x)
        z = self.reparameterize(mu, log_var)
        x_recon = self.decoder(z)

        recon_loss = F.mse_loss(x_recon, x)
        kl_loss = -0.5 * torch.mean(1 + log_var - mu.pow(2) - log_var.exp())
        loss = recon_loss + self._current_beta * kl_loss

        return {"loss": loss, "recon_loss": recon_loss, "kl_loss": kl_loss}

    def training_step(self, batch: tuple, batch_idx: int) -> Tensor:
        losses = self.model_step(batch)
        self.log_dict(
            {f"train/{k}": v for k, v in losses.items()},
            on_step=False,
            on_epoch=True,
            prog_bar=True,
        )
        return losses["loss"]

    def validation_step(self, batch: tuple, batch_idx: int) -> None:
        losses = self.model_step(batch)
        self.log_dict(
            {f"val/{k}": v for k, v in losses.items()},
            on_step=False,
            on_epoch=True,
            prog_bar=True,
        )

    def test_step(self, batch: tuple, batch_idx: int) -> None:
        losses = self.model_step(batch)
        self.log_dict(
            {f"test/{k}": v for k, v in losses.items()},
            on_step=False,
            on_epoch=True,
        )

    def on_train_epoch_start(self) -> None:
        if self.hparams.kl_warmup_epochs > 0:
            progress = min(1.0, self.current_epoch / self.hparams.kl_warmup_epochs)
            self._current_beta = self.hparams.beta * progress

    @torch.no_grad()
    def generate(self, num_samples: int) -> Tensor:
        """Sample from the prior and decode."""
        z = torch.randn(num_samples, self.hparams.latent_dim, device=self.device)
        return self.decoder(z)

    def configure_optimizers(self) -> dict:
        optimizer = self.hparams.optimizer(self.parameters())
        if self.hparams.lr_scheduler is None:
            return {"optimizer": optimizer}
        scheduler = self.hparams.lr_scheduler(optimizer)
        return {
            "optimizer": optimizer,
            "lr_scheduler": scheduler,
            "monitor": "val/loss",
        }
