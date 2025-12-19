from typing import Optional

import lightning as L
import torch
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from torchvision.datasets import MNIST


class BarebonesDataModule(L.LightningDataModule):
    def __init__(
        self,
        data_dir: str = "data/",
        batch_size: int = 32,
        num_workers: int = 0,
    ):
        super().__init__()
        self.save_hyperparameters()

        self.transforms = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        )

    def prepare_data(self):
        """Download data if needed. This method is called only from a single process."""
        MNIST(self.hparams.data_dir, train=True, download=True)
        MNIST(self.hparams.data_dir, train=False, download=True)

    def setup(self, stage: Optional[str] = None):
        """Load data. Set variables: `self.data_train`, `self.data_val`, `self.data_test`."""
        if stage == "fit" or stage is None:
            mnist_full = MNIST(
                self.hparams.data_dir, train=True, transform=self.transforms
            )
            self.data_train, self.data_val = random_split(mnist_full, [55000, 5000])

        if stage == "test" or stage is None:
            self.data_test = MNIST(
                self.hparams.data_dir, train=False, transform=self.transforms
            )

    def train_dataloader(self):
        return DataLoader(
            self.data_train,
            batch_size=self.hparams.batch_size,
            num_workers=self.hparams.num_workers,
            shuffle=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.data_val,
            batch_size=self.hparams.batch_size,
            num_workers=self.hparams.num_workers,
            shuffle=False,
        )

    def test_dataloader(self):
        return DataLoader(
            self.data_test,
            batch_size=self.hparams.batch_size,
            num_workers=self.hparams.num_workers,
            shuffle=False,
        )
