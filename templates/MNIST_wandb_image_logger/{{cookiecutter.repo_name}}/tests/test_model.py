import pytest
import torch
from {{cookiecutter.repo_name}}.barebones_lightningmodule import BarebonesLightningModule


@pytest.fixture
def model():
    return BarebonesLightningModule(hidden_size=64, learning_rate=1e-3)


def test_model_init(model):
    """Test if the model initializes correctly."""
    assert isinstance(model, BarebonesLightningModule)
    assert model.hparams.hidden_size == 64
    assert model.hparams.learning_rate == 1e-3


def test_model_forward(model):
    """Test the forward pass of the model."""
    batch_size = 32
    x = torch.randn(batch_size, 28, 28)
    output = model(x)

    assert output.shape == (batch_size, 10)
    assert not torch.isnan(output).any(), "Output contains NaN values"


def test_model_training_step(model):
    """Test the training step of the model."""
    batch_size = 32
    x = torch.randn(batch_size, 28, 28)
    y = torch.randint(0, 10, (batch_size,))
    loss = model.training_step((x, y), 0)

    assert isinstance(loss, torch.Tensor)
    assert loss.shape == ()  # scalar
    assert not torch.isnan(loss).any(), "Loss contains NaN values"


def test_model_validation_step(model):
    """Test the validation step of the model."""
    batch_size = 32
    x = torch.randn(batch_size, 28, 28)
    y = torch.randint(0, 10, (batch_size,))
    model.validation_step((x, y), 0)
    # Validation step logs metrics but doesn't return anything


def test_model_test_step(model):
    """Test the test step of the model."""
    batch_size = 32
    x = torch.randn(batch_size, 28, 28)
    y = torch.randint(0, 10, (batch_size,))
    model.test_step((x, y), 0)
    # Test step logs metrics but doesn't return anything


def test_configure_optimizers(model):
    """Test if the model configures optimizer correctly."""
    optimizer = model.configure_optimizers()
    assert isinstance(optimizer, torch.optim.Adam)
    assert optimizer.defaults["lr"] == model.hparams.learning_rate
