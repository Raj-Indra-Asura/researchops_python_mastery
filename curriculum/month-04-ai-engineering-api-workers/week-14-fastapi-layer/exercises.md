<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 14 — FastAPI Layer:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 14 FastAPI Layer

## How to use this workbook

Work in order from warm-up to brutal.
Keep routes thin and service-driven.
Do not add Docker, workers, RAG, or Week 15 network fetching.
Every implementation exercise should have a matching test when you are coding.
Use fakes to keep API unit tests fast.
Read status codes before reading JSON bodies.

## Warm-up exercises

1. **Warm-up 1.** Define method/path/query/status in your own words.
2. **Warm-up 2.** Draw the `/health` request-response flow.
3. **Warm-up 3.** Sort success, missing paper, bad query, and crash into status codes.
4. **Warm-up 4.** Explain why `/papers/{paper_id}` uses a path parameter.
5. **Warm-up 5.** Explain why `/papers/search?q=x` uses a query parameter.
6. **Warm-up 6.** Write the sentence: API routes may translate HTTP but services own behavior.
7. **Warm-up 7.** Identify three things not to build this week.

## Code-reading exercises

1. **Read the API package boundary.** Open `src/researchops/api/` and list every Python file currently present. Success: you can say which file should create the FastAPI app and which future files, such as routers or dependency providers, would still belong inside the API layer.
2. **Read `src/researchops/api/main.py`.** Identify the app-factory TODO, the import-order note, and the missing route registration point. Success: you can explain why `create_app()` should wire HTTP concerns without storing business logic.
3. **Read service code before route code.** Open `src/researchops/services/paper_service.py` and `src/researchops/services/search_service.py`. Mark the methods an API route should call for listing papers, getting one paper, and searching. Success: each planned endpoint delegates to a service instead of inventing behavior in the route.
4. **Read domain boundaries.** Open `src/researchops/core/interfaces.py` and identify the protocols the services depend on. Success: you can explain why API code may depend on services but services should not import FastAPI.
5. **Compare CLI wiring to API wiring.** Find a CLI command that calls a service. Write the equivalent API flow as request -> route -> service -> response schema. Success: the API and CLI share behavior through the service layer.
6. **Read fake implementations.** Inspect `tests/fakes/` and choose or sketch fakes for API tests. Success: an endpoint test can run without a live server, real database, or network.
7. **Read validation before coding.** Read this week `validation.md` and list the expected endpoints, status codes, and response shapes. Success: you know what `200`, `404`, and `422` should mean before writing route code.
8. **Search for forbidden imports.** Inspect planned API files for storage imports such as `sqlite3`, repository construction, or raw SQL. Success: route code remains HTTP translation, not persistence.

## Implementation exercises

1. **Implementation 1.** Implement `create_app() -> FastAPI` and `app = create_app()`.
2. **Implementation 2.** Add `GET /health`.
3. **Implementation 3.** Create `PaperResponse` and search response schemas.
4. **Implementation 4.** Add `GET /papers` through a service dependency.
5. **Implementation 5.** Add `GET /papers/{paper_id}` with 404 mapping.
6. **Implementation 6.** Add `GET /papers/search?q=...&limit=...` through search service.
7. **Implementation 7.** Move routes into routers if main becomes hard to scan.
8. **Implementation 8.** Move providers into `dependencies.py` when wiring becomes noisy.
9. **Implementation 9.** Keep all business rules in services.

### Detailed acceptance criteria for implementation work

#### /health
- [ ] returns exactly `200`
- [ ] returns `{"status":"ok"}`
- [ ] does not require a service dependency
- [ ] is covered by one test

#### /papers
- [ ] uses a service dependency
- [ ] does not read storage directly
- [ ] returns a JSON list
- [ ] maps every item through a response schema
- [ ] is covered by fake-service tests

#### /papers/{paper_id}
- [ ] receives `paper_id` from the path
- [ ] calls a service method with that ID
- [ ] returns one response on success
- [ ] returns 404 on missing paper
- [ ] does not return `{}` for missing paper

#### /papers/search
- [ ] requires `q`
- [ ] accepts a bounded `limit` if implemented
- [ ] calls the search service
- [ ] does not rank inside the route
- [ ] returns response schemas

### Extra implementation prompts

1. Write the route signature before writing the body.
2. Underline the part of the signature that is HTTP input.
3. Underline the dependency parameter.
4. Write the one service call the route should make.
5. Write the response-mapping line.
6. Write the expected error mapping.
7. Delete any code that makes a business decision in the route.
8. Compare the endpoint to the matching CLI command.
9. Confirm the service method name is not invented unnecessarily.
10. Confirm the route can be tested with a fake.

## Testing exercises

