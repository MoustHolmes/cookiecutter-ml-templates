# Testing Strategy

This project uses a multi-layered testing approach to ensure the cookiecutter templates work correctly.

## Test Layers

### 1. Fast Tests (Structure & Generation)
These tests run quickly and verify that:
- Templates generate successfully
- Required files and directories exist
- File contents match expectations
- Hook validation logic works correctly

**Run with:**
```bash
pytest tests/ -v -m "not slow"
```

### 2. Slow Integration Tests  
These tests take longer as they:
1. Generate a complete project from a template
2. Install all dependencies in a temporary environment
3. Run the generated project's internal test suite

These tests catch real bugs in the generated templates that structural tests might miss.

**Run with:**
```bash
pytest tests/ -v -m "slow"
```

**Run all tests:**
```bash
pytest tests/ -v
```

## Current Status

### Barebone Template
- ✅ Structure tests pass
- ⚠️ Integration tests reveal issues that need fixing:
  - Missing `configs/data/default_data_module.yaml`
  - Data module test assertions need updating
  - Transform initialization issues

### Flow Matching Template
- ✅ Structure tests pass
- 🔄 Integration tests not yet run (too complex for initial implementation)

## Future Work

1. Fix barebone template issues found by integration tests
2. Add integration tests for other templates (MNIST_wandb, classification)
3. Consider creating simplified "smoke test" versions that don't require full dependency installation
4. Add CI/CD caching for faster integration test runs

## Notes

Integration tests are marked with `@pytest.mark.slow` to allow developers to skip them during rapid development:

```python
@pytest.mark.slow
def test_barebone_template_internal_tests(temp_dir: Path) -> None:
    """Full integration test that runs generated project's tests."""
    ...
```
