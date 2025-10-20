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

    # Check project structure matches the new gold standard (flow_matching template)
    # Root level structure
    assert (generated_dir / "src").exists()
    assert (generated_dir / "configs").exists()
    assert (generated_dir / "data").exists()
    assert (generated_dir / "tests").exists()
    assert (generated_dir / "notebooks").exists()
    assert (generated_dir / "docs").exists()
    assert (generated_dir / "reports").exists()

    # Source directory should use repo_name (not project_name) for consistency
    assert (generated_dir / "src" / "test_structure").exists()
    assert (generated_dir / "src" / "test_structure" / "__init__.py").exists()

    # Check for organized module structure (gold standard)
    assert (generated_dir / "src" / "test_structure" / "models").exists()
    assert (generated_dir / "src" / "test_structure" / "models" / "__init__.py").exists()
    assert (generated_dir / "src" / "test_structure" / "data").exists()
    assert (generated_dir / "src" / "test_structure" / "data" / "__init__.py").exists()

    # Check for train.py in the package root (not in models/)
    assert (generated_dir / "src" / "test_structure" / "train.py").exists()

    # Check config structure
    assert (generated_dir / "configs" / "train_config.yaml").exists()
    assert (generated_dir / "configs" / "paths_config.yaml").exists()
    assert (generated_dir / "configs" / "model").exists()
    assert (generated_dir / "configs" / "data").exists()
    assert (generated_dir / "configs" / "trainer").exists()
    assert (generated_dir / "configs" / "logger").exists()
    assert (generated_dir / "configs" / "callbacks").exists()

    # Check data structure
    assert (generated_dir / "data" / "README.md").exists()

    # Check test structure
    assert (generated_dir / "tests" / "__init__.py").exists()
    assert (generated_dir / "tests" / "conftest.py").exists()
    assert (generated_dir / "tests" / "test_config.py").exists()
    assert (generated_dir / "tests" / "test_data.py").exists()
    assert (generated_dir / "tests" / "test_model.py").exists()

    # Check documentation
    assert (generated_dir / "docs" / "mkdocs.yaml").exists()

    # Check root level files
    assert (generated_dir / "requirements.txt").exists()
    assert (generated_dir / "requirements_dev.txt").exists()
    assert (generated_dir / "tasks.py").exists()
    assert (generated_dir / "pyproject.toml").exists()
    assert (generated_dir / "README.md").exists()
    assert (generated_dir / ".gitignore").exists()
    assert (generated_dir / ".pre-commit-config.yaml").exists()
    assert (generated_dir / "LICENSE").exists()


def test_mnist_wandb_image_logger_template_success(temp_dir: Path) -> None:
    """Test successful generation of MNIST_wandb_image_logger template.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "mnist_wandb_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "MNIST_wandb_image_logger").resolve()

    # Generate project
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_mnist_wandb",
            "author_name": "Test Author",
            "description": "Test MNIST WandB Image Logger",
            "python_version": "3.12",
            "open_source_license": "MIT",
        },
    )

    # Check if critical files and directories exist
    generated_dir = output_dir / "test_mnist_wandb"
    assert generated_dir.exists()
    assert (generated_dir / "src").exists()
    assert (generated_dir / "tests").exists()
    assert (generated_dir / "configs").exists()
    assert (generated_dir / "data").exists()
    assert (generated_dir / "docs").exists()
    assert (generated_dir / "notebooks").exists()
    assert (generated_dir / "logs").exists()
    assert (generated_dir / "outputs").exists()
    assert (generated_dir / "LICENSE").exists()
    assert (generated_dir / "pyproject.toml").exists()
    assert (generated_dir / "README.md").exists()
    assert (generated_dir / "requirements.txt").exists()
    assert (generated_dir / "requirements_dev.txt").exists()
    assert (generated_dir / "tasks.py").exists()


def test_barebone_minimal_structure(temp_dir: Path) -> None:
    """Test generation of barebone template with minimal structure (no docs).

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "minimal_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    # Generate project with minimal structure
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_minimal",
            "author_name": "Test Author",
            "description": "Test Minimal Structure",
            "python_version": "3.12",
            "project_structure": "minimal",
        },
    )

    generated_dir = output_dir / "test_minimal"
    assert generated_dir.exists()

    # Check that docs directory does NOT exist
    assert not (generated_dir / "docs").exists()

    # Check that other directories still exist
    assert (generated_dir / "src").exists()
    assert (generated_dir / "tests").exists()
    assert (generated_dir / "configs").exists()
    assert (generated_dir / "data").exists()
    assert (generated_dir / "notebooks").exists()
    assert (generated_dir / "reports").exists()

    # Check that tasks.py exists but doesn't contain docs tasks
    tasks_file = generated_dir / "tasks.py"
    assert tasks_file.exists()

    with tasks_file.open("r") as f:
        tasks_content = f.read()

    # Verify docs tasks are removed
    assert "def build_docs" not in tasks_content
    assert "def serve_docs" not in tasks_content

    # Verify other tasks still exist
    assert "def test" in tasks_content
    assert "def train" in tasks_content


