# Creating New Templates

How to build a new Copier template and add it to this repo.

## Template Structure

A Copier template directory contains:

```
templates/<category>/<name>/
├── copier.yml          # Questions, validation, exclusion rules
└── <source files>      # Jinja2-templated project files (flat, no outer subdirectory)
```

Unlike Cookiecutter, there is no wrapping `{{project_name}}/` directory. Copier copies files from the template root directly into the destination directory.

## Quick Tips

### 1. Choose a donor template

Pick the most structurally similar existing template:

| New template type | Best donor |
|---|---|
| Supervised learning | `templates/barebone` |
| Classification/regression | `templates/core/classification` |
| Generative model | `templates/generative/flow_matching` |
| RL agent | `templates/rl` |

### 2. Copy donor to `test_temp/`

```bash
cp -r templates/<category>/<donor> test_temp/<new_template>
```

### 3. Edit the three key things

**`copier.yml`** — define questions, validation, and exclusion rules:

```yaml
---
!include ../../_shared/questions/author.yml
---
!include ../../_shared/questions/deps_manager.yml
---
!include ../../_shared/questions/licensing.yml
---

my_custom_option:
    type: str
    help: Description shown to the user
    default: default_value
    choices: [option_a, option_b]

_answers_file: .copier-answers.yml

_exclude:
    - "copier.yml"
    - "{% if deps_manager != 'pip' %}requirements.txt{% endif %}"
    - "{% if deps_manager != 'pixi' %}pixi.toml{% endif %}"
    - "{% if deps_manager == 'pixi' %}tasks.py{% endif %}"
    - "{% if open_source_license == 'No license file' %}LICENSE{% endif %}"
```

Validation is done with `validator:` on the question, not in a hook script:

```yaml
project_name:
    type: str
    help: Python package name (lowercase, underscores only)
    validator: >-
        {% if not project_name.isidentifier() or project_name != project_name.lower() %}
        project_name must be a valid Python identifier and fully lowercase.
        {% endif %}
```

**Template source files** — use Jinja2 variables directly:

```python
# src/{{repo_name}}/__init__.py
"""{{description}}"""
```

**No `hooks/` directory** — post-generation logic that used to live in `hooks/post_gen_project.py` is handled by:
- `validator:` in `copier.yml` for input validation
- `_exclude:` in `copier.yml` for conditional file inclusion
- `_tasks:` in `copier.yml` for post-generation commands (e.g., `gh repo create`)

### 4. Test generation

```bash
mkdir test_temp/generated/my_test && cd test_temp/generated/my_test
copier copy ../../test_temp/<new_template> . --trust --defaults
```

Or using the Python API (more control):

```python
import copier

copier.run_copy(
    src_path="test_temp/<new_template>",
    dst_path="test_temp/generated/my_test",
    data={"project_name": "my_test", "deps_manager": "pip"},
    defaults=True,
    overwrite=True,
    trust=True,
)
```

### 5. Validate before transfer

```bash
cd test_temp/generated/my_test
pip install -e ".[dev]"
pytest tests/
```

Fix issues in the template, then regenerate and retest.

### 6. Transfer to `templates/`

```bash
cp -r test_temp/<new_template> templates/<category>/<new_template>
```

### 7. Add tests

Add to `tests/test_create_project.py`:

```python
def test_<new_template>_structure(temp_dir: Path) -> None:
    """Assert expected files exist after generation."""
    import copier

    template_dir = (Path(__file__).parent / ".." / "templates" / "<category>" / "<new_template>").resolve()
    copier.run_copy(
        src_path=str(template_dir),
        dst_path=str(temp_dir),
        data={"project_name": "test_proj", "python_version": "3.12"},
        defaults=True,
        overwrite=True,
        trust=True,
    )
    generated = temp_dir
    assert (generated / "src" / "test_proj").exists()
    assert (generated / "tests").exists()
    assert (generated / "configs").exists()
    assert (generated / ".copier-answers.yml").exists()
```

### 8. Cleanup

```bash
rm -rf test_temp/<new_template>
rm -rf test_temp/generated/
```

## Extensions

An extension is a template applied to an already-generated project. It reads the project's `.copier-answers.yml` via `_external_data` to avoid re-asking known questions:

```yaml
# templates/extensions/my_extension/copier.yml
_answers_file: .copier-answers.my_extension.yml

_external_data:
    base: .copier-answers.yml

project_name:
    type: str
    default: "{{ _external_data.base.project_name }}"
    when: false

# Extension-specific questions
my_question:
    type: int
    help: Some extension-specific setting
    default: 10
```

Apply an extension from inside the project directory:

```bash
copier copy path/to/extension . --trust
```
