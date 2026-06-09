<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 18 — Docker and Environment Config:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 18 Docker and Environment Configuration

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 18: Docker and Environment Configuration

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Shipping the whole system**.
The practical milestone is: `docker-compose up` starts the API and worker. `curl http://localhost:8000/health` responds.
The expected capability is: Can write a Dockerfile, compose multi-service applications, manage environment configuration with pydantic-settings, and explain layer caching. ---
This chapter is one step in the ResearchOps system, not a random lesson.
The visible feature matters because it proves the idea works.
The hidden skill matters because it lets you build the next chapter without confusion.
A complete pass through this chapter means you can read the code, run it, test it, break it, and explain it aloud.

Use this study order:
- Read the story first without typing.
- Trace the smallest code example.
- Find the project file that owns the behavior.
- Run the validation command.
- Explain one happy path and one failure path.

## What you already know from previous weeks

- Week 14 taught FastAPI Layer; keep its responsibility in mind, but do not rebuild it here.
- Week 15 taught Async I/O Network Fetching; keep its responsibility in mind, but do not rebuild it here.
- Week 16 taught Local Worker and Job System; keep its responsibility in mind, but do not rebuild it here.
- Week 17 taught RAG Assistant; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 18 solves the project problem behind **Docker and Environment Configuration**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept `Dockerfile: `FROM`, `COPY`, `RUN`, `CMD`, layer caching` helps solve part of this gap.
- The concept `Multi-stage builds: separate build and runtime layers` helps solve part of this gap.
- The concept ``docker-compose.yml`: API and worker as separate services` helps solve part of this gap.
- The concept `Volume mounts for the SQLite database` helps solve part of this gap.
- The concept `Environment variable management: `.env`, `pydantic-settings`` helps solve part of this gap.
- The concept `Testing the full stack in containers` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Docker and Environment Configuration**?
- Ask: what is the owner for **Docker and Environment Configuration**?
- Ask: what is the transformation for **Docker and Environment Configuration**?
- Ask: what is the proof for **Docker and Environment Configuration**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| Dockerfile | Dockerfile: `FROM`, `COPY`, `RUN`, `CMD`, layer caching | This term names one job in the Week 18 milestone. |
| Multi-stage builds | Multi-stage builds: separate build and runtime layers | This term names one job in the Week 18 milestone. |
| docker-compose.yml | `docker-compose.yml`: API and worker as separate services | This term names one job in the Week 18 milestone. |
| Volume mounts for the SQLite database | Volume mounts for the SQLite database | This term names one job in the Week 18 milestone. |
| Environment variable management | Environment variable management: `.env`, `pydantic-settings` | This term names one job in the Week 18 milestone. |
| Testing the full stack in containers | Testing the full stack in containers | This term names one job in the Week 18 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: Dockerfile: `FROM`, `COPY`, `RUN`, `CMD`, layer caching
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 18, it supports the milestone: `docker-compose up` starts the API and worker. `curl http://localhost:8000/health` responds.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: Multi-stage builds: separate build and runtime layers
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 18, it supports the milestone: `docker-compose up` starts the API and worker. `curl http://localhost:8000/health` responds.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: `docker-compose.yml`: API and worker as separate services
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 18, it supports the milestone: `docker-compose up` starts the API and worker. `curl http://localhost:8000/health` responds.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Volume mounts for the SQLite database
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 18, it supports the milestone: `docker-compose up` starts the API and worker. `curl http://localhost:8000/health` responds.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: Environment variable management: `.env`, `pydantic-settings`
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 18, it supports the milestone: `docker-compose up` starts the API and worker. `curl http://localhost:8000/health` responds.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: Testing the full stack in containers
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 18, it supports the milestone: `docker-compose up` starts the API and worker. `curl http://localhost:8000/health` responds.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `Dockerfile`
- `docker-compose.yml`
- `.env.example` — documented environment variables
- `src/researchops/config/settings.py` — all config from env vars
Study those files in this order:
1. Find the user-facing entry point.
2. Find the service or core concept that owns the meaning.
3. Find the infrastructure only when outside resources are needed.
4. Find the tests that prove the behavior.
5. Find the validation command that a learner runs manually.
The goal is to know why each file exists.
If two files seem to own the same decision, stop and clarify the boundary.

