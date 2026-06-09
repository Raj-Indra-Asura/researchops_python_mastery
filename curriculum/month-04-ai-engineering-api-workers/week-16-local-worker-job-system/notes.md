# Notes - Week 16 Local Worker and Job System

## Why long-running tasks need a job system

When a user triggers an action in a CLI or API, the response must come back quickly. A user waiting 30 seconds for a command to return is a bad experience. An API that keeps a request open for 5 minutes will time out.

But some tasks genuinely take a long time:
- Fetching 100 remote PDFs over HTTP
- Embedding 10 000 chunks with a local model
- Parsing a large batch of documents

The solution is to separate submission from execution. The user submits a job. The submission is instant. A background worker picks up the job and runs it later. The user can check the job status when they want.

This is the core idea behind job queues, task queues, and message brokers (Celery, SQS, RQ, Temporal). They all implement the same mental model, just at different scales. This week you build the same pattern locally with SQLite.

---

## Jobs, queues, and workers — from first principles

### A job

A job is a unit of deferred work. It has:

- **ID** — a unique identifier so you can look it up later.
- **Type** — what kind of work to do. For example, `"ingest_document"` or `"embed_chunk_batch"`.
- **Payload** — the data the handler needs. Stored as JSON.
- **Status** — where the job is in its lifecycle.
- **Attempts** — how many times it has been tried.
- **Last error** — what went wrong on the most recent failure.
- **Timestamps** — when it was created and last updated.

### A queue

A queue is a storage layer for jobs. Its responsibilities:
- Accept new jobs (enqueue).
- Hand the next job to a worker (dequeue/claim).
- Update job status.
- Report job counts by status.

### A worker

A worker is a loop that repeatedly:
1. Asks the queue for the next available job.
2. Marks it as running.
3. Calls the appropriate handler for that job type.
4. Marks it as succeeded or failed.
5. Waits briefly (polling) before checking again.

---

## The SQLite job table

Storing jobs in SQLite is enough for local development and small-scale production. Here is the schema:

```sql
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    job_type TEXT NOT NULL,
    status TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

Line by line:

`id TEXT PRIMARY KEY` — each job gets a unique identifier, typically a UUID. Using `TEXT` instead of `INTEGER` avoids coordination problems if you ever run multiple inserters.

`job_type TEXT NOT NULL` — a string name for the job type. The worker uses this to look up the right handler. Examples: `"fetch_url"`, `"index_document"`, `"send_summary_email"`.

`status TEXT NOT NULL` — the current lifecycle state. Must be one of a fixed set of values (enforced in application code or via a CHECK constraint).

`payload_json TEXT NOT NULL` — the job's input data, JSON-serialised. Python dict → `json.dumps()` on insert, `json.loads()` on read. Storing as TEXT keeps the schema simple and portable.

`attempts INTEGER NOT NULL DEFAULT 0` — how many times execution has been attempted. Incremented each time the worker tries the job. Used by retry logic to decide when to give up.

`last_error TEXT` — nullable. Contains the error message (or stack trace excerpt) from the most recent failure. Invaluable for debugging.

`created_at TEXT NOT NULL` — ISO 8601 timestamp when the job was inserted. Example: `"2026-06-09T10:30:00Z"`.

`updated_at TEXT NOT NULL` — ISO 8601 timestamp of the most recent status change. Useful for detecting stuck jobs.

---

## Job status lifecycle

```
PENDING → RUNNING → SUCCEEDED
                  ↘ FAILED → RETRIED → RUNNING → ...
                                     ↘ FAILED (permanently)
```

**PENDING** (also called QUEUED): job has been submitted and is waiting for a worker.

**RUNNING**: a worker has claimed the job and is executing it.

**SUCCEEDED**: the handler completed without exception.

**FAILED**: the handler raised an exception. If `attempts < max_attempts`, the status may move back to PENDING for a retry.

**RETRIED**: a transient state indicating the job will be re-queued. Some systems skip this and move directly back to PENDING.

Status transitions must be explicit. Never update the status outside the queue layer. This ensures consistency and makes the transitions testable.

---

## The worker polling loop

The worker is a loop. Here is pseudo-code with full explanation:

```python
def run_worker(queue: JobQueue, handlers: dict, max_attempts: int = 3) -> None:
    while True:                                          # (1)
        job = queue.claim_next_pending()                 # (2)
        if job is None:                                  # (3)
            time.sleep(1)                               # (4)
            continue                                    # (5)
        queue.mark_running(job.id)                      # (6)
        try:
            handler = handlers[job.job_type]            # (7)
            payload = json.loads(job.payload_json)      # (8)
            handler(payload)                            # (9)
            queue.mark_succeeded(job.id)                # (10)
        except KeyError:                                # (11)
            queue.mark_failed(job.id, "unknown job type")  # (12)
        except Exception as exc:                        # (13)
            new_attempts = job.attempts + 1             # (14)
            if new_attempts < max_attempts:             # (15)
                queue.requeue(job.id, str(exc))         # (16)
            else:
                queue.mark_failed(job.id, str(exc))     # (17)
