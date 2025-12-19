"""Post-generation script for classification template."""

import os
from pathlib import Path
from keyword import iskeyword
from operator import ge, le

project_name = "{{cookiecutter.project_name}}"
python_version = "{{cookiecutter.python_version}}"
use_wandb = "{{cookiecutter.use_wandb}}"
include_examples = "{{cookiecutter.include_examples}}"
deps_manager = "{{cookiecutter.deps_manager}}"

# Project name validation
if not project_name.isidentifier() or not project_name.islower():
    msg = (
        "\nProject name must be a valid Python name and lowercase. "
        "It must not contain spaces or special characters, and must not start with a number. "
        "In general, use only lowercase letters and underscores.\n"
    )
    raise ValueError(msg)

if iskeyword(project_name):
    msg = "Project name cannot be a Python keyword."
    raise ValueError(msg)

# Python version validation
min_version = "3.10"
max_version = "3.13"
if not (ge(python_version, min_version) and le(python_version, max_version)):
    msg = (
        f"Python version must be between {min_version} and {max_version}. "
        "These are the versions that still receive support."
    )
    raise ValueError(msg)

# Validate wandb and examples choices
if use_wandb not in ["yes", "no"]:
    msg = "use_wandb must be either 'yes' or 'no'"
    raise ValueError(msg)

if include_examples not in ["yes", "no"]:
    msg = "include_examples must be either 'yes' or 'no'"
    raise ValueError(msg)

# Handle dependency manager option
if deps_manager == "uv":
    # Remove pip-specific files
    for file in ["requirements.txt", "requirements_dev.txt", "tasks_pip.py"]:
        if Path(file).exists():
            os.remove(file)

    # Rename uv tasks
    if Path("tasks_uv.py").exists():
        os.rename("tasks_uv.py", "tasks.py")

elif deps_manager == "pip":
    # Remove uv-specific files
    if Path("tasks_uv.py").exists():
        os.remove("tasks_uv.py")

    # Rename pip tasks
    if Path("tasks_pip.py").exists():
        os.rename("tasks_pip.py", "tasks.py")

