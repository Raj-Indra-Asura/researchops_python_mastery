# Week 14 - FastAPI Layer

## Learning objectives
- Expose ResearchOps features through HTTP endpoints.
- Use Pydantic models for request and response validation.
- Inject dependencies cleanly into API routes.
- Map service errors to useful HTTP responses.
- Write API tests with FastAPI's testing tools.
- Keep transport concerns separate from core logic.
- Design endpoints that are clear and predictable.

## Project milestone
Add a FastAPI application that exposes search, ingest status, or document retrieval through validated HTTP endpoints.

## Files to modify/create
- `src/researchops/api/app.py`
- `src/researchops/api/dependencies.py`
- `src/researchops/api/schemas.py`
- `tests/integration/test_api_search.py`
- `tests/integration/test_api_health.py`

## Concepts covered
FastAPI routing, Pydantic models, dependency injection, status codes, error mapping, and API testing.

## Expected deliverables
- A running FastAPI app.
- Health and search-style endpoints.
- Request and response schemas.
- Integration tests for API behavior.

## Definition of done
- [ ] FastAPI app starts locally.
- [ ] Schemas validate input and output.
- [ ] Dependency injection wires services cleanly.
- [ ] Error responses are intentional.
- [ ] API tests pass.
- [ ] Transport code stays separate from business logic.
- [ ] You can explain one route end to end.
