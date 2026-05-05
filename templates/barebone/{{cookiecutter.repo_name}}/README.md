# {{cookiecutter.repo_name}}

{{cookiecutter.description}}

## Overview

A minimal, well-structured machine learning project template with emphasis on:
- Clean code structure and best practices
- Test-driven development
- Reproducible experiments
- Comprehensive documentation
- Modern tooling integration

## Project Structure

```
├── configs/          # Hydra configuration files
├── data/
│   ├── processed/   # Processed data
│   └── raw/         # Raw data
├── docs/            # Documentation
├── notebooks/       # Jupyter notebooks
├── reports/         # Generated reports and figures
│   └── figures/
├── src/             # Source code
│   └── {{cookiecutter.repo_name}}/
├── tests/           # Unit tests
└── tasks.py         # Automation tasks
```

## Features

- 📊 **Experiment Management**:
  - Hydra for configuration management
  - Weights & Biases for experiment tracking
  - PyTorch Lightning for structured training loops

- 🔍 **Code Quality**:
  - Pre-commit hooks with Ruff and MyPy
  - Automated code formatting
  - Static type checking
  - Security checks with Bandit

- 📝 **Documentation**:
  - Material for MkDocs
  - Google-style docstrings
  - Type hints

- ✅ **Testing**:
  - pytest for unit testing
  - Coverage reporting
  - Test-driven development ready

## Getting Started

{% if cookiecutter.deps_manager == "pixi" %}
1. Install dependencies:
```bash
pixi install
```

2. Initialize pre-commit hooks:
```bash
pixi run pre-commit install
```
{% elif cookiecutter.deps_manager == "uv" %}
1. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

2. Initialize pre-commit hooks:
```bash
pre-commit install
```
{% else %}
1. Create conda environment:
```bash
conda create -n {{cookiecutter.repo_name}} python={{cookiecutter.python_version}}
conda activate {{cookiecutter.repo_name}}
```

2. Install dependencies:
```bash
pip install -e ".[dev]"
```

3. Initialize pre-commit hooks:
```bash
pre-commit install
```
{% endif %}

## Development Workflow

{% if cookiecutter.deps_manager == "pixi" %}
Tasks are defined in `pixi.toml` and run with `pixi run`:

- `pixi run train` - Run training
- `pixi run test` - Run tests
- `pixi run lint` - Lint code
- `pixi run format` - Format code
- `pixi run build-docs` - Build documentation
- `pixi run serve-docs` - Serve documentation locally
{% else %}
The project uses `invoke` for task automation. Here are the main commands:

- `invoke create-environment` - Create a new conda/venv environment
- `invoke requirements` - Install project requirements
- `invoke dev-requirements` - Install development requirements
- `invoke test` - Run tests
- `invoke build-docs` - Build documentation
- `invoke serve-docs` - Serve documentation locally
{% endif %}

## Project Guidelines

- Write tests for all critical components (datasets, models, training loops)
- Document input/output tensor shapes in ML code
- Use type hints consistently
- Keep code modular and follow the project structure
- Handle errors gracefully with informative messages
- Use Hydra for all configuration management
- Implement proper logging with Weights & Biases

## Author

{{cookiecutter.author_name}}
