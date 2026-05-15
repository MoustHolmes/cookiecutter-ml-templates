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
* **MLOps Integrations:**
    * Logging: Weights & Biases (W&B) integration, including Model Registry and Artifacts for datasets/predictions.
    * Testing: Robust unit and integration testing structure within each template.

## Technology Stack

* Templating: [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/)
* ML Framework: [PyTorch](https://pytorch.org/)
* High-Level ML Library: [PyTorch Lightning](https://lightning.ai/pytorch-lightning)
* Configuration Management: [Hydra](https://hydra.cc/)
* Linting/Formatting: [Ruff](https://docs.astral.sh/ruff/), [Black](https://github.com/psf/black)
* Pre-commit Hooks: [pre-commit](https://pre-commit.com/)
* Testing: [Pytest](https://docs.pytest.org/)
* Task Runner: [Invoke](https://www.pyinvoke.org/) (pip/uv) · [Pixi](https://pixi.sh/) (pixi)
* Documentation: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
* Environment Management: [Pixi](https://pixi.sh/) · [uv](https://docs.astral.sh/uv/) · [Conda](https://docs.conda.io/)

## Repository Structure

This repository uses a mono-repo structure containing multiple independent Cookiecutter templates:

```
cookiecutter-ml-templates/
├── docs/                          # Global documentation source (MkDocs)
├── hooks/                         # Shared Cookiecutter hooks
├── templates/                     # Collection of ML project templates
│   ├── barebone/                  # Minimal starting point
│   ├── flow_matching/             # Flow matching / generative models
│   ├── rl/                        # Reinforcement learning (SAC, TD3, PPO, RPO, DQN)
│   ├── MNIST_wandb_image_logger/  # MNIST with W&B logging
│   └── classification/            # Image classification (beta)
├── tests/                         # Tests for template generation validation
├── .pre-commit-config.yaml
├── .github/workflows/             # CI/CD pipelines
├── mkdocs.yml                     # Docs site config
├── README.md                      # This file
└── requirements.txt               # Dev dependencies for the meta-repo
```
## Available Templates

| Template | Directory | Description | Status |
|----------|-----------|-------------|--------|
| **Barebone** | `templates/barebone` | Minimal starting point with core structure | ✅ Stable |
| **Flow Matching** | `templates/flow_matching` | Complete flow matching implementation | ✅ Stable |
| **Reinforcement Learning** | `templates/rl` | SAC, TD3, PPO, RPO, DQN with Gymnasium | ✅ Stable |
| **MNIST W&B Logger** | `templates/MNIST_wandb_image_logger` | MNIST with Weights & Biases logging | ✅ Stable |
| **Classification** | `templates/classification` | Image classification template | 🚧 Beta |

## Getting Started

### 1. Install Cookiecutter

```bash
pip install cookiecutter
```

### 2. (Optional) Pre-fill your name and email

Run once to save your git identity to `~/.cookiecutterrc`. After this, every template prompt for `author_name`, `author_email`, and `github_username` will be pre-filled — you can still edit them at the prompt.

```bash
# Clone this repo first, then:
invoke setup-defaults
```

This reads from `git config --global user.name`, `git config --global user.email`, and `gh api user` (GitHub CLI, optional). The values are written to `~/.cookiecutterrc` and picked up automatically by all cookiecutter templates.

### 3. Generate a project

```bash
# Minimal starting point
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/barebone

# Reinforcement learning (SAC, TD3, PPO, RPO, DQN)
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/rl

# Flow matching / generative models
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/flow_matching
```

Follow the prompts. Each template asks for `deps_manager` — choose **pixi**, **uv**, or **pip**:

| Choice | What you get |
|--------|-------------|
| `pixi` | `pixi.toml` with conda-forge deps + built-in task runner (`pixi run train`) |
| `uv`   | `pyproject.toml` inline deps + `tasks.py` using `uv run` |
| `pip`  | `requirements.txt` + `tasks.py` using standard pip |

For detailed usage instructions, guides on the included tools, and MLOps concepts, refer to the Full Documentation.
## Contributing
Contributions are welcome! Please read the Contributing Guidelines (to be created) and check the Issues page.
## License
This project is licensed under the MIT License - see the LICENSE file for details.
## Acknowledgements
This project draws inspiration from excellent existing templates and tools,
including:
[Lightning-Hydra-Template](https://github.com/ashleve/lightning-hydra-template)
[mlops_template](https://github.com/SkafteNicki/mlops_template )
