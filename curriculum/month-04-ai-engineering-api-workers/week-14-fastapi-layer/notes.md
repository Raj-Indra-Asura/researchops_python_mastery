<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 14 — FastAPI Layer:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 14 FastAPI Layer

## Chapter overview

Week 14 gives ResearchOps an HTTP front door.
Before this week, the main entry point is the CLI.
After this week, another program can ask ResearchOps questions over HTTP.
HTTP is a request-response protocol: a client sends a request and the server returns a response.
FastAPI is the Python framework that receives the request and calls your route function.
Pydantic is the validation layer that turns untrusted input into typed Python values and typed output into predictable JSON.
The service layer is still the owner of ResearchOps behavior.
The API layer is an adapter, not a second copy of the application.
The milestone is small: `GET /health`, `GET /papers`, `GET /papers/{id}`, and `GET /papers/search?q=QUERY`.
The API must call the same service layer the CLI uses.
Routes should be thin enough that a beginner can read them without guessing where business rules hide.
This chapter is not about Docker, background workers, RAG, or async network fetching internals.
Those topics arrive later; building them now would make the learning path muddy.

Study order:
1. Read the HTTP mental model.
2. Trace one request through a route.
3. Trace one service call.
4. Trace one response model.
5. Trace one failure path.
6. Read the tests.
7. Explain why the route delegates instead of deciding.

## What you already know from previous weeks

- Week 1 taught project scaffold, core models, and a CLI shell.
- Week 2 taught path handling, exceptions, and logging.
- Week 3 taught dataclasses and domain modeling.
- Week 4 taught CLI packaging and entry points.
- Week 5 taught SQLite repositories.
- Week 6 taught PDF parsing boundaries.
- Week 7 taught service-layer workflows.
- Week 8 taught multiprocessing boundaries for CPU work.
- Week 9 taught protocols and dependency inversion.
- Week 10 taught testing quality gates.
- Week 11 taught classical ML as a service concern.
- Week 12 taught experiment tracking.
- Week 13 taught search behind a stable interface.
The CLI pattern was: parse user input, call a service, present the result.
The API pattern is: parse HTTP input, call a service, return JSON.
The shape changes, but the ownership rule does not.
Services should not import FastAPI.
Core should not import API schemas.
Routes should not import parser internals or SQL cursor logic.
Tests should use fakes when real storage would distract from the API contract.

## What problem this week solves

The project needs a way for non-CLI clients to read paper data.
A browser, script, notebook, or future frontend cannot conveniently import CLI commands.
HTTP provides a common language for those clients.
The problem is not simply creating endpoints.
The real problem is exposing existing use cases without breaking architecture.
The API has to validate raw inputs.
The API has to choose accurate status codes.
The API has to serialize domain results into public JSON.
The API has to keep expected errors readable and unexpected errors safe.
The API has to be tested without a live server.
- `GET /health` proves the app is alive.
- `GET /papers` proves collection reads work.
- `GET /papers/{id}` proves identity lookup and 404 mapping work.
- `GET /papers/search?q=...` proves query input and search delegation work.

## Beginner mental model

Think of the API as a reception desk.
The client asks the desk for something.
The desk checks the request form.
The desk asks the correct internal team.
The internal team is the service layer.
The desk returns a standard response form.
The standard response form is JSON shaped by Pydantic.
The desk should not walk into the archive and reorganize papers itself.
That would be business logic in the wrong place.
Every endpoint can be traced with five boxes: request, validation, dependency, service call, response.
- Request: method plus path, such as `GET /papers/paper-001`.
- Validation: path/query/body values become typed Python inputs.
- Dependency: FastAPI supplies the service through `Depends`.
- Service call: the route asks the service for the result.
- Response: the route maps the result or error to status code and JSON.

## Core vocabulary

