<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 10 — Testing and Quality Gates:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 10 Testing Discipline and Quality Gates

## 1. Chapter overview
- This chapter turns ResearchOps from code that can be manually checked into code that can defend itself against regressions.
- By Week 10 the system has domain models, parsing, SQLite storage, keyword search, service boundaries, CLI wiring, and protocol-based architecture.
- That is too much behavior to verify by clicking around or rerunning one happy-path command from memory.
- The professional habit is to make every important promise executable as a test.
- The professional gate is to make the important checks run before a change is considered acceptable.
- The exact lint gate for this week is `ruff check src tests`.
- The exact test and coverage gate for this week is `pytest --cov=researchops --cov-report=term-missing -q`.
- The coverage floor is 70 percent through coverage configuration, so low coverage fails the command.
- The goal is not to worship a number; the goal is to stop untested code from growing quietly.
- This week teaches fixtures, `tmp_path`, `monkeypatch`, parametrized tests, fakes, coverage reports, and CI lint-plus-test gates.
- Fixtures make setup reusable without hiding where test values come from.
- `tmp_path` makes file and SQLite tests isolated from a learner's real machine.
- `monkeypatch` makes environment and difficult failure paths controllable for one test at a time.
- Fakes in `tests/fakes/` keep service tests fast by replacing infrastructure with protocol-shaped in-memory objects.
- Coverage reports show which lines were exercised and which lines still need investigation.
- CI runs the same checks in a clean environment so the main branch does not depend on one developer's laptop.
- This chapter does not introduce classical ML model code, because topic classification begins in Week 11.
- This chapter does not introduce embeddings, RAG, FastAPI, or async testing patterns.
- The visible deliverable is a stronger quality gate; the deeper skill is knowing what kind of proof a behavior deserves.
- When finished, you should be able to explain why a fake is enough for a unit test and why real SQLite is still needed for an integration test.
1. In this chapter, **pytest discovery** matters because pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures.
2. In this chapter, **fixtures** matters because pytest fixtures are named setup functions requested by test parameters instead of called directly.
3. In this chapter, **fixture scope** matters because fixture scope controls how long a returned setup object lives before pytest creates a new one.
4. In this chapter, **function scope** matters because function scope gives every test a clean object and is safest for mutable fakes.
5. In this chapter, **module scope** matters because module scope shares one object across a file and is safe only when shared state cannot leak.
6. In this chapter, **session scope** matters because session scope shares one object across the whole run and should be rare in beginner project tests.
7. In this chapter, **tmp_path** matters because tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work.
8. In this chapter, **monkeypatch** matters because monkeypatch temporarily changes environment variables or attributes and then restores them.
9. In this chapter, **fakes** matters because fakes are small test implementations of ResearchOps protocols stored under tests/fakes.
10. In this chapter, **unit tests** matters because unit tests prove one service or function with outside dependencies replaced by fakes.

## 2. What you already know from previous weeks
- Week 1 taught repository scaffold and CLI shape; this matters because tests can now check a package instead of loose scripts.
- Week 2 taught files, pathlib, exceptions, and logging; this matters because `tmp_path` and precise failure assertions now have context.
- Week 3 taught domain models and dataclasses; this matters because tests should create real domain objects instead of vague dictionaries.
- Week 4 taught packaging and entry points; this matters because CLI smoke tests can verify the installed command responds.
- Week 5 taught SQLite storage; this matters because integration tests can prove real persistence without polluting local files.
- Week 6 taught parsing pipeline; this matters because failure-path tests can prove parser errors are recorded safely.
- Week 7 taught keyword search and data quality; this matters because parametrized tests can cover search normalization and edge cases.
- Week 8 taught multiprocessing ingestion; this matters because tests should avoid accidental heavy process work when a fake is enough.
- Week 9 taught protocols and clean architecture; this matters because fakes can implement interfaces so services do not import infrastructure.
- You already know that core should not import storage, CLI, API, workers, search, or ML infrastructure.
- You already know that services should depend on protocols rather than concrete SQLite or parser classes.
- You already know that CLI code should wire dependencies and delegate business behavior to services.
- Testing now becomes the way to prove those boundaries stay honest.
- A service test that cannot run without SQLite is a warning sign unless the service is explicitly about SQLite.
- A fake that cannot implement a protocol cleanly is a warning sign that the protocol may be unclear.
- A test that writes into the repository root is a warning sign that file isolation is missing.
- A failing test is not an insult; it is feedback about a promise that is either broken or poorly stated.
- Prior weeks make **integration tests** meaningful now: integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation.
- Prior weeks make **E2E smoke tests** meaningful now: E2E smoke tests prove the installed CLI starts without trying to test every branch.
- Prior weeks make **parametrize** meaningful now: parametrize runs the same behavior check against multiple clear input and expected output cases.
- Prior weeks make **coverage** meaningful now: coverage records which ResearchOps source lines ran while tests executed.
- Prior weeks make **term-missing** meaningful now: term-missing prints uncovered line numbers so the learner can inspect concrete gaps.
- Prior weeks make **fail_under** meaningful now: fail_under turns a coverage percentage into a failing command when it drops below the floor.
- Prior weeks make **Ruff** meaningful now: Ruff checks source and tests for Python errors, import issues, and selected style rules.
- Prior weeks make **CI gates** meaningful now: CI gates run the same checks automatically so broken changes cannot rely on memory or luck.
- Prior weeks make **flaky tests** meaningful now: flaky tests pass and fail without code changes and destroy trust in the suite.
- Prior weeks make **test names** meaningful now: test names should read like behavior statements so failures explain what broke.

