<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It - Week 15 Async I/O and Network Fetching

## Intentional failure experiments

### 1. Remove the timeout and hang
Remove `timeout=10.0` from `httpx.AsyncClient`. Replace the fake in your test with one that never returns (have `get()` do `await asyncio.sleep(9999)`). Run the test without `asyncio.wait_for`. Watch it stall. Add a test-level timeout: `@pytest.mark.asyncio(timeout=5)`. Confirm the test fails cleanly instead of hanging forever.

### 2. Unbounded retries
Change `max_attempts=3` to `max_attempts=99999` and have the fake always raise `TimeoutException`. Observe the test loop for a very long time. Add `asyncio.sleep(0)` between each retry attempt so the event loop can cancel it via a timeout. Then fix by adding a proper `max_attempts` guard.

### 3. Blocking the event loop with CPU work
Write a coroutine that runs `sum(i * i for i in range(10_000_000))` (a CPU-bound computation) with no `await`. Put it inside an `asyncio.gather` alongside a fast coroutine that should finish in 0 seconds. Observe that the fast coroutine cannot run until the CPU work finishes. Document: "async does not make CPU work parallel". Fix using `run_in_executor`.

### 4. Mixing sync sleep in async code
Inside an `async def` function, call `time.sleep(2)` instead of `await asyncio.sleep(2)`. Run two of these concurrently with `asyncio.gather`. Measure the time. It takes 4 seconds instead of 2. This is because `time.sleep` blocks the entire thread, including the event loop. The fix: use `await asyncio.sleep(2)` for cooperative waiting.

### 5. Retrying non-recoverable errors
Add a 404 to the fake client. Without any check on status code, your retry loop retries a 404 three times before failing. 404 means "this resource does not exist" — retrying cannot fix it. Add a check: if `status_code == 404`, raise immediately without retrying. Write a test that confirms only one attempt is made for 404.

### 6. Swallowing CancelledError
Inside a coroutine, catch `asyncio.CancelledError` and return `None` instead of re-raising. Then run the coroutine with `asyncio.wait_for(coro, timeout=0.1)`. You expect a `TimeoutError`, but instead get `None` (because the cancellation was swallowed). This breaks the cancellation contract. Fix: always re-raise `CancelledError` after cleanup.

### 7. Semaphore set to 1
Set `asyncio.Semaphore(1)` and run 10 concurrent fetches each taking 100ms. Total time becomes 1 second (sequential). Observe that limiting concurrency to 1 makes async effectively synchronous. Raise to 5 and confirm the time drops to ~200ms. This teaches that semaphore value is a tuning parameter.

### 8. Empty URL list
Call `fetch_batch([])`. Does it raise, return an empty list, or hang? It should return an empty list. `asyncio.gather()` with zero arguments returns `[]` immediately. Write a test that confirms this.

### 9. One bad URL in the middle
Call `fetch_batch(["ok1", "BAD", "ok2"])` where "BAD" raises an exception. Confirm that `ok1` and `ok2` still have content in the result and that `BAD` has an error but content is `None`. This tests that partial failure isolation is working.

---

## Debugging tasks

- Add `print(f"[{asyncio.get_event_loop().time():.2f}] starting {url}")` at the top of your fetch function. Run a batch of 5. Observe the timestamps to confirm concurrent execution (start times should be nearly identical).
- When a test fails with `RuntimeError: no running event loop`, check that your test function is marked `@pytest.mark.asyncio` and that `pytest-asyncio` is installed and configured.
- When async tests are unexpectedly slow, add `asyncio.sleep(0)` at key points to yield to the event loop and allow pending tasks to run.

---

## Edge cases to explore

| Case | Expected behaviour |
|------|-------------------|
| `urls = []` | Return `[]` immediately |
| All URLs raise timeout | Return list of all-error `FetchResult` objects |
| `max_attempts = 0` | Raise immediately or define as "no retries allowed" — document your choice |
| URL returns 200 with empty body | `content = ""`, `error = None` |
| URL returns 429 without `Retry-After` header | Fall back to default backoff |
| Semaphore limit exceeds URL count | Behaves the same as if limit were equal to count |

---

## What did you learn?

- Which mistake was hardest to see without timing measurement?
- What is the observable difference between `time.sleep` and `asyncio.sleep` in an async context?
- How did you decide which failure types are retriable?
- If a colleague says "let's make our PDF parser async to speed it up", how do you respond?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
