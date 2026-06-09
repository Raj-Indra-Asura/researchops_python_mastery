# Week 01 - Foundations

## Learning objectives
- Set up a Python 3.11 virtual environment and install the project in editable mode.
- Read `pyproject.toml` and understand how package metadata and dependencies are declared.
- Organize code into `src/`, `tests/`, and package modules with clear imports.
- Write small, focused functions that accept inputs and return values.
- Use lists, dictionaries, sets, tuples, and loops to model simple research data.
- Import from modules without circular dependencies.
- Run a first CLI placeholder and verify that the package entry point resolves.

## Project milestone
Create the initial ResearchOps skeleton: package layout, a tiny CLI placeholder, and basic utility functions that prove the repo can be installed and executed.

## Files to modify/create
- `pyproject.toml`
- `src/researchops/__init__.py`
- `src/researchops/cli/main.py`
- `src/researchops/config.py`
- `src/researchops/utils.py`
- `tests/unit/test_cli.py`
- `tests/unit/test_utils.py`

## Concepts covered
Functions, variables, collections, modules, imports, `__init__.py`, editable installs, virtual environments, command entry points, and repository layout.

## Expected deliverables
- A working `.venv` for local development.
- A `researchops` package importable from Python.
- A placeholder CLI command that prints a friendly status message.
- At least two small utility functions with unit tests.
- A short setup note in the repo README if needed.

## Definition of done
- [ ] Python 3.11 environment created.
- [ ] `pip install -e ".[dev]"` succeeds.
- [ ] `python -c "import researchops"` succeeds.
- [ ] `researchops --help` shows a CLI.
- [ ] Package code lives under `src/researchops`.
- [ ] Imports are absolute and readable.
- [ ] Functions are small and named clearly.
- [ ] Tests for CLI and utility helpers exist.
- [ ] `pytest` passes locally.
- [ ] Notes capture what you found confusing.
