"""Unit tests for _shared/scripts/add_deps.py.

Covers all 9 cases: 3 managers × {runtime dep, dev dep, already-present dep}.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ADD_DEPS = (Path(__file__).parent / ".." / "_shared" / "scripts" / "add_deps.py").resolve()


def _run(dep: str, answers_file: Path, dev: bool = False) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(ADD_DEPS), dep, "--answers-file", str(answers_file)]
    if dev:
        cmd.append("--dev")
    return subprocess.run(cmd, capture_output=True, text=True, cwd=answers_file.parent)


def _write_answers(tmp_path: Path, deps_manager: str) -> Path:
    f = tmp_path / ".copier-answers.yml"
    f.write_text(yaml.dump({"deps_manager": deps_manager, "project_name": "test_proj"}))
    return f


# ── pip ──────────────────────────────────────────────────────────────────────

class TestPip:
    def _setup(self, tmp_path: Path) -> Path:
        (tmp_path / "requirements.txt").write_text("torch>=2.0\n")
        (tmp_path / "requirements_dev.txt").write_text("pytest>=8.0\n")
        return _write_answers(tmp_path, "pip")

    def test_pip_runtime_dep_added(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        result = _run("wandb>=0.16.0", answers)
        assert result.returncode == 0
        content = (tmp_path / "requirements.txt").read_text()
        assert "wandb>=0.16.0" in content

    def test_pip_dev_dep_added(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        result = _run("mypy>=1.0", answers, dev=True)
        assert result.returncode == 0
        content = (tmp_path / "requirements_dev.txt").read_text()
        assert "mypy>=1.0" in content

    def test_pip_runtime_idempotent(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        _run("torch>=2.0", answers)  # already present
        result = _run("torch>=2.0", answers)
        assert result.returncode == 0
        content = (tmp_path / "requirements.txt").read_text()
        assert content.count("torch") == 1, "torch should appear only once"

    def test_pip_dev_idempotent(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        result = _run("pytest>=8.0", answers, dev=True)  # already present
        assert result.returncode == 0
        content = (tmp_path / "requirements_dev.txt").read_text()
        assert content.count("pytest") == 1


# ── uv (pyproject.toml) ──────────────────────────────────────────────────────

_PYPROJECT_UV = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "test_proj"
dependencies = [
    "torch>=2.0",
    "lightning>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
]
"""


class TestUv:
    def _setup(self, tmp_path: Path) -> Path:
        (tmp_path / "pyproject.toml").write_text(_PYPROJECT_UV)
        return _write_answers(tmp_path, "uv")

    def test_uv_runtime_dep_added(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        result = _run("wandb>=0.16.0", answers)
        assert result.returncode == 0
        content = (tmp_path / "pyproject.toml").read_text()
        assert "wandb>=0.16.0" in content

    def test_uv_dev_dep_added(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        result = _run("mypy>=1.0", answers, dev=True)
        assert result.returncode == 0
        content = (tmp_path / "pyproject.toml").read_text()
        assert "mypy>=1.0" in content

    def test_uv_runtime_idempotent(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        _run("torch>=2.0", answers)  # already present
        result = _run("torch>=2.0", answers)
        assert result.returncode == 0
        content = (tmp_path / "pyproject.toml").read_text()
        assert content.count("torch") == 1

    def test_uv_dev_idempotent(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        result = _run("pytest>=8.0", answers, dev=True)  # already present
        assert result.returncode == 0
        content = (tmp_path / "pyproject.toml").read_text()
        assert content.count("pytest") == 1


# ── pixi ─────────────────────────────────────────────────────────────────────

_PIXI_TOML = """\
[project]
name = "test_proj"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64"]

[dependencies]
python = "3.12.*"
torch = "*"

[feature.dev.dependencies]
pytest = "*"

[tasks]
train = "python -m test_proj.train"
"""


class TestPixi:
    def _setup(self, tmp_path: Path) -> Path:
        (tmp_path / "pixi.toml").write_text(_PIXI_TOML)
        return _write_answers(tmp_path, "pixi")

    def test_pixi_runtime_dep_added(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        result = _run("wandb>=0.16.0", answers)
        assert result.returncode == 0
        content = (tmp_path / "pixi.toml").read_text()
        assert "wandb" in content

    def test_pixi_dev_dep_added(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        result = _run("mypy>=1.0", answers, dev=True)
        assert result.returncode == 0
        content = (tmp_path / "pixi.toml").read_text()
        assert "mypy" in content

    def test_pixi_runtime_idempotent(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        _run("torch>=2.0", answers)  # already present
        result = _run("torch>=2.0", answers)
        assert result.returncode == 0
        content = (tmp_path / "pixi.toml").read_text()
        assert content.count("torch") == 1

    def test_pixi_dev_idempotent(self, tmp_path: Path) -> None:
        answers = self._setup(tmp_path)
        result = _run("pytest>=8.0", answers, dev=True)  # already present
        assert result.returncode == 0
        content = (tmp_path / "pixi.toml").read_text()
        assert content.count("pytest") == 1
