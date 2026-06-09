
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 5 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 05 — SQLite Storage:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 05 SQLite Storage Layer

## Pre-validation checklist

Before running the formal checks, confirm every item below.

- [ ] You are in the repository root.
- [ ] Your virtual environment is active.
- [ ] You are using Python 3.11 or newer.
- [ ] The package is installed in editable mode.
- [ ] You have read `src/researchops/storage/schema.sql`.
- [ ] You have read `src/researchops/storage/sqlite_repository.py`.
- [ ] You have read `tests/integration/test_sqlite_repository.py`.
- [ ] You can explain why SQLite stores data after Python exits.
- [ ] You can explain why JSON files are not enough for this milestone.
- [ ] You can identify the `papers` table.
- [ ] You can identify the `paper_tags` table.
- [ ] You can identify the `failed_documents` table.
- [ ] You can explain what `tmp_path` gives to each test.
- [ ] You know this week requires only local SQLite storage, schema design, repository methods, transactions, and integration tests.

---

## Commands to run

Run these commands exactly, from the repository root, when validating Week 5.

```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -c "from pathlib import Path; from researchops.storage.sqlite_repository import SQLitePaperRepository; repo = SQLitePaperRepository(Path('data/week05-validation.db')); print(type(repo).__name__)"
python -c "from pathlib import Path; from researchops.storage.sqlite_repository import SQLitePaperRepository; repo = SQLitePaperRepository(Path('data/week05-validation.db')); print(repo.list_all())"
researchops papers list
pytest tests/integration/test_sqlite_repository.py -v
pytest tests/integration/test_sqlite_repository.py::TestSQLitePaperRepository::test_save_and_get -v
pytest tests/integration/test_sqlite_repository.py::TestSQLitePaperRepository::test_get_raises_when_not_found -v
pytest tests/integration/test_sqlite_repository.py::TestSQLitePaperRepository::test_save_raises_on_duplicate -v
pytest tests/integration/test_sqlite_repository.py::TestSQLitePaperRepository::test_exists -v
pytest tests/integration/test_sqlite_repository.py::TestSQLitePaperRepository::test_list_all -v
pytest tests/integration/test_sqlite_repository.py::TestSQLitePaperRepository::test_delete -v
pytest tests/integration/test_sqlite_repository.py::TestSQLitePaperRepository::test_record_and_list_failures -v
pytest tests/integration/test_sqlite_repository.py::TestSQLitePaperRepository::test_clear_failures -v
pytest -q
ruff check src tests
```

Optional database inspection, if the `sqlite3` shell is already installed:

```bash
sqlite3 data/week05-validation.db ".tables"
sqlite3 data/week05-validation.db "PRAGMA table_info(papers);"
sqlite3 data/week05-validation.db "PRAGMA table_info(failed_documents);"
```

Do not install extra tools just for the optional inspection.
The Python commands and pytest checks are the required validation path.

---

## Expected outputs

### Install command

For:

```bash
python -m pip install -e ".[dev]"
```

Expected result:

- the package installs successfully;
- pytest is available;
- ruff is available;
- there is no dependency resolution failure.

### Repository construction

For:

```bash
python -c "from pathlib import Path; from researchops.storage.sqlite_repository import SQLitePaperRepository; repo = SQLitePaperRepository(Path('data/week05-validation.db')); print(type(repo).__name__)"
```

Expected output:

```text
SQLitePaperRepository
```

Expected side effect:

- `data/week05-validation.db` is created if it did not already exist;
- the repository constructor runs schema initialization;
- SQLite has the Week 5 tables available.

### Empty list check

For:

```bash
python -c "from pathlib import Path; from researchops.storage.sqlite_repository import SQLitePaperRepository; repo = SQLitePaperRepository(Path('data/week05-validation.db')); print(repo.list_all())"
```

Expected output for a fresh validation database:

```text
[]
```

If you previously inserted rows into that file, the output may contain `Paper(...)` objects.
That is acceptable only if you can explain where the rows came from.

### Syllabus CLI smoke command

For:

```bash
researchops papers list
```

Expected Week 5 learning target:

- the command is present;
- it exits without a traceback;
- the intended milestone is listing papers stored in SQLite.

