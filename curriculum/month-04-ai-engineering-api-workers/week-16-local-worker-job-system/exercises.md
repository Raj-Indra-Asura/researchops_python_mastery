<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 16 — Local Worker Job System:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 16 Local Worker and Job System

This workbook is designed to make you practice the local worker and job queue until you can build, test, and explain it without guessing.
Do not skip the written exercises; background systems fail when engineers cannot explain state transitions clearly.

## How to use this workbook
- Work in order unless you already have strong evidence that a later exercise is blocking your project implementation.
- Use a scratch branch or a small local experiment when the exercise asks you to break behavior.
- Keep the Week 16 boundary in mind: local SQLite queue, local worker, no Docker, no RAG, no LLM features.
- When an exercise says "write a test," write the test before or immediately beside the code.
- When an exercise says "explain," answer in your own words before looking at the notes again.
- Prefer one-iteration worker functions in tests so you do not create infinite loops.
- Use fake handlers for most exercises; only use real ingestion or embedding code when the exercise explicitly asks for integration.
- After each implementation exercise, inspect the job row and confirm that status, attempts, and last_error make sense.



Use this practical rhythm for every coding exercise:
- First, state which job row should exist before the code runs.
- Second, state which function is allowed to change that row.
- Third, run only that small function if possible.
- Fourth, inspect the row again and compare it with your prediction.
- Fifth, write or update the test while the behavior is still fresh in your mind.

Keep a small table in your notes while working:

| Question | Your answer |
|---|---|
| What status does the job start in? | |
| What status should it end in? | |
| Should attempts change? | |
| Should last_error change? | |
| Is the handler safe to run twice? | |

If you cannot fill in this table, pause before changing code.
The table forces you to design the state transition instead of discovering it accidentally.

## Warm-up exercises
1. **Draw the state machine.** Draw `queued -> running -> done`, `running -> queued`, and `running -> failed`. Label each arrow with the function that performs it.
2. **Create job examples by hand.** Write three `Job` examples: a queued ingest job, a running embedding job, and a failed parse job. Fill every field with realistic values.
3. **Classify failures.** For each failure, decide transient or permanent: invalid JSON, database locked, missing handler, timeout, missing file, malformed PDF.
4. **Explain idempotency.** In five sentences, explain why `INSERT OR REPLACE` or `ON CONFLICT DO UPDATE` can make a document handler safe to retry.
5. **Trace timestamps.** Given created_at, updated_at, and scheduled_at values, decide whether a job is claimable right now.
6. **Name handlers.** List five ResearchOps job types that belong in Week 16 and one tempting job type that belongs in Week 17 instead.
7. **Spot unsafe transitions.** Identify which transitions are unsafe: `queued -> done`, `done -> running`, `running -> queued`, `failed -> running`, `running -> failed`.
8. **One-loop story.** Write the worker loop in plain English using exactly five verbs: poll, claim, execute, record, stop.

## Code-reading exercises
1. **Find worker files.** Open `src/researchops/workers/`. Identify which file owns the loop, which file owns job models, and which file owns handler registration. If a file does not exist yet, write where it should belong.
2. **Read repository code.** Find the code that inserts a job row. Write down every column that receives a value and why that value is needed.
3. **Read claim logic.** Find the code that claims the next job. Does it update the status inside the same transaction or safe database operation? Explain the race it is trying to prevent.
4. **Read retry logic.** Find where attempts are incremented. Explain what happens when attempts are still below max_attempts and what happens when they are exhausted.
5. **Read unknown type behavior.** Find the handler lookup. What exact error is stored when the job type is unknown? Should that failure be retried?
6. **Read invalid JSON behavior.** Find where `json.loads` is called. What catches `JSONDecodeError`? What status does the job receive?
7. **Read shutdown behavior.** Find the stop condition for the loop. How does the loop avoid starting new work after shutdown is requested?
8. **Read CLI output.** Find `jobs list` or the intended CLI command. Which columns are visible to the learner? Which column would you add if debugging was hard?

