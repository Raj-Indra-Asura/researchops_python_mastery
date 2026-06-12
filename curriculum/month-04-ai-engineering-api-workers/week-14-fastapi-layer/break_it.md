<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 14 — FastAPI Layer:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It - Week 14 FastAPI Layer

## Purpose of failure practice

Break API code on purpose so status codes, validation, dependency wiring, and service delegation become visible instead of mysterious. The goal is to identify which layer owns the fix.

## Failure lab rules

- Break one thing at a time.
- Predict the status code first.
- Inspect response JSON.
- Name the owner layer.
- Restore the correct code before the next experiment.
- Do not add future-week systems while debugging.
- Add or identify the test that would catch the bug.

## Intentional break experiments

### Experiment: Missing required query

#### How to cause it
Call `/papers/search` without `q`.

#### Expected error
`422 Unprocessable Entity`; route body should not run.

#### How to inspect
Read `response.json()["detail"]` and find the `q` location.

#### How to fix
Send `q` or intentionally redesign the contract.

#### Test that should catch it
A test calls `/papers/search` and asserts 422.

#### What this teaches
Boundary validation protects the service from incomplete input.

#### Common wrong fixes
- Returning 200 with empty results.
- Making service accept `None`.
- Ignoring the detail body.

### Experiment: Wrong limit type

#### How to cause it
Call `/papers/search?q=graphs&limit=five`.

#### Expected error
`422` because `five` is not an integer.

#### How to inspect
Inspect detail for `limit`.

#### How to fix
Use numeric limit and add bounds if needed.

#### Test that should catch it
A test asserts bad limit gives 422.

#### What this teaches
Annotations turn raw URL strings into typed Python values.

#### Common wrong fixes
- Manual parsing in the route.
- Passing raw strings to service.
- Catching validation as success.

### Experiment: Business logic in route

#### How to cause it
Put ranking or SQL directly in the route.

#### Expected error
Architecture breaks even if response is 200.

#### How to inspect
Inspect imports and route body for storage/ranking decisions.

#### How to fix
Move behavior to service or infrastructure.

#### Test that should catch it
A fake-service delegation test should fail if service is skipped.

#### What this teaches
Green tests do not excuse wrong ownership.

#### Common wrong fixes
- Leaving small SQL in route.
- Duplicating CLI logic.
- Moving FastAPI into service.

### Experiment: Missing-paper leaks as 500

#### How to cause it
Remove `PaperNotFoundError` to 404 mapping.

#### Expected error
Expected missing resource becomes 500 or raw error.

#### How to inspect
Inspect traceback and service exception.

#### How to fix
Catch domain error and raise `HTTPException(404)`.

#### Test that should catch it
Fake service raises missing error; test asserts 404.

#### What this teaches
Expected domain failures need HTTP translation.

#### Common wrong fixes
- Catch all exceptions as 404.
- Return empty dict with 200.
- Raise HTTPException from service.

### Experiment: Wrong dependency override

#### How to cause it
Override a provider not used by `Depends`.

#### Expected error
Real provider runs or fake data missing.

#### How to inspect
Compare override key to route provider function.

#### How to fix
Override the exact provider and use fresh app.

#### Test that should catch it
Fake records call; test asserts it was called.

#### What this teaches
Overrides are exact function-object replacements.

#### Common wrong fixes
- Patch class globally.
- Share stale app overrides.
- Override a lookalike lambda.

### Experiment: Unserializable return

#### How to cause it
Return raw custom object or file handle.

#### Expected error
Serialization or response validation error.

#### How to inspect
Inspect traceback for non-JSON field.

#### How to fix
Map domain object to Pydantic response model.

#### Test that should catch it
Response-shape test asserts public fields.

#### What this teaches
The API contract must be JSON-compatible.

#### Common wrong fixes
- Remove response model.
- Use `str(obj)` everywhere.
- Expose internals because they serialize.

### Experiment: Route conflict

#### How to cause it
Let `/papers/{paper_id}` swallow `/papers/search`.

#### Expected error
Search endpoint behaves like paper lookup.

#### How to inspect
Use fake call records to see which route ran.

#### How to fix
Clarify routes and add a regression test.

#### Test that should catch it
Test `/papers/search?q=x` calls search fake.

#### What this teaches
Dynamic paths need contract tests.

#### Common wrong fixes
- Accept search as an ID.
- Rename blindly.
- Move path without updating docs.

### Experiment: Unexpected service exception

#### How to cause it
Fake service raises `RuntimeError`.

#### Expected error
Client receives 500; safe handler may hide internals.

#### How to inspect
Inspect body and logs separately.

#### How to fix
Map expected errors; keep unexpected errors generic.

#### Test that should catch it
Test forced exception returns safe 500 if handler exists.

#### What this teaches
Clients need safe errors; maintainers need logs.

#### Common wrong fixes
- Return raw exception string.
- Swallow exception.
- Return 200 with error text.

## Debugging checklist

- [ ] URL and method are correct.
- [ ] Router is included in app.
- [ ] Validation detail has been read.
- [ ] Route body did or did not run.
- [ ] Dependency override key is exact.
- [ ] Fake service recorded expected call.
- [ ] Expected domain errors map to status codes.
- [ ] Response model exposes only public fields.
- [ ] No service imports FastAPI.
- [ ] A focused test catches the failure.

## Reflection after breaking

- Which failure happened before the route ran?
- Which failure was wrong dependency wiring?
- Which failure was wrong architecture?
- Which status code is clearer now?
- Which response body helped most?
- Which wrong fix tempted you?
- Which test would catch the bug fastest?
- Which fix belonged in API?
- Which fix belonged in service?
- What will you inspect first next time?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 14 — FastAPI Layer:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
