# Exercises — Week 05 SQLite Storage Layer

These exercises build from easy to brutal.
Complete them in order.
The later exercises build on the earlier ones.

---

## Easy exercises

### E1 — First SQLite connection

Open a Python REPL or script.
Import `sqlite3`.
Connect to an in-memory database with `sqlite3.connect(":memory:")`.
Run `conn.execute("SELECT sqlite_version()")`.
Print the result.
This verifies that the `sqlite3` module is working.

### E2 — Create a table and insert a row

Using a `:memory:` connection:
1. Create a table called `animals` with columns `name TEXT PRIMARY KEY` and `legs INTEGER NOT NULL`.
2. Insert a row for `("cat", 4)`.
3. Insert a row for `("spider", 8)`.
4. Run `SELECT * FROM animals` and print every row.

### E3 — Access columns by name

Repeat E2 but set `conn.row_factory = sqlite3.Row` before creating the table.
After selecting all rows, access each column by name: `row["name"]` and `row["legs"]`.
Print a sentence like `"A cat has 4 legs."` for each row.

### E4 — The transaction rollback

Using a `:memory:` connection:
1. Create a table `log_entries (id INTEGER PRIMARY KEY AUTOINCREMENT, msg TEXT NOT NULL)`.
2. Start a transaction manually with `conn.execute("BEGIN")`.
3. Insert two rows.
4. Call `conn.rollback()`.
5. Query the table. Assert it is empty.
6. Now insert two rows again, this time call `conn.commit()`.
7. Query the table. Assert it has two rows.

### E5 — Parameterized queries

Create a table `books (title TEXT, year INTEGER)`.
Insert 3 books using parameterized queries (no f-strings or string concatenation).
Then query books published after 2000.

### E6 — Unique constraint

Create a table `users (username TEXT PRIMARY KEY, email TEXT NOT NULL)`.
Insert a user.
Try to insert another user with the same `username`.
Catch the `sqlite3.IntegrityError` that is raised.
Print a helpful message.

---

## Medium exercises

### M1 — Implement `save` and `get`

Write a class `SimpleRepository` that wraps a `sqlite3.Connection`.
It should:
- Accept a connection in its `__init__`.
- Have a `save(paper)` method that inserts a `Paper` into a `papers` table you define.
- Have a `get(paper_id)` method that returns a `Paper` or raises `PaperNotFoundError`.

Write a test that saves a paper and gets it back.
Assert all fields match.

### M2 — The round-trip datetime test

When you save a `Paper`, you convert `created_at` to an ISO string.
When you load it back, you convert the string back to a `datetime`.

Write a test that:
1. Creates a `Paper` with a specific `created_at` (e.g., `datetime(2024, 3, 15, 10, 30, 0)`).
2. Saves it.
3. Loads it.
4. Asserts `loaded.created_at == original.created_at`.

If this test fails, you have a timezone or precision bug.

### M3 — Implement `list_all`

Add a `list_all()` method to your repository.
Write a test that:
1. Saves 5 papers with different `created_at` timestamps.
2. Calls `list_all()`.
3. Asserts the result is ordered newest first.
4. Asserts all 5 papers are returned.

### M4 — Implement `exists`

Add an `exists(paper_id)` method.
Write tests for:
- A paper that exists returns `True`.
- A paper that does not exist returns `False`.

### M5 — Implement `record_failure` and `list_failures`

Add failure recording to your repository.
Create the `failed_documents` table.
Implement `record_failure(failure)` and `list_failures()`.
Write a test that:
1. Records 3 failures.
2. Calls `list_failures()`.
3. Asserts all 3 are returned with correct fields.

### M6 — The source_path uniqueness constraint

Add a `UNIQUE` constraint on `source_path` in your `papers` table.
Write a test that:
1. Saves a paper with a given source path.
2. Attempts to save a different paper (different `id`) with the same source path.
3. Asserts the second save raises an integrity error.

---

## Hard exercises

### H1 — Use `tmp_path` fixtures for all tests

Refactor all your storage tests to use pytest's `tmp_path` fixture.
Create a `repo` fixture that returns a real `SQLitePaperRepository` backed by `tmp_path / "test.db"`.
Every test should use this fixture.
Verify that each test gets a fresh database by asserting `list_all()` returns empty at the start of each test.

### H2 — Isolation between tests

Add a second test that also calls `repo.save(paper)` with the same paper `id` as another test.
Confirm neither test affects the other.
Explain in a comment why this works (hint: each `repo` fixture call creates a new directory).

### H3 — Multi-table transaction

Extend your schema with a `paper_tags` table:
```sql
CREATE TABLE IF NOT EXISTS paper_tags (
    paper_id TEXT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    tag      TEXT NOT NULL,
    PRIMARY KEY (paper_id, tag)
);
```

Write a `save_with_tags(paper)` method that:
1. Inserts the paper.
2. Inserts all tags in the same transaction.

Write a test that:
1. Saves a paper with 3 tags.
2. Queries `paper_tags` directly.
3. Asserts 3 rows exist with the correct `paper_id` and tag values.

Then write a test that:
1. Forces the tags insert to fail (by passing a tag that violates some constraint you add).
2. Asserts the paper was also NOT inserted (rollback worked).

### H4 — Schema migration simulation

