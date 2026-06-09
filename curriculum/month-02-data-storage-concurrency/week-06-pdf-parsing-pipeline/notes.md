# Week 06 Notes — PDF Parsing Pipeline

## 1. Chapter overview

In Week 5 you built the storage layer.
You have a database that can hold papers and failure records.
But the database is empty.

This week you connect the dots.
You will learn how to take a directory of PDF files and turn them into stored papers through a coordinated sequence of steps called a pipeline.

By the end of this week, you will be able to run one command and populate your database with real research papers.
The system will store successes and record failures.
Nothing will be silently lost.

---

## 2. What you already know

You know how to model a `Paper`, `ParsedDocument`, `FailedDocument`, and `IngestionResult`.
You know how to save and retrieve papers using `SQLitePaperRepository`.
You know how to work with file paths using `pathlib.Path`.
You know how to raise and catch exceptions.

This week adds: how to extract text from PDFs, how to chain these steps together in a service, and how to handle the inevitable failures along the way.

---

## 3. What is a pipeline?

A pipeline is a sequence of processing stages where each stage takes the output of the previous stage as its input.

Think of an assembly line in a factory.
Raw materials enter at one end.
Each station performs one specific task.
Finished products exit at the other end.
If a part is defective at one station, it does not disrupt the other stations.

In software, pipelines are useful when:
- You need to transform data through multiple distinct steps.
- Each step has a single clear responsibility.
- Failures in one step should not destroy the whole batch.
- You want to replace or modify one step without rewriting everything.

The ResearchOps ingestion pipeline looks like this:

```text
Directory of PDFs
      |
      v
[Stage 1] Scanner: find all .pdf files
      |
      v
[Stage 2] Parser: extract text from each PDF
      |
      v
[Stage 3] Metadata extractor: derive title, author
      |
      v
[Stage 4] Service: coordinate and make decisions
      |
      v
[Stage 5] Repository: save Paper or record FailedDocument
      |
      v
Database
```

Each box is a separate module or function with a clear contract.
The scanner does not know about the parser.
The parser does not know about the repository.
The service knows about all of them but does not do their jobs.

---

## 4. Why PDFs are hard

PDFs were designed for printing, not for text extraction.

A PDF describes a page in terms of:
- Fonts and their coordinates
- Character codes (which may not map to standard Unicode)
- Vector graphics
- Images

There is no concept of "paragraphs" or "words" in the PDF standard.
Text extraction software has to reverse-engineer words and lines from character positions.
This works well on digitally-created PDFs (made from Word, LaTeX, etc.).
It works poorly on scanned images embedded in PDFs (no embedded text, just pixels).

The practical consequences for ResearchOps:
- Some PDFs yield clean text.
- Some yield text with broken spacing (`"trans former"` instead of `"transformer"`).
- Some yield garbled Unicode from unusual fonts.
- Some yield nothing at all (image-only PDFs).
- Some yield repeated headers and footers on every page.

Your pipeline must handle all of these cases gracefully.

---

## 5. pypdf at a beginner level

`pypdf` is a pure-Python library for working with PDF files.
It does not require any system-level PDF software to be installed.

The basic usage:

```python
from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages).strip()
```

Let us read every line.

`reader = PdfReader(str(pdf_path))` — Opens the PDF file.
`PdfReader` reads the file structure and gives you access to pages.
`str(pdf_path)` converts the `Path` object to a string because `pypdf` expects a string path.

`for page in reader.pages:` — Iterates through every page in the document.
`reader.pages` is a sequence of `PageObject` instances.
Each `PageObject` represents one physical page.

`text = page.extract_text() or ""` — Extracts the text from one page.
The `or ""` is critical.
`extract_text()` can return `None` for image-only pages.
Without the `or ""`, a `None` result would propagate through the pipeline and cause a `TypeError` later.

`pages.append(text)` — Collects each page's text in a list.

`return "\n".join(pages).strip()` — Joins all pages with a newline separator and removes leading/trailing whitespace.

### Getting metadata

PDFs often embed metadata in their file header:

