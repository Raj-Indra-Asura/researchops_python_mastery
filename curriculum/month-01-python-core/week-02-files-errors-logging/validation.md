# Validation - Week 02 Files, Errors, and Logging

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest tests/unit/test_paths.py -v
pytest tests/unit/test_exceptions.py -v
researchops scan examples/sample_papers
researchops --verbose scan examples/sample_papers
```

## Expected outputs
- Path tests pass, including missing-path and non-directory cases.
- Exception tests confirm sub-class hierarchy and message content.
- Manual scan command prints found PDFs (or "No PDF files found") without crashing.
- `--verbose` causes DEBUG log lines to appear.

## Pytest commands and expected results
```bash
pytest -k "paths or exceptions" -v
pytest -q
```

Expected result: missing paths raise `NotADirectoryError`, exceptions carry path context, and logs appear at the configured level.

## Completion checklist
- [ ] `Path` replaces string path joins throughout.
- [ ] `find_pdfs()` handles missing directory: raises `NotADirectoryError`.
- [ ] `find_pdfs()` handles file-instead-of-directory: raises `NotADirectoryError`.
- [ ] `find_pdfs()` handles empty directory: returns `[]`.
- [ ] `find_pdfs(recursive=True)` finds nested PDFs.
- [ ] Uppercase extension handling is understood (`.PDF` vs `.pdf` — test it).
- [ ] Logging is configured via `configure_logging()` from `config/logging.py`.
- [ ] `get_logger(__name__)` is used in every module that emits log lines.
- [ ] INFO and ERROR messages are visible when appropriate.
- [ ] Custom exceptions in `core/exceptions.py` carry path context.
- [ ] Unit tests pass.
- [ ] You can explain why broad exception handling is risky.
- [ ] You can manually scan `examples/sample_papers` and read the output.
