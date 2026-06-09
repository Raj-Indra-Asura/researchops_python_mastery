# Notes - Week 10 Testing Discipline and Quality Gates

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 10 — Testing & Quality Gates](./README.md) › **notes.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Why tests exist

Before automated tests existed, developers verified their code by running it manually, checking the output, and hoping nothing else broke. That works for a single module in isolation. It collapses when the codebase grows.

Tests exist for three reasons:

1. **Verification**: prove that the code does what you intended right now.
2. **Regression protection**: prove that it still does what you intended after a change.
3. **Documentation**: show how the code is meant to be used.

A regression is when a previously working feature breaks because of a change elsewhere. Without automated tests, you discover regressions when users report bugs. With tests, you discover them in seconds, locally, before the code ever ships.

For ResearchOps, this matters enormously. By Month 3 the codebase has ingestion, parsing, storage, search, and is about to get ML models. A change to the text cleaner could silently break search relevance. A change to the SQLite schema could silently break ingestion. Tests are the safety net that lets you move quickly.

---

## The test pyramid

The **test pyramid** is a model that describes how many tests you should have at each level of abstraction:

```
         /\
        /  \
       / E2E \       (few — slow, brittle, end-to-end)
      /--------\
     /          \
    / Integration \  (moderate — test boundaries like SQLite, file system)
   /--------------\
  /                \
 /   Unit Tests     \ (many — fast, isolated, no I/O)
/--------------------\
```

**Unit tests** test a single function or class in complete isolation. They use fakes for all dependencies. They should run in milliseconds. You should have dozens or hundreds.

**Integration tests** test the interaction between two real components — for example, `SQLiteRepository` plus the actual SQLite database. They may be slower (tens of milliseconds). You should have a moderate number.

**End-to-end (E2E) tests** run the full system as a user would. For ResearchOps, that means running the actual CLI commands and checking outputs. They are the slowest and the most brittle (fragile). You should have a small number of the most critical user flows.

The pyramid shape is important. Many codebases have it inverted — lots of slow E2E tests and few unit tests. That leads to a test suite that takes minutes to run, breaks for infrastructure reasons, and gives you no confidence about specific behaviors. Resist this.

In ResearchOps:

- `tests/unit/` — unit tests using fakes. Should be fast and numerous.
- `tests/integration/` — tests using real SQLite. Moderate count.
- `tests/e2e/` — tests using the real installed CLI. Small count.

---

## pytest fundamentals

### Running tests

```bash
pytest tests/unit/ -v        # verbose: see each test name
pytest tests/unit/ -q        # quiet: see only failures
pytest tests/unit/ -k "ingest"  # filter: run only tests whose name contains "ingest"
pytest -x                   # stop at first failure
pytest --maxfail=3           # stop after 3 failures
pytest -s                   # show print() output (useful for debugging)
pytest -vv                  # extra verbose: show diffs on assertion failures
```

### Fixture in depth

A **fixture** is reusable setup code that pytest injects into test functions as arguments.

```python
import pytest

@pytest.fixture()
def sample_query() -> str:
    return "semantic search"

def test_normalize_query(sample_query: str) -> None:
    assert normalize_text(sample_query) == "semantic search"
```

When pytest sees `test_normalize_query(sample_query: str)`, it looks for a fixture named `sample_query`, calls it, and passes the result as the `sample_query` argument. The test function never calls the fixture directly.

Fixtures can be:

- **Function-scoped** (default): called fresh for every test.
- **Module-scoped**: called once per test module file.
- **Session-scoped**: called once for the entire test run.

For fast unit tests, function scope is almost always right. For expensive setup like a filled database, module or session scope can save time.

Fixtures can also use other fixtures:

```python
@pytest.fixture()
def paper_repo() -> FakePaperRepository:
    return FakePaperRepository()

@pytest.fixture()
def service(paper_repo: FakePaperRepository) -> KeywordSearchService:
    return KeywordSearchService(paper_repo=paper_repo)
```