## 3. What problem this week solves
- ResearchOps has reached the point where manual verification is too slow and too unreliable.
- A learner can fix one search case while breaking another search edge case.
- A learner can alter storage code and silently change ingestion behavior.
- A learner can add a source file and forget to add tests for failure paths.
- A learner can pass local tests and still fail CI if the local command differs from the project gate.
- This week solves those problems by making evidence repeatable.
- Every important behavior should have a focused test that names the behavior.
- Every test should prepare its own state or request clean state through a fixture.
- Every file-system test should use pytest-managed paths rather than existing project files.
- Every service unit test should prefer fakes over real infrastructure unless infrastructure is the behavior under inspection.
- Every coverage report should be read as a map of unvisited behavior, not as a scoreboard.
- Every CI failure should block progress until understood.
- The week also solves communication: good test names tell future maintainers what promise failed.
- The week also solves fear: a meaningful suite makes refactoring less scary because behavior is checked automatically.
- The problem addressed by **pytest discovery** is this: pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures, so the learner can move from hope to evidence.
- The problem addressed by **fixtures** is this: pytest fixtures are named setup functions requested by test parameters instead of called directly, so the learner can move from hope to evidence.
- The problem addressed by **fixture scope** is this: fixture scope controls how long a returned setup object lives before pytest creates a new one, so the learner can move from hope to evidence.
- The problem addressed by **function scope** is this: function scope gives every test a clean object and is safest for mutable fakes, so the learner can move from hope to evidence.
- The problem addressed by **module scope** is this: module scope shares one object across a file and is safe only when shared state cannot leak, so the learner can move from hope to evidence.
- The problem addressed by **session scope** is this: session scope shares one object across the whole run and should be rare in beginner project tests, so the learner can move from hope to evidence.
- The problem addressed by **tmp_path** is this: tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work, so the learner can move from hope to evidence.
- The problem addressed by **monkeypatch** is this: monkeypatch temporarily changes environment variables or attributes and then restores them, so the learner can move from hope to evidence.
- The problem addressed by **fakes** is this: fakes are small test implementations of ResearchOps protocols stored under tests/fakes, so the learner can move from hope to evidence.
- The problem addressed by **unit tests** is this: unit tests prove one service or function with outside dependencies replaced by fakes, so the learner can move from hope to evidence.
- The problem addressed by **integration tests** is this: integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation, so the learner can move from hope to evidence.
- The problem addressed by **E2E smoke tests** is this: E2E smoke tests prove the installed CLI starts without trying to test every branch, so the learner can move from hope to evidence.
- The problem addressed by **parametrize** is this: parametrize runs the same behavior check against multiple clear input and expected output cases, so the learner can move from hope to evidence.
- The problem addressed by **coverage** is this: coverage records which ResearchOps source lines ran while tests executed, so the learner can move from hope to evidence.
- The problem addressed by **term-missing** is this: term-missing prints uncovered line numbers so the learner can inspect concrete gaps, so the learner can move from hope to evidence.
- The problem addressed by **fail_under** is this: fail_under turns a coverage percentage into a failing command when it drops below the floor, so the learner can move from hope to evidence.
- The problem addressed by **Ruff** is this: Ruff checks source and tests for Python errors, import issues, and selected style rules, so the learner can move from hope to evidence.
- The problem addressed by **CI gates** is this: CI gates run the same checks automatically so broken changes cannot rely on memory or luck, so the learner can move from hope to evidence.
- The problem addressed by **flaky tests** is this: flaky tests pass and fail without code changes and destroy trust in the suite, so the learner can move from hope to evidence.
- The problem addressed by **test names** is this: test names should read like behavior statements so failures explain what broke, so the learner can move from hope to evidence.

## 4. Beginner mental model
- Think of a test as a tiny science experiment.
- The experiment prepares a controlled world, exercises one behavior, and inspects the result.
- This is the Arrange, Act, Assert pattern.
- Arrange creates papers, repositories, paths, settings, or fakes.
- Act calls the one behavior being tested.
- Assert checks the outcome that matters to ResearchOps.
- A fixture is reusable laboratory equipment supplied by pytest.
- Function-scoped fixtures give each experiment clean equipment.
- `tmp_path` is a clean workbench for temporary files and databases.
- `monkeypatch` is a temporary switch that pytest flips back after the experiment.
- A fake is a stage prop that keeps the same shape as a real dependency but avoids outside resources.
- Coverage is a map of where the experiments walked through the source code.
- A quality gate is a locked door that opens only when the agreed checks pass.
1. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
2. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
3. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
4. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
5. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
6. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
7. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
8. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
9. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
10. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
11. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
12. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
13. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
14. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?
15. Ask before writing a test: what exact behavior am I proving, what state must be isolated, and what assertion would fail if the behavior regressed?

## 5. Core vocabulary
| Term | Beginner meaning | ResearchOps reason |
|---|---|---|
| pytest discovery | pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| fixtures | pytest fixtures are named setup functions requested by test parameters instead of called directly. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| fixture scope | fixture scope controls how long a returned setup object lives before pytest creates a new one. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| function scope | function scope gives every test a clean object and is safest for mutable fakes. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| module scope | module scope shares one object across a file and is safe only when shared state cannot leak. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| session scope | session scope shares one object across the whole run and should be rare in beginner project tests. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| tmp_path | tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| monkeypatch | monkeypatch temporarily changes environment variables or attributes and then restores them. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| fakes | fakes are small test implementations of ResearchOps protocols stored under tests/fakes. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| unit tests | unit tests prove one service or function with outside dependencies replaced by fakes. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| integration tests | integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| E2E smoke tests | E2E smoke tests prove the installed CLI starts without trying to test every branch. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| parametrize | parametrize runs the same behavior check against multiple clear input and expected output cases. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| coverage | coverage records which ResearchOps source lines ran while tests executed. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| term-missing | term-missing prints uncovered line numbers so the learner can inspect concrete gaps. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| fail_under | fail_under turns a coverage percentage into a failing command when it drops below the floor. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| Ruff | Ruff checks source and tests for Python errors, import issues, and selected style rules. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| CI gates | CI gates run the same checks automatically so broken changes cannot rely on memory or luck. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| flaky tests | flaky tests pass and fail without code changes and destroy trust in the suite. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| test names | test names should read like behavior statements so failures explain what broke. | It helps Week 10 build reliable tests and quality gates without future-week features. |
| Arrange | the setup phase. | keeps test data obvious. |
| Act | the behavior call. | keeps the test focused. |
| Assert | the verification phase. | turns expectation into proof. |
| regression | a previously working behavior breaking. | tests catch it early. |
| test double | an object that stands in for a collaborator. | fakes are the preferred project-owned double here. |
| isolation | keeping one test from affecting another. | prevents order-dependent failures. |
| quality gate | a required check before accepting code. | CI automates the standard. |
| failure path | what happens when inputs or dependencies go wrong. | ResearchOps must record and report failures clearly. |
- Vocabulary is useful only when connected to files.
- For each term, point to one test, fixture, fake, command, or configuration line before moving on.

