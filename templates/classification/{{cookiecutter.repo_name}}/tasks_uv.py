"""Tasks for maintaining the project."""

from invoke import task


@task
def create_environment(c):
    """Create a new environment for project."""
    c.run("uv venv")
    c.run("uv pip install -e .[dev]")


@task
def requirements(c):
    """Install project requirements."""
    c.run("uv pip install -e .")


@task
def dev_requirements(c):
    """Install development requirements."""
    c.run("uv pip install -e .[dev]")


@task
def train(c):
    """Train model."""
    c.run("uv run python src/{{cookiecutter.repo_name}}/train.py")


@task
def test(c):
    """Run tests."""
    c.run("uv run pytest tests/")