| Term | Simple meaning | ResearchOps meaning |
|---|---|---|
| HTTP | Request-response protocol | How external clients ask ResearchOps for data |
| Client | Request sender | Browser, test, script, notebook, or future UI |
| Server | Request receiver | The FastAPI app |
| Method | HTTP action word | `GET` for read endpoints this week |
| Path | URL location | `/papers` or `/health` |
| Path parameter | Variable path segment | `paper_id` in `/papers/{paper_id}` |
| Query parameter | Small URL option | `q` in `/papers/search?q=graphs` |
| Body | JSON payload | Useful for structured input, but read endpoints mostly use path/query |
| Status code | Numeric outcome | `200`, `404`, `422`, `500` |
| Route | Method/path to function mapping | A FastAPI handler |
| Pydantic model | Typed data contract | Request or response schema |
| Dependency | Object supplied to a route | Usually a service |
| Provider | Function that returns dependency | `get_paper_service` |
| Service | Use-case owner | Same layer used by CLI |
| DTO | Data transfer object | API schema separate from domain model |
| Serialization | Python to JSON conversion | Response model output |
| TestClient | In-memory API test client | Calls app without uvicorn |
| OpenAPI | API documentation format | Generated from FastAPI metadata |

## Concept explanations from first principles

### HTTP request and response

- A request has a method, path, optional headers, and sometimes a body.
- A response has a status code, headers, and usually a body.
- JSON is used because it maps cleanly to Python dictionaries, lists, strings, numbers, booleans, and null.
- `client.get("/health")` builds an HTTP-like request in memory.
- Returning `{"status":"ok"}` lets FastAPI produce JSON.

### Routes

- `@app.get("/health")` registers a function for one method and path.
- The decorator runs at import time; the function body runs per request.
- No matching path gives 404 automatically.
- Wrong method on an existing path gives 405 automatically.
- Route names, tags, and models feed generated documentation.

### Path parameters

- `/papers/{paper_id}` captures part of the URL.
- A request to `/papers/abc` gives `paper_id="abc"`.
- Type annotations tell FastAPI how to parse the value.
- Use path parameters for resource identity.
- A malformed typed path value can cause 422.

### Query parameters

- Query parameters appear after `?`.
- `/papers/search?q=graphs&limit=3` has two query parameters.
- Use query parameters for filtering, searching, and limits.
- A required query parameter has no default.
- Missing required query input returns 422 before service code runs.

### Pydantic request models

- A request model describes expected JSON input.
- FastAPI builds the model before calling the route.
- Bad body data produces 422.
- Use request models for structured body input.
- Do not put long business workflows in validators.

### Pydantic response models

- A response model describes promised output.
- It protects clients from accidental shape changes.
- It helps prevent internal fields leaking.
- It makes tests and docs clearer.
- It is part of the public API contract.

### Status codes

- 200 means the read succeeded.
- 201 means a creation succeeded, useful later but not central here.
- 404 means a requested resource is absent.
- 422 means validation failed at the HTTP boundary.
- 500 means unexpected server failure.

### Dependency injection

- `Depends(provider)` calls the provider and passes its return value.
- Provider functions are where entry points wire concrete services.
- Tests can override providers with fakes.
- Routes become easier to read and isolate.
- Services should not depend on FastAPI to receive their collaborators.

### App factory

- `create_app()` builds and configures a FastAPI object.
- Tests can call the factory for a clean app.
- The module can still expose `app = create_app()` for uvicorn.
- Routers and exception handlers can be registered inside the factory.
- Factories reduce test-state leaks.

### Testing

- `TestClient` exercises route matching, validation, dependencies, and serialization.
- It does not open a real network socket.
- Assert the status code before the JSON body.
- Use fake services for deterministic tests.
- Dependency overrides prove routes delegate.

## ResearchOps-specific application

