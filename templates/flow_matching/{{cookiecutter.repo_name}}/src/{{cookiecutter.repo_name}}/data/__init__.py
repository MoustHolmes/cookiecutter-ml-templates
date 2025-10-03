"""Data modules for diffusion playground."""

from {{cookiecutter.repo_name}}.data.MNIST_datamodule import MNISTDataModule
from {{cookiecutter.repo_name}}.data.moons_datamodule import MoonsDataModule

__all__ = [
    "MNISTDataModule",
    "MoonsDataModule",
]
