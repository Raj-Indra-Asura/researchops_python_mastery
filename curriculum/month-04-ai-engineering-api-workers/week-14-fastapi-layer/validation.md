# Validation — Week 14 FastAPI Layer

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 14 — FastAPI Layer](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## 1. Pre-validation checklist

- [ ] `.[dev,api,storage]` is installed in an active virtual environment.
- [ ] Route handlers delegate to services; they contain no business logic.
- [ ] Services are injected via `Depends`, not constructed inside routes.
- [ ] The API talks to services, never directly to SQLite.

## 2. Exact commands

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,api,storage]"
ruff check src tests
uvicorn researchops.api.main:app --reload   # Ctrl-C after confirming startup
curl http://localhost:8000/health
pytest tests/e2e/test_api.py -v
pytest -q
```

## 3. Expected behavior

- Uvicorn starts and serves the app.
- `GET /health` returns `200` with JSON.
- `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=...` return validated
  JSON, with correct status codes for missing/invalid input.

## 4. Tests that must pass

- `tests/e2e/test_api.py` (via `TestClient`, no manual server needed)
- `pytest -q` (whole suite)

## 5. Manual checks

- `curl` each endpoint; confirm response shapes match the Pydantic models.
- Request a non-existent paper id; confirm a `404`, not a `200` with `null`.
- Send an invalid query param; confirm a `422` validation error.

## 6. Architecture checks

- No route handler contains search/ranking/persistence logic.
- No route opens a database connection.

```bash
grep -rn "sqlite3\|\.execute(\|SELECT " src/researchops/api/ --include="*.py"
# Expected: no output (routes go through services)
```

## 7. Documentation checks

- `notes.md` explains the app-factory pattern and `Depends` injection.
- Each endpoint's request/response contract is documented.

## 8. Do-not-proceed warnings

**Do not proceed to Week 15 if:**

- **Route handlers contain business logic** — they must only validate, delegate to
  a service, and shape the response.
- **The API bypasses services and talks directly to SQLite.**

## 9. Ruthless mentor checkpoint

- "Read me any route handler. Is there a single line of business logic in it?"
- "Show me where the service a route uses is *constructed*. It must not be inside
  the route."
- "Prove the endpoints pass without you manually starting uvicorn."

## 10. Definition of done

- [ ] App factory exists; uvicorn serves it.
- [ ] `/health`, `/papers`, `/papers/{id}`, `/papers/search` work.
- [ ] Routes delegate to services via `Depends`; zero logic in routes.
- [ ] Responses validated by Pydantic models; status codes are intentional.
- [ ] `tests/e2e/test_api.py` passes; `pytest -q` passes; `ruff` clean.
- [ ] You can describe one request from HTTP to service and back.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 14 — FastAPI Layer** · *validation.md — the checkpoint* (step 5 of 6 this week).

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
8. [Next week → Week 15](../../../curriculum/month-04-ai-engineering-api-workers/week-15-async-io-network-fetching/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 15 — Async I/O Network Fetching](../../../curriculum/month-04-ai-engineering-api-workers/week-15-async-io-network-fetching/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 4 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 4 overview](../README.md) · [📄 Week 14 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
