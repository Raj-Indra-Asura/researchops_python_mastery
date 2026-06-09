# Week 15 - Async I/O and Network Fetching

## Learning objectives
- Understand when async I/O helps compared with multiprocessing.
- Use `asyncio` and async HTTP clients for concurrent fetching.
- Set timeouts, retries, and backoff for unreliable networks.
- Limit concurrency to protect remote services and your own machine.
- Parse fetched responses into ResearchOps inputs.
- Test async code predictably.
- Handle cancellations and partial failures gracefully.

## Project milestone
Add asynchronous network fetching so ResearchOps can pull remote document metadata or content concurrently and safely.

## Files to modify/create
- `src/researchops/network/fetch.py`
- `src/researchops/network/retries.py`
- `src/researchops/cli/fetch.py`
- `tests/unit/test_async_fetch.py`
- `tests/integration/test_fetch_command.py`

## Concepts covered
`asyncio`, coroutines, await, async HTTP, timeouts, retries, semaphores, cancellation, and async testing.

## Expected deliverables
- An async fetcher for URLs.
- Retry and timeout handling.
- CLI support for network fetch workflows.
- Tests for success, timeout, and partial failure paths.

## Definition of done
- [ ] Async fetch code exists.
- [ ] Timeout behavior is explicit.
- [ ] Retry logic is bounded.
- [ ] Concurrency limits are enforced.
- [ ] CLI command exposes fetching.
- [ ] Async tests pass.
- [ ] You can explain why this workload is I/O-bound.
