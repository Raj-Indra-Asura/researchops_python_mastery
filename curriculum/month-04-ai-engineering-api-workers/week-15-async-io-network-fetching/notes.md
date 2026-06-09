<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 15 Async I/O and Network Fetching

This is one unified chapter. There is no beginner summary followed by older notes.
Every section below belongs to the main learning path for Week 15.
The theme is simple: ResearchOps should wait on many network requests without freezing the rest of the program.
The boundary is equally important: async helps network and other I/O waits, not CPU-heavy parsing or ML computation.

## 1. Chapter overview

Week 15 teaches async I/O through a concrete ResearchOps problem: fetching paper metadata and paper files from the network.
The learner has already built local modeling, storage, search, and an API surface; now the system must talk to remote services responsibly.
A remote service might be arXiv metadata, a publisher landing page, or a PDF URL recorded in a paper record.
Remote services are slow compared with memory and local Python objects.
A local function call may finish in microseconds.
A local SQLite query may finish in milliseconds.
A network request may wait hundreds of milliseconds or many seconds before bytes arrive.
If ResearchOps fetches ten URLs one at a time, most of the total time is wasted waiting.
Async I/O lets one Python thread manage many waiting operations at once.
The event loop starts request A, then while request A waits for the network, it can start request B.
When request B waits, the loop can start request C.
This is concurrency, not CPU parallelism.
Concurrency means multiple tasks are in progress during the same time period.
Parallelism means multiple pieces of CPU work are executing at the exact same instant.
Week 15 focuses on concurrency for I/O-bound work.
PDF parsing remains CPU-bound work and still belongs in the Week 8 ProcessPoolExecutor boundary.
Embedding computation remains CPU-bound or accelerator-bound work and does not become faster just because the function is marked async.
The visible milestone is a fetch layer that can fetch metadata or PDFs with timeouts, retries, rate limiting, and structured results.
The hidden milestone is judgment: knowing when async is the right tool and when it is the wrong tool.
By the end, you should be able to explain what happens when Python reaches an await expression.
You should be able to write a small async function and run it with asyncio.run from a synchronous CLI command.
You should be able to use httpx.AsyncClient without leaking open connections.
You should be able to bound concurrent requests with asyncio.Semaphore.
You should be able to retry transient network failures without retrying permanent client errors forever.
You should be able to add tests that simulate network behavior without touching the real network.

Study this chapter in this order:
1. Read the mental model before memorizing syntax.
2. Run the smallest coroutine example and observe that calling an async function does not run its body immediately.
3. Compare sequential awaits with asyncio.gather and measure elapsed time.
4. Add a timeout and prove that a hung request does not hang the whole program forever.
5. Add a semaphore and prove that ResearchOps behaves politely toward remote services.
6. Add retry logic and decide which failures deserve another attempt.
7. Write fake-client tests so the learning remains deterministic and offline.
8. Explain why CPU-bound parsing still goes through ProcessPoolExecutor instead of async def.

## 2. What you already know from previous weeks

Week 1 gave you the project scaffold and the habit of separating source code from tests.
Week 2 introduced files, paths, exceptions, and logging, which matter because network code must report failures clearly.
Week 3 strengthened domain modeling with dataclasses, which matters because fetch results should be structured values, not loose dictionaries.
Week 4 made the CLI a real entry point, which matters because a synchronous command may need to start async work safely.
Week 5 introduced SQLite storage, which matters because fetched metadata eventually becomes stored paper records.
Week 6 and later service-layer work taught you to keep business logic out of CLI code.
Week 8 introduced ProcessPoolExecutor for CPU-heavy operations.
That Week 8 boundary is still active in Week 15.
Do not move PDF parsing into the event loop.
Do not make a slow parser async merely because you want it to be faster.
Week 13 introduced search and embeddings, which may consume fetched text later, but this chapter does not build new search features.
Week 14 introduced FastAPI and the idea that web servers already run event loops.
That matters because nested event loops are a common beginner mistake.
You already know that tests should not depend on external services.
That principle becomes stricter here because real network tests are slow, flaky, and impolite.
You already know that architecture boundaries protect the project from becoming tangled.
The fetch layer is infrastructure because it talks to the outside world.
Service code should depend on an interface or injected client shape rather than constructing a global HTTP client everywhere.

The most important previous-week connection is this:

> Async fetching collects bytes from the outside world; ProcessPoolExecutor handles expensive CPU work after those bytes arrive.

Keep those two responsibilities separate for the rest of the chapter.

## 3. What problem this week solves