`service` depends on `paper_repo`. pytest resolves the dependency chain automatically.

### Temporary directory

`tmp_path` is a built-in pytest fixture that provides a temporary directory unique to the current test. The directory is cleaned up after the test run.

```python
def test_artifact_saved(tmp_path: Path) -> None:
    artifact_file = tmp_path / "model.joblib"
    save_artifact(artifact_file)
    assert artifact_file.exists()
```

You never need to create or clean up `tmp_path` yourself. This is especially useful for integration tests that write files.

### Temporary database

For tests that need SQLite, use `tmp_path` to give each test its own database:

```python
@pytest.fixture()
def sqlite_repo(tmp_path: Path) -> SQLiteRepository:
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    repo = SQLiteRepository(conn)
    repo.initialize_schema()
    return repo
```

Each test gets a fresh, isolated database. No test can contaminate another.

### Parametrize

`@pytest.mark.parametrize` runs the same test with multiple inputs:

```python
@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Machine Learning", "machine learning"),
        ("  NLP  ", "nlp"),
        ("BERT-based Retrieval", "bert-based retrieval"),
    ],
)
def test_normalise_for_search(raw: str, expected: str) -> None:
    assert normalise_for_search(raw) == expected
```

This generates three separate test cases from one test definition. pytest names them `test_normalise_for_search[Machine Learning-machine learning]`, etc. If one fails, the others still run.

---

## monkeypatch in depth

`monkeypatch` is a built-in pytest fixture that temporarily replaces attributes, functions, environment variables, or other objects during a single test. Replacements are automatically undone after the test.

### Patching a function

```python
def test_parser_returns_empty_on_failure(monkeypatch, tmp_path: Path) -> None:
    pdf = tmp_path / "broken.pdf"
    pdf.write_bytes(b"not a pdf")

    # Replace the underlying extract_text call to simulate a failure
    monkeypatch.setattr(
        "researchops.parsing.pdf_parser.fitz.open",
        lambda _: (_ for _ in ()).throw(Exception("cannot open")),
    )
    # Now test how the service handles the failure...
```

### Patching an environment variable

```python
def test_config_uses_env_db_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RESEARCHOPS_DB_PATH", "/tmp/test.db")
    settings = Settings()
    assert settings.db_path == "/tmp/test.db"
```

### When to use monkeypatch

monkeypatch is the right tool when:

- You need to test a specific failure path that is hard to trigger naturally.
- You need to control an environment variable or system call.
- The dependency cannot be injected (e.g., a function call inside a third-party library).

monkeypatch is the wrong tool when:

- The dependency CAN be injected (prefer a fake instead — it is more explicit).
- You find yourself patching many things to test one function (a sign the function has too many responsibilities).

The key difference between monkeypatch and a fake: a fake is explicit architecture. monkeypatch is a surgical bypass of the real code. Prefer fakes for your own collaborators. Prefer monkeypatch for third-party or stdlib code you do not control.

---

## Coverage

**Test coverage** is a measurement of how many lines (or branches) in your code were executed during a test run. It does not tell you whether your tests are correct — a bad test can achieve 100% coverage. But low coverage reliably reveals untested code paths.

Running coverage in ResearchOps:

```bash
pytest --cov=researchops --cov-report=term-missing -q
```

`--cov=researchops` — measure coverage for the `researchops` package only.
`--cov-report=term-missing` — print a summary showing which line numbers were not covered.

Example output:

```
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------
researchops/core/models.py                 45      2    96%   87, 91
researchops/services/ingestion_service.py  63      0   100%
researchops/ml/topic_classifier.py          4      4     0%   1-4
```

The `0%` on `topic_classifier.py` is expected — that module is a stub for Week 11. The `96%` on `models.py` means lines 87 and 91 are not tested — worth investigating.

