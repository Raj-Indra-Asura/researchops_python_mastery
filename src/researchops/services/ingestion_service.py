"""Ingestion service — orchestrates PDF discovery, parsing, and storage.

This is the central use-case for Month 2. It depends on:
- DocumentParser protocol (core/interfaces.py)
- PaperRepository protocol (core/interfaces.py)
- FailureRepository protocol (core/interfaces.py)

It must NOT import concrete sqlite/pdf implementations. Those are
wired together in the CLI (cli/commands/ingest.py).

Week 6: basic sequential ingestion.
Week 8: parallelise with ProcessPoolExecutor (workers/process_pool.py).
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime
from pathlib import Path

from researchops.core.exceptions import ParsingError, ResearchOpsError
from researchops.core.interfaces import (
    DocumentParser,
    FailureRepository,
    PaperRepository,
)
from researchops.core.models import (
    FailedDocument,
    IngestionResult,
    Paper,
    PaperId,
)
from researchops.parsing.metadata_extractor import extract_author, extract_title
from researchops.parsing.text_cleaner import clean_text
from researchops.utils.paths import find_pdfs

log = logging.getLogger(__name__)


class IngestionService:
    """Ingest a directory of PDF files into the paper repository.

    Constructor arguments are *protocols*, not concrete types. This
    allows tests to inject fake implementations without touching a real
    database or real PDFs.
    """

    def __init__(
        self,
        parser: DocumentParser,
        paper_repo: PaperRepository,
        failure_repo: FailureRepository,
    ) -> None:
        self._parser = parser
        self._paper_repo = paper_repo
        self._failure_repo = failure_repo

    def ingest_directory(
        self,
        directory: Path,
        *,
        recursive: bool = False,
        skip_existing: bool = True,
    ) -> IngestionResult:
        """Discover and ingest all PDFs in *directory*.

        Args:
            directory: Root directory to scan for PDF files.
            recursive: If True, recurse into subdirectories.
            skip_existing: If True, skip files already in the repository.

        Returns:
            An :class:`~researchops.core.models.IngestionResult` summary.
        """
        run_id = str(uuid.uuid4())[:8]
        result = IngestionResult(
            run_id=run_id,
            directory=directory,
            started_at=datetime.utcnow(),
        )

        try:
            pdfs = find_pdfs(directory, recursive=recursive)
        except NotADirectoryError as exc:
            log.error("Invalid directory: %s", exc)
            result.finished_at = datetime.utcnow()
            return result

        log.info("Starting ingestion run %s: %d PDF(s) found", run_id, len(pdfs))

        for pdf_path in pdfs:
            paper_id = str(PaperId.from_path(pdf_path))

            if skip_existing and self._paper_repo.exists(paper_id):
                log.debug("Skipping existing paper: %s", pdf_path.name)
                result.skipped.append(pdf_path)
                continue

            paper = self._ingest_one(pdf_path, paper_id)
            if paper is not None:
                result.successes.append(paper)
            else:
                # failure was already recorded inside _ingest_one
                pass

        # Collect failures recorded during this run
        # (simple implementation — a production version would tag by run_id)
        result.finished_at = datetime.utcnow()
        log.info(
            "Ingestion run %s complete: %d ok / %d failed / %d skipped",
            run_id,
            len(result.successes),
            len(result.failures),
            len(result.skipped),
        )
        return result

    def _ingest_one(self, path: Path, paper_id: str) -> Paper | None:
        """Parse and save a single PDF. Returns Paper on success, None on failure."""
        try:
            doc = self._parser.parse(path)
        except (ParsingError, ResearchOpsError) as exc:
            failure = FailedDocument(
                source_path=path,
                error_message=str(exc),
                error_type=type(exc).__name__,
            )
            self._failure_repo.record_failure(failure)
            log.warning("Parse failed: %s — %s", path.name, exc)
            return None
        except Exception as exc:
            failure = FailedDocument(
                source_path=path,
                error_message=f"Unexpected error: {exc}",
                error_type=type(exc).__name__,
            )
            self._failure_repo.record_failure(failure)
            log.error("Unexpected error parsing %s: %s", path.name, exc, exc_info=True)
            return None

        paper = Paper(
            id=paper_id,
            title=extract_title(doc),
            source_path=str(path),
            text=clean_text(doc.raw_text),
            num_pages=doc.num_pages,
            file_size_bytes=doc.file_size_bytes,
            author=extract_author(doc),
            abstract=None,  # TODO (Week 6): call extract_abstract
        )

        try:
            self._paper_repo.save(paper)
        except Exception as exc:
            log.warning("Failed to save paper %s: %s", paper.id, exc)
            return None

        return paper
