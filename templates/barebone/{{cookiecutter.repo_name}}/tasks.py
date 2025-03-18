"""Tasks for maintaining the project."""

from invoke import task


@task
def create_environment(c):
    """Create a new conda environment for project."""
    c.run(
        "conda create -n {{ cookiecutter.repo_name }} python={{ cookiecutter.python_version }}"
    )
    c.run("conda activate {{ cookiecutter.repo_name }}")
    c.run("pip install -e .")


@task
def requirements(c):
    """Install project requirements."""
    c.run("pip install -r requirements.txt")


@task
def dev_requirements(c):
    """Install development requirements."""
    c.run("pip install -r requirements_dev.txt")


@task
def preprocess_data(c):
    """Preprocess data."""
    c.run("python src/{{ cookiecutter.project_name }}/data.py")


@task
def train(c):
    """Train model."""
    c.run("python src/{{ cookiecutter.project_name }}/train.py")


@task
def test(c):
    """Run tests."""
    c.run("pytest tests/")


@task
def build_docs(c):
    """Build documentation."""
    c.run("mkdocs build")


@task
def serve_docs(c):
    """Serve documentation."""
    c.run("mkdocs serve")
