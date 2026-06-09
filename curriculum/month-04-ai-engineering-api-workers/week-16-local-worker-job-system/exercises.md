# Exercises - Week 16 Local Worker and Job System

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 16 — Local Worker & Job System](./README.md) › **exercises.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Beginner

1. **Model a job.** Define a `Job` dataclass with fields: `id: str`, `job_type: str`, `payload_json: str`, `status: str`, `attempts: int`, `last_error: str | None`, `created_at: str`, `updated_at: str`. Create three instances by hand with status `"pending"`. Print them.

2. **State transitions.** Write four functions: `mark_running(job: Job) -> Job`, `mark_succeeded(job: Job) -> Job`, `mark_failed(job: Job, error: str) -> Job`, `requeue(job: Job, error: str) -> Job`. Each should return a new `Job` with the status changed and `updated_at` refreshed. Write a test that chains: `pending → running → failed → pending (requeued)`.

3. **In-memory queue.** Implement an `InMemoryJobQueue` class with methods:
   - `enqueue(job_type: str, payload: dict) -> str` — adds a job, returns its ID.
   - `claim_next_pending() -> Job | None` — returns the oldest PENDING job and marks it RUNNING.
   - `mark_succeeded(job_id: str) -> None`
   - `mark_failed(job_id: str, error: str) -> None`
   Write tests that verify each method.

4. **Run worker once.** Write `run_worker_once(queue: InMemoryJobQueue, handlers: dict) -> None` that claims one job, calls the handler, and updates the status. Write a test with a `"noop"` handler that does nothing. Assert the job moves from PENDING to SUCCEEDED.

5. **Retry count.** Modify `run_worker_once` to accept `max_attempts: int = 3`. When a handler fails, increment `attempts` and requeue if `attempts < max_attempts`, otherwise mark FAILED permanently. Write a test that runs the worker three times on a failing job. Assert that after three attempts the job is FAILED and `attempts == 3`.

---

## Intermediate

1. **SQLite-backed job table.** Create the `jobs` table from notes.md in a SQLite database. Implement `SqliteJobQueue` with the same interface as `InMemoryJobQueue`. Use `INSERT OR REPLACE` to upsert job state. Write integration tests that create a queue, enqueue 3 jobs, run the worker until empty, and assert all jobs are SUCCEEDED.

2. **Atomic claim.** Implement `claim_next_pending` as an atomic SQLite operation: `SELECT ... WHERE status='pending' ORDER BY created_at LIMIT 1` followed immediately by `UPDATE ... SET status='running'` in the same transaction. This prevents two workers from claiming the same job. Write a test that confirms only one claim succeeds when two threads race.

3. **Handler registry.** Create a `HandlerRegistry` class that maps `job_type: str` to handler functions. Support `registry.register("fetch_url", handle_fetch)`. When the worker receives an unknown job type, it should mark the job FAILED with error `"no handler registered for type: {job_type}"`. Write tests for both known and unknown types.

4. **Idempotent document insert.** Write a handler `handle_index_document(payload: dict)` that indexes a document. Make it idempotent using upsert (SQLite `INSERT OR REPLACE`). Write a test that runs the handler twice on the same payload. Assert the document appears only once in the index and no exception is raised.

5. **Worker loop with stop signal.** Wrap `run_worker_once` in a loop: `def run_worker(queue, handlers, stop_event: threading.Event, sleep_seconds: float = 1.0)`. Poll until `stop_event.is_set()`. Write a test that enqueues 5 jobs, starts the worker in a thread, waits for all jobs to complete, then sets the stop event and joins the thread. Assert all 5 jobs are SUCCEEDED.

---

## Advanced

1. **Dead letter handling.** After a job permanently fails (exhausted retries), move it to a `dead_jobs` table instead of leaving it in `jobs`. Implement `SqliteJobQueue.archive_failed()` that moves all FAILED jobs to `dead_jobs`. Write an integration test that enqueues a job, runs the worker until it permanently fails, calls `archive_failed()`, and asserts the job is in `dead_jobs` and gone from `jobs`.

2. **Job inspection CLI.** Add a `jobs list` subcommand to the ResearchOps CLI that displays all jobs from the SQLite queue with their ID, type, status, attempts, and last update. Add `jobs show <job_id>` that prints all fields including `last_error` and `payload_json`. Write CLI tests using the existing test infrastructure.

3. **API + worker integration.** Add `POST /jobs/ingest` to the FastAPI app. It should create a PENDING job and return `{"job_id": "...", "status": "pending"}` with `201 Created`. Add `GET /jobs/{job_id}` that returns the current job status. Write an integration test that submits a job via the API, runs the worker once, then polls the API and asserts the status is `"succeeded"`.

4. **Scheduled backoff.** Modify the worker to wait before re-queuing a failed job: first retry waits 1 second (simulated with a `scheduled_at` timestamp in the job table), second waits 2 seconds, third waits 4 seconds. The worker only claims a job if its `scheduled_at` is in the past. Write tests using fake time (`unittest.mock.patch("datetime.datetime")`) to verify the scheduling without sleeping.

5. **Worker observability.** Add a `WorkerMetrics` class that the worker populates during a run: `jobs_succeeded`, `jobs_failed`, `jobs_requeued`, `total_runtime_seconds`. After each worker run, log the metrics using `logging.info`. Write a test that runs the worker on a mixed batch (2 succeed, 1 fails permanently, 1 is retried) and asserts the metric counts are correct.

---

## Brutal

1. **Crash recovery audit.** Simulate a worker crash at each stage of the worker loop:
   - After `claim_next_pending` but before `mark_running`.
   - After `mark_running` but before the handler runs.
   - After the handler runs but before `mark_succeeded`.
   For each crash scenario, write a test that creates a new worker, starts it, and verifies the job eventually reaches SUCCEEDED or FAILED correctly. This tests your recovery logic for stuck RUNNING jobs (hint: add a `claim_stuck_running` method that rescues jobs stuck in RUNNING for more than N seconds).

2. **Concurrent workers.** Run two `SqliteJobQueue` workers in separate threads simultaneously. Enqueue 20 jobs. Wait for all to complete. Assert every job is SUCCEEDED exactly once and no job was run twice. The atomicity of `claim_next_pending` is critical here. Use SQLite's WAL mode for better concurrency: `PRAGMA journal_mode=WAL`.

3. **Full pipeline via jobs.** Wire the complete Week 13–15 pipeline through the job system. Define three job types: `"fetch_url"`, `"parse_document"`, `"index_document"`. Each handler calls the appropriate service. Implement a submit function that chains them: submitting a URL creates a `fetch_url` job; when it succeeds, its completion handler enqueues a `parse_document` job; and so on. Write an integration test for the full chain.

4. **Job payload validation.** Add Pydantic model validation to each handler's payload. If `json.loads(payload_json)` succeeds but the data does not match the expected schema, mark the job FAILED immediately with a validation error and do not retry (it is a configuration bug, not a transient failure). Write tests for both valid and invalid payloads.

5. **Benchmark and capacity planning.** Write a benchmark that enqueues 1 000 jobs and runs the worker. Measure total time and jobs per second. Try three storage backends: in-memory dict, SQLite without WAL, SQLite with WAL. Document the results in a table. Estimate how long it would take to process 100 000 jobs at each throughput level. This is basic capacity planning — a skill every backend engineer needs.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 16 — Local Worker & Job System** · *exercises.md — the workbook* (step 3 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [notes.md](./notes.md)
- ▶ **Next:** [break_it.md](./break_it.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. **➡ [exercises.md](./exercises.md) ← you are here**
4. [break_it.md](./break_it.md)
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
