# Contributing

We welcome contributions. This guide covers the mechanics.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a branch for your changes
4. Make your changes
5. Run tests
6. Submit a pull request

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/cookiecutter-ml-templates.git
cd cookiecutter-ml-templates
pip install -r requirements.txt
```

## Running Tests

```bash
# Fast tests only
pytest tests/ -m "not slow"

# All tests including integration
pytest tests/ -m slow
```

## Code Style

We use:
- **Ruff** for linting and formatting
- **pre-commit** hooks

Install pre-commit hooks:

```bash
pre-commit install
```

## Adding a New Template

1. Create the template directory under `templates/`
2. Add `copier.yml` with questions and validation
3. Add the flat project skeleton (no outer `{{project_name}}/` wrapper)
4. Add tests in `tests/test_create_project.py`
5. Add documentation in `docs/available-templates/`
6. Run integration tests

See [Creating Templates](creating-templates.md) for the full workflow.

## Pull Request Process

1. Update tests
2. Update documentation
3. Ensure all tests pass (`pytest tests/ -m "not slow"`)
4. Update CHANGELOG (if applicable)
5. Submit PR with clear description

## Questions?

Open an issue on GitHub.
