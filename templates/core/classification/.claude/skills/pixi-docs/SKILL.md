---
name: pixi-docs
description: Provides authoritative pixi documentation by fetching from pixi.sh — including its llms.txt index — instead of relying on training-data recall. Use when working with `pixi.toml`, `pixi.lock`, pixi channels, tasks, features, or environments, or when the user mentions pixi or prefix.dev. Pixi is newer than most of Claude's training data and its file format has evolved fast, so never answer pixi questions from memory.
---

# Pixi documentation

Pixi is a Rust-based cross-platform package and workflow manager built on the
conda ecosystem (via rattler), and it also handles PyPI dependencies. It is
newer than most of Claude's training data and the file format has evolved
quickly. **Never answer pixi questions from memory — fetch first.**

## Canonical sources

Pixi publishes an `llms.txt` index designed for exactly this pattern. **Fetch
the index first** to discover the current page set, then fetch the specific
page.

- LLM index (start here): https://pixi.sh/latest/llms.txt
- Docs index: https://pixi.sh/latest/
- Install: https://pixi.sh/latest/installation/
- `pixi.toml` reference: https://pixi.sh/latest/reference/project_configuration/
- Tasks: https://pixi.sh/latest/features/advanced_tasks/
- Multiple environments / features: https://pixi.sh/latest/features/multi_environment/
- Global tool install: https://pixi.sh/latest/features/global_tools/
- Lockfile: https://pixi.sh/latest/features/lockfile/
- pyproject.toml mode: https://pixi.sh/latest/reference/pyproject_toml/
- GitHub (for "what changed in version X"): https://github.com/prefix-dev/pixi

> Note: confirm `https://pixi.sh/latest/llms.txt` resolves on first use. If it
> 404s, the index may have moved — fall back to the docs index and update this
> skill's URL.

## How to use

1. Start by fetching `https://pixi.sh/latest/llms.txt` — small, current, points
   at the right deep links.
2. Then fetch the specific page it points to.
3. "Is this feature available?" → also check
   https://github.com/prefix-dev/pixi/releases; pixi ships fast and docs lag.

## Common traps

- **`pixi init` vs `pixi init --pyproject`** — different file format.
  `pixi.toml` uses top-level `[project]`, `[dependencies]`,
  `[pypi-dependencies]`, `[tasks]`. `pyproject.toml` mode nests under
  `[tool.pixi.*]`.
- **`channels`** — listed in `[project]`, no default. Always set
  `channels = ["conda-forge"]` at minimum.
- **`platforms`** — explicit list, e.g. `["linux-64", "osx-arm64", "win-64"]`.
  Pixi resolves a multi-platform lockfile by default.
- **Tasks** run via `pixi run <task>` through the deno task shell, not bash —
  some bash-isms don't work.
- **`[feature]` / `[environments]`** — composable feature sets and named
  environments that combine them.
- **PyPI deps** use `[pypi-dependencies]` and PEP 440 specifiers, not conda
  matchspec.
- **`pixi add`** picks conda vs PyPI: `pixi add numpy` (conda) vs
  `pixi add --pypi some-package`.

## Project recommended setup

Pixi is the default env manager for generated templates. Typical `pixi.toml`:

```toml
[project]
name = "..."
channels = ["conda-forge", "pytorch", "nvidia"]
platforms = ["linux-64", "osx-arm64"]

[dependencies]
python = "3.11.*"
pytorch = "*"
lightning = "*"

[pypi-dependencies]
wandb = "*"
hydra-core = "*"

[tasks]
train = "python -m src.train"
test = "pytest"
```

Verify exact names against prefix.dev — PyTorch is `pytorch` on conda-forge but
`torch` on PyPI; pick one channel strategy per project to avoid resolver
fights.

## When to skip the fetch

Skip for: explaining at a high level what pixi is or why the repo uses it.

Fetch for: any `pixi.toml` field, channels, tasks, features, environments,
lockfile behavior, or a "does pixi support X" question.

## Checklist

```
[ ] llms.txt index fetched first, then the specific page
[ ] pixi.toml field answers verified against the reference page
[ ] Feature-availability questions cross-checked against GitHub releases
```
