# Validation - Week 10 Testing Discipline and Quality Gates

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 10 — Testing & Quality Gates](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Exact shell commands to run

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

## Expected outputs

- `ruff check src tests` — exits 0, prints nothing.
- `pytest tests/unit/ -v` — all tests pass. No database files created. Takes under 5 seconds.
- `pytest tests/integration/ -v` — all tests pass. May create temporary SQLite files in `tmp_path`.
- `pytest tests/e2e/ -v` — CLI smoke tests pass.
- `pytest --cov=researchops --cov-report=term-missing -q` — overall coverage is at or above the configured threshold. The missing-lines report shows which lines are not covered.

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

## Completion checklist

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 10 — Testing & Quality Gates** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
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