If the current CLI scaffold still prints a friendly not-yet-implemented message, record that as a CLI wiring gap.
Do not confuse that with the repository integration tests below.

### Integration test file

For:

```bash
pytest tests/integration/test_sqlite_repository.py -v
```

Expected result:

- pytest collects `TestSQLitePaperRepository`;
- all tests in the file pass;
- the test database comes from `tmp_path`;
- failures, if any, point to repository behavior rather than shared machine state.

### Full suite and lint

For:

```bash
pytest -q
ruff check src tests
```

Expected result:

- the full current test suite passes;
- ruff reports no unresolved lint errors in `src` or `tests`.

---

## Tests that must pass

These named tests are non-negotiable for Week 5.
They come from `tests/integration/test_sqlite_repository.py`.

### Paper persistence tests

- `TestSQLitePaperRepository::test_save_and_get`
- `TestSQLitePaperRepository::test_get_raises_when_not_found`
- `TestSQLitePaperRepository::test_save_raises_on_duplicate`
- `TestSQLitePaperRepository::test_exists`
- `TestSQLitePaperRepository::test_list_all`
- `TestSQLitePaperRepository::test_delete`

These prove that `papers` rows can be saved, retrieved, listed, checked for existence, rejected when duplicated, and deleted.

### Failure persistence tests

- `TestSQLitePaperRepository::test_record_and_list_failures`
- `TestSQLitePaperRepository::test_clear_failures`

These prove that failed document records survive in SQLite and can be cleared intentionally.

### Why these are integration tests

A fake repository cannot prove:

- `schema.sql` creates valid tables;
- SQL syntax is valid;
- `sqlite3.Row` mapping works;
- `created_at` and `occurred_at` convert correctly;
- unique constraints reject duplicates;
- missing rows become domain-specific exceptions;
- writes are committed.

That is why Week 5 validates against a real temporary database.

---

## Manual checks

Do these even if tests are green.

- [ ] I can point to the `papers` table definition.
- [ ] I can point to the `paper_tags` table definition.
- [ ] I can point to the `failed_documents` table definition.
- [ ] I can explain `TEXT PRIMARY KEY` on `papers.id`.
- [ ] I can explain `UNIQUE` on `papers.source_path`.
- [ ] I can explain `ON DELETE CASCADE` on `paper_tags.paper_id`.
- [ ] I can explain why `failed_documents.id` is autoincrementing.
- [ ] I can point to `SQLitePaperRepository._connect()`.
- [ ] I can explain `conn.row_factory = sqlite3.Row`.
- [ ] I can explain `PRAGMA foreign_keys=ON`.
- [ ] I can explain `PRAGMA journal_mode=WAL`.
- [ ] I can point to `_load_schema()`.
- [ ] I can explain why schema loading uses `executescript()`.
- [ ] I can point to `save()` and identify the placeholders.
- [ ] I can point to `get()` and explain the missing-paper branch.
- [ ] I can point to `list_all()` and explain the return type.
- [ ] I can point to `_row_to_paper()`.
- [ ] I can explain the `datetime.fromisoformat()` conversion.
- [ ] I can point to `record_failure()`.
- [ ] I can explain why `FailedDocument.source_path` is converted with `str()`.
- [ ] I can explain why each test receives a fresh `tmp_path` database.

---

## Architecture checks

Confirm all of these before moving on.

- [ ] `core/models.py` does not import `sqlite3`.
- [ ] `core/exceptions.py` does not import storage implementations.
- [ ] `storage/sqlite_repository.py` owns SQLite details.
- [ ] SQL statements are not scattered through CLI command files.
- [ ] `schema.sql` owns table definitions.
- [ ] Repository methods return domain objects, not raw `sqlite3.Row` objects.
- [ ] Missing paper behavior becomes `PaperNotFoundError`.
- [ ] Duplicate paper behavior becomes `DuplicatePaperError`.
- [ ] Integration tests do not touch a real user database.
- [ ] The Week 5 solution stays local and synchronous.
- [ ] No API server is required for this week.
- [ ] No extra application layer is required for this week.
- [ ] No advanced storage engine is required for this week.

Architecture failure is still failure even if one insert works.
A storage layer that leaks SQL everywhere will make later weeks harder.

