# Week 16 - Local Worker and Job System

## Learning objectives
- Model background jobs with explicit states.
- Design idempotent job handlers that are safe to retry.
- Add retry policies for failed jobs.
- Separate job submission from job execution.
- Persist job metadata and outputs.
- Build a local worker loop for asynchronous processing.
- Test state transitions and failure recovery.

## Project milestone
Create a local job system that can queue and execute background ResearchOps tasks such as ingest, embedding generation, or remote fetches.

## Files to modify/create
- `src/researchops/jobs/models.py`
- `src/researchops/jobs/queue.py`
- `src/researchops/jobs/worker.py`
- `tests/unit/test_job_states.py`
- `tests/integration/test_local_worker.py`

## Concepts covered
Job queues, state machines, retries, idempotency, background workers, failure recovery, and task persistence.

## Expected deliverables
- A job model with states such as queued, running, succeeded, and failed.
- A local worker that polls and executes jobs.
- Retry behavior with limits.
- Tests covering state transitions and idempotent re-runs.

## Definition of done
- [ ] Job states are explicit.
- [ ] Worker loop can process queued jobs.
- [ ] Failed jobs can retry safely.
- [ ] Idempotency rules are defined.
- [ ] Job metadata is persisted.
- [ ] State transition tests pass.
- [ ] You can explain how duplicate work is prevented.