Add a new column `doi TEXT` to the `papers` table.
Because the table already exists with `IF NOT EXISTS`, your schema creation function will not add the new column.
Implement a `migrate(conn)` function that:
1. Checks if the `doi` column already exists (hint: `PRAGMA table_info(papers)`).
2. If it does not exist, runs `ALTER TABLE papers ADD COLUMN doi TEXT`.
3. Is safe to run multiple times without error.

Write tests that confirm:
- Running `migrate()` once adds the column.
- Running `migrate()` twice does not crash.

### H5 — Implement `delete` with cascade

Add a `delete(paper_id)` method.
Write a test that:
1. Saves a paper with 3 tags.
2. Calls `delete(paper.id)`.
3. Asserts the paper no longer exists.
4. Queries `paper_tags` directly and asserts no rows exist for that `paper_id`.
   (This proves `ON DELETE CASCADE` is working.)

---

## Brutal exercises

### B1 — Full integration test suite

Write a test file `tests/integration/test_storage_roundtrip.py` that covers:
- Save and get round-trip for every field in `Paper`.
- Save and list_all returns correct count and order.
- Duplicate paper_id raises `DuplicatePaperError`.
- Duplicate source_path raises an integrity error.
- `exists()` returns correct boolean.
- Record and list failures.
- Delete removes paper and cascades to tags.
- All tests are isolated (no shared state).

This file should have at least 15 tests.

### B2 — Repository protocol conformance

The `core/interfaces.py` file defines `PaperRepository` as a Protocol.
Write a test that:
1. Imports `isinstance` and `PaperRepository` from interfaces.
2. Asserts `isinstance(repo, PaperRepository)` is `True` for your `SQLitePaperRepository`.
   (This works because `PaperRepository` is `@runtime_checkable`.)
3. Adds a dummy class that is missing the `delete` method.
4. Asserts `isinstance(dummy, PaperRepository)` is `False`.

This test verifies your concrete class satisfies the interface.

### B3 — Concurrent writes test

Write a test that:
1. Starts 5 threads.
2. Each thread saves a different paper to the same database.
3. Waits for all threads.
4. Calls `list_all()` and asserts all 5 papers are present.

This tests whether your connection management is thread-safe.
(Note: SQLite in WAL mode handles this, but you must use one connection per thread.)

Discuss in a comment: what goes wrong if multiple threads share one connection?

### B4 — Benchmark: batch insert performance

Write a script (not a test) that:
1. Creates a repository backed by a temp database.
2. Saves 1000 papers one at a time.
3. Times the total duration.
4. Then creates a fresh repository and saves the same 1000 papers inside one transaction.
5. Prints both durations.

You should observe a significant speedup with a single transaction.
Explain in a comment why this happens.

---

## Written explanation exercises

### W1 — Explain the repository pattern

Write a one-paragraph explanation of the repository pattern.
Write it as if explaining to someone who has just finished Week 4 and has never seen a database.
Focus on: what problem does it solve, what goes inside, what goes outside.

### W2 — Explain a transaction

Write a narrative story (3-5 sentences) that uses a non-computer metaphor to explain what a transaction is.
The story should make clear what commit and rollback mean.

### W3 — Explain primary key vs unique

Write two sentences:
- One explaining what PRIMARY KEY guarantees.
- One explaining what adds UNIQUE adds that PRIMARY KEY does not cover (hint: you can have many UNIQUE columns but only one PRIMARY KEY).

---

## Testing exercises

### T1 — Test that `_row_to_paper` handles NULL optional fields

Create a row where `author` and `abstract` are `NULL`.
Pass it to `_row_to_paper`.
Assert the resulting `Paper` has `author=None` and `abstract=None`.

### T2 — Test failure listing order

Record 3 failures with different `occurred_at` values.
Assert `list_failures()` returns them newest first.

### T3 — Test the schema is idempotent

Call `_init_schema()` three times on the same database.
Assert no exception is raised.
Assert the database has the expected tables.

---

## Debugging exercises

### D1 — Find the bug

The following code has a bug.
Find it and explain what goes wrong.

```python
def save_paper(paper):
    conn = sqlite3.connect("researchops.db")
    conn.execute(
        "INSERT INTO papers (id, title) VALUES (?, ?)",
        (paper.id, paper.title),
    )
    conn.close()
```

### D2 — Find the SQL injection

The following code is dangerous.
Identify the injection vector and rewrite it safely.

```python
def search_by_title(conn, search_term):
    query = f"SELECT * FROM papers WHERE title LIKE '%{search_term}%'"
    return conn.execute(query).fetchall()
```

### D3 — Diagnose the transaction bug

The following function sometimes leaves the database in an inconsistent state.
Identify why and fix it.

```python
def save_paper_and_failure(paper, failure, conn):
    conn.execute("INSERT INTO papers (...) VALUES (...)", (...))
    conn.commit()  # <-- early commit
    conn.execute("INSERT INTO failed_documents (...) VALUES (...)", (...))
    conn.commit()
```

---

## Mini project task

### P1 — Storage layer milestone

Complete the storage layer for ResearchOps:

1. Create `src/researchops/storage/schema.sql` with all three tables.
2. Implement `SQLitePaperRepository` with: `save`, `get`, `list_all`, `exists`, `delete`, `record_failure`, `list_failures`.
3. Write `tests/integration/test_storage_roundtrip.py` with at least 10 integration tests.
4. Run `pytest -k storage` and confirm all tests pass.
5. Run `ruff check src tests` and confirm no lint errors.
6. Open the created database with the `sqlite3` CLI and inspect the tables directly.

Deliverable: a working storage layer with a full integration test suite.
