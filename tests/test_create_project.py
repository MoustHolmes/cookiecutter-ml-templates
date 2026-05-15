"""Tests for cookiecutter template generation (classification, flow_matching, rl).

Barebone template tests have moved to test_base_generation.py (Copier API).
"""

from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


def test_classification_template_success(temp_dir: Path) -> None:
    """Test successful generation of classification template.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "classification_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "core" / "classification").resolve()

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

    generated_dir = output_dir / "test_classification"
    assert generated_dir.exists()
    assert (generated_dir / "src" / "test_classification" / "classification_module.py").exists()
    assert (generated_dir / "src" / "test_classification" / "data" / "mnist_datamodule.py").exists()
    assert (generated_dir / "src" / "test_classification" / "callbacks" / "__init__.py").exists()
    assert (generated_dir / "configs" / "train_config.yaml").exists()
    assert (generated_dir / "configs" / "callbacks" / "default_callbacks.yaml").exists()
    assert (generated_dir / "tests" / "test_model.py").exists()
    assert (generated_dir / "tests" / "test_data.py").exists()
    assert (generated_dir / "pyproject.toml").exists()


def test_classification_with_uv_deps_manager(temp_dir: Path) -> None:
    """Test generation of classification template with UV dependency manager.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "classification_uv_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "core" / "classification").resolve()

    # Generate project with UV dependency manager
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_classification_uv",
            "author_name": "Test Author",
            "description": "Test UV Dependency Manager",
            "python_version": "3.12",
            "deps_manager": "uv",
        },
    )

    generated_dir = output_dir / "test_classification_uv"
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


def test_flow_matching_with_uv_deps_manager(temp_dir: Path) -> None:
    """Test generation of flow_matching template with UV dependency manager.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "flow_matching_uv_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "generative" / "flow_matching").resolve()

    # Generate project with UV dependency manager
    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_flow_uv",
            "author_name": "Test Author",
            "description": "Test UV Dependency Manager",
            "python_version": "3.12",
            "deps_manager": "uv",
        },
    )

    generated_dir = output_dir / "test_flow_uv"
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


def test_rl_template_success(temp_dir: Path) -> None:
    """Test successful generation of RL template with default options.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "rl_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "rl").resolve()

    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_rl_project",
            "author_name": "Test Author",
            "description": "Test RL Template",
            "python_version": "3.11",
            "deps_manager": "pip",
        },
    )

    generated_dir = output_dir / "test_rl_project"
    assert generated_dir.exists()

    assert (generated_dir / "src").exists()
    assert (generated_dir / "tests").exists()
    assert (generated_dir / "configs").exists()
    assert (generated_dir / "pyproject.toml").exists()
    assert (generated_dir / "tasks.py").exists()
    assert (generated_dir / "requirements.txt").exists()
    assert (generated_dir / "requirements_dev.txt").exists()


def test_rl_template_structure(temp_dir: Path) -> None:
    """Test that the generated RL template contains all algorithm files and configs."""
    output_dir = temp_dir / "rl_structure_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "rl").resolve()

    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_rl_struct",
            "author_name": "Test Author",
            "description": "Test RL Structure",
            "python_version": "3.11",
            "deps_manager": "pip",
        },
    )

    g = output_dir / "test_rl_struct"
    src = g / "src" / "test_rl_struct"

    # Lightning modules — one per algorithm
    for module in ("sac_module.py", "td3_module.py", "ppo_module.py", "dqn_module.py"):
        assert (src / module).exists(), f"Missing {module}"

    # Model classes
    for model_file in ("actor.py", "critic.py", "mlp.py"):
        assert (src / "models" / model_file).exists(), f"Missing models/{model_file}"

    # Data classes
    for data_file in ("replay_buffer.py", "env_datamodule.py", "rollout_datamodule.py"):
        assert (src / "data" / data_file).exists(), f"Missing data/{data_file}"

    # Callbacks
    for cb in ("episode_logger.py", "video_logger.py"):
        assert (src / "callbacks" / cb).exists(), f"Missing callbacks/{cb}"

    # Agent configs
    configs = g / "configs"
    for agent_cfg in ("sac.yaml", "td3.yaml", "ppo_discrete.yaml", "ppo_continuous.yaml", "dqn.yaml", "rpo.yaml"):
        assert (configs / "agent" / agent_cfg).exists(), f"Missing configs/agent/{agent_cfg}"

    # Environment configs
    for env_cfg in ("pendulum.yaml", "cartpole.yaml", "cartpole_replay.yaml", "lunar_lander.yaml"):
        assert (configs / "environment" / env_cfg).exists(), f"Missing configs/environment/{env_cfg}"

    # Test files
    tests = g / "tests"
    for test_file in ("conftest.py", "test_config.py", "test_data.py", "test_model.py", "test_train_script.py"):
        assert (tests / test_file).exists(), f"Missing tests/{test_file}"


def test_rl_template_with_pixi_deps_manager(temp_dir: Path) -> None:
    """Test generation of RL template with pixi dependency manager.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "rl_pixi_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "rl").resolve()

    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_rl_pixi",
            "author_name": "Test Author",
            "description": "Test RL Pixi Dependency Manager",
            "python_version": "3.11",
            "deps_manager": "pixi",
        },
    )

    generated_dir = output_dir / "test_rl_pixi"
    assert generated_dir.exists()

    assert (generated_dir / "pixi.toml").exists()
    assert not (generated_dir / "tasks.py").exists()
    assert not (generated_dir / "requirements.txt").exists()
    assert not (generated_dir / "requirements_dev.txt").exists()

    pixi_file = generated_dir / "pixi.toml"
    with pixi_file.open("r") as f:
        pixi_content = f.read()
    assert "gymnasium" in pixi_content
    assert "[tasks]" in pixi_content
    assert "train" in pixi_content


def test_rl_template_with_uv_deps_manager(temp_dir: Path) -> None:
    """Test generation of RL template with UV dependency manager.

    Args:
        temp_dir: temporary directory for test
    """
    output_dir = temp_dir / "rl_uv_test"
    current_dir = Path(__file__).parent
    template_dir = (current_dir / ".." / "templates" / "rl").resolve()

    cookiecutter(
        template=str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_rl_uv",
            "author_name": "Test Author",
            "description": "Test RL UV Dependency Manager",
            "python_version": "3.11",
            "deps_manager": "uv",
        },
    )

    generated_dir = output_dir / "test_rl_uv"
    assert generated_dir.exists()

    # Check that requirements files do NOT exist
    assert not (generated_dir / "requirements.txt").exists()
    assert not (generated_dir / "requirements_dev.txt").exists()

    # Check that pyproject.toml exists with inline dependencies
    pyproject_file = generated_dir / "pyproject.toml"
    assert pyproject_file.exists()

    with pyproject_file.open("r") as f:
        pyproject_content = f.read()

    assert "dependencies = [" in pyproject_content
    assert "[project.optional-dependencies]" in pyproject_content
    assert "dev = [" in pyproject_content

    # Check that tasks.py uses uv run commands
    tasks_file = generated_dir / "tasks.py"
    assert tasks_file.exists()

    with tasks_file.open("r") as f:
        tasks_content = f.read()

    assert "uv run" in tasks_content
    assert "uv pip install" in tasks_content


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
    template_dir = (current_dir / ".." / "templates" / "generative" / "flow_matching").resolve()

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
            f"stderr: {install_result.stderr}",
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
            f"stderr: {test_result.stderr}",
        )

    # Assert that we actually ran some tests
    assert "passed" in test_result.stdout.lower() or "passed" in test_result.stderr.lower()
