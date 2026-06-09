# Exercises - Week 01 Foundations

## Warm-up exercises
1. Write a function `slugify_title(title: str) -> str` that lowercases a title and replaces spaces with hyphens.
2. Given a list of paper titles, return the number of unique titles.
3. Build a dictionary for one paper with keys `title`, `authors`, and `year`.
4. Import a helper function from another module and print its return value.

## Project exercises
1. Create `src/researchops/cli/main.py` with a Typer app that has an `info` command.
2. Add a utility module with two pure functions and unit tests.
3. Add package metadata in `pyproject.toml` and confirm the `researchops` script resolves.
4. Create an empty `tests/unit` package structure and add your first passing tests.

## Stretch exercises
1. Add a `version` command that reads the package version without hard-coding it twice.
2. Create a module that returns standard project paths such as `data/`, `logs/`, and `artifacts/`.
3. Refactor any function longer than 10 lines into smaller helpers.

## Writing questions
1. What felt different about working inside a virtual environment?
2. Which Python collection type still feels fuzzy, and why?
3. Where did imports confuse you this week?
4. What did tests teach you about your function design?
