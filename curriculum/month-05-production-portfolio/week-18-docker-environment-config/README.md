<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 18 — Docker and Environment Config:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 17 Reflection](../week-17-rag-assistant/reflection.md) · ➡️ [Notes →](notes.md)

**📐 Relevant Decisions:** [ADR-0001: Modular Monolith](../../../docs/decisions/0001-modular-monolith.md)

---
<!-- NAV_END -->
## 1. Week title

# Week 18 - Docker and Environment Configuration
**Chapter title:** Shipping the whole system.
This is the first week Docker is allowed because ResearchOps already has local CLI, API, worker, storage, and RAG behavior worth packaging.

## 2. Story of the week

ResearchOps now needs to run the same way on another machine.
The story is simple: a learner should clone the repo, provide safe environment values, run Compose, and reach the API health endpoint.
The container is not the product; it is the reproducible runtime for the product already built.

## 3. What you already know

You can install and run the CLI.
You can explain SQLite persistence.
You can describe the API boundary.
You can describe the worker boundary.
You know secrets do not belong in source control.

## 4. What this week adds

A Dockerfile for the application image.
A Compose file with API and worker services.
A documented `.env.example`.
A settings module under `src/researchops/config/`.
A reproducible data path for SQLite through a mounted volume.

## 5. Why this week matters

Without this week, ResearchOps depends on hidden host-machine setup.
With this week, runtime assumptions become visible and repeatable.
This is essential for research systems because reproducibility is part of trust.

## 6. Learning objectives

Write a Dockerfile using `FROM`, `WORKDIR`, `COPY`, `RUN`, and `CMD`.
Explain Docker layer caching using a source-code edit example.
Run API and worker as separate Compose services.
Read configuration from environment variables through one settings module.
Keep `.env` private while committing `.env.example`.
Persist SQLite data outside disposable containers.

## 7. Project milestone

`docker compose up` starts the API and worker. Older Docker Compose installations may use `docker-compose up`; Windows learners should start Docker Desktop first.
`curl http://localhost:8000/health` returns a healthy response.
The same image can run different commands for CLI, API, and worker paths.

## 8. Files/modules touched

`Dockerfile` — application image recipe.
`docker-compose.yml` — local API and worker orchestration.
`.env.example` — safe configuration template.
`src/researchops/config/settings.py` — environment-driven settings.
`tests/unit/test_settings.py` — defaults and overrides.

## 9. Commands introduced

`docker compose build`
`docker compose up -d`
`docker compose logs api`
`docker compose logs worker`
`docker compose down`
`curl http://localhost:8000/health`

## 10. Tests involved

Settings unit tests for defaults.
Settings unit tests for environment overrides.
A manual container validation path from build to health check.
No new business logic tests are required unless behavior changes outside configuration.

## 11. Study plan

First, read notes through the mental model section.
Second, inspect the Dockerfile example and explain every line aloud.
Third, study the settings example and identify every environment variable.
Fourth, complete warm-up exercises before editing project files.
Fifth, run the validation commands only when your local Docker files are ready.

## 12. Estimated time breakdown

Reading notes: 90 minutes.
Dockerfile exercises: 60 minutes.
Settings exercises: 60 minutes.
Compose exercises: 75 minutes.
Debugging and validation: 60 minutes.
Reflection: 30 minutes.

## 13. How to know the learner is stuck

They say Docker is “like a VM” but cannot explain images and containers separately.
They put secrets into `Dockerfile` or commit `.env`.
They cannot explain why SQLite needs a volume.
They bind the API to localhost inside the container and cannot reach it from the host.
They scatter `os.environ` reads across CLI, API, and worker code.

## 14. Definition of done

Dockerfile builds the app image.
Compose starts API and worker services.
Health endpoint responds from the host.
Settings defaults and overrides are tested.
`.env.example` is safe and complete.
No real secrets are committed.
The learner can explain layer caching and runtime configuration.

## 15. Ruthless mentor checkpoint

If the app only works on your laptop, you are not done.
If deleting a container deletes the learner database, you are not done.
If a secret appears in image history or committed files, you are not done.
If the API and worker require different undocumented setup, you are not done.

## 16. What not to do this week

Do not introduce Docker before verifying the local app works.
Do not rewrite services to understand Docker.
Do not add Kubernetes, cloud deployment, or registry publishing.
Do not add new heavy dependencies.
Do not treat Week 19 documentation or Week 20 release work as completed.

## 17. Bridge to next week

After this week, ResearchOps has a reproducible local runtime.
That makes later polish and presentation work safer because setup instructions are no longer guesswork.
The next step can build on a stable containerized application instead of debugging hidden environment drift.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 17 Reflection](../week-17-rag-assistant/reflection.md) · ➡️ [Notes →](notes.md)

**📐 Relevant Decisions:** [ADR-0001: Modular Monolith](../../../docs/decisions/0001-modular-monolith.md)

**Week 18 — Docker and Environment Config:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