1. **Testing 1.** Test health status and body.
2. **Testing 2.** Test list papers with a fake service.
3. **Testing 3.** Test get one paper success.
4. **Testing 4.** Test missing paper 404.
5. **Testing 5.** Test search forwards query and limit to fake service.
6. **Testing 6.** Test missing query returns 422.
7. **Testing 7.** Test invalid limit if bounds are declared.
8. **Testing 8.** Test response shape does not leak internal fields.
9. **Testing 9.** Test dependency overrides are isolated.
10. **Testing 10.** Optionally translate one test to `httpx.AsyncClient` without adding Week 15 behavior.

### Detailed testing scenarios

| Scenario | Setup | Expected status | Main assertion |
|---|---|---|---|
| health happy path | no dependencies | 200 | exact status body |
| list empty papers | fake returns [] | 200 | empty JSON list |
| list two papers | fake returns two domain objects | 200 | two response objects |
| get known paper | fake returns one paper | 200 | id and title fields |
| get missing paper | fake raises not-found | 404 | detail field |
| search known query | fake records q and limit | 200 | fake received exact values |
| search missing q | no fake call expected | 422 | detail names q |
| search bad limit | no fake call expected | 422 | detail names limit |
| unexpected fake error | fake raises RuntimeError | 500 if handler exists | safe body |

### Test-writing checklist
- [ ] Create a fresh app.
- [ ] Install dependency override before creating the client when possible.
- [ ] Send one request.
- [ ] Assert status code first.
- [ ] Assert JSON shape second.
- [ ] Assert fake-service calls if delegation matters.
- [ ] Clear overrides or discard app.
- [ ] Do not depend on test order.

## Debugging exercises

1. **Debugging 1.** Remove `q` and inspect 422 detail.
2. **Debugging 2.** Use wrong method and inspect 405.
3. **Debugging 3.** Use nonexistent path and inspect framework 404.
4. **Debugging 4.** Raise missing-paper exception and verify API 404.
5. **Debugging 5.** Override wrong dependency and prove fake was not called.
6. **Debugging 6.** Return wrong response type and inspect serialization failure.
7. **Debugging 7.** Create route conflict and prove which handler runs.

## Refactoring exercises

1. **Refactor 1.** Extract `to_paper_response`.
2. **Refactor 2.** Extract `to_search_response`.
3. **Refactor 3.** Move route groups to `APIRouter`.
4. **Refactor 4.** Move dependency providers to `dependencies.py`.
5. **Refactor 5.** Rename vague schemas to `PaperResponse` style names.
6. **Refactor 6.** Remove duplicate CLI/API decisions by moving them to services.

## Written explanation exercises

1. Why should routes not query SQLite directly?
2. Why are API schemas separate from domain models?
3. How does 422 happen before route code?
4. Why do fake services make tests clearer?
5. Why does `HTTPException` belong in API code?
6. How do CLI and API share behavior?
7. What should clients see for unexpected errors?
8. Why are future-week topics excluded?

### Extra written drills

1. Describe a bug where the API and CLI disagree because logic was duplicated.
2. Explain why a response schema can be safer than returning `paper.__dict__`.
3. Explain how `Depends` improves tests without changing service code.
4. Explain why a 422 is usually a client input problem.
5. Explain why a 500 is usually not the client's fault.
6. Explain why generated docs are useful but not a replacement for tests.
7. Explain what makes an API route thin.
8. Explain when a helper mapper is useful.
9. Explain how route tests support future refactoring.
10. Explain why no live server belongs in unit tests.

## Stretch exercises

1. **Stretch 1.** Add `limit` bounds between 1 and 50.
2. **Stretch 2.** Inspect `/docs` and identify schema sources.
3. **Stretch 3.** Add safe no-store header to search responses.
4. **Stretch 4.** Add a simple route docstring and see it in docs.
5. **Stretch 5.** Record fake-service call counts.
6. **Stretch 6.** Add a generic 500 handler only if the project pattern supports it.

## Brutal exercises

1. **Brutal 1.** Write a contract table for every endpoint.
2. **Brutal 2.** Prove every route delegates exactly once to a fake service.
3. **Brutal 3.** Build a CLI/API parity table.
4. **Brutal 4.** Create a failure matrix for each endpoint.
5. **Brutal 5.** Split routers without changing service imports.
6. **Brutal 6.** Convert one sync test to async client style.
7. **Brutal 7.** Audit imports for architecture violations.

### Endpoint-by-endpoint workbook details

#### Health endpoint
- Write the route in the app factory first.
- Keep the response body intentionally tiny.
- Do not add database checks to health yet.
- Test the exact JSON body so accidental wording changes are caught.
- Explain why this endpoint is allowed to avoid the service layer.

#### List papers endpoint
- Decide the public fields before coding.
- Make the fake return two papers with different titles.
- Assert list order only if the service promises order.
- Assert the route does not mutate fake data.
- Explain how this endpoint differs from a CLI table printout.

