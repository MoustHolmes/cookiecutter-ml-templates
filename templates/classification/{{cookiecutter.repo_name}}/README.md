# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Project Structure

```
├── configs/          # Hydra configuration files
├── data/            # Data files and datasets
├── src/             # Source code
│   ├── models/      # Neural network models
│   ├── datasets/    # Dataset and data loading code
│   └── utils/       # Utility functions
└── tests/           # Test files
```

## Setup

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
pip install -r requirements.txt
```

3. Initialize pre-commit hooks:
```bash
pre-commit install
```
{% endif %}

{% if cookiecutter.use_wandb == "yes" %}
3. Set up Weights & Biases:
```bash
wandb login
```
{% endif %}

## Author

{{cookiecutter.author_name}}
