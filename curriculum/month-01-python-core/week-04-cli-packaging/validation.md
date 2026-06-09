# Validation - Week 04 CLI and Packaging

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
researchops --help
researchops scan examples/sample_papers
researchops scan examples/sample_papers --recursive
researchops scan /tmp/does_not_exist
pytest tests/e2e/test_cli.py -v
pytest -q
```

## Expected outputs
- Root help shows the app description and sub-commands including `scan`.
- `researchops scan examples/sample_papers` prints a list of found PDFs (or "No PDF files found" if the directory is empty).
- `researchops scan /tmp/does_not_exist` exits with a non-zero code and a human-readable error.
- All CLI tests in `tests/e2e/test_cli.py` pass.

## Pytest commands and expected results
```bash
pytest tests/e2e/test_cli.py -v
pytest -q
```

Expected result: package installs cleanly, shell entry point resolves, `scan` handles success and failure flows, and all tests pass.

## Completion checklist
- [ ] `scan` command is in `cli/main.py`.
- [ ] Entry point in `pyproject.toml` is `"researchops.cli.main:app"`.
- [ ] `scan` calls `find_pdfs()` from `utils/paths.py` — no scanning logic embedded in the handler.
- [ ] Help text for the `directory` argument is descriptive.
- [ ] Missing-path case returns exit code 1 with a human-readable message.
- [ ] Success case prints PDF names and count.
- [ ] `--recursive` flag is wired through to `find_pdfs(recursive=True)`.
- [ ] `tests/e2e/test_cli.py` tests help, success, and failure.
- [ ] Editable install succeeds after any `pyproject.toml` changes.
- [ ] `pytest -q` passes.
- [ ] You can explain how the entry point maps to Python code.
