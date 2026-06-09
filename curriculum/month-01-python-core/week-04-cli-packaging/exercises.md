# Exercises - Week 04 CLI and Packaging

## Warm-up exercises
1. Run `researchops --help` and describe every section of the output.
2. Run `researchops scan --help` and confirm the `--recursive` flag is listed.
3. Return exit code 1 from a command by raising `typer.Exit(code=1)` and verify `result.exit_code` in a test.
4. Add a `--count-only` boolean option to the `scan` command that prints only the integer count instead of the full table.

## Project exercises
1. Read `src/researchops/cli/main.py` end-to-end. Trace how the `scan` command calls `find_pdfs()` and converts the result to a Rich table.
2. Read `tests/e2e/test_cli.py` end-to-end. Add two new test cases: one that calls `researchops scan` with a path that is a file (not a directory), and one that calls `researchops scan --recursive` and confirms a nested PDF appears in the output.
3. Break the entry point in `pyproject.toml` by changing `"researchops.cli.main:app"` to `"researchops.cli.main:typer_app"`, reinstall with `pip install -e .`, and run `researchops --help`. Read the error, then restore the entry point.
4. Add a `researchops version` command to `cli/main.py` that prints the package version using `importlib.metadata.version("researchops")`. Write a test for it in `tests/e2e/test_cli.py`.

## Stretch exercises
1. Add a `--json` flag to `scan` that prints results as a JSON array of file paths instead of a Rich table. Use `utils/serialization.py`'s `to_json()`.
2. Add a `researchops stats` placeholder command (returns a "not implemented yet" message) to `cli/commands/papers.py`, register it in `cli/main.py`, and write a test.
3. Add shell-friendly exit codes: 0 for "found PDFs", 0 for "no PDFs found", and 1 for "invalid path". Confirm each case in a test.

## Writing questions
1. What makes CLI output easy to trust?
2. Which command-line argument pattern still confuses you?
3. Why should CLI code stay thin?
4. What broke when packaging and code disagreed?
