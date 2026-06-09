# Notes - Week 16 Local Worker and Job System

As applications grow, some tasks should not happen inline with a user request or CLI command. They may take too long, need retries, or run better in the background. A job system solves this by separating submission from execution.

A job usually has an ID, a type, a payload, and a state. Typical states include `queued`, `running`, `succeeded`, and `failed`. You may also add `retrying` or `cancelled` later. What matters is that state transitions are explicit.

```python
from dataclasses import dataclass


@dataclass
class Job:
    job_id: str
    job_type: str
    payload: dict[str, str]
    state: str = "queued"
    attempts: int = 0
```

A worker is a loop that claims jobs, runs the right handler, and updates state. Even a local worker can teach the same design principles used in larger queue systems.

```python
def run_once(queue: JobQueue) -> None:
    job = queue.next_job()
    if job is None:
        return
    queue.mark_running(job.job_id)
    try:
        handle_job(job)
    except Exception:
        queue.mark_failed(job.job_id)
    else:
        queue.mark_succeeded(job.job_id)
```

Retries are useful when failures are temporary. But retries are dangerous without idempotency. Idempotent work can be run more than once without causing duplicate side effects. For example, saving the same parsed document twice may need an upsert or duplicate-check rule. Charging a credit card twice would not be idempotent.

This week's mindset is: assume the worker may crash after partial work. How will the system recover safely? One answer is to store job state and enough metadata to resume or retry. Another is to make handlers check whether their intended output already exists before doing work again.

A queue does not have to be fancy. In a local system, it might be a SQLite table. Submission inserts a row. The worker polls for queued jobs. That is enough to teach scheduling and recovery.

Retry policies should be bounded. For example, a job may retry up to three times, after which it stays failed for manual inspection. Record the failure reason if possible.

Testing a job system often means asserting state transitions. A good unit test might submit a fake job, run the worker once, and confirm the state moved from `queued` to `succeeded`. Another test might force a handler exception, confirm `attempts` increases, and verify retry behavior.

The larger architecture lesson is that background work is another boundary. A user-facing API or CLI can submit a job quickly, while the worker performs the expensive task later. That pattern will matter for production workflows where responsiveness and recovery are more important than immediate completion.
