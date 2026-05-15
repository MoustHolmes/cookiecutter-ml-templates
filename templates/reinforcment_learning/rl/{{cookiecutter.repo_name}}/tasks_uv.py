"""Tasks for maintaining the project (uv dependency manager)."""

from invoke import task


@task
def create_environment(c):
    """Create a new uv virtual environment and install dependencies."""
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
    """Train SAC agent on Pendulum-v1 (default)."""
    c.run("uv run python src/{{cookiecutter.repo_name}}/train.py")


@task
def train_td3(c):
    """Train TD3 agent on Pendulum-v1."""
    c.run("uv run python src/{{cookiecutter.repo_name}}/train.py agent=td3")


@task
def test(c):
    """Run tests."""
    c.run("uv run pytest tests/")


@task
def test_debug(c):
    """Run a fast debug training pass (single step, no WandB)."""
    c.run("uv run python src/{{cookiecutter.repo_name}}/train.py +experiment=debug")


@task
def build_docs(c):
    """Build documentation."""
    c.run("uv run mkdocs build")


@task
def serve_docs(c):
    """Serve documentation locally."""
    c.run("uv run mkdocs serve")