## 6. Concept explanations from first principles
### pytest discovery
- Plain meaning: pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures.
- Why it exists: without pytest discovery, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating pytest discovery as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply pytest discovery only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this pytest discovery example were removed from the quality workflow?
### fixtures
- Plain meaning: pytest fixtures are named setup functions requested by test parameters instead of called directly.
- Why it exists: without fixtures, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating fixtures as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply fixtures only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this fixtures example were removed from the quality workflow?
### fixture scope
- Plain meaning: fixture scope controls how long a returned setup object lives before pytest creates a new one.
- Why it exists: without fixture scope, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating fixture scope as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply fixture scope only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this fixture scope example were removed from the quality workflow?
### function scope
- Plain meaning: function scope gives every test a clean object and is safest for mutable fakes.
- Why it exists: without function scope, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating function scope as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply function scope only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this function scope example were removed from the quality workflow?
### module scope
- Plain meaning: module scope shares one object across a file and is safe only when shared state cannot leak.
- Why it exists: without module scope, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating module scope as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply module scope only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this module scope example were removed from the quality workflow?
### session scope
- Plain meaning: session scope shares one object across the whole run and should be rare in beginner project tests.
- Why it exists: without session scope, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating session scope as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply session scope only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this session scope example were removed from the quality workflow?
### tmp_path
- Plain meaning: tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work.
- Why it exists: without tmp_path, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating tmp_path as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply tmp_path only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this tmp_path example were removed from the quality workflow?
### monkeypatch
- Plain meaning: monkeypatch temporarily changes environment variables or attributes and then restores them.
- Why it exists: without monkeypatch, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating monkeypatch as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply monkeypatch only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this monkeypatch example were removed from the quality workflow?
### fakes
- Plain meaning: fakes are small test implementations of ResearchOps protocols stored under tests/fakes.
- Why it exists: without fakes, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating fakes as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply fakes only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this fakes example were removed from the quality workflow?
### unit tests
- Plain meaning: unit tests prove one service or function with outside dependencies replaced by fakes.
- Why it exists: without unit tests, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating unit tests as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply unit tests only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this unit tests example were removed from the quality workflow?
### integration tests
- Plain meaning: integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation.
- Why it exists: without integration tests, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating integration tests as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply integration tests only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this integration tests example were removed from the quality workflow?
### E2E smoke tests
- Plain meaning: E2E smoke tests prove the installed CLI starts without trying to test every branch.
- Why it exists: without E2E smoke tests, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating E2E smoke tests as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply E2E smoke tests only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this E2E smoke tests example were removed from the quality workflow?
### parametrize
- Plain meaning: parametrize runs the same behavior check against multiple clear input and expected output cases.
- Why it exists: without parametrize, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating parametrize as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply parametrize only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this parametrize example were removed from the quality workflow?
### coverage
- Plain meaning: coverage records which ResearchOps source lines ran while tests executed.
- Why it exists: without coverage, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating coverage as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply coverage only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this coverage example were removed from the quality workflow?
### term-missing
- Plain meaning: term-missing prints uncovered line numbers so the learner can inspect concrete gaps.
- Why it exists: without term-missing, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating term-missing as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply term-missing only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this term-missing example were removed from the quality workflow?
### fail_under
- Plain meaning: fail_under turns a coverage percentage into a failing command when it drops below the floor.
- Why it exists: without fail_under, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating fail_under as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply fail_under only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this fail_under example were removed from the quality workflow?
### Ruff
- Plain meaning: Ruff checks source and tests for Python errors, import issues, and selected style rules.
- Why it exists: without Ruff, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating Ruff as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply Ruff only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this Ruff example were removed from the quality workflow?
### CI gates
- Plain meaning: CI gates run the same checks automatically so broken changes cannot rely on memory or luck.
- Why it exists: without CI gates, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating CI gates as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply CI gates only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this CI gates example were removed from the quality workflow?
### flaky tests
- Plain meaning: flaky tests pass and fail without code changes and destroy trust in the suite.
- Why it exists: without flaky tests, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating flaky tests as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply flaky tests only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this flaky tests example were removed from the quality workflow?
### test names
- Plain meaning: test names should read like behavior statements so failures explain what broke.
- Why it exists: without test names, ResearchOps would rely on memory instead of a repeatable check.
- Beginner risk: treating test names as a magic word instead of tracing what value enters and what proof comes out.
- ResearchOps use: apply test names only at the layer being tested, and do not use it to sneak in Week 11 or later features.
- Good question: what would break if this test names example were removed from the quality workflow?

### Fixture example
```python
import pytest

@pytest.fixture()
def paper_repo() -> FakePaperRepository:
    return FakePaperRepository()

def test_new_repository_starts_empty(paper_repo: FakePaperRepository) -> None:
    assert paper_repo.list_all() == []
```
- Line 1 imports pytest so the fixture decorator is available.
- Line 3 marks the next function as pytest-managed setup.
- Line 4 names the fixture and states the returned fake type.
- Line 5 creates a fresh in-memory repository.
- Line 7 requests the fixture by parameter name.
- Line 8 asserts the visible initial behavior.
- The test does not call the fixture directly because pytest owns fixture setup and scope.
### tmp_path example
```python
def test_reads_title_from_file(tmp_path: Path) -> None:
    paper_file = tmp_path / "paper.txt"
    paper_file.write_text("Quality Gates\nBody", encoding="utf-8")
    title = read_first_line(paper_file)
    assert title == "Quality Gates"
```
- Line 1 requests a pytest-managed temporary directory.
- Line 2 creates a file path inside that directory.
- Line 3 writes controlled test data.
- Line 4 acts by calling the behavior under test.
- Line 5 asserts the exact result.
- No manual cleanup is needed because pytest manages the temporary location.
### monkeypatch example
```python
def test_setting_uses_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RESEARCHOPS_DB_NAME", "quality-gate.db")
    settings = Settings()
    assert settings.db_name == "quality-gate.db"
```
- Line 1 requests the monkeypatch fixture.
- Line 2 changes an environment variable for this one test.
- Line 3 creates settings after the environment is controlled.
- Line 4 asserts the setting used the override.
- pytest restores the environment after the test.

