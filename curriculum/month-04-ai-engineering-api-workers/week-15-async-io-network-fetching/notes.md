# Notes - Week 15 Async I/O and Network Fetching

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 15 — Async I/O Network Fetching](./README.md) › **notes.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Synchronous vs asynchronous code: the core idea

In synchronous code, statements execute one at a time, in order. Each statement must finish before the next one starts.

```python
import time

def fetch_one(url: str) -> str:
    time.sleep(2)          # pretend this is a network round-trip
    return f"content of {url}"

result_a = fetch_one("https://example.com/a")   # waits 2 seconds
result_b = fetch_one("https://example.com/b")   # waits another 2 seconds
# total: 4 seconds
```

The two requests run sequentially. While waiting for `a` to respond, the program does nothing. The CPU is idle. That is waste.

Asynchronous code allows the program to do useful work while waiting. Instead of blocking until a response arrives, the program suspends that operation and moves on to other work.

```python
import asyncio

async def fetch_one(url: str) -> str:
    await asyncio.sleep(2)   # suspend here; let other tasks run
    return f"content of {url}"

async def fetch_all() -> None:
    results = await asyncio.gather(
        fetch_one("https://example.com/a"),
        fetch_one("https://example.com/b"),
    )
    # total: ~2 seconds (both run concurrently)
```

Both fetches start almost simultaneously. While one waits, the other makes progress. The total time is approximately 2 seconds, not 4.

---

## The event loop

Python's `asyncio` module runs on an event loop. The event loop is a scheduler that manages all running coroutines. It works like this:

1. You start the event loop with `asyncio.run(main())`.
2. The loop calls your `main` coroutine.
3. When a coroutine hits `await`, it tells the loop "I'm waiting for something — run someone else."
4. The loop picks the next ready coroutine and runs it.
5. When the awaited operation finishes, the loop resumes the original coroutine.

This happens in a single thread. There is no parallelism. Coroutines take turns using the CPU. They are cooperative: they voluntarily yield control at `await` points.

---

## What is a coroutine?

A coroutine is a function defined with `async def`. Calling it does not run it — it returns a coroutine object. The coroutine runs only when it is awaited or given to the event loop.

```python
async def greet(name: str) -> str:       # line 1: define a coroutine
    await asyncio.sleep(0)               # line 2: yield to the event loop (no-op sleep)
    return f"Hello, {name}"             # line 3: return a value

result = await greet("Alice")            # line 4: run the coroutine and get the result
```

Line 1: `async def` marks this as a coroutine function.

Line 2: `await asyncio.sleep(0)` suspends for zero seconds, giving the event loop a chance to run other tasks. This is often used in tests to simulate a yield point.

Line 3: returns the result normally.

Line 4: `await greet("Alice")` runs the coroutine and waits for its result. You can only `await` inside an `async def` function.

---

## Tasks

A task is a scheduled coroutine. When you create a task, the event loop schedules it to run independently of the current coroutine.

```python
async def main() -> None:
    task_a = asyncio.create_task(fetch_one("url_a"))   # line 1: schedule
    task_b = asyncio.create_task(fetch_one("url_b"))   # line 2: schedule
    result_a = await task_a                            # line 3: wait for result
    result_b = await task_b                            # line 4: wait for result
```

Line 1–2: create two tasks. They start running immediately (as soon as the event loop gets control).

Line 3–4: wait for each to finish. If `task_a` finishes first, awaiting `task_b` does not restart `task_a`.

Using `asyncio.gather` is more concise for multiple tasks:

```python
results = await asyncio.gather(fetch_one("url_a"), fetch_one("url_b"))
```

`gather` collects all results in order, even if the tasks complete out of order.

---

## I/O-bound vs CPU-bound work

This is the most important distinction for async programming.

**I/O-bound work** spends most of its time waiting: waiting for a network response, waiting for a disk read, waiting for a database query. The CPU is idle during that wait. Async helps here because while one I/O operation waits, the event loop runs other coroutines.

