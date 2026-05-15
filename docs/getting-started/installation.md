# Installation

## Requirements

- **Python 3.10 or higher**
- **Git**

## Install Copier

=== "pip"
    ```bash
    pip install copier
    ```

=== "pipx (isolated)"
    ```bash
    # Install pipx if you don't have it
    python -m pip install --user pipx
    python -m pipx ensurepath

    # Install copier
    pipx install copier
    ```

    !!! tip "Why pipx?"
        pipx installs CLI tools in isolated environments, keeping your global Python clean.

=== "uv"
    ```bash
    uv tool install copier
    ```

## Verify Installation

```bash
copier --version
```

## Next Steps

Ready to create your first project? Head to the [Quick Start Guide](quickstart.md).
