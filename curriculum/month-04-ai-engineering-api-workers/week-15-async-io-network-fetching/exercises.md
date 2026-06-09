<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 15 Async I/O and Network Fetching

This workbook turns the chapter into practice. Keep the navigation blocks unchanged and work through the sections in order.
Do not add future-week systems here: no worker queue, no RAG pipeline, and no Docker setup.

## 1. How to use this workbook

**Working rhythm:** read the task, predict the behavior, write the smallest code, run the smallest check, then explain what changed.
**Evidence to collect:** keep timing numbers, fake-client call counts, and structured result examples in your scratch notes so your explanation is based on observations.
**Stop condition:** do not move to implementation tasks until you can say which operations are waiting on I/O and which operations are using CPU.

1. Create small files or tests only where the project already expects learning code or test code.
2. Prefer fake clients over real network calls.
3. Time small examples with `time.perf_counter()` so you can see the difference between sequential and concurrent waits.
4. When an exercise asks for a written explanation, write the answer in your learning notes or say it aloud; do not invent new project documentation unless asked.
5. Keep PDF parsing CPU-bound and route it through the Week 8 ProcessPoolExecutor pattern when the exercise crosses from fetching to parsing.
6. If an exercise feels too large, reduce it to one URL, one fake response, and one assertion first.

## 2. Warm-up exercises

For every timing exercise, write down your prediction before running the program. If the prediction is wrong, explain whether the mistake was caused by sequential awaits, a blocking call, or an incorrect semaphore limit.
For every small coroutine, identify the first line that actually runs and the first line that can yield control back to the event loop.
After each warm-up, rewrite the result in plain English: "This took about X seconds because Y tasks were allowed to wait together."

1. Write `async def greet(name: str) -> str` that awaits `asyncio.sleep(1)` and returns a greeting. Run it with `asyncio.run` from a synchronous script.
2. Call `greet("Ada")` without awaiting it. Observe the coroutine object. Explain why the body did not run.
3. Write three fake fetch coroutines that each sleep one second. Await them sequentially and measure total time.
4. Run the same three fake fetch coroutines with `asyncio.gather` and measure total time.
5. Rewrite the timing example with ten fake fetches and predict the runtime before running it.
6. Classify these as I/O-bound or CPU-bound: downloading a PDF, parsing a PDF, reading a small local config file, calling a remote metadata API, computing embeddings for 10,000 chunks, and waiting for SQLite to commit.
7. Inside an async function, compare `await asyncio.sleep(0.2)` with `time.sleep(0.2)` by running five tasks concurrently.
8. Create an `asyncio.Semaphore(2)` and prove with printed start/end messages that only two protected sections run at once.

## 3. Code-reading exercises

Annotate code with three labels: `starts work`, `waits cooperatively`, and `blocks the event loop`. This makes hidden scheduling behavior visible.
When reading retry code, draw a two-column table: failure type on the left and retry decision on the right.
When reading batch code, trace one successful URL and one failing URL from input list to final result object.

1. Read a small `fetch_bytes(client, url)` function. Mark the exact line where control can return to the event loop.
2. Read a function that constructs `httpx.AsyncClient` inside a loop. Explain why this wastes connection pooling.
3. Read a retry loop that catches every `Exception`. Identify which exceptions or statuses should not be retried.
4. Read a batch fetcher using `asyncio.gather`. Explain why result order matches input order.
5. Read a fake async client. Identify which methods and attributes are required only because production code uses them.
6. Read code that calls `asyncio.run` inside an async test. Explain the error you expect.
7. Read code that parses PDF bytes directly after download in the coroutine. Point to the event-loop blocking risk.

## 4. Implementation exercises

Implementation standard: each helper should have one clear responsibility. Do not combine URL parsing, HTTP fetching, PDF parsing, and storage in one function.
Configuration standard: timeout, concurrency limit, and max attempts should be visible parameters or named constants, not unexplained magic numbers buried in a loop.
Result standard: every input URL should produce an inspectable result, even when the request fails.
Architecture standard: if your implementation needs CPU-heavy parsing, pass bytes to the Week 8 ProcessPoolExecutor boundary rather than parsing in the coroutine.

