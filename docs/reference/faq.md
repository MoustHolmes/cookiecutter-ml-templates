# Frequently Asked Questions

## General

### What is Cookiecutter?

Cookiecutter is a command-line tool that creates projects from templates. It allows you to quickly scaffold new projects with a predefined structure.

### Which template should I use?

- **Barebone:** Starting from scratch, maximum flexibility
- **Flow Matching:** Generative models, flow-based approaches
- **MNIST W&B:** Quick experiments, learning
- **Classification:** Image classification tasks

### Do I need to install cookiecutter in my project?

No! Cookiecutter is only needed to generate the project. After generation, your project has no dependency on cookiecutter.

## Configuration

### How do I change Hydra configs?

Edit files in `configs/` directory. See the [Hydra guide](../guides/hydra-config.md).

### Can I add my own configs?

Yes! Add YAML files to the appropriate subdirectory in `configs/`.

### How do I override configs from command line?

```bash\npython src/my_project/train.py model.learning_rate=0.001 trainer.max_epochs=50\n```

## Dependencies

### pip or uv?

- **pip:** Traditional, widely compatible
- **uv:** Much faster, modern

Both work the same way after installation.

### How do I add new dependencies?

Add to `requirements.txt` or `pyproject.toml`, then reinstall:

```bash
pip install -r requirements.txt
pip install -e .
```

## Testing

### How do I run tests?

```bash
pytest tests/
```

### Tests are failing, what do I do?

1. Check error message carefully
2. Ensure all dependencies installed
3. Verify you're in project root
4. Check configs are correct

### What's the difference between fast and slow tests?

- **Fast:** Structural validation, run quickly
- **Slow:** Integration tests, run full workflows

## Development

### How do I contribute?

See [Contributing Guide](../development/contributing.md).

### Can I create my own template?

Yes! See [Creating Templates](../development/creating-templates.md).

### How do I report bugs?

Open an issue on [GitHub](https://github.com/MoustHolmes/cookiecutter-ml-templates/issues).

## More Questions?

Can't find your answer? Open an issue on GitHub!
