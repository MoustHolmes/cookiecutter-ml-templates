# Testing Strategy

This guide explains the comprehensive testing approach used in both the template repository and generated projects.

## Overview

The project uses a **two-level testing strategy**:

1. **Template Tests** - Validate that templates generate correctly
2. **Integration Tests** - Ensure generated projects actually work

## Template Repository Tests

### Fast Tests (Structural Validation)

These tests run quickly and validate template generation:

```python
# Run only fast tests
pytest tests/
```

**What they check:**

- ✅ Template generates without errors
- ✅ Required files are created
- ✅ Project structure is correct
- ✅ Configuration options work (minimal/full, pip/uv)
- ✅ Input validation (invalid names, versions)

### Slow Tests (Integration Testing)

Integration tests actually run the generated project's tests:

```python
# Run slow tests (marked with @pytest.mark.slow)
pytest tests/ -m slow -v
```

**What they do:**

1. Generate a project from the template
2. Install dependencies (`pip install -r requirements.txt`)
3. Install the package (`pip install -e .`)
4. Run the project's internal test suite
5. Verify all tests pass

!!! info "Why Slow Tests?"
    Integration tests take 30-40 seconds per template because they:
    
    - Create real projects
    - Install actual dependencies
    - Run full test suites
    
    But they catch **real bugs** that structural tests miss!

### Running Specific Tests

```bash
# Run all tests
pytest tests/

# Run only fast tests
pytest tests/ -m "not slow"

# Run only integration tests
pytest tests/ -m slow

# Run specific template integration test
pytest tests/test_create_project.py::test_barebone_template_internal_tests -v
```

## Generated Project Tests

Every generated project includes its own test suite in `tests/`.

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_config.py          # Configuration tests
├── test_data.py            # Data module tests
├── test_model.py           # Model tests
└── test_train_script.py    # Training script tests (if applicable)
```

### Test Categories

#### 1. Configuration Tests (`test_config.py`)

Validates Hydra configuration:

```python
def test_train_config(cfg_train: DictConfig) -> None:
    """Tests the training configuration."""
    assert cfg_train
    assert cfg_train.data
    assert cfg_train.model
    assert cfg_train.trainer
```

**What it checks:**

- Config files load correctly
- Required fields are present
- Can instantiate data modules, models, and trainers

#### 2. Data Tests (`test_data.py`)

Validates data loading and preprocessing:

```python
def test_train_dataloader(datamodule):
    """Test if train_dataloader returns correct format."""
    datamodule.prepare_data()
    datamodule.setup(stage="fit")
    
    loader = datamodule.train_dataloader()
    
    assert isinstance(loader, DataLoader)
    batch = next(iter(loader))
    assert len(batch) == 2  # (x, y)
    assert batch[0].shape[1:] == (1, 28, 28)  # Image shape
```

**What it checks:**

- DataModule initializes correctly
- Dataloaders return proper batches
- Data shapes and types are correct
- Transforms are applied

#### 3. Model Tests (`test_model.py`)

Validates model architecture:

```python
def test_model_forward(model):
    """Test model forward pass."""
    x = torch.randn(2, 1, 28, 28)
    output = model(x)
    
    assert output.shape == (2, 10)  # batch_size, num_classes
```

**What it checks:**

- Model initializes
- Forward pass works
- Output shapes are correct
- Can be trained (backward pass)

#### 4. Training Script Tests (`test_train_script.py`)

End-to-end training validation:

```python
def test_train_script_runs():
    """Test that training script executes."""
    # Run with debug config for speed
    subprocess.run([
        "python", "src/my_project/train.py",
        "experiment=debug"
    ], check=True)
```

## Best Practices

### Writing Tests

!!! tip "Test Pyramid"
    ```
         /\
        /E2E\      ← Few, expensive
       /------\
      /  Integ \   ← Some, moderate
     /----------\
    /   Unit     \  ← Many, fast
    /______________\
    ```

1. **Many unit tests** - Fast, focused on single components
2. **Some integration tests** - Test component interactions
3. **Few E2E tests** - Validate full workflows

### Using Fixtures

Leverage pytest fixtures in `conftest.py`:

```python
@pytest.fixture(scope="function")
def cfg_train() -> DictConfig:
    """Load training configuration."""
    # ... config loading logic
    return cfg
