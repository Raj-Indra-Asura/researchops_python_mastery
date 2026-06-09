# Validation - Week 02 Files, Errors, and Logging

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest tests/unit/test_files.py -v
pytest tests/unit/test_scanner.py -v
pytest tests/unit/test_logging_config.py -v
python -m researchops.cli.main info
```

## Expected outputs
- File and scanner tests pass.
- Logging tests confirm the expected level or message behavior.
- Manual scanner run prints counts or status lines without crashing.

## Pytest commands and expected results
```bash
pytest -k "files or scanner or logging" -v
pytest -q
```

Expected result: missing paths are handled intentionally, unsupported files are skipped predictably, and logs appear at the configured level.

## Completion checklist
- [ ] `Path` replaces string path joins.
- [ ] Missing directory behavior is tested.
- [ ] Non-directory input behavior is tested.
- [ ] Nested directory scanning works.
- [ ] Unsupported extensions are skipped.
- [ ] Uppercase extension behavior is defined.
- [ ] Logging setup is centralized.
- [ ] INFO and ERROR messages are visible when appropriate.
- [ ] Exceptions contain path context.
- [ ] Unit tests pass.
- [ ] You can explain why broad exception handling is risky.
- [ ] You can manually scan a sample folder.