ResearchOps stores, parses, classifies, experiments with, and searches research papers.
The API should expose paper-oriented operations, not storage internals.
A client should never need to know which repository implementation is active.
A client should not need to know how search scores are calculated.
The public contract is JSON.
The private implementation remains Python services and infrastructure.
### Endpoint /health
- Story: liveness check.
- Rule: No business service required.
- Boundary: no parsing, SQL, ranking, or ML inference inside the route.
- Test: use a fake service and assert status code plus JSON.

### Endpoint /papers
- Story: list known papers.
- Rule: Call paper service and map each paper to a response schema.
- Boundary: no parsing, SQL, ranking, or ML inference inside the route.
- Test: use a fake service and assert status code plus JSON.

### Endpoint /papers/{paper_id}
- Story: read one paper.
- Rule: Call paper service and map missing-paper errors to 404.
- Boundary: no parsing, SQL, ranking, or ML inference inside the route.
- Test: use a fake service and assert status code plus JSON.

### Endpoint /papers/search?q=QUERY
- Story: search papers.
- Rule: Call search service and return ranked response schemas.
- Boundary: no parsing, SQL, ranking, or ML inference inside the route.
- Test: use a fake service and assert status code plus JSON.

Suggested file roles:
- `api/main.py`: app factory and router inclusion.
- `api/schemas.py`: Pydantic API models.
- `api/dependencies.py`: provider functions.
- `api/routes/health.py`: health endpoint.
- `api/routes/papers.py`: paper and search endpoints.

## Code examples with line-by-line explanation

### App factory

```python
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(title="ResearchOps API")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app

app = create_app()
```

- Line 1: `from fastapi import FastAPI` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 3: `def create_app() -> FastAPI:` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 4: `app = FastAPI(title="ResearchOps API")` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 6: `@app.get("/health")` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 7: `def health() -> dict[str, str]:` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 8: `return {"status": "ok"}` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 10: `return app` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 12: `app = create_app()` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.

### Schemas

```python
from pydantic import BaseModel, Field

class PaperResponse(BaseModel):
    id: str
    title: str
    abstract: str | None = None
    year: int | None = Field(default=None, ge=1900)

class SearchResultResponse(BaseModel):
    paper: PaperResponse
    score: float
```

- Line 1: `from pydantic import BaseModel, Field` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 3: `class PaperResponse(BaseModel):` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 4: `id: str` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 5: `title: str` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 6: `abstract: str | None = None` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 7: `year: int | None = Field(default=None, ge=1900)` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 9: `class SearchResultResponse(BaseModel):` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 10: `paper: PaperResponse` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 11: `score: float` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.

### Dependency provider

```python
from researchops.services.paper_service import PaperService
from researchops.storage.sqlite_repository import SqlitePaperRepository

def get_paper_service() -> PaperService:
    repository = SqlitePaperRepository("researchops.db")
    return PaperService(repository=repository)
```

- Line 1: `from researchops.services.paper_service import PaperService` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 2: `from researchops.storage.sqlite_repository import SqlitePaperRepository` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 4: `def get_paper_service() -> PaperService:` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 5: `repository = SqlitePaperRepository("researchops.db")` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 6: `return PaperService(repository=repository)` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Notice that concrete infrastructure is wired at the entry point, while the service should still be designed around core protocols.

### List route

```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/papers", tags=["papers"])

@router.get("", response_model=list[PaperResponse])
def list_papers(service: PaperService = Depends(get_paper_service)) -> list[PaperResponse]:
    papers = service.list_papers()
    return [to_paper_response(paper) for paper in papers]
```

- Line 1: `from fastapi import APIRouter, Depends` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 3: `router = APIRouter(prefix="/papers", tags=["papers"])` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 5: `@router.get("", response_model=list[PaperResponse])` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 6: `def list_papers(service: PaperService = Depends(get_paper_service)) -> list[PaperResponse]:` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 7: `papers = service.list_papers()` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 8: `return [to_paper_response(paper) for paper in papers]` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.

### 404 mapping