ResearchOps needs paper information before it can classify, store, search, or summarize papers.
Some paper information lives in local files, but much of it lives behind URLs.
A user may ask for metadata for a search query such as "graph neural networks".
A user may provide a list of paper URLs to fetch.
A user may provide PDF links that must be downloaded before parsing.
The naive approach is sequential fetching.
Sequential fetching means request one URL, wait until it finishes, request the next URL, wait until it finishes, and repeat.
Sequential fetching is easy to understand, but it wastes time when each operation is mostly waiting on a remote server.
The async approach starts several requests, then lets Python switch between them whenever one is waiting.
The practical problem is not only speed.
The practical problem is safe speed.
Without timeouts, a dead connection can hang forever.
Without retries, one temporary network blip can fail a whole batch.
Without rate limits, ResearchOps can overload a polite public API.
Without structured results, one bad URL can hide which other URLs succeeded.
Without tests, async behavior becomes hard to reason about.
Week 15 solves these problems together.

A good Week 15 fetcher should answer these questions for every URL:
- Did the request succeed?
- If it succeeded, what bytes or text did we receive?
- If it failed, what error should the user see?
- Was the failure temporary or permanent?
- How many attempts were made?
- Did we respect the concurrency limit?
- Did we leave network resources open?

## 4. Beginner mental model

Imagine one librarian at a desk.
The librarian receives ten requests for papers stored in ten different archive rooms.
A blocking librarian walks to room one, waits for the elevator, gets the paper, returns, then starts room two.
An async librarian sends a request slip to room one, then while room one is preparing the paper, sends a slip to room two.
The librarian is still one person.
The librarian is not reading ten papers at the exact same instant.
The improvement comes from not standing idle while someone else is doing the waiting.
In Python, the librarian is the event loop.
The request slips are coroutines scheduled as tasks.
The moments when the librarian can switch tasks are await points.
A coroutine must cooperate by reaching await.
If a coroutine starts a giant CPU loop and never awaits, the event loop cannot switch away from it.
That is why CPU-bound PDF parsing blocks async code.
The mental model is: async does not interrupt your code at arbitrary lines.
Async switches at explicit await points.
When you see await, read it as: this operation may pause here and let other scheduled work run.
When the awaited operation is ready, the event loop resumes the coroutine after the await expression.

Use this four-question checklist whenever async feels mysterious:
- What operation is waiting?
- Where is the await point?
- What other coroutine can run while this one waits?
- What happens if the awaited operation never finishes?

## 5. Core vocabulary

- **I/O-bound:** Work whose time is mostly spent waiting for input or output, such as network responses, disk reads, or database replies.
- **CPU-bound:** Work whose time is mostly spent using the processor, such as PDF parsing, image processing, compression, or large numeric loops.
- **Coroutine function:** A function defined with async def. Calling it creates a coroutine object instead of running the body immediately.
- **Coroutine object:** The awaitable object returned by calling an async function.
- **await:** A keyword that pauses the current coroutine until another awaitable has a result, while allowing the event loop to run other tasks.
- **Event loop:** The scheduler that drives coroutines, notices when I/O is ready, and resumes tasks after awaits complete.
- **Task:** A scheduled coroutine managed by the event loop.
- **asyncio.gather:** A helper that waits for multiple awaitables and returns their results in the same order as the input awaitables.
- **httpx.AsyncClient:** An async HTTP client that can make non-blocking network requests when used with await.
- **Timeout:** A maximum allowed wait before treating an operation as failed.
- **Retry:** A second or later attempt after a failure that might be temporary.
- **Backoff:** A strategy that waits longer between repeated retry attempts.
- **Rate limiting:** A deliberate cap on request frequency or concurrency so the client does not overwhelm a server.
- **Semaphore:** An asyncio primitive that allows only a fixed number of coroutines into a protected section at the same time.
- **Cancellation:** A signal that a coroutine should stop because its result is no longer needed or a timeout occurred.
- **Structured result:** A dataclass or model that records success and failure fields explicitly instead of throwing away context.

Vocabulary is useful only when tied to behavior.
If you cannot draw where the event loop waits and resumes, reread the mental model before writing more code.

## 6. Concept explanations from first principles

### Synchronous waiting

Normal Python code is synchronous by default.
Synchronous means the next line does not run until the current line finishes.
If line 1 starts a request and the request takes three seconds, line 2 waits three seconds.
This is not bad by itself.
Synchronous code is often simpler and is the correct choice for simple local operations.
The problem appears when the program has many independent waits.

### Asynchronous waiting

Asynchronous code separates "starting an operation" from "waiting for the result".
When a coroutine awaits a network request, the event loop can resume another coroutine whose network response is ready.
This works because network libraries such as httpx.AsyncClient integrate with the event loop.
A regular blocking library does not become non-blocking just because you call it from async def.
That is why using requests.get inside async def is a bug for this chapter.

### Coroutines are lazy until awaited

A beginner often expects async def to behave like def.
It does not.
Calling an async function creates a coroutine object.
The body begins running only when the coroutine is awaited, passed to asyncio.run, or scheduled as a task.
If you forget await, Python may warn that a coroutine was never awaited.
That warning means your async function did not actually execute.

### gather starts independent waits together

