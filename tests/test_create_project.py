"""Tests for cookiecutter template generation."""

from pathlib import Path

import pytest
from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter


@pytest.fixture()
def temp_dir(tmp_path: Path) -> Path:
    """Provide a temporary directory for tests.

    Args:
        tmp_path: pytest fixture providing temporary directory

    Returns:
        Path to temporary directory
    """
    return tmp_path


def test_barebone_template_success(temp_dir: Path) -> None:
    """Test successful generation of barebone template.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "barebone_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    # Generate project
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_project",
            "author_name": "Test Author",
            "description": "Test Description",
            "python_version": "3.10",
        },
    )

    # Check if critical files exist
    generated_dir = output_dir / "test_project"
    # We use pytest's assert since this is a test file
    assert generated_dir.exists()
    assert (generated_dir / "README.md").exists()
    assert (generated_dir / "pyproject.toml").exists()


def test_project_name_with_number_prefix(temp_dir: Path) -> None:
    """Test that project name cannot start with a number.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "invalid_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    with pytest.raises(FailedHookException):
        cookiecutter(
            template=str(template_dir),
            output_dir=str(output_dir),
            no_input=True,
            extra_context={
                "project_name": "1test_project",
                "author_name": "Test Author",
                "description": "Test Description",
                "python_version": "3.10",
            },
        )


def test_project_name_with_spaces(temp_dir: Path) -> None:
    """Test that project name cannot contain spaces.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "invalid_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    with pytest.raises(FailedHookException):
        cookiecutter(
            template=str(template_dir),
            output_dir=str(output_dir),
            no_input=True,
            extra_context={
                "project_name": "Test Project",
                "author_name": "Test Author",
                "description": "Test Description",
                "python_version": "3.10",
            },
        )


def test_project_name_with_special_chars(temp_dir: Path) -> None:
    """Test that project name cannot contain special characters.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "invalid_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    with pytest.raises(FailedHookException):
        cookiecutter(
            template=str(template_dir),
            output_dir=str(output_dir),
            no_input=True,
            extra_context={
                "project_name": "test-project!",
                "author_name": "Test Author",
                "description": "Test Description",
                "python_version": "3.10",
            },
        )


def test_invalid_python_version(temp_dir: Path) -> None:
    """Test that invalid Python version is rejected.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "invalid_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    with pytest.raises(FailedHookException):
        cookiecutter(
            template=str(template_dir),
            output_dir=str(output_dir),
            no_input=True,
            extra_context={
                "project_name": "test_project",
                "author_name": "Test Author",
                "description": "Test Description",
                "python_version": "3.9",
            },
        )


def test_classification_template_success(temp_dir: Path) -> None:
    """Test successful generation of classification template.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "classification_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "classification").resolve()

    # Generate project
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_classification",
            "author_name": "Test Author",
            "description": "Test Description",
            "python_version": "3.10",
        },
    )

    # Check if critical files and directories exist
    generated_dir = output_dir / "test_classification"
    # We use pytest's assert since this is a test file
    assert generated_dir.exists()
    assert (generated_dir / "src").exists()
    assert (generated_dir / "tests").exists()
    assert (generated_dir / "configs").exists()
    assert (generated_dir / "data").exists()
    assert (generated_dir / "pyproject.toml").exists()


def test_project_structure(temp_dir: Path) -> None:
    """Test that generated project has correct structure.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "structure_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_structure",
            "author_name": "Test Author",
            "description": "Test Description",
            "python_version": "3.10",
        },
    )

    generated_dir = output_dir / "test_structure"
    # We use pytest's assert since this is a test file
    assert generated_dir.exists()

    # Check project structure matches ml_ops template structure
    assert (generated_dir / "src").exists()
    assert (generated_dir / "src" / "test_structure").exists()
    assert (generated_dir / "src" / "test_structure" / "__init__.py").exists()
    assert (generated_dir / "configs").exists()
    assert (generated_dir / "data" / "raw").exists()
    assert (generated_dir / "data" / "processed").exists()
    assert (generated_dir / "tests").exists()
    assert (generated_dir / "tests" / "__init__.py").exists()
    assert (generated_dir / "notebooks").exists()
    assert (generated_dir / "docs").exists()
    assert (generated_dir / "docs" / "mkdocs.yaml").exists()
    assert (generated_dir / "requirements.txt").exists()
    assert (generated_dir / "requirements_dev.txt").exists()
    assert (generated_dir / "tasks.py").exists()
