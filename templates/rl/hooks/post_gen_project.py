"""Post-generation hook for rl cookiecutter template."""

import os
import subprocess
from pathlib import Path

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
create_github_repo = "{{cookiecutter.create_github_repo}}"
github_username = "{{cookiecutter.github_username}}"
repo_name = "{{cookiecutter.repo_name}}"
description = "{{cookiecutter.description}}"
deps_manager = "{{cookiecutter.deps_manager}}"
open_source_license = "{{cookiecutter.open_source_license}}"


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
            check=False,
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
                check=True,
            )
            print("✅ Git repository initialized")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error initializing git repository: {e}")
            return False

    # Create GitHub repository
    print(f"\n🚀 Creating repository: {github_username}/{repo_name}")
    try:
        cmd = [
            "gh",
            "repo",
            "create",
            f"{github_username}/{repo_name}",
            "--description",
            description,
            "--public",
            "--source",
            ".",
            "--push",
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            print("\n✅ GitHub repository created successfully!")
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


def main():
    """Execute the post-generation tasks."""
    # Handle license option
    if open_source_license == "No license file":
        if Path("LICENSE").exists():
            os.remove("LICENSE")

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

    if create_github_repo == "yes":
        try:
            create_github_repository()
        except Exception as e:
            print(f"\n⚠️  Warning: Could not create GitHub repository: {e}")
            print("You can create it manually later with: gh repo create")

    print("\n" + "=" * 80)
    print("✅ Project created successfully!")
    print("=" * 80)
    print(f"\n📁 Location: {PROJECT_DIRECTORY}")
    print("\n🔧 Next steps:")
    print(f"1. cd {repo_name}")
    if deps_manager == "pip":
        print("2. pip install -e .[dev]")
        print(f"3. python src/{repo_name}/train.py              # Train SAC on Pendulum")
        print(f"4. python src/{repo_name}/train.py agent=td3    # Train TD3 instead")
    else:
        print("2. uv venv")
        print("3. source .venv/bin/activate")
        print("4. uv pip install -e .[dev]")
        print(f"5. python src/{repo_name}/train.py              # Train SAC on Pendulum")
        print(f"6. python src/{repo_name}/train.py agent=td3    # Train TD3 instead")
    print("\n📖 Documentation: See README.md for more details")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
