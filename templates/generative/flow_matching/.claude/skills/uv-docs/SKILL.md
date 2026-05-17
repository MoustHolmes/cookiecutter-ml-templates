---
name: uv-docs
description: Provides authoritative uv documentation by fetching from docs.astral.sh/uv instead of relying on training-data recall. Use when working with uv's project interface (`uv init/add/sync/run/lock`), its pip interface (`uv pip ...`), `uv.lock`, `uvx`, workspaces, `[tool.uv.*]` config, or Python-version management. uv evolves monthly and Claude's training data often reflects an older CLI or confuses uv with pip-tools — fetch before writing uv commands or config.
---

# uv documentation

uv is Astral's Rust-based Python package and project manager. It evolves
rapidly — new commands and behaviors land monthly — and Claude's training data
often reflects an older subset of the CLI or confuses uv with pip-tools.
**Fetch authoritative docs before writing uv commands or `pyproject.toml`
config.**

## Canonical sources
- https://docs.astral.sh/uv/llms.txt
- Index: https://docs.astral.sh/uv/
- Getting started: https://docs.astral.sh/uv/getting-started/
- Installation: https://docs.astral.sh/uv/getting-started/installation/
- Projects guide: https://docs.astral.sh/uv/guides/projects/
- Projects concept (deeper): https://docs.astral.sh/uv/concepts/projects/
- Managing dependencies: https://docs.astral.sh/uv/concepts/projects/dependencies/
- Lockfile / sync: https://docs.astral.sh/uv/concepts/projects/sync/
- Workspaces: https://docs.astral.sh/uv/concepts/projects/workspaces/
- The `uv pip` interface: https://docs.astral.sh/uv/pip/
- Scripts (PEP 723 inline metadata): https://docs.astral.sh/uv/guides/scripts/
- Tools / `uvx`: https://docs.astral.sh/uv/guides/tools/
- Python versions: https://docs.astral.sh/uv/concepts/python-versions/
- Settings reference: https://docs.astral.sh/uv/reference/settings/
- CLI reference: https://docs.astral.sh/uv/reference/cli/
- GitHub (release notes — fastest way to see what's new): https://github.com/astral-sh/uv/releases

## How to use

1. uv has **two distinct surfaces**: the project interface (`uv init`,
   `uv add`, `uv sync`, `uv run`, `uv lock`) managing `pyproject.toml` +
   `uv.lock`, and the pip interface (`uv pip install/compile/sync`) as a
   drop-in pip replacement. Confirm which one the question is about first.
2. `pyproject.toml` config questions → fetch the dependencies and sync concept
   pages. `[tool.uv.sources]` for git/path/index sources is non-obvious and
   frequently misremembered.
3. Python version management (uv installs CPython for you) → fetch the Python
   versions page.

## Common traps

- **`uv pip install` does not modify `pyproject.toml`.** It installs into the
  active env. `uv add` updates the manifest.
- **`uv sync` ≠ `uv pip sync`.** Former operates on `pyproject.toml` +
  `uv.lock`; latter on a requirements file.
- **`uv run`** auto-creates and uses the project venv — no manual `source
  .venv/bin/activate` needed.
- **`[tool.uv.sources]`** overrides where a dependency comes from (PyTorch
  index, git URL, local path). Not in `[project.dependencies]`.
- **PyTorch**: use `[tool.uv.index]` + `[tool.uv.sources]` to pin the right
  PyTorch index (cpu / cu121 / cu124). See the settings reference.
- **Workspaces**: `[tool.uv.workspace]` with `members = [...]` for a
  Cargo-style monorepo sharing one lockfile.
- **`uvx`** is shorthand for `uv tool run` — ephemeral env, no permanent
  install.

## When to skip the fetch

Skip for: a trivial `uv pip install <name>` or `uvx <tool>` invocation.

Fetch for: any `pyproject.toml` config, indexes or sources, a named uv
version, workspaces, or PyTorch ecosystem pinning.

## Checklist

```
[ ] Which surface (project vs pip interface) identified before answering
[ ] pyproject.toml / sources answers verified against the page
[ ] uv add vs uv pip install distinction respected in any command given
```
