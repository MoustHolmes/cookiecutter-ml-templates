# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dev dependencies:
```bash
pip install -r requirements.txt
```

Run all tests (excluding slow integration tests):
```bash
pytest tests/ -m "not slow"
```

Run a single test:
```bash
pytest tests/test_base_generation.py::test_barebone_full_structure
```

Run slow integration tests (generate projects, install deps, run their internal tests):
```bash
pytest tests/ -m slow
```

Lint:
```bash
ruff check .
```

## Architecture

This is a mono-repo of [Copier](https://copier.readthedocs.io/) templates for ML projects. The repo itself has no package — it's a template library with a test suite that validates generated output.

### Templates

Templates are **flat** Copier templates: all files render directly into the destination directory (no outer `{{project_name}}/` subdirectory). Users create the project directory first, then run `copier copy` inside it.

Available templates:
- `templates/barebone/` — minimal starting point with core PyTorch Lightning + Hydra structure
- `templates/core/classification/` — MNIST image classification (ClassificationModule + MNISTDataModule + Hydra configs)
- `templates/generative/flow_matching/` — full flow matching implementation (PyTorch Lightning + Hydra)
- `templates/rl/` — reinforcement learning with SAC, TD3, PPO (discrete + continuous), RPO, and DQN; uses Gymnasium

Extensions live in `templates/extensions/` and are applied as a second `copier copy` pass on top of a base template:
- `templates/extensions/image_logger/` — WandB image logging callback for classification projects

### Template structure

Each template directory contains:
- `copier.yml` — questions, defaults, validators, `_exclude` rules, and `_tasks`
- `.copier-answers.yml.jinja` — records answers for `copier update` lifecycle
- Flat source files (`.jinja` suffix for files that need rendering, no suffix for verbatim)
- `src/{{repo_name}}/` — the generated package (directory name is Jinja-rendered)

The `_shared/` directory at the repo root contains:
- `_shared/questions/author.yml`, `deps_manager.yml`, `licensing.yml` — shared question definitions included by all templates via `!include`
- `_shared/scripts/add_deps.py` — deps-manager-aware dependency adder used by extension `_tasks`

### Key template options

- `deps_manager`: `pip`, `uv`, or `pixi`. Controls which dependency files are generated. Handled via `_exclude` in `copier.yml` (no post-gen hook needed).
- `project_structure`: `full` (includes `docs/` with MkDocs) or `minimal` (docs excluded). Barebone only.
- `create_github_repo`: Optionally calls `gh repo create` via `_tasks` after generation.
- `project_name` must be a valid lowercase Python identifier (validated via `validator:` in `_shared/questions/author.yml`).
- `repo_name` is derived from `project_name` as a hidden question (`when: false`) and is NOT stored in `.copier-answers.yml`.

### Generating a project (Copier workflow)

```bash
# Create the project directory first, then copy into it
mkdir my_project && cd my_project
copier copy path/to/templates/barebone . --trust

# Or non-interactively with data overrides
copier copy templates/barebone /tmp/test_proj --defaults \
  --data project_name=my_proj --data deps_manager=uv --trust
```

Applying an extension (from inside the generated project):
```bash
copier copy path/to/templates/extensions/image_logger . --trust
```

Updating a project when the template changes:
```bash
copier update --trust
# Or for a specific extension:
copier update --answers-file .copier-answers.image_logger.yml --trust
```

### Generated project structure (gold standard — `barebone`/`flow_matching`)

```
src/<repo_name>/
    __init__.py
    train.py           # Hydra entry point
    models/
    data/
configs/
    train_config.yaml
    paths_config.yaml
    model/
    data/
    trainer/
    logger/
    callbacks/
tests/
    conftest.py
    test_config.py
    test_data.py
    test_model.py
tasks.py               # Invoke task runner (pip/uv) or absent (pixi uses pixi.toml tasks)
pyproject.toml
.copier-answers.yml    # Records generation answers; required for copier update
```

### Testing strategy

Tests validate template generation using the Copier Python API (`copier.run_copy()`):

- `tests/test_base_generation.py` — structure, deps variants (pip/uv/pixi), license, config naming, answers file; one section per template
- `tests/test_validation.py` — validator rejection tests (invalid project names)
- `tests/test_extension_application.py` — apply extensions on top of base, assert new files appear, base files untouched, deps injected
- `tests/test_add_deps.py` — unit tests for `_shared/scripts/add_deps.py`

The standard test helper pattern:
```python
copier.run_copy(
    src_path=str(TEMPLATE_DIR),
    dst_path=str(dst),
    data={"project_name": "test_proj", ...},
    defaults=True,
    overwrite=True,
    unsafe=True,  # required when template has _tasks
)
```

## Design Philosophy

### Model vs LightningModule separation

**Models** (`src/<repo>/models/`) hold only weights: take data in, return a tensor out. No loss, no optimizer, no training logic.

**LightningModules** (`src/<repo>/<algo>_module.py`) contain all algorithm logic: loss functions, training/validation steps, schedulers, sampling, solver calls.

```
models/unet.py               ← weights + forward pass only
flow_matching_module.py      ← loss, noise schedule, ODE solver, training step
```

### Modularity via dependency injection

All components are injected via Hydra `_target_` — never use internal builder helpers. Any part of the architecture can be swapped in config without touching code:

```yaml
_target_: {{repo_name}}.flow_matching_module.FlowMatching

model:
  _target_: {{repo_name}}.models.unet.UNet
  in_channels: 1
  model_channels: 64

optimizer:
  _target_: torch.optim.Adam
  _partial_: true
  lr: 0.001
```

### Extension contract

An extension may: add new files, declare deps via `add_deps.py`, read the base `.copier-answers.yml` via `_external_data`, ask its own questions.

An extension must NOT: overwrite base files, modify files from other extensions, edit `pyproject.toml`/`tasks.py`/`pixi.toml` directly.

### Code style

- Type hints everywhere; Google-style docstrings on public classes/methods
- Always document tensor shapes in ML code (`# (B, C, H, W)`)
- No hardcoded hyperparameters — everything in `configs/`
- PEP 8 enforced via Ruff

## New Template Development Workflow

Use `test_temp/` as a sandbox. Copier templates are flat — all files render into `dst_path` directly.

### 1. Choose a donor template

| New template type | Best donor |
|---|---|
| Supervised learning | `templates/barebone` |
| Classification/regression | `templates/core/classification` |
| Generative model | `templates/generative/flow_matching` |
| RL agent | `templates/rl` |

### 2. Copy donor to test_temp/ and iterate

```bash
cp -r templates/<category>/<donor> test_temp/<new_template>
```

Key files to edit:
- **`copier.yml`** — questions, `_exclude` rules, `_tasks`
- **`src/{{repo_name}}/`** — source files (`.jinja` suffix for files needing rendering)
- **`configs/`** — Hydra config files

Test generation:
```bash
copier copy test_temp/<new_template> test_temp/generated --defaults \
  --data project_name=my_test --data deps_manager=pip --trust
```

### 3. Add tests to `tests/test_base_generation.py`

Follow the `_generate_*` helper pattern established in that file. Add:
- Full structure test
- Deps variants (pip/uv/pixi)
- Config naming test (assert `_target_` uses `project_name`)

### 4. Run the test suite

```bash
pytest tests/test_base_generation.py -k "<new_template>" -m "not slow"
pytest tests/ -m "not slow"  # full fast suite
```

### 5. Transfer to templates/

```bash
cp -r test_temp/<new_template> templates/<category>/<new_template>
rm -rf test_temp/<new_template> test_temp/generated/
```