```python
reader = PdfReader(str(pdf_path))
meta = reader.metadata  # May be None for some PDFs
if meta:
    title = meta.title      # May be None
    author = meta.author    # May be None
```

The metadata is not always reliable.
Many PDFs have empty or incorrect title fields.
Your metadata extractor should treat it as a hint, not a guarantee.

---

## 6. The parsing stage: a single responsibility

The parser has one job: turn a file path into a `ParsedDocument` or raise an exception.

```python
from pathlib import Path
from researchops.core.models import ParsedDocument
from researchops.core.exceptions import ParsingError, EmptyDocumentError


def parse_pdf(path: Path) -> ParsedDocument:
    if not path.exists():
        raise ParsingError(f"File not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ParsingError(f"Not a PDF file: {path}")

    try:
        import pypdf
        reader = pypdf.PdfReader(str(path))
        pages_text = [page.extract_text() or "" for page in reader.pages]
        full_text = "\n".join(pages_text)
        meta = reader.metadata or {}
        metadata = {
            k.lstrip("/"): v
            for k, v in meta.items()
            if isinstance(v, str) and v.strip()
        }
    except Exception as exc:
        raise ParsingError(f"Failed to parse {path}: {exc}") from exc

    doc = ParsedDocument(
        source_path=path,
        raw_text=full_text,
        num_pages=len(reader.pages),
        file_size_bytes=path.stat().st_size,
        metadata=metadata,
    )

    if doc.is_empty():
        raise EmptyDocumentError(str(path))

    return doc
```

This function does not talk to a database.
It does not log.
It does not build a `Paper`.
It only parses.
This single-responsibility design means you can test parsing without any database setup.

---

## 7. The metadata extraction stage

After parsing, you have raw text and a metadata dictionary from the PDF header.
The next stage derives structured metadata like `title` and `author`.

```python
def extract_title(doc: ParsedDocument) -> str:
    """Try PDF metadata first, then fall back to first line of text."""
    if "Title" in doc.metadata and doc.metadata["Title"].strip():
        return doc.metadata["Title"].strip()
    lines = [l.strip() for l in doc.raw_text.splitlines() if l.strip()]
    if lines:
        return lines[0][:200]  # truncate very long lines
    return "Untitled"


def extract_author(doc: ParsedDocument) -> str | None:
    """Return author from PDF metadata if available."""
    author = doc.metadata.get("Author", "").strip()
    return author if author else None
```

These functions are heuristics.
They will be wrong sometimes.
That is acceptable at this stage.
The important thing is they have a fallback and never crash.

---

## 8. The service layer: orchestrating the pipeline

The ingestion service coordinates all the stages.
It does not implement any stage itself.
It calls the right things in the right order.

```python
class IngestionService:
    def __init__(
        self,
        parser: DocumentParser,
        paper_repo: PaperRepository,
        failure_repo: FailureRepository,
    ) -> None:
        self._parser = parser
        self._paper_repo = paper_repo
        self._failure_repo = failure_repo
```

Line by line:

`def __init__(self, parser, paper_repo, failure_repo):` — The service receives its collaborators through the constructor.
It does not create them.
This is called **constructor injection**, a form of **dependency injection**.

**Dependency injection** means: the dependencies a class needs are given to it from the outside, not created inside.

Why does this matter?

Consider the alternative:
```python
class IngestionService:
    def __init__(self, db_path):
        self._parser = PdfParser()                           # created inside
        self._paper_repo = SQLitePaperRepository(db_path)   # created inside
        self._failure_repo = SQLiteFailureRepository(db_path) # created inside
```

This is tightly coupled.
To test `IngestionService`, you must have a real PDF parser and a real database.
You cannot swap in a fake parser that returns controlled results.

With dependency injection:
```python
# In production code:
service = IngestionService(
    parser=PdfParser(),
    paper_repo=SQLitePaperRepository(db_path),
    failure_repo=SQLitePaperRepository(db_path),
)

# In tests:
service = IngestionService(
    parser=FakeParser(returns=sample_document),
    paper_repo=InMemoryRepository(),
    failure_repo=InMemoryRepository(),
)
```

