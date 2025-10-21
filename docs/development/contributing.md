# Contributing

We welcome contributions! This guide will help you get started.

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
pytest tests/

# All tests including integration
pytest tests/ -m slow
```

## Code Style

We use:
- **Ruff** for linting
- **Black** for formatting
- **pre-commit** hooks

Install pre-commit hooks:

```bash
pre-commit install
```

## Adding a New Template

1. Create template directory in `templates/`
2. Add cookiecutter.json
3. Add tests in `tests/test_create_project.py`
4. Add documentation
5. Run integration tests

## Pull Request Process

1. Update tests
2. Update documentation
3. Ensure all tests pass
4. Update CHANGELOG (if applicable)
5. Submit PR with clear description

## Questions?

Open an issue on GitHub!
