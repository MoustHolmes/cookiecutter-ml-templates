# Barebone Template

The minimal template for maximum flexibility. Use this when you want the project skeleton without any algorithm-specific code.

## Features

- Minimal `src/` layout with PyTorch Lightning boilerplate
- Hydra configuration setup
- pip, uv, and pixi support
- Optional `docs/` directory with MkDocs setup
- Pytest test suite scaffold

## Usage

Create a new directory, then copy the template into it:

```bash
mkdir my_project && cd my_project
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/barebone . --trust
```

## Options

| Option | Choices | Default | Description |
|--------|---------|---------|-------------|
| `project_name` | any valid Python identifier | `my_project` | Package name (lowercase, underscores) |
| `author_name` | string | `Your Name` | |
| `author_email` | string | `your@email.com` | |
| `python_version` | 3.10, 3.11, 3.12, 3.13 | `3.12` | |
| `deps_manager` | pip, uv, pixi | `pip` | Dependency manager |
| `project_structure` | full, minimal | `full` | `full` includes `docs/`; `minimal` removes it |
| `open_source_license` | MIT, BSD-3-Clause, Apache-2.0, No license file | MIT | |
| `create_github_repo` | true/false | false | Create GitHub repo via `gh` CLI after generation |

## Updating

Pull template improvements into an existing project:

```bash
copier update --trust
```

Full documentation coming soon.
