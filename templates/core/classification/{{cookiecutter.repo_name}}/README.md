# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Project Structure

```
├── configs/                      # Hydra configuration files
│   ├── train_config.yaml         # Top-level training config
│   ├── model/                    # Model hyperparameters
│   ├── data/                     # Data module config
│   ├── trainer/                  # Lightning Trainer config
│   ├── callbacks/                # Callback configs
│   ├── logger/                   # W&B logger config
│   └── experiments/              # Experiment overrides (e.g. debug)
├── data/                         # Downloaded datasets
├── src/{{cookiecutter.repo_name}}/
│   ├── classification_module.py  # LightningModule (loss, training step)
│   ├── data/
│   │   └── mnist_datamodule.py   # LightningDataModule
│   ├── models/                   # Model architectures
│   ├── callbacks/                # Training callbacks
│   └── train.py                  # Hydra entry point
└── tests/                        # Unit tests
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

3. Log in to Weights & Biases:
```bash
wandb login
```

## Training

```bash
python src/{{cookiecutter.repo_name}}/train.py
```

Run with debug config for a quick sanity check:
```bash
python src/{{cookiecutter.repo_name}}/train.py +experiment=debug
```

## Author

{{cookiecutter.author_name}}
