# Validation — Week 15 Async I/O and Network Fetching

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 15 — Async I/O Network Fetching](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## 1. Pre-validation checklist

- [ ] `.[dev,api]` is installed in an active virtual environment.
- [ ] Fetching uses `httpx.AsyncClient` with explicit timeouts and bounded
      retries.
- [ ] No CPU-bound work (PDF parsing, embeddings) runs inside async code.
- [ ] Tests mock HTTP — they make no real network calls.

## 2. Exact commands

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,api]"
ruff check src tests
pytest tests/unit/test_fetch_service.py -v
pytest -q
```

## 3. Expected behavior

- Concurrent fetches complete faster than sequential fetches on test fixtures.
- Timeouts trigger, retries are bounded with backoff, and a partial failure does
  not erase successful results.

## 4. Tests that must pass

- `tests/unit/test_fetch_service.py` (success, timeout, and partial-failure paths)
- `pytest -q` (whole suite)

## 5. Manual checks

- Run `researchops fetch-arxiv "<query>"`; confirm metadata returns.
- Simulate a slow/failing endpoint (in a test or scratch script); confirm the
  retry/timeout policy behaves as designed.

## 6. Architecture checks

- Async functions contain only I/O-bound awaits; any CPU work is offloaded to a
  process pool.

```bash
grep -rn "def parse\|ProcessPoolExecutor\|pypdf\|embed(" src/researchops/services/fetch_service.py
# Expected: no inline CPU-bound parsing/embedding in the async fetch path
```

## 7. Documentation checks

- `notes.md` explains the event loop, `async`/`await`, and the I/O-bound vs
  CPU-bound rule (cross-reference ADR-0002).

## 8. Do-not-proceed warnings

**Do not proceed to Week 16 if:**

- **PDF parsing (or any CPU-bound work) happens in async code** — it blocks the
  event loop and must be offloaded.
- **Network failure is untested** — timeouts, retries, and partial failures must
  each have a test.

## 9. Ruthless mentor checkpoint

- "Explain async vs multiprocessing in two sentences. Which does this workload
  need?"
- "Where would PDF parsing go during a fetch — inline or offloaded? Show me."
- "Show me the test that proves a network timeout is handled without killing the
  other fetches."

## 10. Definition of done

- [ ] Async fetcher runs requests concurrently with `httpx.AsyncClient`.
- [ ] Timeouts are explicit; retries are bounded with backoff.
- [ ] No CPU-bound work runs in the event loop.
- [ ] Partial failures preserve successful results.
- [ ] Tests mock HTTP and cover failure paths; `pytest -q` passes; `ruff` clean.
- [ ] You can explain why this workload is I/O-bound.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 15 — Async I/O Network Fetching** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
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
