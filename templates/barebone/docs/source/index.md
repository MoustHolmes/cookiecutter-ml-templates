# {{ cookiecutter.repo_name }}

{{ cookiecutter.description }}

## Project Overview

This project follows the ML Ops template structure for maintainable and reproducible machine learning projects.

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
│   └── {{ cookiecutter.repo_name }}/
├── tests/           # Unit tests
└── tasks.py         # Automation tasks
```

## Getting Started

1. Create environment:
```bash
conda create -n {{ cookiecutter.repo_name }} python={{ cookiecutter.python_version }}
conda activate {{ cookiecutter.repo_name }}
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
