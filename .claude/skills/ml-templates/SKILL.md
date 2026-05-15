---
name: ml-templates
description: Encodes the conventions of the cookiecutter-ml-templates repo — config layout, file structure, callback patterns, environment setup, Cookiecutter mechanics, testing rules. Use when generating a new template, editing an existing one, modifying Cookiecutter hooks, or reviewing template code in this repo. This skill carries the project-specific rules that override generic library defaults; for library API questions defer to the per-library `*-docs` skills.
---

# ml-templates: working in this Cookiecutter ML template library

This is a meta-repo of Cookiecutter templates for ML projects. Each template
under `templates/` is independently usable. The repo's value is **consistency
across templates** and **best-practice defaults**, so the bar for adding or
modifying template code is higher than for one-off project work.

## Division of labor with the docs skills

For library API questions, defer to the per-library skills — don't answer from
memory:

- `pytorch-docs` — `torch.*`
- `lightning-docs` — Trainer, modules, callbacks, strategies
- `hydra-docs` — config composition, `_target_`, overrides
- `wandb-docs` — `wandb.log`, artifacts, registry, integration
- `pixi-docs` — `pixi.toml`, channels, tasks, features
- `uv-docs` — `pyproject.toml` (uv mode), `uv.lock`, `uvx`
- `conda-docs` — `environment.yml`, channels, mamba
- `copier-docs` — `copier.yml`, `copier copy`/`update`, `.copier-answers.yml`, `_tasks`, `_extends`, `_external_data`

**Those skills handle version-correct API questions. This skill handles
project conventions that override or supplement library defaults.**

## Repo conventions

### Hydra config layout
- Configs live in `{{ cookiecutter.project_slug }}/configs/` per template.
- Config groups, not flat configs. Mirror `templates/barebone/configs/`.
- Always `_target_` instantiation for models, datamodules, optimizers — no
  manual `__init__` calls in template code.

### Lightning patterns
- `LightningModule` and `LightningDataModule` are always separate files.
- Use the built-in `WandbLogger`, not raw `wandb` calls inside the module.
- Callbacks live in `src/callbacks/`, one file each — never inline in a
  Trainer instantiation.

### W&B integration
- `templates/MNIST_wandb_image_logger/` is the reference for image logging.
  Mirror its structure for similar callbacks elsewhere.
- Project name and entity always come from Hydra config, never hardcoded.
- RL gameplay video: collect frames in memory, pass to
  `wandb.Video(np_array, fps=...)` — never `wandb.gym.monitor()` (broken for
  Gymnasium ≥1.0).

### Environment management
- New templates default to **pixi** (see `pixi-docs`). `environment.yml`
  templates are legacy.
- `pixi.toml` must include at least `linux-64` and `osx-arm64` platforms.
- For PyTorch, pick one channel strategy per template (conda-forge OR pytorch
  index via uv) — don't mix.

### Cookiecutter mechanics
- Hooks live in `hooks/` at the repo root (shared) and each template's
  `hooks/` (template-specific).
- `cookiecutter.json` keys use snake_case. Boolean prompts are strings
  (`"yes"`/`"no"`), not booleans.
- Jinja2 conditionals in template files must produce valid Python with the
  conditional both present and absent. Test both branches before committing.

### Template testing
- Every template has tests under the top-level `tests/` that generate it with
  various option combinations and run a smoke training step. New templates
  need matching tests.

## Workflows

**Adding a new template:** copy `templates/barebone/` → edit
`cookiecutter.json` → adapt configs/model/datamodule → for any library API the
barebone doesn't already show, consult the relevant `*-docs` skill → add a
generate-and-smoke-test under `tests/`.

**Bumping a template's library version:** read the changelog (the relevant
`*-docs` skill points to it) for breaking changes → update the pin in
`pixi.toml`/`pyproject.toml` → run the smoke test.

**Reviewing a contribution:** check it follows the conventions above → verify
library API usage against the per-library docs skill, not memory → confirm
tests cover the new path.

## What lives where

- `templates/barebone/` — canonical structure; mirror it when in doubt.
- `templates/MNIST_wandb_image_logger/` — reference for W&B image logging.
- `templates/rl/` — RL (SAC, TD3, PPO, RPO, DQN); diverges from supervised
  templates because the training loop differs fundamentally.
- `templates/flow_matching/` — generative-model-specific.
- `hooks/` — shared Cookiecutter hooks.
- `docs/` — MkDocs Material site for the meta-repo (not template internals).

## Checklist

```
[ ] Library API questions routed to the relevant *-docs skill, not memorized
[ ] New/edited config uses groups + _target_, mirrors barebone
[ ] Callbacks are one-file-each under src/callbacks/
[ ] New template has a generate-and-smoke test under tests/
[ ] Jinja2 conditionals tested with the branch both present and absent
```
