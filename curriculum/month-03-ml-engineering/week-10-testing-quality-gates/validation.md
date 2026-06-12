
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 10 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 10 — Testing and Quality Gates:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 10 Testing Discipline and Quality Gates

## Pre-validation checklist

Before running the Week 10 gate:

- [ ] No intentional break-it changes remain in tests, fixtures, or CI configuration.
- [ ] New tests use `tmp_path`, `monkeypatch`, and fakes where appropriate instead of hard-coded paths or real global state.
- [ ] Test names describe behavior, not implementation trivia.
- [ ] You know which commands are unit, integration, E2E, coverage, and full quality gate checks.


## Commands to run

```bash
# Activate your environment
source .venv/bin/activate
python -m pip install -e ".[dev,parsing,storage]"

# Step 1: Lint — no style or import violations
ruff check src tests

# Step 2: Unit tests — fast, no I/O
pytest tests/unit/ -v

# Step 3: Integration tests — real SQLite
pytest tests/integration/ -v

# Step 4: E2E tests — real CLI
pytest tests/e2e/ -v

# Step 5: Coverage report
pytest --cov=researchops --cov-report=term-missing -q

# Step 6: Full quality gate (mirrors CI exactly)
ruff check src tests && pytest --cov=researchops --cov-report=term-missing -q
```

## Tests that must pass

The quality gate is not optional:

- Unit tests: `pytest tests/unit/ -v`.
- Integration tests: `pytest tests/integration/ -v`.
- E2E smoke tests: `pytest tests/e2e/ -v`.
- Coverage gate: `pytest --cov=researchops --cov-report=term-missing -q`.
- Full gate: `ruff check src tests && pytest --cov=researchops --cov-report=term-missing -q`.

## Expected outputs

- `ruff check src tests` — exits 0, prints nothing.
- `pytest tests/unit/ -v` — all tests pass. No database files created. Takes under 5 seconds.
- `pytest tests/integration/ -v` — all tests pass. May create temporary SQLite files in `tmp_path`.
- `pytest tests/e2e/ -v` — CLI smoke tests pass.
- `pytest --cov=researchops --cov-report=term-missing -q` — overall coverage is at or above the configured threshold. The missing-lines report shows which lines are not covered.

## Manual checks

Inspect the test suite like a maintainer:

- Confirm unit tests do not open SQLite databases or rely on files outside pytest-managed paths.
- Confirm shared fixtures in `tests/conftest.py` are genuinely shared and not hiding important Arrange steps.
- Confirm at least one parametrized test covers multiple input cases without copy-paste.
- Confirm monkeypatch use targets the name looked up by the code under test.

## Verifying the test pyramid

Count tests in each layer:

```bash
pytest tests/unit/ --collect-only -q 2>/dev/null | tail -1
pytest tests/integration/ --collect-only -q 2>/dev/null | tail -1
pytest tests/e2e/ --collect-only -q 2>/dev/null | tail -1
```

Unit tests should outnumber integration tests, which should outnumber E2E tests.

## Verifying test isolation

Unit tests must not create files or database connections:

```bash
ls -la *.db 2>/dev/null  # no .db files should exist in the root
pytest tests/unit/ -v 2>&1 | grep -i "sqlite\|database\|\.db"
# expected: no output
```

## Architecture checks

Testing code must reinforce the architecture instead of bypassing it:

- Service unit tests should inject fakes or simple test doubles through protocol-shaped constructors.
- Integration tests may use real SQLite, but only with isolated pytest-managed paths.
- E2E tests may call the CLI, but they should remain smoke-level and not duplicate every service assertion.
- No test should make `core/` or `services/` depend on concrete infrastructure just to become easier to write.

## Documentation checks

- [ ] Exercises teach fixtures, parametrization, monkeypatching, coverage, and CI as learner actions.
- [ ] Break-it labs include restoration steps after every intentional test failure.
- [ ] Validation explains expected outputs clearly enough for a beginner to distinguish `ERROR`, `FAILED`, lint failure, and coverage failure.
- [ ] Commands use existing project tools only: `pytest`, `ruff`, and `researchops`.

## Do-not-proceed warnings

Do not advance to Week 11 if any of these are true:

- The full gate fails and you cannot explain the first failing command.
- Unit tests create files, databases, or hidden global state.
- Coverage is below the configured threshold.
- A flaky test passes only when run alone or only in a certain order.
- CI commands differ from local validation and nobody has documented why.

## Ruthless mentor checkpoint

Answer these aloud before starting ML code:

1. What is the difference between a pytest error and a pytest failure?
2. Why is a fast unit test more valuable than an integration test for service logic?
3. When should you use `tmp_path`, and when should you use a fake instead?
4. What does coverage tell you, and what can it never prove?

## Definition of done

- [ ] `ruff check src tests` exits 0.
- [ ] `pytest tests/unit/ -q` passes, all tests green.
- [ ] `pytest tests/integration/ -q` passes.
- [ ] `pytest tests/e2e/ -q` passes.
- [ ] Coverage is at or above threshold.
- [ ] At least two parametrized tests exist.
- [ ] At least one monkeypatch test exists.
- [ ] `tests/conftest.py` has shared fixtures.
- [ ] No unit test uses real SQLite (verified by audit).
- [ ] You have written at least one regression test.
- [ ] You can read `.github/workflows/ci.yml` and explain each step.
- [ ] You trust the test suite enough to add ML code next week.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 10 — Testing and Quality Gates:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
