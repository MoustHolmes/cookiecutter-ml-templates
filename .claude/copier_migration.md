Plan: Migrate cookiecutter-ml-templates to Copier with Composable Extensions
Goals

Replace Cookiecutter with Copier to enable downstream projects to receive template updates via copier update.
Restructure the monorepo so shared configuration lives in one place and each template stays DRY.
Introduce an "extensions" concept: small, orthogonal Copier templates applied as a second pass on top of a base template, each independently updatable.
Design base templates around natural seams (Hydra config groups, file-per-component layout) so extensions are mostly "drop files + declare deps."

Non-Goals

Solving every possible ML workflow. Templates are starting points and a library for inspiration, not exhaustive solutions.
Supporting extension-to-extension interactions. Extensions are orthogonal by design; if two extensions need to interact, that becomes a third dedicated extension or a full-fledged composed template.
Backward compatibility with existing Cookiecutter-generated projects. Document a one-time migration path; do not preserve cookiecutter.json entry points indefinitely.
Multi-repo split. The monorepo stays; multi-repo is explicitly rejected for discoverability and atomic-change reasons.

Architectural Decisions
Monorepo, not multi-repo. One author, related templates, atomic ecosystem migrations (e.g., ruff → next-tool) are easier in one repo. Copier's update mechanism works fine with subdirectories in a single repo.
Composition over inheritance. Extensions are not parent templates. Copier's _extends is for linear IS-A relationships; extensions are orthogonal mixins applied as a second copier copy pass. Each extension maintains its own .copier-answers.<name>.yml and can be updated independently of the base and of other extensions.
Shared partials, not template inheritance. A _shared/ directory holds Jinja partials (for files like pyproject.toml base, ruff config, CI workflows) and small Python helper scripts (deps patching). Base templates {% include %} partials; extensions call shared scripts via _tasks.
Base templates must be designed for extension. The single biggest design choice: Hydra configs use group composition at the experiment level, never by editing a monolithic default.yaml. Callbacks, loggers, data modules, and models each live in their own files. Extensions then drop files without patching existing ones.
Extension scope rule. If removing a feature leaves the project broken, it belongs in the base template. If removing it leaves the project working with one less capability, it's an extension. Hydra usage and deps manager choice stay in the base; image logging, Gradio app, alternative data loaders become extensions.
Target Repository Structure
ml-templates/                                    # renamed from cookiecutter-ml-templates
├── copier.yml                                   # repo-level metadata only (not a template)
├── _shared/
│   ├── partials/                                # Jinja partials included by base templates
│   │   ├── pyproject_base.toml.jinja
│   │   ├── ruff.toml.jinja
│   │   ├── precommit.yaml.jinja
│   │   └── ci_workflow.yml.jinja
│   ├── macros/                                  # Jinja macros for common patterns
│   │   ├── hydra.jinja
│   │   └── pyproject.jinja
│   ├── questions/                               # shared question YAML, included by templates
│   │   ├── author.yml
│   │   ├── deps_manager.yml
│   │   └── licensing.yml
│   └── scripts/                                 # shared Python helpers for _tasks
│       ├── add_deps.py                          # deps-manager-aware dependency adder
│       ├── add_task.py                          # add entry to tasks.py / pixi tasks
│       └── _utils.py
├── templates/
│   ├── barebone/                                # minimal Python project, no ML
│   ├── lightning_hydra/                         # Lightning + Hydra skeleton, no domain
│   ├── mnist/                                   # MNIST on lightning_hydra base
│   ├── classification/                          # image classification (beta -> stable)
│   ├── rl/                                      # SAC/TD3/PPO/RPO/DQN
│   ├── flow_matching/
│   └── extensions/
│       ├── image_logger/
│       ├── wandb_artifacts/
│       ├── gradio_app/
│       ├── hf_hub/
│       ├── ffcv/
│       ├── litdata/
│       └── mosaic_streaming/
├── meta/                                        # convenience wrapper (Phase 5)
│   └── copier.yml
├── tests/
│   ├── test_base_generation.py
│   ├── test_extension_application.py
│   └── test_update_lifecycle.py
├── docs/                                        # MkDocs Material
│   ├── index.md
│   ├── getting-started.md
│   ├── templates/
│   ├── extensions/
│   ├── contributing-extension.md
│   └── migration-from-cookiecutter.md
├── .github/workflows/
│   ├── ci.yml
│   └── docs.yml
└── README.md
The Extension Contract
Every extension must obey this contract; the contract is what makes extensions composable.
An extension may:

Add new files to the project.
Declare new dependencies via the shared add_deps.py script.
Add new tasks via the shared add_task.py script.
Read the base template's .copier-answers.yml via _external_data to learn package_name, deps_manager, logger, etc.
Declare base-template compatibility via _validate_base checks.
Ask its own questions in its own copier.yml.

