<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 16 — Local Worker Job System:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It - Week 16 Local Worker and Job System

This lab teaches reliability by making the local worker fail in controlled ways.
Do not perform these experiments on important data.
Use a disposable local database, then restore the correct implementation.

## Purpose of failure practice
Background workers fail differently from foreground commands.
A foreground command often either returns or crashes in front of the user.
A worker may fail after the user has walked away.
The only evidence may be a row status, an attempt count, an error message, and a log line.
Failure practice trains you to design those pieces deliberately.
The goal is not to make the worker unbreakable.
The goal is to make breaks visible, bounded, and recoverable.

## Failure lab rules
- Use a throwaway SQLite database for every experiment.
- Change one thing at a time so you know what caused the failure.
- Write down the expected bad behavior before running the experiment.
- Inspect the `jobs` table before and after the worker runs.
- Restore the correct implementation after observing the failure.
- Add or update a test that would catch the failure in the future.
- Do not introduce Docker, RAG, LLM calls, or future-week infrastructure.
- Do not keep intentionally broken code after the lab is complete.

## Intentional break experiments
### Experiment 1: Non-atomic claim lets two workers run one job

#### How to cause it
Replace the safe claim transaction with a plain SELECT followed later by UPDATE. Start two worker threads or simulate two claim calls that both read before either updates.

#### Expected error or bad behavior
Both workers may observe the same queued row. The handler may run twice, and duplicate side effects may appear.

#### How to inspect it
Query the job row, handler output table, and logs. Look for one job id appearing in two handler executions.

#### How to fix it
Restore an atomic claim using `BEGIN IMMEDIATE` plus update, or an equivalent single safe update pattern. Keep `WHERE status = queued` in the update.

#### Test that should catch it
A concurrency or controlled interleaving test should prove that only one claim succeeds for one queued job.

#### What this teaches
Claiming is ownership, not observation.

#### Common wrong fixes
Adding a sleep, hoping workers do not overlap, using a Python-only lock while multiple processes exist, or ignoring duplicate output because it is rare.

### Experiment 2: Crash after marking running leaves a stuck job

#### How to cause it
Insert a job, claim it, then raise `SystemExit` or simulate a process crash before mark_done or mark_failed runs.

#### Expected error or bad behavior
The job remains `running` forever. A normal worker that only claims queued jobs will skip it.

#### How to inspect it
Run a query for `status = running` ordered by `updated_at`. Confirm updated_at is old and attempts did not resolve.

#### How to fix it
Add `rescue_stuck_jobs(timeout_seconds)` that requeues old running jobs or marks them failed according to policy.

#### Test that should catch it
A test should create an old running job, call rescue, and assert the job becomes queued with a useful last_error.

#### What this teaches
Any crash window after claim needs a recovery story.

#### Common wrong fixes
Manually deleting the row, marking it done without running the handler, or making the worker claim running jobs blindly.

### Experiment 3: Non-idempotent handler duplicates documents

#### How to cause it
Change a document handler to always INSERT a new row with a fresh id instead of using the stable document id from the payload.

#### Expected error or bad behavior
Running the same job twice creates duplicate document records or duplicate index rows.

#### How to inspect it
Count rows by logical document id or source path before and after two handler runs.

#### How to fix it
Use a stable key and an upsert such as `ON CONFLICT(id) DO UPDATE`.

#### Test that should catch it
A test should call the handler twice with the same payload and assert exactly one logical document exists.

#### What this teaches
Retries are safe only when side effects are idempotent or guarded.

#### Common wrong fixes
Disabling retries, hiding duplicates in the UI, or generating a new document id on every attempt.

### Experiment 4: Unknown job type crashes or loops

#### How to cause it
Enqueue `job_type = "ingset_document"` with the typo left in place. Remove the guard that handles missing registry entries.

#### Expected error or bad behavior
The worker may raise `KeyError`, crash, or retry a job that can never succeed.

#### How to inspect it
Inspect logs for KeyError and inspect the job row to see whether it stayed running or queued repeatedly.

#### How to fix it
Restore explicit missing-handler handling: mark the job failed with a clear error and do not retry.

#### Test that should catch it
A test should enqueue an unknown type, run one iteration, and assert status failed, attempts bounded, and last_error names the missing type.

#### What this teaches
Wiring problems should become visible job failures.

#### Common wrong fixes
Adding a catch-all handler that silently succeeds, retrying forever, or allowing the worker process to crash.

