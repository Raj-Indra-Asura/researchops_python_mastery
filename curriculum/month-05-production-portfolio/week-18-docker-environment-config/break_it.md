# Break It - Week 18 Docker and Environment Configuration

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › [Week 18 — Docker & Environment Config](./README.md) › **break_it.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Why break it?

Docker and configuration failures in production are often silent and hard to diagnose. This section gives you controlled experience with the exact failures you will encounter. Each experiment has a specific lesson.

---

## Experiment 1: Build without copying a required directory

Remove the `COPY src ./src` line from your `Dockerfile`. Build the image. Run:

```bash
docker run researchops:local researchops --help
```

**What you will see**: a `ModuleNotFoundError` or `ImportError`. The package is installed (via `pyproject.toml`) but the source code is not present because you did not copy it.

**What to learn**: `pip install -e .` installs the package in editable mode, which means it relies on the source directory being present. If the source directory is missing, imports fail. For production images, use a regular install (not editable) and verify by running a smoke test in the `RUN` layer:

```dockerfile
RUN pip install . && python -c "import researchops; print('OK')"
```

---

## Experiment 2: Set a required env var to an invalid value

Set `DATABASE_URL` to a value with a typo or invalid path:

```bash
docker run -e DATABASE_URL=not-a-valid-url researchops:local researchops --help
```

**What you will see**: either the app crashes at startup with a configuration error (if you validate settings early), or it crashes later when the first database operation runs.

**What to learn**: configuration errors should be caught early — at application startup — not deep inside a business operation. Add a validation step in `Settings` or at startup that raises a descriptive error for clearly invalid values.

---

## Experiment 3: Accidentally commit a fake secret

Add a fake key to `.env.example`:

```bash
OPENAI_API_KEY=sk-fake1234567890abcdef
```

Commit it. Now reflect: if this were a real key, it would be permanently in the git history, even after you remove it in the next commit. Any automated GitHub scanner would extract it within minutes.

Then immediately:
1. Remove the value.
2. Replace with `OPENAI_API_KEY=` (empty, showing the variable name without a value).
3. Commit the fix.

**What to learn**: treat `.env.example` values with care. Even "obviously fake" values train bad habits. Use empty strings or descriptive placeholders like `your-api-key-here`.

---

## Experiment 4: Wrong container command

In `docker-compose.yml`, change the `api` service command to:

```yaml
    command: researchops.api.main:app --host 0.0.0.0 --port 8000
```

(missing the `uvicorn` prefix)

Run `docker compose up api`. The container will start and then immediately exit.

**What to see**: `docker compose logs api` will show a `command not found` or `No such file or directory` error.

**What to learn**: always check the container exit code with `docker compose ps`. Exit code 0 means clean exit; anything else is an error. `docker compose logs SERVICE` is the first debugging tool.

---

## Experiment 5: Run the compose without a data volume mount

Remove the volumes section from the `api` service:

```yaml
  api:
    build: .
    command: uvicorn researchops.api.main:app --host 0.0.0.0 --port 8000
    env_file:
      - .env
    ports:
      - "8000:8000"
    # volumes section removed
```

Start the API, ingest a few papers via the API or CLI, then stop the container with `docker compose down`. Start it again. Check whether the papers are still there.

**What you will see**: the papers are gone. The SQLite database was created inside the container's writable layer, which was discarded when the container stopped.

**What to learn**: anything that must persist must be in a volume. This is one of the most common causes of "why did all my data disappear?" in containerised apps.

---

## Experiment 6: Fresh clone failure (the full environment test)

Clone your repository to a new directory (or ask a friend to clone it):

```bash
cd /tmp
git clone <your-repo-url> freshtest
cd freshtest
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

Without creating a `.env` file, run:

```bash
researchops --help
```

**What might fail**:
- If the app tries to read a required env var at import time, it fails before printing help.
- If `DATABASE_URL` has no default, the app might crash on the first database operation.

**What to learn**: verify that `researchops --help` works with no `.env` file present and no environment variables set. Defaults must be safe and the app must not crash on startup just because optional variables are not set.

---

## Experiment 7: Missing env var for a required secret

If you have an `OpenAIGenerator` class, run the API service with `OPENAI_API_KEY` explicitly unset:

```bash
docker run -e OPENAI_API_KEY= researchops:local python -c "from researchops.rag.generator import OpenAIGenerator; OpenAIGenerator()"
```

**What to see**: either a runtime error from the OpenAI client (if it validates eagerly) or no error at construction time but a failure at the first API call.

**What to fix**: add an eager check at `OpenAIGenerator.__init__` that raises `EnvironmentError` with a clear message if the key is empty or missing.

---

## Experiment 8: Broken compose service dependency

If your `worker` service depends on the `api` service being healthy (or the database file existing), remove the volume mount from `api` but keep it on `worker`. Start both:

```bash
docker compose up api worker
```

The worker may crash because it cannot find the database that the API is supposed to create.

**What to learn**: in multi-service setups, services often depend on shared state. Volume configuration inconsistencies between services produce subtle, hard-to-debug failures. Always use the same volume definition for all services that share data.

---

## Debugging commands reference

```bash
# Show running and stopped containers
docker compose ps

# Show logs from a specific service
docker compose logs api

# Follow logs in real time
docker compose logs api -f

# Get a shell inside a running container
docker compose exec api bash

# Inspect a container's environment variables (be careful: may show secrets)
docker inspect CONTAINER_ID | grep -A 20 '"Env"'

# Check which files are in the container
docker run --entrypoint ls researchops:local /app/src/researchops

# Check the image size
docker images researchops
```

---

## Edge cases to handle explicitly

| Case | Expected behaviour |
|---|---|
| `.env` file missing at compose startup | Use defaults; do not crash if defaults are safe |
| `DATABASE_URL` points to a path that does not exist | Create the directory or raise a clear startup error |
| Port 8000 already in use on the host | `docker compose up` reports `bind: address already in use`; document this in README |
| Container runs out of disk space | Fails with `No space left on device`; keep images clean with `.dockerignore` |
| Volume mounted to a read-only path | Write operations fail at runtime, not at build time |

---

## What did you learn?

Answer these in your `reflection.md` after completing the experiments:

1. Which config mistake was hardest to diagnose from the logs?
2. What would be the consequences of accidentally committing a real secret?
3. What should never be set using `ENV` in a Dockerfile?
4. How will you document the required runtime environment for a new developer joining the project?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 18 — Docker & Environment Config** · *break_it.md — the failure lab* (step 4 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [exercises.md](./exercises.md)
- ▶ **Next:** [validation.md](./validation.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. **➡ [break_it.md](./break_it.md) ← you are here**
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 19](../../../curriculum/month-05-production-portfolio/week-19-documentation-portfolio-polish/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 19 — Documentation & Portfolio Polish](../../../curriculum/month-05-production-portfolio/week-19-documentation-portfolio-polish/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 5 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 5 overview](../README.md) · [📄 Week 18 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
