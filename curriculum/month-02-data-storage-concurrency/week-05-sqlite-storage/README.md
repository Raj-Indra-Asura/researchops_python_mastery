<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 05 — SQLite Storage:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 4 Reflection](../../month-01-python-core/week-04-cli-packaging/reflection.md) · ➡️ [Notes →](notes.md)

---
<!-- NAV_END -->

# Week 05 — SQLite Storage Layer

> **Chapter title: "Data that survives a restart."**
> Month 2 begins. This week the system grows a memory.

---

## 1. Week title

Week 5 — SQLite Storage Layer (Month 2, Chapter 1 of 4).

## 2. Story of the week

At the end of Month 1 you had a scanner: `researchops scan ./papers` could *find*
PDFs, but the moment the program exited, it forgot everything. Every run started
from zero. That is fine for a toy, useless for a research tool.

This week you give ResearchOps a place to *remember*. You design a small SQLite
schema, learn to read and write it with Python's built-in `sqlite3`, and — most
importantly — hide all of that SQL behind a **repository** so the rest of the app
never has to know a database exists. By Friday, papers you store survive a
restart.

## 3. What you already know

- From Month 1: the `src/` layout, editable installs, `pathlib`, custom
  exceptions, logging, dataclasses, and pytest.
- The domain model `Paper` from Week 3.
- How to write and run a Typer CLI command.

You do **not** yet know any SQL or databases — that starts now, from zero.

## 4. What this week adds

- A real relational **schema** (`CREATE TABLE`, primary keys, nullable columns).
- The `sqlite3` standard-library API: `connect`, `cursor`, `execute`,
  `fetchall`/`fetchone`.
- **Transactions** via context-managed connections, and WAL journal mode for
  safe writes.
- The **repository pattern**: a `PaperRepository` protocol implemented by a
  concrete `SqlitePaperRepository`.
- Mapping rows back into `Paper` domain objects (not leaking tuples upward).

## 5. Why this week matters

Persistence is the dividing line between a script and an application. Just as
important is *where* the SQL lives: if `SELECT` statements leak into your CLI and
services, Month 3's clean-architecture work becomes a painful untangling. Getting
the repository boundary right now is what lets every later feature — search, ML,
RAG — treat storage as a swappable detail. This is the first concrete instance of
the modular-monolith rule from
[ADR-0001](../../../docs/decisions/0001-modular-monolith.md).

## 6. Learning objectives

By the end of the week you can:

- Design a SQLite schema with sensible keys and nullable columns.
- Use `sqlite3` to execute statements and fetch results.
- Manage connections and transactions with context managers; explain commit vs
  rollback.
- Implement a repository that returns domain objects, not raw rows.
- Explain the difference between a protocol (`PaperRepository`) and its
  implementation (`SqlitePaperRepository`).
- Write integration tests against a real database in `tmp_path`.

## 7. Project milestone

`researchops papers list` shows papers stored in SQLite, and the
`PaperRepository` protocol is implemented by `SqlitePaperRepository`. Data
persists across program restarts.

## 8. Files / modules touched

- `src/researchops/storage/schema.sql` — DDL for all tables.
- `src/researchops/storage/sqlite_repository.py` — `SqlitePaperRepository`.
- `src/researchops/core/interfaces.py` — the `PaperRepository` protocol.
- `tests/integration/test_sqlite_repository.py` — save / retrieve / list.

## 9. Commands introduced

```bash
researchops papers list          # list papers stored in SQLite
```

## 10. Tests involved

- `tests/integration/test_sqlite_repository.py` — round-trips through a **real**
  SQLite database created in `tmp_path` (save, then retrieve, then list).

```bash
pytest tests/integration/test_sqlite_repository.py -v
```

## 11. Study plan for the week

1. **Day 1 — SQL foundations.** Learn `CREATE TABLE`, primary keys, and basic
   `INSERT`/`SELECT` in a throwaway `/tmp` database via the `sqlite3` CLI.
2. **Day 2 — `sqlite3` from Python.** `connect`, `execute`, `fetchone`,
   parameter binding (`?` placeholders, never string formatting).
3. **Day 3 — Schema + repository skeleton.** Write `schema.sql` and the
   `SqlitePaperRepository` save/get/list methods.
4. **Day 4 — Transactions + row mapping.** Context-managed connections, WAL mode,
   and mapping rows back into `Paper`.
5. **Day 5 — Integration tests + milestone.** Test against `tmp_path`, wire
   `papers list`, and write your weekly report.

## 12. Estimated time breakdown

| Activity | Time |
|---|---|
| Reading (README, notes, SQL basics) | ~1.5 hrs |
| Building schema + repository | ~4 hrs |
| Transactions, WAL, row mapping | ~1.5 hrs |
| Integration tests | ~1.5 hrs |
| Break-it + reflection + report | ~1.5 hrs |

## 13. How to know the learner is stuck

- You are concatenating values into SQL strings instead of using `?` parameters.
- Writes seem to "disappear" after the program exits (you never committed).
- Your repository returns raw tuples/rows and the CLI has to index `row[2]`.
- Tests pass but leave a `.db` file in the project root (you used a real path,
  not `tmp_path`).

If any persists more than ~30 minutes, re-read the transaction/repository notes
before pushing on.

## 14. Definition of done

- [ ] A SQLite database is created from `schema.sql`.
- [ ] Tables have clear primary keys and intentional nullable columns.
- [ ] `SqlitePaperRepository` implements the `PaperRepository` protocol.
- [ ] Repository methods return `Paper` objects, not rows.
- [ ] Writes happen inside transactions; a failed write does not partially commit.
- [ ] `researchops papers list` shows persisted papers after a restart.
- [ ] Integration tests pass against a `tmp_path` database.
- [ ] No SQL appears outside `storage/`.

## 15. Ruthless mentor checkpoint

Answer out loud, no notes:

- "Show me the line that prevents SQL injection." (It must be `?` placeholders.)
- "Where does a transaction begin and end in your code, and what happens on an
  exception?"
- "If I deleted `SqlitePaperRepository` and wrote a `PostgresPaperRepository`,
  how many lines of your services would change?" (Answer: zero.)

If you cannot answer all three crisply, you are not done.

## 16. What not to do this week

- Do **not** build SQL strings with f-strings or `+` — always bind parameters.
- Do **not** let `SELECT`/`INSERT` leak into the CLI or any service.
- Do **not** test against your real database file; use `tmp_path`.
- Do **not** reach for SQLAlchemy yet — raw `sqlite3` is the point (see ADR-002
  in [`adr-log.md`](../../../docs/decisions/adr-log.md)).
- Do **not** optimise for speed; correctness and clean boundaries come first.

## 17. Bridge to next week

You can now store and retrieve papers — but you are still storing them *by hand*.
There is no real PDF text in there yet. **Week 6** builds the parsing pipeline:
the scanner discovers files, a parser turns PDF bytes into structured text, and
the `IngestionService` orchestrates `discover → parse → store`, recording
failures instead of dropping them. The schema you designed this week is the
destination that pipeline fills.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 4 Reflection](../../month-01-python-core/week-04-cli-packaging/reflection.md) · ➡️ [Notes →](notes.md)

**Week 05 — SQLite Storage:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
