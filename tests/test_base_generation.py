"""Copier-based generation tests for the barebone template."""

from pathlib import Path

import copier
import pytest

REPO_ROOT = (Path(__file__).parent / "..").resolve()
BAREBONE_TEMPLATE = REPO_ROOT / "templates" / "barebone"


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


def _generate(dst: Path, **data) -> Path:
    defaults = {
        "project_name": "test_project",
        "author_name": "Test Author",
        "description": "Test Description",
        "python_version": "3.12",
    }
    defaults.update(data)
    copier.run_copy(
        src_path=str(BAREBONE_TEMPLATE),
        dst_path=str(dst),
        data=defaults,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return dst


def test_barebone_full_structure(temp_dir: Path) -> None:
    out = _generate(temp_dir / "full")

    assert (out / "src" / "test_project").exists()
    assert (out / "src" / "test_project" / "__init__.py").exists()
    assert (out / "src" / "test_project" / "train.py").exists()
    assert (out / "src" / "test_project" / "barebones_lightningmodule.py").exists()
    assert (out / "src" / "test_project" / "models" / "__init__.py").exists()
    assert (out / "src" / "test_project" / "data" / "__init__.py").exists()
    assert (out / "src" / "test_project" / "data" / "barebones_datamodule.py").exists()

    assert (out / "configs" / "train_config.yaml").exists()
    assert (out / "configs" / "paths_config.yaml").exists()
    assert (out / "configs" / "model" / "default_model.yaml").exists()
    assert (out / "configs" / "data" / "default_data_module.yaml").exists()
    assert (out / "configs" / "trainer" / "default_trainer.yaml").exists()
    assert (out / "configs" / "logger" / "wandb_logger.yaml").exists()
    assert (out / "configs" / "callbacks" / "default_callbacks.yaml").exists()

    assert (out / "tests" / "__init__.py").exists()
    assert (out / "tests" / "conftest.py").exists()
    assert (out / "tests" / "test_config.py").exists()
    assert (out / "tests" / "test_data.py").exists()
    assert (out / "tests" / "test_model.py").exists()

    assert (out / "docs" / "mkdocs.yaml").exists()
    assert (out / "data" / "README.md").exists()
    assert (out / "notebooks" / ".gitkeep").exists()
    assert (out / "reports" / "figures" / ".gitkeep").exists()

    assert (out / "pyproject.toml").exists()
    assert (out / "README.md").exists()
    assert (out / ".gitignore").exists()
    assert (out / ".pre-commit-config.yaml").exists()
    assert (out / ".copier-answers.yml").exists()


def test_barebone_minimal_no_docs(temp_dir: Path) -> None:
    out = _generate(temp_dir / "minimal", project_structure="minimal")

    assert not (out / "docs").exists()
    assert (out / "src" / "test_project").exists()
    assert (out / "tests").exists()

    tasks = (out / "tasks.py").read_text()
    assert "def build_docs" not in tasks
    assert "def serve_docs" not in tasks
    assert "def test" in tasks
    assert "def train" in tasks


def test_barebone_pip_deps_manager(temp_dir: Path) -> None:
    out = _generate(temp_dir / "pip", deps_manager="pip")

    assert (out / "requirements.txt").exists()
    assert (out / "requirements_dev.txt").exists()
    assert not (out / "pixi.toml").exists()

    tasks = (out / "tasks.py").read_text()
    assert "pip install" in tasks
    assert "uv run" not in tasks


def test_barebone_uv_deps_manager(temp_dir: Path) -> None:
    out = _generate(temp_dir / "uv", deps_manager="uv")

    assert not (out / "requirements.txt").exists()
    assert not (out / "pixi.toml").exists()

    pyproject = (out / "pyproject.toml").read_text()
    assert "dependencies = [" in pyproject
    assert "[project.optional-dependencies]" in pyproject

    tasks = (out / "tasks.py").read_text()
    assert "uv run" in tasks


def test_barebone_pixi_deps_manager(temp_dir: Path) -> None:
    out = _generate(temp_dir / "pixi", deps_manager="pixi")

    assert (out / "pixi.toml").exists()
    assert not (out / "requirements.txt").exists()
    assert not (out / "tasks.py").exists()


def test_barebone_mit_license(temp_dir: Path) -> None:
    out = _generate(temp_dir / "mit", open_source_license="MIT")
    assert (out / "LICENSE").exists()
    assert "MIT" in (out / "LICENSE").read_text()


def test_barebone_no_license(temp_dir: Path) -> None:
    out = _generate(temp_dir / "nolicense", open_source_license="No license file")
    assert not (out / "LICENSE").exists()


def test_barebone_config_uses_repo_name(temp_dir: Path) -> None:
    out = _generate(temp_dir / "naming", project_name="my_model")
    model_cfg = (out / "configs" / "model" / "default_model.yaml").read_text()
    assert "my_model.barebones_lightningmodule" in model_cfg
    data_cfg = (out / "configs" / "data" / "default_data_module.yaml").read_text()
    assert "my_model.data.barebones_datamodule" in data_cfg


def test_barebone_answers_file_written(temp_dir: Path) -> None:
    out = _generate(temp_dir / "answers")
    answers = (out / ".copier-answers.yml").read_text()
    assert "project_name: test_project" in answers
    assert "_src_path:" in answers
