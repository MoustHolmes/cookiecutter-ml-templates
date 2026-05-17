# Testing Strategy

Tests validate template generation using the [Copier](https://copier.readthedocs.io/) Python API.

## Test Files

| File | What it tests |
|------|--------------|
| `test_base_generation.py` | Structure, deps variants, config naming, answers file — for all four base templates |
| `test_validation.py` | `validator:` rejection tests (invalid project names) |
| `test_extension_application.py` | Apply extensions on top of base, assert new files appear, base files untouched, deps injected |
| `test_add_deps.py` | Unit tests for `_shared/scripts/add_deps.py` across all three deps managers |

## Running Tests

```bash
# Fast tests (run on every commit)
pytest tests/ -m "not slow" -v

# Slow integration tests (run on main branch merges)
pytest tests/ -m slow -v

# Single template
pytest tests/test_base_generation.py -k "barebone" -v
```

## Test Layers

### Fast tests — structure and generation

Use `copier.run_copy()` with `defaults=True` and `unsafe=True`. Assert expected files/directories exist and file contents match. Run in seconds.

```python
copier.run_copy(
    src_path=str(TEMPLATE_DIR),
    dst_path=str(dst),
    data={"project_name": "test_proj", "deps_manager": "uv"},
    defaults=True,
    overwrite=True,
    unsafe=True,
)
```

### Slow integration tests — internal test suite

Generate a project, install its dependencies, run its own `pytest tests/` suite. Catches bugs that structural tests miss. Marked `@pytest.mark.slow` and excluded from the default run.

## CI

- **Fast tests**: run on every push and pull request, across Python 3.11 and 3.12
- **Slow tests**: run only on main branch merges (see `.github/workflows/ci.yml`)
