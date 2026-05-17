# Image Logger Extension

Add Weights & Biases image logging to an existing project generated from any ML template.

The Image Logger extension lives at `templates/extensions/image_logger`. It is not a standalone template — it is applied on top of a project you have already generated.

## What It Does

- Adds `wandb>=0.16.0` to your project's dependencies (pip, uv, or pixi — detected automatically from `.copier-answers.yml`)
- Scaffolds an image logging callback wired into your training loop
- Saves its own answers to `.copier-answers.image_logger.yml` so it can be updated independently

## Usage

From inside your project directory (a `.copier-answers.yml` must exist):

```bash
cd my_project
copier copy gh:MoustHolmes/cookiecutter-ml-templates/templates/extensions/image_logger . --trust
```

You will be asked two questions:

| Question | Default | Description |
|----------|---------|-------------|
| `log_every_n_batches` | 100 | Log images every N training batches |
| `num_samples` | 8 | Number of sample images to log per step |

`project_name`, `repo_name`, and `deps_manager` are read silently from `.copier-answers.yml` — you will not be prompted for them.

## Updating

```bash
copier update --answers-file .copier-answers.image_logger.yml --trust
```

Using `--answers-file` targets the extension's answer file so that a plain `copier update` on the base project is not affected.

## Requirements

- The project must have been generated with one of the ML templates (a `.copier-answers.yml` is required).
- W&B account for logging (free tier is sufficient for most use cases).

!!! note "Migrated from standalone template"
    This extension replaces the former `MNIST_wandb_image_logger` standalone template. The functionality is now composable — add it to any project instead of starting from a dedicated template.
