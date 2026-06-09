# Exercises - Week 18 Docker and Environment Configuration

## Warm-up exercises

### 1. Write a minimal Dockerfile for a Python command

Create a file called `Dockerfile.minimal` (in `/tmp`, not in the repo root) that:
- Starts from `python:3.11-slim`
- Sets `WORKDIR /app`
- Copies a single `hello.py` file
- Runs `python hello.py` as the default command

`hello.py` should print `"Hello from Docker!"`. Build and run it. Confirm the output.

### 2. Identify which layer is rebuilt

Given this Dockerfile order:

```dockerfile
FROM python:3.11-slim
COPY src ./src
COPY pyproject.toml ./
RUN pip install -e .
CMD ["myapp", "--help"]
```

If you change one line in `src/myapp/cli.py`, which lines get re-executed on the next build? Draw the dependency chain from the changed file upward. Then reorder the Dockerfile so that the `pip install` layer is not invalidated by source code changes.

### 3. Read an env var with a default

Write a Python snippet that reads `LOG_LEVEL` from the environment with a default of `"INFO"` and prints it. Run it without setting the variable, then with `LOG_LEVEL=DEBUG python snippet.py`. Confirm the default and the override both work.

### 4. Write a Settings class with pydantic-settings

Define a `Settings` class that reads three variables:
- `DATABASE_URL` (default: `"sqlite:///data/researchops.db"`)
- `LOG_LEVEL` (default: `"INFO"`)
- `OPENAI_API_KEY` (default: `""`)

Instantiate it and print the values. Override `LOG_LEVEL` via the environment. Confirm the override is applied.

### 5. Write a .env.example file

Write a `.env.example` for ResearchOps. Include all three variables from exercise 4 with placeholder values. Add a comment above each variable explaining what it does. Do not include any real secret values.

### 6. Add entries to .dockerignore

List five things that should appear in `.dockerignore` for a Python project. Explain why each one should be excluded from the build context.

---

## Project exercises

### 1. Write the Dockerfile

In the repo root, create a `Dockerfile` (or update the existing one) that:
- Starts from `python:3.11-slim`.
- Sets `WORKDIR /app`.
- Copies `pyproject.toml` and `README.md` first.
- Installs the package with `pip install --no-cache-dir -e ".[api]"`.
- Copies `src/` after installation.
- Sets `CMD ["researchops", "--help"]`.

Build it: `docker build -t researchops:local .`

Run the default command: `docker run researchops:local`

Confirm you see the CLI help output.

### 2. Write the docker-compose.yml

Create or update `docker-compose.yml` with the three services from notes.md:
- `app`: runs `researchops --help`
- `api`: runs uvicorn on port 8000
- `worker`: runs `researchops jobs run`

All services must use `env_file: .env` and mount `./data:/app/data`.

Start the API: `docker compose up api`

Test it: `curl http://localhost:8000/docs`

### 3. Implement Settings with pydantic-settings

In `src/researchops/settings.py`, implement a `Settings` class using `pydantic-settings`. It should read at minimum:
- `DATABASE_URL`
- `LOG_LEVEL`
- `OPENAI_API_KEY`
- `EMBEDDING_MODEL`

Use a singleton pattern or a `get_settings()` function so the settings are instantiated once.

### 4. Write settings tests

In `tests/unit/test_settings.py`, write tests that:
- Verify the default values are correct.
- Use `monkeypatch.setenv` to override `LOG_LEVEL` and verify the override is applied.
- Use `monkeypatch.setenv` to override `DATABASE_URL` and verify it.
- Verify that the `OPENAI_API_KEY` default is empty string (not `None`).

Run `pytest tests/unit/test_settings.py -v` and confirm all pass.

### 5. Update .env.example

Update `.env.example` in the repo root to document every variable in the `Settings` class. Add a comment for each variable explaining what it configures. Confirm the file is committed but `.env` is not.

### 6. Add .dockerignore

Create `.dockerignore` with at least these entries:
```
.git
.venv
venv
__pycache__
*.pyc
*.pyo
.pytest_cache
.ruff_cache
data/
.env
```

Rebuild the image and confirm it builds successfully. Check whether the build is faster now that Docker is not sending unused files.

---

## Stretch exercises

### 1. Add a separate compose service for the worker

Extend `docker-compose.yml` to define the `worker` service distinctly from `app`. Give `worker` a `restart: unless-stopped` policy so it restarts automatically if it crashes. Start just the worker: `docker compose up worker -d`. Check its logs: `docker compose logs worker`.

### 2. Add a non-root user

In the `Dockerfile`, after installing dependencies but before copying source code, add:

```dockerfile
RUN adduser --disabled-password --gecos "" appuser
USER appuser
```

This runs the process as a non-root user inside the container, which is a security best practice. Rebuild and confirm the app still starts correctly.

### 3. Health check

Add a health check to the `api` service in `docker-compose.yml`:

```yaml
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
```

Add a `/health` endpoint to the FastAPI app that returns `{"status": "ok"}`. Confirm `docker compose ps` shows the api service as healthy.

---

## Writing questions

Answer these in your `reflection.md`:

1. In your own words, explain the difference between an image and a container. Use an analogy.
2. Why does layer order matter in a Dockerfile? Give an example of a bad order and explain what goes wrong.
3. What is the difference between build-time configuration and run-time configuration? Give one example of each.
4. Why should secrets never be set using `ENV` in a Dockerfile?
5. What would happen to the ResearchOps database if you ran the API container without a volume mount, added 10 papers, then stopped and restarted the container?
