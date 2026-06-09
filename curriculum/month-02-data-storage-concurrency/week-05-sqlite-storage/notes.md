<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 05 — SQLite Storage:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 05 Notes — SQLite Storage Layer

## 1. Chapter overview

Welcome to Month 2.

In Month 1 you built a CLI scanner that finds PDF files and turns them into typed domain models.
You have `Paper`, `ParsedDocument`, `FailedDocument`, and `IngestionResult`.
You can run the scanner and see results printed to the terminal.

There is one large problem: the moment the program exits, everything disappears.

Nothing is saved.
Run the same command twice and you get the same output twice.
There is no history.
There is no record.
There is no way to ask "what papers have I already processed?"

That problem has a name: persistence.

This week you solve it.
You will learn what a database is, how SQLite works, how to design a schema for your domain models, and how to write clean Python code that saves and retrieves data reliably.

By the end of this week, ResearchOps will have a permanent memory.

---

## 2. What you already know

You know how to define dataclasses with typed fields.
You know how to use `pathlib.Path` for file operations.
You know how to raise and catch exceptions.
You know that your domain models `Paper`, `ParsedDocument`, and `FailedDocument` hold real data.
You know how to write tests with pytest.

All of that stays active.
This week adds one new layer on top: a place to put data that survives program restarts.

---

## 3. The fundamental problem: memory is temporary

When Python runs a program, variables live in RAM.
RAM is fast but temporary.
When the process ends, RAM is released back to the operating system.
Every variable, every list, every dictionary disappears.

This is not a bug.
This is how computers work by design.
It means programs need an explicit way to save data that should outlast a single run.

There are many ways to do this.
You could write to a text file.
You could write JSON.
You could write CSV.
These all work for simple cases.

But text files have limits.
They do not enforce structure.
They do not check that required fields are present.
They do not prevent duplicate entries.
They make queries hard.
Imagine trying to find all papers with more than 5000 words in a CSV file.
You would have to load the entire file, parse every row, and filter manually.

A relational database solves all of these problems.
It enforces structure.
It prevents duplicates when you ask it to.
It answers queries efficiently.
It handles concurrent access.
It protects writes with transactions.

---

## 4. What is a database?

A database is an organized, persistent store of structured data.

That definition has three important parts.

**Organized** means the data has a defined shape.
You do not dump arbitrary text.
You define tables, columns, and types.
Every row in a table has the same column structure.

**Persistent** means the data survives process restarts.
It lives on disk, not in RAM.
You can stop the program, start it again, and the data is still there.

**Structured** means there are rules.
A column declared as `INTEGER` will not accept arbitrary strings.
A column declared as `NOT NULL` will not accept empty values.
A `PRIMARY KEY` constraint prevents two rows with the same identifier.

When people say "database," they usually mean a **relational database**.
Relational databases organize data into tables that can be linked to each other through shared keys.
SQL (Structured Query Language) is the language used to talk to relational databases.

---

## 5. What is SQLite?

SQLite is a relational database that stores everything in a single file.

Most databases (like PostgreSQL or MySQL) run as a separate server process.
You install the server, start it, connect to it over a network socket, and send queries.
That setup has many moving parts.

SQLite is different.
There is no server.
There is no network socket.
The entire database is one file, such as `researchops.db`.
Your Python program reads and writes that file directly.

SQLite is not a toy.
It is one of the most widely deployed software libraries in the world.
It powers most mobile apps, many browsers, and countless embedded systems.
NASA uses SQLite.
Apple uses SQLite.
Firefox uses SQLite.

For local applications like ResearchOps, SQLite is an excellent default choice.

**Why SQLite is good for learning:**

- No installation beyond Python itself (the `sqlite3` module is in the standard library).
- The database is a single visible file you can inspect, copy, delete, and version.
- The same SQL concepts you learn here transfer to PostgreSQL, MySQL, and every other relational database.
- You can use the `sqlite3` command-line tool to explore your data directly.
- It is fast enough for thousands of papers without tuning.

---

## 6. Core vocabulary

### Table

A table is a collection of rows that all have the same structure.
Think of it as a spreadsheet where the column headers are fixed.

