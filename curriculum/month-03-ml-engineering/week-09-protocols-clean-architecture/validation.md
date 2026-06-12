
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 9 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 09 Protocols and Clean Architecture

## Pre-validation checklist

Before running commands, verify the Week 9 work is in a clean learning state:

- [ ] You have read `src/researchops/core/interfaces.py` and can name each protocol.
- [ ] Any scratch protocol, fake, or service experiment has been either promoted intentionally or removed.
- [ ] No service file was left importing `sqlite3`, `researchops.storage`, or concrete parsing adapters.
- [ ] Unit-test examples use fakes from `tests/fakes/` rather than a real database.


## Philosophy

Validation this week is less about running new code and more about proving that the architecture is sound. The key signal is: unit tests pass using only fakes, with no database created.

## Commands to run

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

## Tests that must pass

Week 9 is validated by fast fake-based unit tests plus adapter-level integration tests:

- `pytest tests/unit/ -v` must pass without creating a database file in the repository root.
- `pytest tests/integration/ -v` must pass with real adapters.
- `pytest -q` must pass after both narrow suites are green.
- `mypy src tests` should confirm that fakes and services still match the protocol contracts; if local third-party stubs are missing, document the exact stub issue instead of ignoring real protocol errors.

## Expected outputs

- `ruff check src tests` — exits 0, no errors.
- `mypy src` — exits 0 or reports only known type stubs issues.
- `pytest tests/unit/ -v` — all unit tests pass. No database files created in the project directory.
- `pytest tests/integration/ -v` — all integration tests pass with real SQLite.
- `pytest -q` — full suite passes. Coverage above configured threshold.

## Manual checks

Open these files and inspect them directly:

- `src/researchops/core/interfaces.py`: protocols import only core models and standard-library typing/path helpers.
- `tests/fakes/fake_repository.py`: fake method names and exception behavior match the protocols.
- `src/researchops/services/ingestion_service.py`: constructor arguments are protocols, not concrete repositories or parsers.
- CLI composition files: concrete adapters are wired at the outside edge, not inside services.

## Architecture checks

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

## Documentation checks

- [ ] Notes explain protocols, dependency inversion, and composition roots in beginner language.
- [ ] Exercises include code-reading, implementation, testing, debugging, refactoring, stretch, and brutal practice.
- [ ] Break-it labs tell the learner how to restore each intentional architecture break.
- [ ] Validation commands match the project CLI (`researchops`), pytest, Ruff, and mypy commands used elsewhere in the curriculum.

## Do-not-proceed warnings

Do not advance to Week 10 if any of these are true:

- A service imports `sqlite3`, `researchops.storage`, `researchops.parsing`, or ML libraries directly.
- A fake silently behaves differently from the real adapter for duplicate saves or missing records.
- Unit tests require a real database, real PDF, or network access.
- You cannot explain why changing a protocol method forces fakes, adapters, and services to be rechecked.

## Ruthless mentor checkpoint

Answer these aloud without reading notes:

1. Why is `PaperRepository` in `core/interfaces.py` instead of `storage/sqlite_repository.py`?
2. What exact damage happens if `IngestionService` constructs `SQLiteRepository` itself?
3. What does `@runtime_checkable` check, and what does it not check?
4. Which layer is allowed to wire concrete implementations, and why?

## Definition of done

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
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
