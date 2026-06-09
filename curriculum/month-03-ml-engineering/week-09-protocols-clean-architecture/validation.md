# Validation - Week 09 Protocols and Clean Architecture

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,parsing,storage]"
pytest tests/unit/test_service_with_fake_repo.py -v
pytest tests/integration/test_ingest_pipeline.py -v
pytest -k "fake_repo or service" -v
```

## Expected outputs
- Unit tests using fakes pass quickly.
- Existing integration tests still pass with real adapters.
- No service layer requires a concrete SQLite type in its signature.

## Pytest commands and expected results
```bash
pytest tests/unit -v
pytest tests/integration -v
pytest -q
```

Expected result: services operate correctly against both fake and real implementations, showing that the abstractions are meaningful and not only theoretical.

## Completion checklist
- [ ] Protocols are defined for key dependencies.
- [ ] Services depend on protocols.
- [ ] Fake repository exists.
- [ ] At least one service test uses the fake.
- [ ] Infrastructure imports are pushed outward.
- [ ] Integration tests still pass.
- [ ] Constructor injection is used clearly.
- [ ] You can name the domain, application, and infrastructure layers.
- [ ] `pytest -q` passes.
- [ ] You can explain ports and adapters with your code.
