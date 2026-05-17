# ML Template Library

[![Build Status](https://github.com/MoustHolmes/cookiecutter-ml-templates/actions/workflows/ci.yml/badge.svg)](https://github.com/MoustHolmes/cookiecutter-ml-templates/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A curated collection of [Copier](https://copier.readthedocs.io/) templates for ML projects, focused on PyTorch, PyTorch Lightning, Hydra, and MLOps best practices. Templates support `copier update` — when the template improves, your project can pull in the changes.

## Motivation

ML projects involve repetitive setup and boilerplate. This library provides clean, opinionated starting points that capture real patterns — not toy examples — with dependency injection, Hydra config composition, and a consistent test structure across all templates.

## Getting Started

### 1. Install Copier

```bash
pip install copier
```

### 2. Generate a project

```bash
mkdir my_project && cd my_project
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/barebone . --trust
```

Or for a specific template:

```bash
# Flow matching / generative models
mkdir my_flow && cd my_flow
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/generative/flow_matching . --trust

# Reinforcement learning (SAC, TD3, PPO, RPO, DQN)
mkdir my_rl && cd my_rl
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/rl . --trust
```

Each template asks for `deps_manager` — choose **pixi**, **uv**, or **pip**:

| Choice | What you get |
|--------|-------------|
| `pixi` | `pixi.toml` with conda-forge deps + `pixi run train` |
| `uv` | `pyproject.toml` inline deps + `tasks.py` using `uv run` |
| `pip` | `requirements.txt` + `tasks.py` using standard pip |

### 3. Apply an extension (optional)

Extensions add features without modifying your base files. Apply from inside your project:

```bash
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/extensions/image_logger . --trust
```

### 4. Pull template updates

When the upstream template improves, update your project:

```bash
copier update --trust
# Update only an extension:
copier update --answers-file .copier-answers.image_logger.yml --trust
```

## Available Templates

| Template | Path | Description | Status |
|----------|------|-------------|--------|
| **Barebone** | `templates/barebone` | Minimal PyTorch Lightning + Hydra starting point | ✅ Stable |
| **Classification** | `templates/core/classification` | MNIST image classification | ✅ Stable |
| **Flow Matching** | `templates/generative/flow_matching` | Complete flow matching implementation | ✅ Stable |
| **Reinforcement Learning** | `templates/rl` | SAC, TD3, PPO, RPO, DQN with Gymnasium | ✅ Stable |

## Available Extensions

| Extension | Path | Description | Compatible with |
|-----------|------|-------------|-----------------|
| **Image Logger** | `templates/extensions/image_logger` | WandB image logging callback | classification |

## Repository Structure

```
cookiecutter-ml-templates/
├── _shared/
│   ├── questions/          # Shared Copier question definitions (author, deps, licensing)
│   └── scripts/            # Shared Python helpers (add_deps.py for dep injection)
├── templates/
│   ├── barebone/           # Minimal starting point
│   ├── core/
│   │   └── classification/ # Image classification
│   ├── generative/
│   │   └── flow_matching/  # Flow matching / generative models
│   ├── rl/                 # Reinforcement learning
│   └── extensions/
│       └── image_logger/   # WandB image logging extension
├── tests/                  # Template generation tests (Copier API)
├── .github/workflows/      # CI: fast tests on every push, slow tests on main
└── requirements.txt        # Dev dependencies (copier, pytest, tomlkit, ...)
```

## Core Principles

- **Dependency injection**: all components injected via Hydra `_target_`; no internal `_build_*` helpers
- **Model/LightningModule separation**: models are pure `forward()`, modules own the training algorithm
- **Composable extensions**: extensions add files without touching base template output
- **Three deps managers supported**: pip, uv, and pixi — all tested

## Technology Stack

- Templating: [Copier](https://copier.readthedocs.io/)
- ML Framework: [PyTorch](https://pytorch.org/)
- High-Level ML Library: [PyTorch Lightning](https://lightning.ai/pytorch-lightning)
- Configuration: [Hydra](https://hydra.cc/)
- Linting: [Ruff](https://docs.astral.sh/ruff/)
- Testing: [Pytest](https://docs.pytest.org/)
- Task Runner: [Invoke](https://www.pyinvoke.org/) (pip/uv) · [Pixi](https://pixi.sh/) (pixi)
- Documentation: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

## Contributing

Contributions welcome. See the [Contributing Guidelines](docs/development/contributing.md).

## Acknowledgements

Inspired by [lightning-hydra-template](https://github.com/ashleve/lightning-hydra-template) and [mlops_template](https://github.com/SkafteNicki/mlops_template).
