"""Tasks for maintaining the project."""

from invoke import task


@task
def create_environment(c):
    """Create a new uv environment for project."""
    c.run("uv venv")
    c.run("uv pip install -e .[dev]")


@task
def requirements(c):
    """Install project requirements using uv."""
    c.run("uv pip install -e .")


@task
def dev_requirements(c):
    """Install development requirements using uv."""
    c.run("uv pip install -e .[dev]")


@task
def preprocess_data(c):
    """Preprocess data."""
    c.run("uv run python src/{{ cookiecutter.repo_name }}/data.py")


@task
def train(c):
    """Train model."""
    c.run("uv run python src/{{ cookiecutter.repo_name }}/train.py")


@task
def test(c):
    """Run tests."""
    c.run("uv run pytest tests/")


@task
def build_docs(c):
    """Build documentation."""
    c.run("uv run mkdocs build")


@task
def serve_docs(c):
    """Serve documentation."""
    c.run("uv run mkdocs serve")
