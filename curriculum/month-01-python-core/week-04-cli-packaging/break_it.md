# Break It - Week 04 CLI and Packaging

## Intentional failure experiments
1. Change the entry point in `pyproject.toml` to a wrong module path (`"researchops.cli.broken:app"`) and run `pip install -e . && researchops --help`. Read the error, then restore the entry point.
2. Remove the `recursive` parameter from the `scan` command signature and run `researchops scan examples/sample_papers --recursive`. Confirm Typer rejects the unknown option with a clear error.
3. Raise a raw `RuntimeError` inside the `scan` command (instead of a clean `typer.Exit`) and compare the output a user sees — then see why converting domain exceptions to exit codes matters.
4. Pass a path with spaces to `researchops scan` (e.g. `researchops scan "/tmp/my papers"`) and confirm it works without quoting issues.
5. Add a command with the same name twice to the Typer app (e.g. two `@app.command()` functions both named `scan`) and read how Typer handles the conflict.

## Debugging tasks
- Reinstall the package with `pip install -e .` after entry point changes.
- Use `pytest tests/e2e/test_cli.py -v -k scan` to focus on scan-related tests.
- Print `str(path)` inside the command handler during one manual run to confirm the `Path` resolves as expected.

## Edge cases to explore
- Paths containing spaces.
- Empty directories — confirm exit code is 0, not 1.
- Relative paths like `./examples/sample_papers` versus absolute paths.
- `--help` on both the root app (`researchops --help`) and the sub-command (`researchops scan --help`).

## What did you learn?
- Which CLI failure felt like packaging rather than code?
- What output would help a new user most?
- How will you keep commands small as the tool grows?
