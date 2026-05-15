# Testing Templates

How the test suite validates generated projects.

## Test Structure

Tests live in `tests/test_create_project.py`. Each template has:

1. A structure test — asserts expected files exist after generation
2. Optionally, variant tests — one per `deps_manager` value
3. A slow integration test — generates the project, installs dependencies, runs its internal `pytest` suite

## Running Tests

```bash
# Fast tests only (structure assertions, no installs)
pytest tests/ -m "not slow"

# Single test
pytest tests/test_create_project.py::test_barebone_template_success

# Slow integration tests (full install + internal test suite)
pytest tests/ -m slow
```

## Writing Tests

Use the `copier` Python API directly — `copier.run_copy()` replaces the old `cookiecutter()` call:

```python
import copier
from pathlib import Path
import pytest


def test_my_template_structure(temp_dir: Path) -> None:
    """Assert expected files exist after generation."""
    template_dir = (
        Path(__file__).parent / ".." / "templates" / "my_category" / "my_template"
    ).resolve()

    copier.run_copy(
        src_path=str(template_dir),
        dst_path=str(temp_dir),
        data={"project_name": "test_proj", "python_version": "3.12"},
        defaults=True,
        overwrite=True,
        trust=True,
    )

    assert (temp_dir / "src" / "test_proj").exists()
    assert (temp_dir / "tests").exists()
    assert (temp_dir / "configs").exists()
    assert (temp_dir / ".copier-answers.yml").exists()
    assert (temp_dir / "pyproject.toml").exists()


@pytest.mark.parametrize("deps_manager", ["pip", "uv", "pixi"])
def test_my_template_deps_variants(temp_dir: Path, deps_manager: str) -> None:
    template_dir = (
        Path(__file__).parent / ".." / "templates" / "my_category" / "my_template"
    ).resolve()

    copier.run_copy(
        src_path=str(template_dir),
        dst_path=str(temp_dir),
        data={"project_name": "test_proj", "deps_manager": deps_manager},
        defaults=True,
        overwrite=True,
        trust=True,
    )

    if deps_manager == "pip":
        assert (temp_dir / "requirements.txt").exists()
    elif deps_manager == "pixi":
        assert (temp_dir / "pixi.toml").exists()
    # uv uses pyproject.toml, which is always present


@pytest.mark.slow
def test_my_template_internal_tests(temp_dir: Path) -> None:
    """Generate project, install deps, run its test suite."""
    import subprocess

    template_dir = (
        Path(__file__).parent / ".." / "templates" / "my_category" / "my_template"
    ).resolve()

    copier.run_copy(
        src_path=str(template_dir),
        dst_path=str(temp_dir),
        data={"project_name": "test_proj", "deps_manager": "pip"},
        defaults=True,
        overwrite=True,
        trust=True,
    )

    subprocess.run(["pip", "install", "-e", ".[dev]"], cwd=temp_dir, check=True)
    subprocess.run(["pytest", "tests/"], cwd=temp_dir, check=True)
```

## Key differences from Cookiecutter tests

- `copier.run_copy()` instead of `cookiecutter()`
- `dst_path` is the directory receiving generated files (no extra project subdirectory — files land directly in `temp_dir`)
- `data=` instead of `extra_context=`
- `defaults=True` skips prompts; `overwrite=True` lets tests re-run cleanly into the same temp dir
- `trust=True` is required when the template uses `_tasks:`
- Check for `.copier-answers.yml` instead of `cookiecutter.json`

## Integration Tests

Slow integration tests (`@pytest.mark.slow`) are the authoritative check that a generated project actually works. They:

1. Call `copier.run_copy()` into a temp directory
2. Install the generated project with `pip install -e ".[dev]"`
3. Run the generated project's own `pytest tests/` suite

Run them before merging any change that touches template source files:

```bash
pytest tests/ -m slow -v
```