## 7. ResearchOps-specific application
- Service tests should use fakes for repositories, parsers, and failure stores when the service decision is under test.
- SQLite repository tests should use the real repository and a database path under `tmp_path`.
- CLI smoke tests should prove the command starts and delegates, not duplicate every service test.
- `tests/fakes/` should contain reusable fake implementations of core protocols.
- `tests/conftest.py` should contain shared fixtures only when sharing improves clarity.
- The coverage command should measure `researchops`, not the tests themselves.
- The CI workflow should run Ruff and pytest coverage as named, understandable steps.
- No future-week model, embedding, API, or async behavior is needed to complete this week.
- In researchops-specific application, **pytest discovery** means pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **fixtures** means pytest fixtures are named setup functions requested by test parameters instead of called directly; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **fixture scope** means fixture scope controls how long a returned setup object lives before pytest creates a new one; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **function scope** means function scope gives every test a clean object and is safest for mutable fakes; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **module scope** means module scope shares one object across a file and is safe only when shared state cannot leak; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **session scope** means session scope shares one object across the whole run and should be rare in beginner project tests; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **tmp_path** means tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **monkeypatch** means monkeypatch temporarily changes environment variables or attributes and then restores them; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **fakes** means fakes are small test implementations of ResearchOps protocols stored under tests/fakes; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **unit tests** means unit tests prove one service or function with outside dependencies replaced by fakes; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **integration tests** means integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation; apply it only when it proves a real ResearchOps responsibility.
- In researchops-specific application, **E2E smoke tests** means E2E smoke tests prove the installed CLI starts without trying to test every branch; apply it only when it proves a real ResearchOps responsibility.

## 8. Code examples with line-by-line explanation
- In code examples with line-by-line explanation, **pytest discovery** means pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **fixtures** means pytest fixtures are named setup functions requested by test parameters instead of called directly; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **fixture scope** means fixture scope controls how long a returned setup object lives before pytest creates a new one; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **function scope** means function scope gives every test a clean object and is safest for mutable fakes; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **module scope** means module scope shares one object across a file and is safe only when shared state cannot leak; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **session scope** means session scope shares one object across the whole run and should be rare in beginner project tests; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **tmp_path** means tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **monkeypatch** means monkeypatch temporarily changes environment variables or attributes and then restores them; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **fakes** means fakes are small test implementations of ResearchOps protocols stored under tests/fakes; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **unit tests** means unit tests prove one service or function with outside dependencies replaced by fakes; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **integration tests** means integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation; apply it only when it proves a real ResearchOps responsibility.
- In code examples with line-by-line explanation, **E2E smoke tests** means E2E smoke tests prove the installed CLI starts without trying to test every branch; apply it only when it proves a real ResearchOps responsibility.

### Shared conftest fixture example
```python
import pytest

from tests.fakes.fake_repository import FakePaperRepository


@pytest.fixture()
def paper_repo() -> FakePaperRepository:
    return FakePaperRepository()
```
- Line 1 imports pytest because fixture decorators belong to pytest.
- Line 3 imports the test fake, not a production SQLite repository.
- Line 6 marks the function as a fixture available to tests below this conftest scope.
- Line 7 gives the fixture a behavior name instead of a vague name like data.
- Line 8 returns a fresh fake repository for each test by default.
- This belongs in conftest only when multiple test modules use the same idea.
- If one test file uses the fixture, keeping it local can be clearer.
- A huge conftest file is a hidden dependency map and becomes hard for beginners to follow.
### Fake repository behavior example
```python
class FakePaperRepository:
    def __init__(self) -> None:
        self._papers: dict[str, Paper] = {}

    def save(self, paper: Paper) -> None:
        self._papers[paper.id] = paper

    def list_all(self) -> list[Paper]:
        return list(self._papers.values())
```
- Line 1 defines a fake, not a mock tied to call counts.
- Line 2 creates private in-memory storage for the fake.
- Line 3 chooses a dictionary so paper IDs stay unique.
- Line 5 implements the same save idea the service expects from a repository.
- Line 6 stores the paper by ID.
- Line 8 implements list behavior expected by services.
- Line 9 returns papers without touching SQLite.
- The fake is intentionally boring because its job is to support service tests, not simulate every database detail.
- If a service needs sorting, filtering, or existence behavior, the fake should implement enough of the protocol to make that service test honest.
- If the fake grows complex, check whether the production protocol is too broad or the test is trying to prove too much.
### SQLite integration example
```python
def test_sqlite_delete_removes_saved_paper(tmp_path: Path) -> None:
    database_path = tmp_path / "researchops.db"
    repository = SQLitePaperRepository(database_path)
    repository.initialize_schema()

    repository.save(make_paper(paper_id="p1"))
    repository.save(make_paper(paper_id="p2"))
    repository.delete("p1")

    remaining_ids = [paper.id for paper in repository.list_all()]

    assert remaining_ids == ["p2"]
    assert repository.exists("p1") is False
```
- Line 1 names a real persistence behavior.
- Line 2 uses tmp_path so the test does not touch a developer database.
- Line 3 creates the real SQLite repository because this is integration coverage.
- Line 4 initializes tables before saving data.
- Lines 6 and 7 arrange two records.
- Line 8 acts by deleting one record.
- Line 10 reads the visible state after deletion.
- Line 12 asserts the remaining record list.
- Line 13 asserts the deleted record no longer exists.
- This is not a unit test because it intentionally crosses the SQLite boundary.
- The value of the test is that SQL schema, write behavior, delete behavior, and read behavior all meet correctly.
### Parametrized search validation example
```python
@pytest.mark.parametrize(
    ("query", "should_raise"),
    [
        ("", True),
        ("   ", True),
        ("graph", False),
        ("Graph", False),
    ],
)
def test_search_query_validation(query: str, should_raise: bool, paper_repo: FakePaperRepository) -> None:
    service = KeywordSearchService(paper_repo=paper_repo)

    if should_raise:
        with pytest.raises(EmptyQueryError):
            service.search(query)
    else:
        service.search(query)
```
- Line 1 starts parametrization for repeated validation behavior.
- Line 2 names the changing values.
- Lines 4 and 5 cover empty and whitespace-only inputs.
- Lines 6 and 7 cover normal text with different casing.
- Line 10 requests the fake repository fixture.
- Line 11 creates the service under test.
- Line 13 branches inside the test based on the expected category.
- Line 14 asserts the exact exception for invalid input.
- Line 15 calls the behavior that should reject the query.
- Line 17 calls the behavior that should not reject the query.
- This example is acceptable because all cases test one concept: query validation.
- If the normal query cases needed detailed result assertions, they should become separate search-result tests.
### Coverage output reading example
```text
Name                                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
researchops/services/search_service.py       54      6    89%   41-44, 67
researchops/storage/sqlite_repository.py     88     18    80%   102-130
researchops/cli/main.py                      20      2    90%   35-36
TOTAL                                       240     26    89%
```
- Line 1 is the table header produced by coverage.
- Line 3 shows a service module with missing lines.
- The learner should open lines 41 through 44 before deciding what test to write.
- Line 4 shows a larger SQLite gap that may need integration tests.
- The learner should not blindly test every line if some belong to unreachable defensive code.
- Line 5 shows CLI missing lines, which may be appropriate for a small smoke test.
- Line 6 shows total coverage, but the total is less important than meaningful missing behavior.
- A strong coverage workflow reads missing lines, classifies behavior, then writes the smallest useful test.
- A weak coverage workflow adds shallow calls only to move the percentage.
### CI gate example
```yaml
- name: Lint source and tests
  run: ruff check src tests

- name: Run tests with coverage
  run: pytest --cov=researchops --cov-report=term-missing -q
```
- Line 1 gives the lint gate a readable CI name.
- Line 2 runs the exact Week 10 Ruff command.
- Line 4 gives the test gate a readable CI name.
- Line 5 runs the exact Week 10 pytest coverage command.
- The 70 percent floor can live in coverage configuration rather than being repeated in the command.
- Readable CI names help beginners understand which gate failed.
- Do not add model training, web service startup, embedding generation, or async workers to this Week 10 gate.
### Choosing the right proof
- If the behavior is pure text normalization, use a parametrized unit test.
- If the behavior is service coordination, use fakes for repositories and parsers.
- If the behavior is SQLite persistence, use a real SQLite repository under tmp_path.
- If the behavior is CLI startup, use a small E2E smoke test.
- If the behavior is environment configuration, use monkeypatch.setenv or monkeypatch.delenv.
- If the behavior is a third-party failure that is hard to trigger, monkeypatch may be appropriate.
- If the behavior is a project-owned dependency with a protocol, prefer a fake.
- If the behavior is future model training, stop because that belongs to Week 11.
- If the behavior is embeddings or RAG, stop because that belongs later.
- If the behavior is FastAPI or async wiring, stop because this week is not about that layer.
### Good assertion checklist
- Assert exact IDs when identity matters.
- Assert exact counts when count matters.
- Assert ordering when ranking matters.
- Assert exception types when invalid input matters.
- Assert failure records when failure handling matters.
- Assert file existence only when file creation is the promise.
- Assert file content when content correctness is the promise.
- Avoid `assert result` when an empty list is a meaningful outcome.
- Avoid `assert result is not None` when a precise value is available.
- Avoid asserting private helper calls unless the call itself is the public contract.

