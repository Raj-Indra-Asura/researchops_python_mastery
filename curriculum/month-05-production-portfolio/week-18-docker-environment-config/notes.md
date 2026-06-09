<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 18 — Docker and Environment Config:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->
# Notes - Week 18 Docker and Environment Configuration

## Chapter overview

Week 18 is the first week where Docker is allowed in ResearchOps.
That timing is deliberate: Docker is not a substitute for a working application.
You already have a CLI, API, worker loop, job storage, search paths, and the RAG assistant from Week 17.
This week packages that already-working system into a reproducible runtime.
The chapter title from the syllabus is **Shipping the whole system**.
The milestone is concrete: `docker-compose up` starts the API and worker, and `curl http://localhost:8000/health` responds.
The main files are `Dockerfile`, `docker-compose.yml`, `.env.example`, and `src/researchops/config/settings.py`.
The skill is not memorising Docker commands; the skill is knowing which settings belong in code, which belong in the image, and which belong at runtime.
A ResearchOps container should run the same command on every machine without asking the learner to recreate hidden setup steps.
By the end of the chapter, you should be able to explain why the database lives in a mounted volume, why secrets never go into an image, and why the API and worker are separate compose services.

## What you already know from previous weeks

From Week 1, you know a Python project can expose a `researchops` command through `pyproject.toml`.
From Week 2, you know configuration and logging are separate concerns from business logic.
From Week 4, you know the CLI entry point is the user-facing shell command, not a random script.
From Week 5, you know SQLite stores data in a real file that must survive process restarts.
From Week 8, you know CPU-heavy work belongs in process workers, not inside the async event loop.
From Week 14, you know FastAPI owns HTTP request/response wiring and delegates real work to services.
From Week 16, you know the local job worker polls persistent jobs and performs work outside the API request.
From Week 17, you know the RAG assistant depends on the already-built retrieval pipeline and should not be rewritten here.
This week does not change those responsibilities; it wraps them in a reproducible runtime boundary.

## What problem this week solves

Before Docker, ResearchOps works only if the host machine happens to have the right Python version, dependencies, working directory, environment variables, and data paths.
That is fragile because two learners can run the same command and get different results.
Docker solves the runtime reproducibility problem by describing the operating system layer, Python layer, installed package layer, source-code layer, and default command in one file.
Compose solves the multi-process problem by starting the API and worker as separate services with shared configuration.
Environment variables solve the deployment variation problem: development and production can use different database paths and log levels without changing Python source.
Volumes solve the persistence problem: a container can be deleted while the SQLite database file remains available on the host or in a named volume.
.env handling solves the local convenience problem while `.env.example` documents required variables without committing real secrets.

## Beginner mental model

Think of an image as a sealed lunchbox recipe and a container as one lunchbox opened and used for a meal.
The Dockerfile is the recipe for building the image.
Each Dockerfile instruction creates or configures a layer.
A layer is like a transparent sheet placed on top of previous sheets.
If you change an early sheet, Docker must rebuild every sheet above it.
If you change only source code near the end, Docker can reuse dependency layers from cache.
Compose is a small local conductor: it starts multiple containers, gives them names, passes environment variables, mounts volumes, and connects ports.
A `.env` file is not magic; it is just a convenient local source of environment variables for Compose and settings libraries.
Runtime configuration is information the same image can receive differently each time it starts.
Build-time configuration changes the image itself and should not contain secrets.

## Core vocabulary

**Dockerfile**: text file containing instructions for building an image.
**Image**: read-only packaged filesystem plus metadata used to create containers.
**Container**: running process created from an image with its own filesystem view, environment, and network settings.
**Layer**: cached filesystem change produced by a Dockerfile instruction.
**Build context**: files sent to Docker during build; `.dockerignore` keeps unnecessary files out.
**Base image**: starting filesystem, such as `python:3.11-slim`.
**WORKDIR**: default directory for later Dockerfile commands and container startup.
**COPY**: instruction that copies files from the build context into the image.
**RUN**: build-time command that changes the image, such as installing dependencies.
**CMD**: default runtime command for containers created from the image.
**Port mapping**: host-to-container mapping such as `8000:8000`.
**Volume**: storage mounted into a container so data can outlive the container.
**Environment variable**: key/value string available to a running process.
**`.env`**: local uncommitted file containing environment variable values.
**`.env.example`**: committed template showing variable names and safe placeholder values.
**Secret**: sensitive value such as an API key; never bake it into images or commit it.
**12-factor config**: practice of keeping deploy-specific config in the environment, separate from code.
**Compose service**: named container definition in `docker-compose.yml`, such as `api` or `worker`.
**Health endpoint**: lightweight API route that proves the service is alive.

