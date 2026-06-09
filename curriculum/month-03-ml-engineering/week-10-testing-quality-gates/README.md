<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 10 — Testing and Quality Gates:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 9 Reflection](../week-09-protocols-clean-architecture/reflection.md) · ➡️ [Notes →](notes.md)

---
<!-- NAV_END -->

# Week 10 — Testing Discipline and Quality Gates

## Theme

You now have clean architecture. This week you build the safety net that protects it. Testing discipline means having a suite you can trust — fast, isolated, reliable — and quality gates that enforce it automatically.

## Learning objectives

By the end of this week you will be able to:

- Explain the test pyramid and why unit tests should be the most numerous.
- Write pytest fixtures, parametrized tests, and monkeypatched tests.
- Use `tmp_path` for tests that need files or databases.
- Run coverage reports and interpret the output.
- Explain what a regression test is and how to write one.
- Identify and eliminate flaky tests.
- Configure and run the full quality gate: ruff + pytest + coverage.
- Read `.github/workflows/ci.yml` and understand each step.
- Follow the Arrange / Act / Assert pattern in every test.
- Name tests after behaviors, not implementations.

## Project milestone

Build a test suite you can trust. Ensure the CI pipeline runs ruff, pytest, and coverage. Write at least five new tests that cover previously untested behavior.

## Key source files to study

| File | What it teaches |
|---|---|
| `tests/unit/test_ingestion_service.py` | Full example of a fixture-based unit test suite |
| `tests/fakes/fake_repository.py` | Fakes used in unit tests |
| `tests/integration/test_sqlite_repository.py` | Integration tests using real SQLite |
| `tests/e2e/test_cli.py` | End-to-end test using the real CLI |
| `pyproject.toml` | Coverage configuration, ruff rules, pytest settings |
| `.github/workflows/ci.yml` | The CI pipeline that runs on every push |

## Concepts covered

Unit test, integration test, E2E test, test pyramid, fixture, scope, parametrize, monkeypatch, tmp_path, temporary database, coverage, threshold, CI, linting, type checking, quality gates, Arrange/Act/Assert, regression test, flaky test, test naming, conftest.py.

## Expected deliverables

- A `tests/conftest.py` with at least two shared fixtures.
- At least two parametrized tests.
- At least one test using monkeypatch.
- A coverage report showing overall project coverage.
- A written explanation of what each CI step protects.

## Definition of done

- [ ] You understand the test pyramid and can place each test file in the right layer.
- [ ] You can write a fixture from scratch in under 2 minutes.
- [ ] You can write a parametrized test across at least three inputs.
- [ ] You can explain when to use monkeypatch versus a fake.
- [ ] `pytest --cov=researchops --cov-report=term-missing -q` runs without errors.
- [ ] Coverage is at or above the configured threshold.
- [ ] `ruff check src tests` exits clean.
- [ ] You can read the CI workflow file and explain each step.
- [ ] You have written at least one regression test for a real bug or edge case.
- [ ] You can explain what a flaky test is and give one example of a cause.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 9 Reflection](../week-09-protocols-clean-architecture/reflection.md) · ➡️ [Notes →](notes.md)

**Week 10 — Testing and Quality Gates:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