## 9. Common beginner mistakes
- Using real SQLite in every service unit test makes the suite slow and hides service intent.
- Using monkeypatch instead of an injected fake couples tests to internal names.
- Putting every helper into `conftest.py` hides local test setup.
- Making mutable fixtures module-scoped creates order-dependent failures.
- Asserting only `is not None` gives coverage without useful proof.
- Lowering `fail_under` after failure weakens the gate instead of fixing the gap.
- Adding future-week features distracts from testing discipline.
- Ignoring Ruff in tests treats test code as disposable even though it protects the project.
- In common beginner mistakes, **pytest discovery** means pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **fixtures** means pytest fixtures are named setup functions requested by test parameters instead of called directly; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **fixture scope** means fixture scope controls how long a returned setup object lives before pytest creates a new one; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **function scope** means function scope gives every test a clean object and is safest for mutable fakes; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **module scope** means module scope shares one object across a file and is safe only when shared state cannot leak; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **session scope** means session scope shares one object across the whole run and should be rare in beginner project tests; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **tmp_path** means tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **monkeypatch** means monkeypatch temporarily changes environment variables or attributes and then restores them; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **fakes** means fakes are small test implementations of ResearchOps protocols stored under tests/fakes; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **unit tests** means unit tests prove one service or function with outside dependencies replaced by fakes; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **integration tests** means integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation; apply it only when it proves a real ResearchOps responsibility.
- In common beginner mistakes, **E2E smoke tests** means E2E smoke tests prove the installed CLI starts without trying to test every branch; apply it only when it proves a real ResearchOps responsibility.

## 10. Debugging guidance
- Start with the first failing test name, then classify the failure as import, fixture, runtime, assertion, lint, or coverage.
- Fixture-not-found means pytest could not discover a name; check spelling and `conftest.py` visibility.
- Import failure means the test module did not load; fix paths and dependencies before debugging behavior.
- Assertion failure means the behavior ran and produced an unexpected value; inspect the closest value to the assertion.
- Monkeypatch failure often means the wrong object was patched; patch where the code under test looks up the object.
- File-not-found in tests often means the code used a different path than the one created under `tmp_path`.
- Coverage failure means the suite completed but did not execute enough source; read missing lines before editing configuration.
- CI-only failure often means local commands, environment, or hidden state differ from the clean gate.
- In debugging guidance, **pytest discovery** means pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **fixtures** means pytest fixtures are named setup functions requested by test parameters instead of called directly; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **fixture scope** means fixture scope controls how long a returned setup object lives before pytest creates a new one; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **function scope** means function scope gives every test a clean object and is safest for mutable fakes; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **module scope** means module scope shares one object across a file and is safe only when shared state cannot leak; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **session scope** means session scope shares one object across the whole run and should be rare in beginner project tests; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **tmp_path** means tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **monkeypatch** means monkeypatch temporarily changes environment variables or attributes and then restores them; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **fakes** means fakes are small test implementations of ResearchOps protocols stored under tests/fakes; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **unit tests** means unit tests prove one service or function with outside dependencies replaced by fakes; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **integration tests** means integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation; apply it only when it proves a real ResearchOps responsibility.
- In debugging guidance, **E2E smoke tests** means E2E smoke tests prove the installed CLI starts without trying to test every branch; apply it only when it proves a real ResearchOps responsibility.