## Implementation exercises
1. **Define the job table.** Create or update the SQLite schema for `jobs` with id, job_type, payload_json, status, attempts, max_attempts, last_error, created_at, updated_at, and scheduled_at.
2. **Implement enqueue.** Write a repository method that accepts `job_type`, `payload`, and optional `max_attempts`, serializes payload as JSON, inserts a queued row, commits, and returns the job id.
3. **Implement claim.** Write `claim_next(now)` so it returns the oldest queued job whose scheduled_at is not in the future and marks it running safely.
4. **Implement status updates.** Write `mark_done`, `mark_failed`, and `retry_or_fail`. Each method must update `updated_at`; retry must also update attempts and scheduled_at.
5. **Implement handler registry.** Create a small registry that maps job type strings to handler callables. Unknown job types must produce a clear failed job, not a worker crash.
6. **Implement run-one-job.** Write a function that claims one job, decodes JSON, finds a handler, runs it, and records done/retry/failed. Return whether a job was handled.
7. **Implement worker loop.** Wrap run-one-job in a loop with a stop callback and poll interval. The loop must sleep only when no job was handled.
8. **Implement job listing.** Add a repository method or service method that returns jobs ordered by created_at or updated_at for CLI display.
9. **Implement stuck-job rescue.** Add a method that requeues running jobs whose updated_at is older than a timeout. Store an explanatory last_error when rescuing.
10. **Implement idempotent document handler.** Write a handler that stores or updates a document using a stable document id instead of appending duplicates.

## Testing exercises
1. **Enqueue test.** Assert a new job is queued, has attempts 0, has no last_error, and stores valid JSON.
2. **Oldest claim test.** Insert three queued jobs with different created_at values. Assert the oldest eligible job is claimed first.
3. **Scheduled retry test.** Insert a queued job scheduled in the future and one scheduled in the past. Assert only the past job is claimable.
4. **Empty queue test.** Assert run-one-job returns False and does not throw when no jobs are queued.
5. **Success test.** Register a fake handler that records its payload. Assert the job becomes done and the handler saw the expected payload.
6. **Unknown handler test.** Enqueue `job_type="missing"`. Assert one worker iteration marks it failed with a useful last_error.
7. **Invalid JSON test.** Insert a malformed payload directly. Assert the worker marks failed and does not call any handler.
8. **Transient retry test.** Use a handler that raises a transient error once. Assert attempts increments and the job returns to queued.
9. **Attempts exhausted test.** Use a handler that always raises transient errors. Run enough iterations to exhaust max_attempts and assert status failed.
10. **Idempotency test.** Run the same document handler twice with the same payload. Assert exactly one document row exists.
11. **Stuck rescue test.** Create an old running job. Call rescue. Assert it becomes queued and records a rescue message.
12. **Shutdown test.** Run the loop with a stop callback that becomes true after a small number of iterations. Assert the loop exits.



13. **List ordering test.** Insert jobs in a mixed order of creation and update times. Assert the listing function uses the order promised by the CLI documentation.
14. **Last error clearing test.** Create a job that fails once and then succeeds after retry. Decide whether success should clear `last_error`, then write a test that locks in that decision.
15. **Payload preservation test.** Enqueue a payload with multiple keys. Assert the stored JSON can be loaded back into the same dictionary and that handler execution receives the same values.

## Debugging exercises
1. **Inspect by SQL.** After enqueueing jobs, run a local SQLite query through the project helper or CLI and record counts by status.
2. **Trace transitions.** Add temporary logging around state changes. Process three jobs and write the exact transition sequence for each job.
3. **Find a stuck job.** Manually create a running job with an old updated_at. Use a query to find it, then rescue it.
4. **Bad payload drill.** Manually insert invalid JSON. Run one worker iteration and inspect last_error.
5. **Unknown type drill.** Enqueue a typo job type such as `ingset_document`. Confirm the worker fails the job clearly.
6. **Backoff drill.** Force a transient failure and inspect scheduled_at after each retry. Confirm it moves forward.
7. **Duplicate output drill.** Temporarily remove idempotent upsert behavior from a handler. Run the same job twice and observe duplicate rows; then restore the upsert.
8. **Signal drill.** Start the worker, request shutdown, and verify the log shows a clean stop after a safe loop boundary.

## Refactoring exercises
1. **Extract clock.** Replace direct `datetime.now()` calls in worker logic with a clock dependency so tests can control time.
2. **Extract state constants.** Move status strings into a single enum or literal definition used by repository, worker, and tests.
3. **Extract row mapper.** Create one `row_to_job` function so all SQLite-to-domain conversion is consistent.
4. **Separate permanent and transient errors.** Create explicit exception types or classification functions so retry policy is not hidden inside broad `except Exception` blocks.
5. **Separate loop from iteration.** Ensure the infinite or long-running loop calls a testable one-iteration function.
6. **Move business code out of worker.** If a handler contains too much ResearchOps domain logic, move that logic into a service and let the handler call the service.
7. **Simplify CLI formatting.** Move job display formatting into a small helper so command tests can focus on output and repository tests can focus on data.

