<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 16 — Local Worker Job System:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 16 Local Worker and Job System

This is one unified chapter. There is no short version followed by a second older version.
Read it as a textbook chapter, then use the workbook, failure lab, validation checklist, and reflection prompts.

## Chapter overview
Week 16 teaches ResearchOps how to do work after the user has already asked for it.
The central idea is a local background job system.
A background job system lets the CLI or API accept a request quickly and finish the slow part later.
In ResearchOps, slow work includes ingesting papers, parsing files, computing embeddings, and updating search indexes.
This week does not teach cloud queues, Docker, distributed workers, RAG, or LLM calls.
Those ideas belong to later weeks.
This week stays local, inspectable, and beginner-friendly.
The queue is persisted in SQLite so a learner can open the database and see the job rows directly.
The worker process polls the database, claims one job, runs the matching handler, and records the result.
The worker is intentionally boring.
Boring infrastructure is easier to debug than clever infrastructure.
A job has a type, a payload, a status, an attempt count, timestamps, and an optional error message.
A job type answers: what kind of work should happen?
A payload answers: what exact input should the worker use?
A status answers: where is this job in its lifecycle?
Attempts answer: how many times have we tried to do this work?
The error message answers: why did the latest attempt fail?
Timestamps answer: when was the job created, claimed, updated, or scheduled for retry?
The chapter milestone is a local command such as `researchops jobs run` that starts the worker loop.
A companion command such as `researchops jobs list` shows queued, running, done, and failed jobs.
The learner should finish this chapter able to explain every state transition without hand-waving.
The learner should also be able to answer what happens if the worker crashes halfway through a job.
That crash question is the heart of this chapter.
A background system is not reliable because it never fails.
It is reliable because failures are expected, visible, recoverable, and tested.

By the end of the chapter, you should be able to:
- Design a small job table in SQLite.
- Enqueue a job from a foreground command.
- Claim a pending job safely so two workers do not process the same row.
- Run a handler based on `job_type`.
- Move a job through queued, running, done, and failed states.
- Retry transient failures without retrying permanent data bugs forever.
- Write idempotent handlers so rerunning the same job does not corrupt data.
- Stop a worker gracefully when the user presses Ctrl+C or sends a shutdown signal.
- Test the worker without sleeping for real time whenever possible.
- Keep worker code inside `src/researchops/workers/` while respecting the project architecture.

The most important mindset is this: the queue is not magic.
It is a table.
The worker is not magic.
It is a loop.
Reliability is not magic.
It is a set of explicit decisions about state, retries, idempotency, and shutdown.

## What you already know from previous weeks
This chapter builds on the earlier ResearchOps journey instead of starting over.
Week 1 gave you the repository shape and the first CLI path.
That matters because job commands still enter through the CLI layer, not through random scripts.
Week 2 introduced file paths, exceptions, and logging.
That matters because workers must log progress and convert low-level errors into useful job errors.
Week 3 strengthened the domain model idea.
That matters because a `Job` is a domain concept, not just a loose dictionary.
Week 4 made CLI packaging and entry points feel normal.
That matters because `researchops jobs run` should behave like a real command.
Week 5 introduced SQLite storage.
That matters because this queue is persisted in SQLite, not kept only in memory.
Week 6 made testing more serious.
That matters because worker behavior must be tested across success, failure, retry, and shutdown paths.
Week 7 taught configuration and operational habits.
That matters because a worker needs settings such as poll interval, database path, and maximum attempts.
Week 8 introduced process pools for CPU-heavy work.
That matters because a worker may call ingestion or embedding tasks that should not freeze the main loop.
Week 9 introduced interfaces and dependency boundaries.
That matters because services depend on protocols, not concrete SQLite details.
Week 10 through Week 12 improved the data pipeline and experiment tracking story.
That matters because background jobs are often used to run these pipeline steps safely.
Week 13 introduced embeddings and semantic search.
That matters because embedding jobs are a realistic kind of work, but this chapter does not deepen the math.
Week 14 introduced the FastAPI layer.
That matters because an API endpoint can enqueue a job instead of doing slow work during the request.
Week 15 introduced async I/O and network fetching.
That matters because you now understand why blocking the foreground request is a poor user experience.
Week 16 uses all of that knowledge to separate request acceptance from work completion.

A helpful review question is: what should happen immediately, and what can happen later?
If the answer is "later", a job is probably involved.
If the answer is "the user must see the result before continuing", a job may not be the right tool.

## What problem this week solves
Before a job system, ResearchOps has a timing problem.
A user can ask the system to ingest a paper or generate embeddings.
That work may take seconds or minutes.
If the CLI or API performs the work immediately, the user waits with no durable record of what is happening.
If the process crashes, the system may forget what was requested.
If the user repeats the command, duplicate output may be created.
If the work fails halfway through, it may be unclear whether retrying is safe.
A persisted job queue solves these problems by recording intent before doing work.
Recording intent means the system writes a row that says, in effect, "this work should happen."
The worker can then pick up that row and execute it.
If the worker dies, the row still exists.
If the job fails, the row can store the error.
If the failure is transient, the row can be retried.
If the failure is permanent, the row can remain failed for inspection.
The problem is not only speed.
The bigger problem is operational honesty.
A foreground command that hides slow work gives the learner little visibility.
A job table makes system behavior visible.
Visibility is the first step toward reliability.

