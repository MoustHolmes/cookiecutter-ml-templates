from __future__ import annotations

import subprocess
from pathlib import Path

import yaml
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


@task
def setup_defaults(_c: Context) -> None:
    """Write author defaults to ~/.cookiecutterrc from git config and GitHub CLI.

    After running this once, cookiecutter will pre-fill author_name, author_email,
    and github_username in every template prompt — you can still edit them at runtime.
    """

    def _run(*cmd: str) -> str:
        try:
            return subprocess.check_output(list(cmd), text=True, stderr=subprocess.DEVNULL).strip()  # noqa: S603
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    author_name = _run("git", "config", "--global", "user.name")
    author_email = _run("git", "config", "--global", "user.email")
    github_username = _run("gh", "api", "user", "--jq", ".login") or _run(
        "git", "config", "--global", "github.user",
    )

    if not any([author_name, author_email, github_username]):
        print("Nothing to save — set git config first:")
        print("  git config --global user.name 'Your Name'")
        print("  git config --global user.email 'your@email.com'")
        return

    rc_path = Path.home() / ".cookiecutterrc"
    existing: dict = yaml.safe_load(rc_path.read_text()) if rc_path.exists() else {}
    existing = existing or {}
    ctx = existing.setdefault("default_context", {})

    if author_name:
        ctx["author_name"] = author_name
    if author_email:
        ctx["author_email"] = author_email
    if github_username:
        ctx["github_username"] = github_username

    rc_path.write_text(yaml.dump(existing, default_flow_style=False, allow_unicode=True))

    print(f"Saved to {rc_path}")
    for k, v in ctx.items():
        print(f"  {k}: {v}")
