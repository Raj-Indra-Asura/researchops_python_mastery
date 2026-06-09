# Break It - Week 10 Testing Discipline and Quality Gates

## Intentional failure experiments
1. Delete one fixture import or rename it and watch multiple tests fail.
2. Lower the coverage by removing a test and inspect the threshold failure.
3. Break the CI workflow command name and see how quickly automation fails.
4. Monkeypatch the wrong symbol path and note why the test still uses the real function.
5. Introduce a lint error and confirm the gate blocks it.

## Debugging tasks
- Run a single failing test with `-vv` and `-s`.
- Use `pytest --maxfail=1` to focus on the first failure.
- Compare local test output with the CI workflow commands.

## Edge cases to explore
- Flaky tests that depend on order.
- Slow tests mixed into unit scope.
- Environment-dependent paths or variables.
- Hidden network calls in tests.

## What did you learn?
- Which gate gives the highest value per minute?
- What made one test brittle?
- How will you keep the suite fast enough to trust daily?
