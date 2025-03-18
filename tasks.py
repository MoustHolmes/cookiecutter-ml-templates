from __future__ import annotations

from invoke import Context, task


@task
def test(c: Context) -> None:
    """Run tests."""
    c.run("pytest -v")


@task
def setup(c: Context) -> None:
    """Set up the development environment."""
    c.run("pip install -e '.[dev]'")
    c.run("pre-commit install")


@task
def create_template(c: Context, template: str, output_dir: str | None = None) -> None:
    """Create a new project from a template."""
    cmd = f"cookiecutter templates/{template}"
    if output_dir:
        cmd += f" --output-dir {output_dir}"
    c.run(cmd)
