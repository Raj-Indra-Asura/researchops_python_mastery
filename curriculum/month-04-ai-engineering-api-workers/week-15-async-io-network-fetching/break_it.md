<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It - Week 15 Async I/O and Network Fetching

Failure practice teaches you how async network code breaks before it breaks in a real research workflow.

## 1. Purpose of failure practice

Async I/O bugs are often invisible until timing, cancellation, or remote-service behavior changes.
This lab makes those failures visible in small controlled experiments.
Each experiment should be run with fake clients or toy coroutines, not the real internet.
The goal is not to memorize errors; the goal is to recognize the shape of the bug quickly.

## 2. Failure lab rules

- Change one thing at a time.
- Predict the failure before running it.
- Capture the exact error message, warning, or timing symptom.
- Fix the smallest possible cause.
- Add or name the test that would prevent the bug from returning.
- Do not leave intentionally broken code in the project.
- Do not use real public services for these failure experiments.
- Do not move CPU-heavy parsing into async code as a fix.

## 3. Intentional break experiments

### Experiment 1: Forget to await the request

#### How to cause it
In `fetch_bytes`, change `response = await client.get(url)` to `response = client.get(url)`.

#### Expected error
You may see an attribute error such as a coroutine object has no attribute `raise_for_status`, or a warning that a coroutine was never awaited.

#### How to inspect
Print `type(response)` before calling `raise_for_status`; it will be a coroutine object rather than a response-like object.

#### How to fix
Restore `await client.get(url)` and rerun the smallest success test.

#### Test that should catch it
A unit test for successful fetch should assert content and should fail if the coroutine body is not awaited.

#### What this teaches
Calling an async function creates work to be awaited; it does not run like a normal function call.

#### Common wrong fixes
Do not fix this by making the fake client synchronous; that hides the production behavior.

### Experiment 2: Block the event loop with time.sleep

#### How to cause it
Inside an async retry loop, replace `await asyncio.sleep(delay)` with `time.sleep(delay)`.

#### Expected error
Concurrent fake requests run one after another, and elapsed time becomes roughly the sum of all sleeps.

#### How to inspect
Measure with `time.perf_counter()` around `asyncio.gather` and compare against the expected concurrent time.

#### How to fix
Use `await asyncio.sleep(delay)` for async waiting.

#### Test that should catch it
A timing test with five 0.1-second waits should complete close to one wave, not five sequential waits.

#### What this teaches
Async code is cooperative; blocking the thread blocks every coroutine on that event loop.

#### Common wrong fixes
Do not increase the semaphore limit to hide the problem; blocked threads still cannot schedule other coroutines.

### Experiment 3: Remove the timeout

#### How to cause it
Remove timeout configuration from `httpx.AsyncClient` and use a fake client whose `get` awaits a very long sleep.

#### Expected error
The test appears to hang instead of failing clearly.

#### How to inspect
Wrap the call in a short test timeout or inspect that no result is returned after the expected time.

#### How to fix
Restore a client timeout and/or wrap the operation with a controlled timeout policy.

#### Test that should catch it
A timeout test should simulate a never-returning request and assert a structured timeout failure.

#### What this teaches
Network code without timeouts can turn one bad connection into a frozen program.

#### Common wrong fixes
Do not solve this by lowering concurrency only; one request can still hang forever.

### Experiment 4: Retry a permanent 404

#### How to cause it
Make the fake response return 404 and let the retry loop treat every HTTPStatusError as retryable.

#### Expected error
The fake client is called `max_attempts` times even though the URL is permanently missing.

#### How to inspect
Assert `client.calls` length and inspect the recorded status code in the FetchResult.

#### How to fix
Add a branch that returns immediately for 404 or other non-retryable client errors.

#### Test that should catch it
A 404 test should assert exactly one attempt.

#### What this teaches
Retries are a policy decision; permanent failures should fail fast.

#### Common wrong fixes
Do not add more backoff for 404; slower wrong behavior is still wrong behavior.

### Experiment 5: Launch unbounded concurrency