ResearchOps has a `papers` table.
Every row in `papers` represents one research paper.

### Row

A row is one record in a table.
One row in `papers` is one paper.
One row in `failed_documents` is one failure event.

### Column

A column is one named field in a table.
Every row has a value for each column.
In `papers`, the columns include `id`, `title`, `source_path`, `text`, `num_pages`, and so on.

### Schema

A schema is the full definition of what a database contains.
It lists all tables and for each table it lists all columns with their types and constraints.
You create a schema once, and then use it forever after.

### Primary key

A primary key is a column (or combination of columns) whose value uniquely identifies each row.
No two rows in a table can have the same primary key.

In `papers`, the `id` column is the primary key.
That `id` is a short SHA-256 hash of the file path, computed in Python (see `PaperId.from_path`).

### Foreign key

A foreign key is a column in one table that refers to the primary key of another table.
It creates a link between tables.

In ResearchOps, `parsed_documents.paper_id` is a foreign key that references `papers.id`.
This says: every parsed document belongs to a paper.
If you try to insert a `parsed_documents` row with a `paper_id` that does not exist in `papers`, SQLite will reject it when foreign key enforcement is enabled.

Foreign keys enforce referential integrity.
They prevent orphan records (a parsed document with no matching paper).

### SQL

SQL stands for Structured Query Language.
It is the standard language for working with relational databases.
SQL has several categories of statements:

**DDL (Data Definition Language)**: creates and modifies table structure.
- `CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`

**DML (Data Manipulation Language)**: inserts, updates, and deletes rows.
- `INSERT`, `UPDATE`, `DELETE`

**DQL (Data Query Language)**: reads data.
- `SELECT`

### Transaction

A transaction is a unit of work that either fully succeeds or fully fails.

Imagine you need to write to two tables at once.
You insert a paper, then insert its parsed document.
What if the second insert fails after the first one succeeds?
Now you have a paper with no document — an inconsistent state.

A transaction prevents this.
Inside a transaction, you can do multiple writes.
If everything succeeds, you **commit** the transaction and the changes become permanent.
If anything fails, you **roll back** the transaction and every change made inside it is undone.

### Commit

A commit finalizes a transaction.
After a commit, the changes are permanent on disk.

### Rollback

A rollback cancels a transaction.
All changes made since the transaction started are undone as if they never happened.

### Connection

A connection is an active session between your Python code and the SQLite database file.
You open a connection, do your work, and close it.

### Parameterized query

A parameterized query is a SQL statement where values are passed separately from the query text.
Instead of building SQL with string concatenation or f-strings, you write placeholders and pass values as a tuple.

This is important for two reasons:
1. It prevents SQL injection attacks.
2. It avoids quoting bugs.

---

## 7. Designing the ResearchOps schema

Before writing any code, think about what data you need to store.

You have these domain models from Week 3:

**`Paper`**: id, title, source_path, text, num_pages, file_size_bytes, created_at, author, abstract, tags

**`ParsedDocument`**: source_path, raw_text, num_pages, file_size_bytes, metadata

**`FailedDocument`**: source_path, error_message, error_type, occurred_at

**`IngestionResult`**: run_id, directory, started_at, finished_at, successes, failures, skipped

Not every model maps 1-to-1 to a table.
`ParsedDocument` is an intermediate processing object, not something that needs permanent storage.
Once it becomes a `Paper`, the raw parsing artifact is no longer needed.
`IngestionResult` is a summary view — you can reconstruct it from the other tables.

So your core tables are:
- `papers` — one row per successfully ingested paper
- `failed_documents` — one row per failed ingestion attempt
- `paper_tags` — one row per paper-tag pair (because a paper can have multiple tags)

### The papers table

```sql
CREATE TABLE IF NOT EXISTS papers (
    id           TEXT    PRIMARY KEY,
    title        TEXT    NOT NULL,
    source_path  TEXT    NOT NULL UNIQUE,
    text         TEXT    NOT NULL,
    num_pages    INTEGER NOT NULL,
    file_size_bytes INTEGER NOT NULL,
    author       TEXT,
    abstract     TEXT,
    created_at   TEXT    NOT NULL
);
```

