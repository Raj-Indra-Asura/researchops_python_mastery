# Validation - Week 10 Testing Discipline and Quality Gates

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,parsing,storage]"
ruff check src tests
mypy src
pytest --cov=src/researchops --cov-report=term-missing
```

## Expected outputs
- Ruff reports no errors.
- MyPy reports success with no unexpected type errors.
- Pytest passes and prints coverage information at or above the configured threshold.
- CI workflow mirrors the same core commands.

## Pytest commands and expected results
```bash
pytest tests/unit -v
pytest tests/integration -v
pytest tests/e2e -v
pytest -q
```

Expected result: the suite passes at all scopes, coverage stays above the threshold, and CI can enforce the same gates automatically.

## Completion checklist
- [ ] Shared fixtures exist.
- [ ] Parametrized test exists.
- [ ] `monkeypatch` is used in at least one meaningful test.
- [ ] Coverage command runs successfully.
- [ ] Coverage threshold is configured.
- [ ] CI workflow file exists.
- [ ] CI runs lint, type, and tests.
- [ ] Test directories reflect scope.
- [ ] Flaky behavior is investigated or eliminated.
- [ ] `pytest -q` passes.
- [ ] You can explain what each gate protects.
