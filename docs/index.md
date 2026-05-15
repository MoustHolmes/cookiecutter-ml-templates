# ML Templates

A curated collection of production-ready [Copier](https://copier.readthedocs.io/) templates for ML projects, with best practices built in.

## Why This Project?

Developing ML models involves repetitive setup. These templates give you a tested, opinionated starting point so you can focus on the model.

- Clean structure derived from real projects
- Consistent layout across ML task types
- PyTorch Lightning + Hydra + modern tooling
- pip, uv, and pixi all supported

## Quick Start

```bash
# Install copier
pip install copier

# Create a new project from the barebone template
mkdir my_project && cd my_project
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/barebone . --trust
```

[Get Started →](getting-started/quickstart.md){ .md-button .md-button--primary }

## Features

<div class="grid cards" markdown>

- :material-lightning-bolt: **PyTorch Lightning**

    ---
    
    Built on PyTorch Lightning for structure, callbacks, and distributed training

- :material-cog: **Hydra Configuration**

    ---
    
    Config management with composition, overrides, and experiments

- :material-test-tube: **Testing First**

    ---
    
    Comprehensive unit and integration tests included in every template

- :material-package-variant: **Three Package Managers**

    ---
    
    Support for pip, uv, and pixi

- :material-code-braces: **Code Quality**

    ---
    
    Pre-configured with Ruff and pre-commit hooks

- :material-file-tree: **Flexible Structure**

    ---
    
    Choose minimal or full project structure with docs

</div>

## Available Templates

| Template | Description | Status |
|----------|-------------|--------|
| [**Barebone**](available-templates/barebone.md) | Minimal starting point with core structure | ✅ Stable |
| [**Flow Matching**](available-templates/flow-matching.md) | Complete flow matching implementation | ✅ Stable |
| [**Reinforcement Learning**](available-templates/rl.md) | SAC, TD3, PPO, RPO, DQN with Gymnasium | ✅ Stable |
| [**Classification**](available-templates/classification.md) | Image classification template | 🚧 Beta |
| [**Image Logger** (extension)](available-templates/mnist-wandb.md) | W&B image logging, added to an existing project | ✅ Stable |

## Technology Stack

<div class="grid" markdown>

=== "Core"
    - **[PyTorch](https://pytorch.org/)** - Deep learning framework
    - **[PyTorch Lightning](https://lightning.ai/)** - High-level ML library
    - **[Hydra](https://hydra.cc/)** - Configuration management

=== "Dev Tools"
    - **[Ruff](https://docs.astral.sh/ruff/)** - Fast Python linter and formatter
    - **[Pytest](https://docs.pytest.org/)** - Testing framework
    - **[Invoke](https://www.pyinvoke.org/)** - Task runner

=== "MLOps"
    - **[Weights & Biases](https://wandb.ai/)** - Experiment tracking
    - **[uv](https://docs.astral.sh/uv/)** / **[pixi](https://pixi.sh/)** - Fast package managers
    - **[MkDocs](https://www.mkdocs.org/)** - Documentation

</div>

## Core Principles

!!! tip "Design Philosophy"
    1. **Best Practices** - Modern MLOps with robust config, testing, and versioning
    2. **Educational** - Templates that teach through clear examples
    3. **Modular** - Separation of concerns for maintainability and debugging

## What's New

### Recent Updates

- Migrated from Cookiecutter to **Copier** — flat template structure, `copier update` support
- Added **pixi** as a fully supported dependency manager alongside pip and uv
- MNIST W&B Logger converted to a composable **extension** (`templates/extensions/image_logger`)
- Added **Reinforcement Learning** template with SAC, TD3, PPO, RPO, and DQN
- Integration tests that validate generated projects end-to-end

## Next Steps

<div class="grid cards" markdown>

- [:material-rocket-launch: **Quick Start**](getting-started/quickstart.md)
  
    Get your first project running in minutes

- [:material-book-open-page-variant: **Browse Templates**](available-templates/overview.md)
  
    Explore all available templates and choose the right one

- [:material-school: **Read Guides**](guides/hydra-config.md)
  
    Learn about configuration, testing, and best practices

- [:material-github: **Contribute**](development/contributing.md)
  
    Help make these templates even better

</div>
