# Break It - Week 16 Local Worker and Job System

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 16 — Local Worker & Job System](./README.md) › **break_it.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Intentional failure experiments

### 1. Non-atomic claim
Implement `claim_next_pending` as two separate database calls: SELECT (to find the job) and UPDATE (to mark it running), without wrapping them in a transaction. Start two worker threads. Both may SELECT the same job before either one runs the UPDATE. Both workers run the same job. Observe duplicate processing. Fix: use a single `UPDATE ... WHERE status='pending' ... RETURNING *` or wrap SELECT+UPDATE in `BEGIN IMMEDIATE` / `COMMIT`.

### 2. Crash after marking running
Simulate a worker that marks a job RUNNING and then raises an exception before completing. Restart the worker. The job stays RUNNING forever. Add a `rescue_stuck_jobs(timeout_seconds: int = 300)` method to your queue that finds jobs in RUNNING status with `updated_at` older than the timeout and resets them to PENDING. Write a test that simulates a stuck job and calls `rescue_stuck_jobs`.

### 3. Non-idempotent handler
Write a handler that always appends a new row to the database (no upsert). Run the same job twice. Observe two identical rows. Fix: use `INSERT OR REPLACE` or check for existence first. Write a test that runs the handler twice and asserts exactly one row exists.

### 4. Unknown job type
Enqueue a job with `job_type="does_not_exist"`. Run the worker. Without a guard, you get a `KeyError` or silent crash. Add explicit handling: if no handler is registered, mark the job FAILED with `"unknown job type: does_not_exist"` and do not retry. Write a test that confirms the job is FAILED after one attempt and `attempts == 1`.

### 5. Infinite retries
Set `max_attempts=999999` and have the handler always fail. Without a time limit or iteration limit in your test, the worker loops forever. Add a safeguard: in tests, limit the worker to `max_iterations=10`. In production, keep `max_attempts` bounded (3–5 is standard). Write a test that confirms the worker exits the loop after the configured limit.

### 6. Corrupt payload JSON
Insert a job with `payload_json = "this is not json"` directly into the database. Run the worker. `json.loads` raises `json.JSONDecodeError`. Without handling this, the worker crashes. Add a try/except around `json.loads` that marks the job FAILED with `"invalid JSON payload"` without retrying (this is a data bug, not transient). Write a test.

### 7. Status not updated on exception
Remove `mark_failed` from the except block. Run the worker on a failing job. The job stays RUNNING after the handler raises. It never gets retried or resolved. Observe this, then put `mark_failed` back. Write a test that confirms `mark_failed` is called even when the handler raises.

### 8. Retry a 404 fetch job
Have a `fetch_url` handler that raises `httpx.HTTPStatusError` with status 404. In your retry logic, treat this as a retryable error (mistake). The worker retries 3 times. All fail. Write the correct version: check the status code in the except block and mark 404 jobs FAILED immediately without retrying.

### 9. Job enqueued twice
Submit the same logical job twice — for example, indexing the same document ID. Without deduplication, the worker runs the handler twice. Whether this is a problem depends on idempotency. Write a test that enqueues the same document ID twice, runs the worker to completion, and asserts the document appears only once in the index (assuming an idempotent handler). Then disable idempotency and observe what breaks.

---

## Debugging tasks

- Add `logging.info(f"Job {job.id} status → {new_status}")` at every status transition. Run the worker on 5 jobs and read the log to trace each job's lifecycle.
- When a job is stuck in RUNNING, print `jobs WHERE status='running' AND updated_at < now - 60 seconds` using SQLite CLI to identify it manually.
- Run `pytest tests/unit/test_job_states.py -v` and inspect failure output when you intentionally break a state transition.
- Print `queue.get_counts_by_status()` (implement this as a debugging utility) after each worker iteration to observe the queue draining.

---

## Edge cases to explore

| Case | Expected behaviour |
|------|-------------------|
| Empty queue | Worker sleeps and polls; does not crash |
| All jobs already SUCCEEDED | Worker finds nothing, sleeps, loops |
| Job with empty payload `{}` | Handler receives empty dict; define whether it's valid per type |
| Job type registered but handler raises `SystemExit` | Do not catch `SystemExit` or `KeyboardInterrupt` in the except block — let them propagate |
| `max_attempts = 1` | No retries — one failure and the job is permanently FAILED |
| Worker stopped mid-batch | Jobs in RUNNING state need rescue on restart |

---

## What did you learn?

- What was the hardest state transition to get right?
- Which assumption about atomicity did you make that turned out to be wrong?
- How did writing the crash-recovery test change the way you structured the worker loop?
- Why is idempotency not just a nice-to-have but a correctness requirement?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 16 — Local Worker & Job System** · *break_it.md — the failure lab* (step 4 of 6 this week).

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
