# Exercises - Week 10 Testing Discipline and Quality Gates

## Warm-up exercises
1. Write a fixture that returns a temporary SQLite path.
2. Parametrize a normalization test across three inputs.
3. Use `monkeypatch` to fake one function failure.
4. Run coverage and note which module has missing lines.

## Project exercises
1. Add shared fixtures in `tests/conftest.py`.
2. Write a unit test that uses a fake repository and monkeypatch.
3. Configure CI to run lint, type checks, and pytest.
4. Enforce or verify a coverage threshold in project config.

## Stretch exercises
1. Split slow integration tests with markers.
2. Add a smoke e2e test for the installed CLI.
3. Make CI upload coverage output or artifacts.

## Writing questions
1. Which check catches your mistakes earliest?
2. When is monkeypatching helpful versus dangerous?
3. What part of your suite is still under-tested?
4. How should CI failures influence your workflow?