**CPU-bound work** spends most of its time computing: parsing a PDF, running a machine learning model, sorting a huge list. The CPU is fully occupied. Async does NOT help here. A coroutine doing CPU-heavy work blocks the event loop for the entire duration, preventing all other coroutines from running.

```
Async waits efficiently.
Async does not make CPU-heavy work magically faster.
```

This rule is worth repeating until it is automatic.

Consequences:
- Network fetching → async. Good fit.
- PDF parsing → synchronous or multiprocessing. Not async.
- Embedding computation → synchronous or multiprocessing. Not async.
- Database queries → async (with an async driver like `aiosqlite`). Good fit.

If you put PDF parsing inside an `async def` function, you block the event loop. Every other coroutine stalls until parsing completes. This is worse than just running it synchronously.

---

## Async HTTP client

For async HTTP requests, use `httpx.AsyncClient`:

```python
import httpx


async def fetch(url: str) -> str:                         # line 1
    async with httpx.AsyncClient(timeout=10.0) as client: # line 2
        response = await client.get(url)                  # line 3
        response.raise_for_status()                       # line 4
        return response.text                              # line 5
```

Line 1: async function — it can be awaited.

Line 2: `async with` creates the client and ensures it is closed when the block exits, even if an exception is raised. `timeout=10.0` sets a 10-second timeout on the request.

Line 3: `await client.get(url)` suspends this coroutine while waiting for the server to respond. The event loop runs other tasks during this wait.

Line 4: raises `httpx.HTTPStatusError` if the status code indicates failure (4xx, 5xx).

Line 5: returns the response body as a string.

---

## Timeouts

Without a timeout, a hanging server can stall your coroutine indefinitely.

```python
async with httpx.AsyncClient(timeout=10.0) as client:
    try:
        response = await client.get(url)
    except httpx.TimeoutException:
        # handle timeout
        raise
```

Always set a timeout. A good default for academic APIs is 10–30 seconds. For internal services, 5 seconds is usually generous.

`httpx.Timeout` lets you set different timeouts for connect, read, and write phases:
```python
timeout = httpx.Timeout(connect=5.0, read=30.0, write=10.0)
```

---

## Retries and backoff

Not all failures are permanent. A `503 Service Unavailable` might resolve in a second. A timeout might be a brief network blip. Retrying with a short wait can recover from these.

```python
async def fetch_with_retry(url: str, max_attempts: int = 3) -> str:
    last_error: Exception | None = None
    for attempt in range(max_attempts):                       # line 1
        try:
            return await fetch(url)                           # line 2
        except (httpx.TimeoutException, httpx.HTTPStatusError) as exc:
            last_error = exc                                  # line 3
            wait = 0.5 * (attempt + 1)                        # line 4
            await asyncio.sleep(wait)                         # line 5
    raise RuntimeError(f"Failed after {max_attempts} attempts") from last_error  # line 6
```

Line 1: try up to `max_attempts` times.

Line 2: if the fetch succeeds, return immediately.

Line 3: save the exception.

Line 4: compute wait time. First retry waits 0.5s, second waits 1.0s, third waits 1.5s. This is linear backoff.

Line 5: `await asyncio.sleep(wait)` suspends without blocking. The event loop runs other tasks during the wait.

Line 6: if all attempts fail, raise a descriptive error that wraps the last exception.

**When to retry:** temporary failures — timeouts, 429 (rate limit), 503 (temporary unavailability).

**When not to retry:** permanent failures — 404 (not found), 400 (bad request), 401 (unauthorized). Retrying these wastes time and may cause harm.

---

## Concurrency limits with semaphores

Just because async can launch hundreds of concurrent requests does not mean it should. Too many concurrent requests can:
- Overwhelm the remote server (especially academic APIs).
- Hit your machine's file descriptor limits.
- Trigger rate limiting (429 responses).

A semaphore is a counter that limits how many coroutines can be in a critical section simultaneously.

```python
semaphore = asyncio.Semaphore(10)          # line 1: allow at most 10 concurrent


async def fetch_bounded(url: str) -> str:
    async with semaphore:                  # line 2: acquire before fetching
        return await fetch(url)            # line 3: fetch (semaphore released when block exits)
```

