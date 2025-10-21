# Cookiecutter ML Templates

!!! success "Latest Update"
    All templates now include integration tests and are verified to work end-to-end! ✨

A curated collection of **production-ready** Cookiecutter templates designed to jumpstart Machine Learning projects with best practices baked in.

## Why This Project?

Developing ML models often involves repetitive setup and boilerplate code. Existing projects can be:

- 📦 Outdated or poorly documented
- 🎯 Too simplistic for real-world use
- 🔧 Lacking modern MLOps practices

**This library solves these problems** by providing:

✅ **Reusable Foundations** - Clean, well-structured templates from real projects  
✅ **Standardization** - Consistent structure across different ML tasks  
✅ **Educational** - Clear examples with explanations of *why*  
✅ **Production-Ready** - Robust starting points with testing, CI/CD, and more  
✅ **Easy to Share** - Package and distribute successful patterns  

## Quick Start

```bash
# Install cookiecutter
pip install cookiecutter

# Create a new project from the barebone template
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/barebone

# Or from the flow matching template
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/flow_matching
```

[Get Started →](getting-started/quickstart.md){ .md-button .md-button--primary }

## Features

<div class="grid cards" markdown>

- :material-lightning-bolt: **PyTorch Lightning**

    ---
    
    Built on PyTorch Lightning for structure, callbacks, and distributed training

- :material-cog: **Hydra Configuration**

    ---
    
    Powerful config management with composition, overrides, and experiments

- :material-test-tube: **Testing First**

    ---
    
    Comprehensive unit and integration tests included in every template

- :material-package-variant: **Dual Package Managers**

    ---
    
    Support for both pip and UV for dependency management

- :material-code-braces: **Code Quality**

    ---
    
    Pre-configured with Ruff, Black, and pre-commit hooks

- :material-file-tree: **Flexible Structure**

    ---
    
    Choose minimal or full project structure with docs

</div>

## Available Templates

| Template | Description | Status |
|----------|-------------|--------|
| [**Barebone**](available-templates/barebone.md) | Minimal starting point with core structure | ✅ Stable |
| [**Flow Matching**](available-templates/flow-matching.md) | Complete flow matching implementation | ✅ Stable |
| [**MNIST W&B Logger**](available-templates/mnist-wandb.md) | MNIST with Weights & Biases logging | ✅ Stable |
| [**Classification**](available-templates/classification.md) | Image classification template | 🚧 Beta |

## Technology Stack

<div class="grid" markdown>

=== "Core"
    - **[PyTorch](https://pytorch.org/)** - Deep learning framework
    - **[PyTorch Lightning](https://lightning.ai/)** - High-level ML library
    - **[Hydra](https://hydra.cc/)** - Configuration management

=== "Dev Tools"
    - **[Ruff](https://docs.astral.sh/ruff/)** - Fast Python linter
    - **[Black](https://black.readthedocs.io/)** - Code formatter
    - **[Pytest](https://docs.pytest.org/)** - Testing framework
    - **[Invoke](https://www.pyinvoke.org/)** - Task runner

=== "MLOps"
    - **[Weights & Biases](https://wandb.ai/)** - Experiment tracking
    - **[UV](https://docs.astral.sh/uv/)** - Fast package manager
    - **[MkDocs](https://www.mkdocs.org/)** - Documentation

</div>

## Core Principles

!!! tip "Design Philosophy"
    1. **Best Practices** - Modern MLOps with robust config, testing, and versioning
    2. **Educational** - Templates that teach through clear examples
    3. **Modular** - Separation of concerns for maintainability and debugging

## What's New

### Recent Updates

- ✨ Added integration tests that validate generated projects
- 🎯 Standardized structure across all templates
- 📦 Optional project scaffolding (minimal vs full)
- ⚡ UV package manager support
- 🧪 Comprehensive test suite with pytest markers
- 📝 Fixed all template bugs found by integration tests

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