## 11. Design tradeoffs
- Unit tests are fast and precise but cannot prove real SQLite wiring.
- Integration tests prove boundaries but should be fewer because they are slower and more setup-heavy.
- E2E smoke tests prove package entry points but become brittle when they assert too much formatting.
- Function-scoped fixtures repeat setup but protect isolation.
- Broader fixture scopes can save time but require strong confidence that state cannot leak.
- Fakes make architecture visible but must stay faithful to protocols.
- Monkeypatch reaches hard failure paths but should not replace clean dependency injection.
- Coverage thresholds prevent neglect but cannot judge assertion quality.
- In design tradeoffs, **pytest discovery** means pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **fixtures** means pytest fixtures are named setup functions requested by test parameters instead of called directly; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **fixture scope** means fixture scope controls how long a returned setup object lives before pytest creates a new one; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **function scope** means function scope gives every test a clean object and is safest for mutable fakes; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **module scope** means module scope shares one object across a file and is safe only when shared state cannot leak; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **session scope** means session scope shares one object across the whole run and should be rare in beginner project tests; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **tmp_path** means tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **monkeypatch** means monkeypatch temporarily changes environment variables or attributes and then restores them; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **fakes** means fakes are small test implementations of ResearchOps protocols stored under tests/fakes; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **unit tests** means unit tests prove one service or function with outside dependencies replaced by fakes; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **integration tests** means integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation; apply it only when it proves a real ResearchOps responsibility.
- In design tradeoffs, **E2E smoke tests** means E2E smoke tests prove the installed CLI starts without trying to test every branch; apply it only when it proves a real ResearchOps responsibility.

## 12. Testing implications
- Every new feature needs a test in the same change.
- Every bug fix should add a regression test when the behavior can be reproduced.
- Unit tests belong in `tests/unit/` and should be fast.
- Integration tests belong in `tests/integration/` and may use real SQLite under `tmp_path`.
- E2E smoke tests belong in `tests/e2e/` and should remain small.
- Fake implementations belong in `tests/fakes/`.
- Shared fixtures belong in `tests/conftest.py` only when they express common vocabulary.
- The two required validation commands are `ruff check src tests` and `pytest --cov=researchops --cov-report=term-missing -q`.
- In testing implications, **pytest discovery** means pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **fixtures** means pytest fixtures are named setup functions requested by test parameters instead of called directly; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **fixture scope** means fixture scope controls how long a returned setup object lives before pytest creates a new one; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **function scope** means function scope gives every test a clean object and is safest for mutable fakes; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **module scope** means module scope shares one object across a file and is safe only when shared state cannot leak; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **session scope** means session scope shares one object across the whole run and should be rare in beginner project tests; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **tmp_path** means tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **monkeypatch** means monkeypatch temporarily changes environment variables or attributes and then restores them; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **fakes** means fakes are small test implementations of ResearchOps protocols stored under tests/fakes; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **unit tests** means unit tests prove one service or function with outside dependencies replaced by fakes; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **integration tests** means integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation; apply it only when it proves a real ResearchOps responsibility.
- In testing implications, **E2E smoke tests** means E2E smoke tests prove the installed CLI starts without trying to test every branch; apply it only when it proves a real ResearchOps responsibility.

## 13. Architecture implications
- Tests should reinforce the inward dependency direction rather than bypass it.
- Core tests should not need infrastructure imports.
- Service tests should depend on protocols and fakes rather than concrete SQLite implementations.
- Infrastructure tests may import infrastructure because that boundary is the subject.
- CLI tests should check user-visible command behavior and not host business logic.
- A hard-to-test service often reveals hidden dependencies.
- A fake that mirrors a protocol confirms that the protocol is usable.
- A CI gate protects architecture only when tests and lint rules reflect the intended boundaries.
- In architecture implications, **pytest discovery** means pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **fixtures** means pytest fixtures are named setup functions requested by test parameters instead of called directly; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **fixture scope** means fixture scope controls how long a returned setup object lives before pytest creates a new one; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **function scope** means function scope gives every test a clean object and is safest for mutable fakes; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **module scope** means module scope shares one object across a file and is safe only when shared state cannot leak; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **session scope** means session scope shares one object across the whole run and should be rare in beginner project tests; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **tmp_path** means tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **monkeypatch** means monkeypatch temporarily changes environment variables or attributes and then restores them; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **fakes** means fakes are small test implementations of ResearchOps protocols stored under tests/fakes; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **unit tests** means unit tests prove one service or function with outside dependencies replaced by fakes; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **integration tests** means integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation; apply it only when it proves a real ResearchOps responsibility.
- In architecture implications, **E2E smoke tests** means E2E smoke tests prove the installed CLI starts without trying to test every branch; apply it only when it proves a real ResearchOps responsibility.

## 14. How this connects to AI engineering / ML research
- AI systems fail quietly when data pipelines change without proof.
- A parser regression can corrupt future training data while producing plausible text.
- A search normalization regression can change retrieval results while still returning papers.
- A storage regression can lose labels or metadata that future models need.
- Testing discipline creates reproducibility before model evaluation begins.
- Coverage reveals whether failure paths in research infrastructure have been exercised.
- Fakes keep service rules testable without expensive computation.
- CI gives every experiment-supporting change the same baseline evidence.
- In how this connects to ai engineering / ml research, **pytest discovery** means pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **fixtures** means pytest fixtures are named setup functions requested by test parameters instead of called directly; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **fixture scope** means fixture scope controls how long a returned setup object lives before pytest creates a new one; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **function scope** means function scope gives every test a clean object and is safest for mutable fakes; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **module scope** means module scope shares one object across a file and is safe only when shared state cannot leak; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **session scope** means session scope shares one object across the whole run and should be rare in beginner project tests; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **tmp_path** means tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **monkeypatch** means monkeypatch temporarily changes environment variables or attributes and then restores them; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **fakes** means fakes are small test implementations of ResearchOps protocols stored under tests/fakes; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **unit tests** means unit tests prove one service or function with outside dependencies replaced by fakes; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **integration tests** means integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation; apply it only when it proves a real ResearchOps responsibility.
- In how this connects to ai engineering / ml research, **E2E smoke tests** means E2E smoke tests prove the installed CLI starts without trying to test every branch; apply it only when it proves a real ResearchOps responsibility.

