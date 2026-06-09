# Validation - Week 05 SQLite Storage Layer

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest tests/unit/test_sqlite_repository.py -v
pytest tests/integration/test_storage_roundtrip.py -v
pytest -k storage -v
```

## Expected outputs
- Schema initialization tests pass.
- Repository unit tests pass.
- Integration test proves rows round-trip from models to SQLite and back.

## Pytest commands and expected results
```bash
pytest tests/integration/test_storage_roundtrip.py -v
pytest -q
```

Expected result: inserts are committed only on success, duplicate or invalid writes fail predictably, and repository methods return the correct domain data.

## Completion checklist
- [ ] Database initialization function exists.
- [ ] Tables and constraints are defined.
- [ ] Repository object encapsulates SQL.
- [ ] Insert path is transactional.
- [ ] Read path maps rows to models.
- [ ] Duplicate source-path behavior is tested.
- [ ] Rollback behavior is tested.
- [ ] Integration round trip passes.
- [ ] SQL uses parameters, not string interpolation.
- [ ] `pytest -q` passes.
- [ ] You can explain the repository pattern in one paragraph.