Let us go through every line.

`CREATE TABLE IF NOT EXISTS papers (` — This statement creates a table named `papers`.
The `IF NOT EXISTS` clause is important.
Without it, running the schema creation twice would throw an error saying the table already exists.
With it, the statement is idempotent: safe to run multiple times.

`id  TEXT  PRIMARY KEY,` — This column holds the paper's unique identifier.
The type is `TEXT` because our identifiers are hex strings like `"a3f2c9d1b8e47f02"`.
`PRIMARY KEY` tells SQLite that this column uniquely identifies each row and cannot be NULL.
SQLite will reject any `INSERT` that tries to use an `id` already in the table.

`title  TEXT  NOT NULL,` — Every paper must have a title.
`NOT NULL` means SQLite will reject any `INSERT` that omits this value or passes `NULL`.

`source_path  TEXT  NOT NULL  UNIQUE,` — Every paper comes from exactly one file path.
`NOT NULL` ensures the path is always present.
`UNIQUE` ensures you cannot store two different papers from the same file.
If you try to ingest the same PDF twice, this constraint will reject the second attempt.

`text  TEXT  NOT NULL,` — The extracted text must be present.
If a PDF cannot yield text, it goes to `failed_documents` instead.

`num_pages  INTEGER  NOT NULL,` — Page count is a number, so we use `INTEGER`.
SQLite stores small integers very efficiently.

`file_size_bytes  INTEGER  NOT NULL,` — File size is also an integer.

`author  TEXT,` — No `NOT NULL` here.
Author extraction is best-effort.
Many PDFs do not embed clean author metadata.
NULL is valid for optional columns.

`abstract  TEXT,` — Same reasoning as author.

`created_at  TEXT  NOT NULL` — SQLite does not have a native `DATETIME` type.
The standard practice is to store ISO 8601 timestamp strings like `"2024-03-15T10:30:00"`.
Python's `datetime.isoformat()` produces exactly this format.

### The failed_documents table

```sql
CREATE TABLE IF NOT EXISTS failed_documents (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_path TEXT    NOT NULL,
    error_message TEXT  NOT NULL,
    error_type  TEXT    NOT NULL,
    occurred_at TEXT    NOT NULL
);
```

`id  INTEGER  PRIMARY KEY  AUTOINCREMENT` — A failure record does not have a natural unique key the way a paper does.
We use an auto-incrementing integer as the surrogate primary key.
SQLite assigns the next available integer automatically when you insert a row.

`source_path` can repeat here.
If you try to ingest the same broken PDF three times, you get three failure records.
This is useful for debugging.

### The paper_tags table

```sql
CREATE TABLE IF NOT EXISTS paper_tags (
    paper_id  TEXT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    tag       TEXT NOT NULL,
    PRIMARY KEY (paper_id, tag)
);
```

A paper can have zero or many tags.
Storing tags as a comma-separated list inside the `papers` table would make querying impossible.
Instead, each paper-tag pair gets its own row.

`REFERENCES papers(id)` is a foreign key declaration.
It says `paper_id` must match an existing `id` in the `papers` table.

`ON DELETE CASCADE` means if a paper is deleted from `papers`, all its tags are automatically deleted too.
Without this, deleting a paper would leave orphan rows in `paper_tags`.

`PRIMARY KEY (paper_id, tag)` is a composite primary key.
This prevents adding the same tag to the same paper twice.

---

## 8. Connecting to SQLite in Python

Python ships with the `sqlite3` module.
No extra installation needed.

```python
import sqlite3
from pathlib import Path


def open_connection(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn
```

Line by line:

`conn = sqlite3.connect(str(db_path))` — Opens the database file at the given path.
If the file does not exist, SQLite creates it.
`str(db_path)` converts the `Path` object to a string because the `sqlite3` module expects a string.
You could also pass `":memory:"` instead of a file path to get an in-memory database that disappears when the connection closes — useful for tests.

`conn.row_factory = sqlite3.Row` — Without this, `fetchone()` and `fetchall()` return plain tuples.
With this setting, they return `Row` objects that support both index and name access.
Instead of `row[2]`, you can write `row["title"]`.
This makes mapping rows back to domain objects much cleaner and less fragile.