## Written explanation exercises
1. Explain why enqueueing is a durable promise to do work later.
2. Explain why a job id is better than making the user stare at a frozen command.
3. Explain the difference between `queued` and `running`.
4. Explain why `done` should usually be terminal.
5. Explain why `failed` jobs should keep their error message.
6. Explain how a worker crash can create a stuck running job.
7. Explain how rescue logic avoids losing stuck jobs.
8. Explain why retrying invalid JSON is a mistake.
9. Explain why handler idempotency protects recovery after crashes.
10. Explain how Week 8 process pools can be called from a worker handler without putting CPU-heavy work in the event loop.
11. Explain how Week 15 async I/O influences fetch-style jobs without turning the whole worker into magic.
12. Explain why Week 16 should not implement RAG or Docker.



13. Explain why a worker that logs an error but leaves the row `running` has not truly handled the failure.
14. Explain why a retry policy belongs near the worker orchestration instead of being copied into every handler.
15. Explain the difference between "the job failed" and "the worker process crashed."
16. Explain how a local SQLite worker prepares you to understand larger queue systems later without adding those systems now.

## Stretch exercises
1. **Status summary command.** Add a command or helper that prints counts grouped by status. Include queued, running, done, and failed even when the count is zero.
2. **Retry backoff.** Implement exponential backoff using scheduled_at: 1 second, 2 seconds, 4 seconds. Test with fake time, not real sleeping.
3. **Job detail view.** Add a `jobs show <job_id>` path that displays payload_json and last_error for one job.
4. **Dead-letter archive.** Move permanently failed jobs into a `dead_jobs` table while preserving the original payload and error.
5. **Handler-specific attempts.** Allow `build_embeddings` to use a different max_attempts than `ingest_document`, while keeping defaults safe.
6. **Metrics object.** Collect jobs_started, jobs_done, jobs_failed, jobs_retried, and loop_iterations during a worker run.
7. **Concurrent claim smoke test.** Start two worker threads against the same SQLite database and prove a single job is not processed twice.

## Brutal exercises
1. **Crash window analysis.** List every point between claim and mark_done where a crash can happen. For each point, write the resulting row state and recovery strategy.
2. **Idempotency audit.** Pick three potential handlers. For each one, describe exactly what duplicate side effect could happen and how to prevent it.
3. **Retry policy table.** Create a table of ten exception scenarios and classify each as retry, fail, or rescue later. Justify each classification.
4. **Worker chaos test.** Create fake handlers that succeed, fail permanently, fail transiently twice then succeed, and corrupt their own payload. Process a mixed batch and assert final counts.
5. **No-sleep loop test.** Test the worker loop with a fake sleep function and a stop condition. Assert sleep is called only when no job was available.
6. **Migration compatibility.** Pretend a previous database lacks scheduled_at. Design a migration that adds the column with a safe default.

## Mini project task
- Build a small local worker milestone for ResearchOps.
- The mini project must support enqueueing at least one realistic job type, running one worker iteration, running a polling worker loop, listing jobs, and inspecting failures.
- Use SQLite for persistence.
- Use a handler registry instead of if/elif chains spread across the worker.
- Include tests for success, unknown job type, invalid JSON, retry, attempts exhausted, idempotency, and graceful shutdown.
- The handler may be a simplified ingestion or embedding placeholder if the real project code is not ready, but it must follow the same boundaries the real handler would use.
- Do not add Docker.
- Do not add RAG.
- Do not add LLM provider calls.
- When finished, you should be able to demo: enqueue job, list queued job, run worker, list done job, show failed job with error.

## Completion checklist
- [ ] I can draw the Week 16 job state machine from memory.
- [ ] I can explain why claim must be safer than a plain SELECT.
- [ ] I implemented or can identify the SQLite jobs table.
- [ ] I implemented or can identify enqueue, claim, mark_done, mark_failed, and retry_or_fail behavior.
- [ ] I can run one job without starting an infinite loop.
- [ ] I can explain how the worker stops gracefully.
- [ ] I tested success, failure, retry, and exhausted attempts.
- [ ] I tested invalid JSON and unknown job type.
- [ ] I tested or explained idempotency for at least one handler.
- [ ] I can inspect jobs by status.
- [ ] I did not add Week 17 RAG behavior.
- [ ] I did not add Week 18 Docker behavior.
- [ ] I can explain how Week 8 process pools and Week 15 async ideas connect to worker handlers.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 16 — Local Worker Job System:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
