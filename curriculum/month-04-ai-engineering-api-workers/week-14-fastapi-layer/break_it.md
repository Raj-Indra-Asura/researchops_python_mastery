# Break It - Week 14 FastAPI Layer

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 14 — FastAPI Layer](./README.md) › **break_it.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Intentional failure experiments

### 1. Missing required field
Send a POST request to `/search` without the `query` field. FastAPI returns `422 Unprocessable Entity`. Read the response body. Find the path in `"detail"` that names `query`. Understand this: the `422` is automatic — you wrote zero code to produce it. Pydantic validation happens before your handler is called.

### 2. Wrong type in body
Send `{"query": 42, "limit": "five"}`. FastAPI will try to coerce `42` to `str` (it succeeds — Pydantic casts it). But `"five"` cannot become `int`. Read the `422` error and find which field failed. Add a validator that rejects numeric queries using `@field_validator`.

### 3. Returning a raw domain object
Create a route that returns a domain model object directly instead of a `SearchHitResponse`. Watch FastAPI raise a serialisation error. Understand why: FastAPI cannot serialise arbitrary Python objects. Wrap all returns in Pydantic response models.

### 4. Leaking a stack trace
In a route, raise a raw `Exception("something broke")` without any handler. What does the client receive by default? It receives a 500 response that may include internal details. Add a global exception handler. Verify the response body no longer contains the exception message.

### 5. Forgetting to wire a dependency
Remove `Depends(get_search_service)` from a route parameter. FastAPI will still call the function but `service` will not be injected. Watch the `TypeError` or `NameError`. Learn to read FastAPI's startup validation output — it often catches wiring problems before any request is made.

### 6. Returning 200 for a 404 case
Remove the `raise HTTPException(status_code=404)` from the document lookup route. Instead, return an empty dict. Write a test that confirms this is wrong: the status code is 200 but the document is missing. Then fix it. This exercise teaches the habit of using correct status codes rather than always returning 200.

### 7. Circular dependency
Create two dependency providers where A calls B and B calls A. FastAPI will raise a recursion error at startup. This is a design smell — split the concerns.

### 8. Large limit value
Send `{"query": "transformers", "limit": 10000}`. Does your service crash or return gracefully? Add a Pydantic validator that caps `limit` at a maximum value (for example, 50). Write a test that sends `limit=10000` and gets `422`.

### 9. Empty query string
Send `{"query": "", "limit": 5}`. Pydantic accepts it (empty string is a valid `str`). Your service may behave oddly. Add a Pydantic validator that rejects empty strings. Write a test that confirms `422` is returned for an empty query.

---

## Debugging tasks

- When a test fails with a 422, print `response.json()["detail"]` to read the full validation error path.
- When a test fails with a 500, add `print(response.text)` to see any debug detail.
- Run `pytest -k api -v` and inspect each test name to confirm routes are being tested individually.
- Use `uvicorn --reload` and interact with `http://localhost:8000/docs` to manually test your routes.

---

## Edge cases to explore

| Case | Expected behaviour |
|------|-------------------|
| `limit = 0` | Return empty list (or raise 400 — define your policy) |
| `limit` negative | Raise 422 via Pydantic validator |
| `query` with only whitespace | Raise 422 or normalise to empty |
| JSON body with extra unknown fields | Pydantic ignores by default; consider using `model_config = ConfigDict(extra="forbid")` |
| Route not found | FastAPI returns 404 with `{"detail": "Not Found"}` automatically |
| Wrong HTTP method (GET on a POST route) | FastAPI returns 405 Method Not Allowed |

---

## What did you learn?

- Which error happened before your handler ran?
- What was the difference between a Pydantic validation error and a service-layer error?
- Which status code did you forget to use first?
- How does a thin route make the handler easier to test in isolation?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 14 — FastAPI Layer** · *break_it.md — the failure lab* (step 4 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [exercises.md](./exercises.md)
- ▶ **Next:** [validation.md](./validation.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. **➡ [break_it.md](./break_it.md) ← you are here**
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