The queue also solves a learning problem.
Many production systems use background jobs, but beginners often see them as mysterious infrastructure.
This chapter removes the mystery by implementing the smallest useful local version.
The local version teaches the same mental model as larger systems: enqueue, claim, execute, acknowledge, retry, fail, inspect.

## Beginner mental model
Imagine a library desk with a tray labeled "to do."
A librarian places a paper request card into the tray.
A worker takes the oldest card, writes "in progress" on it, performs the work, then writes "done."
If the worker cannot finish, they write the error on the card.
If the problem might be temporary, they put the card back into the tray with a note saying how many times it has been tried.
If the problem is clearly permanent, they leave the card in the failed pile.
SQLite is the tray.
The `jobs` table stores the cards.
The CLI or API is the librarian accepting requests.
The worker process is the person taking cards from the tray.
The handler function is the specialized skill needed to perform one kind of card.
The status field is the label written on the card.
The attempt count is the tally mark written after each failed try.
The payload is the detailed instruction on the card.
The error field is the note explaining what went wrong.

Use this five-step worker story whenever the code feels confusing:
1. Poll: ask the queue whether work is available.
2. Claim: mark one pending job as running so this worker owns it.
3. Execute: decode the payload and call the correct handler.
4. Record: mark the job done, failed, or queued for retry.
5. Repeat or stop: continue polling unless shutdown was requested.

The word "claim" is especially important.
Claiming is not just reading a row.
Claiming is reading and changing ownership in a way that prevents another worker from taking the same job at the same time.

## Core vocabulary
- **Job:** A durable record of one piece of work the system should perform.
- **Queue:** A collection of jobs waiting to be processed, ordered by a rule such as creation time or scheduled time.
- **Worker:** A process or loop that repeatedly claims jobs and runs handlers.
- **Handler:** A function that knows how to perform one job type.
- **Payload:** The serialized input data for a job, usually stored as JSON text.
- **Status:** The current state of a job, such as queued, running, done, or failed.
- **State machine:** A small set of allowed states and allowed transitions between them.
- **Retry:** Trying a failed job again because the failure may be temporary.
- **Max attempts:** The upper limit that prevents a bad job from retrying forever.
- **Idempotency:** The property that running the same operation more than once has the same final effect as running it once.
- **Atomic operation:** A database operation that completes as one indivisible unit from the point of view of other workers.
- **Transaction:** A group of database statements that succeed or fail together.
- **Polling:** Checking the queue repeatedly for available work.
- **Backoff:** Waiting longer before retrying after repeated failures.
- **Graceful shutdown:** Stopping after the current safe point instead of killing the process in the middle of a write.
- **Stuck job:** A job left in running state because a worker crashed or was killed.
- **Dead letter:** A permanently failed job kept for inspection instead of retried.
- **Job repository:** The storage object that reads and writes job records.
- **Job service:** The application-level object that enqueues jobs and coordinates worker behavior.
- **Observability:** The ability to inspect what the worker is doing through rows, logs, metrics, and errors.

Do not memorize these as isolated flash cards only.
Connect each word to a row in the job table and to one branch in the worker loop.

## Concept explanations from first principles
### Why persist jobs?
A list in Python memory disappears when the process exits.
A SQLite row remains after the process exits.
A queue that disappears on crash is useful for practice but not enough for ResearchOps.
Persisting the job before running it means the system has a durable promise to do work.
That promise can be inspected by `jobs list` and recovered after a restart.

### Why use states?
Without states, a job is just a blob of unknown progress.
States let the system answer simple operational questions.
How many jobs are waiting?
Which jobs are actively running?
Which jobs succeeded?
Which jobs need human attention?
A state machine keeps these answers consistent.

### Why not run every request immediately?
Immediate work is simple for tiny tasks.
Immediate work becomes painful for slow parsing, embedding, or network-dependent tasks.
Foreground execution makes the user wait and gives poor crash recovery.
A job system accepts the request quickly and gives the user a job id.
The job id becomes the handle for later inspection.

### Why retries need limits?
Some failures are temporary, such as a locked database or a network timeout.
Some failures are permanent, such as invalid JSON or a missing handler.
Retrying temporary failures can make the system resilient.
Retrying permanent failures wastes time and hides the real bug.
A maximum attempt count protects the worker from infinite loops.

### Why idempotency matters?
Workers can crash after completing real work but before recording success.
When the job is retried, the handler may run again.
If running twice creates duplicate records, the system corrupts itself during recovery.
If running twice leaves the same final database state, recovery is safe.
Idempotency turns retries from dangerous into normal.

### Why graceful shutdown matters?
A user may press Ctrl+C while a worker is polling.
A deployment system may send a termination signal.
A laptop may be closed.
The worker should stop accepting new jobs when shutdown is requested.
It should finish or safely release the current job according to the design.
Abrupt shutdown in the middle of state updates creates stuck jobs.

