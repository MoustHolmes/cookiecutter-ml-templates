# Quick Start

Get a project running from a template in a few minutes.

## Prerequisites

- Python 3.10 or higher
- Git
- Copier (`pip install copier`)

## Create Your First Project

### 1. Make the project directory

Templates are flat — you create the directory first, then copy the template into it.

```bash
mkdir my_project && cd my_project
```

### 2. Choose a template and run copier

Start with the **barebone** template for maximum flexibility:

```bash
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/barebone . --trust
```

Or use the **flow matching** template for a complete generative model example:

```bash
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/generative/flow_matching . --trust
```

### 3. Answer the prompts

```plaintext
project_name [my_project]: awesome_classifier
author_name [Your Name]: Jane Doe
author_email [your@email.com]: jane@example.com
python_version [3.12]: 3.12
deps_manager [pip]: uv
project_structure [full]: full
```

!!! info "Template options"
    - **`project_structure`**: `full` includes a `docs/` directory with MkDocs setup; `minimal` removes it.
    - **`deps_manager`**: `pip`, `uv`, or `pixi` — controls which dependency files are generated.

Copier writes all files directly into the current directory and saves your answers to `.copier-answers.yml`.

### 4. Set up the environment

=== "pip"
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    pip install -e .
    ```

=== "uv"
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    uv pip install -r requirements.txt
    uv pip install -e .
    ```

=== "pixi"
    ```bash
    pixi install
    ```

### 5. Run the tests

```bash
pytest tests/
```

### 6. Start training

```bash
python src/awesome_classifier/train.py
```

## What's in the generated project

```
awesome_classifier/
├── configs/              # Hydra configuration files
│   ├── train_config.yaml
│   ├── data/
│   ├── model/
│   └── trainer/
├── src/
│   └── awesome_classifier/
│       ├── train.py     # Hydra entry point
│       └── ...
├── tests/
├── data/
├── notebooks/
├── docs/                # Only present if project_structure=full
├── pyproject.toml
└── .copier-answers.yml  # Saved answers for copier update
```

## Updating your project later

When the template releases improvements, pull them into your existing project:

```bash
copier update --trust
```

Copier re-runs the questions (defaulting to your saved answers) and merges changes into your project.

## Next Steps

1. **[Customize Configuration](../guides/hydra-config.md)** — learn Hydra config groups and overrides
2. **[Add Your Data](../guides/project-structure.md)** — set up your datasets
3. **[Write Tests](../guides/testing.md)** — keep the test suite green

## Common Issues

!!! warning "Import errors"
    Make sure you installed the package in editable mode:
    ```bash
    pip install -e .
    ```

!!! warning "Hydra config errors"
    Run from the project root so Hydra can resolve config paths:
    ```bash
    cd my_project
    python src/my_project/train.py
    ```

## Getting Help

- Browse the [Template Documentation](../available-templates/overview.md)
- Check the [FAQ](../reference/faq.md)
- Report issues on [GitHub](https://github.com/MoustHolmes/cookiecutter-ml-templates/issues)
