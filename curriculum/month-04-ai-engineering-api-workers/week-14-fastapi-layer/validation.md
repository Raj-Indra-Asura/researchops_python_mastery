# Validation - Week 14 FastAPI Layer

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,api,storage]"
uvicorn researchops.api.app:app --reload
pytest tests/integration/test_api_health.py -v
pytest tests/integration/test_api_search.py -v
```

## Expected outputs
- Uvicorn starts and serves the FastAPI app.
- `/health` returns a `200` JSON response.
- Search API tests pass.

## Pytest commands and expected results
```bash
pytest -k "api_health or api_search" -v
pytest -q
```

Expected result: the API validates request data, returns predictable JSON, maps common failures to useful HTTP responses, and passes integration tests.

## Completion checklist
- [ ] FastAPI app object exists.
- [ ] Health route exists.
- [ ] Search or document route exists.
- [ ] Pydantic schemas are defined.
- [ ] Dependency providers are defined.
- [ ] Error mapping is intentional.
- [ ] API tests pass.
- [ ] Uvicorn can serve the app locally.
- [ ] `pytest -q` passes.
- [ ] You can describe the request-to-service flow.