A minimal state machine for this chapter looks like this:

```text
queued  -> running
running -> done
running -> queued   # retry after transient failure
running -> failed   # permanent failure or attempts exhausted
running -> queued   # rescue after worker crash and timeout
```

The first transition is a claim.
The second transition is a successful acknowledgment.
The third transition is a retry.
The fourth transition is a final failure.
The fifth transition is crash recovery.
Notice what is missing: `done -> running` is not allowed.
A completed job should not become running again unless the user creates a new job.
Also missing: `failed -> done` is not a normal worker transition.
A failed job may be manually inspected and requeued, but that should be explicit.

## ResearchOps-specific application
ResearchOps processes research papers.
A paper may enter the system from a local file path, a metadata import, or a fetched URL.
The user wants a responsive command, not a frozen terminal.
A local job system lets the command enqueue `ingest_paper` and return a job id.
The worker later claims that job and calls an ingestion handler.
The ingestion handler may validate the file, parse metadata, store a document row, and schedule follow-up embedding work.
The embedding handler may read stored chunks and compute vectors using the embedding code from Week 13.
This chapter can refer to embedding work as a job type, but it does not introduce new embedding algorithms.
The handler should call existing service functions when possible.
That keeps business rules in services instead of scattering them through worker code.
The worker is orchestration glue.
It decides when and how to run work.
It should not become the place where every ResearchOps rule is rewritten.

Possible Week 16 job types include:
- `ingest_document`: validate and store a paper record.
- `parse_pdf`: run CPU-heavy parsing through the Week 8 process pool boundary.
- `build_embeddings`: compute embeddings for stored chunks using Week 13 infrastructure.
- `refresh_search_index`: update local search tables from stored documents.
- `fetch_metadata`: perform I/O-heavy network fetching using Week 15 async ideas where appropriate.

Do not add RAG answer generation in this week.
Do not add LLM prompt templates in this week.
Do not add Docker orchestration in this week.
The worker exists so those later features have a safe operational foundation.

## Code examples with line-by-line explanation
This section shows a beginner-readable implementation shape.
The exact project code may differ, but the responsibilities should remain recognizable.

### Example 1: a Job model

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

JobStatus = Literal["queued", "running", "done", "failed"]

@dataclass(frozen=True)
class Job:
    id: str
    job_type: str
    payload_json: str
    status: JobStatus
    attempts: int
    max_attempts: int
    last_error: str | None
    created_at: datetime
    updated_at: datetime
    scheduled_at: datetime
