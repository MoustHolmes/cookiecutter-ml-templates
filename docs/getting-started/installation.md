# Installation

## Requirements

Before installing Cookiecutter ML Templates, ensure you have:

- **Python 3.10 or higher**
- **pip** or **conda** package manager
- **Git** (for cloning repositories)

## Install Cookiecutter

Choose your preferred method:

=== "pipx (Recommended)"
    ```bash
    # Install pipx if you don't have it
    python -m pip install --user pipx
    python -m pipx ensurepath
    
    # Install cookiecutter
    pipx install cookiecutter
    ```
    
    !!! tip "Why pipx?"
        pipx installs packages in isolated environments, perfect for CLI tools!

=== "pip"
    ```bash
    pip install cookiecutter
    ```

=== "conda"
    ```bash
    conda install -c conda-forge cookiecutter
    ```

## Verify Installation

```bash
cookiecutter --version
```

You should see something like: `Cookiecutter 2.x.x`

## Next Steps

Ready to create your first project? Head to the [Quick Start Guide](quickstart.md)!