#### How to cause it
Remove the semaphore and run 100 or more fake requests that record in-flight count.

#### Expected error
The maximum in-flight count jumps to the full number of URLs.

#### How to inspect
Use a fake client counter that increments on entry and decrements on exit to inspect peak concurrency.

#### How to fix
Reintroduce `asyncio.Semaphore(limit)` around the actual request.

#### Test that should catch it
A concurrency-limit test should assert peak in-flight count is less than or equal to the configured limit.

#### What this teaches
Concurrency must be bounded to protect memory, local resources, and remote services.

#### Common wrong fixes
Do not rely on gather alone as a rate limiter; gather schedules all awaitables you give it.

### Experiment 6: Swallow cancellation

#### How to cause it
Catch `Exception` or `BaseException` around an awaited operation and return a success-like value when cancellation occurs.

#### Expected error
Timeout or cancellation tests may return `None` or a misleading result instead of stopping the task.

#### How to inspect
Create a toy coroutine, cancel it, and inspect whether `asyncio.CancelledError` propagates.

#### How to fix
If cleanup is needed, catch `asyncio.CancelledError`, perform cleanup, and re-raise it.

#### Test that should catch it
A cancellation test should cancel a task and assert cancellation is observed by the caller.

#### What this teaches
Cancellation is part of the event-loop control protocol and should not be hidden by broad handlers.

#### Common wrong fixes
Do not replace cancellation with a generic error string unless the function explicitly owns cancellation semantics.

### Experiment 7: Parse PDF bytes directly in async code

#### How to cause it
After fetching bytes, call a slow CPU parser directly inside the coroutine.

#### Expected error
Other coroutines stop making progress while the parser consumes CPU.

#### How to inspect
Run one fake fast coroutine beside the parser and observe that it cannot finish until parsing yields or ends.

#### How to fix
Send CPU-heavy parsing to the Week 8 ProcessPoolExecutor boundary with `run_in_executor`.

#### Test that should catch it
A timing or scheduling test should prove a fast coroutine can still complete while parsing work is offloaded.

#### What this teaches
Async is for I/O waits; CPU-heavy parsing needs a process pool boundary.

#### Common wrong fixes
Do not mark the parser `async def` unless it actually awaits non-blocking I/O; that only changes the wrapper shape.

### Experiment 8: Leak the AsyncClient lifecycle

#### How to cause it
Construct `httpx.AsyncClient()` without `async with` and forget to close it.

#### Expected error
You may see resource warnings, open connection warnings, or flaky behavior across repeated tests.

#### How to inspect
Run tests with warnings visible and inspect whether the client close path is exercised.

#### How to fix
Use `async with httpx.AsyncClient(...) as client` or explicitly `await client.aclose()` in cleanup.

#### Test that should catch it
A lifecycle test can use a fake context manager to assert enter and exit were called.

#### What this teaches
Network clients own resources; resource cleanup is part of correctness.

#### Common wrong fixes
Do not create a global client casually in beginner code; globals make lifecycle and tests harder.

## 4. Debugging checklist

- Is every async operation awaited?
- Is any `time.sleep` or blocking library call inside `async def`?
- Is the HTTP client opened and closed exactly once per batch or session?
- Is there a timeout for every network request?
- Is retry behavior limited by `max_attempts`?
- Are 404 and other permanent client errors excluded from retry?
- Is concurrency bounded by a semaphore or equivalent local limit?
- Does the batch return one result per input URL?
- Do tests use fake clients instead of real network calls?
- Does CPU-heavy parsing use the Week 8 ProcessPoolExecutor boundary?
- Are cancellation errors re-raised after cleanup?

## 5. Reflection after breaking

- Which failure was easiest to predict?
- Which failure only became obvious after measuring time?
- Which bug produced a misleading success instead of a clear failure?
- Which test would you add first to protect the fetch layer?
- How did the semaphore change runtime and in-flight behavior?
- How did the timeout change the user experience of a hung request?
- How would you explain to a teammate that async fetching and CPU parsing need different tools?
- What rule will you remember before writing the next async function?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