```

- `from dataclasses import dataclass`: imports the decorator that writes a simple initializer and representation for us.
- `from datetime import datetime`: imports the timestamp type used for created, updated, and scheduled fields.
- `from typing import Literal`: lets the type checker know that status should be one of a small fixed set of strings.
- `JobStatus = Literal[...]`: names the allowed status values so the rest of the code can reuse one definition.
- `@dataclass(frozen=True)`: creates an immutable value object so code does not casually mutate jobs in surprising places.
- `class Job:`: starts the domain model for one durable unit of work.
- `id: str`: stores the unique handle shown to users and used in logs.
- `job_type: str`: tells the worker which handler should run.
- `payload_json: str`: stores the handler input as JSON text because SQLite stores text naturally.
- `status: JobStatus`: records where the job is in the state machine.
- `attempts: int`: counts how many times the worker has tried the job.
- `max_attempts: int`: keeps the retry limit with the job so different job types can choose different limits.
- `last_error: str | None`: keeps the latest failure message for inspection and debugging.
- `created_at: datetime`: records when the job entered the queue.
- `updated_at: datetime`: records when the row last changed state.
- `scheduled_at: datetime`: controls when a queued retry becomes eligible to claim.

The model is intentionally not responsible for writing SQL.
It is the shape of the data, not the storage mechanism.

### Example 2: the SQLite table

```sql
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    job_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    last_error TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    scheduled_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_jobs_claimable
ON jobs(status, scheduled_at, created_at);
```

- `CREATE TABLE IF NOT EXISTS jobs`: makes startup repeatable; running migrations twice should not crash during local learning.
- `id TEXT PRIMARY KEY`: uses a string id so UUIDs can be stored without conversion.
- `job_type TEXT NOT NULL`: requires every job to name the kind of work it represents.
- `payload_json TEXT NOT NULL`: keeps the payload as text so it can be inspected with ordinary SQLite tools.
- `status TEXT NOT NULL`: keeps the state machine visible in the table.
- `attempts INTEGER NOT NULL DEFAULT 0`: starts new jobs with zero tries.
- `max_attempts INTEGER NOT NULL DEFAULT 3`: uses a safe default that prevents infinite retry loops.
- `last_error TEXT`: allows null because a job that has not failed should not pretend to have an error.
- `created_at TEXT NOT NULL`: stores ISO-formatted timestamps that sort well as strings.
- `updated_at TEXT NOT NULL`: supports debugging and stuck-job rescue.
- `scheduled_at TEXT NOT NULL`: supports immediate jobs and delayed retries with the same column.
- `idx_jobs_claimable`: helps the worker find queued jobs without scanning the whole table every time.

The table does not use a separate message broker.
SQLite is enough for the local single-machine learning milestone.

### Example 3: enqueueing a job

```python
import json
import uuid
from datetime import datetime, timezone

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def enqueue_job(connection, job_type: str, payload: dict, max_attempts: int = 3) -> str:
    job_id = str(uuid.uuid4())
    now = utc_now().isoformat()
    payload_json = json.dumps(payload, sort_keys=True)
    connection.execute(
        """
        INSERT INTO jobs (
            id, job_type, payload_json, status, attempts, max_attempts,
            last_error, created_at, updated_at, scheduled_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (job_id, job_type, payload_json, "queued", 0, max_attempts, None, now, now, now),
    )
    connection.commit()
    return job_id
```

- `import json`: lets the function convert a Python dictionary into text for storage.
- `import uuid`: lets the function create a unique id without asking the user for one.
- `datetime, timezone`: let the code create timezone-aware UTC timestamps.
- `utc_now()`: centralizes the clock so tests can patch or replace time more easily.
- `enqueue_job(...)`: is called by the foreground side of the system, such as CLI or API wiring.
- `job_id = str(uuid.uuid4())`: creates a unique public handle for the job.
- `now = utc_now().isoformat()`: stores the timestamp as an ISO string, which is readable and sortable.
- `json.dumps(payload, sort_keys=True)`: serializes the payload deterministically, which helps tests and idempotency keys.
- `connection.execute(...)`: inserts exactly one durable job row.
- `status` value `"queued"`: means the worker is allowed to claim the job.
- `attempts` value `0`: means no handler has been tried yet.
- `last_error` value `None`: means there is no failure to report yet.
- `scheduled_at` equal to `now`: means the job is eligible immediately.
- `connection.commit()`: makes the enqueue durable before returning to the caller.
- `return job_id`: gives the user or API caller a way to inspect progress later.

### Example 4: claiming one job

```python
def claim_next_job(connection, now_iso: str) -> Job | None:
    connection.execute("BEGIN IMMEDIATE")
    try:
        row = connection.execute(
            """
            SELECT * FROM jobs
            WHERE status = ? AND scheduled_at <= ?
            ORDER BY created_at ASC
            LIMIT 1
            """,
            ("queued", now_iso),
        ).fetchone()
        if row is None:
            connection.commit()
            return None
        connection.execute(
            """
            UPDATE jobs
            SET status = ?, updated_at = ?
            WHERE id = ? AND status = ?
            """,
            ("running", now_iso, row["id"], "queued"),
        )
        connection.commit()
        return row_to_job(row, status="running", updated_at=now_iso)
    except Exception:
        connection.rollback()
        raise
```

- `BEGIN IMMEDIATE`: asks SQLite for a write lock before selecting, which reduces race conditions between workers.
- `try:`: ensures the transaction is either committed or rolled back.
- `SELECT * FROM jobs`: reads the oldest eligible queued job.
- `status = ?`: keeps SQL values parameterized instead of string-formatted.
- `scheduled_at <= ?`: prevents the worker from claiming a delayed retry too early.
- `ORDER BY created_at ASC`: makes older jobs run before newer jobs.
- `LIMIT 1`: claims at most one job per worker iteration.
- `if row is None`: handles an empty queue as a normal situation, not an error.
- `UPDATE jobs SET status = ?`: turns the selected job into a running job.
- `WHERE id = ? AND status = ?`: protects the update from accidentally changing a job already moved by another process.
- `connection.commit()` after update: makes the claim visible and durable.
- `row_to_job(...)`: converts storage data back into a domain object.
- `except Exception`: rolls back partial work so the database is not left in a half-claimed state.

Some SQLite versions support `UPDATE ... RETURNING`, which can make claiming cleaner.
The beginner version above is explicit so you can see each step.

### Example 5: the handler registry

```python
from collections.abc import Callable

JobHandler = Callable[[dict], None]

class HandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, JobHandler] = {}

    def register(self, job_type: str, handler: JobHandler) -> None:
        self._handlers[job_type] = handler

    def get(self, job_type: str) -> JobHandler | None:
        return self._handlers.get(job_type)
```

- `Callable[[dict], None]`: means a handler receives a payload dictionary and returns nothing when successful.
- `HandlerRegistry`: keeps job-type lookup in one small object.
- `self._handlers`: stores the mapping from job type string to function.
- `register(...)`: is called during application wiring, not inside the worker loop for every job.
- `get(...)`: returns `None` for unknown types so the worker can mark a clear failure instead of crashing with `KeyError`.

### Example 6: running one job

```python
import json

def run_one_job(queue, registry: HandlerRegistry, clock=utc_now) -> bool:
    now_iso = clock().isoformat()
    job = queue.claim_next(now_iso)
    if job is None:
        return False

    handler = registry.get(job.job_type)
    if handler is None:
        queue.mark_failed(job.id, "unknown job type: " + job.job_type)
        return True

    try:
        payload = json.loads(job.payload_json)
    except json.JSONDecodeError as error:
        queue.mark_failed(job.id, "invalid JSON payload: " + str(error))
        return True

    try:
        handler(payload)
    except TransientJobError as error:
        queue.retry_or_fail(job.id, str(error))
    except Exception as error:
        queue.mark_failed(job.id, str(error))
    else:
        queue.mark_done(job.id)

    return True
```

- `run_one_job(...)`: does one worker iteration, which makes it easy to test without an infinite loop.
- `clock=utc_now`: allows tests to pass a fake clock.
- `queue.claim_next(now_iso)`: moves one eligible job from queued to running.
- `return False` for no job: tells the outer loop there was no work this time.
- `registry.get(job.job_type)`: finds the function that knows how to process the job.
- `handler is None`: treats an unknown job type as a permanent job failure.
- `json.loads(job.payload_json)`: turns stored text back into a Python dictionary.
- `JSONDecodeError`: is a permanent data problem, not something a retry will fix.
- `handler(payload)`: runs the actual business work.
- `TransientJobError`: represents failures worth retrying, such as temporary locks or timeouts.
- `queue.retry_or_fail(...)`: increments attempts and either requeues or fails permanently.
- `except Exception`: is the safety net for unexpected permanent handler failures.
- `else: queue.mark_done(...)`: records success only when no exception was raised.
- `return True`: tells the outer loop that a job was handled, even if it failed.

### Example 7: a graceful worker loop

```python
import logging
import time

def run_worker(queue, registry: HandlerRegistry, stop_requested, poll_seconds: float = 1.0) -> None:
    logging.info("ResearchOps worker started")
    while not stop_requested():
        did_work = run_one_job(queue, registry)
        if did_work:
            continue
        time.sleep(poll_seconds)
    logging.info("ResearchOps worker stopped")
```

- `logging.info(...)` at start: gives the operator a visible marker that the worker is alive.
- `while not stop_requested()`: checks a shutdown hook at the top of each loop.
- `run_one_job(...)`: keeps the loop small by delegating one job attempt.
- `if did_work: continue`: immediately checks for more work when the queue is active.
- `time.sleep(poll_seconds)`: avoids burning CPU when the queue is empty.
- `logging.info(...)` at stop: makes graceful shutdown visible in logs.

In tests, do not let this loop run forever.
Test `run_one_job` directly for most behavior.
For loop tests, pass a stop function or maximum iteration guard so the test always exits.

### Example 8: an idempotent handler

```python
def handle_store_document(payload: dict, connection) -> None:
    document_id = payload["document_id"]
    title = payload["title"]
    source_path = payload["source_path"]
    connection.execute(
        """
        INSERT INTO documents (id, title, source_path)
        VALUES (?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            source_path = excluded.source_path
        """,
        (document_id, title, source_path),
    )
    connection.commit()
```

- `document_id = payload["document_id"]`: uses a stable logical id instead of inventing a new row every attempt.
- `title = payload["title"]`: extracts required metadata from the job payload.
- `source_path = payload["source_path"]`: records where the document came from.
- `INSERT INTO documents`: creates the document if it does not exist.
- `ON CONFLICT(id) DO UPDATE`: turns a second run into an update rather than a duplicate insert.
- `excluded.title`: means the title from the attempted insert.
- `connection.commit()`: makes the handler result durable before the worker marks the job done.

This handler is safe to run twice for the same document id.
That is the practical meaning of idempotency in this chapter.

## Common beginner mistakes
- **Using `pending`, `queued`, and `waiting` interchangeably:** Pick one vocabulary in the code and tests. This chapter uses `queued` for jobs waiting to be claimed.
- **Claiming with a plain SELECT:** A plain SELECT only observes a job. It does not reserve it. Two workers can observe the same row.
- **Forgetting to commit after enqueue:** The job may appear in the current connection but not be durable for another process.
- **Retrying invalid JSON:** Bad JSON will still be bad on the next attempt. Mark it failed and show the error.
- **Letting unknown job types crash the worker:** Unknown types are data or wiring problems. Record a clear job failure.
- **Sleeping in unit tests:** Long sleeps make tests slow and flaky. Prefer fake clocks or one-iteration worker functions.
- **Putting business logic inside the worker loop:** The worker should orchestrate. Services and handlers should own business rules.
- **Ignoring idempotency:** Retries can duplicate rows or files unless handlers use stable keys and upserts.
- **Never rescuing stuck running jobs:** A crash after claim can leave jobs running forever unless recovery exists.
- **Catching every exception as retryable:** Some failures should fail immediately. Retry only when there is a reason.
- **Forgetting shutdown behavior:** A loop with no stop check is annoying locally and unsafe operationally.
- **Hiding errors in logs only:** The job row itself should store enough error text for `jobs show` to help.

A good beginner rule is: every state transition deserves a test.
Another good rule is: every failure class should have a visible row state after the worker handles it.
If a failure disappears into the terminal output only, the job system is not doing its job.

## Debugging guidance
Debug workers by shrinking the problem to one job.
Do not start by staring at the whole loop.
First inspect the row.
Ask whether the row is eligible to claim.
Check `status`.
Check `scheduled_at`.
Check `attempts` and `max_attempts`.
Check whether `payload_json` is valid JSON.
Check whether a handler is registered for `job_type`.
Then run one worker iteration.
After one iteration, inspect the row again.
The row should have moved to `done`, `failed`, or back to `queued` for retry.
If it is still `running`, the exception path probably failed to update the state.
If it is duplicated in the output table, the handler is probably not idempotent.
If it was never claimed, the scheduled time may be in the future or the status string may not match.

Useful inspection queries:

```sql
SELECT id, job_type, status, attempts, max_attempts FROM jobs ORDER BY created_at;
SELECT id, last_error FROM jobs WHERE status = 'failed';
SELECT status, COUNT(*) FROM jobs GROUP BY status;
SELECT id, updated_at FROM jobs WHERE status = 'running' ORDER BY updated_at;
SELECT id, scheduled_at FROM jobs WHERE status = 'queued' ORDER BY scheduled_at;
```

When debugging a worker, log transitions rather than random values.
A useful log line says which job moved from which state to which state.
For example: `job=abc type=ingest_document queued->running`.
Another useful log line says why a retry was scheduled.
For example: `job=abc retry attempts=2 error=database locked`.
Avoid logging the entire payload if it may contain large text or sensitive metadata.
Log identifiers and concise error summaries.

## Design tradeoffs
- **SQLite queue versus in-memory queue:** SQLite is slower than a list but survives process exit and can be inspected. In-memory is useful for unit tests but not enough for this milestone.
- **Polling versus notifications:** Polling is easy to understand and works locally. Notifications are more efficient but add complexity that this chapter does not need.
- **One worker versus many workers:** One worker is simpler and enough for local learning. Multiple workers require stronger claim tests and careful idempotency.
- **Immediate retry versus scheduled retry:** Immediate retry is simple but can hammer a broken dependency. Scheduled retry with backoff is safer but needs timestamps and fake-time tests.
- **Generic handler signature versus typed payload objects:** A dictionary is simple and maps directly from JSON. Typed payload models are safer but add ceremony; use them only when the project is ready.
- **Storing errors in the row versus logs only:** Rows make errors visible from CLI inspection. Logs provide operational history. Use both when possible.
- **Marking failed permanently versus dead-letter table:** Keeping failed jobs in `jobs` is simpler. Archiving to a dead-letter table can keep active views clean but adds another recovery path.
- **Worker owns retries versus handler owns retries:** Central worker retry logic is consistent. Handler-specific retry can be more precise but may duplicate policy.
- **Running CPU work directly versus process pool:** Direct calls are easier but can block the worker. CPU-heavy parsing should use the Week 8 process pool boundary.
- **Async inside worker versus separate async service:** Use async for I/O where it already exists, but do not put CPU-heavy work in an event loop.

There is no perfect queue design.
There is only a design whose tradeoffs match the project stage.
For Week 16, clarity, durability, and testability matter more than maximum throughput.

## Testing implications
Worker tests should be layered.
Start with pure state-transition tests.
Then test repository methods against a temporary SQLite database controlled by the test.
Then test `run_one_job` with fake handlers.
Finally test the CLI command that lists or runs jobs.
Most tests should not start a real infinite loop.
A one-iteration function is the testing seam.
A fake clock is another testing seam.
A fake handler registry is another testing seam.
A fake queue can test service behavior without SQLite.
SQLite integration tests can test locking, persistence, and SQL correctness.

Important test cases include:
- Enqueue creates a queued job with attempts set to zero.
- Claim returns the oldest eligible queued job.
- Claim changes the job status to running.
- Empty queue returns no job without crashing.
- Successful handler marks the job done.
- Unknown job type marks the job failed without retrying forever.
- Invalid JSON marks the job failed without calling a handler.
- Transient handler error increments attempts and requeues when attempts remain.
- Transient handler error marks failed when attempts are exhausted.
- Permanent handler error marks failed immediately.
- Idempotent handler can run twice with one final stored result.
- Stuck running job can be rescued after timeout.
- Worker loop exits when stop is requested.
- Job list command displays id, type, status, attempts, and updated time.

Avoid tests that depend on real time passing.
If backoff is needed, store `scheduled_at` and pass a fake `now` value to claim logic.
Avoid tests that depend on thread timing unless the goal is specifically to test claim safety.
Thread race tests are useful but should be few and carefully written.

## Architecture implications
The worker job system must respect the ResearchOps dependency direction.
`core/` may define models, exceptions, and interfaces.
`core/` must not import worker code.
`services/` may coordinate use cases through protocols.
`services/` should not import concrete SQLite worker repositories directly.
`storage/` may implement SQLite persistence.
`workers/` may contain worker loops, job runners, handler registration, and process-pool integration.
`cli/` wires concrete implementations to commands.
`api/` can enqueue jobs through services, but it should not run slow worker logic inside request handlers.
Handlers should call services or infrastructure through clear boundaries.
If a handler needs PDF parsing, it should use the parsing layer and the Week 8 process pool design.
If a handler needs network fetching, it should use the existing async-aware fetching layer from Week 15.
If a handler needs embeddings, it should use the search or embedding infrastructure already introduced in Week 13.
The job system should not become a shortcut that imports everything from everywhere.

A healthy dependency picture is:

```text
CLI / API
  -> services
  -> core protocols
  -> concrete job repository and worker wiring

workers
  -> core models and protocols
  -> services or registered handlers
  -> infrastructure through explicit wiring
```

An unhealthy dependency picture is:

```text
core -> workers -> cli -> api -> storage -> core
```

That cycle makes the curriculum harder to understand and the project harder to test.

## How this connects to AI engineering / ML research
AI engineering work often includes slow, failure-prone background tasks.
Embedding a document collection may take time.
Parsing a PDF may fail on one malformed file while many other files are fine.
Fetching metadata may hit timeouts or rate limits.
Updating a search index may need to resume after interruption.
Experiment pipelines may need to record progress across multiple steps.
A job system gives those tasks a durable operational shape.
It also creates a clear audit trail.
For research workflows, auditability matters because results must be reproducible.
If an embedding update failed, the researcher needs to know which document failed and why.
If the same document was queued twice, idempotency prevents duplicate scientific records.
If a laptop dies during a long local indexing run, stuck-job rescue helps the learner continue without deleting everything.
This chapter also prepares the learner for production ML systems where workers are separated from request handlers.
The local queue is not the final scaling solution.
It is the conceptual foundation for understanding larger queues later.

Do not confuse this with Week 17 RAG.
A worker can prepare documents and embeddings for later retrieval.
It should not generate LLM answers in this chapter.

## Mini quizzes
1. **Question:** Why does the system write a job row before running the handler?
   **Check yourself:** So the request is durable and inspectable even if the worker crashes later.
2. **Question:** What is the difference between polling and claiming?
   **Check yourself:** Polling checks for work; claiming reserves one job by changing its state.
3. **Question:** Why is `running` not the final success state?
   **Check yourself:** `running` only means a worker owns the job right now; success must be recorded as `done`.
4. **Question:** Why should invalid JSON usually not be retried?
   **Check yourself:** The same stored string will still fail to parse unless someone changes the data.
5. **Question:** What makes a handler idempotent?
   **Check yourself:** Running it multiple times for the same logical input leaves one correct final result.
6. **Question:** Why is `max_attempts` necessary?
   **Check yourself:** It prevents one bad job from consuming the worker forever.
7. **Question:** What can leave a job stuck in `running`?
   **Check yourself:** A worker crash or kill after claim but before marking done, failed, or queued.
8. **Question:** Why should CLI/API not contain business logic?
   **Check yourself:** They are wiring layers; services and handlers should own business behavior.
9. **Question:** Why use a fake clock in retry tests?
   **Check yourself:** To test scheduled retries without sleeping in real time.
10. **Question:** What does graceful shutdown protect?
   **Check yourself:** It prevents the worker from starting unsafe new work while shutdown is requested.

## Explain-it-aloud prompts
- Explain the full lifecycle of a job from enqueue to done.
- Explain why a worker should claim a job before running the handler.
- Explain why a persisted SQLite queue is safer than an in-memory list for local ResearchOps.
- Explain what should happen when a handler raises a transient error.
- Explain what should happen when a handler raises a permanent error.
- Explain why invalid JSON is different from a network timeout.
- Explain idempotency using a document insert example.
- Explain how a worker can stop gracefully.
- Explain how a stuck running job can happen and how to rescue it.
- Explain how Week 8 process pools relate to Week 16 worker jobs.
- Explain how Week 15 async fetching relates to a background fetch job.
- Explain why Week 16 should not introduce RAG or Docker.

When you answer these aloud, avoid saying "it just works."
Name the table, the state, the function, and the failure path.

## What to memorize
- The basic lifecycle: `queued -> running -> done`.
- The retry lifecycle: `running -> queued` until attempts are exhausted.
- The final failure lifecycle: `running -> failed`.
- A worker loop is poll, claim, execute, record, repeat.
- A job needs at least id, type, payload, status, attempts, timestamps, and error.
- Claiming must be atomic enough that two workers do not run the same job.
- Idempotent handlers make retries safe.
- Invalid job data should fail visibly, not crash the whole worker.
- Unit tests should focus on one worker iteration.
- Long-running loops need a stop condition.

Memorization is not the same as understanding.
Memorize these because they are the vocabulary you will use while debugging.

## What to understand deeply
Understand why state transitions are the real design, not an implementation detail.
Understand that a row in `jobs` is both data and operational evidence.
Understand that retries are dangerous unless handlers are idempotent or carefully guarded.
Understand that a crash can happen between any two lines of code.
Understand that every place a crash can happen should leave a recoverable state or a visible failure.
Understand that a queue does not remove the need for good service boundaries.
Understand that the worker should not hide business behavior inside an untestable loop.
Understand why a one-iteration function is the key to testing.
Understand how `scheduled_at` turns backoff into data instead of sleep-heavy code.
Understand why the CLI/API returns a job id instead of pretending the slow task already finished.

The deepest lesson is recovery.
A happy-path worker is easy.
A trustworthy worker is designed around what happens when the happy path is interrupted.

## What not to worry about yet
Do not worry about distributed queue brokers such as Redis, RabbitMQ, or cloud queues yet.
Do not worry about Docker or container orchestration yet.
Do not worry about Kubernetes workers yet.
Do not worry about RAG prompt construction yet.
Do not worry about LLM provider APIs yet.
Do not worry about high-throughput scheduling algorithms yet.
Do not worry about exactly-once processing guarantees as a marketing phrase.
Do not worry about complex worker dashboards yet.
Do not worry about multi-machine clock drift yet.
Do not worry about advanced priority queues unless the current milestone already works.

The local worker teaches the concepts beneath those future tools.
If you cannot explain the SQLite version, a cloud version will only hide the confusion behind more services.

## Bridge to next week
Week 16 gives ResearchOps a reliable way to prepare work in the background.
That preparation matters for Week 17.
Week 17 can build on documents, chunks, embeddings, and indexes that may be produced by worker jobs.
The next step is not to throw away the job system.
The next step is to use it as the operational foundation for more advanced AI features.
When retrieval or answer generation becomes slow, you will already know how to decide what belongs in the foreground and what belongs in the background.
When a future AI task fails, you will already know to record the failure in a durable place.
When a future indexing task must be retried, you will already know why idempotency matters.
When a future API endpoint accepts long-running work, you will already know why it should return a job id.
Carry forward the same discipline: visible states, explicit boundaries, tested failure paths, and no hidden magic.

## Additional walkthrough: tracing one concrete job
- **Step 1:** The user runs `researchops ingest paper.pdf`.
- **Step 2:** The CLI validates that the path exists enough to create a meaningful request.
- **Step 3:** The CLI calls a service method such as `enqueue_ingest_document`.
- **Step 4:** The service creates a payload like `{ "source_path": "paper.pdf" }`.
- **Step 5:** The job repository serializes that payload as JSON.
- **Step 6:** The repository inserts a row with status `queued`.
- **Step 7:** The CLI prints the job id and exits quickly.
- **Step 8:** The user starts `researchops jobs run`.
- **Step 9:** The worker opens the same SQLite database.
- **Step 10:** The worker asks for the oldest queued job whose `scheduled_at` is not in the future.
- **Step 11:** The repository marks the row `running` in a transaction.
- **Step 12:** The worker looks up the `ingest_document` handler.
- **Step 13:** The worker parses `payload_json` into a dictionary.
- **Step 14:** The handler calls the appropriate ingestion service.
- **Step 15:** The ingestion service stores or updates document records idempotently.
- **Step 16:** The handler returns without an exception.
- **Step 17:** The worker marks the job `done`.
- **Step 18:** The user runs `researchops jobs list`.
- **Step 19:** The list output shows the job id, type, done status, and attempt count.
- **Step 20:** The durable row remains as evidence of completed work.

Now trace a failed version of the same job:
- The worker claims the job and marks it running.
- The handler attempts to parse a missing file.
- The parsing layer raises a clear exception.
- The worker catches the exception.
- If the exception is permanent, the worker marks the job failed immediately.
- If the exception is transient, the worker increments attempts and requeues if attempts remain.
- The job row stores `last_error` so the learner can inspect the reason.
- The worker continues with later jobs instead of crashing the entire process.

## Additional walkthrough: choosing retry categories
- **Database is locked for a moment:** classify as **Transient**. Retry with backoff because the lock may clear.
- **Network timeout while fetching metadata:** classify as **Transient**. Retry because the remote server or connection may recover.
- **Payload is invalid JSON:** classify as **Permanent**. Retrying the same bytes will not change them.
- **No handler registered for job type:** classify as **Permanent until deployment changes**. Fail visibly so wiring can be fixed.
- **File path does not exist:** classify as **Usually permanent**. The user likely supplied bad input; retrying wastes attempts.
- **PDF parser crashes on malformed file:** classify as **Usually permanent for that file**. Record the error and allow other jobs to continue.
- **Embedding model temporarily unavailable locally:** classify as **Possibly transient**. Retry if the local service can recover, but keep a bounded attempt count.

Classification is a design decision.
Write tests for the classifications that matter to ResearchOps.

## Additional walkthrough: status transition checklist
- Before adding a new job type, answer these questions.
- What payload fields are required?
- Can the handler safely run twice?
- Which exceptions are transient?
- Which exceptions are permanent?
- What should `last_error` say when the job fails?
- Does the handler call a service instead of embedding business logic in the worker?
- Does the handler need CPU isolation through the process pool?
- Does the handler need async I/O from the previous week?
- What test proves success?
- What test proves retry?
- What test proves permanent failure?
- What test proves idempotency?
- What CLI or API output lets the learner inspect the job?

<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 16 — Local Worker Job System:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
