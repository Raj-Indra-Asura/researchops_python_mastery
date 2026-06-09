# Notes - Week 10 Testing Discipline and Quality Gates

As software grows, manual checking stops being enough. You need repeatable signals that tell you whether a change preserved behavior. That is what tests and quality gates provide. A quality gate is any automated check that must pass before you trust a change: unit tests, integration tests, coverage thresholds, linting, type checking, or CI workflows.

Pytest is powerful because it scales from tiny function tests to integration suites. A fixture is reusable setup code provided to tests as an argument.

```python
import pytest


@pytest.fixture
def sample_query() -> str:
    return "semantic search"


def test_normalize_query(sample_query: str) -> None:
    assert normalize_text(sample_query) == "semantic search"
```

Fixtures reduce duplication and make setup more readable. They can create temporary directories, fake repositories, seeded databases, or sample documents.

Parametrization is helpful when the same behavior should hold for multiple inputs.

```python
@pytest.mark.parametrize(
    ("query", "expected"),
    [("ML", "ml"), ("  AI ", "ai")],
)
def test_normalize_text(query: str, expected: str) -> None:
    assert normalize_text(query) == expected
```

`monkeypatch` is a pytest fixture that temporarily changes attributes, environment variables, or functions. It is useful when you need to simulate failure paths without changing production code.

```python
def test_parser_failure(monkeypatch):
    monkeypatch.setattr("researchops.parsing.pdf_parser.extract_text", lambda _: "")
    ...
```

Coverage tells you which lines executed during tests. High coverage does not guarantee correctness, but low coverage often reveals blind spots. This project already has coverage configuration in `pyproject.toml`, including a minimum threshold. A threshold is not a badge of honor; it is a pressure mechanism reminding you to add tests alongside features.

CI turns these checks into a shared rule. A simple GitHub Actions workflow might:
1. install dependencies
2. run Ruff
3. run MyPy
4. run pytest with coverage

That means every push or pull request gets the same validation, which reduces "works on my machine" problems.

Test scope matters. Unit tests should be fast and isolate one behavior. Integration tests should cover boundaries like SQLite or PDF parsing. End-to-end tests should exercise real commands or user flows. Mixing them carelessly makes the suite harder to reason about.

A good test names a behavior, not an implementation detail. Prefer `test_search_returns_results_in_score_order` over `test_uses_sorted_call`. The first survives refactors better.

This week is really about discipline. Quality gates protect future you. They make it safe to refactor architecture, add ML models, or expose APIs because regressions are caught close to the change. The codebase becomes a place where you can move quickly without gambling every time you edit a file.
