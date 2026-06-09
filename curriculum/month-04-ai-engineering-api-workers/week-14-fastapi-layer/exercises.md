# Exercises - Week 14 FastAPI Layer

## Warm-up exercises
1. Create a `/health` endpoint that returns JSON.
2. Define a Pydantic model with two fields and validate sample input.
3. Return a `404` response for a missing document ID.
4. Write one `TestClient` test for a GET route.

## Project exercises
1. Build the FastAPI app and route modules.
2. Add dependency providers that construct search or repository services.
3. Implement a search endpoint backed by existing logic.
4. Write integration tests for health, validation, and successful search responses.

## Stretch exercises
1. Add API pagination fields.
2. Add response models for ingestion summaries.
3. Override dependencies in tests with a fake service.

## Writing questions
1. Why should routes stay thin?
2. What did Pydantic validate for you automatically?
3. Which HTTP status codes did you need most?
4. How is the API layer similar to the CLI layer?
