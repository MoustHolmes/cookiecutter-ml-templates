# Template Options Reference

Complete reference for all template configuration options. Options are defined in `copier.yml` and prompted interactively when you run `copier copy`.

## Shared Options (all templates)

These come from `_shared/questions/author.yml` and `_shared/questions/deps_manager.yml`.

### project_name

```yaml
project_name:
    type: str
    help: Python package name (lowercase, underscores only)
    default: my_project
    validator: >-
        {% if not project_name.isidentifier() or project_name != project_name.lower() %}
        project_name must be a valid Python identifier and fully lowercase.
        {% endif %}
```

- Must be a valid Python identifier (letters, digits, underscores; cannot start with a digit)
- Must be fully lowercase
- Cannot be a Python keyword

### repo_name

Derived automatically from `project_name`. Not prompted.

```yaml
repo_name:
    type: str
    default: "{{ project_name | lower | replace(' ', '_') | replace('-', '_') }}"
    when: false
```

### author_name / author_email

Standard author fields. No validation.

### github_username

Defaults to `author_name` lowercased with spaces removed. Used by the optional `gh repo create` task.

### description

Short project description. Used in `pyproject.toml` and `gh repo create`.

### python_version

```yaml
python_version:
    type: str
    help: Python version
    default: "3.12"
    choices: ["3.10", "3.11", "3.12", "3.13"]
```

### deps_manager

```yaml
deps_manager:
    type: str
    help: Dependency manager
    default: pip
    choices: [pip, uv, pixi]
```

Controls which dependency files are generated:

| Value | Generated files |
|-------|----------------|
| `pip` | `requirements.txt`, `requirements_dev.txt` |
| `uv` | `pyproject.toml` with inline deps (no `requirements.txt`) |
| `pixi` | `pixi.toml` (no `requirements.txt`, no `tasks.py`) |

### open_source_license

```yaml
# from _shared/questions/licensing.yml
open_source_license:
    choices: [MIT, BSD-3-Clause, Apache-2.0, No license file]
```

### create_github_repo

Boolean. If `true`, the `_tasks:` block runs `gh repo create` after generation. Requires the [GitHub CLI](https://cli.github.com/) (`gh`) to be installed and authenticated.

## Barebone-Only Options

### project_structure

```yaml
project_structure:
    type: str
    help: Include docs/ with MkDocs setup?
    default: full
    choices: [full, minimal]
```

| Value | Effect |
|-------|--------|
| `full` | Includes `docs/` with MkDocs Material setup |
| `minimal` | `docs/` directory is excluded; `build_docs`/`serve_docs` tasks are removed from `tasks.py` |

## Flow Matching-Only Options

### pytorch_lightning_version

```yaml
pytorch_lightning_version:
    type: str
    help: PyTorch Lightning version
    default: "2.2.0"
```

## Copier Internal Keys

These keys in `copier.yml` control Copier's behaviour (not prompted to the user):

| Key | Purpose |
|-----|---------|
| `_answers_file` | Where Copier saves answers (default: `.copier-answers.yml`) |
| `_exclude` | List of file/directory patterns to skip, supports Jinja2 conditions |
| `_tasks` | Shell commands to run after generation |
| `_skip_if_exists` | Patterns Copier will not overwrite on `copier update` |
| `_jinja_extensions` | Jinja2 extensions loaded during rendering |
| `_external_data` | Load data from external files (used by extensions) |

## Answer File

Copier writes your answers to `.copier-answers.yml` after generation. This file is used by `copier update` to default prompts to your original values. Commit it to version control.

```yaml
# .copier-answers.yml (example)
_commit: main
_src_path: gh:MoustHolmes/cookiecutter-ml-templates/templates/barebone
author_email: jane@example.com
author_name: Jane Doe
deps_manager: uv
description: A machine learning project.
github_username: janedoe
open_source_license: MIT
project_name: awesome_classifier
project_structure: full
python_version: "3.12"
repo_name: awesome_classifier
```
