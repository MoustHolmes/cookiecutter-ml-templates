from __future__ import annotations

from invoke import Context, task


@task
def test(c: Context) -> None:
    """Run tests."""
    c.run("pytest -v")


@task
def test_fast(c: Context) -> None:
    """Run fast tests only (exclude slow integration tests)."""
    c.run('pytest tests/ -m "not slow" -v')


@task
def setup(c: Context) -> None:
    """Set up the development environment."""
    c.run("pip install -r requirements.txt")
    c.run("pre-commit install")


@task
def create(c: Context, template: str, dest: str = ".", project_name: str = "") -> None:
    """Generate a project from a template using Copier.

    Example:
        invoke create --template barebone
        invoke create --template rl --dest /tmp/my_rl --project-name my_rl
    """
    template_path = f"templates/{template}"
    cmd = f'copier copy "{template_path}" "{dest}" --trust'
    if project_name:
        cmd += f" --data project_name={project_name}"
    c.run(cmd)


@task
def docs(c: Context) -> None:
    """Serve the MkDocs documentation site locally."""
    c.run("mkdocs serve")


@task
def lint(c: Context) -> None:
    """Run ruff linter."""
    c.run("ruff check .")