`conn.execute("PRAGMA foreign_keys = ON")` — By default, SQLite does not enforce foreign key constraints.
You must enable them explicitly with this PRAGMA statement.
Always do this.
Without it, you can insert a `paper_tags` row pointing to a non-existent `paper_id` and SQLite will silently allow it.

`conn.execute("PRAGMA journal_mode = WAL")` — WAL stands for Write-Ahead Logging.
It is SQLite's most reliable journaling mode for concurrent access.
In WAL mode, readers do not block writers and writers do not block readers.
This matters when multiple processes or threads might access the database at the same time (which you will do in Week 8).

---

## 9. Parameterized queries

Every time you put data into a SQL statement, use parameterized queries.

**Wrong:**
```python
# NEVER do this
title = user_input
conn.execute(f"INSERT INTO papers (title) VALUES ('{title}')")
```

If `title` contains `'); DROP TABLE papers; --`, the f-string approach executes that as SQL.
This is SQL injection.
It destroys data and creates security holes.

**Correct:**
```python
conn.execute(
    "INSERT INTO papers (title) VALUES (?)",
    (title,),
)
```

The `?` is a placeholder.
The second argument is a tuple of values to substitute.
SQLite handles all quoting and escaping for you.
The string `'); DROP TABLE papers; --` becomes a safe literal text value.

For multiple columns:
```python
conn.execute(
    """
    INSERT INTO papers
        (id, title, source_path, text, num_pages, file_size_bytes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        paper.id,
        paper.title,
        paper.source_path,
        paper.text,
        paper.num_pages,
        paper.file_size_bytes,
        paper.created_at.isoformat(),
    ),
)
```

Notice `paper.created_at.isoformat()`.
SQLite does not know how to store a Python `datetime` object directly.
You must convert it to a string.
`isoformat()` produces `"2024-03-15T10:30:00"`.
When you read the value back, use `datetime.fromisoformat(row["created_at"])` to reconstruct the object.
This round-trip conversion is your responsibility.
SQLite will not do it for you.

---

## 10. Transactions in practice

When you use a connection object as a context manager in Python, it manages the transaction for you:

```python
with conn:
    conn.execute("INSERT INTO papers ...")
    conn.execute("INSERT INTO paper_tags ...")
```

If both statements succeed, `with conn` automatically calls `conn.commit()`.
If either statement raises an exception, `with conn` automatically calls `conn.rollback()`.
No data is partially written.

Let us trace a scenario where this matters.

```python
def save_paper_with_tags(conn, paper):
    with conn:
        # Insert the paper row
        conn.execute(
            "INSERT INTO papers (id, title, ...) VALUES (?, ?, ...)",
            (paper.id, paper.title, ...),
        )
        # Insert each tag
        for tag in paper.tags:
            conn.execute(
                "INSERT INTO paper_tags (paper_id, tag) VALUES (?, ?)",
                (paper.id, tag),
            )
```

If the paper insert succeeds but then a tag insert fails (maybe the tag string is invalid), the `with conn` context manager rolls back the paper insert too.
When the function returns (after re-raising the exception), the database has no partial data.
The paper with incomplete tags does not exist in storage.
This protects you from corrupt states.

---

## 11. The repository pattern

The repository pattern is a design idea that says: all database code should live in one place, and the rest of the application should not know the details.

Without a repository, your CLI or service code might look like this:

```python
# Don't do this in a real service
def ingest_paper(conn, paper):
    conn.execute(
        "INSERT INTO papers (id, title, source_path) VALUES (?, ?, ?)",
        (paper.id, paper.title, paper.source_path),
    )
```

This mixes SQL into your service logic.
If you later change the schema, you need to update every place in the code that has SQL.
If you want to test the service without a database, you cannot because the SQL is embedded.

The repository pattern extracts all of that:

```python
class SQLitePaperRepository:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def save(self, paper: Paper) -> None:
        """Persist a Paper. Raises DuplicatePaperError if id already exists."""
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO papers (...) VALUES (...)",
                (...),
            )

    def get(self, paper_id: str) -> Paper:
        """Retrieve a Paper by id. Raises PaperNotFoundError if missing."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM papers WHERE id = ?", (paper_id,)
            ).fetchone()
        if row is None:
            raise PaperNotFoundError(paper_id)
        return self._row_to_paper(row)

    def list_all(self) -> list[Paper]:
        """Return all Papers, ordered by created_at descending."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM papers ORDER BY created_at DESC"
            ).fetchall()
        return [self._row_to_paper(r) for r in rows]

    def exists(self, paper_id: str) -> bool:
        """Return True if a paper with this id is stored."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM papers WHERE id = ?", (paper_id,)
            ).fetchone()
        return row is not None
```

Now the service code looks like this:

```python
class IngestionService:
    def __init__(self, parser, paper_repo, failure_repo):
        self._parser = parser
        self._paper_repo = paper_repo
        self._failure_repo = failure_repo

    def ingest_one(self, path):
        doc = self._parser.parse(path)
        paper = build_paper_from(doc)
        self._paper_repo.save(paper)
```

The service knows nothing about SQL.
It knows only about the interface: `save()`, `get()`, `list_all()`, `exists()`.

This design has several advantages:
- You can test the service with a fake in-memory repository.
- You can switch from SQLite to PostgreSQL by writing a new repository class without changing the service.
- The SQL lives in one place, which is easier to audit and maintain.
- The service is easier to read because it talks about domain concepts, not query strings.

### Why storage code belongs in `storage/`

The project has a clear module structure.
Domain models live in `core/models.py`.
They must not import anything from storage, CLI, or other infrastructure.
The repository implementations live in `storage/`.
The services live in `services/` and depend on interfaces, not implementations.

This separation ensures that the most important logic — the domain model — stays clean and testable without any database setup.

---

## 12. Mapping domain models to rows and back

When you save a `Paper`, you convert its attributes to SQLite-compatible values.
When you retrieve a row, you convert it back to a `Paper`.
This mapping is your responsibility.

### Paper to row (save direction)

```python
conn.execute(
    """
    INSERT INTO papers
        (id, title, source_path, text, num_pages, file_size_bytes,
         author, abstract, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        paper.id,                        # str — already text
        paper.title,                     # str — already text
        paper.source_path,               # str — already text
        paper.text,                      # str — already text
        paper.num_pages,                 # int — already integer
        paper.file_size_bytes,           # int — already integer
        paper.author,                    # str | None — NULL if None
        paper.abstract,                  # str | None — NULL if None
        paper.created_at.isoformat(),    # datetime → str conversion needed
    ),
)
```

Note that Python `None` maps to SQL `NULL` automatically.
The datetime conversion is the only non-trivial mapping here.

### Row to Paper (load direction)

```python
@staticmethod
def _row_to_paper(row: sqlite3.Row) -> Paper:
    return Paper(
        id=row["id"],
        title=row["title"],
        source_path=row["source_path"],
        text=row["text"],
        num_pages=row["num_pages"],
        file_size_bytes=row["file_size_bytes"],
        author=row["author"],          # may be None
        abstract=row["abstract"],      # may be None
        created_at=datetime.fromisoformat(row["created_at"]),  # str → datetime
    )
```

`datetime.fromisoformat()` is the inverse of `isoformat()`.
It parses `"2024-03-15T10:30:00"` back into a `datetime` object.

### FailedDocument to row

```python
conn.execute(
    """
    INSERT INTO failed_documents
        (source_path, error_message, error_type, occurred_at)
    VALUES (?, ?, ?, ?)
    """,
    (
        str(failure.source_path),        # Path → str conversion needed
        failure.error_message,
        failure.error_type,
        failure.occurred_at.isoformat(),
    ),
)
```

Note `str(failure.source_path)`.
`FailedDocument.source_path` is a `Path` object.
SQLite cannot store a `Path` directly.
You must convert it to a string with `str()`.
When you read it back, use `Path(row["source_path"])` to reconstruct the `Path` object.

---

## 13. Writing integration tests

