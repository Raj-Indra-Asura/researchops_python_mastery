<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 10 — Testing and Quality Gates:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 10 Testing Discipline and Quality Gates

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 10: Testing Discipline and Quality Gates

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Tests that give you confidence**.
The practical milestone is: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
The expected capability is: Can write `conftest.py` fixtures, use `monkeypatch`, explain test coverage, and configure a minimum threshold in CI. ---
This chapter is one step in the ResearchOps system, not a random lesson.
The visible feature matters because it proves the idea works.
The hidden skill matters because it lets you build the next chapter without confusion.
A complete pass through this chapter means you can read the code, run it, test it, break it, and explain it aloud.

Use this study order:
- Read the story first without typing.
- Trace the smallest code example.
- Find the project file that owns the behavior.
- Run the validation command.
- Explain one happy path and one failure path.

## What you already know from previous weeks

- Week 6 taught PDF Parsing Pipeline; keep its responsibility in mind, but do not rebuild it here.
- Week 7 taught Keyword Search and Data Quality; keep its responsibility in mind, but do not rebuild it here.
- Week 8 taught Multiprocessing Ingestion; keep its responsibility in mind, but do not rebuild it here.
- Week 9 taught Protocols, Interfaces, and Clean Architecture; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 10 solves the project problem behind **Testing Discipline and Quality Gates**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept ``pytest` fixture scopes: `function`, `module`, `session`` helps solve part of this gap.
- The concept ``tmp_path` for temporary file system fixtures` helps solve part of this gap.
- The concept ``monkeypatch` for environment variables and dependency substitution` helps solve part of this gap.
- The concept ``conftest.py` for shared fixtures` helps solve part of this gap.
- The concept ``pytest-cov` and minimum coverage threshold` helps solve part of this gap.
- The concept `CI failure on coverage regression` helps solve part of this gap.
- The concept `Parametrised tests with `@pytest.mark.parametrize`` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Testing Discipline and Quality Gates**?
- Ask: what is the owner for **Testing Discipline and Quality Gates**?
- Ask: what is the transformation for **Testing Discipline and Quality Gates**?
- Ask: what is the proof for **Testing Discipline and Quality Gates**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| pytest` fixture scopes | `pytest` fixture scopes: `function`, `module`, `session` | This term names one job in the Week 10 milestone. |
| tmp_path` for temporary file system fixtures | `tmp_path` for temporary file system fixtures | This term names one job in the Week 10 milestone. |
| monkeypatch` for environment variables and dependency substitution | `monkeypatch` for environment variables and dependency substitution | This term names one job in the Week 10 milestone. |
| conftest.py` for shared fixtures | `conftest.py` for shared fixtures | This term names one job in the Week 10 milestone. |
| pytest-cov` and minimum coverage threshold | `pytest-cov` and minimum coverage threshold | This term names one job in the Week 10 milestone. |
| CI failure on coverage regression | CI failure on coverage regression | This term names one job in the Week 10 milestone. |
| Parametrised tests with `@pytest.mark.parametrize | Parametrised tests with `@pytest.mark.parametrize` | This term names one job in the Week 10 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: `pytest` fixture scopes: `function`, `module`, `session`
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 10, it supports the milestone: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: `tmp_path` for temporary file system fixtures
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 10, it supports the milestone: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: `monkeypatch` for environment variables and dependency substitution
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 10, it supports the milestone: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: `conftest.py` for shared fixtures
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 10, it supports the milestone: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: `pytest-cov` and minimum coverage threshold
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 10, it supports the milestone: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: CI failure on coverage regression
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 10, it supports the milestone: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 7: Parametrised tests with `@pytest.mark.parametrize`
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 10, it supports the milestone: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `tests/conftest.py` — shared fixtures
- `pyproject.toml` — `fail_under = 70`
- `.github/workflows/ci.yml` — coverage gate
Study those files in this order:
1. Find the user-facing entry point.
2. Find the service or core concept that owns the meaning.
3. Find the infrastructure only when outside resources are needed.
4. Find the tests that prove the behavior.
5. Find the validation command that a learner runs manually.
The goal is to know why each file exists.
If two files seem to own the same decision, stop and clarify the boundary.

## Code examples with line-by-line explanation

```python
import pytest

@pytest.mark.parametrize("query, expected", [("ml", 1), ("missing", 0)])
def test_search_counts_results(search_service, query: str, expected: int) -> None:
    assert len(search_service.search(query)) == expected
```