```

(1) Loop forever. A real worker runs until stopped by a signal.

(2) Ask the queue for the next PENDING job. This should be atomic (SELECT + UPDATE in a single transaction) so two workers cannot claim the same job.

(3) If no job is available, the queue is empty.

(4) Sleep briefly before polling again. Without this, the worker hammers the database with queries when idle.

(5) `continue` skips the rest of the loop body and polls again.

(6) Mark the job as RUNNING before executing. If the worker crashes after this, the job stays RUNNING indefinitely — this is a "stuck job". Production systems detect stuck jobs by checking `updated_at`.

(7) Look up the handler function for this job type. Raises `KeyError` if unknown.

(8) Deserialise the JSON payload into a Python dict.

(9) Execute the handler. This is where the real work happens: fetching, parsing, indexing.

(10) If the handler returns without raising, mark the job SUCCEEDED.

(11) Unknown job type — no handler registered.

(12) Mark failed with a descriptive error. Do not retry unknown types.

(13) Any other exception — a real failure.

(14) Increment the attempt count.

(15) Check whether we have more attempts remaining.

(16) `requeue` increments `attempts`, stores the error in `last_error`, and sets status back to PENDING. The job will be picked up again.

(17) Exceeded retry limit. Mark permanently failed.

---

## Idempotency

Idempotency means: running the same operation more than once produces the same result as running it once.

Why it matters for jobs: if a worker crashes after completing the work but before marking the job SUCCEEDED, the job will be retried. The handler runs again. If the handler is not idempotent, it may create duplicate records, send duplicate emails, or corrupt state.

**Non-idempotent (dangerous):**
```python
def handle_index_document(payload: dict) -> None:
    doc = parse(payload["text"])
    db.insert_document(doc)   # will fail or duplicate if called twice
```

**Idempotent (safe):**
```python
def handle_index_document(payload: dict) -> None:
    doc = parse(payload["text"])
    db.upsert_document(doc)   # insert or update, safe to call twice
```

Use `INSERT OR REPLACE` or `INSERT ... ON CONFLICT DO UPDATE` in SQLite for idempotent inserts.

Alternatively, check first:
```python
if not db.document_exists(doc.id):
    db.insert_document(doc)
```

A simpler approach: store the document's content hash in the job payload. Before inserting, check if a document with that hash already exists. If yes, skip the insert.

---

## Poison jobs

A poison job is a job that consistently fails, exhausts its retry limit, and stays in FAILED state permanently. Left unchecked, poison jobs accumulate and pollute your job table.

Handling poison jobs:
1. Set a clear `max_attempts` limit (e.g., 3).
2. Store the full error in `last_error` for diagnosis.
3. Provide a CLI command to list and inspect FAILED jobs.
4. Allow manual re-queuing after a human investigates and fixes the root cause.
5. Optionally, move permanently-failed jobs to a dead-letter table for archival.

---

## Why workers call services, not raw storage

A worker's handler should call the application service layer, not query the database directly.

**Wrong:**
```python
def handle_embed(payload: dict) -> None:
    conn = sqlite3.connect("data.db")
    chunks = conn.execute("SELECT ...").fetchall()
    # embed and insert directly
```

**Right:**
```python
def handle_embed(payload: dict) -> None:
    service = build_embedding_service()
    service.embed_document(payload["document_id"])
```

This keeps the worker as a thin dispatcher, just like route handlers. The service layer contains business logic. The worker just orchestrates: claim job, call service, update status.

---

## API + worker: the standard pattern

A common production pattern:

1. User sends `POST /jobs/ingest` with a document URL.
2. The API creates a PENDING job in the database and returns `{"job_id": "abc123"}` with `201 Created`.
3. The background worker polls, finds the job, and fetches and indexes the document.
4. The user polls `GET /jobs/abc123` and eventually sees `{"status": "succeeded"}`.

The API is never blocked waiting for the document to be indexed. The user gets instant feedback. The worker does the real work asynchronously.

This pattern prepares you for production: replicate the worker, use a proper queue (Redis, SQS), and the architecture scales horizontally.

---

## Testing a job system

Unit tests should focus on state transitions:

```python
def test_successful_job() -> None:
    queue = InMemoryJobQueue()
    job_id = queue.enqueue("noop", {"value": 1})
    assert queue.get_status(job_id) == "pending"
    
    run_worker_once(queue, handlers={"noop": lambda p: None})
    
    assert queue.get_status(job_id) == "succeeded"


def test_failed_job_retries() -> None:
    queue = InMemoryJobQueue()
    job_id = queue.enqueue("fail", {})

    def always_fail(payload: dict) -> None:
        raise RuntimeError("boom")

    run_worker_once(queue, handlers={"fail": always_fail})
    assert queue.get_status(job_id) == "pending"  # re-queued for retry
    assert queue.get_attempts(job_id) == 1
```

Use an in-memory queue implementation for unit tests. This avoids the database and keeps tests fast. The in-memory implementation should satisfy the same interface as the SQLite-backed queue.

---

## Summary

- Long-running work should not block the API or CLI — use a job system.
- A job has ID, type, status, payload, attempts, error, and timestamps.
- The SQLite schema stores everything needed to run, retry, and inspect jobs.
- Status transitions are explicit: PENDING → RUNNING → SUCCEEDED or FAILED.
- The worker polling loop claims, executes, and updates status.
- Polling with a small sleep prevents wasted database queries when idle.
- Idempotency means handlers are safe to run more than once.
- Use upsert logic or existence checks to make handlers idempotent.
- Poison jobs exhaust retries; store the error and provide manual inspection tools.
- Workers call services, not raw storage — the same rule as route handlers.
- The API + worker pattern is the standard production model for async work.
- Test with an in-memory queue for fast, isolated state-transition tests.
