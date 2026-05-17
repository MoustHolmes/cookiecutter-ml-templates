#!/usr/bin/env python3
"""Add a dependency to a generated project, dispatching on deps_manager.

Reads .copier-answers.yml (or --answers-file) to determine the deps_manager,
then adds the dependency idempotently to the appropriate file(s).

Usage:
    python add_deps.py wandb>=0.16.0
    python add_deps.py "wandb>=0.16.0" --dev
    python add_deps.py "wandb>=0.16.0" --answers-file .copier-answers.base.yml
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import tomlkit
import yaml


def _parse_dep_name(dep: str) -> str:
    """Extract bare package name from a dep spec like 'wandb[media]>=0.16.0'."""
    return re.split(r"[><=!~\[]", dep)[0].strip()


def _load_answers(answers_file: str) -> dict:
    path = Path(answers_file)
    if not path.exists():
        sys.exit(f"[add_deps] answers file not found: {answers_file}")
    with path.open() as f:
        return yaml.safe_load(f) or {}


def _dep_in_list(name: str, items: list) -> bool:
    """Return True if a dep with the given bare name already exists in a list."""
    return any(_parse_dep_name(str(item)) == name for item in items)


# ── pip ──────────────────────────────────────────────────────────────────────


def _add_pip(dep: str, *, dev: bool) -> None:
    name = _parse_dep_name(dep)
    fname = "requirements_dev.txt" if dev else "requirements.txt"
    path = Path(fname)
    if not path.exists():
        print(f"[add_deps] {fname} not found, skipping")
        return
    content = path.read_text()
    if re.search(rf"(?m)^{re.escape(name)}([><=!~\[]|$)", content):
        print(f"[add_deps] {name} already present in {fname}")
        return
    with path.open("a") as f:
        f.write(f"{dep}\n")
    print(f"[add_deps] Added {dep} to {fname}")


# ── uv / pip (pyproject.toml) ────────────────────────────────────────────────


def _add_pyproject(dep: str, *, dev: bool) -> None:
    name = _parse_dep_name(dep)
    path = Path("pyproject.toml")
    if not path.exists():
        print("[add_deps] pyproject.toml not found, skipping")
        return
    doc = tomlkit.parse(path.read_text())
    if dev:
        target = doc.get("project", {}).get("optional-dependencies", {}).get("dev", None)
        if target is None:
            print("[add_deps] [project.optional-dependencies.dev] not found, skipping")
            return
        if _dep_in_list(name, target):
            print(f"[add_deps] {name} already present in [project.optional-dependencies.dev]")
            return
        target.append(dep)
    else:
        target = doc.get("project", {}).get("dependencies", None)
        if target is None:
            print("[add_deps] [project.dependencies] not found, skipping")
            return
        if _dep_in_list(name, target):
            print(f"[add_deps] {name} already present in [project.dependencies]")
            return
        target.append(dep)
    path.write_text(tomlkit.dumps(doc))
    section = "dev" if dev else "runtime"
    print(f"[add_deps] Added {dep} to pyproject.toml ({section})")


# ── pixi ─────────────────────────────────────────────────────────────────────


def _add_pixi(dep: str, *, dev: bool) -> None:
    name = _parse_dep_name(dep)
    # Try pixi CLI first (handles lock file update automatically)
    try:
        cmd = ["pixi", "add"]
        if dev:
            cmd += ["--feature", "dev"]
        cmd.append(dep)
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print(f"[add_deps] Added {dep} via pixi add")
            return
        # pixi add failed — fall through to manual edit
    except FileNotFoundError:
        pass

    # Manual edit via tomlkit
    path = Path("pixi.toml")
    if not path.exists():
        print("[add_deps] pixi.toml not found, skipping")
        return
    doc = tomlkit.parse(path.read_text())
    if dev:
        section = doc.get("feature", {}).get("dev", {}).get("dependencies", None)
        if section is None:
            print("[add_deps] [feature.dev.dependencies] not found in pixi.toml, skipping")
            return
    else:
        section = doc.get("dependencies", None)
        if section is None:
            print("[add_deps] [dependencies] not found in pixi.toml, skipping")
            return
    if name in section:
        print(f"[add_deps] {name} already present in pixi.toml")
        return
    section[name] = "*"
    path.write_text(tomlkit.dumps(doc))
    print(f"[add_deps] Added {name} = '*' to pixi.toml (run 'pixi update {name}' to lock)")


# ── main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dep", help="Dependency spec, e.g. 'wandb>=0.16.0'")
    parser.add_argument("--dev", action="store_true", help="Add as a dev dependency")
    parser.add_argument("--answers-file", default=".copier-answers.yml")
    args = parser.parse_args()

    answers = _load_answers(args.answers_file)
    deps_manager = answers.get("deps_manager", "pip")

    if deps_manager == "pip":
        _add_pip(args.dep, dev=args.dev)
    elif deps_manager == "uv":
        _add_pyproject(args.dep, dev=args.dev)
    elif deps_manager == "pixi":
        _add_pixi(args.dep, dev=args.dev)
    else:
        sys.exit(f"[add_deps] Unknown deps_manager: {deps_manager!r}")


if __name__ == "__main__":
    main()