```

Benefits:

- Reusable test setup
- Automatic cleanup
- Clear dependencies

### Parametrized Tests

Test multiple scenarios efficiently:

```python
@pytest.mark.parametrize("stage", ["fit", "test", "predict"])
def test_datamodule_setup(datamodule, stage):
    """Test setup for all stages."""
    datamodule.setup(stage=stage)
    assert datamodule is not None
```

## Debugging Failed Tests

### 1. Check Test Output

```bash
# Run with verbose output
pytest tests/ -v

# Show print statements
pytest tests/ -v -s

# Stop at first failure
pytest tests/ -x
```

### 2. Run Specific Tests

```bash
# Run single test
pytest tests/test_data.py::test_train_dataloader -v

# Run tests matching pattern
pytest tests/ -k "dataloader" -v
```

### 3. Use Debugger

Add breakpoint in test:

```python
def test_model_forward(model):
    x = torch.randn(2, 1, 28, 28)
    breakpoint()  # Debugger stops here
    output = model(x)
```

Then run:

```bash
pytest tests/test_model.py::test_model_forward -v -s
```

## CI/CD Integration

Tests can be automated in GitHub Actions:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -e .
      
      - name: Run fast tests
        run: pytest tests/ -m "not slow"
      
      - name: Run integration tests
        run: pytest tests/ -m slow
```

## Coverage Reports

Track test coverage:

```bash
# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

!!! success "Target Coverage"
    Aim for **>80% coverage** for critical paths:
    
    - Data loading: 90%+
    - Model forward/backward: 85%+
    - Training loop: 70%+

## Example: Adding a New Test

Let's add a test for a custom loss function:

```python
# tests/test_model.py
import torch
import pytest

def test_custom_loss():
    """Test custom loss function."""
    from my_project.losses import CustomLoss
    
    loss_fn = CustomLoss()
    pred = torch.randn(10, 5)  # batch_size=10, classes=5
    target = torch.randint(0, 5, (10,))
    
    loss = loss_fn(pred, target)
    
    # Assertions
    assert loss.item() > 0  # Loss should be positive
    assert loss.requires_grad  # Should be differentiable
    assert not torch.isnan(loss)  # Should not be NaN
```

## Common Testing Patterns

### Testing Data Transformations

```python
def test_transforms():
    """Test that transforms are applied correctly."""
    from torchvision import transforms
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    
    # Create dummy image
    img = Image.new('L', (28, 28), color=128)
    tensor = transform(img)
    
    assert tensor.shape == (1, 28, 28)
    assert -1 <= tensor.min() <= tensor.max() <= 1
```

### Testing Model Device Placement

```python
@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
def test_model_on_gpu(model):
    """Test model works on GPU."""
    model = model.cuda()
    x = torch.randn(2, 1, 28, 28).cuda()
    
    output = model(x)
    
    assert output.is_cuda
```

### Testing Checkpoint Saving/Loading

```python
def test_checkpoint_save_load(model, tmp_path):
    """Test model can be saved and loaded."""
    checkpoint_path = tmp_path / "model.ckpt"
    
    # Save
    torch.save(model.state_dict(), checkpoint_path)
    
    # Load
    new_model = type(model)(**model_config)
    new_model.load_state_dict(torch.load(checkpoint_path))
    
    # Compare
    for p1, p2 in zip(model.parameters(), new_model.parameters()):
        assert torch.allclose(p1, p2)
```

## Further Reading

- [Pytest Documentation](https://docs.pytest.org/)
- [PyTorch Testing Best Practices](https://pytorch.org/docs/stable/notes/testing.html)
- [Lightning Testing](https://lightning.ai/docs/pytorch/stable/common/trainer.html#testing)
