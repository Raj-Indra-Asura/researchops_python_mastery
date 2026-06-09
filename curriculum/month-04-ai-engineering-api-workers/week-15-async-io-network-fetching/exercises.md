<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 15 Async I/O and Network Fetching

## Beginner

1. **Your first coroutine.** Write an `async def greet(name: str) -> str` that waits 1 second with `await asyncio.sleep(1)` and returns `f"Hello, {name}"`. Run it with `asyncio.run(greet("Alice"))`. Then write a second async function `greet_two` that awaits `greet("Alice")` and `greet("Bob")` sequentially. Time it. Then rewrite `greet_two` using `asyncio.gather`. Time it again. Note the difference.

2. **Sync vs async timing.** Write two versions of a batch fetcher: one synchronous (using `time.sleep(1)` to simulate each request) and one async (using `await asyncio.sleep(1)`). Fetch 5 items. Measure elapsed time with `time.time()`. Print both durations. Confirm the async version takes ~1 second and the sync version takes ~5 seconds.

3. **Identify I/O vs CPU.** For each operation below, write "I/O-bound" or "CPU-bound" and explain why in one sentence:
   - Downloading a PDF from a URL
   - Parsing that PDF into text
   - Querying a SQLite database
   - Computing cosine similarity for 10 000 chunks
   - Sending an email via SMTP
   - Resizing an image in memory
   
4. **Timeout experiment.** Write an async function that uses `asyncio.wait_for` with a 1-second timeout on a coroutine that sleeps for 5 seconds. Catch `asyncio.TimeoutError`. Print "timed out" when it happens. Verify: without `wait_for`, the program waits 5 seconds. With `wait_for`, it waits 1 second.

5. **Semaphore demonstration.** Create a semaphore with `asyncio.Semaphore(2)`. Create 10 coroutines that each print "start", acquire the semaphore, sleep 0.5 seconds, print "end", then release. Run all 10 with `asyncio.gather`. Observe from the output that at most 2 run simultaneously (pairs of "start/end" interleave).

---

## Intermediate

1. **FakeHttpClient.** Implement `FakeHttpClient` and `FakeResponse` as shown in notes.md. Write three tests using it:
   - A test for a successful fetch that returns known content.
   - A test for a timeout (have the fake raise `httpx.TimeoutException`).
   - A test for a 404 (have `raise_for_status` raise `httpx.HTTPStatusError`).

2. **fetch_with_retry.** Implement `fetch_with_retry` from notes.md. Write tests using `FakeHttpClient` that:
   - Succeed on the first attempt.
   - Fail twice then succeed on the third attempt (count how many calls were made).
   - Fail all attempts and assert `RuntimeError` is raised.

3. **Bounded batch fetcher.** Implement `fetch_batch` from notes.md with a semaphore limit of 5. Write a test with 20 fake URLs, 3 of which raise `TimeoutException`. Assert the result list has 20 items, 17 with content and 3 with an error, and none are missing.

4. **pytest-asyncio setup.** Configure `pytest-asyncio` in `pyproject.toml` or `conftest.py`. Write an async test for `fetch_with_retry`. Confirm that `pytest -k async_fetch -v` runs and reports the test as passed. Read the `pytest-asyncio` docs to understand the difference between `auto` and `strict` mode.

5. **Do not put PDF parsing in async.** Write an `async def parse_and_index(pdf_bytes: bytes)` function that: (1) parses the PDF synchronously using a fake `slow_parse` function that sleeps for 1 second with `time.sleep(1)`, and (2) awaits an async database write. Time running 5 of these with `asyncio.gather`. Notice it takes 5 seconds, not 1. This is the blocking-the-event-loop problem. Document the fix: use `asyncio.run_in_executor` to offload the synchronous parse to a thread pool.

---

## Advanced

1. **run_in_executor.** Refactor `parse_and_index` to use `await asyncio.get_event_loop().run_in_executor(None, slow_parse, pdf_bytes)`. This runs `slow_parse` in a thread pool, freeing the event loop. Time 5 concurrent calls. They should now take ~1 second total. Write a test that confirms the result is correct.

2. **Retry with exponential backoff.** Modify `fetch_with_retry` to use exponential backoff: first retry waits 1 second, second waits 2 seconds, third waits 4 seconds. Add a jitter: randomly add 0–0.5 seconds to each wait. Write a test using a mock `asyncio.sleep` that records how many times it was called and with what arguments.

3. **Rate-limit aware retry.** Handle `429 Too Many Requests` specially: read the `Retry-After` header (if present) and wait that many seconds before retrying. Write a test where the fake client returns 429 with `Retry-After: 2` on the first call, then 200 on the second. Assert the retry waited approximately 2 seconds (mock the sleep).

4. **Streaming large responses.** Use `httpx.AsyncClient.stream()` to fetch a large response without loading the entire body into memory. Process it line by line. Write a test with a fake streaming server (or a mock that yields chunks). This is important for PDF download where files can be hundreds of MB.

5. **Async CLI command.** Add a `fetch` subcommand to the ResearchOps CLI that takes a list of URLs as arguments. It should call `fetch_batch`, print a success or failure line for each URL, and exit with code 1 if any URL failed. Use `asyncio.run()` as the synchronous entry point. Write a CLI test using `TestClient` or by calling the function directly.

---

## Brutal

1. **Full async ingestion pipeline.** Build an end-to-end function `ingest_from_urls(urls: list[str]) -> list[IngestResult]` that: fetches each URL asynchronously (bounded to 5 concurrent), parses the response synchronously in a thread pool executor, indexes the parsed content via the search service. Return structured results for each URL. Write integration tests for the happy path, timeout, and parse failure cases.

2. **Graceful shutdown.** Extend `fetch_batch` to accept a `shutdown_event: asyncio.Event`. If the event is set while fetching, cancel all pending tasks and return partial results. Write a test that sets the event after 3 of 10 fetches complete and asserts that exactly 3 results are successful and the rest are marked as cancelled.

3. **Async context manager for client lifecycle.** Create a reusable `AsyncFetchSession` class that is an async context manager. When entering, it creates and configures the `httpx.AsyncClient`. When exiting, it closes the client and logs total requests made. Write tests using `async with AsyncFetchSession() as session:` and verify cleanup happens even when exceptions occur.

4. **Benchmark concurrency levels.** Write a benchmarking script that runs `fetch_batch` with 20 fake URLs (each with 100ms simulated delay) at semaphore limits of 1, 2, 5, 10, and 20. Measure elapsed time for each. Print a table. Identify where increasing the limit stops helping. This is the point where the simulated I/O cost per request matches the total concurrency capacity.

5. **Async dependency in FastAPI.** Modify the Week 14 `POST /search` route to call an async search service instead of a synchronous one. Use FastAPI's async route syntax (`async def search(...)`). Write a test that confirms the route still works. Then write a test that deliberately puts a `time.sleep(2)` inside an async route handler and observes that it blocks all other requests (hint: use concurrent `TestClient` calls). This is the "blocking event loop" bug in an API context.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