## Code examples with line-by-line explanation

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install .[all]
CMD ["uvicorn", "researchops.api.main:app", "--host", "0.0.0.0"]
```

Line-by-line explanation:
- Line 1: `FROM python:3.11-slim` — This produces the result or performs the declared setup step.
- Line 2: `WORKDIR /app` — This produces the result or performs the declared setup step.
- Line 3: `COPY . .` — This produces the result or performs the declared setup step.
- Line 4: `RUN pip install .[all]` — This produces the result or performs the declared setup step.
- Line 5: `CMD ["uvicorn", "researchops.api.main:app", "--host", "0.0.0.0"]` — This produces the result or performs the declared setup step.

How to use this example:
- Name the input.
- Name the output.
- Predict the result before running anything.
- Connect the shape to the real ResearchOps file.
- Write one sentence about why each line belongs.

## Common beginner mistakes

- **Mistake:** Pasting code before knowing the owner of the behavior.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Changing many files at once.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Skipping the failure path.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Reading only the happy path test.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Ignoring the validation command.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Using vague names.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Putting business rules in the user interface layer.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Treating logs, errors, and tests as decoration.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Optimizing before correctness is visible.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Building future-week features early.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.

## Debugging guidance

- Copy the exact failing command.
- Read the first useful error line.
- Read the final error line.
- Classify the failure as import, input, state, file, database, network, model, or expectation.
- Reproduce it with the smallest command.
- Inspect the value closest to the failure.
- Fix the cause, not only the symptom.
- Run the narrowest test.
- Run the chapter validation command.
- Write down what the error was teaching.
Debugging questions:
- What did I expect?
- What happened?
- Which value first became wrong?
- Which layer created that value?
- Which test should catch this next time?

## Design tradeoffs

- **Simple first version:** Easy to understand, but not the final production shape.
- **Clear layers:** More files, but less confusion as features grow.
- **Explicit errors:** More code, but failures become teachable.
- **Small unit tests:** Fast feedback, but less end-to-end confidence.
- **Integration tests:** Real wiring, but slower and more setup.
- **Configuration:** Flexible behavior, but defaults must be clear.
The right question is not "What is the fanciest design?"
The right question is "What design teaches the responsibility clearly and can grow next week?"

## Testing implications

Tests for this chapter:
- `tests/e2e/test_docker.py` (optional) — smoke test against running container
Validation commands:
```bash
docker-compose build
docker-compose up -d
curl http://localhost:8000/health
docker-compose down
```
- Arrange the data.
- Act on the system.
- Assert the visible promise.
- Check one failure path.
- Keep unit tests fast.
- Use integration tests only when real wiring matters.

## Architecture implications

ResearchOps stays understandable when dependencies point inward.
```text
CLI / API / Worker -> Services -> Core
Infrastructure implements core-facing contracts and is wired at the outside.
```
- Does the UI layer avoid business logic?
- Does the service layer own workflow decisions?
- Does core avoid infrastructure imports?
- Does infrastructure do outside-world work?
- Do tests use fakes when possible?
Architecture is not ceremony.
Architecture is named responsibility.

## How this connects to AI engineering / ML research

AI engineering needs more than models.
It needs reliable data flow, clear interfaces, repeatable experiments, visible failures, and honest evaluation.
Week 18 contributes by making **docker and environment configuration** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 18 solve?
- What is the main input?
- What is the main output?
- Which file owns the main responsibility?
- Which layer should not contain business logic?
- What is one happy path?
- What is one failure path?
- What command proves the chapter works?
- What should you not build early?
- How does this prepare the next week?

## Explain-it-aloud prompts

- Explain Docker and Environment Configuration in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Docker and Environment Configuration.
- The milestone: `docker-compose up` starts the API and worker. `curl http://localhost:8000/health` responds.
- The main project files.
- The validation command.
- The boundary rule for the layer you are touching.
- The habit of testing before moving forward.

## What to understand deeply

- Why this feature belongs now.
- How data moves through the chapter.
- Which file owns which decision.
- How the failure path is handled.
- Why the tests prove behavior.
- How this week makes future work safer.

## What not to worry about yet

- Perfect scale.
- Fancy abstractions.
- Future-week features.
- Every option in every library.
- Premature optimization.
- Comparing your speed to someone else.
Focus on the milestone.
A clear small milestone beats a confusing large one.

## Bridge to next week

