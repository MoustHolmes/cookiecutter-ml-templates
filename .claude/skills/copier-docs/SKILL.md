---
name: copier-docs
description: Provides authoritative Copier documentation by fetching from copier.readthedocs.io/en/stable instead of relying on training-data recall. Use when working with `copier.yml`, `copier copy`, `copier update`, `.copier-answers.yml`, `_tasks`, `_extends`, `_external_data`, Jinja template rendering, or the `!include` mechanism. Use when migrating from Cookiecutter to Copier, designing extensions, or testing the update lifecycle. Copier's config schema and update semantics differ significantly from Cookiecutter and from older Copier versions — always fetch rather than recalling.
---

# Copier documentation

Copier is a library and CLI for rendering project templates, with first-class
support for updating existing projects from an evolved template. It is not a
drop-in replacement for Cookiecutter: the config schema (`copier.yml`),
template suffix convention, answer-tracking file (`.copier-answers.yml`), and
update lifecycle are distinct concepts with no Cookiecutter equivalent.
**Fetch before answering anything beyond "what is copier".**

## Canonical sources

- Overview: https://copier.readthedocs.io/en/stable/
- Creating a template: https://copier.readthedocs.io/en/stable/creating/
- Configureing a template: https://copier.readthedocs.io/en/stable/configuring/
- Generating a project: https://copier.readthedocs.io/en/stable/generating/
- Updating a project: https://copier.readthedocs.io/en/stable/updating/
- Settings: https://copier.readthedocs.io/en/stable/settings/
- Reference: https://copier.readthedocs.io/en/stable/reference/api/
- FAQ: https://copier.readthedocs.io/en/stable/faq/
- Tasks (`_tasks`): https://copier.readthedocs.io/en/stable/configuring/#tasks
- External data (`_external_data`): https://copier.readthedocs.io/en/stable/configuring/#external-data
- Template inheritance (`_extends`): https://copier.readthedocs.io/en/stable/configuring/#extending-a-template
- Subdirectory mode (`_subdirectory`): https://copier.readthedocs.io/en/stable/configuring/#subdirectory


## How to use

1. For anything in `copier.yml` (a key, a special variable like `_tasks` or
   `_external_data`) — fetch the configuration reference first.
2. For `copier update` questions (merge strategy, conflict resolution, answers
   file) — fetch the updating page; the three-way-merge semantics aren't
   obvious.
3. For "does copier support X" — check the configuring page; the feature set
   has grown and some things only appeared in recent releases.
4. For multi-template / extension-on-project architectures — fetch both
   `_answers_file` and `_external_data`; this is the highest-hallucination
   area because it's advanced and thinly documented.

## Common traps

- **`.jinja` suffix required by default** — template files must end in
  `.jinja` (or the configured `_templates_suffix`) to be rendered; files
  without the suffix are copied verbatim, not Jinja-rendered.
- **`copier.yml` ≠ `cookiecutter.json`** — questions use a different schema:
  each key is a question name, with `type`, `default`, `help`, `choices`
  sub-keys. Boolean questions use `type: bool`, not string `"yes"`/`"no"`.
- **`_tasks` ≠ cookiecutter hooks** — tasks are shell commands run after
  rendering; there's no `pre_gen_project` equivalent. Pre-generation logic
  must be in Jinja (validators/conditions) or `_jinja_extensions`.
- **`.copier-answers.yml` is not optional for `copier update`** — the answers
  file is what links a generated project back to its template. Without it,
  `copier update` cannot work. The path is controlled by `_answers_file`.
- **`_extends` is linear IS-A, not mixin** — it inherits another template's
  questions and rendering but it's a single-parent chain; it's not the right
  mechanism for orthogonal extensions applied on top of a base template.
- **`_external_data` reads from external sources at render time** — useful for
  extensions reading the base's `.copier-answers.yml`; but the path is
  relative to the destination directory, not the template.
- **`!include`** — YAML `!include` lets you split questions across files, but
  Copier must be configured with `_include_dotfiles: true` if the included
  files start with `.`; standard include paths are relative to `copier.yml`.

## When to skip the fetch

Skip for: explaining at a high level what copier is, or why it differs from
Cookiecutter conceptually.

Fetch for: any `copier.yml` key, `copier copy`/`update` flags, the answers
file format, `_tasks` command structure, `_external_data` paths, `_extends`
semantics, Jinja rendering behavior, or the update lifecycle in detail.

## Checklist

```
[ ] Fetched the relevant docs page (not answered from memory)
[ ] copier.yml keys verified against the configuration reference
[ ] Template files use .jinja suffix where rendering is needed
[ ] _answers_file present and correct for copier update to work
[ ] _tasks vs hooks distinction respected (no pre-gen logic in tasks)
[ ] _extends vs mixin/extension pattern clearly distinguished
```
