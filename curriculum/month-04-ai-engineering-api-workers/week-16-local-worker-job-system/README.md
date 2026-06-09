# Week 16 — Local Worker and Job System

> **Chapter title: "Work that happens in the background."**
> The week ResearchOps learns to do long jobs without making anyone wait — and to
> survive a crash mid-job.

---

## 1. Week title

Week 16 — Local Worker and Job System (Month 4, Chapter 4 of 4 — month finale).

## 2. Story of the week

Some work is too long for a request or a single CLI call: ingesting a thousand
papers, embedding a whole corpus, fetching hundreds of URLs. This week you build a
**job system** so that work can be *submitted* now and *executed* later by a
background worker. You model a job as a small **state machine** (pending → running
→ done / failed), persist the queue in SQLite, and write a worker loop that polls,
claims, executes, and updates state. The hard, important parts are **retries**,
**idempotency** (a retried job must not double-apply its effect), and **crash
recovery** without corrupting data.

## 3. What you already know

- From Week 15: async I/O, timeouts, retries, and partial-failure handling.
- From Week 5: SQLite and the repository pattern.
- From Month 3: protocols, fakes, and unit testing state transitions.

You have not yet built a persistent queue, a worker loop, or idempotent handlers.

## 4. What this week adds

- A **job state machine**: pending → running → done / failed.
- A **persistent job queue** in SQLite (`JobRepository`).
- A **worker loop**: poll → claim → execute → update state.
- **Retry logic** and **idempotency**.
- **Worker failure recovery** without data corruption.
- `JobService` (submission/management) and `JobRepository` (persistence).

## 5. Why this week matters

Background processing is the backbone of every real platform, and it forces you to
confront failure as a first-class concern. A naive worker that retries a
non-idempotent job will double-charge, double-insert, or double-send. A worker that
crashes mid-job and leaves a row stuck in "running" forever will silently stall the
queue. Designing for *retries* and *crash recovery* now is what separates a toy
queue from a dependable one — and the discipline carries straight into production
systems.

## 6. Learning objectives

By the end of the week you can:

- Implement a job state machine with explicit, legal transitions.
- Persist a job queue in SQLite behind a repository.
- Build a polling worker loop that claims and executes jobs.
- Design idempotent handlers safe to retry.
- Recover from a mid-job crash without corrupting state or losing the error.
- Test state transitions with a fake repository.

## 7. Project milestone

`researchops jobs run` starts a worker that processes jobs from the queue, and
`researchops jobs list` shows job states.

## 8. Files / modules touched

- `src/researchops/storage/job_repository.py` — persistent queue (`JobRepository`).
- `src/researchops/services/job_service.py` — submission and management.
- `src/researchops/workers/job_runner.py` — the worker loop.
- `src/researchops/cli/commands/ingest.py` — `jobs list`, `jobs run`, `jobs retry`.

## 9. Commands introduced

```bash
researchops jobs list      # show jobs and their states
researchops jobs run        # start a worker that drains the queue
researchops jobs retry <id> # re-enqueue a failed job
```

## 10. Tests involved

- `tests/unit/test_job_service.py` — state transitions with a fake repository.
- `tests/integration/test_job_repository.py` — persistence against a real
  (tmp) DB.

```bash
pytest tests/unit/test_job_service.py -v
```

## 11. Study plan for the week

1. **Day 1 — State machine.** Define states and legal transitions; reject illegal
   ones (e.g. done → running).
2. **Day 2 — JobRepository.** Persist jobs in SQLite; claim a job atomically so two
   workers cannot grab the same one.
3. **Day 3 — Worker loop.** poll → claim → execute → update; mark failures with
   their error.
4. **Day 4 — Retries + idempotency.** Add retry counts; make a handler safe to run
   twice; think through crash-in-the-middle.
5. **Day 5 — Tests + CLI + month report.**

## 12. Estimated time breakdown

| Activity | Time |
|---|---|
| Reading + state-machine design | ~2 hrs |
| JobRepository + claiming | ~2.5 hrs |
| Worker loop | ~2 hrs |
| Retries, idempotency, recovery | ~2.5 hrs |
| Tests + month report | ~1.5 hrs |

## 13. How to know the learner is stuck

- A job can move between states with no rules (e.g. failed → done directly).
- A crashed worker leaves a job stuck in "running" forever.
- Retrying a job applies its effect twice (not idempotent).
- A failed job's error is discarded, so you cannot tell why it failed.

## 14. Definition of done

- [ ] Job states and legal transitions are explicit.
- [ ] The queue is persisted in SQLite via `JobRepository`.
- [ ] The worker loop claims, executes, and updates jobs.
- [ ] Retry is bounded and recorded; the failure reason is stored.
- [ ] Handlers are idempotent (documented and tested).
- [ ] A mid-job crash leaves recoverable state, not corruption.
- [ ] `jobs list` / `jobs run` / `jobs retry` work; unit tests pass.

## 15. Ruthless mentor checkpoint

- "Walk me through what happens if the worker is killed *during* a running job.
  Where does that job end up, and can it be retried safely?"
- "Show me the idempotency reasoning for one handler. If it runs twice, what is the
  net effect?"
- "Force a job to fail. Can I read *why* it failed from the job record?"

If retries are not idempotent or failures are silent, you are not done.

## 16. What not to do this week

- Do **not** allow retries without thinking through idempotency.
- Do **not** discard a failed job's error — persist it.
- Do **not** let two workers claim the same job (claim atomically).
- Do **not** leave a state machine with undefined/illegal transitions.

## 17. Bridge to next week

Month 4 is complete: ResearchOps can retrieve semantically, serve over HTTP, fetch
asynchronously, and run long work as background jobs. You now have every piece a
RAG assistant needs — retrieval, services, and async/background execution.
**Week 17** opens Month 5 by combining retrieval with generation into a **RAG
assistant** that answers questions **with citations**, controls hallucination, and
stays fully testable with a fake generator (no real LLM required).
