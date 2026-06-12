
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 16 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 16 — Local Worker Job System:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation — Week 16 Local Worker and Job System

## Pre-validation checklist

- [ ] `.[dev,storage]` is installed in an active virtual environment.
- [ ] Job states and legal transitions are explicit.
- [ ] Every job handler has been reasoned about for **idempotency**.
- [ ] Failed jobs persist their **error reason**.

## Commands to run

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,storage]"
ruff check src tests
pytest tests/unit/test_job_service.py -v
pytest tests/integration/test_job_repository.py -v
pytest -q
```

## Expected outputs

Expected output should prove persistence, safe state transitions, and recoverable failure handling. A worker that only prints something is not enough; the job rows must change correctly.

- `source .venv/bin/activate` prints nothing, except possibly a changed shell prompt.
- `python -m pip install -e ".[dev,storage]"` ends successfully and provides the SQLite/storage dependencies already used by the project.
- `ruff check src tests` ends with `All checks passed!`. Repository SQL code, worker code, and tests must all be lint-clean.
- `pytest tests/unit/test_job_service.py -v` shows service-level tests as `PASSED`: enqueue, run-one-job, success, unknown job type, invalid JSON, retry, attempts exhausted, and graceful no-job behavior.
- `pytest tests/integration/test_job_repository.py -v` shows SQLite persistence tests as `PASSED`: insert, claim oldest eligible queued job, mark done, retry/fail, list jobs, and stuck-job rescue if implemented.
- `pytest -q` finishes with a green summary such as `... passed`. The suite must not hang in an infinite worker loop.

Behavior you should be able to observe after the commands pass:

- Jobs move through `queued → running → done` or `queued → running → failed` with no illegal transitions.
- Retryable failures increment attempts, reschedule the job, and eventually stop at `max_attempts`.
- A retried handler does not double-apply its effect; a failed job stores a human-readable `last_error`.
- Manual `researchops jobs list` output shows enough status and error information for a beginner to debug a stuck or failed job.

## Tests that must pass

- `tests/unit/test_job_service.py` (state transitions with a fake repo)
- `tests/integration/test_job_repository.py` (persistence)
- `pytest -q` (whole suite)

## Manual checks

- `researchops jobs run` drains the queue; `researchops jobs list` shows states.
- Force a job to fail; confirm `jobs list` shows it failed *with a reason*.
- `researchops jobs retry <id>`; confirm a safe re-run.

## Architecture checks

- `JobRepository` hides SQL; `JobService` depends on the repository protocol.
- Job claiming is atomic so two workers cannot grab the same job.

## Documentation checks

- `notes.md` documents the state machine and the idempotency rule for each handler.

## Do-not-proceed warnings

**Do not proceed to Week 17 if:**

- **Jobs can be retried without idempotency thinking** — a retried job must not
  double-apply effects.
- **Failed job errors are discarded** — the failure reason must be persisted and
  visible.
- Claiming a job is a plain `SELECT` followed later by an `UPDATE`; two workers could process the same row.
- The worker loop cannot be run for exactly one iteration in a test, or the test suite can hang.
- Unknown job types or invalid JSON crash the worker process instead of failing the specific job row.

## Ruthless mentor checkpoint

- "If the worker is killed mid-job, where does that job end up, and can it be
  retried safely?"
- "Walk me through the idempotency of one handler: if it runs twice, what is the
  net effect?"
- "Force a failure. Can I read *why* it failed from the job record?"

## Definition of done

- [ ] Job states and legal transitions are explicit and enforced.
- [ ] The queue is persisted via `JobRepository`; claiming is atomic.
- [ ] The worker loop claims, executes, and updates jobs.
- [ ] Retries are bounded and idempotent; failure reasons are stored.
- [ ] A mid-job crash leaves recoverable (not corrupt) state.
- [ ] Unit + integration tests pass; `pytest -q` passes; `ruff` clean.
- [ ] You can explain how duplicate work is prevented.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 16 — Local Worker Job System:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