```python
from fastapi import HTTPException, status
from researchops.core.exceptions import PaperNotFoundError

@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: str, service: PaperService = Depends(get_paper_service)) -> PaperResponse:
    try:
        paper = service.get_paper(paper_id)
    except PaperNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    return to_paper_response(paper)
```

- Line 1: `from fastapi import HTTPException, status` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 2: `from researchops.core.exceptions import PaperNotFoundError` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 4: `@router.get("/{paper_id}", response_model=PaperResponse)` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 5: `def get_paper(paper_id: str, service: PaperService = Depends(get_paper_service)) -> PaperResponse:` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 6: `try:` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 7: `paper = service.get_paper(paper_id)` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 8: `except PaperNotFoundError as error:` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 9: `raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 11: `return to_paper_response(paper)` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.

### Search route

```python
@router.get("/search", response_model=list[SearchResultResponse])
def search_papers(
    q: str,
    limit: int = 10,
    service: SearchService = Depends(get_search_service),
) -> list[SearchResultResponse]:
    results = service.search(query=q, limit=limit)
    return [to_search_response(result) for result in results]
```

- Line 1: `@router.get("/search", response_model=list[SearchResultResponse])` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 2: `def search_papers(` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 3: `q: str,` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 4: `limit: int = 10,` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 5: `service: SearchService = Depends(get_search_service),` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 6: `) -> list[SearchResultResponse]:` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 7: `results = service.search(query=q, limit=limit)` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 8: `return [to_search_response(result) for result in results]` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.

### TestClient test

```python
from fastapi.testclient import TestClient
from researchops.api.main import create_app
from researchops.api.dependencies import get_paper_service

def test_get_paper_returns_json() -> None:
    app = create_app()
    app.dependency_overrides[get_paper_service] = lambda: FakePaperService()
    client = TestClient(app)

    response = client.get("/papers/paper-001")

    assert response.status_code == 200
    assert response.json()["id"] == "paper-001"
```

- Line 1: `from fastapi.testclient import TestClient` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 2: `from researchops.api.main import create_app` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 3: `from researchops.api.dependencies import get_paper_service` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 5: `def test_get_paper_returns_json() -> None:` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 6: `app = create_app()` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 7: `app.dependency_overrides[get_paper_service] = lambda: FakePaperService()` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 8: `client = TestClient(app)` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 10: `response = client.get("/papers/paper-001")` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 12: `assert response.status_code == 200` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- Line 13: `assert response.json()["id"] == "paper-001"` — this line has one job in the HTTP adapter. Read it by asking whether it registers the app, defines input, injects a service, delegates behavior, maps an error, or shapes JSON.
- This test proves the route can be called without a live server and can receive a fake service.

### Additional beginner walkthrough: request shapes

#### Health request

- Client sends: GET /health.
- FastAPI matches: method GET and path /health.
- Route receives: no path parameter, no query parameter, no body.
- Route delegates: no service needed because this is liveness, not business data.
- Route returns: a small dictionary.
- FastAPI serializes: dictionary to JSON.
- Client sees: status 200 and body {"status":"ok"}.

#### List papers request

- Client sends: GET /papers.
- FastAPI matches: the papers collection route.
- Route receives: no body and usually no required query.
- Dependency provider returns: paper service.
- Route delegates: service.list_papers or equivalent.
- Service owns: how papers are retrieved.
- Route maps: each domain paper to PaperResponse.
- Client sees: status 200 and a JSON array.

#### Single paper request

- Client sends: GET /papers/paper-001.
- FastAPI matches: /papers/{paper_id}.
- Route receives: paper_id as the string paper-001.
- Dependency provider returns: paper service.
- Route delegates: service.get_paper(paper_id).
- Service owns: whether that paper exists.
- Route maps success: domain Paper to PaperResponse.
- Route maps missing: PaperNotFoundError to HTTP 404.
- Client sees: one JSON object or a 404 error body.

#### Search request

- Client sends: GET /papers/search?q=graphs&limit=3.
- FastAPI matches: the search route.
- Route receives: q as text and limit as int.
- FastAPI validates: missing q or non-integer limit before service call.
- Dependency provider returns: search service.
- Route delegates: service.search(query=q, limit=limit).
- Service owns: ranking and retrieval.
- Route maps: service results to SearchResultResponse.
- Client sees: status 200 and a JSON array of hits.

### Additional code example: explicit query validation with `Query`

```python
from typing import Annotated
from fastapi import Query