The test does not touch the filesystem or database.
It can run in milliseconds.
It can test every code path by controlling what the fake objects return.

### The ingest_directory method

```python
def ingest_directory(
    self,
    directory: Path,
    *,
    recursive: bool = False,
    skip_existing: bool = True,
) -> IngestionResult:
    run_id = str(uuid.uuid4())[:8]
    result = IngestionResult(
        run_id=run_id,
        directory=directory,
        started_at=datetime.utcnow(),
    )

    pdfs = find_pdfs(directory, recursive=recursive)

    for pdf_path in pdfs:
        paper_id = str(PaperId.from_path(pdf_path))

        if skip_existing and self._paper_repo.exists(paper_id):
            result.skipped.append(pdf_path)
            continue

        paper = self._ingest_one(pdf_path, paper_id)
        if paper is not None:
            result.successes.append(paper)

    result.finished_at = datetime.utcnow()
    return result
```

`run_id = str(uuid.uuid4())[:8]` — Creates a short unique identifier for this ingestion run.
Useful for log correlation and debugging.

`pdfs = find_pdfs(directory, recursive=recursive)` — Scans the directory.
`find_pdfs` is a utility function that uses `pathlib` to find `.pdf` files.
This separates scanning from the service logic.

`paper_id = str(PaperId.from_path(pdf_path))` — Computes the stable hash-based ID for the paper.
The same file path always produces the same ID.
This means `skip_existing` works correctly across multiple runs.

`if skip_existing and self._paper_repo.exists(paper_id):` — Avoids re-ingesting files that are already in the database.
This is an idempotency check.
Running the ingest command twice should not double the data.

### The _ingest_one method

```python
def _ingest_one(self, path: Path, paper_id: str) -> Paper | None:
    try:
        doc = self._parser.parse(path)
    except (ParsingError, ResearchOpsError) as exc:
        failure = FailedDocument(
            source_path=path,
            error_message=str(exc),
            error_type=type(exc).__name__,
        )
        self._failure_repo.record_failure(failure)
        return None
    except Exception as exc:
        failure = FailedDocument(
            source_path=path,
            error_message=f"Unexpected error: {exc}",
            error_type=type(exc).__name__,
        )
        self._failure_repo.record_failure(failure)
        return None

    paper = Paper(
        id=paper_id,
        title=extract_title(doc),
        source_path=str(path),
        text=clean_text(doc.raw_text),
        num_pages=doc.num_pages,
        file_size_bytes=doc.file_size_bytes,
        author=extract_author(doc),
        abstract=None,
    )

    try:
        self._paper_repo.save(paper)
    except Exception as exc:
        return None

    return paper
```

`try: doc = self._parser.parse(path)` — Attempts to parse the PDF.

`except (ParsingError, ResearchOpsError) as exc:` — Catches expected parsing errors.
Expected errors are ones your code knows about and has a plan for.

`except Exception as exc:` — Catches unexpected errors.
A corrupt PDF might raise a low-level exception from inside `pypdf` that your code did not anticipate.
You still want to record it as a failure rather than crash.

**One bad PDF should not crash the whole batch.**
This is the critical design principle of the `_ingest_one` method.
Each PDF is processed independently.
A failure for one creates a `FailedDocument` record and continues with the next.

`failure = FailedDocument(source_path=path, error_message=str(exc), error_type=type(exc).__name__)` — Records exactly what went wrong, for which file, and what type of error it was.
This is how you debug ingestion problems later.

`text=clean_text(doc.raw_text)` — Applies text cleaning before storing.
This removes control characters, normalizes whitespace, and collapses repeated blank lines.

---

## 9. Failure handling philosophy

Failures are data.

A naive pipeline treats failures as exceptions to be logged and ignored.
The result is a database full of gaps that you cannot query.
You do not know which papers failed.
You do not know why.
You cannot even tell how many papers are missing.

The ResearchOps approach:
- Every failure is a `FailedDocument` record stored in the database.
- The failure includes the source path, error message, error type, and timestamp.
- You can query failures: `repo.list_failures()`.
- You can re-process specific failures later (perhaps with a different parser or after fixing a corrupt file).
- The `IngestionResult` summary reports exact counts of successes, failures, and skips.