1. Implement a frozen `FetchResult` dataclass with `url`, `status_code`, `content`, `error`, and `attempts` fields plus a `succeeded` property.
2. Implement `fetch_bytes(client, url)` using `await client.get(url)`, `raise_for_status`, and `response.content`.
3. Implement `fetch_one_result(client, url)` that returns `FetchResult` for both success and HTTP failure.
4. Implement `fetch_many_bounded(urls, limit=5)` using one shared `httpx.AsyncClient`, one semaphore, and `asyncio.gather`.
5. Implement `fetch_with_retry(client, url, max_attempts=3)` for timeouts, connection errors, and retryable 5xx statuses.
6. Add exponential backoff with delays of 1, 2, and 4 seconds. Keep the sleep injectable or easy to monkeypatch for tests.
7. Handle 429 responses by reading `Retry-After` when present and falling back to normal backoff when absent or invalid.
8. Implement a metadata fetch function that builds query parameters for a paper search endpoint and returns response text or bytes without parsing future-week features.
9. Implement a PDF download helper that returns bytes and refuses to parse the PDF in the event loop.

## 5. Testing exercises

Testing standard: a unit test should not require DNS, Wi-Fi, a public API, or the current date. If it does, replace the dependency with a fake.
Timing standard: avoid real multi-second sleeps in tests. Use tiny sleeps for scheduling demonstrations or monkeypatch the sleep function for retry backoff.
Assertion standard: assert both the returned value and the interaction evidence, such as call counts or maximum in-flight calls.
Failure standard: every retry test should include the final failed result path, not only the eventual success path.

1. Write `FakeResponse` with `status_code`, `content`, `headers`, and `raise_for_status`.
2. Write `FakeAsyncClient` with an async `get` method and a `calls` list.
3. Test a successful fetch and assert URL, content, status code, attempts, and `succeeded`.
4. Test a 404 response and assert it is not retried.
5. Test a timeout followed by success and assert the fake client was called twice.
6. Test all attempts failing and assert the final `FetchResult` records the final attempt count.
7. Test a batch containing success, timeout, and 404, and assert the result list length matches the input list length.
8. Test `fetch_many_bounded([])` and assert it returns an empty list immediately.
9. Test semaphore behavior with a fake client that records maximum in-flight calls.
10. Test 429 with `Retry-After: 2` by monkeypatching sleep and asserting the requested delay.

## 6. Debugging exercises

Debugging method: first reproduce the bug with one URL, then with three URLs, then with a larger batch. This prevents concurrency noise from hiding the root cause.
Logging method: include URL, attempt number, status code, and elapsed time in temporary debug output.
Cleanup method: after the bug is understood, remove noisy prints or convert them to project-appropriate logging if the codebase already uses logging there.

1. Intentionally remove `await` before `client.get(url)`. Run the test and explain the observed failure or warning.
2. Replace `await asyncio.sleep` with `time.sleep` in a coroutine. Run concurrent tasks and explain the timing change.
3. Remove the timeout configuration from an AsyncClient example. Use a fake that never returns and observe why tests need timeout protection.
4. Set the semaphore limit to 1 and time ten fake requests. Explain why the code became effectively sequential.
5. Make the fake client raise `httpx.ConnectError` for every call. Confirm the retry loop stops at `max_attempts`.
6. Make a retry loop catch 404 as retryable. Use call counts to prove the bug.
7. Catch and swallow `asyncio.CancelledError` in a toy coroutine. Explain why cancellation contracts matter.

## 7. Refactoring exercises

Refactoring rule: keep behavior covered by a test before changing structure. Async refactors can accidentally change scheduling behavior while still returning the same final value.
Refactoring rule: move resource ownership outward. A batch-level client is easier to close than many request-level clients.
Refactoring rule: name policy decisions. `is_retryable_status` is easier to review than repeated inline comparisons.

1. Refactor a function that creates an AsyncClient per URL into one that shares a client for the whole batch.
2. Refactor loose tuple results like `(url, content, error)` into the `FetchResult` dataclass.
3. Refactor a CLI command so it parses arguments synchronously and calls one async workflow with `asyncio.run` at the edge.
4. Refactor a service function so it accepts a fetch dependency rather than importing `httpx` directly.
5. Refactor repeated retry-status checks into a named helper such as `is_retryable_status(status_code)`.
6. Refactor real sleeps in retry tests into an injectable sleep function or monkeypatched `asyncio.sleep`.
7. Refactor CPU-bound parsing out of an async function and into a ProcessPoolExecutor handoff.

## 8. Written explanation exercises

Write these explanations without using the words "magic" or "just". If an explanation depends on those words, it probably skips the mechanism.
Use one ResearchOps example in each answer, such as fetching arXiv metadata, downloading a PDF, or handing PDF bytes to the parser.
End each explanation with one rule you would apply in code review.