SearchQuery = Annotated[str, Query(min_length=1, description="Text to search for")]
SearchLimit = Annotated[int, Query(ge=1, le=50, description="Maximum hits to return")]

@router.get("/search", response_model=list[SearchResultResponse])
def search_papers(
    q: SearchQuery,
    limit: SearchLimit = 10,
    service: SearchService = Depends(get_search_service),
) -> list[SearchResultResponse]:
    results = service.search(query=q, limit=limit)
    return [to_search_response(result) for result in results]
```

- Line 1: imports `Annotated`, which lets one type carry extra FastAPI validation metadata.
- Line 2: imports `Query`, the FastAPI helper for query-parameter constraints.
- Line 3: adds a visual pause between imports and type aliases.
- Line 4: defines a reusable query type; it is still a string, but it must have at least one character.
- Line 5: defines a reusable limit type; it must be at least 1 and at most 50.
- Line 6: adds a visual pause before the route.
- Line 7: registers the endpoint and promises a list response.
- Line 8: starts a readable multi-line function definition.
- Line 9: declares required query text with validation metadata.
- Line 10: declares optional limit with default 10 and bounds.
- Line 11: injects the search service through the provider.
- Line 12: states the Python return type.
- Line 13: delegates actual search behavior to the service.
- Line 14: maps service results into API response objects.

The validation rule here is an HTTP-boundary rule because it protects the route from an empty query and a dangerous result size.
The ranking rule is still not here because ranking is business/search behavior.

### Additional code example: mapper helpers

```python
def to_paper_response(paper: Paper) -> PaperResponse:
    return PaperResponse(
        id=paper.id,
        title=paper.title,
        abstract=paper.abstract,
        year=paper.year,
    )

def to_search_response(result: SearchResult) -> SearchResultResponse:
    return SearchResultResponse(
        paper=to_paper_response(result.paper),
        score=result.score,
    )
```

- Line 1: `def to_paper_response(paper: Paper) -> PaperResponse:` keeps response-shaping code explicit and local to the API boundary.
- Line 2: `return PaperResponse(` keeps response-shaping code explicit and local to the API boundary.
- Line 3: `id=paper.id,` keeps response-shaping code explicit and local to the API boundary.
- Line 4: `title=paper.title,` keeps response-shaping code explicit and local to the API boundary.
- Line 5: `abstract=paper.abstract,` keeps response-shaping code explicit and local to the API boundary.
- Line 6: `year=paper.year,` keeps response-shaping code explicit and local to the API boundary.
- Line 7: `)` keeps response-shaping code explicit and local to the API boundary.
- Line 9: `def to_search_response(result: SearchResult) -> SearchResultResponse:` keeps response-shaping code explicit and local to the API boundary.
- Line 10: `return SearchResultResponse(` keeps response-shaping code explicit and local to the API boundary.
- Line 11: `paper=to_paper_response(result.paper),` keeps response-shaping code explicit and local to the API boundary.
- Line 12: `score=result.score,` keeps response-shaping code explicit and local to the API boundary.
- Line 13: `)` keeps response-shaping code explicit and local to the API boundary.

Mapper helpers are useful when several routes return the same public shape.
They should not perform storage queries, search ranking, parsing, or ML inference.
They translate one already-known object into one public response object.

### Additional code example: async test style without async feature creep

```python
import httpx
import pytest

from researchops.api.main import create_app