## Concept explanations from first principles

### Why a container is not a virtual machine
A virtual machine usually runs a full guest operating system.
A container runs ordinary host-kernel processes with filesystem, network, and environment isolation.
For this project, that means the ResearchOps API process still behaves like a Python process, but it starts inside a predictable filesystem.

### Why images should be boring
A good image contains application code and installed dependencies.
It should not contain your personal `.env`, private API keys, downloaded papers, local databases, or shell history.
If an image can be pushed to a registry without leaking secrets, the boundary is healthier.

### Why layer order matters
Docker checks whether each instruction can reuse a cached result.
If `COPY . .` happens before dependency installation, every source edit invalidates the dependency install layer.
A better order copies dependency metadata first, installs dependencies, then copies source code.

### Why Compose uses two services
The API answers HTTP requests.
The worker polls jobs and performs background work.
They share the same image and configuration style, but they run different commands because they own different runtime responsibilities.

### Why environment variables matter
Hard-coded paths make the app brittle.
Environment variables let the same image run with `DATABASE_URL=sqlite:////app/data/researchops.db` in Docker and a local path outside Docker.
The Python settings module becomes the one place that translates strings from the environment into typed application settings.


ResearchOps trace:
- Start with the already-working local command.
- Identify the process that owns the behavior: CLI, API, or worker.
- Move only runtime setup into Docker or settings.
- Keep domain decisions in core and service decisions in services.
- Pass variable values through environment variables.
- Store durable files in `/app/data` or another configured data directory.
- Use logs to prove the container received the expected settings.
- Use the health endpoint to prove the API process is reachable.

## ResearchOps-specific application

ResearchOps has three runtime concerns this week: API, worker, and data.
The API service should run the FastAPI app on `0.0.0.0` so Docker port mapping can expose it to the host.
The worker service should use the same image but start the job runner command instead of the HTTP server.
The SQLite file should be under a configured data directory, commonly `/app/data/researchops.db` inside the container.
The compose file should mount persistent data into `/app/data` so ingested papers, job rows, and experiment records are not lost when containers restart.
The settings module under `src/researchops/config/` should be importable by CLI, API, and workers without making services import infrastructure.
The `.env.example` file should document values like `RESEARCHOPS_DATABASE_URL`, `RESEARCHOPS_LOG_LEVEL`, `RESEARCHOPS_DATA_DIR`, and optional RAG provider keys using placeholders only.
The Dockerfile should install ResearchOps as a package so the `researchops` command works inside the container the same way it works locally.

ResearchOps trace:
- Start with the already-working local command.
- Identify the process that owns the behavior: CLI, API, or worker.
- Move only runtime setup into Docker or settings.
- Keep domain decisions in core and service decisions in services.
- Pass variable values through environment variables.
- Store durable files in `/app/data` or another configured data directory.
- Use logs to prove the container received the expected settings.
- Use the health endpoint to prove the API process is reachable.

## Code examples with line-by-line explanation

```dockerfile
FROM python:3.11-slim AS runtime
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e .
CMD ["researchops", "--help"]
```
Line 1: `FROM python:3.11-slim AS runtime` starts from a small official Python image and names the stage `runtime`.
Line 2: `WORKDIR /app` creates or selects `/app` as the default directory for following instructions.
Line 3: `PYTHONDONTWRITEBYTECODE=1` prevents `.pyc` files from being written into the container filesystem.
Line 4: `PYTHONUNBUFFERED=1` makes logs appear immediately, which matters when reading container logs.
Line 5: `COPY pyproject.toml README.md ./` copies package metadata before source code so dependency layers can be cached when possible.
Line 6: `COPY src ./src` copies the ResearchOps package into the image.
Line 7: `RUN pip install --no-cache-dir -e .` installs the package and console entry point inside the image without keeping pip cache files.
Line 8: `CMD ["researchops", "--help"]` gives a safe default command that proves the CLI is installed.

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    database_url: str = "sqlite:////app/data/researchops.db"
    log_level: str = "INFO"
    data_dir: str = "/app/data"

    model_config = SettingsConfigDict(
        env_prefix="RESEARCHOPS_",
        env_file=".env",
        extra="ignore",
    )

