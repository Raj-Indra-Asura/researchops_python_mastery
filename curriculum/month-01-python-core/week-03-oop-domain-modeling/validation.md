# Validation - Week 03 OOP and Domain Modeling

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest tests/unit/test_models.py -v
pytest tests/unit/test_value_objects.py -v
pytest -k model -v
```

## Expected outputs
- Model tests pass including `word_count`, `is_empty`, `success_rate`, `summary`, and aggregation tests.
- Value object tests confirm `Query` rejects empty input and `Tag` normalises to lowercase-with-hyphens.
- Any new methods you added (`display_summary`, `slug`, `to_dict`) are tested and pass.

## Pytest commands and expected results
```bash
pytest tests/unit/test_models.py -v
pytest tests/unit/test_value_objects.py -v
pytest -q
```

Expected result: the core layer has typed, tested objects and all week 3 tests pass with no loose dictionaries in core code paths.

## Completion checklist
- [ ] `Paper` dataclass is defined in `core/models.py`.
- [ ] `ParsedDocument` dataclass is defined in `core/models.py`.
- [ ] `FailedDocument` dataclass is defined in `core/models.py`.
- [ ] `IngestionResult` dataclass is defined in `core/models.py`.
- [ ] `PaperId.from_path()` is defined in `core/models.py`.
- [ ] `IngestionStatus` enum is defined in `core/models.py`.
- [ ] Mutable list fields use `field(default_factory=list)`.
- [ ] `Query` and `Tag` value objects are in `core/value_objects.py`.
- [ ] `tests/unit/test_models.py` covers methods and properties.
- [ ] `tests/unit/test_value_objects.py` covers invariants.
- [ ] `tests/fakes/fake_repository.py` implements the repository protocols.
- [ ] `pytest -q` passes.
- [ ] You can explain why `core/` must not import from `storage/` or `cli/`.