1. Explain in five sentences why async improves network fetching but not PDF parsing.
2. Explain the difference between a coroutine function, a coroutine object, and a task.
3. Explain why `asyncio.gather` returns results in input order even when completion order differs.
4. Explain why ResearchOps should not make unbounded concurrent requests to public research services.
5. Explain how a timeout changes an infinite wait into a controlled failure.
6. Explain why retrying 503 can be useful but retrying 404 is usually wasteful.
7. Explain why fake-client tests are better than live-network unit tests.
8. Explain where `asyncio.run` belongs in a CLI program and where it does not belong.

## 9. Stretch exercises

Stretch work should still be beginner-readable. Prefer small helper functions and explicit names over compact clever code.
When adding jitter or size limits, make the source of randomness or the size threshold injectable so tests stay deterministic.
When benchmarking, compare the measured result to a rough expected number of waves: `ceil(url_count / limit) * per_request_delay`.

1. Add jitter to exponential backoff while keeping tests deterministic by injecting a jitter function.
2. Implement per-host concurrency limits if all URLs include hostnames, but keep the design local and simple.
3. Add a small result summary function that counts successes, timeouts, permanent HTTP errors, and retryable failures.
4. Write a benchmark table for limits 1, 2, 5, and 10 using fake 100ms network waits.
5. Add content-type checking for PDF downloads and return a structured error when the response is not a PDF-like type.
6. Add a maximum response-size guard for PDF downloads so a fake huge response can be rejected safely.
7. Add cancellation handling that re-raises `asyncio.CancelledError` after cleanup.

## 10. Brutal exercises

Brutal tasks are integration-style practice, but they must still respect this week's boundary. Fetching can be async; CPU parsing must be offloaded.
Write the happy path last if the failure paths are confusing. A robust batch fetcher is mostly defined by how it behaves when some URLs fail.
Keep the return shape stable. A caller should not need one code path for all-success batches and another shape for partial failures.

1. Build `fetch_paper_inputs(urls)` that fetches many URLs, records partial failures, and returns only structured results. Do not parse PDFs in this function.
2. Build `fetch_then_parse_one(url, executor)` that fetches bytes asynchronously and hands CPU parsing to a provided ProcessPoolExecutor.
3. Write tests for `fetch_then_parse_one` using a fake parser function and a real small executor boundary only if the project already has that pattern.
4. Implement retry behavior that respects `Retry-After`, stops on 404, and uses exponential backoff for 5xx and timeouts.
5. Write a concurrency stress test with 50 fake URLs and assert the maximum in-flight count never exceeds the limit.
6. Write a cancellation test where pending tasks are cancelled and completed results remain inspectable.
7. Write a CLI-facing summary formatter that prints one line per URL and a final success/failure count.

## 11. Mini project task

Mini project acceptance criteria: one shared client, explicit timeout, bounded concurrency, retry policy, structured results, fake tests, and no event-loop PDF parsing.
Mini project review question: can another learner change the concurrency limit without reading the entire implementation?
Mini project review question: can another learner tell which failures are permanent and which failures are retried?

1. Create a small async fetching workflow for ResearchOps paper inputs.
2. The workflow should accept a list of URLs and a concurrency limit.
3. It should fetch with one shared AsyncClient, a timeout, bounded concurrency, and retry policy.
4. It should return one FetchResult per URL in the same order as the input URLs.
5. It should treat 404 as permanent, 429 and 5xx as retryable, and timeouts as retryable until max attempts is reached.
6. It should not parse PDFs directly in the event loop.
7. It should include fake-client unit tests for success, timeout, 404, 429, empty input, and one bad URL among good URLs.
8. It should include a short written explanation of the event-loop boundary and the ProcessPoolExecutor boundary.

## 12. Completion checklist

Final proof: choose one exercise from warm-up, one from implementation, one from testing, and one from debugging, then explain how they connect.
Final proof: describe one bug that would make the program too slow, one bug that would make it impolite to a remote service, and one bug that would make failures invisible.
Final proof: point to the exact boundary where fetched bytes stop being async network work and become CPU-bound parsing work.

1. I can define async def, await, coroutine, task, event loop, timeout, retry, backoff, semaphore, and cancellation.
2. I can show a timing difference between sequential awaits and gather.
3. I can use httpx.AsyncClient with async with.
4. I can write a fetch function that returns bytes and raises or records HTTP errors deliberately.
5. I can limit concurrency with asyncio.Semaphore.
6. I can implement retry logic with max attempts and backoff.
7. I can explain why not all errors should be retried.
8. I can test async code with fake clients and no real network.
9. I can keep PDF parsing out of the event loop and use the Week 8 ProcessPoolExecutor boundary for CPU work.
10. I can explain why this week does not include worker queues, RAG, or Docker.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
