# Notes - Week 15 Async I/O and Network Fetching

Async I/O is useful when your program spends most of its time waiting. Network fetching is a classic example. While one request waits for a server response, another request can make progress. That is why async fits this week's workload better than multiprocessing.

In Python, an `async def` function defines a coroutine. Calling it does not run it immediately; it returns a coroutine object that must be awaited.

```python
import asyncio


async def hello() -> str:
    await asyncio.sleep(1)
    return "done"
```

To run many I/O-bound tasks concurrently, you can use `asyncio.gather()`.

```python
results = await asyncio.gather(*(fetch(url) for url in urls))
```

For HTTP, libraries like `httpx.AsyncClient` are convenient.

```python
import httpx


async def fetch(url: str) -> str:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
```

Timeouts are essential. Without them, one hanging request can stall the entire workflow. Retries are also useful, but only for failures that may recover, such as temporary network issues or `503` responses. Retries should be bounded and often paired with backoff.

```python
for attempt in range(3):
    try:
        return await client.get(url)
    except httpx.TimeoutException:
        await asyncio.sleep(0.5 * (attempt + 1))
```

Concurrency limits matter too. Just because async can launch hundreds of requests does not mean it should. Use a semaphore to cap in-flight work.

```python
semaphore = asyncio.Semaphore(10)

async with semaphore:
    return await fetch(url)
```

This protects both your machine and the remote service.

Testing async code often uses `pytest.mark.asyncio` or equivalent tooling. The important idea is to make the event loop explicit and to isolate network dependencies with mocks or test servers. You do not want flaky tests that depend on real internet conditions.

Error handling in async systems should preserve partial progress. If you fetch 20 URLs and 2 time out, you probably still want the 18 successes. Return structured results with success and failure detail rather than crashing the whole batch.

Another important difference from multiprocessing: async concurrency is usually single-process and cooperative. Tasks yield control when they `await`. CPU-heavy work still blocks the loop, so do not move PDF parsing into async code just because async feels modern.

This week expands ResearchOps beyond local files. Once the system can fetch remote content or metadata concurrently, it becomes easier to ingest references from APIs, preprint servers, or internal services. The core skill is learning to reason about waiting, timeouts, and partial success without losing clarity.