Unit tests test one function in isolation with mocks.
Integration tests test how real components work together.
For storage code, integration tests are especially important.

An integration test for a repository should:
1. Create a real (but temporary) database in memory or in `/tmp`.
2. Call repository methods.
3. Assert that the data round-trips correctly.

The best approach is an **in-memory SQLite database**:

```python
import sqlite3
import pytest
from pathlib import Path
from datetime import datetime

from researchops.storage.sqlite_repository import SQLitePaperRepository
from researchops.core.models import Paper


@pytest.fixture
def repo(tmp_path):
    """Return a repository backed by a temporary database."""
    db_path = tmp_path / "test.db"
    return SQLitePaperRepository(db_path)


def test_save_and_get(repo):
    paper = Paper(
        id="abc123",
        title="Attention Is All You Need",
        source_path="papers/attention.pdf",
        text="We propose a new architecture...",
        num_pages=15,
        file_size_bytes=912345,
        created_at=datetime(2024, 3, 15, 10, 30, 0),
    )

    repo.save(paper)
    loaded = repo.get("abc123")

    assert loaded.id == "abc123"
    assert loaded.title == "Attention Is All You Need"
    assert loaded.num_pages == 15
    assert loaded.created_at == datetime(2024, 3, 15, 10, 30, 0)


def test_get_nonexistent_raises(repo):
    from researchops.core.exceptions import PaperNotFoundError
    with pytest.raises(PaperNotFoundError):
        repo.get("does-not-exist")


def test_duplicate_raises(repo):
    from researchops.core.exceptions import DuplicatePaperError
    paper = Paper(
        id="dup1",
        title="Test",
        source_path="test.pdf",
        text="...",
        num_pages=1,
        file_size_bytes=1000,
        created_at=datetime.utcnow(),
    )
    repo.save(paper)
    with pytest.raises(DuplicatePaperError):
        repo.save(paper)


def test_list_all_returns_papers(repo):
    papers = [
        Paper(id=f"id{i}", title=f"Paper {i}", source_path=f"p{i}.pdf",
              text="text", num_pages=1, file_size_bytes=100,
              created_at=datetime.utcnow())
        for i in range(3)
    ]
    for p in papers:
        repo.save(p)

    all_papers = repo.list_all()
    assert len(all_papers) == 3
```

Using `tmp_path` (a pytest built-in fixture) gives you a real temporary directory that is cleaned up automatically after each test.
This is better than using `:memory:` when your `SQLitePaperRepository` constructor creates a connection to a file path.

---

## 14. Temporary test databases

There are two patterns for test databases.

**Pattern 1: `tmp_path` with a file**

```python
@pytest.fixture
def repo(tmp_path):
    return SQLitePaperRepository(tmp_path / "test.db")
```

Each test gets its own directory under `/tmp/pytest-*/`.
Files are isolated between tests.
The directory is cleaned up after the test run.

**Pattern 2: `:memory:` with a custom constructor**

```python
@pytest.fixture
def repo():
    # Requires a constructor that accepts an existing connection
    conn = sqlite3.connect(":memory:")
    return SQLitePaperRepository.from_connection(conn)
```

In-memory databases are slightly faster because they skip disk I/O.
But they require your repository to support an alternative constructor.

For ResearchOps, `tmp_path` is simpler and works with the standard `SQLitePaperRepository(db_path)` constructor.

---

## 15. Common mistakes

### Forgetting `conn.row_factory = sqlite3.Row`

Without this, every `fetchone()` returns a plain tuple.
You access columns by index: `row[0]`, `row[1]`, etc.
If you ever add or reorder a column, every index reference breaks silently.
Always set `row_factory`.

### Building SQL with f-strings

```python
# Dangerous
query = f"SELECT * FROM papers WHERE title = '{user_input}'"
conn.execute(query)
```

Use parameterized queries.

### Forgetting to commit

The `sqlite3` module does not auto-commit by default in many usage patterns.
If you call `conn.execute(...)` but never commit, the data is in memory but not written to disk.
The next read in the same connection may see it, but a new connection will not.
Using `with conn:` handles this automatically.

### Storing `Path` objects directly