Line 1: create a semaphore with a limit of 10.

Line 2: `async with semaphore` decrements the counter. If the counter is already 0, this coroutine suspends until another coroutine releases the semaphore.

Line 3: do the actual work. When the `async with` block exits, the semaphore is released (counter incremented).

A good default limit for public academic APIs is 5–10 concurrent requests.

---

## Cancellation

Sometimes you want to abandon a running operation. `asyncio.wait_for` adds a deadline:

```python
try:
    result = await asyncio.wait_for(fetch(url), timeout=15.0)
except asyncio.TimeoutError:
    # the coroutine was cancelled
    pass
```

When the timeout expires, `asyncio` raises `CancelledError` inside the coroutine at its next `await` point. The coroutine can catch it to do cleanup, but must re-raise it (or let it propagate) to actually cancel.

Do not silently swallow `CancelledError` in most cases. If you catch it for cleanup, re-raise it:

```python
try:
    result = await some_operation()
except asyncio.CancelledError:
    await cleanup()
    raise  # always re-raise CancelledError
```

---

## Testing async code

Use `pytest-asyncio` to write async test functions:

```bash
pip install pytest-asyncio
```

```python
import pytest


@pytest.mark.asyncio
async def test_fetch_success() -> None:
    result = await fetch_with_retry("https://httpbin.org/get")
    assert result is not None
```

However, tests must not depend on real network access. Use a fake HTTP client:

```python
class FakeHttpClient:
    def __init__(self, responses: dict[str, str]) -> None:
        self._responses = responses

    async def get(self, url: str) -> "FakeResponse":
        if url not in self._responses:
            raise httpx.TimeoutException(f"No mock for {url}")
        return FakeResponse(self._responses[url])


class FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text
        self.status_code = 200

    def raise_for_status(self) -> None:
        pass
```

Inject the fake in tests. This gives you complete control over responses, timeouts, and error conditions without any network activity.

---

## Partial failure and batch results

When fetching a batch of URLs, do not crash the entire batch if one URL fails. Return structured results:

```python
from dataclasses import dataclass


@dataclass
class FetchResult:
    url: str
    content: str | None
    error: str | None


async def fetch_batch(urls: list[str]) -> list[FetchResult]:
    async def fetch_one_safe(url: str) -> FetchResult:
        try:
            content = await fetch_with_retry(url)
            return FetchResult(url=url, content=content, error=None)
        except Exception as exc:
            return FetchResult(url=url, content=None, error=str(exc))

    return list(await asyncio.gather(*(fetch_one_safe(url) for url in urls)))
```

This returns one `FetchResult` per URL. Successes have `content`. Failures have `error`. The caller decides what to do with partial failures.

---

## Summary

- Synchronous code waits serially. One operation at a time.
- Asynchronous code suspends at `await` points, letting the event loop run other coroutines.
- The event loop is a single-threaded cooperative scheduler.
- A coroutine is an `async def` function. Calling it returns a coroutine object; it only runs when awaited.
- A task is a scheduled coroutine. `asyncio.gather` runs multiple tasks concurrently.
- **Async helps I/O-bound work. It does not help CPU-bound work.**
- PDF parsing, embedding computation, and data transformation are CPU-bound. Do not put them in async paths.
- Network fetching is I/O-bound. Always use async for it.
- Always set timeouts. Without them, one hanging server stalls your program.
- Retry only recoverable failures. Do not retry 404 or 400.
- Use semaphores to cap concurrent requests and protect remote services.
- Use `FakeHttpClient` in tests — never real network access.
- Return structured batch results that capture partial failures.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 15 — Async I/O Network Fetching** · *notes.md — the textbook chapter* (step 2 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [README](./README.md)
- ▶ **Next:** [exercises.md](./exercises.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. **➡ [notes.md](./notes.md) ← you are here**
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 16](../../../curriculum/month-04-ai-engineering-api-workers/week-16-local-worker-job-system/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 16 — Local Worker & Job System](../../../curriculum/month-04-ai-engineering-api-workers/week-16-local-worker-job-system/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 4 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 4 overview](../README.md) · [📄 Week 15 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
