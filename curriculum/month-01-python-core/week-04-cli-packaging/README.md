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
- `src/researchops/cli/scan.py`
- `src/researchops/scanner.py`
- `pyproject.toml`
- `tests/unit/test_cli_scan.py`
- `tests/e2e/test_scan_command.py`

## Concepts covered
Typer commands, options and arguments, entry points, package installation, exit codes, user-facing errors, and command structure.

## Expected deliverables
- `researchops --help` shows organized commands.
- `researchops scan <path>` scans a directory and prints a summary.
- CLI tests cover help, success, and failure flows.
- Packaging metadata still installs cleanly.

## Definition of done
- [ ] `scan` command exists.
- [ ] Help text is readable.
- [ ] CLI arguments are typed.
- [ ] Missing-path failures produce a helpful message.
- [ ] Exit codes are meaningful.
- [ ] End-to-end command test exists.
- [ ] Editable install still works.
- [ ] Manual run against sample data succeeds.
- [ ] README or command help explains usage.
