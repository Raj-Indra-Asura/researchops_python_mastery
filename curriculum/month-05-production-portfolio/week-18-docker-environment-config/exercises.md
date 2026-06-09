<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 18 — Docker and Environment Config:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->
# Exercises - Week 18 Docker and Environment Configuration

## How to use this workbook

- Work in order unless a mentor tells you otherwise.
- Write commands in your own terminal notes, but do not commit scratch files.
- For every exercise, identify the file changed, the command that proves it, and the failure you would expect if it were wrong.
- Do not use real secrets.
- Do not write examples under forbidden temporary locations; keep practice files in an ignored local practice folder if needed.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Warm-up exercises

- Define image, container, layer, volume, build context, and environment variable in one sentence each.
- Sketch a Dockerfile with only `FROM`, `WORKDIR`, `COPY`, `RUN`, and `CMD`.
- Explain why Docker arrives in Week 18 rather than Week 2.
- Write a safe `.env.example` with placeholders for database URL, log level, and data directory.
- List five files that belong in `.dockerignore` and explain each choice.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Code-reading exercises

- Read the planned Dockerfile and mark which lines run at build time and which define runtime behavior.
- Read `src/researchops/config/settings.py` and identify defaults, env names, and types.
- Read the compose file and name each service, command, port, and volume.
- Find where the API app is created and explain why Docker should not add business logic there.
- Find the worker command and explain why it should share settings with the API.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Implementation exercises

- Create or refine `src/researchops/config/settings.py` so one `AppSettings` object owns database URL, log level, and data directory.
- Add `.env.example` with safe placeholder values and comments.
- Write a Dockerfile that installs ResearchOps and exposes a safe default command.
- Write a compose file with `api` and `worker` services sharing the same data volume.
- Ensure the API command binds to `0.0.0.0` and port `8000`.
- Ensure the worker command uses the existing job runner path rather than inventing a new worker.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Testing exercises

- Test settings defaults with no environment variables.
- Test an environment override for database URL.
- Test log level override and confirm cached settings do not leak between tests.
- Test that `.env.example` contains no obvious real secret values.
- Manually validate that `curl http://localhost:8000/health` reaches the API after Compose starts.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Debugging exercises

- Break the API host by binding to `127.0.0.1`; observe the host curl failure; fix it.
- Remove the volume mount; explain where data would go; restore it.
- Misspell `RESEARCHOPS_DATABASE_URL`; prove the default is used; fix the variable name.
- Copy `.env` into the image intentionally in a throwaway branch; explain why that is unsafe; remove the risk with `.dockerignore`.
- Change source code and predict which Docker layers rebuild.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Refactoring exercises

- Replace scattered `os.environ` reads with imports from the config settings module.
- Move Docker-specific paths out of CLI command bodies and into settings defaults or env values.
- Ensure API and worker wiring both request settings in the same style.
- Keep services dependent on protocols rather than concrete Docker paths.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Written explanation exercises

- Explain image versus container using a ResearchOps example.
- Explain build-time versus runtime configuration.
- Explain why `.env.example` is committed and `.env` is not.
- Explain why the SQLite database needs a mounted volume.
- Explain how Compose lets API and worker share the same image but run different commands.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Stretch exercises

- Add a lightweight healthcheck to the API service if curl or an equivalent tool is available in the image.
- Add a non-root user to the Dockerfile and explain what file permissions must still work.
- Add a `docker compose logs` debugging checklist for API and worker.
- Make the data directory configurable without changing compose service commands.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Brutal exercises

- Start from a clean clone mindset and write the exact setup steps another learner needs.
- Simulate a broken environment variable and write the shortest diagnosis path.
- Explain every line of Dockerfile, compose, settings, and `.env.example` without saying “this is obvious.”
- Prove no secrets are present in committed config templates.
- Explain why Docker does not change the architecture dependency direction.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Mini project task

- Deliver a local containerized ResearchOps stack.
- The stack must have one application image, two runtime services, shared persistent data, documented environment variables, and a health check path.
- Write a short operator note in your own words describing how to build, start, inspect logs, and stop the stack.
- Do not add future portfolio or release material.

Practice detail 1: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 2: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 3: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 4: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.
Practice detail 5: apply this section to the real ResearchOps API, worker, settings module, Dockerfile, and SQLite data path; write the expected command and the expected failure if it is wrong.

## Completion checklist

- I can build the image.
- I can start API and worker with Compose.
- I can reach `/health` from the host.
- I can explain the database volume.
- I can explain every committed environment variable.
- I did not commit `.env` or any real secret.
- I updated settings tests with defaults and overrides.
- I can explain why Docker begins this week and not earlier.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 18 — Docker and Environment Config:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
