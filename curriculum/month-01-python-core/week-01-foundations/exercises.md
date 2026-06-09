# Exercises - Week 01 Foundations

## Warm-up exercises
1. Write a function `slugify_title(title: str) -> str` that lowercases a title and replaces spaces with hyphens.
2. Given a list of paper titles, return the number of unique titles.
3. Build a dictionary for one paper with keys `title`, `authors`, and `year`.
4. Import a helper function from another module and print its return value.

## Project exercises
1. Create `src/researchops/cli/main.py` with a Typer app that has a `scan` command.
2. Add `src/researchops/utils/paths.py` with a `find_pdfs(directory, recursive)` helper and unit tests in `tests/unit/test_paths.py`.
3. Confirm `pyproject.toml` has the `researchops = "researchops.cli.main:app"` entry point and that `researchops --help` resolves.
4. Create `tests/e2e/test_cli.py` and add a test that invokes `scan` on a temporary directory using Typer's `CliRunner`.

## Stretch exercises
1. Add a `version` command to `cli/main.py` that reads the package version from `importlib.metadata` without hard-coding it.
2. Add `src/researchops/utils/paths.py` helpers: `ensure_dir(path)` that creates a directory and its parents, and `safe_resolve(path)` that returns an absolute path without raising on symlink loops.
3. Refactor any function longer than 10 lines into smaller helpers.

## Writing questions
1. What felt different about working inside a virtual environment?
2. Which Python collection type still feels fuzzy, and why?
3. Where did imports confuse you this week?
4. What did tests teach you about your function design?