```python
conn.execute("INSERT INTO papers (source_path) VALUES (?)", (paper.source_path,))
```

If `paper.source_path` is a `Path` object, this will likely cause a type adapter warning and store an ambiguous representation.
Always convert: `str(paper.source_path)`.

### Forgetting `IF NOT EXISTS` in schema creation

If you run schema creation twice (which happens every time `SQLitePaperRepository.__init__` is called), you get an error about the table already existing.
Use `CREATE TABLE IF NOT EXISTS`.

### Not enabling foreign keys

```python
conn.execute("PRAGMA foreign_keys = ON")
```

Without this, SQLite ignores all foreign key constraints.
Data integrity bugs become invisible.
Always enable this.

---

## 16. Schema initialization pattern

Your repository should initialize the schema on construction:

```python
class SQLitePaperRepository:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self) -> None:
        schema_path = Path(__file__).parent / "schema.sql"
        with self._connect() as conn:
            schema_sql = schema_path.read_text(encoding="utf-8")
            conn.executescript(schema_sql)
```

Keeping the schema in a `schema.sql` file (not hardcoded as a Python string) has advantages:
- You can open it with any SQL editor or viewer.
- It is version-controlled separately.
- It is easy to inspect without reading Python.

`executescript()` runs multiple SQL statements separated by semicolons in one call.
This is different from `execute()`, which runs one statement at a time.
Use `executescript()` for DDL files.

---

## 17. Connecting directly to Week 3 models

Every Week 3 model maps cleanly to this week's tables.

`Paper` → `papers` table.
Every field in `Paper` has a corresponding column.
The only mapping work is `created_at` (datetime ↔ ISO string) and `source_path` (str, already a string in this model).

`FailedDocument` → `failed_documents` table.
The source_path conversion is needed (Path → str).
The occurred_at conversion is needed (datetime → ISO string).

`ParsedDocument` → not stored directly.
It is a transient processing artifact.
The ingestion service converts it to a `Paper` and stores the `Paper`.

`IngestionResult` → not stored directly.
It is a summary object built from counting successes, failures, and skips.
You can reconstruct it from the other tables if needed.

---

## 18. Review questions and self-checks

**Conceptual questions:**

1. What is the difference between data in RAM and data in a database?

2. Why does SQLite not need a server process when PostgreSQL does?

3. A friend says "I'll just store everything as JSON files, databases are too complex."
   What are three situations where a relational database handles problems that JSON files handle poorly?

4. What does `PRIMARY KEY` guarantee?

5. What does `UNIQUE` guarantee that is different from `PRIMARY KEY`?

6. You have a paper with 5 tags. How many rows exist in `paper_tags` for this paper?

7. What happens to `paper_tags` rows when their paper is deleted, given `ON DELETE CASCADE`?

8. You insert a paper, then try to insert it again with the same `id`. What happens?

9. Why should you use parameterized queries instead of f-strings?

10. What is the difference between `commit` and `rollback`?

**Code-reading questions:**

11. Look at the `_row_to_paper` method in `sqlite_repository.py`.
    Which field requires a type conversion from string to Python object?
    Why?

12. Look at the `save` method.
    Which line would fail if the paper already exists in the database?
    What exception is raised?

13. In the `_connect` context manager, what happens if `conn.commit()` is about to run but an exception occurs?

**Design questions:**

14. Why does the repository pattern improve testability?

15. Why should `Paper` and other domain models in `core/models.py` not import `sqlite3`?

16. You want to add a `doi` column to `papers` later.
    Where do you make the change?
    Does the `Paper` dataclass need to change too?

17. Two functions both call `repo.save(paper)` in separate threads at the same time.
    What could go wrong?
    (Hint: think about the `exists()` check and the `INSERT` statement as two separate operations.)

**Practice tasks:**

18. Open a Python REPL and create an in-memory SQLite database.
    Create one table with three columns.
    Insert two rows.
    Query them back.

19. Write a function that takes a `Paper` and a connection and returns `True` if the paper's title already exists (ignoring `id`).

20. Write an integration test that saves three papers, calls `list_all()`, and verifies the order matches creation time.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 05 — SQLite Storage:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
