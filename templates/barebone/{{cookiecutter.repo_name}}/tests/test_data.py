from pathlib import Path

import pytest
import torch
from torch.utils.data import DataLoader

from {{cookiecutter.repo_name}}.barebones_datamodule import BarebonesDataModule


@pytest.fixture
def data_dir(tmp_path):
    return str(tmp_path / "data")


@pytest.fixture
def datamodule(data_dir):
    return BarebonesDataModule(
        data_dir=data_dir,
        batch_size=32,
        num_workers=0,
    )


def test_datamodule_attributes(datamodule):
    """Test if the datamodule has the correct attributes."""
    assert datamodule.hparams.batch_size == 32
    assert datamodule.hparams.num_workers == 0
    assert isinstance(datamodule.transforms, torch.nn.Module)


def test_prepare_data(datamodule):
    """Test prepare_data creates the required files."""
    datamodule.prepare_data()
    data_path = Path(datamodule.hparams.data_dir)
    assert (data_path / "MNIST").exists()


def test_setup(datamodule):
    """Test setup creates the correct splits."""
    datamodule.prepare_data()
    datamodule.setup(stage="fit")

    assert datamodule.data_train is not None
    assert datamodule.data_val is not None
    assert len(datamodule.data_train) == 55000
    assert len(datamodule.data_val) == 5000

    datamodule.setup(stage="test")
    assert datamodule.data_test is not None
    assert len(datamodule.data_test) == 10000


def test_train_dataloader(datamodule):
    """Test if train_dataloader returns the correct type and batch size."""
    datamodule.prepare_data()
    datamodule.setup(stage="fit")

    loader = datamodule.train_dataloader()

    assert isinstance(loader, DataLoader)
    assert loader.batch_size == datamodule.hparams.batch_size

    batch = next(iter(loader))
    assert len(batch) == 2  # (x, y) tuple
    assert batch[0].shape[1:] == (28, 28)  # Image dimensions
    assert batch[1].shape[0] == datamodule.hparams.batch_size  # Labels


def test_val_dataloader(datamodule):
    """Test if val_dataloader returns the correct type and batch size."""
    datamodule.prepare_data()
    datamodule.setup(stage="fit")

    loader = datamodule.val_dataloader()

    assert isinstance(loader, DataLoader)
    assert loader.batch_size == datamodule.hparams.batch_size

    batch = next(iter(loader))
    assert len(batch) == 2
    assert batch[0].shape[1:] == (28, 28)
    assert batch[1].shape[0] == datamodule.hparams.batch_size


def test_test_dataloader(datamodule):
    """Test if test_dataloader returns the correct type and batch size."""
    datamodule.prepare_data()
    datamodule.setup(stage="test")

    loader = datamodule.test_dataloader()

    assert isinstance(loader, DataLoader)
    assert loader.batch_size == datamodule.hparams.batch_size

    batch = next(iter(loader))
    assert len(batch) == 2
    assert batch[0].shape[1:] == (28, 28)
    assert batch[1].shape[0] == datamodule.hparams.batch_size
