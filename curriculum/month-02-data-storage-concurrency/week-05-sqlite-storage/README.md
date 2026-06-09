# Week 05 - SQLite Storage Layer

## Learning objectives
- Understand relational tables, primary keys, and foreign keys.
- Design a first SQLite schema for papers and parsed documents.
- Use transactions to keep writes consistent.
- Implement a repository layer that hides raw SQL from the CLI.
- Distinguish between connection management and domain logic.
- Read rows from SQLite and map them back into domain objects.
- Write tests around persistence behavior.

## Project milestone
Persist ingested paper metadata and parsed text in SQLite through a small repository layer.

## Files to modify/create
- `src/researchops/storage/schema.py`
- `src/researchops/storage/sqlite.py`
- `src/researchops/storage/repository.py`
- `tests/unit/test_sqlite_repository.py`
- `tests/integration/test_storage_roundtrip.py`

## Concepts covered
SQLite, DDL, DML, transactions, commits, rollbacks, repository pattern, row mapping, and persistence testing.

## Expected deliverables
- A schema creation function.
- Repository methods for insert and query operations.
- Integration tests that write to a temporary database and read data back.
- CLI-ready storage code that other layers can call.

## Definition of done
- [ ] SQLite file can be initialized from code.
- [ ] Tables have clear keys and constraints.
- [ ] Repository methods return domain models.
- [ ] Writes happen inside transactions.
- [ ] Failed writes do not partially commit.
- [ ] Tests cover insert and fetch flows.
- [ ] Storage code is not mixed into CLI handlers.
- [ ] Schema is documented in comments or notes.
