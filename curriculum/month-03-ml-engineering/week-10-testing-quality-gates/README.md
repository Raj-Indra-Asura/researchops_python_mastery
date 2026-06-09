# Week 10 — Testing Discipline and Quality Gates

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › **Week 10 — Testing & Quality Gates**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 10 — Testing & Quality Gates** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 9 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 11](../../../curriculum/month-03-ml-engineering/week-11-classical-ml-topic-classification/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 11 — Classical ML: Topic Classification](../../../curriculum/month-03-ml-engineering/week-11-classical-ml-topic-classification/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 10 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
