# cookiecutter-ml-templates
Cookiecutter-based templates for reproducible ML research and rapid prototyping.

# Cookiecutter Machine Learning Template Library

A library of Cookiecutter templates for machine learning projects – designed to promote clean, reproducible, and modular research workflows. This repository provides a collection of specialized templates for various ML use cases such as classification, regression, object detection, and reinforcement learning. It’s aimed at both improving your own workflow and serving as a collaborative resource for the community.

## Overview

The project is designed to:
- **Offer Multiple Specialized Templates:**
  Each template is tailored to a specific task (e.g., barebone, MNIST classification, object detection, cartpole reinforcement learning) to help you quickly get to a working project without extensive modifications.
- **Leverage Cookiecutter Flexibility:**
  Utilize Cookiecutter hooks (`pre_prompt.py`, `pre_gen_project.py`, `post_gen_project.py`) to allow users to include or exclude sections of the template based on project needs.
- **Enhance Code Quality and Reproducibility:**
  Integrate tools like pre-commit (with Ruff and Black), GitHub Actions for CI/CD, and unit tests to ensure the generated projects are reliable and maintainable.
- **Streamline Experiment Management:**
  Utilize PyTorch Lightning for streamlined training loops, Hydra for flexible configuration, and Weights & Biases (WandB) for logging, model registry, and artifact management.
- **Provide Rich Documentation:**
  Documentation is built using MkDocs Material, including educational content, usage examples, and references to additional resources like Lightning-Hydra-Template and ml_ops_template.

## Repository Structure
```
Cookiecutter_machine_learning_template_library/
├── docs/ # Global documentation (MkDocs Material)
├── hooks/ # Shared Cookiecutter hooks (optional; can also be per template)
├── templates/ # Collection of ML project templates
│ ├── barebone/
│ │ ├── cookiecutter.json
│ │ ├── hooks/
│ │ ├── {{ cookiecutter.repo_name }}/
│ │ └── ... (other files)
│ ├── barebone_classification/
│ │ ├── cookiecutter.json
│ │ └── ... (classification-specific scaffold)
│ ├── mnist_classification/
│ │ └── ... (MNIST demo project)
│ ├── barebone_regression/
│ │ └── ... (regression template)
│ ├── starfish_object_detection/
│ │ └── ... (object detection scaffold)
│ └── cartpole_reinforcement_learning/
│ └── ... (reinforcement learning scaffold)
├── tests/ # Integration tests for validating template generation
├── tasks.py # Automation tasks (e.g., build, test, docs, environment setup)
├── .pre-commit-config.yaml # Pre-commit hook configuration (using Ruff, Black, etc.)
├── .github/
│ └── workflows/ # GitHub Actions CI/CD workflows for linting, testing, and docs building
├── README.md # This file
└── requirements.txt # Global development dependencies
```


## Getting Started

### Prerequisites

- **Cookiecutter:**
  Install Cookiecutter if you haven’t already:
  ```bash
  pip install cookiecutter
  ```
- Pre-commit:
To ensure code quality, install pre-commit:
```bash
  pip install pre-commit
  pre-commit install
```

- Conda (optional):
We use Conda for environment management. You can also use alternatives like Poetry if preferred.

Generating a New Project
You can generate a project from a specific template using Cookiecutter’s --directory flag. For example, to generate a barebone project:
```bash
cookiecutter https://github.com/MoustHolmes/Cookiecutter_machine_learning_template_library.git --directory=templates/barebone
```
Replace templates/barebone with the directory of your desired template.

- Templates
Each template is designed for a specific use case:

- barebone: Minimal scaffold for any ML project.
- barebone_classification: Basic structure for classification tasks.
- mnist_classification: A demo project for MNIST classification.
- barebone_regression: Starter for regression projects.
- starfish_object_detection: Scaffold for object detection projects.
- cartpole_reinforcement_learning: Template for reinforcement learning experiments.

Detailed documentation on each template is available in the docs folder.

Contributing
We welcome contributions! Whether you have a new template idea or improvements to existing ones, please check out our CONTRIBUTING.md for guidelines on how to get started.

License
This project is licensed under the MIT License – see the LICENSE file for details.

Additional Resources
Cookiecutter Documentation
PyTorch Lightning
Hydra
Weights & Biases