Next week is Week 19: **Documentation and Portfolio Polish**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: README is portfolio-quality. Architecture document explains every design decision. A demo script exists.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace `Dockerfile: `FROM`, `COPY`, `RUN`, `CMD`, layer caching` from user input to project result.
- Drill 2: Write one sentence defining `Dockerfile: `FROM`, `COPY`, `RUN`, `CMD`, layer caching` without copying the notes.
- Drill 3: Find the file where `Dockerfile: `FROM`, `COPY`, `RUN`, `CMD`, layer caching` appears or should appear.
- Drill 4: Name one wrong implementation of `Dockerfile: `FROM`, `COPY`, `RUN`, `CMD`, layer caching` and why it would hurt.
- Drill 5: Name one test that would protect `Dockerfile: `FROM`, `COPY`, `RUN`, `CMD`, layer caching`.
- Drill 6: Trace `Multi-stage builds: separate build and runtime layers` from user input to project result.
- Drill 7: Write one sentence defining `Multi-stage builds: separate build and runtime layers` without copying the notes.
- Drill 8: Find the file where `Multi-stage builds: separate build and runtime layers` appears or should appear.
- Drill 9: Name one wrong implementation of `Multi-stage builds: separate build and runtime layers` and why it would hurt.
- Drill 10: Name one test that would protect `Multi-stage builds: separate build and runtime layers`.
- Drill 11: Trace ``docker-compose.yml`: API and worker as separate services` from user input to project result.
- Drill 12: Write one sentence defining ``docker-compose.yml`: API and worker as separate services` without copying the notes.
- Drill 13: Find the file where ``docker-compose.yml`: API and worker as separate services` appears or should appear.
- Drill 14: Name one wrong implementation of ``docker-compose.yml`: API and worker as separate services` and why it would hurt.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes

## Why packaging matters

You have built a working Python application. It runs on your machine. But "works on my machine" is not a product. It is a promise that is broken the moment anyone else tries to run it.

Packaging solves this by capturing not just your code, but the exact Python version, the installed libraries, the required files, and the command needed to start the app. A packaged application can be reproduced — same code, same behaviour — on any machine that can run the package format.

Docker is the most widely used packaging format for Python applications. Understanding it is a professional skill that appears in nearly every engineering job that involves running Python in any kind of server or cloud context.

---

## What Docker is

Docker is a system for building and running containers.

A **container** is a lightweight, isolated environment that runs one or more processes. It looks like a miniature operating system from the perspective of the process running inside it, but it shares the host machine's kernel. This makes containers much lighter than full virtual machines.

Docker gives you:
- A standard way to describe the environment your app needs (a `Dockerfile`).
- A command to build that description into an image.
- A command to run the image as a container.
- Tools to manage multiple containers together (`docker compose`).

The key promise of Docker is reproducibility: an image built on your laptop can run identically on a colleague's laptop, a CI server, or a cloud VM.

---

## Image

A Docker **image** is a read-only, layered snapshot of a filesystem and its metadata. It includes:
- A base operating system or language runtime.
- Any libraries you installed.
- Your application's source code.
- The command to run when the container starts.

An image is a built artifact. You build an image once (or rebuild it when code changes) and run it many times. Images are identified by a name and optional tag, e.g., `researchops:latest` or `researchops:1.0.0`.