### Experiment 5: Corrupt payload JSON kills the worker

#### How to cause it
Insert a job directly with `payload_json = "not valid json"` and a valid known job_type.

#### Expected error or bad behavior
`json.loads` raises `JSONDecodeError`. Without handling, the worker stops before recording a useful state.

#### How to inspect it
Inspect the process output and the job row. If the row is still running, the exception path is incomplete.

#### How to fix it
Catch `JSONDecodeError`, mark failed with `invalid JSON payload`, and skip the handler.

#### Test that should catch it
A test should insert malformed JSON and assert no handler was called and the job failed permanently.

#### What this teaches
Bad stored data is usually permanent until a person fixes the row or re-enqueues correctly.

#### Common wrong fixes
Retrying the same malformed string, swallowing the exception and marking done, or logging only without updating the row.

### Experiment 6: Infinite retries hide a permanent failure

#### How to cause it
Set max_attempts extremely high or remove the exhausted-attempts branch. Use a handler that always raises a transient error.

#### Expected error or bad behavior
The worker keeps requeueing the same job and may never make progress through later jobs.

#### How to inspect it
Inspect attempts over time and status counts. You may see one job cycling queued/running repeatedly.

#### How to fix it
Restore a small bounded max_attempts and mark failed when attempts are exhausted.

#### Test that should catch it
A test should run enough iterations to exhaust attempts and assert final status failed.

#### What this teaches
Retries need limits because classification can be wrong and dependencies can stay broken.

#### Common wrong fixes
Using huge retry counts, making tests run forever, or resetting attempts to zero on each retry.

### Experiment 7: Status not updated when handler raises

#### How to cause it
Remove `mark_failed` or `retry_or_fail` from the exception block around handler execution.

#### Expected error or bad behavior
A raised exception leaves the job running or crashes the loop without a durable failure state.

#### How to inspect it
Run a failing handler once, then query the job row. Look for `running` with no useful last_error.

#### How to fix it
Use try/except/else so every handler outcome records done, retry, or failed.

#### Test that should catch it
A test should use a handler that raises and then assert the job is not left running.

#### What this teaches
The exception path is part of the state machine, not an optional cleanup detail.

#### Common wrong fixes
Catching exceptions outside the worker loop only, printing the error, or marking done in a finally block.

### Experiment 8: Graceful shutdown ignored during empty polling

#### How to cause it
Write the loop as `while True` with sleep and no stop callback check, or check stop only after long blocking work.

#### Expected error or bad behavior
The worker does not stop promptly when requested. Tests may hang and local users may need to kill the process.

#### How to inspect it
Use logs or a fake sleep counter to see that the loop continues after stop is requested.

#### How to fix it
Check the stop condition at the top of the loop and after safe boundaries. Keep sleeps short or injectable in tests.

#### Test that should catch it
A test should use a stop callback that becomes true and assert the loop exits within bounded iterations.

#### What this teaches
Long-running workers must have a cooperative shutdown path.

#### Common wrong fixes
Using only Ctrl+C stack traces, setting poll_seconds to zero and spinning CPU, or relying on test timeouts.

## Debugging checklist
- [ ] Inspect the job id, job_type, status, attempts, max_attempts, last_error, updated_at, and scheduled_at.
- [ ] Confirm the job is eligible before wondering why the worker did not claim it.
- [ ] Confirm the handler is registered before debugging handler internals.
- [ ] Confirm payload_json parses before debugging business logic.
- [ ] Run one worker iteration before running the long polling loop.
- [ ] Check whether the failure is transient or permanent.
- [ ] Check whether attempts increased after a retryable failure.
- [ ] Check whether scheduled_at moved forward after backoff.
- [ ] Check whether the handler is idempotent before enabling retries.
- [ ] Check whether shutdown is requested at safe loop boundaries.
- [ ] Check logs for transition lines, not just stack traces.
- [ ] After fixing, add a regression test that fails on the broken version.

## Reflection after breaking
- Which failure surprised me most?
- Which job state made the failure visible?
- Which error was hidden until I inspected the database?
- Which failure would have corrupted data without idempotency?
- Which failure would have caused an infinite loop without max_attempts?
- Which failure would have hung a test without a stop condition?
- What test did I add or improve after the experiment?
- What part of the worker still feels fragile?
- Can I explain how to recover from a worker crash after claim?
- Can I explain which failures should never be retried?

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 16 — Local Worker Job System:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