This is the same philosophy as structured logging over silent try-except swallowing.
Visible failures are fixable failures.

---

## 10. Wiring it all together in the CLI

The CLI is where concrete implementations are assembled.

```python
# src/researchops/cli/commands/ingest.py

from pathlib import Path
import click

from researchops.parsing.pdf_parser import PdfParserAdapter
from researchops.services.ingestion_service import IngestionService
from researchops.storage.sqlite_repository import SQLitePaperRepository


@click.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--db", default="researchops.db", help="Database file path.")
def ingest(directory: Path, db: str) -> None:
    """Ingest all PDFs in DIRECTORY into the database."""
    db_path = Path(db)
    repo = SQLitePaperRepository(db_path)
    parser = PdfParserAdapter()

    service = IngestionService(
        parser=parser,
        paper_repo=repo,
        failure_repo=repo,   # same object implements both protocols
    )

    result = service.ingest_directory(directory)
    click.echo(f"Ingested: {len(result.successes)} ok / "
               f"{len(result.failures)} failed / "
               f"{len(result.skipped)} skipped")
```

The CLI does three things:
1. Parses command-line arguments.
2. Wires up the concrete implementations.
3. Calls the service.

The service knows nothing about Click or the CLI.
The service can be called from tests, scripts, or other commands with no changes.

---

## 11. Parser abstraction

The `DocumentParser` protocol in `core/interfaces.py` defines the contract:

```python
class DocumentParser(Protocol):
    def parse(self, path: Path) -> ParsedDocument:
        ...
```

Any class with a `parse(path)` method that returns a `ParsedDocument` satisfies this protocol.

This means:
- In production: `PdfParserAdapter` wraps `pypdf`.
- In tests: `FakeParser` returns controlled results.

```python
class FakeParser:
    """Returns a pre-set ParsedDocument for any path."""

    def __init__(self, document: ParsedDocument) -> None:
        self._document = document

    def parse(self, path: Path) -> ParsedDocument:
        return self._document
```

Using `FakeParser` in tests:

```python
def test_ingest_records_success(tmp_path):
    fake_doc = ParsedDocument(
        source_path=tmp_path / "paper.pdf",
        raw_text="Deep learning enables...",
        num_pages=5,
        file_size_bytes=10000,
    )

    repo = SQLitePaperRepository(tmp_path / "test.db")
    service = IngestionService(
        parser=FakeParser(fake_doc),
        paper_repo=repo,
        failure_repo=repo,
    )

    # Create a placeholder file so the scanner finds it
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"fake pdf content")

    result = service.ingest_directory(tmp_path)

    assert len(result.successes) == 1
    assert len(result.failures) == 0
    papers = repo.list_all()
    assert len(papers) == 1
    assert papers[0].num_pages == 5
```

This test does not require a real PDF.
It is fast, deterministic, and covers the full flow from scanning to storage.

---

## 12. End-to-end integration tests

End-to-end tests use real files and a real database.
They are slower but test the actual integration of all components.

For end-to-end tests, the repository provides sample PDFs in `examples/sample_papers/`.

```python
import pytest
from pathlib import Path
from researchops.parsing.pdf_parser import parse_pdf
from researchops.services.ingestion_service import IngestionService
from researchops.storage.sqlite_repository import SQLitePaperRepository


@pytest.fixture
def sample_papers_dir() -> Path:
    return Path(__file__).parent.parent.parent / "examples" / "sample_papers"


def test_ingest_sample_papers(tmp_path, sample_papers_dir):
    """Full end-to-end: scan, parse, store, verify."""
    if not sample_papers_dir.exists():
        pytest.skip("No sample papers directory")

    repo = SQLitePaperRepository(tmp_path / "test.db")
    from researchops.parsing.pdf_parser import PdfParserAdapter
    service = IngestionService(
        parser=PdfParserAdapter(),
        paper_repo=repo,
        failure_repo=repo,
    )

    result = service.ingest_directory(sample_papers_dir)

    assert result.total > 0
    assert len(result.successes) >= 0  # depends on sample PDFs
    stored = repo.list_all()
    assert len(stored) == len(result.successes)
```

