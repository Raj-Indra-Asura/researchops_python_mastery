# Break It - Week 14 FastAPI Layer

## Intentional failure experiments
1. Send a blank or malformed request body and inspect FastAPI validation errors.
2. Return a raw domain model that is not JSON-serializable and fix the response schema.
3. Raise a domain exception in a route and map it to an HTTP error intentionally.
4. Forget to wire a dependency and inspect the startup or request failure.
5. Call a missing route and compare `404` behavior with application errors.

## Debugging tasks
- Inspect `response.json()` in failing API tests.
- Override one dependency with a fake and compare results.
- Run `pytest -k api_ -v` while developing routes.

## Edge cases to explore
- Empty search query.
- Very large `limit` value.
- Missing document ID.
- Unexpected service exception.

## What did you learn?
- Which error should be handled at the route layer?
- What schema mismatch surprised you?
- How will you keep API responses stable over time?
