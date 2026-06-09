# Validation — Week 16 Local Worker and Job System

## 1. Pre-validation checklist

- [ ] `.[dev,storage]` is installed in an active virtual environment.
- [ ] Job states and legal transitions are explicit.
- [ ] Every job handler has been reasoned about for **idempotency**.
- [ ] Failed jobs persist their **error reason**.

## 2. Exact commands

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,storage]"
ruff check src tests
pytest tests/unit/test_job_service.py -v
pytest tests/integration/test_job_repository.py -v
pytest -q
```

## 3. Expected behavior

- Jobs move through `pending → running → done / failed` with no illegal
  transitions.
- The worker loop claims and processes queued jobs; retries are bounded.
- A retried job does not double-apply its effect; a failed job records why.

## 4. Tests that must pass

- `tests/unit/test_job_service.py` (state transitions with a fake repo)
- `tests/integration/test_job_repository.py` (persistence)
- `pytest -q` (whole suite)

## 5. Manual checks

- `researchops jobs run` drains the queue; `researchops jobs list` shows states.
- Force a job to fail; confirm `jobs list` shows it failed *with a reason*.
- `researchops jobs retry <id>`; confirm a safe re-run.

## 6. Architecture checks

- `JobRepository` hides SQL; `JobService` depends on the repository protocol.
- Job claiming is atomic so two workers cannot grab the same job.

## 7. Documentation checks

- `notes.md` documents the state machine and the idempotency rule for each handler.

## 8. Do-not-proceed warnings

**Do not proceed to Week 17 if:**

- **Jobs can be retried without idempotency thinking** — a retried job must not
  double-apply effects.
- **Failed job errors are discarded** — the failure reason must be persisted and
  visible.

## 9. Ruthless mentor checkpoint

- "If the worker is killed mid-job, where does that job end up, and can it be
  retried safely?"
- "Walk me through the idempotency of one handler: if it runs twice, what is the
  net effect?"
- "Force a failure. Can I read *why* it failed from the job record?"

## 10. Definition of done

- [ ] Job states and legal transitions are explicit and enforced.
- [ ] The queue is persisted via `JobRepository`; claiming is atomic.
- [ ] The worker loop claims, executes, and updates jobs.
- [ ] Retries are bounded and idempotent; failure reasons are stored.
- [ ] A mid-job crash leaves recoverable (not corrupt) state.
- [ ] Unit + integration tests pass; `pytest -q` passes; `ruff` clean.
- [ ] You can explain how duplicate work is prevented.
