# Notes - Week 14 FastAPI Layer

## What a web API is

An API is a way for one program to talk to another. A web API uses HTTP — the same protocol a web browser uses — so that any program, on any machine, can communicate with your application over a network.

Until now, ResearchOps only ran from the command line. That means only a human with terminal access can use it. An HTTP API changes that: a web frontend, a mobile app, a data pipeline, a teammate's script, or an automated test can all send a request and get a structured response.

---

## HTTP from first principles

HTTP is a request-response protocol. A client sends a request. The server returns a response. That is the entire model.

### The request

A request has four main parts:

**Method** — a verb that describes what the client wants to do.

| Method | Meaning |
|--------|---------|
| `GET` | Read or retrieve something |
| `POST` | Create or submit something |
| `PUT` | Replace something |
| `PATCH` | Update part of something |
| `DELETE` | Remove something |

**Path** — the URL path that identifies the resource. For example `/search`, `/documents/42`, `/health`.

**Query parameters** — optional key-value pairs appended to the URL after a `?`. For example: `/search?query=transformers&limit=5`. They are often used to filter or configure a GET request.

**Body** — data sent with the request. Usually JSON. Only meaningful for methods like POST, PUT, and PATCH. GET requests should not have a body.

### The response

A response has three main parts:

**Status code** — a three-digit number that tells the client whether the request succeeded or failed, and why.

| Code | Meaning |
|------|---------|
| `200 OK` | Request succeeded. Response body contains the result. |
| `201 Created` | Resource was created successfully. |
| `400 Bad Request` | Client sent invalid input. The client must fix the request. |
| `404 Not Found` | The resource does not exist. |
| `422 Unprocessable Entity` | FastAPI validation error — the body did not match the schema. |
| `500 Internal Server Error` | Something unexpected broke on the server side. |

**Headers** — metadata about the response. For example, `Content-Type: application/json` tells the client the body is JSON.

**Body** — the response data. Usually JSON when building an API.

---

## JSON

JSON is the standard text format for API data. It maps closely to Python dicts, lists, strings, numbers, and booleans.

```json
{
  "query": "attention mechanism",
  "limit": 5,
  "results": [
    {"title": "Transformers paper", "score": 0.92, "snippet": "..."},
    {"title": "BERT", "score": 0.88, "snippet": "..."}
  ]
}
```

Python's `json` module can parse and generate JSON. FastAPI does this automatically for you when you return a dict or a Pydantic model.

---

## FastAPI from first principles

FastAPI is a Python web framework. It lets you define routes — URL paths with handler functions — and handles the HTTP plumbing for you.

```python
from fastapi import FastAPI       # line 1

app = FastAPI()                   # line 2


@app.get("/health")               # line 3
def health() -> dict[str, str]:   # line 4
    return {"status": "ok"}       # line 5
```

Line 1: import the `FastAPI` class.

Line 2: create the application object. This is the central object that registers routes and starts the server.

Line 3: the `@app.get("/health")` decorator tells FastAPI: "when a GET request arrives at `/health`, call the function below". The decorator registers the route.

Line 4: the handler function. It takes no parameters here because this is a simple status check.

Line 5: return a Python dict. FastAPI automatically serialises this to JSON and sets `Content-Type: application/json`.

To run locally:
```bash
uvicorn researchops.api.main:app --reload
```

Then visit `http://localhost:8000/health` in a browser or with `curl`.

---

## Pydantic models for validation

Pydantic is FastAPI's data validation library. You define a class that inherits from `BaseModel`, declare fields with types, and Pydantic validates incoming data automatically.

```python
from pydantic import BaseModel    # line 1


class SearchRequest(BaseModel):   # line 2
    query: str                    # line 3
    limit: int = 5                # line 4
```

Line 1: import `BaseModel` from Pydantic.

Line 2: define the schema. Any class inheriting `BaseModel` becomes a schema.

Line 3: `query` is a required `str`. If the client omits it or sends a non-string, Pydantic raises a validation error and FastAPI returns `422` automatically.

Line 4: `limit` is an optional `int` with a default of 5. If the client does not include it, the default is used.

Response schemas work the same way:

```python
class SearchHitResponse(BaseModel):
    title: str
    score: float
    snippet: str
```

When you return an instance of this class, FastAPI serialises it to JSON. The fields and types are documented automatically.

---

## Why API comes after CLI

Weeks 1–12 built the CLI, services, and storage. The API reuses all of that. The rule is:

