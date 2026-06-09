# Break It - Week 01 Foundations

## Intentional failure experiments
1. Remove `src` from the pytest python path and run tests. Observe the import error and restore the setting.
2. Rename `researchops/cli/main.py` to a different filename without updating `pyproject.toml`. Run `researchops --help` and inspect the failure.
3. Create a circular import between `utils.py` and `config.py`. Read the traceback and then move shared code into one place.
4. Return `None` from a function that tests expect to return a string. Watch the assertion fail.
5. Misspell the package name in one import statement and identify how Python reports `ModuleNotFoundError`.

## Debugging tasks
- Use `python -c "import researchops"` to isolate package import issues.
- Use `pytest -k cli -v` to narrow the failing test set.
- Compare a broken import path with the actual directory structure.

## Edge cases to explore
- What happens when a utility function receives an empty list?
- What happens if the CLI command has no subcommands yet?
- What happens when two modules define the same function name?

## What did you learn?
- Which failure was easiest to diagnose?
- Which traceback line actually mattered most?
- What project structure rule will you follow from now on?