The project enforces a minimum coverage threshold in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=researchops --cov-fail-under=70"
```

`--cov-fail-under=70` — pytest exits with a failure code if coverage drops below 70%. This means a PR that deletes tests will fail CI automatically.

---

## Arrange / Act / Assert pattern

Every test has three phases. Making them explicit improves readability.

```python
def test_search_returns_results_in_score_order(
    paper_repo: FakePaperRepository,
) -> None:
    # Arrange — set up the system under test
    paper_repo.save(Paper(id="a", title="NLP", text="neural language model", ...))
    paper_repo.save(Paper(id="b", title="NLP NLP", text="neural neural language", ...))
    service = KeywordSearchService(paper_repo=paper_repo)

    # Act — do the thing being tested
    results = service.search("neural")

    # Assert — verify the outcome
    assert len(results) == 2
    assert results[0].score >= results[1].score
```

The blank lines between sections make the test easy to scan. Avoid mixing Arrange and Assert. Avoid having multiple Act phases. If you need multiple assertions after one Act, that is fine, but if you need two separate Act phases, write two tests.

---

## Test naming

Good test names describe the behavior being tested, not the implementation:

| Bad name | Good name |
|---|---|
| `test_search_1` | `test_search_returns_results_in_score_order` |
| `test_uses_sorted_call` | `test_empty_query_raises_empty_query_error` |
| `test_ingestion_service_ingest_directory` | `test_ingestion_skips_existing_paper` |

The good names are longer. That is intentional. A test name should be a specification: "when X, then Y." When the test fails, the name tells you what behavior broke.

Use classes to group related tests:

```python
class TestIngestDirectory:
    def test_ingests_single_pdf(self, ...) -> None: ...
    def test_ingests_multiple_pdfs(self, ...) -> None: ...
    def test_parse_failure_recorded(self, ...) -> None: ...
```

The class name is the "describe" and each method is an "it":

- Describe `IngestDirectory`
- It `ingests_single_pdf`
- It `records parse failure`

---

## How to test bugs

When you find a bug, write a test that fails because of the bug before you fix the bug. This is called a **regression test**. The steps are:

1. Reproduce the bug minimally — find the smallest input that triggers it.
2. Write a test that captures that input and the expected correct behavior.
3. Run the test. It should fail (because the bug exists).
4. Fix the bug.
5. Run the test. It should now pass.
6. Never delete this test. It protects against the same bug re-appearing.

Example: you discover that `normalise_for_search` crashes on an empty string. The test:

```python
def test_normalise_for_search_handles_empty_string() -> None:
    # This was a bug: empty string caused IndexError in the split
    result = normalise_for_search("")
    assert result == ""
```

This test is named after the behavior, not the bug number. Future maintainers do not need to know the history — the test just says "empty strings should not crash."

---

## Flaky tests

A **flaky test** is a test that sometimes passes and sometimes fails, without any code change. Flaky tests are extremely damaging because they erode trust in the suite. Developers start ignoring failures ("oh, that one is flaky") and miss real regressions.

Common causes:

- **Time dependency**: `datetime.utcnow()` returns different values. Fix: inject a `FixedClock` (see Week 9 stretch exercise).
- **Random seed**: randomness without a fixed seed. Fix: set `random.seed(42)` in the fixture.
- **Ordering dependency**: test A depends on state left by test B. Fix: each test must set up its own state.
- **Network call**: test reaches out to a real URL. Fix: monkeypatch or use a fake.
- **Filesystem state**: test assumes a file exists that a previous test created. Fix: use `tmp_path`.

The rule: every test must be able to run independently, in any order, any number of times.

---

## CI: the quality gate that never sleeps

**CI** (Continuous Integration) means automatically running validation checks on every code change. In ResearchOps, CI is configured in `.github/workflows/ci.yml`.

The workflow runs:

1. `ruff check src tests` — linting: catches syntax errors, unused imports, style issues.
2. `pytest --cov=researchops --cov-report=term-missing -q` — tests and coverage.

Every push and pull request triggers this. If any check fails, the CI is marked red. The rule: never merge a red PR.

CI means that "it works on my machine" is not enough. It must work on a clean, reproducible environment. This prevents a common failure mode where local development environments accumulate quirks that make broken code seem to pass.

The CI commands can be reproduced locally:

```bash
ruff check src tests
pytest --cov=researchops --cov-report=term-missing -q
```

Running these before pushing is a good habit. It means you see CI failures before the push, which is faster.

---

## Linting with Ruff

**Ruff** is a fast Python linter written in Rust. It catches:

- Syntax errors.
- Unused imports (`F401`).
- Undefined names (`F821`).
- Style issues (many PEP 8 rules).
- Complexity issues (function too long, too many branches).

Run it:

```bash
ruff check src tests         # report errors
ruff check src tests --fix   # auto-fix what is fixable
```

Ruff is configured in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP"]
```

