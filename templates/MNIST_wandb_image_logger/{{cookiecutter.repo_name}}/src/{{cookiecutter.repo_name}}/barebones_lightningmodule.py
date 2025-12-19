import lightning as L
import torch
import torch.nn as nn
import torch.nn.functional as F


class BarebonesLightningModule(L.LightningModule):
    def __init__(
        self,
        hidden_size: int = 64,
        learning_rate: float = 1e-3,
    ):
        super().__init__()
        self.save_hyperparameters()

        # Simple feed-forward network
        self.layer = nn.Linear(28 * 28, hidden_size)
        self.layer2 = nn.Linear(hidden_size, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass of the model.

        Args:
            x: Input tensor of shape (batch_size, 28, 28)

        Returns:
            torch.Tensor: Output tensor of shape (batch_size, 10)
        """
        x = x.view(x.size(0), -1)
        x = F.relu(self.layer(x))
        x = self.layer2(x)
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        self.log("val_loss", loss)

    def test_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        self.log("test_loss", loss)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)
