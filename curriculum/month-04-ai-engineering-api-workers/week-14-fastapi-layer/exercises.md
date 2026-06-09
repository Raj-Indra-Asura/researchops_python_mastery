# Exercises - Week 14 FastAPI Layer

## Beginner

1. **Health endpoint.** Create a FastAPI app in `src/researchops/api/main.py`. Add a `GET /health` route that returns `{"status": "ok"}`. Run it with `uvicorn` and open `http://localhost:8000/health` in a browser. Then write a `TestClient` test that asserts the status code is 200 and the body matches.

2. **Pydantic model validation.** Define a `SearchRequest` model with `query: str` and `limit: int = 5`. Write a standalone Python script (outside FastAPI) that tries to construct `SearchRequest(query=123, limit="five")`. What error does Pydantic raise? Read the error message. Then fix the call to use the correct types.

3. **404 for missing resource.** Add a `GET /documents/{doc_id}` route that raises `HTTPException(status_code=404)` for any `doc_id`. Write a test that sends a GET request to `/documents/missing` and asserts the status code is 404.

4. **Query parameters.** Add a `GET /search` route that accepts `query` and `limit` as URL query parameters (not a JSON body). For example: `/search?query=transformers&limit=3`. Return them echoed back as JSON. Write a test using `client.get("/search?query=transformers&limit=3")`.

5. **Response model.** Define a `SearchHitResponse` Pydantic model with `title: str`, `score: float`, and `snippet: str`. Have a POST `/search` route return a list of three hardcoded `SearchHitResponse` instances. Write a test that checks the response body is a list of length 3 and each item has a `score` field.

---

## Intermediate

1. **Thin route with service.** Implement `get_search_service` as a dependency provider that returns a `FakeSearchService`. Wire it into a `POST /search` route using `Depends`. The fake service should return two `SearchHit` objects with known titles. Write a test that overrides the dependency with the fake and asserts those titles appear in the response.

2. **Validation error shape.** Post a request to `/search` with a missing `query` field. FastAPI returns `422`. Inspect `response.json()` in a test. Find the `"detail"` array and assert it contains a message mentioning `"query"`. This teaches you how to read FastAPI's automatic validation errors.

3. **Error mapping.** In your search service, raise a custom `PaperNotFoundError` when the paper doesn't exist. In the route, catch that exception and raise `HTTPException(status_code=404)`. Write two tests: one for a successful search, one for a missing document, asserting the correct status codes.

4. **Dependency override in tests.** Write a test file that creates two different `FakeSearchService` implementations: one that returns results, one that raises an exception. Override the dependency for each test function and assert that the correct behaviour occurs in each case.

5. **OpenAPI docs check.** Run `uvicorn` locally. Visit `http://localhost:8000/docs`. Read the auto-generated API documentation. Identify where FastAPI read the information from — it comes from your Pydantic models and docstrings. Add a docstring to one route function and reload the docs to see it appear.

---

## Advanced

1. **Pagination.** Add `page: int = 1` and `page_size: int = 10` fields to `SearchRequest`. In the route, use them to slice the results from the service. Add a `PaginatedSearchResponse` model with `items: list[SearchHitResponse]`, `page: int`, `page_size: int`, and `total: int`. Write tests that verify the correct slice is returned for different page numbers.

2. **Global exception handler.** Add a FastAPI exception handler using `@app.exception_handler(Exception)`. It should log the exception and return a `500` response with a generic error message, not a stack trace. Write a test that forces an unhandled exception in a route and asserts the response is `500` with a non-revealing body.

3. **Request logging middleware.** Add FastAPI middleware using `@app.middleware("http")`. Log the method, path, and response status code for every request. Use Python's standard `logging` module. Write a test that calls one route and then checks the log output (capture logs with `caplog` in pytest).

4. **API router separation.** Move routes into separate files: `src/researchops/api/routes/health.py`, `src/researchops/api/routes/search.py`. Use `APIRouter` and `include_router` in `main.py`. Write tests that confirm all routes still work after the reorganisation.

5. **Response caching header.** Add a `Cache-Control: no-store` header to all search responses to prevent clients from caching results (which might become stale). Use FastAPI's `Response` object or middleware to add the header. Write a test that asserts the header is present in the search response.

---

## Brutal

1. **Full search API integration.** Wire your `Week 13` semantic search service into the API. `POST /search` should call `SemanticSearchService.search()`, which chunks, embeds, and retrieves. Use `FakeEmbeddingModel` in tests. Write an end-to-end integration test that indexes a document through the API and retrieves it via the search route. This tests the complete stack from HTTP to vector search.

2. **Document ingestion endpoint.** Add `POST /documents/ingest` that accepts `{"title": "...", "text": "..."}` in the body, calls the ingestion service, and returns `201 Created` with the new document ID. Handle validation errors (empty title), duplicate documents (409 Conflict), and unexpected errors (500). Write tests for all four cases.

3. **API versioning.** Add a `/v1/` prefix to all existing routes. Add a `GET /` route that returns metadata about available API versions. Ensure existing tests still pass. Think about: if you add `/v2/` later, how would you avoid duplicating all route handlers?

4. **Auth stub.** Add an API key header requirement to all non-health routes: the client must send `X-API-Key: test-key` or the server returns `401 Unauthorized`. Implement this as a FastAPI dependency that reads the header and validates it against a configured key. In tests, pass the correct header. Also write a test that sends a wrong key and asserts `401`.

5. **Load testing baseline.** Use Python's `concurrent.futures.ThreadPoolExecutor` to send 100 requests to the health endpoint from a test. Measure how long they take. Document the result. This is not about optimisation — it is about knowing what baseline performance looks like before you add async workers and caching in later weeks.
