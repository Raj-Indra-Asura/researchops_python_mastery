# Validation — Week 16 Local Worker and Job System

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 16 — Local Worker & Job System](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 16 — Local Worker & Job System** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 17](../../../curriculum/month-05-production-portfolio/week-17-rag-assistant/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 17 — RAG Assistant](../../../curriculum/month-05-production-portfolio/week-17-rag-assistant/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 4 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 4 overview](../README.md) · [📄 Week 16 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