## 15. Mini quizzes
1. What does pytest discover by naming convention?
2. Why should mutable fixtures usually be function-scoped?
3. What does `tmp_path` return?
4. When is monkeypatch better than a fake?
5. When is a fake better than monkeypatch?
6. Why should fakes live under `tests/fakes/`?
7. What is the difference between unit and integration tests?
8. What exact command runs Ruff for Week 10?
9. What exact command runs pytest with coverage for Week 10?
10. What does `term-missing` show?
11. What does `fail_under = 70` enforce?
12. Why can high coverage still hide weak assertions?
13. What does CI add beyond local commands?
14. Why are flaky tests urgent?
15. Which future-week topics are forbidden here?

## 16. Explain-it-aloud prompts
- Explain pytest discovery in your own words, then give one ResearchOps example where pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures.
- Explain fixtures in your own words, then give one ResearchOps example where pytest fixtures are named setup functions requested by test parameters instead of called directly.
- Explain fixture scope in your own words, then give one ResearchOps example where fixture scope controls how long a returned setup object lives before pytest creates a new one.
- Explain function scope in your own words, then give one ResearchOps example where function scope gives every test a clean object and is safest for mutable fakes.
- Explain module scope in your own words, then give one ResearchOps example where module scope shares one object across a file and is safe only when shared state cannot leak.
- Explain session scope in your own words, then give one ResearchOps example where session scope shares one object across the whole run and should be rare in beginner project tests.
- Explain tmp_path in your own words, then give one ResearchOps example where tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work.
- Explain monkeypatch in your own words, then give one ResearchOps example where monkeypatch temporarily changes environment variables or attributes and then restores them.
- Explain fakes in your own words, then give one ResearchOps example where fakes are small test implementations of ResearchOps protocols stored under tests/fakes.
- Explain unit tests in your own words, then give one ResearchOps example where unit tests prove one service or function with outside dependencies replaced by fakes.
- Explain integration tests in your own words, then give one ResearchOps example where integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation.
- Explain E2E smoke tests in your own words, then give one ResearchOps example where E2E smoke tests prove the installed CLI starts without trying to test every branch.
- Explain parametrize in your own words, then give one ResearchOps example where parametrize runs the same behavior check against multiple clear input and expected output cases.
- Explain coverage in your own words, then give one ResearchOps example where coverage records which ResearchOps source lines ran while tests executed.
- Explain term-missing in your own words, then give one ResearchOps example where term-missing prints uncovered line numbers so the learner can inspect concrete gaps.
- Explain fail_under in your own words, then give one ResearchOps example where fail_under turns a coverage percentage into a failing command when it drops below the floor.
- Explain Ruff in your own words, then give one ResearchOps example where Ruff checks source and tests for Python errors, import issues, and selected style rules.
- Explain CI gates in your own words, then give one ResearchOps example where CI gates run the same checks automatically so broken changes cannot rely on memory or luck.
- Explain flaky tests in your own words, then give one ResearchOps example where flaky tests pass and fail without code changes and destroy trust in the suite.
- Explain test names in your own words, then give one ResearchOps example where test names should read like behavior statements so failures explain what broke.
- Explain why Week 10 is a quality chapter rather than a feature chapter.
- Explain what evidence would make you comfortable changing a service next week.

## 17. What to memorize
- `ruff check src tests` is the lint gate.
- `pytest --cov=researchops --cov-report=term-missing -q` is the test and coverage gate.
- Coverage must fail under 70 percent.
- Fixtures are requested by parameter name.
- Function scope is the default and safest mutable-fixture scope.
- `tmp_path` is for isolated file and database paths.
- `monkeypatch` changes are temporary.
- Fakes for protocols live in `tests/fakes/`.
- Unit tests use fakes; integration tests use real boundaries intentionally.
- Week 10 does not introduce classical ML models, embeddings, FastAPI, or async patterns.
- Remember the role of pytest discovery in the Week 10 quality gate.
- Remember the role of fixtures in the Week 10 quality gate.
- Remember the role of fixture scope in the Week 10 quality gate.
- Remember the role of function scope in the Week 10 quality gate.
- Remember the role of module scope in the Week 10 quality gate.
- Remember the role of session scope in the Week 10 quality gate.
- Remember the role of tmp_path in the Week 10 quality gate.
- Remember the role of monkeypatch in the Week 10 quality gate.
- Remember the role of fakes in the Week 10 quality gate.
- Remember the role of unit tests in the Week 10 quality gate.
- Remember the role of integration tests in the Week 10 quality gate.
- Remember the role of E2E smoke tests in the Week 10 quality gate.
- Remember the role of parametrize in the Week 10 quality gate.
- Remember the role of coverage in the Week 10 quality gate.
- Remember the role of term-missing in the Week 10 quality gate.
- Remember the role of fail_under in the Week 10 quality gate.
- Remember the role of Ruff in the Week 10 quality gate.
- Remember the role of CI gates in the Week 10 quality gate.
- Remember the role of flaky tests in the Week 10 quality gate.
- Remember the role of test names in the Week 10 quality gate.

