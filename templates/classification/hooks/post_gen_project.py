from keyword import iskeyword
from operator import ge, le

project_name = "{{cookiecutter.project_name}}"
python_version = "{{cookiecutter.python_version}}"
use_wandb = "{{cookiecutter.use_wandb}}"
include_examples = "{{cookiecutter.include_examples}}"

# Project name validation
if not project_name.isidentifier() or not project_name.islower():
    raise ValueError(
        "\n"
        "Project name must be a valid project name, meaning that it must be a valid Python name and also be lowercase."
        " This means that it must not contain spaces or special characters, and must not start with a number."
        " In general it is best to use only lowercase letters and underscores."
        "\n",
    )
if iskeyword(project_name):
    raise ValueError(
        "Project name must not be a built-in keyword, as it will cause syntax errors.",
    )

# Python version validation
min_version = "3.10"
max_version = "3.13"
if not (ge(python_version, min_version) and le(python_version, max_version)):
    raise ValueError(
        f"Python version must be between {min_version} and {max_version}."
        " These are the versions that still receive support."
    )

# Validate wandb and examples choices
if use_wandb not in ["yes", "no"]:
    raise ValueError("use_wandb must be either 'yes' or 'no'")

if include_examples not in ["yes", "no"]:
    raise ValueError("include_examples must be either 'yes' or 'no'")