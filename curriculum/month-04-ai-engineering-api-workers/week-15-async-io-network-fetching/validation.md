
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 15 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation — Week 15 Async I/O and Network Fetching

## Pre-validation checklist

- [ ] `.[dev,api]` is installed in an active virtual environment.
- [ ] Fetching uses `httpx.AsyncClient` with explicit timeouts and bounded
      retries.
- [ ] No CPU-bound work (PDF parsing, embeddings) runs inside async code.
- [ ] Tests mock HTTP — they make no real network calls.

## Commands to run

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,api]"
ruff check src tests
pytest tests/unit/test_fetch_service.py -v
pytest -q
```

## Expected outputs

Expected output should prove three things: the code is async, the network policy is bounded, and failures are visible instead of swallowed.

- `source .venv/bin/activate` prints nothing, except possibly a changed shell prompt.
- `python -m pip install -e ".[dev,api]"` ends successfully and provides `httpx` for async HTTP work. It must not require optional ML or worker extras for this week.
- `ruff check src tests` ends with `All checks passed!`. If it reports unused awaits, broad exception problems, or import-order issues, fix them before running the full suite.
- `pytest tests/unit/test_fetch_service.py -v` shows fetch-service tests as `PASSED`: success, timeout, retryable failure, permanent `404`, partial batch failure, empty input, and bounded concurrency.
- `pytest -q` finishes with a green summary such as `... passed`. Unit tests should use fake clients or mocked transports; they should not depend on DNS, Wi-Fi, public APIs, or the current date.

Behavior you should be able to observe after the commands pass:

- Concurrent fake fetches complete in waves controlled by the semaphore limit, not one request at a time.
- Timeouts trigger controlled failures; retries stop at `max_attempts`; backoff is testable without real multi-second sleeps.
- A batch with one bad URL still returns inspectable results for the good URLs.
- PDF parsing, embedding generation, and other CPU-heavy work are absent from `src/researchops/services/fetch_service.py` and remain behind the appropriate process-pool boundary.

## Tests that must pass

- `tests/unit/test_fetch_service.py` (success, timeout, and partial-failure paths)
- `pytest -q` (whole suite)

## Manual checks

- Run `researchops fetch-arxiv "<query>"`; confirm metadata returns.
- Simulate a slow/failing endpoint (in a test or scratch script); confirm the
  retry/timeout policy behaves as designed.

## Architecture checks

- Async functions contain only I/O-bound awaits; any CPU work is offloaded to a
  process pool.

```bash
grep -rn "def parse\|ProcessPoolExecutor\|pypdf\|embed(" src/researchops/services/fetch_service.py
# Expected: no inline CPU-bound parsing/embedding in the async fetch path
```

## Documentation checks

- `notes.md` explains the event loop, `async`/`await`, and the I/O-bound vs
  CPU-bound rule (cross-reference ADR-0002).

## Do-not-proceed warnings

**Do not proceed to Week 16 if:**

- **PDF parsing (or any CPU-bound work) happens in async code** — it blocks the
  event loop and must be offloaded.
- **Network failure is untested** — timeouts, retries, and partial failures must
  each have a test.
- A coroutine calls `time.sleep`, `requests.get`, PDF parsing, or embedding code directly.
- Tests pass only against the live internet instead of fake clients or mocked HTTP responses.
- Retry logic treats permanent errors such as `404` the same as temporary errors such as timeouts or `503`.

## Ruthless mentor checkpoint

- "Explain async vs multiprocessing in two sentences. Which does this workload
  need?"
- "Where would PDF parsing go during a fetch — inline or offloaded? Show me."
- "Show me the test that proves a network timeout is handled without killing the
  other fetches."

## Definition of done

- [ ] Async fetcher runs requests concurrently with `httpx.AsyncClient`.
- [ ] Timeouts are explicit; retries are bounded with backoff.
- [ ] No CPU-bound work runs in the event loop.
- [ ] Partial failures preserve successful results.
- [ ] Tests mock HTTP and cover failure paths; `pytest -q` passes; `ruff` clean.
- [ ] You can explain why this workload is I/O-bound.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
