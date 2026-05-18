"""Slow integration tests: generate each template, install its deps, run its test suite."""

import subprocess
from pathlib import Path
from typing import Any

import copier
import pytest

REPO_ROOT = (Path(__file__).parent / "..").resolve()
BAREBONE_TEMPLATE = REPO_ROOT / "templates" / "barebone"
CLASSIFICATION_TEMPLATE = REPO_ROOT / "templates" / "core" / "classification"
FLOW_MATCHING_TEMPLATE = REPO_ROOT / "templates" / "generative" / "flow_matching"
RL_TEMPLATE = REPO_ROOT / "templates" / "rl"

_BASE_DATA: dict[str, Any] = {
    "user_name": "Test Author",
    "user_email": "test@example.com",
    "description": "Integration test project",
    "deps_manager": "uv",
}


def _generate(src: Path, dst: Path, **data: Any) -> Path:
    copier.run_copy(
        src_path=str(src),
        dst_path=str(dst),
        data={**_BASE_DATA, **data},
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return dst


def _run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


@pytest.mark.slow
def test_barebone_generated_tests_pass(tmp_path: Path) -> None:
    """Generate barebone project, install deps, verify model and config tests pass."""
    dst = _generate(BAREBONE_TEMPLATE, tmp_path, project_name="test_project")
    _run(["uv", "sync", "--extra", "dev"], dst)
    _run(["uv", "run", "pytest", "tests/test_model.py", "tests/test_config.py", "-x", "-q"], dst)


@pytest.mark.slow
def test_classification_generated_tests_pass(tmp_path: Path) -> None:
    """Generate classification project, install deps, verify model tests pass."""
    dst = _generate(CLASSIFICATION_TEMPLATE, tmp_path, project_name="test_cls")
    _run(["uv", "sync", "--extra", "dev"], dst)
    _run(["uv", "run", "pytest", "tests/test_model.py", "-x", "-q"], dst)


@pytest.mark.slow
def test_flow_matching_generated_tests_pass(tmp_path: Path) -> None:
    """Generate flow matching project, install deps, verify model and config tests pass."""
    dst = _generate(FLOW_MATCHING_TEMPLATE, tmp_path, project_name="test_flow")
    _run(["uv", "sync", "--extra", "dev"], dst)
    _run(["uv", "run", "pytest", "tests/test_model.py", "tests/test_config.py", "-x", "-q"], dst)


@pytest.mark.slow
def test_rl_generated_tests_pass(tmp_path: Path) -> None:
    """Generate RL project, install deps, verify model, config, data, and train tests pass."""
    dst = _generate(RL_TEMPLATE, tmp_path, project_name="test_rl", python_version="3.11")
    _run(["uv", "sync", "--extra", "dev"], dst)
    _run(
        ["uv", "run", "pytest",
         "tests/test_model.py", "tests/test_config.py",
         "tests/test_data.py", "tests/test_train_script.py",
         "-x", "-q"],
        dst,
    )
