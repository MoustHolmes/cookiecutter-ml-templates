---
name: dtu-mlops-docs
description: Provides authoritative MLOps course material by fetching from skaftenicki.github.io/dtu_mlops instead of relying on training-data recall. Use when the user asks about any MLOps topic covered in the DTU MLOps course — development environments, version control, DVC, Docker, config files, CI/CD, cloud deployment, monitoring, distributed training — or when the user says "the mlops course", "session N", or names a specific module like "data drifting", "pre-commit", "CML", "distributed training". Fetch even for questions that feel basic; the course has specific exercise instructions and tool choices that differ from generic tutorials.
---

# DTU MLOps course documentation

The DTU MLOps course (by Nicki Skafte) covers the full ML lifecycle from dev environment
setup to scalable cloud deployment. **Fetch the relevant module page before answering
questions about tools, exercises, or course-specific recommendations** — the course has
opinionated tool choices and exercise structures that differ from generic documentation.

## Canonical sources

- Course home: https://skaftenicki.github.io/dtu_mlops/latest/

### S1 — Development Environment
- Command line: https://skaftenicki.github.io/dtu_mlops/s1_development_environment/command_line/
- Package manager: https://skaftenicki.github.io/dtu_mlops/s1_development_environment/package_manager/
- Editor: https://skaftenicki.github.io/dtu_mlops/s1_development_environment/editor/
- Deep learning software: https://skaftenicki.github.io/dtu_mlops/s1_development_environment/deep_learning_software/

### S2 — Organisation and Version Control
- Git: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/git/
- Code structure: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/code_structure/
- Good coding practice: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/good_coding_practice/
- DVC: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/dvc/
- CLI: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/cli/

### S3 — Reproducibility
- Docker: https://skaftenicki.github.io/dtu_mlops/s3_reproducibility/docker/
- Config files: https://skaftenicki.github.io/dtu_mlops/s3_reproducibility/config_files/

### S4 — Debugging, Profiling and Logging
- Debugging: https://skaftenicki.github.io/dtu_mlops/s4_debugging_and_logging/debugging/
- Profiling: https://skaftenicki.github.io/dtu_mlops/s4_debugging_and_logging/profiling/
- Logging: https://skaftenicki.github.io/dtu_mlops/s4_debugging_and_logging/logging/
- Boilerplate: https://skaftenicki.github.io/dtu_mlops/s4_debugging_and_logging/boilerplate/

### S5 — Continuous Integration
- Unit testing: https://skaftenicki.github.io/dtu_mlops/s5_continuous_integration/unittesting/
- GitHub Actions: https://skaftenicki.github.io/dtu_mlops/s5_continuous_integration/github_actions/
- Pre-commit: https://skaftenicki.github.io/dtu_mlops/s5_continuous_integration/pre_commit/
- CML: https://skaftenicki.github.io/dtu_mlops/s5_continuous_integration/cml/

### S6 — The Cloud
- Cloud setup: https://skaftenicki.github.io/dtu_mlops/s6_the_cloud/cloud_setup/
- Using the cloud: https://skaftenicki.github.io/dtu_mlops/s6_the_cloud/using_the_cloud/

### S7 — Deployment
- APIs: https://skaftenicki.github.io/dtu_mlops/s7_deployment/apis/
- Cloud deployment: https://skaftenicki.github.io/dtu_mlops/s7_deployment/cloud_deployment/
- Testing APIs: https://skaftenicki.github.io/dtu_mlops/s7_deployment/testing_apis/
- ML deployment: https://skaftenicki.github.io/dtu_mlops/s7_deployment/ml_deployment/
- Frontend: https://skaftenicki.github.io/dtu_mlops/s7_deployment/frontend/

### S8 — Monitoring
- Data drifting: https://skaftenicki.github.io/dtu_mlops/s8_monitoring/data_drifting/
- Monitoring: https://skaftenicki.github.io/dtu_mlops/s8_monitoring/monitoring/

### S9 — Scalable Applications
- Data loading: https://skaftenicki.github.io/dtu_mlops/s9_scalable_applications/data_loading/
- Distributed training: https://skaftenicki.github.io/dtu_mlops/s9_scalable_applications/distributed_training/
- Inference: https://skaftenicki.github.io/dtu_mlops/s9_scalable_applications/inference/

## How to use

1. Match the user's topic to the session + module above, fetch that page.
2. For exercises, fetch the module page and look for the "Exercises" section — each
   module ends with numbered exercises that define what "done" looks like.
3. For tool questions (Docker, DVC, pre-commit, etc.) fetch the module page first;
   the course may recommend a specific workflow that differs from the tool's own docs.
   Then defer to the tool's own skill (`copier-docs`, `wandb-docs`, etc.) for API details.
4. For "what does session N cover" — fetch the course home or the session's first module.

## Common traps

- **Generic tutorials vs course path** — the course picks specific tools and patterns
  (e.g. `invoke`/`typer` for CLI, Hydra for config, specific Docker base images). Don't
  substitute generic alternatives without checking what the course recommends.
- **Exercise numbering** — each module has its own exercise list starting at M1. "Exercise
  3" is ambiguous without the module; always confirm which module page you're reading.
- **Config files = Hydra** — S3 config files means Hydra specifically, not generic YAML.
  Defer to `hydra-docs` for Hydra API details.
- **Boilerplate = Lightning** — S4 boilerplate refers to PyTorch Lightning. Defer to
  `lightning-docs` for Lightning API details.

## When to skip the fetch

Skip for: generic Git basics, general Python packaging concepts, standard Docker commands
unrelated to the course exercises.

Fetch for: any exercise question, any "how does the course recommend X", any tool the
course introduces (DVC, CML, pre-commit, Evidently, Locust), anything in S6–S9 where
cloud and deployment specifics are highly course-dependent.

## Checklist

```
[ ] Matched the topic to the correct session + module URL
[ ] Fetched the module page (not answered from memory)
[ ] Checked the Exercises section for what the course specifically asks
[ ] Deferred to the relevant tool's docs skill for API-level details
```
