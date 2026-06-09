# Week 14 — FastAPI Layer

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › **Week 14 — FastAPI Layer**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

> **Chapter title: "Your work, available over HTTP."**
> The week ResearchOps grows a second door — the web — without growing a second
> brain.

---

## 1. Week title

Week 14 — FastAPI Layer (Month 4, Chapter 2 of 4).

## 2. Story of the week

For thirteen weeks every feature has been driven from the terminal. That was
deliberate: the CLI forced the *logic* to work before any transport existed (see
[ADR-0003](../../../docs/decisions/0003-cli-before-api.md)). Now that the
services are proven, you expose them over HTTP with FastAPI. The key idea this
week is restraint: a route handler is a **thin adapter** — it validates the
request, calls a service, and shapes the response. No business logic lives in the
route. If you do this right, the API is almost boring, which is exactly what you
want.

## 3. What you already know

- From Months 1–3: clean services behind protocols, dependency injection, and a
  full test suite.
- From Week 13: semantic search you can now expose.
- Pydantic-style data validation concepts and HTTP at a basic level.

You have not yet built a web API or used FastAPI's dependency system.

## 4. What this week adds

- The **FastAPI app-factory** pattern.
- **Route handlers that delegate to services** — no logic in routes.
- **`Depends`** for injecting services into routes.
- **Pydantic response models** to validate what you return.
- **HTTP status codes** (200, 201, 404, 422, 500) and intentional error mapping.
- **API testing** with `TestClient` / `httpx.AsyncClient` — no real server needed.

## 5. Why this week matters

This is where the layering discipline of the whole project pays off. Because logic
lives in services, adding HTTP is a thin shell — and the *same* services could
later back a different transport with zero duplication. The opposite path
(business logic in routes) is how projects rot into untestable web handlers. This
week teaches you to keep transport and logic separate for good.

## 6. Learning objectives

By the end of the week you can:

- Define REST endpoints with FastAPI using an app factory.
- Inject services into routes with `Depends`.
- Validate responses with Pydantic models.
- Map service errors to correct HTTP status codes.
- Test endpoints with `TestClient` without launching a server.
- Explain why a route must contain no business logic.

## 7. Project milestone

`GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, and `GET /health`
work and return correct, validated JSON.

## 8. Files / modules touched

- `src/researchops/api/main.py` — the FastAPI app factory.
- `src/researchops/api/routes/papers.py` — papers routes.
- `src/researchops/api/routes/search.py` — search routes.
- `tests/e2e/test_api.py` — endpoint tests with `TestClient`.

## 9. Commands introduced

```bash
uvicorn researchops.api.main:app --reload    # serve the API locally
curl http://localhost:8000/health             # smoke-test an endpoint
```

## 10. Tests involved

- `tests/e2e/test_api.py` — exercises each endpoint via `TestClient`, asserting
  status codes and response shapes.

```bash
pytest tests/e2e/test_api.py -v
```

## 11. Study plan for the week

1. **Day 1 — App factory + /health.** Stand up FastAPI, return a health JSON.
2. **Day 2 — Dependency injection.** Use `Depends` to provide services
   (constructed at the composition root, not inside routes).
3. **Day 3 — Papers routes.** `GET /papers`, `GET /papers/{id}` delegating to
   `PaperService`; add Pydantic response models.
4. **Day 4 — Search route + error mapping.** `GET /papers/search`; map "not
   found" to 404, validation to 422.
5. **Day 5 — e2e tests + milestone + report.**

## 12. Estimated time breakdown

| Activity | Time |
|---|---|
| Reading + app factory + /health | ~1.5 hrs |
| `Depends` wiring | ~2 hrs |
| Routes + Pydantic response models | ~3 hrs |
| Error mapping + e2e tests | ~2.5 hrs |
| Reflection + report | ~1 hr |

## 13. How to know the learner is stuck

- A route opens a SQLite connection or contains search/ranking logic.
- Endpoints return raw dicts you assemble by hand instead of Pydantic models.
- You can only test by manually starting uvicorn (you have not used
  `TestClient`).
- A missing paper returns 200 with `null` instead of 404.

## 14. Definition of done

- [ ] FastAPI app factory exists and starts under uvicorn.
- [ ] `/health`, `/papers`, `/papers/{id}`, `/papers/search` all work.
- [ ] Routes delegate to services via `Depends`; no business logic in routes.
- [ ] Responses are validated by Pydantic models.
- [ ] Error cases map to intentional status codes (404, 422, …).
- [ ] `tests/e2e/test_api.py` passes without a manually started server.

## 15. Ruthless mentor checkpoint

- "Open any route handler. Read it to me. If it contains anything beyond
  validate-call-respond, why?"
- "Request a paper id that does not exist. What status code comes back?"
- "Show me a test that proves an endpoint works *without* you running uvicorn by
  hand."

If routes carry logic or bypass services, you are not done.

## 16. What not to do this week

- Do **not** put business logic in route handlers.
- Do **not** let the API talk directly to SQLite — go through services.
- Do **not** skip Pydantic response models and hand-assemble JSON.
- Do **not** rely on manual curl testing in place of `TestClient` tests.

## 17. Bridge to next week

Your services are now reachable over HTTP. But ResearchOps still only knows about
papers that are already on disk. **Week 15** adds the ability to *go get* new ones:
asynchronous network fetching with `asyncio` and `httpx`, with timeouts and
retries. The reflex to keep transport thin carries over — and you will learn a new
rule: async is for *waiting*, never for CPU work.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 14 — FastAPI Layer** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 13 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
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
