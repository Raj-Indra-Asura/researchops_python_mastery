
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 14 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 14 — FastAPI Layer:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation — Week 14 FastAPI Layer

## Pre-validation checklist

- [ ] `.[dev,api,storage]` is installed in an active virtual environment.
- [ ] Route handlers delegate to services; they contain no business logic.
- [ ] Services are injected via `Depends`, not constructed inside routes.
- [ ] The API talks to services, never directly to SQLite.

## Commands to run

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,api,storage]"
ruff check src tests
uvicorn researchops.api.main:app --reload   # Ctrl-C after confirming startup
curl http://localhost:8000/health
pytest tests/e2e/test_api.py -v
pytest -q
```

## Expected outputs

Expected output is partly command text and partly HTTP behavior. Do not continue just because a server starts; the responses and tests must prove the API contract.

- `source .venv/bin/activate` prints nothing, except possibly a changed shell prompt.
- `python -m pip install -e ".[dev,api,storage]"` ends successfully. It may reuse installed packages. It must not report missing FastAPI, Pydantic, or storage extras.
- `ruff check src tests` ends with `All checks passed!`. Route files, schemas, and tests must be lint-clean.
- `uvicorn researchops.api.main:app --reload` prints startup lines similar to `Uvicorn running on http://127.0.0.1:8000` and `Application startup complete`. Stop it with Ctrl-C only after the health check works.
- `curl http://localhost:8000/health` prints JSON equivalent to `{"status":"ok"}` and the server logs a `200 OK` request.
- `pytest tests/e2e/test_api.py -v` shows endpoint tests as `PASSED`: health, list papers, get one paper, missing paper `404`, search, and invalid input `422`.
- `pytest -q` finishes with a green summary such as `... passed`. No test should require a manually running uvicorn process.

Behavior you should be able to observe after the commands pass:

- `GET /health` returns status `200` and a tiny JSON body.
- `GET /papers`, `GET /papers/{paper_id}`, and `GET /papers/search?q=...` return response-schema-shaped JSON.
- Missing resources become `404`; malformed or missing query parameters become `422`; route code delegates to services.

## Tests that must pass

- `tests/e2e/test_api.py` (via `TestClient`, no manual server needed)
- `pytest -q` (whole suite)

## Manual checks

- `curl` each endpoint; confirm response shapes match the Pydantic models.
- Request a non-existent paper id; confirm a `404`, not a `200` with `null`.
- Send an invalid query param; confirm a `422` validation error.

## Architecture checks

- No route handler contains search/ranking/persistence logic.
- No route opens a database connection.

```bash
grep -rn "sqlite3\|\.execute(\|SELECT " src/researchops/api/ --include="*.py"
# Expected: no output (routes go through services)
```

## Documentation checks

- `notes.md` explains the app-factory pattern and `Depends` injection.
- Each endpoint's request/response contract is documented.

## Do-not-proceed warnings

**Do not proceed to Week 15 if:**

- **Route handlers contain business logic** — they must only validate, delegate to
  a service, and shape the response.
- **The API bypasses services and talks directly to SQLite.**
- Endpoint tests pass only when uvicorn is already running manually; e2e tests should create the app in-process.
- API responses expose raw domain objects, debug fields, or Python repr strings instead of Pydantic-shaped JSON.
- CLI behavior and API behavior disagree because the same business rule was copied into a route.

## Ruthless mentor checkpoint

- "Read me any route handler. Is there a single line of business logic in it?"
- "Show me where the service a route uses is *constructed*. It must not be inside
  the route."
- "Prove the endpoints pass without you manually starting uvicorn."

## Definition of done

- [ ] App factory exists; uvicorn serves it.
- [ ] `/health`, `/papers`, `/papers/{id}`, `/papers/search` work.
- [ ] Routes delegate to services via `Depends`; zero logic in routes.
- [ ] Responses validated by Pydantic models; status codes are intentional.
- [ ] `tests/e2e/test_api.py` passes; `pytest -q` passes; `ruff` clean.
- [ ] You can describe one request from HTTP to service and back.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 14 — FastAPI Layer:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
