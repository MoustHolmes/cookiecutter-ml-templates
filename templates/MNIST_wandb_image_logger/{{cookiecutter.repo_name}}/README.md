# wandb_logger

WandB logging development for ML templates

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
│   └── wandb_logger/
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

1. Create environment:
```bash
conda create -n wandb_logger python=3.10
conda activate wandb_logger
```

2. Install dependencies:
```bash
pip install -e ".[dev]"  # Install package in development mode with dev dependencies
```

3. Initialize pre-commit hooks:
```bash
pre-commit install
```

## Development Workflow

The project uses `invoke` for task automation. Here are the main commands:

- `invoke create-environment` - Create a new conda environment
- `invoke requirements` - Install project requirements
- `invoke dev-requirements` - Install development requirements
- `invoke test` - Run tests
- `invoke build-docs` - Build documentation
- `invoke serve-docs` - Serve documentation locally

## Project Guidelines

- Write tests for all critical components (datasets, models, training loops)
- Document input/output tensor shapes in ML code
- Use type hints consistently
- Keep code modular and follow the project structure
- Handle errors gracefully with informative messages
- Use Hydra for all configuration management
- Implement proper logging with Weights & Biases

## Author

Moust Holmes
