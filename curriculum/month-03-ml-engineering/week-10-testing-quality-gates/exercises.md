# Exercises - Week 10 Testing Discipline and Quality Gates

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 10 — Testing & Quality Gates](./README.md) › **exercises.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Warm-up: pytest mechanics

**Exercise W10-1: Write your first fixture chain**

Write three fixtures: `empty_paper_repo`, `paper_repo_with_one_paper` (depends on `empty_paper_repo` and adds one paper), and `paper_repo_with_three_papers` (adds three more). Write a test that uses each fixture. Verify that adding a paper in one fixture does not affect the others (function scope).

**Exercise W10-2: Parametrize a normalisation test**

Write a parametrized test for `normalise_for_search` covering at least six cases:
- Mixed case input.
- Leading and trailing whitespace.
- Multiple spaces between words.
- Empty string.
- Already normalised string.
- String with hyphens and numbers.

The test should run six separate cases and fail independently if one is wrong.

**Exercise W10-3: Write a regression test**

Find a function in `researchops` that has no test covering its edge cases. Write at least one test that covers an edge case you discovered. Name it with the pattern `test_<function>_handles_<condition>`.

**Exercise W10-4: Use tmp_path for a file test**

Write a test that:
1. Creates a file in `tmp_path`.
2. Calls a function that reads from that file.
3. Asserts on the result.
4. Does NOT manually clean up — let pytest handle it.

---

## Project exercises: ResearchOps codebase

**Exercise W10-5: Read test_ingestion_service.py completely**

Open `tests/unit/test_ingestion_service.py`. For every test, write:
- Which behavior it is testing.
- Which fixture it depends on.
- What the Arrange, Act, and Assert phases are.

Do this in a scratch file or notebook. After doing it, can you find any behavior that is NOT tested?

**Exercise W10-6: Write tests for KeywordSearchService**

The file `tests/unit/test_search_service.py` already exists. Open it and check if these behaviors are covered:

- Empty query raises `EmptyQueryError`.
- Query that matches no papers returns empty list.
- Query that matches one paper returns one result.
- Query that matches multiple papers returns results in descending score order.
- Limit parameter restricts the number of results.
- Query matching text in the body is found even if not in the title.

Write tests for any behaviors that are missing. Use `FakePaperRepository`.

**Exercise W10-7: Write an integration test for SQLiteRepository**

Open `tests/integration/test_sqlite_repository.py`. Add a test that:

1. Creates a real SQLite database with `tmp_path`.
2. Saves three papers.
3. Deletes one paper.
4. Calls `list_all()` and verifies only two papers remain.
5. Calls `exists()` on the deleted paper ID and verifies it returns `False`.

This test should use real SQLite, not a fake.

**Exercise W10-8: Run and interpret coverage**

Run:

```bash
pytest --cov=researchops --cov-report=term-missing -q
```

Find three modules with less than 100% coverage. For each, look at the missing lines. Write one sentence explaining why each line might be uncovered. Then write one test that covers one of those lines.

**Exercise W10-9: Explore the CI pipeline**

Open `.github/workflows/ci.yml`. Answer:

1. What Python version does CI use?
2. What are the exact commands CI runs?
3. What would happen if coverage dropped to 40%?
4. What would happen if you introduced a syntax error that `ruff` catches?
5. Can you reproduce every CI check locally? Run them all and verify they pass.

---

## monkeypatch exercises

**Exercise W10-10: Patch a failure path**

`IngestionService._ingest_one` has two failure paths: `ParsingError` and unexpected `Exception`. The `ParsingError` path is tested. Write a test that patches the parser to raise `RuntimeError` and verify that the failure is recorded in `FakeFailureRepository` with the error type `"RuntimeError"`.

**Exercise W10-11: Patch an environment variable**

If your `Settings` class reads a path from an environment variable (look in `src/researchops/config/settings.py`), write a test that uses `monkeypatch.setenv` to override that variable and verify the setting is read correctly.

**Exercise W10-12: When monkeypatch is wrong**

Write a test that uses monkeypatch to fake `FakePaperRepository.save`. Now rewrite the same test using `FakePaperRepository` directly without monkeypatching. Which test is easier to read? Which is more fragile if you rename a method? Write a one-paragraph explanation of your conclusion.

---

## Stretch exercises

**Exercise W10-S1: Add pytest markers for slow tests**

Add a custom pytest marker `@pytest.mark.slow` to any test that takes more than 100ms. Configure `pyproject.toml` so that `pytest -m "not slow"` skips those tests. This lets you run a fast subset locally while CI runs all tests.

**Exercise W10-S2: Write a smoke E2E test**

Write an E2E test in `tests/e2e/test_cli.py` that:
1. Calls the real installed CLI with `subprocess.run`.
2. Verifies the `--help` flag exits with code 0.
3. Verifies the `version` or `--version` flag prints a version string.

This does not need to test full ingestion — just that the CLI is installed and responds.

**Exercise W10-S3: Add conftest.py shared fixtures**

Identify fixtures that appear in more than one test file. Move them to `tests/conftest.py`. Verify that the tests still pass. Count how many lines of duplication you removed.

---

## Written reflection questions

1. You have a test suite with 200 unit tests and 5 integration tests. Your colleague says "we should have more integration tests." How do you respond?

2. A test has been failing randomly in CI for two weeks. Nobody has time to investigate. What are the dangers of keeping it around? What would you do?

3. Coverage is 85%. You just added a complex function with 10 branches and zero tests. Coverage is now 75%. The CI fails. What is the right response — lower the threshold or add tests?

4. Your `test_ingestion_skips_existing_paper` test has 30 lines. Can it be broken into smaller tests? Try it.

5. A test named `test_case_7` is failing. Without looking at the test body, what can you say about the quality of this test? Rename it to a behavior-based name.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 10 — Testing & Quality Gates** · *exercises.md — the workbook* (step 3 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [notes.md](./notes.md)
- ▶ **Next:** [break_it.md](./break_it.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. **➡ [exercises.md](./exercises.md) ← you are here**
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