#### Get paper endpoint
- Use a realistic ID string.
- Write one fake that returns a paper.
- Write one fake that raises not found.
- Assert 404 instead of checking only the body.
- Explain why path parameters represent identity.

#### Search endpoint
- Use `q` as the required search text.
- Use `limit` as a small integer.
- Make the fake record both values.
- Assert the route forwards the exact values.
- Explain why ranking stays outside the route.

### Self-review rubric

| Skill | Beginner evidence | Strong evidence |
|---|---|---|
| HTTP basics | Can name method and path | Can predict status code and body for success and failure |
| FastAPI routes | Can write `@app.get` | Can explain import-time registration versus request-time execution |
| Pydantic schemas | Can define fields | Can explain why schemas protect public contracts |
| Dependencies | Can use `Depends` | Can override the provider with a fake in tests |
| Service delegation | Can call a service | Can prove no business logic lives in routes |
| Error mapping | Can raise 404 | Can map domain errors without leaking framework code into services |
| Testing | Can use TestClient | Can assert status, body, and fake-service call arguments |
| Architecture | Can recite the rule | Can detect and fix a forbidden import direction |

### Pair-programming prompts

1. Navigator: ask which layer owns this line before the driver writes it.
2. Driver: say the expected status code before running the test.
3. Navigator: stop the driver if a route imports storage for behavior.
4. Driver: explain the fake service method before writing assertions.
5. Navigator: compare the API response with the Pydantic schema.
6. Driver: remove one unnecessary line from the route.
7. Navigator: ask whether the CLI would need the same decision.
8. Driver: move shared behavior to the service if the answer is yes.
9. Navigator: inspect a 422 body out loud.
10. Driver: write the final explanation from request to response.

### Common review comments to practice responding to

- Review comment: This route has business logic.
  - Good response: Identify the decision and move it to the service. Leave only HTTP mapping in the route.
- Review comment: This test uses the real database.
  - Good response: Replace the dependency with a fake and assert the API contract.
- Review comment: This endpoint returns raw objects.
  - Good response: Add or use a response schema and mapper.
- Review comment: This missing resource returns 200.
  - Good response: Map the domain not-found condition to 404.
- Review comment: This provider cannot be overridden easily.
  - Good response: Expose a named provider function and use it in `Depends`.
- Review comment: This schema name is vague.
  - Good response: Rename it to describe request or response purpose.
- Review comment: This code adds future-week behavior.
  - Good response: Remove it and keep the Week 14 boundary focused.

### Extra API contract edge cases

Work through these without adding future-week systems:

1. If `/papers` has no papers, should the API return `[]` or `404`? Defend the choice.
2. If `/papers/search?q=   ` contains only spaces, should validation reject it or should the service normalize it? Defend the owner.
3. If a paper has no abstract, what should the JSON field contain: missing field, empty string, or `null`? Match the response schema.
4. If `limit=100000`, what protects the service from an expensive request? Name the boundary rule.
5. If the fake service returns an internal debug attribute, what prevents the client from seeing it?
6. If the CLI and API disagree about paper titles, where should you look for duplicated logic?
7. If generated docs show the wrong response shape, which annotation should you inspect first?
8. If a test passes alone but fails with the suite, what dependency override cleanup problem might exist?

## Mini project task

- Build read-only API slice: `/health`, `/papers`, `/papers/{paper_id}`, `/papers/search`.
- Use FastAPI under `src/researchops/api/`.
- Use Pydantic response models.
- Use dependency providers for services.
- Use same service layer as CLI.
- Map missing resources to 404.
- Let bad inputs produce 422.
- Test with `TestClient` or `httpx.AsyncClient`.
- Use fakes in API tests.
- Avoid future-week infrastructure.

### Study log prompts before checking completion

1. Which endpoint felt easiest and why?
2. Which endpoint forced you to think about architecture?
3. Which validation error did you inspect most carefully?
4. Which fake service was most useful?
5. Which route would be easiest to break accidentally?
6. Which assertion protects the public contract best?
7. Which line proves the route delegates to a service?
8. Which line proves a missing resource becomes 404?
9. Which future-week feature did you avoid adding?
10. What would you explain to a teammate before they review your API code?

## Completion checklist

- [ ] FastAPI app factory exists.
- [ ] Health endpoint returns expected JSON.
- [ ] Paper endpoints use response models.
- [ ] Routes delegate to services.
- [ ] Dependency providers are override-friendly.
- [ ] Missing paper returns 404.
- [ ] Invalid input returns 422.
- [ ] Tests use fakes and no live server.
- [ ] Services do not import FastAPI.
- [ ] No Docker/workers/RAG/network fetching added.
- [ ] You can explain one happy path and one failure path.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 14 — FastAPI Layer:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
