---
name: ml-templates
description: Encodes the architecture and conventions of the cookiecutter-ml-templates repo. Covers the flat template structure, shared question infrastructure, extension contract, `.jinja` suffix rules, `_exclude` patterns, `add_deps.py` usage, and test API. Use when adding or editing a template, building an extension, writing template tests, touching `_shared/`, or asking "where does X live in this repo?". Use even for seemingly simple questions like "how do I add a new question to a template?" — the `!include` setup and `_external_data` pattern are non-obvious. Defer to `copier-docs` for Copier API details and to `*-docs` skills for library API questions.
---

# ml-templates: Copier template library conventions

**The hardest part is the extension contract and the flat template layout — both differ from the Cookiecutter mental model in ways that cause silent bugs.**

## Repo layout

```
_shared/
    questions/          # author.yml, deps_manager.yml, licensing.yml
    scripts/
        add_deps.py     # deps-manager-aware dep injector (pip/uv/pixi)
templates/
    barebone/           # canonical structure; mirror when unsure
    core/classification/
    generative/flow_matching/
    rl/
    extensions/
        image_logger/   # reference extension implementation
tests/
    test_base_generation.py     # structure + deps variants per template
    test_validation.py          # validator rejection tests
    test_extension_application.py
    test_add_deps.py
```

## Template anatomy

Templates are **flat** — all files render directly into `dst_path`. No outer `{{project_name}}/` wrapper.

Every template contains:
- `copier.yml` — questions via `!include`, `_exclude`, `_tasks`, `_jinja_extensions`
- `.copier-answers.yml.jinja` — always present; records answers for `copier update`
- `src/{{repo_name}}/` — Jinja-rendered directory name; holds the package
- Files ending in `.jinja` are rendered; files without are copied verbatim

Typical `copier.yml` structure:
```yaml
---
!include ../../_shared/questions/author.yml   # path depth varies by template location
---
!include ../../_shared/questions/deps_manager.yml
---
!include ../../_shared/questions/licensing.yml
---

# template-specific questions here

_answers_file: .copier-answers.yml
_jinja_extensions:
    - jinja2_time.TimeExtension

_exclude:
    - "copier.yml"
    - "{% if deps_manager != 'pip' %}requirements.txt{% endif %}"
    - "{% if deps_manager != 'pixi' %}pixi.toml{% endif %}"
    - "{% if deps_manager == 'pixi' %}tasks.py{% endif %}"
    - "{% if open_source_license == 'No license file' %}LICENSE{% endif %}"

_tasks:
    - command: >-
          gh repo create {{github_username}}/{{repo_name}} ...
      when: "{{create_github_repo}}"
```

**`_exclude` matches destination filename** (after `.jinja` stripped), not the source filename. `{% if ... %}pixi.toml{% endif %}` is the correct pattern, not `pixi.toml.jinja`.

**`repo_name` is a hidden `when: false` question** — derived from `project_name`, NOT stored in `.copier-answers.yml`. Templates must use `{{repo_name}}` in directory names and `_target_` paths.

## Shared infrastructure

All templates share questions via `!include`. `!include` paths are relative to `copier.yml` and use multi-document YAML (`---` separators):

```yaml
---
!include ../../_shared/questions/author.yml
---
!include ../../_shared/questions/deps_manager.yml
```

Path depth: `templates/barebone/` uses `../../_shared/`, `templates/core/classification/` uses `../../../_shared/`.

`_shared/scripts/add_deps.py` is called by extension `_tasks`. It reads `deps_manager` from `.copier-answers.yml`, then dispatches to the right file (requirements.txt / pyproject.toml / pixi.toml). It's idempotent — safe to call if the dep already exists.

## Extension architecture

Extensions live in `templates/extensions/`. Each extension:
- Has its own `copier.yml` with `_answers_file: .copier-answers.<name>.yml`
- Reads base answers via `_external_data: base: .copier-answers.yml`
- Derives `repo_name` from `_external_data.base.project_name` (since `repo_name` isn't stored)
- Calls `add_deps.py` in `_tasks` using `{{ _copier_conf.src_path }}/../../../_shared/scripts/add_deps.py`

**Extension contract: extensions may add files and inject deps. They must NOT overwrite base files or touch files owned by other extensions.**

`image_logger` is the reference implementation — read it before building a new extension.

## Testing pattern

```python
copier.run_copy(
    src_path=str(TEMPLATE_DIR),
    dst_path=str(dst),
    data={"project_name": "test_proj", "deps_manager": "uv", ...},
    defaults=True,
    overwrite=True,
    unsafe=True,   # required when template has _tasks
)
```

`dst_path` IS the project dir (not its parent — templates are flat). Each test file has a `_generate_*()` helper; follow the established pattern. Extension tests: generate base first, then `run_copy` the extension into the same `dst`.

## ML code conventions

**Model vs LightningModule:** models are pure `forward()` — no loss, no optimizer. LightningModules own all training logic. This split applies to every template.

**Hydra config layout:** config groups, not flat configs. `_target_` instantiation for models, datamodules, optimizers. Each callback gets its own file under `configs/callbacks/` — never a monolithic list — so extensions can drop a new callback config without patching anything.

**Callbacks:** one file each under `src/<pkg>/callbacks/`. Non-essential training functionality (logging, visualization) always goes in a callback, never inline in the module.

## Workflows

**Add a template:** copy `templates/barebone/` → update `copier.yml` (add template-specific questions, fix `!include` depth) → rename/add `.jinja` files → add `_generate_<name>()` helper in `test_base_generation.py` → add structure + deps variant + config-naming tests.

**Add an extension:** copy `templates/extensions/image_logger/` → update `copier.yml` (`_answers_file`, `_external_data`, questions, `_tasks` path) → add files → test in `test_extension_application.py` (base files unchanged, new files present, dep injected).

**Run tests:** `pytest tests/ -m "not slow" -q`

## Checklist

```
[ ] New template: copier.yml uses !include at correct depth for _shared/
[ ] New template: .copier-answers.yml.jinja present
[ ] New template: _exclude patterns match destination filenames (not source)
[ ] New/edited file: .jinja suffix added if file references {{vars}}
[ ] Extension: _answers_file is .copier-answers.<name>.yml (not .copier-answers.yml)
[ ] Extension: repo_name derived from _external_data.base.project_name
[ ] Extension: add_deps.py path uses _copier_conf.src_path with 3 levels up to repo root
[ ] Tests: dst_path is the project dir itself, not a parent
[ ] ML code: model is pure forward(), training logic is in LightningModule
[ ] Hydra: one file per callback/config component for extension-friendliness
```
