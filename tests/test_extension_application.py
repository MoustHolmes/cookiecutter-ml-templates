"""Tests for the Copier extension system.

Each test generates a base project then applies an extension on top,
asserting that extension files appear, base files are untouched, and
the dep injection via add_deps.py worked.
"""

from pathlib import Path
from typing import Any

import copier

REPO_ROOT = (Path(__file__).parent / "..").resolve()
CLASSIFICATION_TEMPLATE = REPO_ROOT / "templates" / "core" / "classification"
IMAGE_LOGGER_EXTENSION = REPO_ROOT / "templates" / "extensions" / "image_logger"


def _generate_cls(dst: Path, **data: Any) -> Path:
    defaults = {
        "project_name": "test_cls",
        "author_name": "Test Author",
        "description": "Test Description",
        "python_version": "3.12",
    }
    defaults.update(data)
    copier.run_copy(
        src_path=str(CLASSIFICATION_TEMPLATE),
        dst_path=str(dst),
        data=defaults,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return dst


def _apply_image_logger(dst: Path, **data: Any) -> Path:
    copier.run_copy(
        src_path=str(IMAGE_LOGGER_EXTENSION),
        dst_path=str(dst),
        data=data,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return dst


def test_image_logger_adds_callback_file(tmp_path: Path) -> None:
    out = _generate_cls(tmp_path / "proj")
    _apply_image_logger(out)

    assert (out / "src" / "test_cls" / "callbacks" / "image_logger.py").exists()


def test_image_logger_adds_hydra_config(tmp_path: Path) -> None:
    out = _generate_cls(tmp_path / "proj")
    _apply_image_logger(out)

    config = out / "configs" / "callbacks" / "image_logger.yaml"
    assert config.exists()
    content = config.read_text()
    assert "test_cls.callbacks.image_logger.ImageLoggerCallback" in content
    assert "log_every_n_batches:" in content
    assert "num_samples:" in content


def test_image_logger_config_respects_custom_values(tmp_path: Path) -> None:
    out = _generate_cls(tmp_path / "proj")
    _apply_image_logger(out, log_every_n_batches=50, num_samples=4)

    content = (out / "configs" / "callbacks" / "image_logger.yaml").read_text()
    assert "log_every_n_batches: 50" in content
    assert "num_samples: 4" in content


def test_image_logger_writes_own_answers_file(tmp_path: Path) -> None:
    out = _generate_cls(tmp_path / "proj")
    _apply_image_logger(out)

    answers = (out / ".copier-answers.image_logger.yml").read_text()
    assert "_src_path:" in answers
    assert "log_every_n_batches:" in answers
    assert "num_samples:" in answers


def test_image_logger_does_not_modify_base_answers(tmp_path: Path) -> None:
    out = _generate_cls(tmp_path / "proj")
    base_answers_before = (out / ".copier-answers.yml").read_text()

    _apply_image_logger(out)

    base_answers_after = (out / ".copier-answers.yml").read_text()
    assert base_answers_before == base_answers_after


def test_image_logger_does_not_overwrite_classification_module(tmp_path: Path) -> None:
    out = _generate_cls(tmp_path / "proj")
    module_before = (out / "src" / "test_cls" / "classification_module.py").read_text()

    _apply_image_logger(out)

    module_after = (out / "src" / "test_cls" / "classification_module.py").read_text()
    assert module_before == module_after


def test_image_logger_adds_wandb_dep_uv(tmp_path: Path) -> None:
    out = _generate_cls(tmp_path / "proj", deps_manager="uv")
    _apply_image_logger(out)

    pyproject = (out / "pyproject.toml").read_text()
    assert "wandb" in pyproject


def test_image_logger_adds_wandb_dep_pip(tmp_path: Path) -> None:
    out = _generate_cls(tmp_path / "proj", deps_manager="pip")
    _apply_image_logger(out)

    requirements = (out / "requirements.txt").read_text()
    assert "wandb" in requirements


def test_image_logger_works_with_different_project_name(tmp_path: Path) -> None:
    out = _generate_cls(tmp_path / "proj", project_name="my_classifier")
    _apply_image_logger(out)

    assert (out / "src" / "my_classifier" / "callbacks" / "image_logger.py").exists()
    config = (out / "configs" / "callbacks" / "image_logger.yaml").read_text()
    assert "my_classifier.callbacks.image_logger.ImageLoggerCallback" in config
