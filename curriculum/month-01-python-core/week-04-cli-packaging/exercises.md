# Exercises - Week 04 CLI and Packaging

## Warm-up exercises
1. Write a Typer command that echoes a provided name.
2. Add a boolean `--verbose` option to a command.
3. Return exit code 1 when a `Path` does not exist.
4. Run `researchops --help` and describe what information is shown.

## Project exercises
1. Implement `researchops scan <path>` using your scanner from week 2.
2. Add rich help text for the `scan` command argument and options.
3. Write tests for success, missing-path failure, and help output.
4. Refactor command logic so scanning work is not embedded directly in `main.py`.

## Stretch exercises
1. Add a `--json` flag for machine-readable output.
2. Add a shared formatter for CLI summary tables.
3. Add shell-friendly exit codes for partial success versus total failure.

## Writing questions
1. What makes CLI output easy to trust?
2. Which command-line argument pattern still confuses you?
3. Why should CLI code stay thin?
4. What broke when packaging and code disagreed?