End-to-end tests are valuable for verifying that the whole chain works.
But they are fragile when PDFs change.
Balance end-to-end tests with unit tests that cover error paths using fakes.

---

## 13. Connecting to Week 5

This week depends on Week 5 completely.

`IngestionService` calls `self._paper_repo.save(paper)`.
That method is `SQLitePaperRepository.save()` from Week 5.

`IngestionService` calls `self._failure_repo.record_failure(failure)`.
That method is `SQLitePaperRepository.record_failure()` from Week 5.

`IngestionResult` collects `Paper` objects in `result.successes`.
Those `Paper` objects are what Week 5 stores.

The clean separation is possible only because Week 5 defined a repository with a stable interface.
The service does not know or care how papers are stored.
It only calls the interface.

---

## 14. What belongs where

| Concern                     | Module                              |
|-----------------------------|-------------------------------------|
| Parse PDF to raw text       | `parsing/pdf_parser.py`             |
| Extract title, author       | `parsing/metadata_extractor.py`     |
| Clean text                  | `parsing/text_cleaner.py`           |
| Coordinate ingestion flow   | `services/ingestion_service.py`     |
| Save papers to database     | `storage/sqlite_repository.py`      |
| CLI arguments and output    | `cli/commands/ingest.py`            |
| Domain models               | `core/models.py`                    |
| Interface contracts         | `core/interfaces.py`                |

The rule: each module should have one reason to change.
If you change the PDF library from `pypdf` to something else, only `pdf_parser.py` changes.
If you change the database from SQLite to PostgreSQL, only `storage/` changes.
If you change the CLI framework, only `cli/` changes.
The domain models and interfaces stay stable.

---

## 15. Review questions and self-checks

**Conceptual questions:**

1. Draw the ingestion pipeline as a box-and-arrow diagram.
   Label each box with its module name.

2. What does `or ""` protect against in `page.extract_text() or ""`?

3. Why does one bad PDF not crash the whole ingestion batch?

4. What is the difference between `ParsingError` (expected failure) and the catch-all `except Exception` (unexpected failure)?

5. What is dependency injection?
   Give a one-sentence definition.

6. Why does the `IngestionService` receive its parser and repository through the constructor rather than creating them internally?

7. What would you need to change to switch from `pypdf` to a different PDF library?
   Name all files that would need to change.

8. What information does `FailedDocument` store?
   Why is each field important?

**Code-reading questions:**

9. Look at `_ingest_one` in the actual `ingestion_service.py`.
   What happens when parsing succeeds but saving to the repository fails?

10. Look at `ingest_directory`.
    What is the `skip_existing` check doing?
    Under what circumstances would you want `skip_existing=False`?

11. Why does `_ingest_one` return `Paper | None` instead of always returning a `Paper` or always raising an exception?

**Design questions:**

12. The current pipeline processes PDFs sequentially.
    If you had 1000 PDFs, how would you know the current approach is too slow?
    What information would you collect?

13. A team member suggests adding a `print()` statement inside `parse_pdf` to show progress.
    What problems does this create for testing?
    What is the better alternative?

14. You want to add a "page count filter" that skips PDFs with fewer than 3 pages.
    Where in the pipeline does this belong?
    Write a one-line pseudocode description.

**Practice tasks:**

15. Without running code, trace through the `ingest_directory` method for a directory containing:
    - `paper_a.pdf` (valid, not yet in database)
    - `paper_b.pdf` (valid, already in database, `skip_existing=True`)
    - `paper_c.pdf` (corrupt, raises `ParsingError`)

    What is in `result.successes`, `result.skipped`, and `result.failures` after the run?

16. Write a fake `DocumentParser` that raises `ParsingError` for every file.
    Use it in a test to verify that `ingest_directory` handles 3 parsing failures correctly.

17. What would `IngestionResult.success_rate` return after the scenario in question 15?
