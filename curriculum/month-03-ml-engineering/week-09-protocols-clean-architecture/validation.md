# Validation - Week 09 Protocols and Clean Architecture

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 9 — Protocols & Clean Architecture](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Philosophy

Validation this week is less about running new code and more about proving that the architecture is sound. The key signal is: unit tests pass using only fakes, with no database created.

## Exact shell commands to run

```bash
# Activate your environment
source .venv/bin/activate
python -m pip install -e ".[dev,parsing,storage]"

# Lint: no infrastructure imports inside core or services
ruff check src tests

# Type check: fakes satisfy protocols, services have correct signatures
mypy src tests

# Unit tests: no SQLite, no PDFs, fast
pytest tests/unit/ -v

# Integration tests: real SQLite, real parsing adapters
pytest tests/integration/ -v

# Full suite
pytest -q
```

## Proof that fakes satisfy protocols

You can verify at a Python REPL that fakes satisfy their protocols:

```python
from researchops.core.interfaces import PaperRepository, DocumentParser, FailureRepository
from tests.fakes.fake_repository import (
    FakePaperRepository, FakeDocumentParser, FakeFailureRepository
)

assert isinstance(FakePaperRepository(), PaperRepository)
assert isinstance(FakeDocumentParser(), DocumentParser)
assert isinstance(FakeFailureRepository(), FailureRepository)
print("All fakes satisfy their protocols.")
```

## Expected outputs

- `ruff check src tests` — exits 0, no errors.
- `mypy src` — exits 0 or reports only known type stubs issues.
- `pytest tests/unit/ -v` — all unit tests pass. No database files created in the project directory.
- `pytest tests/integration/ -v` — all integration tests pass with real SQLite.
- `pytest -q` — full suite passes. Coverage above configured threshold.

## Architecture verification checklist

Verify manually or by script:

```bash
# Services must not import infrastructure
grep -r "import sqlite3\|from researchops.storage\|from researchops.parsing" \
  src/researchops/services/ --include="*.py"
# Expected: no output (zero violations)

# Core must not import infrastructure
grep -r "import sqlite3\|from researchops.storage\|from researchops.parsing\|from researchops.ml" \
  src/researchops/core/ --include="*.py"
# Expected: no output (zero violations)
```

## Completion checklist

- [ ] You have read all six protocols in `interfaces.py` and can explain each in your own words.
- [ ] You can identify the concrete adapter for each protocol.
- [ ] You can identify the fake for each protocol.
- [ ] `FakePaperRepository`, `FakeFailureRepository`, and `FakeDocumentParser` all exist in `tests/fakes/`.
- [ ] At least one unit test file uses only fakes with no database.
- [ ] `pytest tests/unit/ -q` passes with no database files created.
- [ ] `pytest tests/integration/ -q` passes with real adapters.
- [ ] `ruff check src tests` exits clean.
- [ ] You can describe what "composition root" means using `cli/commands/ingest.py` as an example.
- [ ] You can draw the dependency graph for `IngestionService` from memory.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 9 — Protocols & Clean Architecture** · *validation.md — the checkpoint* (step 5 of 6 this week).

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
8. [Next week → Week 10](../../../curriculum/month-03-ml-engineering/week-10-testing-quality-gates/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 10 — Testing & Quality Gates](../../../curriculum/month-03-ml-engineering/week-10-testing-quality-gates/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 9 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