@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
```
Line 1: `lru_cache` lets the application create settings once per process instead of reparsing the environment repeatedly.
Line 2: `BaseSettings` reads values from environment variables and optional env files.
Line 4: `AppSettings` is the one typed object the rest of the app asks for when it needs configuration.
Line 5: `database_url` defaults to the container path where Compose will mount persistent storage.
Line 6: `log_level` defaults to `INFO`, which is useful in containers because logs are the main debugging surface.
Line 7: `data_dir` names the directory where durable runtime files should live.
Line 9: `model_config` controls how settings are loaded.
Line 10: `env_prefix="RESEARCHOPS_"` means `database_url` is overridden by `RESEARCHOPS_DATABASE_URL`.
Line 11: `env_file=".env"` allows local development to load values from a local file.
Line 12: `extra="ignore"` prevents unrelated variables in the environment from breaking settings creation.
Line 16: `get_settings` is a small factory used by API, CLI, and worker wiring code.
Line 17: `return AppSettings()` performs the actual load from defaults, environment variables, and `.env`.

```yaml
services:
  api:
    build: .
    command: uvicorn researchops.api.main:app --host 0.0.0.0 --port 8000
    env_file: .env
    ports:
      - "8000:8000"
    volumes:
      - researchops-data:/app/data

  worker:
    build: .
    command: researchops jobs run
    env_file: .env
    volumes:
      - researchops-data:/app/data

volumes:
  researchops-data:
