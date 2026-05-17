---
name: conda-docs
description: Provides authoritative conda documentation by fetching from docs.conda.io and conda-forge.org. Use when working with `environment.yml` files, conda channels and channel priority, conda MatchSpec, the libmamba solver, mamba, or when comparing conda against pixi and uv. Conda basics are well-represented in training data, but channel-priority and solver behavior have changed — verify those against current docs.
---

# Conda documentation

Conda's basics are well-represented in training data, but channel priority, the
libmamba solver's behavior, lockfile ecosystems, and conda-forge conventions
are worth verifying against current docs.

## Canonical sources

- Conda docs index: https://docs.conda.io/projects/conda/en/latest/
- User guide: https://docs.conda.io/projects/conda/en/latest/user-guide/
- Managing environments: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
- Managing channels: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html
- MatchSpec reference: https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/pkg-specs.html#package-match-specifications
- conda-forge: https://conda-forge.org/docs/
- mamba: https://mamba.readthedocs.io/en/latest/

## When to use which tool

For new projects in this repo, prefer **pixi** (see `pixi-docs`) over raw conda
— it handles lockfiles, cross-platform resolution, and tasks natively. Use
conda directly only when: working with an existing un-migrated
`environment.yml` project, the user explicitly asks about conda commands, or
debugging a channel/solver issue at the conda level.

## Common traps

- **Channel priority** — `conda-forge` should usually be first. Mixing
  `defaults` + `conda-forge` without `channel_priority: strict` produces
  unsolvable environments.
- **`environment.yml`** does not produce a true lockfile. Use `conda-lock` or
  migrate to pixi for reproducibility.
- **`pip:` section in `environment.yml`** — conda installs everything first,
  then pip installs the `pip:` section into the same env. Conda doesn't track
  pip-installed packages.
- **`libmamba`** is the default solver in modern conda — much faster, but
  occasionally resolves differently from the classic solver.

## How to use

1. "How do I make environment X" → fetch the managing environments page.
2. Channel/solver issues → fetch the channels page; check the user's
   `.condarc` if relevant.
3. conda-forge package availability → search
   https://prefix.dev/channels/conda-forge directly rather than guessing.

## When to skip the fetch

Skip for: basic `conda create` / `conda activate` / `conda install` commands —
stable and well-known.

Fetch for: channel priority and `.condarc` config, MatchSpec syntax, solver
behavior, conda-forge conventions, or lockfile/reproducibility questions.

## Checklist

```
[ ] For new-project questions, pixi was recommended over raw conda
[ ] Channel-priority / solver answers verified against current docs
[ ] Package-availability checked on prefix.dev, not guessed
```