Images are stored locally (in Docker's local cache) and can be pushed to a registry like Docker Hub or GitHub Container Registry to share with others.

---

## Container

A Docker **container** is a running instance of an image. The image is the recipe; the container is the dish.

You can run many containers from the same image. Each container gets its own isolated filesystem (a copy-on-write layer on top of the image). Changes made inside a container (like writing a file) are local to that container and disappear when the container stops, unless you explicitly use a volume to persist data.

Containers are ephemeral by default. If you run a container, stop it, and start a new one, the new container starts fresh from the image, with no memory of what the previous container did. This is a feature: it forces you to store important data outside the container (in a volume or a database), which makes the system more reliable.

---

## Dockerfile

A `Dockerfile` is a text file that describes how to build an image. It is a sequence of instructions, each of which adds a layer to the image.

Here is a Dockerfile appropriate for ResearchOps, explained line by line:

```dockerfile
FROM python:3.11-slim                        # line 1
WORKDIR /app                                 # line 2
COPY pyproject.toml README.md ./             # line 3
COPY src ./src                               # line 4
RUN pip install --no-cache-dir -e ".[api]"  # line 5
CMD ["researchops", "--help"]               # line 6
```

**Line 1**: `FROM python:3.11-slim` — start from the official Python 3.11 "slim" image (a minimal Debian-based image with Python pre-installed). The `slim` variant excludes most optional system packages, keeping the image small. Always pin the Python version: `python:3.11` not `python:latest`. `latest` can change without warning.

**Line 2**: `WORKDIR /app` — set the working directory inside the container. All subsequent commands run in `/app`. This creates the directory if it does not exist. Using `/app` is a common convention for Python apps.

**Line 3**: `COPY pyproject.toml README.md ./` — copy the project metadata files into `/app`. These are copied before the source code so Docker can cache the dependency installation layer. If `pyproject.toml` does not change, Docker reuses the cached layer from the previous build and skips the `pip install` step.

**Line 4**: `COPY src ./src` — copy the application source code into `/app/src`. This comes after the dependency copy. If you change source code (which is frequent), only layers from this line onwards are rebuilt. The dependency installation (line 5) is still cached.

**Line 5**: `RUN pip install --no-cache-dir -e ".[api]"` — install the package in editable mode with the `api` extras. `--no-cache-dir` prevents pip from writing its own cache inside the image, keeping the image smaller. In a production image you might use a plain install (not editable), but for a learning project, editable mode is fine.

**Line 6**: `CMD ["researchops", "--help"]` — the default command to run when the container starts. `CMD` uses the exec form (a JSON array of strings), which is preferred over the shell form. This is the default; it can be overridden when running the container.

---

## Build context

The **build context** is the set of files that Docker sends to the Docker daemon when you run `docker build`. By default it is the current directory (`.`).

```bash
docker build -t researchops:local .
```

The `.` at the end is the build context. Docker reads the `Dockerfile` from the context and sends the files to the daemon, which builds the image.

A `.dockerignore` file (similar to `.gitignore`) excludes files from the build context. Always exclude:
- `.git/` (large, not needed)
- `__pycache__/`
- `.venv/` or `venv/` (the container installs its own dependencies)
- `data/` (runtime data, not source)
- `*.pyc`

A smaller build context means faster builds and smaller images.

---

## Layer

Each instruction in the `Dockerfile` that modifies the filesystem creates a new **layer**. Docker caches layers. When you rebuild, Docker checks whether the instruction and its inputs have changed. If not, it reuses the cached layer.

This is why layer order matters: put infrequently changing instructions (like `FROM`, `RUN pip install`) before frequently changing ones (like `COPY src`). If the source code changes and `COPY src` is the last instruction, Docker can reuse all earlier layers and only rebuild from `COPY src` onwards. This makes rebuilds fast.

If you copy the source code before installing dependencies, any source code change forces a full reinstall. That is slow and unnecessary.

**Correct order**: copy metadata → install dependencies → copy source.

---

## Environment variable

An **environment variable** is a named value that the operating system makes available to running processes. Programs read environment variables to configure their behaviour without hardcoding values.

In a container, you can set environment variables:
- In the `Dockerfile` with `ENV KEY=value` (build-time, baked into the image).
- At runtime with `docker run -e KEY=value` (run-time, not in the image).
- From a file with `docker run --env-file .env` or in a compose file with `env_file: .env`.

Run-time variables are preferred for anything that should change between environments (development, staging, production) or contains a secret.

```bash
docker run -e LOG_LEVEL=DEBUG researchops:local researchops --help
```

Inside the container, your Python code reads `LOG_LEVEL` with `os.environ.get("LOG_LEVEL", "INFO")`.

---

## `.env` file

A `.env` file is a plain text file containing key-value pairs, one per line:

```bash
DATABASE_URL=sqlite:///data/researchops.db
LOG_LEVEL=INFO
OPENAI_API_KEY=your-key-here
```

Tools like `docker compose`, `pydantic-settings`, and the `python-dotenv` package can load `.env` files automatically.

**Critical rules**:
- `.env` must be in `.gitignore`. It may contain secrets. Never commit it.
- `.env.example` (no real values) must be committed so teammates know which variables are needed.

The difference:
- `.env` → contains real values, never committed.
- `.env.example` → contains placeholder values, always committed.

---

## Volume

A Docker **volume** is a persistent storage location that exists outside the container's lifecycle. When a container stops and is removed, its internal filesystem disappears. Anything you want to survive (databases, uploaded files, generated data) must be stored in a volume.

Two kinds of volumes:
- **Named volume**: `docker volume create mydata`. Managed by Docker. Survives container restarts.
- **Bind mount**: a directory on your host machine mounted into the container. Used in development.

```yaml
volumes:
  - ./data:/app/data    # bind mount: ./data on host → /app/data in container
```

This means any file written to `/app/data` inside the container is actually written to `./data` on your host. When the container stops, the data persists in `./data`.

For ResearchOps, the SQLite database and any artifact files should be stored in a volume so they survive container restarts.

---

## Port mapping

A container runs in isolation. By default, network ports inside the container are not accessible from outside. You must map a container port to a host port.

```bash
docker run -p 8000:8000 researchops:local uvicorn researchops.api.main:app --host 0.0.0.0 --port 8000
```

`-p 8000:8000` means: map port 8000 on the host to port 8000 in the container. After this, `curl http://localhost:8000` on your host reaches the FastAPI server running inside the container.

The format is `-p HOST_PORT:CONTAINER_PORT`. You can use different port numbers:

```bash
-p 9000:8000    # host port 9000 → container port 8000
```

Inside the container, the app must listen on `0.0.0.0` (all interfaces), not `127.0.0.1` (loopback only). `0.0.0.0` allows traffic that arrives from outside the container to reach the app.

---

## docker-compose

**docker compose** (or the older `docker-compose` command) is a tool for defining and running multi-container applications. Instead of running multiple long `docker run` commands manually, you define all services in a single `docker-compose.yml` file.

Benefits:
- One command (`docker compose up`) starts everything.
- Services can reference each other by name.
- Volumes and environment variables are defined once.
- Easy to reproduce the exact local setup.

---

## ResearchOps docker-compose.yml explained

```yaml
services:
  app:
    build: .
    command: researchops --help
    env_file:
      - .env
    volumes:
      - ./data:/app/data

  api:
    build: .
    command: uvicorn researchops.api.main:app --host 0.0.0.0 --port 8000
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data

  worker:
    build: .
    command: researchops jobs run
    env_file:
      - .env
    volumes:
      - ./data:/app/data
```

**`services:`** — the top-level key. Each named entry is a service (a container definition).

**`app:` service**

```yaml
  app:
    build: .
    command: researchops --help
    env_file:
      - .env
    volumes:
      - ./data:/app/data
```

`build: .` — build the image from the `Dockerfile` in the current directory. Docker will rebuild it only if the source files change.

`command: researchops --help` — override the `CMD` from the `Dockerfile`. This service just prints the CLI help and exits. Useful for smoke-testing that the CLI entry point is working.

`env_file: - .env` — load environment variables from `.env`. The variables become available inside the container.

`volumes: - ./data:/app/data` — bind mount the `./data` directory. The ResearchOps database and artifact files live here. This ensures they persist between container runs.

**`api:` service**

```yaml
  api:
    build: .
    command: uvicorn researchops.api.main:app --host 0.0.0.0 --port 8000
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
```

`command: uvicorn researchops.api.main:app --host 0.0.0.0 --port 8000` — start the FastAPI app using uvicorn. `--host 0.0.0.0` is required (see port mapping section above). `--port 8000` is the port inside the container.

`ports: - "8000:8000"` — map host port 8000 to container port 8000. After `docker compose up api`, `curl http://localhost:8000` reaches FastAPI.

**`worker:` service**

```yaml
  worker:
    build: .
    command: researchops jobs run
    env_file:
      - .env
    volumes:
      - ./data:/app/data
```

`command: researchops jobs run` — run the background job worker. Same environment and volume as the other services.

**This is a learning template.** Real production compose files add health checks, restart policies, resource limits, and separate networks. Start with this template and adapt it to your needs.

---

## Service

In docker-compose terms, a **service** is one container definition. Each service has:
- A build source or pre-built image.
- A command to run.
- Environment variables.
- Ports.
- Volumes.

Services are independent but can communicate over a shared network that docker compose creates automatically. Services reference each other by name (e.g., `http://api:8000` from the `worker` container).

---

## Why Docker comes late in the curriculum

Docker is introduced in Week 18 rather than Week 1 because:

1. **First, make it work. Then make it portable.** You need to understand what the application does before packaging it. A Docker image of a broken app is just a broken app in a box.

2. **Docker reveals assumptions.** When you containerise an app, Docker forces you to be explicit about everything: which files are needed, which env vars are required, which ports are used, where data is stored. This is only meaningful once the app is mature enough to have those answers.

3. **Learning curve.** Docker has its own conceptual model (images, layers, contexts, volumes). Learning it while also learning the application domain is too much at once.

4. **Reward structure.** In Week 18 you already have a working app. Containerising it is satisfying. The demo is clean: `docker compose up api` → `curl http://localhost:8000/papers` → it works.

---

## pydantic-settings for environment configuration

Instead of reading `os.environ.get(...)` manually throughout the codebase, use `pydantic-settings` to centralise configuration:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "sqlite:///data/researchops.db"
    log_level: str = "INFO"
    openai_api_key: str = ""
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
```

Line by line:

`from pydantic_settings import BaseSettings, SettingsConfigDict` — import the base class and the configuration descriptor.

`model_config = SettingsConfigDict(env_file=".env", ...)` — tell pydantic-settings to load variables from `.env` if the file exists. Environment variables take precedence over `.env` values.

`database_url: str = "sqlite:///data/researchops.db"` — declare a setting with a default value. If `DATABASE_URL` is set in the environment, pydantic-settings uses that value. If not, it uses the default.

`openai_api_key: str = ""` — an empty string default means the app starts without the key. Any code that uses the key should check whether it is empty before making API calls.

To use settings anywhere in the codebase:

```python
from researchops.settings import Settings

settings = Settings()
print(settings.database_url)
```

---

## Testing configuration

Configuration bugs often appear only in deployment. Writing tests for settings prevents this.

```python
import os
import pytest
from researchops.settings import Settings


def test_default_database_url():
    settings = Settings()
    assert settings.database_url == "sqlite:///data/researchops.db"


def test_env_override(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///tmp/test.db")
    settings = Settings()
    assert settings.database_url == "sqlite:///tmp/test.db"
```

`monkeypatch.setenv` sets an environment variable for the duration of the test and removes it afterwards. This keeps tests isolated: they do not accidentally affect each other or the real environment.

Always test:
- Default values are correct.
- Environment variable overrides are applied.
- Missing required variables raise a clear error (not a silent `None`).

---

## `.env.example` conventions

A well-written `.env.example` documents every variable:

```bash
# ResearchOps environment configuration
# Copy this file to .env and fill in your values.
# Never commit .env.

# Path to the SQLite database file
DATABASE_URL=sqlite:///data/researchops.db

# Logging verbosity: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# Embedding model name (sentence-transformers hub name)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Optional: OpenAI-compatible API key for real generation
# Leave empty to use Ollama or the fake generator.
OPENAI_API_KEY=
```

This serves as self-documenting configuration. Any new developer clones the repo, copies `.env.example` to `.env`, fills in values, and the app runs.

---

## Common mistakes and how to avoid them

**Mistake 1: Copying `.venv` into the image**
If you do not add `.venv/` to `.dockerignore`, Docker copies the entire virtual environment into the build context. This makes builds slow and images huge. Add `.venv/` to `.dockerignore`.

**Mistake 2: Using `ENV` in Dockerfile for secrets**
`ENV KEY=value` in a `Dockerfile` bakes the value into the image. The image can be inspected with `docker inspect`. Never use `ENV` for secrets. Use `--env-file` at run time.

**Mistake 3: Listening on `127.0.0.1` in the container**
If uvicorn binds to `127.0.0.1`, traffic from outside the container is rejected. Always use `0.0.0.0` inside a container.

**Mistake 4: No data volume**
If you write the SQLite database inside the container without a volume mount, every `docker compose down` wipes the data. Mount `./data:/app/data` to persist data across restarts.

**Mistake 5: Building every time**
`docker compose up --build` rebuilds the image every time. In development, omit `--build` after the first build, unless you have actually changed the source code. `docker compose up` (no `--build`) starts existing containers quickly.

---

## Build and run commands

```bash
# Build the image
docker build -t researchops:local .

# Run the CLI help
docker run researchops:local researchops --help

# Run the API server
docker run -p 8000:8000 --env-file .env -v $(pwd)/data:/app/data researchops:local \
    uvicorn researchops.api.main:app --host 0.0.0.0 --port 8000

# With docker compose
docker compose up           # start all services (uses cached images)
docker compose up --build   # rebuild and start all services
docker compose up api       # start only the api service
docker compose down         # stop and remove containers (data volume persists)
docker compose logs api     # show logs from the api service
```

---

## Summary

- Docker packages an application with its runtime environment for reproducible execution.
- An image is a read-only snapshot; a container is a running instance.
- A `Dockerfile` describes how to build an image, layer by layer.
- Layer order matters: put infrequently changing instructions first.
- Environment variables configure runtime behaviour without changing code.
- A `.env` file stores local settings; never commit it. `.env.example` documents the variables; always commit it.
- Volumes persist data outside the container lifecycle.
- Port mapping exposes container ports to the host.
- `docker-compose.yml` orchestrates multiple services with a single command.
- `pydantic-settings` centralises configuration and makes it testable.
- Docker comes late because it is most valuable once the app is working.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 18 — Docker and Environment Config:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