@pytest.mark.anyio
async def test_health_with_async_client() -> None:
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- Line 1: imports httpx for the async client.
- Line 2: imports pytest so the test can be marked for async execution.
- Line 3: separates imports by source.
- Line 4: imports the app factory.
- Line 5: adds a visual pause.
- Line 6: marks the test as async-capable.
- Line 7: defines an async test function.
- Line 8: creates a clean app.
- Line 9: wraps the app in an ASGI transport instead of opening a network port.
- Line 10: creates an async client pointed at the in-memory app.
- Line 11: awaits one GET request.
- Line 12: adds a visual pause before assertions.
- Line 13: asserts the status code.
- Line 14: asserts the JSON body.

This test style does not mean Week 14 is implementing async network fetching.
It only changes how the test client calls the ASGI app.
The endpoint can remain a normal synchronous route if it calls synchronous services.

### Additional beginner checkpoint: layer ownership table

| Question | Correct owner | Why |
|---|---|---|
| What JSON field should clients see? | API schema | It is an external contract. |
| How is a paper loaded? | Service/repository | It is application behavior and persistence. |
| What status code means missing paper? | API route | It is HTTP translation. |
| How are search results ranked? | Search service/infrastructure | It is search behavior, not transport. |
| What database path is used? | Entry-point wiring/config | It selects concrete infrastructure. |
| What does the CLI print? | CLI adapter | It is terminal presentation. |
| What does the API return? | API adapter | It is HTTP presentation. |
| What is a Paper? | Core domain | It is central project vocabulary. |

### Trace drill 1: /health
- Write the exact request method and path. Focus: liveness without service.
- Name the route that should match, or say no route should match. Focus: liveness without service.
- Name every input value FastAPI extracts. Focus: liveness without service.
- Name the dependency provider, if any. Focus: liveness without service.
- Name the service method, if any. Focus: liveness without service.
- Name the expected status code. Focus: liveness without service.
- Name the expected JSON shape. Focus: liveness without service.
- Name the test assertion that proves the behavior. Focus: liveness without service.

### Trace drill 2: /papers
- Write the exact request method and path. Focus: collection response.
- Name the route that should match, or say no route should match. Focus: collection response.
- Name every input value FastAPI extracts. Focus: collection response.
- Name the dependency provider, if any. Focus: collection response.
- Name the service method, if any. Focus: collection response.
- Name the expected status code. Focus: collection response.
- Name the expected JSON shape. Focus: collection response.
- Name the test assertion that proves the behavior. Focus: collection response.

### Trace drill 3: /papers/{paper_id}
- Write the exact request method and path. Focus: identity lookup.
- Name the route that should match, or say no route should match. Focus: identity lookup.
- Name every input value FastAPI extracts. Focus: identity lookup.
- Name the dependency provider, if any. Focus: identity lookup.
- Name the service method, if any. Focus: identity lookup.
- Name the expected status code. Focus: identity lookup.
- Name the expected JSON shape. Focus: identity lookup.
- Name the test assertion that proves the behavior. Focus: identity lookup.

### Trace drill 4: /papers/search
- Write the exact request method and path. Focus: query validation.
- Name the route that should match, or say no route should match. Focus: query validation.
- Name every input value FastAPI extracts. Focus: query validation.
- Name the dependency provider, if any. Focus: query validation.
- Name the service method, if any. Focus: query validation.
- Name the expected status code. Focus: query validation.
- Name the expected JSON shape. Focus: query validation.
- Name the test assertion that proves the behavior. Focus: query validation.

### Trace drill 5: /papers/search?limit=bad
- Write the exact request method and path. Focus: 422 validation.
- Name the route that should match, or say no route should match. Focus: 422 validation.
- Name every input value FastAPI extracts. Focus: 422 validation.
- Name the dependency provider, if any. Focus: 422 validation.
- Name the service method, if any. Focus: 422 validation.
- Name the expected status code. Focus: 422 validation.
- Name the expected JSON shape. Focus: 422 validation.
- Name the test assertion that proves the behavior. Focus: 422 validation.