An extension must NOT:

Overwrite files created by the base template.
Modify files created by another extension.
Depend on the presence of another extension.
Edit pyproject.toml, tasks.py, or pixi.toml directly — always go through the shared scripts so all three deps managers stay supported.

The base template must provide these seams so the contract is achievable:

Hydra config groups composed at the experiment level, not via monolithic defaults files.
One file per callback, logger, data module, model — never a registry list that needs patching.
pyproject.toml deps in a format add_deps.py can parse and patch idempotently.
A .copier-answers.yml rich enough that extensions can introspect the project (package name, deps manager, logger choice, Lightning vs. raw PyTorch, etc.).

Migration Phases
Phase 0: Preparation

Create a copier-migration branch.
Audit current cookiecutter templates for shared content; list every file that's duplicated across templates/*/ (pyproject.toml, ruff config, pre-commit, CI workflows, tasks.py).
Inventory current MNIST variants and any "almost a duplicate template" cases. Map each to either a base-template question or a future extension.
Decide answers-file naming convention: .copier-answers.yml for base, .copier-answers.<extension_name>.yml for extensions.

Phase 1: Build Shared Infrastructure
Build _shared/ before porting any template.

_shared/partials/: extract the duplicated pieces of the current templates into Jinja partials. Start with pyproject_base.toml.jinja, ruff.toml.jinja, precommit.yaml.jinja, ci_workflow.yml.jinja.
_shared/questions/: shared question definitions (author.yml, deps_manager.yml, licensing.yml) so every template gets the same prompts in the same order with the same defaults.
_shared/scripts/add_deps.py: deps-manager-aware. Reads .copier-answers.yml to learn the deps manager, then dispatches:

pixi: invokes pixi add or edits pixi.toml.
uv: invokes uv add or edits the inline deps in pyproject.toml.
pip: edits requirements.txt and pyproject.toml dependencies array.
Idempotent: if the dep is already present (any version spec), no-op.


_shared/scripts/add_task.py: same shape but for tasks.py (invoke) and pixi tasks.
Unit-test the scripts in isolation before any template depends on them.

Phase 2: Port One Base Template (MNIST) as Proof of Concept
MNIST is small, real, and the extension-friendliness will be obvious.

Create templates/mnist/copier.yml with shared questions included via Copier's !include mechanism plus MNIST-specific questions.
Render the project tree using _shared/partials/ for shared files.
Redesign Hydra config layout to use group composition at the experiment level. No monolithic configs/callbacks/default.yaml that lists every callback; instead, each callback gets its own file under configs/callbacks/, and configs/experiment/<name>.yaml composes them.
Ensure .copier-answers.yml captures everything an extension might need (package_name, deps_manager, logger, uses_lightning, uses_hydra).
Manual end-to-end test: generate a project, run training, verify copier update works after making a trivial change to the template.

Phase 3: Build One Extension (image_logger) End-to-End
Don't generalize until one extension fully works.

Create templates/extensions/image_logger/.
copier.yml declares: _external_data reading the base's answers file; _validate_base checks (requires Lightning, requires W&B logger); extension-specific questions (log frequency, num samples).
Template tree: just the callback Python file, the Hydra config for the callback, and one example experiment showing how to use it. No patching of existing files.
_tasks entry: one call to _shared/scripts/add_deps.py to add wandb.
Full lifecycle test:

Generate MNIST project.
Apply image_logger extension via copier copy -a .copier-answers.image_logger.yml ....
Modify the user's project in some realistic way.
Make a change to the image_logger template upstream.
Run copier update -a .copier-answers.image_logger.yml.
Confirm the update applies cleanly and doesn't touch base-template files.
Make a change to the MNIST base template.
Run copier update -a .copier-answers.yml.
Confirm the base update doesn't break the extension's additions.


This phase is the riskiest. If copier update semantics don't behave the way the docs suggest in this two-template-on-one-project setup, the entire architecture needs adjustment. Validate before proceeding.

Phase 4: Build Second Extension to Confirm Composition
Pick an extension that touches different files than image_logger. ffcv (touches data layer) or wandb_artifacts (touches the trainer or a separate logging module) are good candidates.

Build it following the same pattern as image_logger.
Test: generate MNIST, apply both extensions, confirm no conflicts.
Test: generate MNIST, apply only the second extension, confirm it works without image_logger.
This confirms the orthogonality property in practice.

Phase 5: Port Remaining Base Templates
In order: barebone → lightning_hydra → classification → rl → flow_matching.

For each, follow the Phase 2 recipe: use shared partials, design Hydra config for extension-friendliness, populate .copier-answers.yml with enough metadata.
After each port, verify at least one existing extension applies cleanly to the new base (where compatible).