```
Line 1: `services:` starts the list of runnable containers.
Line 2: `api:` names the HTTP service.
Line 3: `build: .` tells Compose to build the image from the current repository.
Line 4: the API command starts Uvicorn and binds to `0.0.0.0` so the host can reach it through port mapping.
Line 5: `env_file: .env` passes local runtime settings into the container.
Line 6: `ports:` starts host/container port mappings.
Line 7: `8000:8000` maps host port 8000 to container port 8000.
Line 8: `volumes:` starts persistent storage mounts.
Line 9: `researchops-data:/app/data` stores SQLite data outside the container filesystem.
Line 11: `worker:` names the background job service.
Line 13: `researchops jobs run` starts the existing worker command rather than an API server.
Line 18: `volumes:` declares named volumes managed by Docker.

Additional `.env.example` pattern:
```dotenv
# SQLite database URL used by CLI, API, and worker.
RESEARCHOPS_DATABASE_URL=sqlite:////app/data/researchops.db
# Log level for container logs.
RESEARCHOPS_LOG_LEVEL=INFO
# Directory for durable local application data.
RESEARCHOPS_DATA_DIR=/app/data
# Optional provider key; leave blank until you intentionally configure one.
RESEARCHOPS_OPENAI_API_KEY=
```
Line 1: # SQLite database URL used by CLI, API, and worker. -- this line is safe for a template because it contains no real secret.
Line 2: RESEARCHOPS_DATABASE_URL=sqlite:////app/data/researchops.db -- this line is safe for a template because it contains no real secret.
Line 3: # Log level for container logs. -- this line is safe for a template because it contains no real secret.
Line 4: RESEARCHOPS_LOG_LEVEL=INFO -- this line is safe for a template because it contains no real secret.
Line 5: # Directory for durable local application data. -- this line is safe for a template because it contains no real secret.
Line 6: RESEARCHOPS_DATA_DIR=/app/data -- this line is safe for a template because it contains no real secret.
Line 7: # Optional provider key; leave blank until you intentionally configure one. -- this line is safe for a template because it contains no real secret.
Line 8: RESEARCHOPS_OPENAI_API_KEY= -- this line is safe for a template because it contains no real secret.

## Common beginner mistakes

Putting `.env` into the image with `COPY . .` and forgetting to exclude it in `.dockerignore`.
Using `localhost` inside one container to reach another container; service names are used for container-to-container networking.
Binding Uvicorn to `127.0.0.1` inside the container, then wondering why the host cannot connect.
Writing the SQLite database inside an unmounted image path, then losing data when the container is removed.
Adding secrets with Dockerfile `ENV`, which bakes them into image history.
Letting services import Docker-specific details; Docker belongs in deployment files, while Python reads normal settings.
Confusing `docker compose build` with `docker compose up`; one builds images, the other starts containers.
Rebuilding the world after every source change because the Dockerfile copies the whole repository before installing dependencies.

## Debugging guidance

If the image fails to build, read the first failing Dockerfile instruction, not only the last line.
If `researchops` is not found in the container, confirm the package installation step ran and that `pyproject.toml` defines the script.
If the API starts but `curl` fails, check the Uvicorn host, Compose port mapping, and container logs.
If settings ignore your `.env`, check the prefix: `RESEARCHOPS_LOG_LEVEL` is not the same as `LOG_LEVEL` when an env prefix is configured.
If the worker cannot find the same database rows as the API, confirm both services mount the same volume and use the same database URL.
If a secret appears in build output, stop and remove it from Dockerfile instructions before sharing the image.
Use `docker compose logs api` for API errors and `docker compose logs worker` for background job errors.
Use `docker compose config` to see the final Compose configuration after variable interpolation.

ResearchOps trace:
- Start with the already-working local command.
- Identify the process that owns the behavior: CLI, API, or worker.
- Move only runtime setup into Docker or settings.
- Keep domain decisions in core and service decisions in services.
- Pass variable values through environment variables.
- Store durable files in `/app/data` or another configured data directory.
- Use logs to prove the container received the expected settings.
- Use the health endpoint to prove the API process is reachable.

## Design tradeoffs

One shared image for API and worker avoids duplicate builds and keeps dependency versions identical.
Separate service commands keep runtime responsibilities clean: API handles HTTP, worker handles jobs.
A named Docker volume is easier for beginners than bind-mounting many host paths, but bind mounts can be useful when inspecting files directly.
Editable install inside an image is acceptable for this learning project; a later hardened release could build a wheel, but that is not required this week.
Using `.env` improves local ergonomics, but production systems often inject variables through deployment platforms instead.
Keeping configuration in `src/researchops/config/settings.py` centralises decisions and avoids scattering `os.environ` across commands and routes.

ResearchOps trace:
- Start with the already-working local command.
- Identify the process that owns the behavior: CLI, API, or worker.
- Move only runtime setup into Docker or settings.
- Keep domain decisions in core and service decisions in services.
- Pass variable values through environment variables.
- Store durable files in `/app/data` or another configured data directory.
- Use logs to prove the container received the expected settings.
- Use the health endpoint to prove the API process is reachable.

## Testing implications

Settings tests should prove defaults work when no environment variables are set.
Settings tests should prove environment variables override defaults.
Tests should use `monkeypatch` for environment variables so one test does not leak state into another.
If `get_settings` is cached, tests must clear the cache before checking a new environment.
Container validation is not a replacement for unit tests; it proves packaging and service wiring.
The health endpoint should stay lightweight and should not require expensive model loading or network calls.

ResearchOps trace:
- Start with the already-working local command.
- Identify the process that owns the behavior: CLI, API, or worker.
- Move only runtime setup into Docker or settings.
- Keep domain decisions in core and service decisions in services.
- Pass variable values through environment variables.
- Store durable files in `/app/data` or another configured data directory.
- Use logs to prove the container received the expected settings.
- Use the health endpoint to prove the API process is reachable.

## Architecture implications

The `config/` package is allowed to depend on settings libraries and Python standard library tools.
Core models and protocols must not import settings because core must remain independent of runtime environment.
Services should still depend on protocols, not concrete repositories, even when running inside Docker.
CLI, API, and worker entry points are the correct places to read settings and wire concrete infrastructure.
Docker files live at the deployment boundary; they should not force business logic into command handlers.
The image packages the modular monolith; it does not turn the app into microservices.

ResearchOps trace:
- Start with the already-working local command.
- Identify the process that owns the behavior: CLI, API, or worker.
- Move only runtime setup into Docker or settings.
- Keep domain decisions in core and service decisions in services.
- Pass variable values through environment variables.
- Store durable files in `/app/data` or another configured data directory.
- Use logs to prove the container received the expected settings.
- Use the health endpoint to prove the API process is reachable.

## How this connects to AI engineering / ML research

Research and ML projects often fail to reproduce because environment setup is implicit.
A container makes the Python version, installed dependencies, command, and runtime paths explicit.
Experiment tracking is more trustworthy when the runtime can be recreated.
RAG behavior depends on storage, retrieval, and configuration; Docker helps run those pieces together consistently.
Secrets for model providers or external APIs must be injected at runtime so images can be shared safely.
Workers are common in ML systems because expensive tasks should not block API requests.

## Mini quizzes

1. What is the difference between an image and a container?
2. Which Dockerfile instruction usually installs Python dependencies?
3. Why should `.env` be ignored by Git and Docker build context?
4. Why does the API bind to `0.0.0.0` inside the container?
5. What happens to SQLite data stored only inside a removed container?
6. Why can the API and worker use the same image but different commands?
7. What setting should override the default database URL at runtime?
8. Why should tests clear a cached settings factory?

## Explain-it-aloud prompts

Explain the path from `docker compose up` to a running FastAPI server.
Explain why Docker was not introduced before the CLI and API worked locally.
Explain how `RESEARCHOPS_DATABASE_URL` changes application behavior without editing Python code.
Explain how a named volume protects the SQLite database from container deletion.
Explain why a secret in a Dockerfile is more dangerous than a secret in an uncommitted local `.env` file.

## What to memorize

Images are built; containers run.
Put secrets in runtime environment, not images.
Use `.env.example` for documentation and `.env` for local private values.
Use volumes for data that must survive container removal.
Use `docker compose up --build` when you need to rebuild and start services.
Bind web servers to `0.0.0.0` inside containers when exposing ports.

## What to understand deeply

Understand that Docker packages the runtime boundary, not the business architecture.
Understand that settings are part of application design because they define what can vary safely between environments.
Understand layer caching well enough to place slow-changing files before fast-changing source code.
Understand that API and worker containers can share image code while performing different process roles.
Understand that persistence belongs outside disposable containers.

## What not to worry about yet

Do not worry about Kubernetes.
Do not worry about publishing images to registries.
Do not worry about production secrets managers.
Do not worry about final portfolio packaging or release notes.
Do not rewrite the RAG assistant, worker, API, or storage layer while learning Docker.
Do not introduce new heavy ML dependencies this week.

## Bridge to next week

At the end of Week 18, ResearchOps should be runnable as a complete local stack.
That gives the next week a stable runtime story to build on.
You will be able to say: the app runs locally, the app runs in containers, and the runtime settings are documented.
The next chapter can focus on communicating and polishing the system rather than discovering hidden setup problems.

## Detailed beginner review drill

1. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
2. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
3. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
4. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
5. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
6. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
7. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
8. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
9. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
10. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
11. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
12. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
13. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
14. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
15. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
16. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
17. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
18. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
19. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
20. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
21. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
22. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
23. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
24. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
25. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
26. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
27. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
28. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
29. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
30. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
31. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
32. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
33. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
34. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
35. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
36. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
37. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
38. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
39. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
40. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
41. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
42. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
43. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
44. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
45. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
46. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
47. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
48. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
49. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
50. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
51. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
52. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
53. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
54. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
55. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
56. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
57. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
58. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
59. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
60. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
61. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
62. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
63. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
64. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
65. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
66. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
67. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
68. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
69. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
70. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
71. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
72. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
73. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
74. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
75. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
76. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
77. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
78. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
79. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
80. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
81. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
82. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
83. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
84. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
85. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
86. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
87. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
88. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
89. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
90. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
91. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
92. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
93. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
94. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
95. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
96. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
97. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
98. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
99. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
100. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
101. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
102. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
103. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
104. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
105. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
106. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
107. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
108. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
109. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
110. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
111. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
112. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
113. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
114. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
115. Trace the ResearchOps container decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
116. Trace the ResearchOps layer decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
117. Trace the ResearchOps settings decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
118. Trace the ResearchOps volume decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
119. Trace the ResearchOps compose service decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
120. Trace the ResearchOps image decision with a real value: start from the file that declares it, name the process that reads it, and state the command that proves it worked.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 18 — Docker and Environment Config:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
