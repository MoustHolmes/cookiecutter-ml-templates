"""Post-generation hook for cookiecutter template."""

import os
import subprocess
import sys

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    """Remove a file."""
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def main():
    """Execute the post-generation tasks."""
    print("✅ Project created successfully!")
    print(f"📁 Location: {PROJECT_DIRECTORY}")
    print("\n🔧 Next steps:")
    print("1. cd {{cookiecutter.repo_name}}")
    print("2. pip install -r requirements.txt")
    print("3. pip install -e .")
    print("4. python src/{{cookiecutter.repo_name}}/train.py experiment=moons  # Run training")
    print("\n📖 Documentation: See README.md for more details")


if __name__ == "__main__":
    main()