Phase 6: Build Remaining Extensions
For each of: wandb_artifacts, gradio_app, hf_hub, ffcv (if not done in Phase 4), litdata, mosaic_streaming.

One extension per PR or commit, so each can be reviewed in isolation.
Each extension should ship with: copier.yml, the rendered files, a README.md documenting what it does and which bases it supports, and at least one test that applies it to a compatible base.

Phase 7: Meta-Template (Optional Convenience Wrapper)
Once ~4 extensions exist, build meta/copier.yml.

Asks: which base? which extensions? then base questions, then per-extension questions.
Uses Copier _tasks to drive copier copy for the base and each selected extension.
Document clearly that updates should still be done per-template, not via the meta. The meta is generation-time convenience only.

Phase 8: Documentation and Migration Guide

Update README to lead with Copier usage.
Write docs/migration-from-cookiecutter.md for users of the old Cookiecutter version. Approach: existing projects either (a) accept they won't get updates, or (b) manually create a .copier-answers.yml matching the closest current template and run copier update to see the diff. Set expectations honestly: this is a manual process, not automated.
Write docs/contributing-extension.md capturing the Extension Contract above, with the image_logger as a worked example.
Per-template docs under docs/templates/.
Per-extension docs under docs/extensions/ including compatibility matrix (which extensions work with which bases).

Phase 9: Deprecate Cookiecutter Path

Remove cookiecutter.json files from each template.
Remove hooks/ directory.
Update CI to test Copier generation, not Cookiecutter.
Keep the templates/ directory layout so existing bookmarks/links still resolve to the right place.
Tag a v1.0-copier release. Tag the last Cookiecutter state as v0.x-cookiecutter-final for archival reference.

Testing Strategy
Tests live in tests/ and run in CI.

test_base_generation.py: For each base template, generate a project with default answers and assert the resulting structure, that it imports, and that a smoke-test training command runs (small epoch count, dummy data).
test_extension_application.py: For each (base, extension) compatible pair, generate the base, apply the extension, assert no files from the base were modified, assert deps were added correctly across all three deps managers.
test_update_lifecycle.py: For each base template and at least one extension per base, simulate the full lifecycle: generate → modify user files → upstream change → copier update → assert clean merge.
Matrix CI: Run tests across deps_manager ∈ {pixi, uv, pip} because the shared scripts behave differently for each.

Risks and Mitigations
Risk: Copier _tasks aren't expressive enough for deps patching across three deps managers. Mitigation: Phase 1 builds and unit-tests add_deps.py in isolation before any template depends on it. If it's not feasible, fall back to documenting "after generation, run pixi add wandb" in the extension README — less clean but acceptable.
Risk: copier update doesn't compose cleanly when a project has multiple answers files. Mitigation: Phase 3 is explicitly a go/no-go validation gate. If the update story doesn't hold up, reconsider whether extensions should instead be flags on a meta-template that regenerates rather than updates.
Risk: Designing the Hydra config layout for extension-friendliness changes the user experience of the base template in ways existing users don't like. Mitigation: the new layout is genuinely cleaner (group composition at the experiment level is closer to how Hydra is meant to be used). Document the rationale. Existing users on old Cookiecutter-generated projects are unaffected.
Risk: Scope creep — wanting to make extensions interact. Mitigation: enforce the orthogonality rule at PR review time. If two extensions need to interact, the answer is a third dedicated extension or a full-fledged composed template, never a special case in either of the original two.
Risk: The meta-template (Phase 7) becomes a maintenance burden. Mitigation: build it only after Phase 6 proves the underlying primitives work. If it's painful, drop it — users can run two copier copy commands.
Open Questions to Resolve During Implementation

Exact format of the .copier-answers.yml metadata that extensions read. Suggest a _extension_api_version field so the contract can evolve without silently breaking extensions.
Whether add_deps.py should run as a Copier _tasks shell-out or be imported as a Jinja extension. Shell-out is simpler; Jinja extension is faster and avoids subprocess overhead. Start with shell-out.
How to handle dev-deps vs. runtime deps in add_deps.py. Probably an --dev flag.
Whether to publish the templates as a Copier-discoverable index somewhere, or rely on the GitHub URL pattern. GitHub URL is fine for now.
Versioning policy for extensions. Probably tag the whole repo, not per-template — simpler, and atomic-change-friendly.

Definition of Done
The migration is complete when:

All current templates work via Copier, generating projects that pass smoke tests across all three deps managers.
At least four extensions exist and apply cleanly to their compatible bases.
The full update lifecycle (base updates and extension updates, independently) is tested in CI.
Docs cover getting started, each template, each extension, the extension contract, and the migration path from Cookiecutter.
The Cookiecutter path is removed; the repo is Copier-only.
A v1.0-copier release is tagged.

**USE THE copier-docs SKILL OFTEN**