---

## Documentation checks

Confirm the curriculum materials match this milestone.

- [ ] `README.md` describes the Week 5 SQLite storage goal.
- [ ] `notes.md` teaches persistence from beginner level.
- [ ] `notes.md` explains schema design.
- [ ] `notes.md` explains repository boundaries.
- [ ] `notes.md` explains transactions.
- [ ] `notes.md` explains integration tests with `tmp_path`.
- [ ] `exercises.md` gives practice with storage code.
- [ ] `break_it.md` gives SQLite failure practice.
- [ ] `validation.md` names `tests/integration/test_sqlite_repository.py`.
- [ ] The chapter avoids future-week topics as required.
- [ ] You can connect every validation command to a concept in the notes.

---

## Do-not-proceed warnings

Do not move forward if any of these are true.

- [ ] You cannot explain why RAM is temporary.
- [ ] You think SQLite requires a separate server process.
- [ ] You cannot explain table, row, and column.
- [ ] You cannot explain primary keys.
- [ ] You cannot explain unique constraints.
- [ ] You cannot explain nullable columns.
- [ ] You cannot explain parameterized queries.
- [ ] You cannot explain commit and rollback.
- [ ] You cannot explain why `tmp_path` is used.
- [ ] You cannot identify the duplicate-save test.
- [ ] You cannot identify the missing-paper test.
- [ ] You cannot trace `repo.save(paper)` into the database.
- [ ] You cannot trace `repo.get("paper1")` back into a `Paper` object.
- [ ] You weakened a schema constraint only to make a test pass.
- [ ] You skipped the failure-record tests because the paper tests passed.

If any warning applies, revisit the notes, exercises, and break-it labs.
Passing commands without understanding them is not enough.

---

## Ruthless mentor checkpoint

Answer these without opening the code if possible.

1. Why is SQLite a good Week 5 storage choice?
2. What file defines the database schema?
3. What table stores successful papers?
4. What table stores failed documents?
5. Why is `papers.id` a primary key?
6. Why is `papers.source_path` unique?
7. Why are tags stored in `paper_tags`?
8. What does `conn.row_factory = sqlite3.Row` change?
9. Why does `_load_schema()` use `executescript()`?
10. Why does `save()` use `?` placeholders?
11. What exception should `get()` raise for an unknown id?
12. What test proves duplicate saves fail?
13. What test proves failures can be listed?
14. Why does each integration test use `tmp_path / "test.db"`?
15. What is commit?
16. What is rollback?
17. Why should CLI code not contain raw `INSERT INTO papers` SQL?
18. Which method maps a row back into a `Paper`?
19. Which field uses `datetime.fromisoformat()`?
20. What future topics should stay out of Week 5?

If you cannot answer at least 16 of 20 clearly, review before advancing.

---

## Definition of done

Week 5 is complete only when all of these are true.

- [ ] Editable install works.
- [ ] `SQLitePaperRepository` imports successfully.
- [ ] Constructing the repository initializes the schema.
- [ ] `schema.sql` contains `papers`.
- [ ] `schema.sql` contains `paper_tags`.
- [ ] `schema.sql` contains `failed_documents`.
- [ ] `papers.id` is a primary key.
- [ ] `papers.source_path` is unique.
- [ ] `paper_tags.paper_id` references `papers(id)`.
- [ ] Repository writes use parameterized SQL.
- [ ] Repository reads map rows to domain objects.
- [ ] Missing papers raise `PaperNotFoundError`.
- [ ] Duplicate papers raise `DuplicatePaperError`.
- [ ] Failure records can be saved.
- [ ] Failure records can be listed.
- [ ] Failure records can be cleared.
- [ ] Integration tests use `tmp_path`.
- [ ] `pytest tests/integration/test_sqlite_repository.py -v` passes.
- [ ] `pytest -q` passes.
- [ ] `ruff check src tests` passes.
- [ ] You understand `researchops papers list` as the syllabus smoke command.
- [ ] You can explain object → row → disk → row → object.
- [ ] You can explain why the repository pattern protects the rest of the app from SQL details.
- [ ] You completed the reflection prompts honestly.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 05 — SQLite Storage:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
