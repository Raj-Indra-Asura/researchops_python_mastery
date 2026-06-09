# Notes - Week 14 FastAPI Layer

An API layer gives other programs a stable way to use your application. Instead of only running CLI commands, clients can send HTTP requests. FastAPI is a productive framework because it uses Python type hints and Pydantic models to validate data automatically.

A minimal app looks like this:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

Routes should be thin, just like CLI commands. A route should parse input, call a service, and shape the response. Business logic belongs in services, not directly in the route function.

Pydantic models are useful for both requests and responses.

```python
from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


class SearchHitResponse(BaseModel):
    title: str
    score: float
    snippet: str
```

These models validate data and document the API shape. FastAPI also uses them to generate OpenAPI docs automatically.

Dependency injection means routes receive the collaborators they need from small provider functions.

```python
from fastapi import Depends


def get_search_service() -> SearchService:
    return SearchService(...)


@app.post("/search")
def search(request: SearchRequest, service: SearchService = Depends(get_search_service)):
    return service.search(request.query, request.limit)
```

This keeps route code flexible and testable. In tests, you can override the dependency with a fake service.

HTTP status codes communicate meaning. `200 OK` signals success. `400 Bad Request` means the client sent invalid input. `404 Not Found` means a resource is missing. `500 Internal Server Error` is for unexpected failures. Try not to return `200` for everything, because that hides useful semantics from clients.

FastAPI tests usually use `TestClient`.

```python
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

When mapping service errors to HTTP responses, avoid leaking internal stack traces. If a query is blank, return a clear validation-style response. If the database is unavailable, log the internal error and return a suitable server response.

An API boundary should not distort your architecture. The domain and application layers remain the same; FastAPI is simply another adapter, like the CLI. That is why week 9's protocol work matters. The API can depend on the same services already used elsewhere.

This week prepares the project for external integrations and future deployment. Once your logic is available behind HTTP routes, frontends, scripts, or other systems can build on top of ResearchOps without shelling into the machine.
