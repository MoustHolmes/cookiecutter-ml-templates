"""Post-generation script for barebone template."""

import os
import shutil
import subprocess
import sys
from keyword import iskeyword
from operator import ge, le
from pathlib import Path

project_name = "{{cookiecutter.project_name}}"
python_version = "{{cookiecutter.python_version}}"
project_structure = "{{cookiecutter.project_structure}}"
deps_manager = "{{cookiecutter.deps_manager}}"
create_github_repo = "{{cookiecutter.create_github_repo}}"
github_username = "{{cookiecutter.github_username}}"
repo_name = "{{cookiecutter.repo_name}}"
description = "{{cookiecutter.description}}"

# Project name validation
if not project_name.isidentifier() or not project_name.islower():
    msg = (
        "\nProject name must be a valid Python name and lowercase. "
        "It must not contain spaces or special characters, and must not start with a number. "
        "In general, use only lowercase letters and underscores.\n"
        "See: https://peps.python.org/pep-0008/#package-and-module-names\n"
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
        "These are the versions that still receive support. "
        "See: https://devguide.python.org/versions/"
    )
    raise ValueError(msg)

# Handle dependency manager option
if deps_manager == "uv":
    # Remove pip-specific files
    for file in ["requirements.txt", "requirements_dev.txt", "pyproject_pip.toml", "tasks_pip.py"]:
        file_path = Path(file)
        if file_path.exists():
            os.remove(file_path)

    # Rename uv files to default names
    if Path("pyproject_uv.toml").exists():
        os.rename("pyproject_uv.toml", "pyproject.toml")
    if Path("tasks_uv.py").exists():
        os.rename("tasks_uv.py", "tasks.py")

elif deps_manager == "pip":
    # Remove uv-specific files
    for file in ["pyproject_uv.toml", "tasks_uv.py"]:
        file_path = Path(file)
        if file_path.exists():
            os.remove(file_path)

    # Rename pip files to default names
    if Path("pyproject_pip.toml").exists():
        os.rename("pyproject_pip.toml", "pyproject.toml")
    if Path("tasks_pip.py").exists():
        os.rename("tasks_pip.py", "tasks.py")

# Handle project structure option (after deps_manager to work with the final tasks.py)
if project_structure == "minimal":
    # Remove docs directory
    docs_dir = Path("docs")
    if docs_dir.exists():
        shutil.rmtree(docs_dir)

    # Remove documentation-related tasks from tasks.py
    tasks_file = Path("tasks.py")
    if tasks_file.exists():
        with tasks_file.open("r") as f:
            lines = f.readlines()

        # Filter out build_docs and serve_docs tasks
        filtered_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]

            # Check if this is the start of a docs-related task
            if line.strip().startswith("@task"):
                # Look ahead to see if next line is build_docs or serve_docs
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if "def build_docs" in next_line or "def serve_docs" in next_line:
                        # Skip this task (skip lines until we hit the next @task or end of file)
                        i += 1
                        while i < len(lines) and not lines[i].strip().startswith("@task"):
                            i += 1
                        # Skip one more empty line if present
                        if i < len(lines) and lines[i].strip() == "":
                            i += 1
                        continue

            filtered_lines.append(line)
            i += 1

        with tasks_file.open("w") as f:
            f.writelines(filtered_lines)


# GitHub repository creation
def create_github_repository():
    """Create a GitHub repository using GitHub CLI."""
    print("\n" + "=" * 80)
    print("Creating GitHub repository...")
    print("=" * 80)

    # Check if gh CLI is installed
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n❌ GitHub CLI (gh) is not installed or not in PATH.")
        print("\nTo install GitHub CLI:")
        print("  macOS:   brew install gh")
        print("  Linux:   See https://github.com/cli/cli/blob/trunk/docs/install_linux.md")
        print("  Windows: See https://github.com/cli/cli#installation")
        print("\nAfter installation, run: gh auth login")
        return False

    # Check if user is authenticated
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print("\n❌ Not authenticated with GitHub CLI.")
            print("\nPlease run: gh auth login")
            return False
    except Exception as e:
        print(f"\n❌ Error checking GitHub authentication: {e}")
        return False

    # Initialize git repository if not already initialized
    if not Path(".git").exists():
        print("\n📦 Initializing git repository...")
        try:
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit from cookiecutter template"],
                check=True
            )
            print("✅ Git repository initialized")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error initializing git repository: {e}")
            return False

    # Create GitHub repository
    print(f"\n🚀 Creating repository: {github_username}/{repo_name}")
    try:
        cmd = [
            "gh", "repo", "create",
            f"{github_username}/{repo_name}",
            "--description", description,
            "--public",
            "--source", ".",
            "--push"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print(f"\n✅ GitHub repository created successfully!")
            print(f"🔗 Repository URL: https://github.com/{github_username}/{repo_name}")
            print("\n📤 Initial commit has been pushed to GitHub")
            return True
        else:
            print(f"\n❌ Error creating repository: {result.stderr}")
            if "already exists" in result.stderr.lower():
                print(f"\n💡 Repository {github_username}/{repo_name} already exists.")
                print("   You can push to it manually with: git push")
            return False
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


if create_github_repo == "yes":
    try:
        create_github_repository()
    except Exception as e:
        print(f"\n⚠️  Warning: Could not create GitHub repository: {e}")
        print("You can create it manually later with: gh repo create")

print("\n" + "=" * 80)
print("✅ Project created successfully!")
print("=" * 80)
print(f"\n📁 Location: {Path.cwd()}")
print("\n🔧 Next steps:")
print("1. cd", repo_name)
if deps_manager == "pip":
    print("2. pip install -r requirements.txt")
else:
    print("2. uv pip install -r requirements.txt")
print("3. pip install -e .")
print("4. python src/" + repo_name + "/train.py  # Run training")
print("\n📖 Documentation: See README.md for more details")
print("=" * 80 + "\n")
