# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

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

Templates are **flat** Copier templates: all files render directly into the destination directory (no outer `{{project_name}}/` subdirectory).

| Template | Domain |
|---|---|
| `templates/barebone/` | Minimal PyTorch Lightning + Hydra scaffold |
| `templates/core/classification/` | MNIST image classification |
| `templates/generative/flow_matching/` | Flow matching generative model |
| `templates/rl/` | RL with SAC, TD3, PPO, RPO, DQN (Gymnasium) |
| `templates/extensions/image_logger/` | WandB image logging (applied on top of a base) |

### Key template options

- `deps_manager`: `pip`, `uv`, or `pixi` — controls which dependency files are generated via `_exclude` in `copier.yml`
- `project_structure`: `full` (includes `docs/`) or `minimal` — barebone only
- `create_github_repo`: calls `gh repo create` via `_tasks` after generation
- `project_name` must be a valid lowercase Python identifier; `repo_name` is derived from it as a hidden question and is NOT stored in `.copier-answers.yml`

The `_shared/` directory contains shared question definitions (`!include`-d by all templates) and `_shared/scripts/add_deps.py` (used by extension `_tasks`).

### Testing strategy

Tests validate template generation using the Copier Python API:

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

- `tests/test_base_generation.py` — structure, deps variants, license, config naming, answers file
- `tests/test_validation.py` — validator rejection tests
- `tests/test_extension_application.py` — extension application and deps injection
- `tests/test_add_deps.py` — unit tests for `add_deps.py`

## Design Philosophy

### Model vs LightningModule separation

**Models** (`src/<repo>/models/`) hold only weights: take data in, return a tensor out. No loss, no optimizer, no training logic.

**LightningModules** (`src/<repo>/<algo>_module.py`) contain all algorithm logic: loss functions, training/validation steps, schedulers, sampling, solver calls.

```
models/unet.py               ← weights + forward pass only
flow_matching_module.py      ← loss, noise schedule, ODE solver, training step
```

### Modularity via dependency injection

All components are injected via Hydra `_target_` — never use internal builder helpers.

### Extension contract

Extensions may add files and declare deps via `add_deps.py`. They must NOT overwrite base files or edit `pyproject.toml`/`tasks.py`/`pixi.toml` directly. See the `ml-templates` skill for the full contract.

## New Template Development Workflow

Use `test_temp/` as a sandbox.

### 1. Choose a donor template

| New template type | Best donor |
|---|---|
| Supervised learning | `templates/barebone` |
| Classification/regression | `templates/core/classification` |
| Generative model | `templates/generative/flow_matching` |
| RL agent | `templates/rl` |

### 2. Copy and iterate in test_temp/

Key files: `copier.yml`, `src/{{repo_name}}/`, `configs/`

### 3. Add tests to `tests/test_base_generation.py`

Follow the `_generate_*` helper pattern. Add: full structure test, deps variants, config naming test.

### 4. Run the test suite

```bash
pytest tests/test_base_generation.py -k "<new_template>" -m "not slow"
pytest tests/ -m "not slow"
```

### 5. Transfer to templates/

```bash
cp -r test_temp/<new_template> templates/<category>/<new_template>
rm -rf test_temp/<new_template> test_temp/generated/
```
