"""WandB image logger callback — logs generated samples and reconstructions each validation epoch."""

from __future__ import annotations

import lightning as L
import torch
import torchvision

try:
    import wandb
    _WANDB_AVAILABLE = True
except ImportError:
    _WANDB_AVAILABLE = False


class VAEImageLoggerCallback(L.Callback):
    """Logs a grid of generated samples (and reconstructions) to WandB.

    Captures a fixed batch from the first validation step so reconstructions
    are comparable across epochs.

    Args:
        num_samples: Number of images to generate / reconstruct.
        every_n_epochs: Log every N validation epochs (1 = every epoch).
    """

    def __init__(self, num_samples: int = 8, every_n_epochs: int = 1) -> None:
        super().__init__()
        self.num_samples = num_samples
        self.every_n_epochs = every_n_epochs
        self._fixed_batch: torch.Tensor | None = None

    def on_validation_batch_end(
        self,
        trainer: L.Trainer,
        pl_module: L.LightningModule,
        outputs,
        batch: tuple,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> None:
        if self._fixed_batch is None and batch_idx == 0:
            x, _ = batch
            self._fixed_batch = x[: self.num_samples].detach().cpu()

    def on_validation_epoch_end(
        self, trainer: L.Trainer, pl_module: L.LightningModule
    ) -> None:
        if not _WANDB_AVAILABLE:
            return
        if trainer.logger is None or not hasattr(trainer.logger, "experiment"):
            return
        if (trainer.current_epoch + 1) % self.every_n_epochs != 0:
            return

        device = pl_module.device
        images: dict = {}

        with torch.no_grad():
            samples = pl_module.generate(self.num_samples).cpu()
            images["generated/samples"] = wandb.Image(
                _make_grid_numpy(samples)
            )

            if self._fixed_batch is not None:
                originals = self._fixed_batch.to(device)
                mu, log_var = pl_module.encoder(originals)
                z = pl_module.reparameterize(mu, log_var)
                recons = pl_module.decoder(z).cpu()
                images["generated/originals"] = wandb.Image(
                    _make_grid_numpy(self._fixed_batch)
                )
                images["generated/reconstructions"] = wandb.Image(
                    _make_grid_numpy(recons)
                )

        # commit=False lets Lightning batch this with the next metrics commit
        trainer.logger.experiment.log(images, commit=False)


def _make_grid_numpy(images: torch.Tensor, nrow: int = 4):
    grid = torchvision.utils.make_grid(images.detach(), nrow=nrow, normalize=True)
    return grid.permute(1, 2, 0).numpy()
