# Week 04 - CLI and Packaging

## Learning objectives
- Build a Typer CLI with subcommands and typed arguments.
- Understand package entry points and how shell commands are installed.
- Organize CLI code so command handlers stay small.
- Parse options such as input paths, flags, and default values.
- Return non-zero exit codes for user-facing failures.
- Update `pyproject.toml` responsibly as the package grows.
- Ship a `researchops scan` command backed by earlier scanner logic.

## Project milestone
Turn the package skeleton into a usable command-line application with a real `researchops scan` command and clear help output.

## Files to modify/create
- `src/researchops/cli/main.py`
- `src/researchops/cli/commands/__init__.py`
- `src/researchops/utils/paths.py`
- `pyproject.toml`
- `tests/e2e/test_cli.py`

## Concepts covered
Typer commands, options and arguments, entry points, package installation, exit codes, user-facing errors, and command structure.

## Expected deliverables
- `researchops --help` shows the app description and sub-commands.
- `researchops scan <path>` lists PDFs and prints a count.
- `researchops scan <path> --recursive` descends into sub-directories.
- CLI tests cover help, success, missing-path failure, and recursive flag.
- Packaging metadata still installs cleanly after any `pyproject.toml` edits.

## Definition of done
- [ ] `scan` command exists in `cli/main.py`.
- [ ] Help text is readable and describes the argument.
- [ ] CLI argument is typed as `str` (converted to `Path` inside the handler).
- [ ] Missing-path failure produces a human-friendly message and exit code 1.
- [ ] Exit codes are meaningful (0 for success, 1 for user error).
- [ ] `tests/e2e/test_cli.py` covers help, success, and failure flows.
- [ ] Editable install still works after any `pyproject.toml` changes.
- [ ] Manual run against `examples/sample_papers` succeeds.
- [ ] `pytest -q` passes.