asyncio.gather is useful when several operations can happen independently.
Fetching URL A usually does not need the result of fetching URL B.
That independence makes batch fetching a perfect gather example.
gather preserves result order.
If the input order is [url_a, url_b, url_c], the result order matches that input order even if url_c finishes first.
That property helps CLI output and tests stay predictable.

### Timeouts are part of correctness

A network request that never returns is not merely slow.
It is a correctness problem because the caller may wait forever.
Timeouts turn an infinite wait into a controlled failure.
Controlled failures can be retried, logged, shown to users, or recorded in structured results.
Every production-style network request should have a timeout.

### Retries require judgment

Retries are useful for temporary failures such as timeouts, connection resets, and 503 responses.
Retries are harmful for permanent failures such as 404 Not Found or 400 Bad Request.
Retrying a 404 usually means asking the server the same impossible question several times.
Retrying too quickly can make an outage worse.
Backoff slows repeated attempts so the remote service has time to recover.
Rate-limit responses such as 429 deserve special care because the server is explicitly telling the client to slow down.

### Async is not a magic speed button

Async code improves throughput when tasks spend time waiting outside Python.
Async code does not make a CPU loop run on multiple cores.
If a PDF parser consumes three seconds of CPU, putting it in async def still consumes the event loop thread for three seconds.
The correct ResearchOps boundary is to fetch bytes asynchronously, then hand CPU-heavy parsing to the Week 8 ProcessPoolExecutor.
After parsing completes, async code may resume for I/O steps such as writing a response or fetching another URL.

## 7. ResearchOps-specific application

In ResearchOps, async fetching belongs in infrastructure code that knows how to communicate with external HTTP services.
A fetch module may expose functions such as fetch_text, fetch_bytes, fetch_many, or fetch_arxiv_metadata.
Those functions should return project-specific structured results rather than leaking every httpx detail upward.
The CLI can call an application service, and that service can call the fetcher through an injected dependency.
The CLI remains responsible for argument parsing and printing.
The service remains responsible for workflow decisions.
The fetcher remains responsible for HTTP behavior.
A metadata fetch for arXiv should set query parameters clearly.
A PDF download should treat the response as bytes, not text.
A batch fetch should accept a concurrency limit because public research services should not be hammered with unbounded requests.
A result for one URL should not disappear because another URL failed.
That partial-failure rule matters in research workflows because a collection may contain one dead link among many useful links.
The user should see which URLs succeeded, which failed, and why.
The system should log enough context to debug failures later.
The system should not store raw exception objects in domain models when a string or error code is enough for display.
The system should not require internet access during unit tests.

A simple Week 15 ownership map looks like this:
- `core/` defines stable models or protocols if the fetch behavior becomes part of a service boundary.
- `services/` decides when metadata fetching is part of a user workflow.
- `cli/` starts the workflow with `asyncio.run` only at the outer synchronous edge.
- `infrastructure` or a fetch-specific module owns `httpx.AsyncClient` usage.
- `tests/` use fake clients and do not make real HTTP requests.

## 8. Code examples with line-by-line explanation

### Example 1: the smallest coroutine

```python
import asyncio

async def greet(name: str) -> str:
    await asyncio.sleep(1)
    return f"Hello, {name}"

message = asyncio.run(greet("Ada"))
print(message)
```

Line-by-line explanation:
- Line 1 imports asyncio, the standard library package that provides the event loop and coroutine helpers.
- Line 3 defines a coroutine function because it uses async def instead of def.
- Line 3 also says the function expects a string name and eventually produces a string.
- Line 4 awaits asyncio.sleep(1), which is a non-blocking timer controlled by the event loop.
- Line 4 does not freeze the event loop; other scheduled coroutines could run during that one second.
- Line 5 resumes after the sleep completes and builds the greeting string.
- Line 7 calls greet("Ada"), receives a coroutine object, and passes it to asyncio.run.
- Line 7 asyncio.run creates an event loop, runs the coroutine to completion, then closes the loop.
- Line 8 prints the final string after the coroutine has completed.

### Example 2: sequential awaits versus gather

```python
import asyncio
import time

async def fake_fetch(label: str) -> str:
    await asyncio.sleep(1)
    return f"result for {label}"

async def fetch_sequential() -> list[str]:
    first = await fake_fetch("paper-1")
    second = await fake_fetch("paper-2")
    third = await fake_fetch("paper-3")
    return [first, second, third]

async def fetch_concurrent() -> list[str]:
    results = await asyncio.gather(
        fake_fetch("paper-1"),
        fake_fetch("paper-2"),
        fake_fetch("paper-3"),
    )
    return list(results)

start = time.perf_counter()
print(asyncio.run(fetch_concurrent()))
print(time.perf_counter() - start)
```