> Route handlers must stay thin. They parse input, call a service, and shape the response. Business logic belongs in services, not in routes.

A route that does its own database queries, validation, and computation is hard to test, hard to maintain, and breaks the separation of concerns built in earlier weeks.

Compare a fat route to a thin route:

**Fat route (wrong):**
```python
@app.post("/search")
def search(body: dict) -> list:
    # queries database directly
    # applies ranking logic here
    # formats response here
    return results
```

**Thin route (correct):**
```python
@app.post("/search")
def search(request: SearchRequest, service: SearchService = Depends(get_search_service)) -> list[SearchHitResponse]:
    hits = service.search(request.query, request.limit)
    return [SearchHitResponse(title=h.title, score=h.score, snippet=h.snippet) for h in hits]
```

The thin route does exactly three things: receive the validated request, call the service, and map the result to a response schema.

---

## Dependency injection

Dependency injection means a function receives the objects it needs rather than constructing them itself. FastAPI has a built-in system for this using `Depends`.

```python
from fastapi import Depends


def get_search_service() -> SearchService:      # line 1
    return SearchService(...)                   # line 2


@app.post("/search")
def search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),   # line 3
) -> list[SearchHitResponse]:
    hits = service.search(request.query, request.limit)
    return [SearchHitResponse(...) for h in hits]
```

Line 1: a plain Python function that returns a `SearchService`. This is a "dependency provider".

Line 2: construct and return the service. In practice this might read from settings, open a database connection, and pass it to the service.

Line 3: `Depends(get_search_service)` tells FastAPI: before calling `search`, call `get_search_service()` and pass its return value as `service`. FastAPI handles this for every request.

Why does this matter for tests? In tests you can replace the dependency with a fake:

```python
from fastapi.testclient import TestClient

app.dependency_overrides[get_search_service] = lambda: FakeSearchService()
client = TestClient(app)
```

Now every test request uses `FakeSearchService` instead of the real one. No database, no file system, fast tests.

---

## Status codes and error mapping

Do not return `200` for every response. Status codes carry meaning that clients rely on.

```python
from fastapi import HTTPException


@app.get("/documents/{doc_id}")
def get_document(doc_id: str, service: DocumentService = Depends(get_doc_service)) -> DocumentResponse:
    doc = service.get(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")
    return DocumentResponse(...)
```

`HTTPException` is FastAPI's way to return an error response. The `detail` field is returned in the JSON body as `{"detail": "..."}`.

Common mapping rules:
- Domain "not found" → `404`
- Validation failure (your own logic) → `400` with a helpful message
- Unexpected exception → log it, return `500`, do not leak stack traces

Do not return `200` with `{"success": false}` in the body. That hides the error from automated clients.

---

## Testing the API

FastAPI's `TestClient` wraps the app in a test harness. Requests go through your route handlers, validation, and dependency injection — but no real network is involved.

```python
from fastapi.testclient import TestClient
from researchops.api.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")           # line 1
    assert response.status_code == 200         # line 2
    assert response.json() == {"status": "ok"} # line 3
```

Line 1: send a GET request to `/health`. Returns a `Response` object.

Line 2: check the HTTP status code.

Line 3: check the JSON body. `response.json()` parses the response body as JSON and returns a Python dict or list.

For routes that require a body:
```python
def test_search() -> None:
    response = client.post("/search", json={"query": "transformers", "limit": 3})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 3
```

Use `dependency_overrides` to inject fake services in tests. This avoids real database or file system operations.

---

## The API as an adapter

The most important architectural concept this week is that the API is just another adapter for your application. Your services, models, and storage did not change. The API layer is a new entry point — alongside the CLI — that connects the outside world to your existing logic.

This mirrors the CLI architecture from earlier weeks: CLI commands are thin adapters over services. API routes are thin adapters over the same services. Both use the same protocols and domain objects.

That is why good architecture from Month 3 pays dividends in Month 4. If services were well-defined and protocol-driven, adding an API layer is just plumbing.

---

## Summary

- HTTP is a request-response protocol: method + path + optional body → status code + body.
- Common methods: GET (read), POST (create/submit).
- Status codes communicate success (200, 201) and failure (400, 404, 500).
- FastAPI creates an app object, routes are registered with decorators.
- Pydantic models validate and document request and response data automatically.
- Route handlers must be thin: validate → call service → return response.
- Dependency injection keeps route code flexible and testable.
- Use `app.dependency_overrides` in tests to inject fakes.
- `TestClient` lets you test routes without a real server.
- The API is another adapter; services and business logic do not change.
