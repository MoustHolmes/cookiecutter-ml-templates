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
pytest tests/test_create_project.py::test_barebone_template_success
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

This is a mono-repo of [Cookiecutter](https://cookiecutter.readthedocs.io/) templates for ML projects. The repo itself has no package — it's a template library with a test suite that validates generated output.

### Templates

Each template lives in `templates/<name>/` with this structure:
- `cookiecutter.json` — prompts/defaults presented to the user during generation
- `hooks/post_gen_project.py` — runs after generation to handle conditional file removal/renaming and optional GitHub repo creation
- `{{cookiecutter.repo_name}}/` — the generated project skeleton (Jinja2-templated)

Available templates:
- `barebone` — gold-standard minimal template; used as reference structure for tests
- `classification` — barebone configured for classification tasks
- `flow_matching` — full flow matching implementation (PyTorch Lightning + Hydra); the most complete supervised-learning template
- `rl` — reinforcement learning template with SAC, TD3, PPO (discrete + continuous), RPO, and DQN; uses Gymnasium environments; has its own `hooks/post_gen_project.py`
- `MNIST_wandb_image_logger` — MNIST example with W&B image logging

The top-level `hooks/post_gen_project.py` is a shared hook used by simpler templates (e.g., `classification`).

### Key template options (cookiecutter.json)

- `deps_manager`: `pip` or `uv`. Controls whether `requirements.txt`/`requirements_dev.txt` or inline `pyproject.toml` dependencies are used. The post-gen hook renames `tasks_pip.py` or `tasks_uv.py` to `tasks.py` and removes the other.
- `project_structure`: `full` (includes `docs/` with MkDocs) or `minimal` (docs removed, `build_docs`/`serve_docs` tasks stripped from `tasks.py`).
- `create_github_repo`: Optionally calls `gh repo create` via GitHub CLI post-generation.
- `project_name` must be a valid lowercase Python identifier (validated in the hook); `repo_name` is derived from it automatically.
- Supported Python versions: 3.10–3.13 (enforced by hook validation).

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
tasks.py               # Invoke task runner (generated from tasks_pip.py or tasks_uv.py)
pyproject.toml
```

### Testing strategy

`tests/test_create_project.py` validates template generation by:
1. Calling `cookiecutter()` programmatically with `no_input=True` and `extra_context` overrides
2. Asserting that expected files/directories exist in the output
3. For `@pytest.mark.slow` tests: installing deps and running the generated project's own `pytest tests/` suite

The barebone template's `test_project_structure` test serves as the authoritative spec for generated project layout — update it when changing the expected structure.

## Design Philosophy

### Model vs LightningModule separation

**Models** (`src/<repo>/models/`) hold only weights and are responsible for one thing: take data in, return a prediction out. They are task-agnostic. A `UNet` doesn't know whether it's being used for flow matching or segmentation — data goes in, a tensor comes out. Models must not contain loss computation, optimizer logic, or any training algorithm.

**LightningModules** (`src/<repo>/<algo>_module.py`) contain all algorithm logic: loss functions, training/validation steps, schedulers, sampling, solver calls. The module defines *how* the model is trained, not what it is. Examples: `FlowMatchingModule`, `PPOModule`, `SegmentationModule`, `AutoEncoderModule`.

```
models/unet.py        ← weights + forward pass only
flow_matching_module.py  ← loss, noise schedule, ODE solver, training step
```

When implementing a new template, ask: "would this code change if I swapped the backbone architecture?" If yes → it belongs in the LightningModule, not the model.

### Modularity via dependency injection

Never write internal builder helpers like `_build_mlp()` or `_create_encoder()`. If a module needs an MLP, it receives one as a constructor argument. All components are injected via Hydra `_target_` so any part of the architecture can be swapped in config without touching code:

```yaml
_target_: {{cookiecutter.repo_name}}.flow_matching_module.FlowMatching

model:
  _target_: {{cookiecutter.repo_name}}.models.unet.UNet
  in_channels: 1
  model_channels: 64

alpha_beta_scheduler:
  _target_: {{cookiecutter.repo_name}}.modules.schedulers.LinearScheduler

sampler:
  _target_: {{cookiecutter.repo_name}}.modules.samplers.GaussianSampler

ode_solver:
  _target_: {{cookiecutter.repo_name}}.modules.solvers.EulerSolver

optimizer:
  _target_: torch.optim.Adam
  _partial_: true
  lr: 0.001
```

Every dependency that might reasonably change (model architecture, optimizer, scheduler, sampler, solver) is a Hydra-injectable argument. This is the compositional pattern all templates follow.

### Code style

- Type hints everywhere; Google-style docstrings on public classes/methods
- Always document tensor shapes in ML code (`# (B, C, H, W)`)
- Callbacks for non-essential training functionality (logging, checkpointing, visualization)
- No hardcoded hyperparameters — everything goes in `configs/`
- PEP 8 enforced via Ruff; no Black (Ruff formatter handles formatting)

### Testing

- Write tests for all critical components: datasets, models, training steps
- Unit-test models and data modules in isolation (no full training run)
- Use `conftest.py` fixtures for shared objects (model instances, dummy batches, configs)
- Slow integration tests (`@pytest.mark.slow`) install deps and run the generated project's full test suite

### Things to avoid

- Internal `_build_*` helpers that hide architecture choices — inject instead
- Logic about loss or training algorithm inside `models/` — put it in the LightningModule
- Hardcoded values that belong in `configs/`
- Skipping tests for new datasets or model components
- Unnecessary dependencies beyond the template's stated purpose

## New Template Development Workflow

Use `test_temp/` as a sandbox when building a new template. This keeps work-in-progress out of `templates/` until it's ready.

### 1. Choose a donor template

Pick the most structurally similar existing template:

| New template type | Best donor |
|---|---|
| Supervised learning | `barebone` or `flow_matching` |
| Classification/regression | `classification` |
| RL agent | `rl` |
| Logging / quick demo | `MNIST_wandb_image_logger` |

### 2. Copy donor to test_temp/

```bash
cp -r templates/<donor> test_temp/<new_template>
```

The template dir contains only: `cookiecutter.json`, `hooks/`, `{{cookiecutter.repo_name}}/` — no generated output.

### 3. Iterate in sandbox

Edit these three things in `test_temp/<new_template>/`:

- **`cookiecutter.json`** — add/remove/rename parameters
- **`hooks/post_gen_project.py`** — update validation logic and conditional file management
- **`{{cookiecutter.repo_name}}/`** — modify the generated project skeleton (Jinja2-templated files)

Test generation after each major change (outputs land in `test_temp/generated/`, separate from the template):

```bash
cookiecutter test_temp/<new_template> --output-dir test_temp/generated/ --no-input
```

Or use the Python API (more control over parameters):

```python
from cookiecutter.main import cookiecutter
cookiecutter(
    "test_temp/<new_template>",
    no_input=True,
    output_dir="test_temp/generated/",
    extra_context={"project_name": "my_test", "deps_manager": "pip"},
)
```

Inspect the generated output in `test_temp/generated/<project_name>/`. Delete and regenerate freely.

### 4. Validate before transfer

Run the generated project's own test suite:

```bash
cd test_temp/generated/<project_name>
pip install -e ".[dev]"
pytest tests/
```

Fix anything that fails back in `test_temp/<new_template>/`, regenerate, retest.

### 5. Transfer to templates/

When the template is working, copy it across. A template directory is identifiable by the presence of `cookiecutter.json` at its root — generated projects never have this file.

```bash
# Safety check: confirm this is a template, not a generated project
ls test_temp/<new_template>/cookiecutter.json

# Transfer
cp -r test_temp/<new_template> templates/<new_template>
```

The template dir is clean (no `.venv`, `.pixi`, `__pycache__` — those only appear in generated output dirs). A plain `cp -r` is safe.

### 6. Add tests to the test suite

Add to `tests/test_create_project.py` (follow the existing pattern):

```python
def test_<new_template>_structure(temp_dir: Path) -> None:
    """Assert expected files exist after generation."""
    template_dir = (Path(__file__).parent / ".." / "templates" / "<new_template>").resolve()
    cookiecutter(
        template=str(template_dir),
        output_dir=str(temp_dir),
        no_input=True,
        extra_context={"project_name": "test_proj", "python_version": "3.12"},
    )
    generated = temp_dir / "test_proj"
    assert (generated / "src" / "test_proj").exists()
    assert (generated / "tests").exists()
    assert (generated / "configs").exists()
    # Add all expected files/dirs

@pytest.mark.parametrize("deps_manager", ["pip", "uv", "pixi"])
def test_<new_template>_deps_variants(temp_dir: Path, deps_manager: str) -> None:
    """Test each dependency manager variant."""
    ...

@pytest.mark.slow
def test_<new_template>_internal_tests(temp_dir: Path) -> None:
    """Generate project, install deps, run its test suite."""
    ...
```

### 7. Run the test suite

```bash
# Fast check on the new template only
pytest tests/test_create_project.py -k "<new_template>" -m "not slow"

# Full fast suite (no regressions)
pytest tests/ -m "not slow"

# Slow integration test for the new template
pytest tests/test_create_project.py::test_<new_template>_internal_tests
```

### Cleanup

After the template is in `templates/` and tests pass, remove sandbox artifacts:

```bash
rm -rf test_temp/<new_template>
rm -rf test_temp/generated/
```

Keep `test_temp/` itself (it is git-ignored for generated output).