### Trace drill 6: /papers/missing
- Write the exact request method and path. Focus: 404 mapping.
- Name the route that should match, or say no route should match. Focus: 404 mapping.
- Name every input value FastAPI extracts. Focus: 404 mapping.
- Name the dependency provider, if any. Focus: 404 mapping.
- Name the service method, if any. Focus: 404 mapping.
- Name the expected status code. Focus: 404 mapping.
- Name the expected JSON shape. Focus: 404 mapping.
- Name the test assertion that proves the behavior. Focus: 404 mapping.

### Trace drill 7: /not-real
- Write the exact request method and path. Focus: framework 404.
- Name the route that should match, or say no route should match. Focus: framework 404.
- Name every input value FastAPI extracts. Focus: framework 404.
- Name the dependency provider, if any. Focus: framework 404.
- Name the service method, if any. Focus: framework 404.
- Name the expected status code. Focus: framework 404.
- Name the expected JSON shape. Focus: framework 404.
- Name the test assertion that proves the behavior. Focus: framework 404.

### Trace drill 8: POST /health
- Write the exact request method and path. Focus: 405 method failure.
- Name the route that should match, or say no route should match. Focus: 405 method failure.
- Name every input value FastAPI extracts. Focus: 405 method failure.
- Name the dependency provider, if any. Focus: 405 method failure.
- Name the service method, if any. Focus: 405 method failure.
- Name the expected status code. Focus: 405 method failure.
- Name the expected JSON shape. Focus: 405 method failure.
- Name the test assertion that proves the behavior. Focus: 405 method failure.

## Common beginner mistakes

- Mistake: Putting search ranking in the route. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Importing FastAPI inside services. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Returning raw domain objects without response schemas. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Using `200` for missing data. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Testing only through uvicorn. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Overriding the wrong dependency provider. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Letting dependency overrides leak between tests. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Confusing `/papers/search` with `/papers/{paper_id}`. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Parsing query strings manually. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Catching every exception and returning success. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Adding Docker or workers early. Recovery: identify the owner of the behavior and move it to the correct layer.
- Mistake: Making routes async just because FastAPI supports async. Recovery: identify the owner of the behavior and move it to the correct layer.

## Debugging guidance

- If you see 404: Check path, method, router inclusion, and prefix.
- If you see 405: Path exists but HTTP method is wrong.
- If you see 422: Inspect `response.json()["detail"]` for field location.
- If you see 500: Your code ran and raised an unexpected exception.
- If you see wrong fake: Compare dependency override key with the provider used in `Depends`.
- If you see bad JSON: Check response model and mapper.
- If you see wrong docs: Check route decorator, tags, model annotations, and docstring.
1. Read status code.
2. Read response body.
3. Identify layer that produced failure.
4. Fix the owner layer only.
5. Add or update the focused test.

## Design tradeoffs

- global app vs factory: use factory for clean tests and module app for uvicorn.
- one file vs routers: start simple, split when scanning gets hard.
- domain model vs API schema: schemas protect the external contract.
- sync vs async route: sync is fine for synchronous service calls this week.
- detailed vs safe errors: expected errors can be specific; unexpected errors should be safe.
- manual dict vs Pydantic: Pydantic is clearer for public contracts.
- provider per request vs lifecycle: simple providers teach the boundary first.

## Testing implications

- Test: health returns 200 and ok JSON.
- Test: list papers returns fake data.
- Test: get paper success returns one fake paper.
- Test: missing paper maps to 404.
- Test: search forwards q and limit to fake service.
- Test: missing q returns 422.
- Test: invalid limit returns 422 if bounded.
- Test: response JSON contains only public fields.
- Test: dependency override is isolated per test.
- Test: route does not call real storage in unit tests.
Arrange: create app, install fake dependency, create client.
Act: send one request.
Assert: status code, JSON body, and important fake-service call details.

