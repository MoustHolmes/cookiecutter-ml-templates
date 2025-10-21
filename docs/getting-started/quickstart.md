# Quick Start

Get up and running with Cookiecutter ML Templates in minutes!

## Prerequisites

- Python 3.10 or higher
- pip or conda package manager
- Git (for cloning from GitHub)

## Installation

### Install Cookiecutter

=== "pip"
    ```bash
    pip install cookiecutter
    ```

=== "conda"
    ```bash
    conda install -c conda-forge cookiecutter
    ```

=== "pipx (recommended)"
    ```bash
    pipx install cookiecutter
    ```

!!! tip "Why pipx?"
    `pipx` installs packages in isolated environments, preventing dependency conflicts. Perfect for CLI tools like cookiecutter!

## Create Your First Project

### 1. Choose a Template

Start with the **barebone** template for maximum flexibility:

```bash
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/barebone
```

Or use the **flow matching** template for a complete example:

```bash
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/flow_matching
```

### 2. Answer the Prompts

You'll be asked to configure your project:

```plaintext
repo_name [my_ml_project]: awesome_classifier
author_name [Your Name]: Jane Doe
author_email [your.email@example.com]: jane@example.com
python_version [3.10]: 3.10
project_structure [full]: full
deps_manager [pip]: uv
```

!!! info "Template Options"
    - **project_structure**: `full` includes docs, `minimal` excludes them
    - **deps_manager**: Choose between `pip` or `uv` for dependency management

### 3. Navigate to Your Project

```bash
cd awesome_classifier
```

### 4. Set Up the Environment

=== "pip"
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    pip install -e .
    ```

=== "uv (faster!)"
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    uv pip install -r requirements.txt
    uv pip install -e .
    ```

### 5. Run the Tests

Verify everything works:

```bash
pytest tests/
```

You should see all tests passing! ✅

### 6. Start Training

Run a training example:

```bash
python src/awesome_classifier/train.py
```

## What's Included?

Your generated project contains:

```
awesome_classifier/
├── configs/              # Hydra configuration files
│   ├── train_config.yaml
│   ├── data/            # Data module configs
│   ├── model/           # Model configs
│   └── trainer/         # Trainer configs
├── src/                 # Source code
│   └── awesome_classifier/
│       ├── train.py     # Training script
│       └── ...
├── tests/               # Unit tests
├── data/                # Data directory
├── notebooks/           # Jupyter notebooks
├── docs/                # Documentation (if full structure)
└── pyproject.toml       # Project metadata
```

## Next Steps

Now that you have a project running:

1. **[Customize Configuration](../guides/hydra-config.md)** - Learn how to use Hydra
2. **[Add Your Data](../guides/project-structure.md)** - Set up your datasets
3. **[Implement Your Model](../guides/project-structure.md)** - Create your architecture
4. **[Write Tests](../guides/testing.md)** - Ensure code quality

## Common Issues

!!! warning "Import Errors"
    If you get import errors, make sure you installed the package in editable mode:
    ```bash
    pip install -e .
    ```

!!! warning "Hydra Config Errors"
    If Hydra can't find configs, ensure you're running from the project root:
    ```bash
    cd awesome_classifier
    python src/awesome_classifier/train.py
    ```

## Getting Help

- 📖 Browse the [Template Documentation](../available-templates/overview.md)
- 💬 Check the [FAQ](../reference/faq.md)
- 🐛 Report issues on [GitHub](https://github.com/MoustHolmes/cookiecutter-ml-templates/issues)
