"""Copier validator rejection tests for the barebone template."""

from pathlib import Path

import copier
import pytest

BAREBONE_TEMPLATE = (Path(__file__).parent / ".." / "templates" / "barebone").resolve()


def _copy_expect_fail(tmp_path: Path, project_name: str) -> None:
    with pytest.raises(ValueError, match="Validation error"):
        copier.run_copy(
            src_path=str(BAREBONE_TEMPLATE),
            dst_path=str(tmp_path),
            data={"project_name": project_name},
            defaults=True,
            overwrite=True,
            unsafe=True,
        )


def test_rejects_name_starting_with_digit(tmp_path: Path) -> None:
    _copy_expect_fail(tmp_path, "1invalid")


def test_rejects_name_with_spaces(tmp_path: Path) -> None:
    _copy_expect_fail(tmp_path, "my project")


def test_rejects_name_with_uppercase(tmp_path: Path) -> None:
    _copy_expect_fail(tmp_path, "MyModel")


def test_rejects_python_keyword(tmp_path: Path) -> None:
    _copy_expect_fail(tmp_path, "if")


def test_rejects_name_with_hyphens(tmp_path: Path) -> None:
    _copy_expect_fail(tmp_path, "my-project")


@pytest.mark.parametrize("name", ["my_model", "project123", "a", "mnist_classifier"])
def test_accepts_valid_names(name: str, tmp_path: Path) -> None:
    copier.run_copy(
        src_path=str(BAREBONE_TEMPLATE),
        dst_path=str(tmp_path),
        data={"project_name": name},
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    assert (tmp_path / "src" / name).exists()