Line-by-line explanation:
- Line 1 imports asyncio for coroutine scheduling.
- Line 2 imports time so the example can measure elapsed time.
- Line 4 defines a fake network request that behaves like I/O.
- Line 5 awaits an async sleep, which simulates waiting for a remote server.
- Line 6 returns a label so you can see which request produced which result.
- Line 8 defines the sequential version.
- Line 9 waits for paper-1 to finish before paper-2 even starts.
- Line 10 waits for paper-2 to finish before paper-3 starts.
- Line 11 waits for paper-3 last, so total time is about three seconds.
- Line 12 returns the results in ordinary list form.
- Line 14 defines the concurrent version.
- Line 15 awaits asyncio.gather, which schedules all three fake_fetch calls together.
- Lines 16 to 18 create three independent coroutine objects.
- Line 20 converts gather output to a list because gather returns a tuple-like collection of results.
- Line 22 records a high-resolution start time.
- Line 23 runs the concurrent coroutine from synchronous top-level code.
- Line 24 prints elapsed time, which should be close to one second instead of three.

### Example 3: a structured fetch result

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class FetchResult:
    url: str
    status_code: int | None
    content: bytes | None
    error: str | None
    attempts: int

    @property
    def succeeded(self) -> bool:
        return self.error is None and self.content is not None
```

Line-by-line explanation:
- Line 1 imports dataclass so the result can be a small explicit value object.
- Line 3 decorates FetchResult as a frozen dataclass, meaning fields cannot be reassigned after creation.
- Line 4 defines the class that represents one URL outcome.
- Line 5 stores the URL so errors remain connected to the original input.
- Line 6 stores the HTTP status when one exists; network timeouts may not have a status code.
- Line 7 stores response bytes for PDF downloads or encoded metadata responses.
- Line 8 stores a displayable error string when the fetch fails.
- Line 9 stores how many attempts were made, which helps tests and debugging.
- Line 11 creates a read-only computed property.
- Line 12 treats the result as successful only when there is content and no error.

### Example 4: fetching one URL with httpx.AsyncClient

```python
import httpx

async def fetch_bytes(client: httpx.AsyncClient, url: str) -> bytes:
    response = await client.get(url)
    response.raise_for_status()
    return response.content
```

Line-by-line explanation:
- Line 1 imports httpx, the HTTP client library used by this chapter.
- Line 3 defines an async function because network I/O should not block the event loop.
- Line 3 accepts a client instead of constructing one inside the function, which makes testing easier.
- Line 3 returns bytes because PDFs and metadata payloads may not be plain Python strings yet.
- Line 4 awaits the GET request; this is where the event loop can run other tasks while the server responds.
- Line 5 raises an exception for HTTP errors such as 404 or 500.
- Line 6 returns the raw response bytes after the status has been checked.

### Example 5: owning the AsyncClient lifecycle

```python
import httpx

