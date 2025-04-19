# Cookiecutter Machine Learning Template Library

[![Documentation Status](https://readthedocs.org/projects/your-docs-slug/badge/?version=latest)](https://your-docs-slug.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://github.com/YourUsername/YourRepoName/actions/workflows/ci.yml/badge.svg)](https://github.com/YourUsername/YourRepoName/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A curated collection of Cookiecutter templates designed to jumpstart Machine Learning projects with a focus on PyTorch, PyTorch Lightning, Hydra, and MLOps best practices.

## Motivation

Developing Machine Learning models often involves repetitive setup and boilerplate code. Existing projects on platforms like GitHub can be outdated, poorly documented, or overly simplistic. This library aims to solve these issues by providing:

* **Reusable Foundations:** Clean, well-structured templates that capture best practices learned from real projects.
* **Standardization:** A consistent structure across different ML task types (classification, regression, RL, etc.).
* **Educational Resource:** Clear examples and documentation explaining *why* certain choices were made and how to use the included tools effectively.
* **Bridging the Gap:** Moving beyond simple code snippets to provide robust starting points for complex projects.
* **Ease of Sharing:** A way to package and share successful project structures and patterns.

## Core Principles

1.  **Best Practices:** Adherence to modern MLOps principles, including robust configuration management, code formatting, testing, and versioning.
2.  **Educational:** Templates and documentation designed to be learning resources, explaining the tools and techniques used.
3.  **Modular:** Clear separation of concerns (e.g., data loading, model definition, training loop, configuration) to enhance readability, maintainability, and debuggability. Enables easy toggling of features and backtracking to simpler states.

## Features

* **Multiple Specialized Templates:** Start closer to your specific goal (e.g., image classification, regression, RL) rather than adapting a generic template.
* **Cookiecutter Driven:** Flexible project generation allowing users to choose components and configure settings upfront. No runtime dependency on Cookiecutter after project creation.
* **Modern Tech Stack:** Built upon PyTorch, PyTorch Lightning (for structure and features like Callbacks, distributed training), and Hydra (for powerful configuration).
* **Developer Experience:** Integrates standard tooling like Ruff, Black, pre-commit, Pytest, and Invoke for code quality, consistency, and task automation.
* **Comprehensive Documentation:** Using MkDocs Material for clear, searchable, and extensive documentation beyond simple API references.
* **MLOps Integrations (Planned/Included):**
    * Logging: Weights & Biases (W&B) integration, including Model Registry and Artifacts for datasets/predictions.
    * Launchers: Support for local execution, Docker, and planned integration with cloud platforms (GCP Vertex AI) and potentially cluster schedulers (SLURM).
    * Testing: Robust unit and integration testing structure within each template.

## Technology Stack

* Templating: [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/)
* ML Framework: [PyTorch](https://pytorch.org/)
* High-Level ML Library: [PyTorch Lightning](https://lightning.ai/pytorch-lightning)
* Configuration Management: [Hydra](https://hydra.cc/)
* Linting/Formatting: [Ruff](https://docs.astral.sh/ruff/), [Black](https://github.com/psf/black)
* Pre-commit Hooks: [pre-commit](https://pre-commit.com/)
* Testing: [Pytest](https://docs.pytest.org/)
* Task Runner: [Invoke](https://www.pyinvoke.org/)
* Documentation: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
* Environment Management: [Conda](https://docs.conda.io/) (Recommended, potentially with `uv` support later)

## Repository Structure

This repository uses a mono-repo structure containing multiple independent Cookiecutter templates:

```
Cookiecutter_machine_learning_template_library/
├── docs/             # Global documentation source (MkDocs)
├── hooks/            # Shared Cookiecutter hooks (optional)
├── templates/        # Collection of ML project templates
│   ├── barebone/     # Minimalistic template
│   ├── barebone_classification/
│   └── ...           # Other specialized templates (regression, RL, etc.)
├── tests/            # Tests for template generation validation
├── tasks.py          # Invoke tasks for automation
├── .pre-commit-config.yaml
├── .github/workflows/ # CI/CD pipelines
├── README.md         # This file
└── requirements.txt  # Dev dependencies for the meta-repo
```
## Available Templates (Initial)

* `templates/barebone`: A minimal starting point with the core structure.
* `templates/barebone_classification`: Barebone template configured for a classification task.
* *(Planned)* `mnist_classification`: A full example for MNIST classification.
* *(Planned)* `barebone_regression`: Barebone template for regression.
* *(Planned)* Other templates for Object Detection, Reinforcement Learning, LLM Finetuning, Diffusion Models, etc.

## Getting Started

To use a template, install Cookiecutter and point it to this repository, specifying the desired template directory:

```bash
pip install cookiecutter

# Example: Use the barebone classification template
# Remember to replace YourUsername/YourRepoName with the actual repository path
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/barebone

# Or use the full URL:
# Remember to replace YourUsername/YourRepoName with the actual repository path
cookiecutter https://github.com/MoustHolmes/cookiecutter-ml-templates --directory=templates/barebone

Follow the prompts to configure your new project.DocumentationFor detailed usage instructions, guides on the included tools, MLOps concepts, and contribution guidelines, please refer to the Full Documentation. ## ContributingContributions are welcome! Please read the Contributing Guidelines (to be created) and check the Issues page. ## LicenseThis project is licensed under the MIT License - see the LICENSE file for details. ## AcknowledgementsThis project draws inspiration from excellent existing templates and tools, including:[Lightning-Hydra-Template](https://github.com/ashleve/lightning-hydra-template)[mlops_template](https://github.com/SkafteNicki/mlops_template )
