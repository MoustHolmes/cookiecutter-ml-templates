"""Post-generation script for classification template."""

from keyword import iskeyword
from operator import ge, le

project_name = "{{cookiecutter.project_name}}"
python_version = "{{cookiecutter.python_version}}"

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
