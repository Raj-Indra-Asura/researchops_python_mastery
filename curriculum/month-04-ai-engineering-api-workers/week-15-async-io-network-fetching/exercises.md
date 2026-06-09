# Exercises - Week 15 Async I/O and Network Fetching

## Warm-up exercises
1. Write an `async` function that sleeps and returns a value.
2. Fetch two URLs concurrently and compare runtime with sequential fetching.
3. Add a timeout and catch the timeout exception.
4. Limit concurrency with a semaphore.

## Project exercises
1. Implement an async URL fetcher using `httpx.AsyncClient`.
2. Add bounded retries with backoff for transient failures.
3. Build a CLI command to fetch a batch of URLs.
4. Write tests for success, timeout, and retry behavior.

## Stretch exercises
1. Support cancellation of long-running fetch batches.
2. Persist fetched metadata to SQLite.
3. Add rate-limit aware backoff for `429` responses.

## Writing questions
1. Why is this workload I/O-bound instead of CPU-bound?
2. When should you retry versus fail fast?
3. What does a concurrency limit protect?
4. How will you keep async tests deterministic?
