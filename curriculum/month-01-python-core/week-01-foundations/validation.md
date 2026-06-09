# Validation - Week 01 Foundations

## Exact shell commands to run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -c "import researchops; print('import ok')"
researchops --help
pytest tests/unit -v
```

## Expected outputs
- `pip install -e ".[dev]"` finishes without dependency errors.
- `python -c ...` prints `import ok`.
- `researchops --help` shows Typer help text and at least one command.
- `pytest tests/unit -v` reports passing tests.

## Pytest commands and expected results
```bash
pytest tests/unit/test_cli.py -v
pytest tests/unit/test_utils.py -v
pytest -q
```

Expected result: all current week 1 tests pass, no import errors, and no unexpected collection failures.

## Completion checklist
- [ ] `.venv` exists.
- [ ] Editable install succeeds.
- [ ] `pyproject.toml` has project metadata.
- [ ] CLI entry point is declared.
- [ ] `src/researchops/__init__.py` exists.
- [ ] `src/researchops/cli/main.py` exists.
- [ ] At least one command prints output.
- [ ] Utility functions are pure where possible.
- [ ] Unit tests cover utilities.
- [ ] Unit tests cover CLI help or command output.
- [ ] `pytest -q` passes.
- [ ] You can explain why the repo uses `src/` layout.
