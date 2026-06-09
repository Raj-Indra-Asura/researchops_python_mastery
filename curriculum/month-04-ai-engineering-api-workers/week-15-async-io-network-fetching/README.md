<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 15 — Async IO and Network Fetching:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 14 Reflection](../week-14-fastapi-layer/reflection.md) · ➡️ [Notes →](notes.md)

**📐 Relevant Decisions:** [ADR-0002: Multiprocessing vs Asyncio](../../../docs/decisions/0002-multiprocessing-vs-asyncio.md)

---
<!-- NAV_END -->

# Week 15 — Async I/O and Network Fetching

> **Chapter title: "Waiting without blocking."**
> The week ResearchOps reaches out to the network — concurrently, and without
> freezing.

---

## 1. Week title

Week 15 — Async I/O and Network Fetching (Month 4, Chapter 3 of 4).

## 2. Story of the week

Until now every paper came from your local disk. This week ResearchOps learns to
fetch papers and metadata from the internet — for example, querying the arXiv API.
Fetching is mostly *waiting* on the network, and waiting sequentially is slow. So
you meet `asyncio`: a single thread running an event loop that keeps many requests
in flight at once. You will write `async def` functions, `await` network calls
with `httpx.AsyncClient`, add timeouts and bounded retries with backoff, and learn
the one rule that keeps async healthy: **never block the event loop with CPU
work.**

## 3. What you already know

- From Week 14: a FastAPI layer and clean service boundaries.
- From Week 8: CPU-bound vs I/O-bound, and `ProcessPoolExecutor` for CPU work.
- From Month 3: testing with fakes and monkeypatch.

You have not yet written async code or used an event loop.

## 4. What this week adds

- The **`asyncio` event loop**: one thread, many concurrent waits.
- **`async def` / `await`** — what they actually do (yield control while waiting).
- **`httpx.AsyncClient`** for concurrent async HTTP requests.
- **Timeouts and retries** with exponential backoff.
- The rule **never block the event loop** — CPU-bound work belongs in a process
  pool.
- **`pytest-asyncio`** and monkeypatched HTTP for testing async code.

## 5. Why this week matters

Async is the natural model for I/O-bound concurrency, and fetching many URLs is
the textbook case. But async is also where beginners cause subtle, severe bugs by
running CPU-heavy work (PDF parsing, embeddings) inside a coroutine and freezing
the whole loop. This week makes the I/O-bound vs CPU-bound distinction *concrete*
and teaches the offloading pattern, reinforcing
[ADR-0002](../../../docs/decisions/0002-multiprocessing-vs-asyncio.md). Robust
networking — timeouts, retries, partial-failure handling — is also a core AI
engineering skill, since real data pipelines fetch from flaky services.

## 6. Learning objectives

By the end of the week you can:

- Write `async def` functions and explain what `await` yields.
- Fetch many URLs concurrently with `httpx.AsyncClient`.
- Apply timeouts and bounded retries with backoff.
- Keep CPU-bound work off the event loop (offload to a process pool).
- Handle partial failures so one bad fetch does not erase the others.
- Test async code with `pytest-asyncio` and mocked HTTP.

## 7. Project milestone

`researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv
API asynchronously, and `researchops fetch-url URL` fetches a single paper.

## 8. Files / modules touched

- `src/researchops/services/fetch_service.py` — async fetching with retry/timeout.
- `src/researchops/cli/commands/ingest.py` — `fetch-url` and `fetch-arxiv`
  commands.

## 9. Commands introduced

```bash
researchops fetch-url https://example.org/paper.pdf
researchops fetch-arxiv "attention is all you need"
```

## 10. Tests involved

- `tests/unit/test_fetch_service.py` — async tests with HTTP mocked via
  monkeypatch, covering success, timeout, and partial-failure paths.

```bash
pytest tests/unit/test_fetch_service.py -v
```

## 11. Study plan for the week

1. **Day 1 — Async mental model.** Run a tiny script that `await`s
   `asyncio.sleep` concurrently vs sequentially; feel the difference.
2. **Day 2 — httpx.AsyncClient.** Fetch several URLs concurrently with
   `asyncio.gather`.
3. **Day 3 — Timeouts + retries.** Add per-request timeouts and bounded
   exponential backoff.
4. **Day 4 — Partial failure + offloading.** Ensure one failed fetch does not sink
   the batch; confirm any CPU work is offloaded, not run inline.
5. **Day 5 — Async tests + CLI + milestone + report.**

## 12. Estimated time breakdown

| Activity | Time |
|---|---|
| Reading + async experiments | ~2 hrs |
| Concurrent fetching with httpx | ~2.5 hrs |
| Timeouts, retries, backoff | ~2 hrs |
| Partial failure + async tests | ~2.5 hrs |
| Reflection + report | ~1 hr |

## 13. How to know the learner is stuck

- A "coroutine was never awaited" warning — you called an async function without
  `await`.
- Concurrent fetches run no faster than sequential — you awaited them one by one
  instead of gathering.
- The event loop freezes during a run — you ran CPU-bound work inside a coroutine.
- A single network error aborts the whole fetch batch.

## 14. Definition of done

- [ ] Async fetcher uses `httpx.AsyncClient` and runs requests concurrently.
- [ ] Per-request timeouts are explicit.
- [ ] Retries are bounded with backoff.
- [ ] No CPU-bound work runs inside the event loop.
- [ ] Partial failures are handled; successes are preserved.
- [ ] `fetch-url` / `fetch-arxiv` commands work.
- [ ] `pytest tests/unit/test_fetch_service.py` passes (HTTP mocked).

## 15. Ruthless mentor checkpoint

- "Explain async vs multiprocessing in two sentences. Which one does *this*
  workload need, and why?"
- "Where would PDF parsing go if it happened during a fetch — inline, or offloaded
  to a process pool? Show me."
- "Simulate a network timeout in a test. Does the fetch retry, then fail cleanly
  without killing the other fetches?"

If parsing runs in the loop, or network failure is untested, you are not done.

## 16. What not to do this week

- Do **not** run PDF parsing, embeddings, or any CPU-heavy work inside async code.
- Do **not** leave fetches unbounded — always set timeouts and retry limits.
- Do **not** make real network calls in tests; mock the HTTP client.
- Do **not** let one failed request discard the successful results.

## 17. Bridge to next week

You can now fetch data concurrently — but some operations (bulk fetching, ingest,
embedding a large corpus) are simply too long to run inside a single request or
command. **Week 16** introduces a **local worker and job system**: a persistent
job queue with an explicit state machine, a polling worker loop, retries, and
idempotency. The async and offloading lessons from this week feed directly into
running long work safely in the background.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 14 Reflection](../week-14-fastapi-layer/reflection.md) · ➡️ [Notes →](notes.md)

**📐 Relevant Decisions:** [ADR-0002: Multiprocessing vs Asyncio](../../../docs/decisions/0002-multiprocessing-vs-asyncio.md)

**Week 15 — Async IO and Network Fetching:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
