# Notes - Week 05 SQLite Storage Layer

SQLite is a file-based relational database. That makes it a great learning tool and a practical default for local-first applications. You do not need a separate database server process. The database is just a file, but it still supports tables, indexes, transactions, and SQL queries.

A schema defines the shape of your data. For ResearchOps, a simple first schema might include a `papers` table and a `parsed_documents` table.

```sql
CREATE TABLE papers (
    id TEXT PRIMARY KEY,
    source_path TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    source_type TEXT NOT NULL
);

CREATE TABLE parsed_documents (
    paper_id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    word_count INTEGER NOT NULL,
    FOREIGN KEY (paper_id) REFERENCES papers(id)
);
```

The `papers` table stores document identity and metadata. The `parsed_documents` table stores extracted content. Splitting them keeps responsibilities clearer and leaves room for papers that failed parsing.

Python ships with the `sqlite3` module, so you can start without extra dependencies.

```python
import sqlite3
from pathlib import Path


def connect(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection
```

Setting `row_factory` lets you access columns by name, which makes mapping rows back to domain objects easier.

A transaction is a unit of work that either fully succeeds or fully fails. That matters when one logical operation writes to multiple tables. If inserting into `papers` works but inserting into `parsed_documents` fails, you usually want both writes rolled back.

```python
with connection:
    connection.execute(...)
    connection.execute(...)
```

Using the connection as a context manager commits on success and rolls back on exception.

The repository pattern is a thin abstraction over persistence. Its purpose is not to hide SQL forever. Its purpose is to keep the rest of the application from knowing table details.

```python
class PaperRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def save_parsed_document(self, paper: Paper, document: ParsedDocument) -> None:
        with self.connection:
            self.connection.execute(...)
            self.connection.execute(...)
```

The CLI should not construct SQL strings. It should call methods like `save_parsed_document()` or `get_paper_by_id()`.

Be careful about where you put schema creation. It is usually fine to have a dedicated `initialize_database()` function that runs DDL statements exactly once or idempotently. A common beginner mistake is recreating tables during every read or write call.

Testing storage code should include round trips. A round trip test writes domain data into the database and then reads it back, asserting the values match. This proves more than mocking ever could because it exercises the real SQL, constraints, and mapping logic.

Another important idea is parameterized SQL. Do not build SQL strings with f-strings when values come from users or files. Instead, pass parameters separately.

```python
connection.execute(
    "INSERT INTO papers (id, source_path, title, source_type) VALUES (?, ?, ?, ?)",
    (paper.id, str(paper.source_path), paper.title, paper.source_type),
)
```

That protects against SQL injection and avoids quoting mistakes.

By the end of this week, persistence should feel like another boundary: the application speaks in domain models, while the repository translates those models into database rows and back. That boundary is what will let you swap real and fake repositories later for testing and architecture work.