Line-by-line explanation:
- Line 1: `import pytest` — This imports a tool before the example can use it.
- Line 2: `(blank line)` — This blank line separates ideas so the example is easier to read.
- Line 3: `@pytest.mark.parametrize("query, expected", [("ml", 1), ("missing", 0)])` — This attaches framework or test behavior to the next function or class.
- Line 4: `def test_search_counts_results(search_service, query: str, expected: int) -> None:` — This names a reusable action and shows what information it receives.
- Line 5: `assert len(search_service.search(query)) == expected` — This stores a clear intermediate value for the next step.

How to use this example:
- Name the input.
- Name the output.
- Predict the result before running anything.
- Connect the shape to the real ResearchOps file.
- Write one sentence about why each line belongs.

## Common beginner mistakes

- **Mistake:** Pasting code before knowing the owner of the behavior.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Changing many files at once.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Skipping the failure path.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Reading only the happy path test.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Ignoring the validation command.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Using vague names.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Putting business rules in the user interface layer.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Treating logs, errors, and tests as decoration.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Optimizing before correctness is visible.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Building future-week features early.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.

## Debugging guidance

- Copy the exact failing command.
- Read the first useful error line.
- Read the final error line.
- Classify the failure as import, input, state, file, database, network, model, or expectation.
- Reproduce it with the smallest command.
- Inspect the value closest to the failure.
- Fix the cause, not only the symptom.
- Run the narrowest test.
- Run the chapter validation command.
- Write down what the error was teaching.
Debugging questions:
- What did I expect?
- What happened?
- Which value first became wrong?
- Which layer created that value?
- Which test should catch this next time?

## Design tradeoffs

- **Simple first version:** Easy to understand, but not the final production shape.
- **Clear layers:** More files, but less confusion as features grow.
- **Explicit errors:** More code, but failures become teachable.
- **Small unit tests:** Fast feedback, but less end-to-end confidence.
- **Integration tests:** Real wiring, but slower and more setup.
- **Configuration:** Flexible behavior, but defaults must be clear.
The right question is not "What is the fanciest design?"
The right question is "What design teaches the responsibility clearly and can grow next week?"

## Testing implications

Tests for this chapter:
- Coverage of all service modules ≥ 70%
Validation commands:
```bash
pytest --cov=researchops --cov-report=term-missing -q
ruff check src tests
```
- Arrange the data.
- Act on the system.
- Assert the visible promise.
- Check one failure path.
- Keep unit tests fast.
- Use integration tests only when real wiring matters.

## Architecture implications

ResearchOps stays understandable when dependencies point inward.
```text
CLI / API / Worker -> Services -> Core
Infrastructure implements core-facing contracts and is wired at the outside.
```
- Does the UI layer avoid business logic?
- Does the service layer own workflow decisions?
- Does core avoid infrastructure imports?
- Does infrastructure do outside-world work?
- Do tests use fakes when possible?
Architecture is not ceremony.
Architecture is named responsibility.

## How this connects to AI engineering / ML research

AI engineering needs more than models.
It needs reliable data flow, clear interfaces, repeatable experiments, visible failures, and honest evaluation.
Week 10 contributes by making **testing discipline and quality gates** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 10 solve?
- What is the main input?
- What is the main output?
- Which file owns the main responsibility?
- Which layer should not contain business logic?
- What is one happy path?
- What is one failure path?
- What command proves the chapter works?
- What should you not build early?
- How does this prepare the next week?

## Explain-it-aloud prompts

- Explain Testing Discipline and Quality Gates in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Testing Discipline and Quality Gates.
- The milestone: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
- The main project files.
- The validation command.
- The boundary rule for the layer you are touching.
- The habit of testing before moving forward.

## What to understand deeply

- Why this feature belongs now.
- How data moves through the chapter.
- Which file owns which decision.
- How the failure path is handled.
- Why the tests prove behavior.
- How this week makes future work safer.

## What not to worry about yet

- Perfect scale.
- Fancy abstractions.
- Future-week features.
- Every option in every library.
- Premature optimization.
- Comparing your speed to someone else.
Focus on the milestone.
A clear small milestone beats a confusing large one.

## Bridge to next week

Next week is Week 11: **Classical ML — Topic Classification**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace ``pytest` fixture scopes: `function`, `module`, `session`` from user input to project result.
- Drill 2: Write one sentence defining ``pytest` fixture scopes: `function`, `module`, `session`` without copying the notes.
- Drill 3: Find the file where ``pytest` fixture scopes: `function`, `module`, `session`` appears or should appear.
- Drill 4: Name one wrong implementation of ``pytest` fixture scopes: `function`, `module`, `session`` and why it would hurt.
- Drill 5: Name one test that would protect ``pytest` fixture scopes: `function`, `module`, `session``.
- Drill 6: Trace ``tmp_path` for temporary file system fixtures` from user input to project result.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes

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
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 10 — Testing and Quality Gates:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