## Architecture implications

Allowed: API imports services, core, config, and concrete infrastructure for wiring.
Forbidden: services importing FastAPI.
Forbidden: core importing API schemas.
Forbidden: routes owning SQL, parsing, ranking, or ML decisions.
Healthy direction is API -> services -> core protocols.
Concrete infrastructure implements core protocols and is selected by entry points.
- HTTPException mapping: API.
- search ranking: service/search infrastructure.
- paper existence: service/repository.
- JSON field names: API schema.
- database file path wiring: entry point/config.
- CLI/API shared behavior: service.

## How this connects to AI engineering / ML research

AI engineering needs reliable interfaces around model and data capabilities.
A search engine hidden behind a script is hard to reuse.
A tested API makes paper search reachable by scripts, notebooks, and future user interfaces.
Stable JSON contracts make experiments easier to compare.
Accurate failures prevent silent data mistakes.
This week adds access, not new model intelligence.
That restraint is part of engineering maturity.

## Mini quizzes

1. What is an HTTP method?
2. What is a path parameter?
3. What is a query parameter?
4. Why does missing `q` return 422?
5. Why should missing paper return 404?
6. What does `Depends` do?
7. Why use response models?
8. Why should routes be thin?
9. Which layer owns ranking?
10. Which layer imports FastAPI?
11. Why test without uvicorn?
12. How do dependency overrides work?
13. What should not be built this week?
14. How does API mirror CLI?
15. What does app factory solve?
16. What is OpenAPI generated from?
17. Why assert status code first?
18. What is a DTO?
19. What is serialization?
20. What prepares Week 15?

## Explain-it-aloud prompts

- Explain request to response for `/health`.
- Explain request to response for `/papers/{id}`.
- Explain why API routes delegate to services.
- Explain where validation happens.
- Explain why `HTTPException` is an adapter concern.
- Explain a fake service test.
- Explain 200 vs 404 vs 422 vs 500.
- Explain why response schemas are not storage schemas.
- Explain how CLI and API stay consistent.
- Explain what future topics are intentionally excluded.

## What to memorize

- `FastAPI()` creates the app.
- `@app.get` registers a GET endpoint.
- `APIRouter` groups routes.
- `Depends` injects dependencies.
- `HTTPException` returns HTTP errors.
- `response_model` declares output shape.
- `TestClient` tests in memory.
- `dependency_overrides` installs fakes.
- `200`, `404`, `422`, `500` have distinct meanings.
- Routes are adapters over services.

## What to understand deeply

- HTTP is a boundary, not the application itself.
- Validation at the edge protects services.
- Status codes are part of the contract.
- Dependency injection enables test isolation.
- Response schemas prevent accidental leakage.
- Expected domain errors need HTTP mapping.
- Unexpected errors should be safe for clients.
- The API and CLI should share services.
- Clean architecture makes new entry points cheap.
- Deferring future-week concepts keeps the curriculum teachable.

## What not to worry about yet

- Do not worry about Docker deployment yet.
- Do not worry about background workers yet.
- Do not worry about RAG prompts yet.
- Do not worry about async arXiv fetching yet.
- Do not worry about authentication systems yet.
- Do not worry about perfect API versioning yet.
- Do not worry about frontend design yet.
- Do not worry about large-scale lifecycle tuning yet.
- Do not worry about model optimization yet.
- Do not worry about every FastAPI feature yet.

## Bridge to next week

Week 15 adds async I/O network fetching.
Week 14 prepares for it by giving the project a clean HTTP boundary.
A clean route can later call a service that performs I/O responsibly.
A messy route will become harder when network failures arrive.
Before moving on, explain health, paper lookup, search, dependency overrides, and 404 mapping aloud.
The bridge sentence: Week 14 opens the HTTP front door; Week 15 teaches selected services how to fetch network data behind that door.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 14 — FastAPI Layer:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
