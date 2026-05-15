"""Tasks for maintaining the project (pip dependency manager)."""

from invoke import task


@task
def create_environment(c):
    """Create a new conda environment for project."""
    c.run("conda create -n {{cookiecutter.repo_name}} python={{cookiecutter.python_version}}")
    c.run("conda activate {{cookiecutter.repo_name}}")
    c.run("pip install -e .[dev]")


@task
def requirements(c):
    """Install project requirements."""
    c.run("pip install -e .")


@task
def dev_requirements(c):
    """Install development requirements."""
    c.run("pip install -e .[dev]")


@task
def train(c):
    """Train SAC agent on Pendulum-v1 (default)."""
    c.run("python src/{{cookiecutter.repo_name}}/train.py")


@task
def train_td3(c):
    """Train TD3 agent on Pendulum-v1."""
    c.run("python src/{{cookiecutter.repo_name}}/train.py agent=td3")


@task
def test(c):
    """Run tests."""
    c.run("pytest tests/")


@task
def test_debug(c):
    """Run a fast debug training pass (single step, no WandB)."""
    c.run("python src/{{cookiecutter.repo_name}}/train.py +experiment=debug")


@task
def build_docs(c):
    """Build documentation."""
    c.run("mkdocs build")


@task
def serve_docs(c):
    """Serve documentation locally."""
    c.run("mkdocs serve")
