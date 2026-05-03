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
