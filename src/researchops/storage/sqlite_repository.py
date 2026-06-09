"""SQLite-backed paper repository.

Implements the PaperRepository and FailureRepository protocols
from core/interfaces.py.

Week 5: basic save/get/list/exists for Paper objects.
Week 6: add FailedDocument persistence.
Week 7: add keyword search support.

Design notes:
- We use raw sqlite3 (stdlib) to avoid adding SQLAlchemy before Week 5.
- SQLAlchemy can be introduced in Week 5 as a refactor exercise.
- All public methods are synchronous — they run in a thread or process,
  never directly in the asyncio event loop.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from researchops.config.logging import get_logger
from researchops.core.exceptions import DuplicatePaperError, PaperNotFoundError
from researchops.core.models import FailedDocument, Paper

log = get_logger(__name__)


def _load_schema(conn: sqlite3.Connection, schema_path: Path) -> None:
    """Execute the schema SQL file against *conn*."""
    sql = schema_path.read_text(encoding="utf-8")
    conn.executescript(sql)


class SQLitePaperRepository:
    """Persist and retrieve Paper objects in a local SQLite database.

    Usage:
        repo = SQLitePaperRepository(Path("data/researchops.db"))
        repo.save(paper)
        paper = repo.get("abc123")
    """

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _connect(self) -> Generator[sqlite3.Connection, None, None]:
        """Yield a database connection with row_factory set."""
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_schema(self) -> None:
        schema_path = Path(__file__).parent / "schema.sql"
        with self._connect() as conn:
            _load_schema(conn, schema_path)
        log.debug("Schema initialised at %s", self._db_path)

    # ------------------------------------------------------------------
    # PaperRepository protocol
    # ------------------------------------------------------------------

    def save(self, paper: Paper) -> None:
        """Persist a paper. Raises DuplicatePaperError if ID already exists."""
        if self.exists(paper.id):
            raise DuplicatePaperError(paper.id)

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO papers
                    (id, title, source_path, text, num_pages, file_size_bytes,
                     author, abstract, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    paper.id,
                    paper.title,
                    paper.source_path,
                    paper.text,
                    paper.num_pages,
                    paper.file_size_bytes,
                    paper.author,
                    paper.abstract,
                    paper.created_at.isoformat(),
                ),
            )
            for tag in paper.tags:
                conn.execute(
                    "INSERT OR IGNORE INTO paper_tags (paper_id, tag) VALUES (?, ?)",
                    (paper.id, tag),
                )
        log.info("Saved paper %s (%s)", paper.id, paper.title[:60])

    def get(self, paper_id: str) -> Paper:
        """Retrieve a paper by ID. Raises PaperNotFoundError if missing."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM papers WHERE id = ?", (paper_id,)
            ).fetchone()

        if row is None:
            raise PaperNotFoundError(paper_id)

        return self._row_to_paper(row)

    def list_all(self) -> list[Paper]:
        """Return all stored papers."""
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM papers ORDER BY created_at DESC").fetchall()
        return [self._row_to_paper(r) for r in rows]

    def exists(self, paper_id: str) -> bool:
        """Return True if a paper with this ID is stored."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM papers WHERE id = ?", (paper_id,)
            ).fetchone()
        return row is not None

    def delete(self, paper_id: str) -> None:
        """Delete a paper by ID."""
        with self._connect() as conn:
            conn.execute("DELETE FROM papers WHERE id = ?", (paper_id,))

    # ------------------------------------------------------------------
    # FailureRepository protocol
    # ------------------------------------------------------------------

    def record_failure(self, failure: FailedDocument) -> None:
        """Persist a failure record."""
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO failed_documents
                    (source_path, error_message, error_type, occurred_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    str(failure.source_path),
                    failure.error_message,
                    failure.error_type,
                    failure.occurred_at.isoformat(),
                ),
            )

    def list_failures(self) -> list[FailedDocument]:
        """Return all recorded failures."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM failed_documents ORDER BY occurred_at DESC"
            ).fetchall()
        return [
            FailedDocument(
                source_path=Path(r["source_path"]),
                error_message=r["error_message"],
                error_type=r["error_type"],
                occurred_at=datetime.fromisoformat(r["occurred_at"]),
            )
            for r in rows
        ]

    def clear_failures(self) -> None:
        """Remove all failure records."""
        with self._connect() as conn:
            conn.execute("DELETE FROM failed_documents")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_paper(row: sqlite3.Row) -> Paper:
        return Paper(
            id=row["id"],
            title=row["title"],
            source_path=row["source_path"],
            text=row["text"],
            num_pages=row["num_pages"],
            file_size_bytes=row["file_size_bytes"],
            created_at=datetime.fromisoformat(row["created_at"]),
            author=row["author"],
            abstract=row["abstract"],
        )
