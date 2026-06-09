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
pytest tests/unit/test_paths.py -v
pytest tests/e2e/test_cli.py -v
pytest -q
```

Expected result: all current week 1 tests pass, no import errors, and no unexpected collection failures.

## Completion checklist
- [ ] `.venv` exists.
- [ ] Editable install succeeds.
- [ ] `pyproject.toml` has project metadata.
- [ ] CLI entry point (`researchops = "researchops.cli.main:app"`) is declared.
- [ ] `src/researchops/__init__.py` exists.
- [ ] `src/researchops/cli/main.py` exists with the Typer app.
- [ ] `src/researchops/utils/paths.py` exists with `find_pdfs()`.
- [ ] `src/researchops/config/settings.py` exists with `Settings` and the `settings` singleton.
- [ ] At least one CLI command prints output.
- [ ] `find_pdfs()` raises `NotADirectoryError` for missing or non-directory paths.
- [ ] Unit tests cover `find_pdfs()` in `tests/unit/test_paths.py`.
- [ ] E2E tests cover `scan` command in `tests/e2e/test_cli.py`.
- [ ] `pytest -q` passes.
- [ ] You can explain why the repo uses `src/` layout.
