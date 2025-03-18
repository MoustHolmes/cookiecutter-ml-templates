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

1. Create a virtual environment:
```bash
conda create -n {{cookiecutter.repo_name}} python={{cookiecutter.python_version}}
conda activate {{cookiecutter.repo_name}}
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

{% if cookiecutter.use_wandb == "yes" %}
3. Set up Weights & Biases:
```bash
wandb login
```
{% endif %}

## Author

{{cookiecutter.author_name}}
