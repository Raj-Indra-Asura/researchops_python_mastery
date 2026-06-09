# Break It - Week 04 CLI and Packaging

## Intentional failure experiments
1. Change the entry point in `pyproject.toml` to a wrong module path and run `researchops --help`.
2. Remove the path argument type hint and notice how validation changes.
3. Raise a raw exception from the command and compare the traceback with a clean `typer.Exit` flow.
4. Pass a missing directory to `researchops scan` and verify the message is human-friendly.
5. Add a command with the same name twice and inspect how Typer handles it.

## Debugging tasks
- Reinstall the package with `python -m pip install -e .` after entry point changes.
- Use `pytest -k scan_command -v` to focus on command tests.
- Print the resolved `Path` value during one manual run.

## Edge cases to explore
- Paths containing spaces.
- Empty directories.
- Relative versus absolute paths.
- `--help` on both the root app and a subcommand.

## What did you learn?
- Which CLI failure felt like packaging rather than code?
- What output would help a new user most?
- How will you keep commands small as the tool grows?