## 18. What to understand deeply
- Isolation is what lets tests run in any order.
- Fakes are possible because services depend on protocols.
- Coverage is a map, not a moral score.
- A threshold is useful only when the tests have meaningful assertions.
- Monkeypatch is safest when used surgically.
- Fixture scope is a design decision about shared state.
- CI is the project standard repeated automatically.
- Testing pain often reveals architecture pain.
- Understand deeply that pytest discovery is not separate from design: pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures.
- Understand deeply that fixtures is not separate from design: pytest fixtures are named setup functions requested by test parameters instead of called directly.
- Understand deeply that fixture scope is not separate from design: fixture scope controls how long a returned setup object lives before pytest creates a new one.
- Understand deeply that function scope is not separate from design: function scope gives every test a clean object and is safest for mutable fakes.
- Understand deeply that module scope is not separate from design: module scope shares one object across a file and is safe only when shared state cannot leak.
- Understand deeply that session scope is not separate from design: session scope shares one object across the whole run and should be rare in beginner project tests.
- Understand deeply that tmp_path is not separate from design: tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work.
- Understand deeply that monkeypatch is not separate from design: monkeypatch temporarily changes environment variables or attributes and then restores them.
- Understand deeply that fakes is not separate from design: fakes are small test implementations of ResearchOps protocols stored under tests/fakes.
- Understand deeply that unit tests is not separate from design: unit tests prove one service or function with outside dependencies replaced by fakes.
- Understand deeply that integration tests is not separate from design: integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation.
- Understand deeply that E2E smoke tests is not separate from design: E2E smoke tests prove the installed CLI starts without trying to test every branch.
- Understand deeply that parametrize is not separate from design: parametrize runs the same behavior check against multiple clear input and expected output cases.
- Understand deeply that coverage is not separate from design: coverage records which ResearchOps source lines ran while tests executed.
- Understand deeply that term-missing is not separate from design: term-missing prints uncovered line numbers so the learner can inspect concrete gaps.
- Understand deeply that fail_under is not separate from design: fail_under turns a coverage percentage into a failing command when it drops below the floor.
- Understand deeply that Ruff is not separate from design: Ruff checks source and tests for Python errors, import issues, and selected style rules.
- Understand deeply that CI gates is not separate from design: CI gates run the same checks automatically so broken changes cannot rely on memory or luck.
- Understand deeply that flaky tests is not separate from design: flaky tests pass and fail without code changes and destroy trust in the suite.
- Understand deeply that test names is not separate from design: test names should read like behavior statements so failures explain what broke.

## 19. What not to worry about yet
- Do not write classical ML classifier code; Week 11 owns that.
- Do not write embedding code.
- Do not write RAG prompt or retrieval-answer tests.
- Do not add FastAPI test clients.
- Do not add async test patterns.
- Do not chase perfect coverage before meaningful behavior.
- Do not introduce new heavy dependencies.
- Do not turn `conftest.py` into a hidden maze.
- Do not benchmark performance formally.
- Do not mock every call when state-based assertions are clearer.
- For now, prefer one clear behavior test over advanced tooling idea 1.
- For now, prefer one clear behavior test over advanced tooling idea 2.
- For now, prefer one clear behavior test over advanced tooling idea 3.
- For now, prefer one clear behavior test over advanced tooling idea 4.
- For now, prefer one clear behavior test over advanced tooling idea 5.
- For now, prefer one clear behavior test over advanced tooling idea 6.
- For now, prefer one clear behavior test over advanced tooling idea 7.
- For now, prefer one clear behavior test over advanced tooling idea 8.
- For now, prefer one clear behavior test over advanced tooling idea 9.
- For now, prefer one clear behavior test over advanced tooling idea 10.
- For now, prefer one clear behavior test over advanced tooling idea 11.
- For now, prefer one clear behavior test over advanced tooling idea 12.
- For now, prefer one clear behavior test over advanced tooling idea 13.
- For now, prefer one clear behavior test over advanced tooling idea 14.
- For now, prefer one clear behavior test over advanced tooling idea 15.

## 20. Bridge to next week
- Week 11 introduces classical ML topic classification, which will depend on reliable data and stable service behavior.
- Week 10 prepares that work by making existing behavior testable and guarded.
- The future classifier will need clean inputs, trustworthy storage, and repeatable validation habits.
- The coverage gate will prevent large untested additions.
- The fake pattern will help service tests avoid expensive work.
- The integration-test pattern will keep persistence honest.
- The CI commands will give every future change the same baseline gate.
- Do not move to Week 11 until you can explain the Week 10 gate without reading the notes.
- The bridge includes pytest discovery: pytest finds files named like tests, then functions named like tests, and treats uncaught exceptions as failures, which keeps later ML work safer without implementing it early.
- The bridge includes fixtures: pytest fixtures are named setup functions requested by test parameters instead of called directly, which keeps later ML work safer without implementing it early.
- The bridge includes fixture scope: fixture scope controls how long a returned setup object lives before pytest creates a new one, which keeps later ML work safer without implementing it early.
- The bridge includes function scope: function scope gives every test a clean object and is safest for mutable fakes, which keeps later ML work safer without implementing it early.
- The bridge includes module scope: module scope shares one object across a file and is safe only when shared state cannot leak, which keeps later ML work safer without implementing it early.
- The bridge includes session scope: session scope shares one object across the whole run and should be rare in beginner project tests, which keeps later ML work safer without implementing it early.
- The bridge includes tmp_path: tmp_path gives each test a pathlib.Path directory managed by pytest for isolated file work, which keeps later ML work safer without implementing it early.
- The bridge includes monkeypatch: monkeypatch temporarily changes environment variables or attributes and then restores them, which keeps later ML work safer without implementing it early.
- The bridge includes fakes: fakes are small test implementations of ResearchOps protocols stored under tests/fakes, which keeps later ML work safer without implementing it early.
- The bridge includes unit tests: unit tests prove one service or function with outside dependencies replaced by fakes, which keeps later ML work safer without implementing it early.
- The bridge includes integration tests: integration tests prove real boundaries such as SQLite repository behavior with tmp_path isolation, which keeps later ML work safer without implementing it early.
- The bridge includes E2E smoke tests: E2E smoke tests prove the installed CLI starts without trying to test every branch, which keeps later ML work safer without implementing it early.
- The bridge includes parametrize: parametrize runs the same behavior check against multiple clear input and expected output cases, which keeps later ML work safer without implementing it early.
- The bridge includes coverage: coverage records which ResearchOps source lines ran while tests executed, which keeps later ML work safer without implementing it early.
- The bridge includes term-missing: term-missing prints uncovered line numbers so the learner can inspect concrete gaps, which keeps later ML work safer without implementing it early.
- The bridge includes fail_under: fail_under turns a coverage percentage into a failing command when it drops below the floor, which keeps later ML work safer without implementing it early.
- The bridge includes Ruff: Ruff checks source and tests for Python errors, import issues, and selected style rules, which keeps later ML work safer without implementing it early.
- The bridge includes CI gates: CI gates run the same checks automatically so broken changes cannot rely on memory or luck, which keeps later ML work safer without implementing it early.
- The bridge includes flaky tests: flaky tests pass and fail without code changes and destroy trust in the suite, which keeps later ML work safer without implementing it early.
- The bridge includes test names: test names should read like behavior statements so failures explain what broke, which keeps later ML work safer without implementing it early.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 10 — Testing and Quality Gates:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