def test_barebone_with_uv_deps_manager(temp_dir: Path) -> None:
    """Test generation of barebone template with UV dependency manager.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "uv_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    # Generate project with UV dependency manager
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_uv",
            "author_name": "Test Author",
            "description": "Test UV Dependency Manager",
            "python_version": "3.12",
            "deps_manager": "uv",
        },
    )

    generated_dir = output_dir / "test_uv"
    assert generated_dir.exists()

    # Check that requirements files do NOT exist
    assert not (generated_dir / "requirements.txt").exists()
    assert not (generated_dir / "requirements_dev.txt").exists()

    # Check that pyproject.toml exists with dependencies
    pyproject_file = generated_dir / "pyproject.toml"
    assert pyproject_file.exists()

    with pyproject_file.open("r") as f:
        pyproject_content = f.read()

    # Verify it's the UV version with inline dependencies
    assert "dependencies = [" in pyproject_content
    assert "[project.optional-dependencies]" in pyproject_content
    assert "dev = [" in pyproject_content

    # Check that tasks.py uses uv run commands
    tasks_file = generated_dir / "tasks.py"
    assert tasks_file.exists()

    with tasks_file.open("r") as f:
        tasks_content = f.read()

    # Verify uv run commands are present
    assert "uv run" in tasks_content
    assert "uv pip install" in tasks_content


def test_barebone_with_pip_deps_manager(temp_dir: Path) -> None:
    """Test generation of barebone template with pip dependency manager.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "pip_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    # Generate project with pip dependency manager
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_pip",
            "author_name": "Test Author",
            "description": "Test Pip Dependency Manager",
            "python_version": "3.12",
            "deps_manager": "pip",
        },
    )

    generated_dir = output_dir / "test_pip"
    assert generated_dir.exists()

    # Check that requirements files DO exist
    assert (generated_dir / "requirements.txt").exists()
    assert (generated_dir / "requirements_dev.txt").exists()

    # Check that pyproject.toml exists with dynamic dependencies
    pyproject_file = generated_dir / "pyproject.toml"
    assert pyproject_file.exists()

    with pyproject_file.open("r") as f:
        pyproject_content = f.read()

    # Verify it's the pip version with dynamic dependencies
    assert 'dynamic = ["dependencies", "optional-dependencies"]' in pyproject_content
    assert "[tool.setuptools.dynamic]" in pyproject_content

    # Check that tasks.py uses regular python commands
    tasks_file = generated_dir / "tasks.py"
    assert tasks_file.exists()

    with tasks_file.open("r") as f:
        tasks_content = f.read()

    # Verify no uv run commands are present
    assert "uv run" not in tasks_content
    assert "pip install" in tasks_content


# Integration tests that run the generated project's internal tests
@pytest.mark.slow
def test_barebone_template_internal_tests(temp_dir: Path) -> None:
    """Test that the generated barebone template's internal tests pass.

    This is an integration test that:
    1. Generates a project from the template
    2. Installs its dependencies
    3. Runs the generated project's test suite

    Args:
        temp_dir: temporary directory for test
    """
    import subprocess

    output_dir = temp_dir / "barebone_integration"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "barebone").resolve()

    # Generate project
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_barebone_internal",
            "author_name": "Test Author",
            "description": "Test Barebone Internal Tests",
            "python_version": "3.12",
            "deps_manager": "pip",
        },
    )

    generated_dir = output_dir / "test_barebone_internal"
    assert generated_dir.exists()

    # Install dependencies (in editable mode with dev dependencies)
    install_result = subprocess.run(
        ["pip", "install", "-e", ".[dev]"],
        cwd=generated_dir,
        capture_output=True,
        text=True,
        timeout=300,  # 5 minute timeout for installation
    )

    # Check if installation succeeded
    if install_result.returncode != 0:
        pytest.fail(
            f"Failed to install dependencies:\n"
            f"stdout: {install_result.stdout}\n"
            f"stderr: {install_result.stderr}"
        )

    # Run the generated project's tests
    test_result = subprocess.run(
        ["pytest", "tests/", "-v"],
        cwd=generated_dir,
        capture_output=True,
        text=True,
        timeout=120,  # 2 minute timeout for tests
    )

    # Check if tests passed
    if test_result.returncode != 0:
        pytest.fail(
            f"Generated project's tests failed:\n"
            f"stdout: {test_result.stdout}\n"
            f"stderr: {test_result.stderr}"
        )

    # Assert that we actually ran some tests
    assert "passed" in test_result.stdout.lower() or "passed" in test_result.stderr.lower()


@pytest.mark.slow
def test_flow_matching_template_internal_tests(temp_dir: Path) -> None:
    """Test that the generated flow_matching template's internal tests pass.

    This is an integration test that:
    1. Generates a project from the template
    2. Installs its dependencies
    3. Runs the generated project's test suite

    Args:
        temp_dir: temporary directory for test
    """
    import subprocess

    output_dir = temp_dir / "flow_matching_integration"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "flow_matching").resolve()

    # Generate project
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_flow_internal",
            "author_name": "Test Author",
            "description": "Test Flow Matching Internal Tests",
            "python_version": "3.12",
        },
    )

    generated_dir = output_dir / "test_flow_internal"
    assert generated_dir.exists()

    # Install dependencies (in editable mode with dev dependencies)
    install_result = subprocess.run(
        ["pip", "install", "-e", ".[dev]"],
        cwd=generated_dir,
        capture_output=True,
        text=True,
        timeout=300,  # 5 minute timeout for installation
    )

    # Check if installation succeeded
    if install_result.returncode != 0:
        pytest.fail(
            f"Failed to install dependencies:\n"
            f"stdout: {install_result.stdout}\n"
            f"stderr: {install_result.stderr}"
        )

    # Run the generated project's tests
    test_result = subprocess.run(
        ["pytest", "tests/", "-v", "--tb=short"],
        cwd=generated_dir,
        capture_output=True,
        text=True,
        timeout=120,  # 2 minute timeout for tests
    )

    # Check if tests passed
    if test_result.returncode != 0:
        pytest.fail(
            f"Generated project's tests failed:\n"
            f"stdout: {test_result.stdout}\n"
            f"stderr: {test_result.stderr}"
        )

    # Assert that we actually ran some tests
    assert "passed" in test_result.stdout.lower() or "passed" in test_result.stderr.lower()
