# Validation - Week 03 OOP and Domain Modeling

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest tests/unit/test_models.py -v
pytest tests/unit/test_ingestion_result.py -v
pytest -k model -v
```

## Expected outputs
- Model tests pass.
- Invalid object construction raises expected exceptions.
- Success and failure aggregation behaves predictably.

## Pytest commands and expected results
```bash
pytest tests/unit/test_models.py -v
pytest tests/unit/test_ingestion_result.py -v
pytest -q
```

Expected result: your model layer has clear, typed objects and all week 3 tests pass without relying on loose dictionaries.

## Completion checklist
- [ ] Dataclasses are defined for all core entities.
- [ ] Field names use domain language.
- [ ] Mutable defaults use `default_factory`.
- [ ] At least one invariant is enforced.
- [ ] `Paper` tests exist.
- [ ] `ParsedDocument` tests exist.
- [ ] `FailedDocument` tests exist.
- [ ] `IngestionResult` aggregation is tested.
- [ ] Factory helpers reduce test duplication.
- [ ] `pytest -q` passes.
- [ ] You can explain why separate success and failure models help.
