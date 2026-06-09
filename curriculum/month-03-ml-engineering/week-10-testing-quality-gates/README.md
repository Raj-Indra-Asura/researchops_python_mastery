# Week 10 - Testing Discipline and Quality Gates

## Learning objectives
- Organize tests by unit, integration, and end-to-end scope.
- Use fixtures, parametrization, and monkeypatching in pytest.
- Add coverage measurement and minimum thresholds.
- Treat CI as an automated quality gate, not just a badge.
- Write tests that document behavior rather than implementation trivia.
- Fail fast on lint, type, and test regressions.
- Build confidence for later ML and API features.

## Project milestone
Establish reliable quality gates: pytest structure, coverage, linting, and CI checks that protect the ResearchOps codebase.

## Files to modify/create
- `tests/conftest.py`
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/unit/test_*.py`
- `tests/integration/test_*.py`

## Concepts covered
Pytest fixtures, monkeypatch, coverage, CI pipelines, regression testing, and disciplined feedback loops.

## Expected deliverables
- A reusable test fixture setup.
- Coverage reporting integrated into local runs or CI.
- CI workflow that runs lint, type checks, and tests.
- Tests for at least one failure mode using monkeypatching.

## Definition of done
- [ ] Fixtures reduce duplication.
- [ ] Monkeypatch is used intentionally.
- [ ] Coverage command works.
- [ ] CI workflow runs the key checks.
- [ ] Quality gates fail on regressions.
- [ ] Test scope is clear by directory.
- [ ] You can explain what each gate protects.
