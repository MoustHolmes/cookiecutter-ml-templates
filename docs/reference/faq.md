# Frequently Asked Questions

## General

### What is Copier?

Copier is a command-line tool that generates projects from templates and can update existing projects when the template changes. Run `copier copy <template> <destination>` to generate, and `copier update` to pull in template improvements later.

### Which template should I use?

- **Barebone:** Starting from scratch, maximum flexibility
- **Flow Matching:** Generative models, flow-based approaches
- **Classification:** Image classification tasks
- **RL:** Reinforcement learning research and baselines
- **Image Logger extension:** Add W&B image logging to an existing project

### Do I need Copier installed in my generated project?

No. Copier is only needed to generate or update the project. The generated project has no runtime dependency on Copier.

### Why does Copier need `--trust`?

Templates can define `_tasks:` — shell commands that run after generation (e.g., `gh repo create`). The `--trust` flag confirms you trust the template source to run those commands. All templates in this repo use `--trust` only for the optional GitHub repo creation task.

## Workflow

### How do I create a project?

Create the directory first, then copy the template into it:

```bash
mkdir my_project && cd my_project
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/barebone . --trust
```

### How do I update a project when the template changes?

From inside your project directory:

```bash
copier update --trust
```

Copier re-prompts using your saved `.copier-answers.yml` as defaults, then merges changes.

### What is `.copier-answers.yml`?

Copier saves your answers to `.copier-answers.yml` after generation. Commit this file — it is what `copier update` uses to know which template you used and what answers you gave.

### Can I re-run copier to change an option I chose at generation time?

Yes. Use `copier update --trust` and override the answer when prompted, or edit `.copier-answers.yml` first and then run `copier update --trust`.

## Configuration

### How do I change Hydra configs?

Edit files in `configs/`. See the [Hydra guide](../guides/hydra-config.md).

### Can I add my own configs?

Yes. Add YAML files to the appropriate subdirectory in `configs/`.

### How do I override configs from the command line?

```bash
python src/my_project/train.py model.learning_rate=0.001 trainer.max_epochs=50
```

## Dependencies

### pip, uv, or pixi?

- **pip:** Traditional, widest compatibility. Generates `requirements.txt`.
- **uv:** Much faster than pip, modern resolver. Uses `pyproject.toml` inline deps.
- **pixi:** Conda-compatible, manages Python itself. Uses `pixi.toml`.

All three produce an equivalent development environment. Choose based on your team's tooling.

### How do I add new dependencies?

=== "pip"
    Add to `requirements.txt`, then:
    ```bash
    pip install -r requirements.txt
    ```

=== "uv"
    ```bash
    uv add <package>
    ```

=== "pixi"
    ```bash
    pixi add <package>
    ```

## Testing

### How do I run tests?

```bash
pytest tests/
```

### Tests are failing — what do I do?

1. Read the error message carefully
2. Ensure all dependencies are installed (`pip install -e ".[dev]"`)
3. Verify you are running from the project root
4. Check that your Hydra configs are correct

### What is the difference between fast and slow tests?

- **Fast** (`pytest tests/ -m "not slow"`): Structural validation, run in seconds
- **Slow** (`pytest tests/ -m slow`): Integration tests that install deps and run the generated project's full test suite

## Development

### How do I contribute?

See the [Contributing Guide](../development/contributing.md).

### Can I create my own template?

Yes. See [Creating Templates](../development/creating-templates.md).

### How do I report bugs?

Open an issue on [GitHub](https://github.com/MoustHolmes/cookiecutter-ml-templates/issues).

## More Questions?

Open an issue on GitHub.