`E` — pycodestyle errors (PEP 8 style).
`F` — Pyflakes (unused imports, undefined names).
`W` — pycodestyle warnings.
`I` — isort (import ordering).
`UP` — pyupgrade (modernize Python syntax).

A clean `ruff check src tests` means no violations. This should always be true before committing.

---

## Type checking with mypy (or pyright)

Python is dynamically typed, meaning you can pass anything to any function at runtime. Type annotations are optional hints. A **type checker** reads those hints and reports mismatches statically — without running the code.

```python
def save(self, paper: Paper) -> None: ...
```

If you call `repo.save("not a paper")`, a type checker will flag this as an error even though Python itself would not complain until runtime.

Type checking catches:

- Wrong argument types.
- Missing return values.
- Calling methods that do not exist.
- Protocol violations (a fake that does not satisfy its protocol).

Running mypy:

```bash
mypy src
```

Type checking is not yet enforced in CI for ResearchOps (the codebase is being built progressively), but running it locally teaches you to write more precise code and catches real bugs before they become runtime failures.

---

## Quality gates summary

| Gate | Tool | What it catches | When to run |
|---|---|---|---|
| Linting | `ruff check` | Style, unused imports, syntax | Always before commit |
| Type checking | `mypy src` | Type mismatches, protocol violations | Often locally |
| Unit tests | `pytest tests/unit/` | Service and domain logic bugs | Always before commit |
| Integration tests | `pytest tests/integration/` | Database and file system integration | Before push |
| Coverage threshold | `pytest --cov-fail-under=70` | Untested code | In CI |
| E2E tests | `pytest tests/e2e/` | CLI behavior | Before release |

All of these together form the quality gate. CI automates the most important ones. The others you run locally as needed.

---

## Fixtures in conftest.py

When multiple test files need the same fixtures, put them in `tests/conftest.py`. pytest automatically discovers this file and makes its fixtures available to all tests in the directory tree.

```python
# tests/conftest.py
import pytest
from tests.fakes.fake_repository import FakePaperRepository, FakeFailureRepository

@pytest.fixture()
def paper_repo() -> FakePaperRepository:
    return FakePaperRepository()

@pytest.fixture()
def failure_repo() -> FakeFailureRepository:
    return FakeFailureRepository()
```

Now any test file under `tests/` can use `paper_repo` and `failure_repo` as arguments without importing them.

---

## Summary

Testing discipline is a professional habit. It is not optional for a portfolio-grade project. The rules:

1. Write tests for every feature and every bug fix.
2. Keep unit tests fast and isolated.
3. Use fakes, not real databases, in unit tests.
4. Name tests after behaviors, not implementations.
5. Follow Arrange / Act / Assert.
6. Never delete regression tests.
7. Eliminate flaky tests immediately when you find them.
8. Run `ruff check src tests` and `pytest -q` before every commit.
9. Treat CI failures as blockers — never merge a red pipeline.
10. Let coverage reports guide you toward under-tested code.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 10 — Testing & Quality Gates** · *notes.md — the textbook chapter* (step 2 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [README](./README.md)
- ▶ **Next:** [exercises.md](./exercises.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. **➡ [notes.md](./notes.md) ← you are here**
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