async def fetch_many_bytes(urls: list[str]) -> list[bytes]:
    timeout = httpx.Timeout(10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        responses = await asyncio.gather(
            *(fetch_bytes(client, url) for url in urls)
        )
    return list(responses)
```

Line-by-line explanation:
- Line 1 imports httpx for the async client and timeout configuration.
- Line 3 defines a batch fetch function that accepts a list of URLs.
- Line 4 creates a ten-second timeout that applies to client operations.
- Line 5 opens an AsyncClient using async with so network connections are cleaned up automatically.
- Line 6 awaits gather so all URL fetches can make progress concurrently.
- Line 7 uses a generator expression to create one coroutine per URL.
- Line 8 closes the gather call.
- Line 9 runs after the async with block has closed the client.
- Line 9 converts the gathered results to a regular list.
- This example assumes every request succeeds; production code should capture partial failures.

### Example 6: bounded concurrency with a semaphore

```python
import asyncio
import httpx

async def fetch_many_bounded(urls: list[str], limit: int = 5) -> list[bytes]:
    semaphore = asyncio.Semaphore(limit)
    timeout = httpx.Timeout(10.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        async def fetch_one(url: str) -> bytes:
            async with semaphore:
                return await fetch_bytes(client, url)

        results = await asyncio.gather(*(fetch_one(url) for url in urls))
    return list(results)
```

Line-by-line explanation:
- Line 1 imports asyncio for the semaphore and gather.
- Line 2 imports httpx for the HTTP client.
- Line 4 defines a batch fetcher with a default maximum of five simultaneous requests.
- Line 5 creates the semaphore; only five coroutines can hold it when limit is five.
- Line 6 creates the timeout configuration.
- Line 8 opens one shared AsyncClient for the whole batch.
- Line 9 defines an inner helper that fetches one URL.
- Line 10 waits until the semaphore has an available slot.
- Line 11 performs the actual fetch while holding the slot.
- Line 11 releases the slot automatically when the async with block exits.
- Line 13 schedules one fetch_one coroutine per URL.
- Line 14 returns the ordered results after all fetches finish.

### Example 7: partial failure isolation

```python
async def fetch_one_result(client: httpx.AsyncClient, url: str) -> FetchResult:
    attempts = 1
    try:
        response = await client.get(url)
        response.raise_for_status()
        return FetchResult(
            url=url,
            status_code=response.status_code,
            content=response.content,
            error=None,
            attempts=attempts,
        )
    except httpx.HTTPError as exc:
        status_code = None
        if isinstance(exc, httpx.HTTPStatusError):
            status_code = exc.response.status_code
        return FetchResult(
            url=url,
            status_code=status_code,
            content=None,
            error=str(exc),
            attempts=attempts,
        )
```

Line-by-line explanation:
- Line 1 defines a helper that always returns FetchResult instead of letting HTTP errors escape.
- Line 2 records the attempt count for this simple no-retry version.
- Line 3 begins the protected section.
- Line 4 awaits the network request.
- Line 5 turns bad HTTP statuses into exceptions.
- Lines 6 to 12 build a successful FetchResult with content and no error.
- Line 13 catches httpx HTTP-related failures.
- Line 14 starts with no known status code because timeouts and connection errors do not have one.
- Line 15 checks whether the exception came from an HTTP response status.
- Line 16 extracts the response status code for errors such as 404 or 500.
- Lines 17 to 23 build a failed FetchResult while preserving the URL and attempt count.

### Example 8: retry with backoff and non-retryable statuses

```python
import asyncio
import httpx

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

async def fetch_with_retry(
    client: httpx.AsyncClient,
    url: str,
    max_attempts: int = 3,
) -> FetchResult:
    for attempt in range(1, max_attempts + 1):
        try:
            response = await client.get(url)
            if response.status_code == 404:
                return FetchResult(url, 404, None, "not found", attempt)
            response.raise_for_status()
            return FetchResult(url, response.status_code, response.content, None, attempt)
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status not in RETRYABLE_STATUS_CODES or attempt == max_attempts:
                return FetchResult(url, status, None, str(exc), attempt)
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            if attempt == max_attempts:
                return FetchResult(url, None, None, str(exc), attempt)
        await asyncio.sleep(2 ** (attempt - 1))
    return FetchResult(url, None, None, "unreachable retry state", max_attempts)
```

Line-by-line explanation:
- Line 1 imports asyncio for the backoff sleep.
- Line 2 imports httpx exception types.
- Line 4 names statuses that might be temporary or rate-limit related.
- Line 6 starts an async retry helper.
- Lines 7 to 9 list the injected client, target URL, and attempt limit.
- Line 11 loops over attempt numbers starting at one so logs match human language.
- Line 12 begins the try block for one attempt.
- Line 13 awaits the HTTP request.
- Line 14 treats 404 as permanent and returns immediately.
- Line 15 records a clear user-facing not found error.
- Line 16 raises for other bad statuses.
- Line 17 returns success with the status, content, and attempt count.
- Line 18 catches status-code errors such as 500 or 503.
- Line 19 extracts the status code from the response.
- Line 20 stops retrying if the status is not retryable or this was the final attempt.
- Line 21 returns a failed structured result.
- Line 22 catches timeout and connection failures, which are common transient network errors.
- Line 23 checks whether there are attempts left.
- Line 24 returns failure after the final temporary-error attempt.
- Line 25 waits before the next attempt; the delay sequence is 1, then 2, then 4 seconds.
- Line 26 is defensive; normal control flow should return before reaching it.

### Example 9: reading Retry-After for 429

```python
def retry_after_seconds(response: httpx.Response) -> float | None:
    raw_value = response.headers.get("Retry-After")
    if raw_value is None:
        return None
    try:
        return float(raw_value)
    except ValueError:
        return None
```

Line-by-line explanation:
- Line 1 defines a small synchronous helper because parsing a header is CPU-trivial and does not need async.
- Line 2 reads the Retry-After header if the server provided one.
- Line 3 checks for the missing-header case.
- Line 4 returns None to mean "use the default backoff".
- Line 5 starts a try block because headers are strings and may not be valid numbers.
- Line 6 converts values such as "2" or "0.5" into seconds.
- Line 7 catches invalid header values.
- Line 8 returns None for invalid values so the caller can fall back safely.

### Example 10: keeping CPU parsing out of the event loop

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor


def parse_pdf_bytes(pdf_bytes: bytes) -> str:
    return slow_pdf_parser(pdf_bytes)

async def fetch_then_parse(
    client: httpx.AsyncClient,
    executor: ProcessPoolExecutor,
    url: str,
) -> str:
    pdf_bytes = await fetch_bytes(client, url)
    loop = asyncio.get_running_loop()
    text = await loop.run_in_executor(executor, parse_pdf_bytes, pdf_bytes)
    return text
```

Line-by-line explanation:
- Line 1 imports asyncio so the coroutine can access the running event loop.
- Line 2 imports ProcessPoolExecutor, the Week 8 tool for CPU-heavy work.
- Line 5 defines a normal synchronous parsing function.
- Line 6 calls the slow parser in ordinary sync code because CPU work itself is not async.
- Line 8 defines an async workflow that combines network I/O and CPU parsing safely.
- Line 9 accepts the async HTTP client.
- Line 10 accepts the process pool instead of creating a new pool for every URL.
- Line 11 accepts the URL to download.
- Line 13 asynchronously fetches the PDF bytes.
- Line 14 gets the currently running event loop.
- Line 15 sends the CPU-bound parser to the process pool and awaits its result without blocking the loop.
- Line 16 returns the parsed text after the worker process finishes.

### Example 11: fake client testing shape

```python
class FakeResponse:
    def __init__(self, status_code: int, content: bytes) -> None:
        self.status_code = status_code
        self.content = content
        self.headers: dict[str, str] = {}

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            request = httpx.Request("GET", "https://example.test/paper")
            response = httpx.Response(self.status_code, request=request)
            raise httpx.HTTPStatusError("bad status", request=request, response=response)

class FakeAsyncClient:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self.responses = responses
        self.calls: list[str] = []

    async def get(self, url: str) -> FakeResponse:
        self.calls.append(url)
        return self.responses.pop(0)
```

Line-by-line explanation:
- Line 1 defines a fake response for unit tests.
- Line 2 accepts a status code and byte content.
- Line 3 stores the status code like httpx.Response does.
- Line 4 stores the content bytes.
- Line 5 provides headers because retry logic may inspect Retry-After.
- Line 7 implements the method production code expects to call.
- Line 8 treats 400 and above as errors.
- Line 9 creates a request object because httpx.HTTPStatusError requires one.
- Line 10 creates a response object with the failing status.
- Line 11 raises the same kind of exception production httpx code would raise.
- Line 13 defines a fake async client.
- Line 14 accepts a queue of responses that tests control.
- Line 15 stores those responses.
- Line 16 records requested URLs so tests can assert attempt counts.
- Line 18 defines an async get method matching the production client shape.
- Line 19 records the URL.
- Line 20 returns the next fake response without touching the network.

## 9. Common beginner mistakes

### Mistake: Forgetting await
Calling fetch_bytes(client, url) without await creates a coroutine object and does not run the request.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Using requests in async code
The requests library blocks the event loop; use httpx.AsyncClient for this chapter.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Calling asyncio.run inside an existing event loop
FastAPI handlers and async tests already have a running loop; await the coroutine instead.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Creating one AsyncClient per URL
That wastes connection pooling and makes cleanup harder; share a client for a batch.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: No timeout
A network hang can become a program hang.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Unbounded gather
Thousands of simultaneous requests can overwhelm your machine or the remote server.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Retrying every error
A 404 or malformed URL usually will not become valid if you ask again.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Catching Exception around cancellation
Broad exception handling can accidentally hide cancellation or timeout behavior.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Blocking with time.sleep
Use await asyncio.sleep for async waits; time.sleep blocks the event loop thread.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Putting CPU parsing in async def
The parser still consumes CPU on the event loop thread unless sent to ProcessPoolExecutor.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Returning only successful content
Dropping failures makes it impossible to tell which URL broke.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

### Mistake: Testing against the real internet
Real services make tests flaky and slow; use fake clients.
How to notice it: write a tiny timing test, inspect warnings, or assert the fake client call count.
How to fix it: make the wait explicit, use the async library, or preserve structured failure information.

## 10. Debugging guidance

- Debug async code by making scheduling visible.
- Print or log when each URL starts, when it receives a response, and when it returns a result.
- Use time.perf_counter to compare sequential and concurrent versions.
- If concurrent code takes exactly N times the single-request delay, something is still sequential or blocked.
- If a test hangs, add a test-level timeout so failure is visible.
- If you see "coroutine was never awaited", search for a missing await or missing asyncio.run at the synchronous edge.
- If you see "no running event loop", you probably called a loop-only API outside async code.
- If you see "asyncio.run() cannot be called from a running event loop", remove asyncio.run from inside async code and await directly.
- If all requests fail immediately, inspect timeout configuration and fake-client behavior before blaming gather.
- If only the first fake response is used, your fake client may be sharing mutable response state incorrectly.
- If retries are too slow in tests, inject or monkeypatch the sleep function instead of really sleeping.
- If cancellation behaves strangely, check for broad except blocks that swallow cancellation.

A useful debug log format is:

```text
[12.04] start url=https://example.test/a attempt=1
[12.06] start url=https://example.test/b attempt=1
[12.41] done  url=https://example.test/b status=200
[13.02] retry url=https://example.test/a status=503 delay=1.0
```

The exact timestamps do not matter; the overlap does.

## 11. Design tradeoffs

- **One shared AsyncClient versus one client per request:** A shared client reuses connections and centralizes timeout settings. A client per request is simpler but wasteful and easier to leak.
- **Return exceptions versus structured results:** Exceptions are natural for one failing operation. Structured results are better for batches where partial success matters.
- **Low concurrency limit versus high concurrency limit:** A low limit is polite and predictable but slower. A high limit is faster until it causes rate limits, memory pressure, or remote-service harm.
- **Retry count:** Too few retries fail through temporary problems. Too many retries waste time and may make outages worse.
- **Backoff length:** Short backoff gives fast recovery. Longer backoff respects struggling services.
- **Timeout length:** Short timeouts make the CLI responsive. Long timeouts may be necessary for large PDFs or slow archives.
- **Bytes versus text return values:** Bytes are correct for PDFs and general downloads. Text is convenient for metadata only after encoding is known.
- **Where to parse metadata:** The fetcher can retrieve bytes or text; parsing into domain objects may belong in a separate adapter or service.

Tradeoffs should be written down near configuration defaults because future maintainers need to know why a limit exists.

## 12. Testing implications

- Async tests should be deterministic.
- Deterministic means the test result does not depend on a live website, current network speed, or a public API being available.
- Use fake async clients with async get methods.
- Assert returned FetchResult values rather than only checking that no exception was raised.
- Assert attempt counts for retry behavior.
- Assert call order only when order is part of the contract.
- Remember that gather returns results in input order even if completion order differs.
- Test empty input because fetch_batch([]) should return [] immediately.
- Test one bad URL in a batch because partial failure is a major requirement.
- Test 404 separately from timeout because they should not have the same retry behavior.
- Test 429 with Retry-After separately because rate-limit handling is user- and service-friendly.
- Test cancellation only if your function owns cancellation behavior.
- Do not sleep for real seconds in unit tests when you can inject a fake sleep function.
- Use pytest markers or async test support already present in the project rather than inventing a new test framework.

A minimal async test shape is:

```python
async def test_fetch_success() -> None:
    client = FakeAsyncClient([FakeResponse(200, b"paper")])
    result = await fetch_with_retry(client, "https://example.test/paper")
    assert result.succeeded
    assert result.content == b"paper"
    assert client.calls == ["https://example.test/paper"]
```

The test awaits the function under test because the function is async.
The fake client makes the test fast and offline.
The assertions check behavior, content, and interaction count.

## 13. Architecture implications

- Async fetching is an infrastructure concern because it talks to external systems.
- Core models should remain unaware of httpx.
- Service code should not import a concrete PDF parser or concrete HTTP implementation when a protocol or injected dependency is enough.
- CLI code can use asyncio.run at the outermost boundary because Typer or a normal command function is synchronous.
- FastAPI route handlers from Week 14 are already async-capable, so they should await service functions directly instead of calling asyncio.run.
- Storage code remains responsible for persistence and should not hide network requests inside database methods.
- Parsing code remains responsible for converting PDF bytes to text and should not fetch URLs itself unless explicitly designed as an adapter.
- The ProcessPoolExecutor boundary remains the correct place for CPU-heavy parsing.
- Do not introduce a worker queue system in this week; that belongs to Week 16.
- Do not introduce RAG behavior in this week; that belongs to Week 17.
- Do not introduce Docker deployment in this week; that belongs to Week 18.
- A good architecture lets you test fetching, parsing, storage, and services separately.

The dependency direction should still feel like this:

```text
CLI/API edge
    -> service workflow
        -> core models and protocols
        -> injected async fetch implementation
            -> httpx.AsyncClient
        -> Week 8 ProcessPoolExecutor for CPU parsing
```

## 14. How this connects to AI engineering / ML research

- AI engineering systems often spend surprising amounts of time moving data before any model runs.
- Paper metadata must be fetched before it can be cleaned.
- PDFs must be downloaded before they can be parsed.
- Parsed text must exist before embeddings or classifiers can process it.
- Slow and unreliable fetching creates slow and unreliable ML workflows.
- Async I/O lets a research platform collect data efficiently while still respecting remote systems.
- Rate limiting matters ethically because public research services are shared infrastructure.
- Timeouts matter operationally because model pipelines should fail clearly instead of hanging overnight.
- Structured failures matter scientifically because missing papers can bias a dataset if failures are invisible.
- Retries matter practically because temporary network failures should not ruin a long-running collection job.
- The async skill you learn here generalizes to API calls, metadata enrichment, object storage reads, and remote evaluation services.
- The boundary skill you learn here is just as important: keep CPU-heavy ML work out of the event loop.

## 15. Mini quizzes

1. **Question:** What does calling an async function return before it is awaited?
   **Answer:** A coroutine object.
2. **Question:** Why does asyncio.sleep not block the event loop?
   **Answer:** It registers a timer and yields control until the timer is ready.
3. **Question:** Why is time.sleep inside async def dangerous?
   **Answer:** It blocks the event loop thread and prevents other coroutines from running.
4. **Question:** What does asyncio.gather preserve: completion order or input order?
   **Answer:** Input order.
5. **Question:** Should a 404 normally be retried?
   **Answer:** No, it usually means the resource does not exist.
6. **Question:** Name two retryable failures.
   **Answer:** Timeouts, connection errors, 429, 500, 502, 503, or 504.
7. **Question:** Why use a semaphore?
   **Answer:** To limit how many coroutines enter a section such as HTTP fetching at once.
8. **Question:** Where should CPU-heavy PDF parsing run?
   **Answer:** In the Week 8 ProcessPoolExecutor boundary.
9. **Question:** Why inject the HTTP client into a function?
   **Answer:** It makes lifecycle ownership and fake-client testing easier.
10. **Question:** Why should unit tests avoid real network calls?
   **Answer:** Real network calls are slow, flaky, and depend on external services.

## 16. Explain-it-aloud prompts

- Explain the difference between concurrency and parallelism using the librarian story.
- Explain what happens when Python reaches `await client.get(url)`.
- Explain why calling an async function does not immediately run its body.
- Explain why three sequential awaits take about three seconds when each waits one second.
- Explain why `asyncio.gather` can reduce that time to about one second.
- Explain why `httpx.AsyncClient` should be used with `async with`.
- Explain why every network request should have a timeout.
- Explain why a 503 may be retried but a 404 usually should not be retried.
- Explain how a semaphore protects both ResearchOps and the remote service.
- Explain what partial failure means in a batch fetch.
- Explain why PDF parsing belongs in ProcessPoolExecutor even when fetching is async.
- Explain how you would test retry logic without waiting real seconds.

## 17. What to memorize

- `async def` defines a coroutine function.
- Calling a coroutine function returns a coroutine object.
- `await` pauses the current coroutine and lets the event loop run other ready tasks.
- `asyncio.run(coro)` is for the outer synchronous entry point, not inside an already-running event loop.
- `asyncio.gather(a, b, c)` waits for multiple awaitables and returns results in input order.
- `async with httpx.AsyncClient(...) as client` manages network resources safely.
- `asyncio.Semaphore(limit)` caps concurrent access.
- Timeouts are required for network code.
- Retries need a maximum attempt count.
- Do not retry permanent client errors such as 404.
- Use `await asyncio.sleep(...)` inside async retry backoff.
- Do not use `time.sleep(...)` inside async code.
- CPU-bound parsing goes to ProcessPoolExecutor, not the event loop.

## 18. What to understand deeply

- Understand that async is cooperative.
- A coroutine must reach await before another coroutine can run on the event loop thread.
- Understand that an event loop can manage many waits but does not create many CPU cores.
- Understand that network behavior is unreliable by default, so timeouts and retries are not extras.
- Understand that retries are a policy decision, not a reflex.
- Understand that rate limiting is a form of respect for remote services.
- Understand that structured results preserve information during partial failure.
- Understand that dependency injection makes async code testable without the internet.
- Understand that resource lifecycle matters because clients hold connections.
- Understand that architecture boundaries matter more as asynchronous workflows cross CLI, API, service, and infrastructure layers.

A deep understanding should let you predict behavior before running code.
For example, if five tasks each await `asyncio.sleep(1)` inside gather, you should predict about one second total.
If five tasks each call `time.sleep(1)` inside async def, you should predict about five seconds total.
If a batch uses `Semaphore(2)` and has six one-second requests, you should predict about three waves and roughly three seconds total.

## 19. What not to worry about yet

- Do not build a background worker or job queue system in this chapter.
- Do not build a RAG pipeline in this chapter.
- Do not containerize the project in this chapter.
- Do not optimize kernel-level networking details.
- Do not memorize every httpx exception type on the first pass.
- Do not implement full arXiv XML parsing unless the exercise or project file asks for it.
- Do not make every function async just because one function nearby is async.
- Do not chase perfect retry policies before you can explain simple max attempts and backoff.
- Do not add heavy dependencies to solve simple HTTP behavior.
- Do not worry about distributed rate limiting; a local semaphore is enough for Week 15.

## 20. Bridge to next week

Week 15 gives ResearchOps the ability to fetch remote data without wasting time on sequential network waits.
It also gives the project safety rules: timeouts, retries, rate limits, structured results, and CPU-bound boundaries.
Next week can build on this by treating longer-running workflows as managed work rather than immediate one-shot commands.
Do not jump there early while learning this chapter.
First become confident that one process can fetch several URLs safely and explain every await point.
The clean handoff is: Week 15 obtains remote bytes and metadata; Week 8 parsing boundaries process CPU-heavy content; later workflow orchestration can decide when and how to run larger jobs.
Before moving forward, you should be able to answer three questions without notes.
First: which line yields control to the event loop?
Second: which failures are retried and which are not?
Third: where does CPU-heavy PDF parsing run?

If those answers are clear, Week 15 has done its job.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
