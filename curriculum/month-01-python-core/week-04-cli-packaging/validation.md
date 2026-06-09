# Validation - Week 04 CLI and Packaging

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
researchops --help
researchops scan examples/sample_papers
pytest tests/unit/test_cli_scan.py -v
pytest tests/e2e/test_scan_command.py -v
```

## Expected outputs
- Root help shows the app description and commands.
- `researchops scan examples/sample_papers` prints a scan summary.
- CLI tests and e2e tests pass.

## Pytest commands and expected results
```bash
pytest -k "cli_scan or scan_command" -v
pytest -q
```

Expected result: the package installs, the shell entry point resolves, the scan command works on sample input, and command failures return useful exit codes.

## Completion checklist
- [ ] `scan` command is registered.
- [ ] Entry point in `pyproject.toml` is correct.
- [ ] Help text is readable.
- [ ] Missing-path case returns a non-zero exit code.
- [ ] Success case prints counts.
- [ ] CLI tests assert on output.
- [ ] E2E test invokes the installed command path.
- [ ] Editable install still succeeds.
- [ ] Manual command run works from repo root.
- [ ] `pytest -q` passes.
- [ ] You can explain how the entry point maps to Python code.
