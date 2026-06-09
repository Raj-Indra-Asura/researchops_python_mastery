<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 06 Notes — PDF Parsing Pipeline

## Chapter overview

Week 06 is the chapter where ResearchOps turns raw PDF files into structured project data.

The chapter title is **Raw bytes become structured knowledge**.

That phrase is literal: a PDF starts as bytes on disk, and the pipeline turns those bytes into `Paper` or `FailedDocument` records.

The visible milestone is the syllabus command `researchops ingest ./papers`, with the sample validation path `./examples/sample_papers`.

The command must extract text and metadata, save successful papers, and record failures instead of dropping them.

This is not a random PDF lesson; it is the first complete data-ingestion workflow in the ResearchOps platform.

By the end, you should be able to trace a directory path through discovery, parsing, cleaning, metadata extraction, storage, and reporting.

The happy path is `PDF -> ParsedDocument -> Paper -> SQLite`.

The failure path is `PDF -> ParsingError or EmptyDocumentError -> FailedDocument -> SQLite`.

Both paths are equally important because real research libraries always contain imperfect files.

- Pipeline stage: Directory of PDFs.
- Pipeline stage: find `.pdf` files.
- Pipeline stage: parse each file with `pypdf`.
- Pipeline stage: clean extracted text.
- Pipeline stage: derive title and author hints.
- Pipeline stage: save a `Paper`.
- Pipeline stage: record a `FailedDocument` for parse failures.
- Pipeline stage: return an `IngestionResult` summary.
A complete pass through this chapter means you can run the command, read the code, break one PDF on purpose, inspect the failure, and explain why the rest of the batch continues.

## What you already know from previous weeks

- Week 1 gave you repository scaffold, core models, and the idea that packages have separate responsibilities.
  In Week 6, that earlier skill appears inside the ingestion pipeline rather than as a separate exercise.
- Week 2 gave you `pathlib.Path`, exceptions, logging, and safe file handling.
  In Week 6, that earlier skill appears inside the ingestion pipeline rather than as a separate exercise.
- Week 3 gave you domain modeling with names such as `Paper`, `ParsedDocument`, `FailedDocument`, and `IngestionResult`.
  In Week 6, that earlier skill appears inside the ingestion pipeline rather than as a separate exercise.
- Week 4 gave you CLI shape, entry points, and the rule that terminal commands should delegate business work.
  In Week 6, that earlier skill appears inside the ingestion pipeline rather than as a separate exercise.
- Week 5 gave you SQLite persistence and repository methods that hide SQL from services.
  In Week 6, that earlier skill appears inside the ingestion pipeline rather than as a separate exercise.
If you are unsure where a concept came from, trace one concrete file named `paper.pdf` through the pipeline.
When the code asks whether the path exists, that is Week 2.
When the parser returns `ParsedDocument`, that is Week 3.
When the user runs `researchops ingest`, that is Week 4.
When the service saves a `Paper`, that is Week 5.
The new Week 6 skill is coordination: several already-known ideas now have to work together.

## What problem this week solves

- **Discovery:** A user gives a directory, not a hand-written list of every file.
  Without this part, the ingest command gives the learner an incomplete or misleading result.
- **Extraction:** The system must open each PDF and recover page text.
  Without this part, the ingest command gives the learner an incomplete or misleading result.
- **Metadata:** The system must keep useful facts such as title, author, page count, and file size.
  Without this part, the ingest command gives the learner an incomplete or misleading result.
- **Cleanup:** The system must normalize text enough that later commands can read it.
  Without this part, the ingest command gives the learner an incomplete or misleading result.
- **Persistence:** Successful documents must become stored `Paper` records.
  Without this part, the ingest command gives the learner an incomplete or misleading result.
- **Failure recording:** Unreadable or empty documents must become stored `FailedDocument` records.
  Without this part, the ingest command gives the learner an incomplete or misleading result.
- **Reporting:** The user must see counts for successes, failures, and skips.
  Without this part, the ingest command gives the learner an incomplete or misleading result.
The central problem is partial success.
A batch of PDFs can contain five good files, one corrupt file, and one scanned image-only file.
The correct result is not all-or-nothing.
The correct result is five saved papers and two recorded failures.
Silent failure is dangerous because the database looks complete even when documents were lost.
Week 6 teaches you to make failures visible and queryable.

## Beginner mental model

Use the conveyor-belt mental model.
A directory enters the belt.
The scanner station finds PDF paths.
The parser station turns one path into a `ParsedDocument`.
The cleaner station improves text shape without changing the parser responsibility.
The metadata station chooses title and author hints.
The service station decides whether to save a paper or record a failure.
The repository station writes durable records.
The result station counts what happened.

- **Input:** the concrete thing entering a stage.
- **Owner:** the module or object responsible for the decision.
- **Transformation:** the useful change made by the stage.
- **Proof:** the command or test that confirms behavior.
For every Week 6 feature, ask those four questions before editing code.
If you cannot name the owner, you are likely about to put code in the wrong layer.
If you cannot name the proof, you are likely about to make an untested change.

## Core vocabulary

- **Pipeline:** a sequence of stages where each output becomes the next input.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **PDF:** a page-layout file format optimized for viewing and printing, not always for text extraction.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Text extraction:** recovering strings from PDF page instructions.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **pypdf:** the third-party library used this week to read PDF pages and metadata.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Optional dependency:** a package needed for one feature but not for the entire project.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Parser:** code that turns one source file into a structured parsed result.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **ParsedDocument:** the parser output containing path, raw text, page count, file size, and metadata.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Raw text:** text as the PDF library extracted it before ResearchOps cleanup.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Cleaned text:** text after simple normalization such as whitespace cleanup.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Metadata:** descriptive facts such as title, author, and PDF header fields.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Heuristic:** a practical rule that often works but is not guaranteed.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Paper:** the successful stored ResearchOps record.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **FailedDocument:** the stored record for a file that could not become a paper.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **IngestionResult:** the summary of one ingestion run.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Idempotency:** safe repeated execution without accidental duplicates.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Failure path:** the planned route for errors.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.
- **Integration test:** a test that exercises multiple real components together.
  In Week 6, this word helps you name one piece of the ingestion pipeline clearly.

## Concept explanations from first principles

### Third-party library integration (`pypdf`)
- Plain meaning: Python does not ship a complete PDF text extractor, so ResearchOps uses `pypdf` inside the parsing layer only.
- ResearchOps use: The rest of the system should ask the parser for `ParsedDocument` and should not learn the `pypdf` API.
- Beginner question: what exact value enters this concept?
- Output question: what exact value should leave this concept?
- Failure question: what can be missing, malformed, empty, duplicated, or unreadable?
- Test question: which test would catch the mistake before a learner trusts the command?
- Mastery signal: you can explain the concept without using the words "magic" or "somehow".

### Optional dependencies and graceful import errors
- Plain meaning: PDF parsing is optional project capability, so `pypdf` belongs in the `parsing` extra.
- ResearchOps use: A missing dependency should raise a ResearchOps parsing error with the install hint `pip install -e ".[parsing]"` or the full Week 6 install command.
- Beginner question: what exact value enters this concept?
- Output question: what exact value should leave this concept?
- Failure question: what can be missing, malformed, empty, duplicated, or unreadable?
- Test question: which test would catch the mistake before a learner trusts the command?
- Mastery signal: you can explain the concept without using the words "magic" or "somehow".

### Parsers return domain objects, not strings
- Plain meaning: A string alone loses source path, page count, file size, and metadata.
- ResearchOps use: `ParsedDocument` keeps those facts together so later stages can build a useful `Paper`.
- Beginner question: what exact value enters this concept?
- Output question: what exact value should leave this concept?
- Failure question: what can be missing, malformed, empty, duplicated, or unreadable?
- Test question: which test would catch the mistake before a learner trusts the command?
- Mastery signal: you can explain the concept without using the words "magic" or "somehow".

### `IngestionService` orchestration
- Plain meaning: The service owns the order: discover, skip existing, parse, clean, save, record failure, summarize.
- ResearchOps use: It should coordinate collaborators rather than become a PDF library or SQL module.
- Beginner question: what exact value enters this concept?
- Output question: what exact value should leave this concept?
- Failure question: what can be missing, malformed, empty, duplicated, or unreadable?
- Test question: which test would catch the mistake before a learner trusts the command?
- Mastery signal: you can explain the concept without using the words "magic" or "somehow".

### Real parsing failures
- Plain meaning: PDFs can be corrupt, encrypted, image-only, missing, or unsupported.
- ResearchOps use: The system should record a `FailedDocument` for failures so the learner can inspect what happened.
- Beginner question: what exact value enters this concept?
- Output question: what exact value should leave this concept?
- Failure question: what can be missing, malformed, empty, duplicated, or unreadable?
- Test question: which test would catch the mistake before a learner trusts the command?
- Mastery signal: you can explain the concept without using the words "magic" or "somehow".

### Integration tests with real PDF fixtures
- Plain meaning: Fake parsers are excellent for service decisions but cannot prove real extraction.
- ResearchOps use: A real integration test proves parser, service, and SQLite wiring work together.
- Beginner question: what exact value enters this concept?
- Output question: what exact value should leave this concept?
- Failure question: what can be missing, malformed, empty, duplicated, or unreadable?
- Test question: which test would catch the mistake before a learner trusts the command?
- Mastery signal: you can explain the concept without using the words "magic" or "somehow".

## ResearchOps-specific application

- `src/researchops/parsing/pdf_parser.py` — opens PDFs, extracts page text, reads metadata, returns `ParsedDocument`, and raises parsing exceptions.
  Study this file only for that responsibility; do not make it own unrelated work.
- `src/researchops/parsing/text_cleaner.py` — normalizes extracted text without knowing about PDF files or SQLite.
  Study this file only for that responsibility; do not make it own unrelated work.
- `src/researchops/parsing/metadata_extractor.py` — derives title and author hints from parsed document metadata and text.
  Study this file only for that responsibility; do not make it own unrelated work.
- `src/researchops/services/ingestion_service.py` — coordinates discovery, parsing, saving, failure recording, skipping, and result summary.
  Study this file only for that responsibility; do not make it own unrelated work.
- `src/researchops/cli/commands/ingest.py` — accepts user arguments, wires concrete parser and repository implementations, and prints a summary.
  Study this file only for that responsibility; do not make it own unrelated work.
- `src/researchops/storage/sqlite_repository.py` — persists successful papers and failed document records.
  Study this file only for that responsibility; do not make it own unrelated work.
- `tests/unit/test_ingestion_service.py` — checks orchestration with fakes and includes current service test names.
  Study this file only for that responsibility; do not make it own unrelated work.
- `tests/integration/test_ingestion_service.py` — is the syllabus-named full pipeline test with sample PDFs.
  Study this file only for that responsibility; do not make it own unrelated work.
The ResearchOps-specific rule is: if you change where a decision lives, you change how easy the project is to teach.
Keep parsing in parsing, orchestration in services, wiring in CLI, and persistence in storage.

## Code examples with line-by-line explanation

### Example 1: parser shape

```python
from pathlib import Path
from researchops.core.models import ParsedDocument

def parse_pdf(path: Path) -> ParsedDocument:
    reader = pypdf.PdfReader(str(path))
    pages_text: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)

    full_text = "\n".join(pages_text)

    return ParsedDocument(
        source_path=path,
        raw_text=full_text,
        num_pages=len(reader.pages),
        file_size_bytes=path.stat().st_size,
        metadata={},
    )
```

- Line 1: `from pathlib import Path`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 2: `from researchops.core.models import ParsedDocument`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 4: `def parse_pdf(path: Path) -> ParsedDocument:`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 5: `    reader = pypdf.PdfReader(str(path))`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 6: `    pages_text: list[str] = []`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 8: `    for page in reader.pages:`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 9: `        text = page.extract_text() or ""`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 10: `        pages_text.append(text)`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 12: `    full_text = "\n".join(pages_text)`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 14: `    return ParsedDocument(`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 15: `        source_path=path,`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 16: `        raw_text=full_text,`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 17: `        num_pages=len(reader.pages),`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 18: `        file_size_bytes=path.stat().st_size,`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 19: `        metadata={},`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.
- Line 20: `    )`
  This line contributes one traceable step in turning a PDF path into a structured parsed document.

### Example 2: one-file ingestion

```python
def _ingest_one(self, path: Path, paper_id: str) -> Paper | None:
    try:
        doc = self._parser.parse(path)
    except ParsingError as exc:
        failure = FailedDocument(
            source_path=path,
            error_message=str(exc),
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

    self._paper_repo.save(paper)
    return paper
```

- Line 1: `def _ingest_one(self, path: Path, paper_id: str) -> Paper | None:`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 2: `    try:`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 3: `        doc = self._parser.parse(path)`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 4: `    except ParsingError as exc:`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 5: `        failure = FailedDocument(`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 6: `            source_path=path,`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 7: `            error_message=str(exc),`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 8: `            error_type=type(exc).__name__,`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 9: `        )`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 10: `        self._failure_repo.record_failure(failure)`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 11: `        return None`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 13: `    paper = Paper(`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 14: `        id=paper_id,`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 15: `        title=extract_title(doc),`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 16: `        source_path=str(path),`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 17: `        text=clean_text(doc.raw_text),`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 18: `        num_pages=doc.num_pages,`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 19: `        file_size_bytes=doc.file_size_bytes,`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 20: `        author=extract_author(doc),`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 21: `        abstract=None,`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 22: `    )`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 24: `    self._paper_repo.save(paper)`
  Read this line as part of the happy path or the failure path, then name which model it touches.
- Line 25: `    return paper`
  Read this line as part of the happy path or the failure path, then name which model it touches.

### Example 3: directory loop

```python
for pdf_path in pdfs:
    paper_id = str(PaperId.from_path(pdf_path))

    if skip_existing and self._paper_repo.exists(paper_id):
        result.skipped.append(pdf_path)
        continue

    paper = self._ingest_one(pdf_path, paper_id)
    if paper is not None:
        result.successes.append(paper)
```

- Line 1: `for pdf_path in pdfs:`
  This line keeps the batch readable by delegating detailed work to focused helpers.
- Line 2: `    paper_id = str(PaperId.from_path(pdf_path))`
  This line keeps the batch readable by delegating detailed work to focused helpers.
- Line 4: `    if skip_existing and self._paper_repo.exists(paper_id):`
  This line keeps the batch readable by delegating detailed work to focused helpers.
- Line 5: `        result.skipped.append(pdf_path)`
  This line keeps the batch readable by delegating detailed work to focused helpers.
- Line 6: `        continue`
  This line keeps the batch readable by delegating detailed work to focused helpers.
- Line 8: `    paper = self._ingest_one(pdf_path, paper_id)`
  This line keeps the batch readable by delegating detailed work to focused helpers.
- Line 9: `    if paper is not None:`
  This line keeps the batch readable by delegating detailed work to focused helpers.
- Line 10: `        result.successes.append(paper)`
  This line keeps the batch readable by delegating detailed work to focused helpers.

### Worked scenario: tracing three files through the pipeline

Imagine the input directory contains exactly three entries.

- `good.pdf` is a normal digitally-created PDF with embedded text.
- `scan.pdf` is a scanned image-only PDF with no embedded text.
- `notes.txt` is a non-PDF file that happens to sit in the same folder.

- **Discovery:** `find_pdfs` should include `good.pdf` and `scan.pdf` because their suffix is `.pdf`.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Discovery:** `notes.txt` should not enter the parser because it is not a PDF candidate.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Parsing good.pdf:** the parser opens the file with `pypdf.PdfReader`.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Parsing good.pdf:** the parser loops through pages and collects text strings.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Parsing good.pdf:** the parser builds a `ParsedDocument` with path, raw text, page count, file size, and metadata.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Cleaning good.pdf:** the service passes raw text to `clean_text` before storing the `Paper`.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Metadata good.pdf:** the service asks the metadata extractor for a title and optional author.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Saving good.pdf:** the repository saves one successful `Paper` record.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Parsing scan.pdf:** `pypdf` may return empty strings because the pages contain pictures of text, not embedded text.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Failure scan.pdf:** the parser should raise `EmptyDocumentError` when the resulting document is empty.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Recording scan.pdf:** the service should convert that exception into a `FailedDocument` record.
  This is a concrete checkpoint you can verify with a test or manual command.
- **Summary:** the final result should communicate one success, one failure, and zero or one skipped files depending on existing state.
  This is a concrete checkpoint you can verify with a test or manual command.

The important beginner lesson is that `scan.pdf` is not invisible.

It attempted ingestion and failed for a recorded reason.

That is better than pretending only `good.pdf` existed.

### Worked example: optional dependency failure

A learner may install only the base package.

The base package can run commands that do not parse PDFs.

When the learner runs PDF parsing, the parser needs `pypdf`.

If `pypdf` is missing, Python raises `ImportError`.

The parser should catch that import error.

The parser should raise `ParsingError` with an installation hint.

The service can then record that as a failed document if it happens during batch ingestion.

The CLI can display a readable result instead of a traceback wall.

```python
try:
    import pypdf
except ImportError as exc:
    raise ParsingError(
        "pypdf is required for PDF parsing. "
        "Install it with: pip install 'researchops[parsing]'"
    ) from exc
```

- Line 1: `try:`
  The parser is about to run code that might fail because an optional dependency may be absent.
- Line 2: `    import pypdf`
  The third-party package is imported only when the parsing feature is actually needed.
- Line 3: `except ImportError as exc:`
  This catches the missing-package case specifically rather than hiding every possible problem.
- Line 4: `    raise ParsingError(`
  The low-level import problem becomes a ResearchOps parsing problem.
- Line 5: `        "pypdf is required for PDF parsing. "`
  The message teaches the learner what to install next.
- Line 6: `        "Install it with: pip install 'researchops[parsing]'"`
  The message teaches the learner what to install next.
- Line 7: `    ) from exc`
  The original exception remains attached for deeper debugging.

### Trace table practice

| Stage | Input | Output on success | Output on failure | Proof |
|---|---|---|---|---|
| Discovery | directory path | list of PDF paths | empty list or invalid-directory result | unit test for recursive and non-recursive discovery |
| Parser | one PDF path | `ParsedDocument` | `ParsingError` or `EmptyDocumentError` | parser unit test |
| Cleaner | raw text | normalized text | normally no exception for ordinary strings | text cleaner unit test |
| Metadata extractor | `ParsedDocument` | title and optional author | fallback values | metadata extractor unit test |
| Service | PDF path plus collaborators | saved `Paper` | recorded `FailedDocument` | ingestion service unit test |
| CLI | terminal arguments | printed summary | readable error or zero-count summary | manual command |
| Repository | domain model | durable SQLite row | storage exception or duplicate behavior | integration test |

Fill this table before changing code.

If a row has no proof, add or identify a test.

If two rows name the same owner, check whether responsibilities are mixed.

If a failure output says only "log it", ask where the learner can query it later.

If the CLI is the owner of parsing, move that logic down into parsing and service layers.

If the parser is the owner of saving, move that logic out to the service and repository.

If the service is the owner of PDF page extraction, move that logic into the parser.

If storage is the owner of title extraction, move that logic into the metadata extractor.

### Mini lab: predict before running

1. Predict how many `.pdf` files discovery should find before running the command.
   After running validation, compare the actual evidence to this prediction.
2. Predict which files should become `Paper` records.
   After running validation, compare the actual evidence to this prediction.
3. Predict which files should become `FailedDocument` records.
   After running validation, compare the actual evidence to this prediction.
4. Predict whether a second run should skip anything.
   After running validation, compare the actual evidence to this prediction.
5. Predict which command will prove the successful records exist.
   After running validation, compare the actual evidence to this prediction.
6. Predict which command will prove the failed records exist.
   After running validation, compare the actual evidence to this prediction.
7. Predict which test protects parser behavior.
   After running validation, compare the actual evidence to this prediction.
8. Predict which test protects service behavior.
   After running validation, compare the actual evidence to this prediction.
9. Predict which test protects real component wiring.
   After running validation, compare the actual evidence to this prediction.
10. Predict which module you would edit if text cleanup is wrong.
   After running validation, compare the actual evidence to this prediction.
11. Predict which module you would edit if title fallback is wrong.
   After running validation, compare the actual evidence to this prediction.
12. Predict which module you would edit if the CLI summary is wrong.
   After running validation, compare the actual evidence to this prediction.
13. Predict which module you would edit if SQLite rows are wrong.
   After running validation, compare the actual evidence to this prediction.
14. Predict what should happen when `pypdf` is missing.
   After running validation, compare the actual evidence to this prediction.
15. Predict what should happen when a PDF has pages but no extractable text.
   After running validation, compare the actual evidence to this prediction.
16. Predict what should happen when the directory is empty.
   After running validation, compare the actual evidence to this prediction.
17. Predict what should happen when a nested PDF exists and recursive mode is false.
   After running validation, compare the actual evidence to this prediction.
18. Predict what should happen when recursive mode is true.
   After running validation, compare the actual evidence to this prediction.
19. Predict why a logged-only failure is insufficient.
   After running validation, compare the actual evidence to this prediction.
20. Predict why adding future worker behavior would distract from this week.
   After running validation, compare the actual evidence to this prediction.

## Common beginner mistakes

- **Mistake:** Returning only a string from the parser.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Importing `pypdf` inside the service layer.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Letting one corrupt PDF crash the whole batch.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Catching an exception and doing nothing.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Logging a failure but not saving `FailedDocument`.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Trusting PDF metadata as guaranteed truth.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Forgetting that `extract_text()` can return `None`.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Saving empty extracted text as a successful paper.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Putting text cleanup inside the CLI.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Hard-coding the database path inside the service.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Treating skipped files as failures.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Using a real database in every unit test.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Skipping the integration test because fakes pass.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Adding worker options to Week 6 validation.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Adding OCR before local text extraction is clear.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.
- **Mistake:** Changing many layers without a focused proof.
  **Why it hurts:** it hides a boundary, hides evidence, or makes the pipeline harder to debug.
  **Better move:** keep the stage focused, record evidence, and prove behavior with a targeted test.

## Debugging guidance

- **Symptom:** No PDFs are found.
  **Inspect:** inspect the sample directory with `find examples/sample_papers -maxdepth 2 -type f`.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
- **Symptom:** `pypdf` is missing.
  **Inspect:** reinstall with `python -m pip install -e ".[dev,parsing,storage]"`.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
- **Symptom:** A PDF yields empty text.
  **Inspect:** decide whether it is image-only and confirm `EmptyDocumentError` handling.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
- **Symptom:** The title looks wrong.
  **Inspect:** inspect metadata and first-line fallback behavior.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
- **Symptom:** The CLI prints a placeholder.
  **Inspect:** check `src/researchops/cli/commands/ingest.py` wiring.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
- **Symptom:** Papers are not listed after ingest.
  **Inspect:** confirm the ingest and papers commands use the same database.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
- **Symptom:** Failures are not visible.
  **Inspect:** check `record_failure` and `researchops papers failed`.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
- **Symptom:** Recursive tests fail.
  **Inspect:** draw the directory tree and compare recursive versus non-recursive discovery.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
- **Symptom:** Unit tests pass but manual ingest fails.
  **Inspect:** suspect CLI wiring or real dependency setup.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
- **Symptom:** Manual ingest works but tests fail.
  **Inspect:** suspect hard-coded paths or missing fakes.
  **Reason:** debugging one stage at a time is faster than guessing across the whole pipeline.
When stuck, make a trace table with columns: stage, input, output, failure, proof.
Fill one row at a time until the broken stage becomes obvious.

## Design tradeoffs

- **Sequential processing:** easier to teach and trace than faster approaches; Week 6 values correctness over speed.
  The chosen tradeoff should make the Week 6 milestone more reliable and easier to explain.
- **Raw text vs cleaned text:** parser output should remain raw, while stored `Paper` text can be cleaned by a dedicated helper.
  The chosen tradeoff should make the Week 6 milestone more reliable and easier to explain.
- **Raise errors vs return failure objects:** parser raises when it cannot parse; service converts that exception into stored failure data.
  The chosen tradeoff should make the Week 6 milestone more reliable and easier to explain.
- **PDF metadata vs fallback text:** metadata is convenient but unreliable, so title extraction should have a fallback.
  The chosen tradeoff should make the Week 6 milestone more reliable and easier to explain.
- **Fakes vs real fixtures:** fakes prove decisions, real fixtures prove integration.
  The chosen tradeoff should make the Week 6 milestone more reliable and easier to explain.
- **Broad exception handling:** dangerous if careless, useful around one-file ingestion so a batch can continue.
  The chosen tradeoff should make the Week 6 milestone more reliable and easier to explain.
- **Strict empty-document policy:** prevents blank papers from polluting later search results.
  The chosen tradeoff should make the Week 6 milestone more reliable and easier to explain.
- **Beginner readability vs compact code:** explicit loops can be better teaching code than clever one-liners.
  The chosen tradeoff should make the Week 6 milestone more reliable and easier to explain.

## Testing implications

- Command: `pytest tests/integration/test_ingestion_service.py -v`
  This command protects one part of the Week 6 pipeline or the full regression surface.
- Command: `pytest tests/unit/test_ingestion_service.py -v`
  This command protects one part of the Week 6 pipeline or the full regression surface.
- Command: `pytest tests/unit/test_pdf_parser.py -v`
  This command protects one part of the Week 6 pipeline or the full regression surface.
- Command: `pytest tests/unit/test_metadata_extractor.py -v`
  This command protects one part of the Week 6 pipeline or the full regression surface.
- Command: `pytest tests/unit/test_text_cleaner.py -v`
  This command protects one part of the Week 6 pipeline or the full regression surface.
- Command: `pytest -k "ingestion_service or pdf_parser or metadata_extractor or text_cleaner" -v`
  This command protects one part of the Week 6 pipeline or the full regression surface.
- Command: `pytest -q`
  This command protects one part of the Week 6 pipeline or the full regression surface.
Current service test names to understand:
- `TestIngestDirectory::test_ingests_single_pdf`
- `TestIngestDirectory::test_ingests_multiple_pdfs`
- `TestIngestDirectory::test_parse_failure_recorded`
- `TestIngestDirectory::test_unexpected_error_recorded_as_failure`
- `TestIngestDirectory::test_skip_existing_paper`
- `TestIngestDirectory::test_no_skip_when_skip_existing_false`
- `TestIngestDirectory::test_empty_directory_returns_empty_result`
- `TestIngestDirectory::test_invalid_directory_returns_empty_result`
- `TestIngestDirectory::test_result_has_run_id`
- `TestIngestDirectory::test_recursive_discovers_nested_pdfs`
- `TestIngestDirectory::test_nonrecursive_misses_nested_pdfs`
The syllabus specifically names `tests/integration/test_ingestion_service.py` as the Week 6 full-pipeline test.
If a parser test file is missing, that is a Week 6 implementation gap, not a reason to skip parser validation.

## Architecture implications

- `core/` must not import parser, storage, CLI, API, ML, workers, or search packages.
  This preserves the dependency direction taught by the project architecture.
- `parsing/pdf_parser.py` may import `pypdf` because it is infrastructure.
  This preserves the dependency direction taught by the project architecture.
- `services/ingestion_service.py` should not import `SQLitePaperRepository`.
  This preserves the dependency direction taught by the project architecture.
- `cli/commands/ingest.py` may wire `PdfParser` and `SQLitePaperRepository` into `IngestionService`.
  This preserves the dependency direction taught by the project architecture.
- `storage/sqlite_repository.py` may know SQL because persistence is its job.
  This preserves the dependency direction taught by the project architecture.
- Failures belong in domain records, not only in terminal output.
  This preserves the dependency direction taught by the project architecture.
- The command line should display results, not own business policy.
  This preserves the dependency direction taught by the project architecture.
- Do not add future parallel or API architecture to Week 6.
  This preserves the dependency direction taught by the project architecture.

## How this connects to AI engineering / ML research

- Search quality depends on extracted text quality.
  This is why Week 6 is an AI-engineering foundation rather than merely a file-format exercise.
- A classifier trained on bad extraction learns from bad data.
  This is why Week 6 is an AI-engineering foundation rather than merely a file-format exercise.
- A question-answering system with missing papers gives incomplete answers.
  This is why Week 6 is an AI-engineering foundation rather than merely a file-format exercise.
- Failure records support research integrity because they show which sources were attempted.
  This is why Week 6 is an AI-engineering foundation rather than merely a file-format exercise.
- Metadata quality affects how humans trust later search results.
  This is why Week 6 is an AI-engineering foundation rather than merely a file-format exercise.
- Ingestion counts make data preparation reproducible.
  This is why Week 6 is an AI-engineering foundation rather than merely a file-format exercise.
- Reliable local ingestion is a prerequisite for later AI features.
  This is why Week 6 is an AI-engineering foundation rather than merely a file-format exercise.
- Do not jump to models before the document pipeline is observable.
  This is why Week 6 is an AI-engineering foundation rather than merely a file-format exercise.

## Mini quizzes

1. What is the input to `researchops ingest ./examples/sample_papers`?
2. Why should the parser return `ParsedDocument`?
3. What does `page.extract_text() or ""` protect against?
4. Why can a scanned PDF produce no text?
5. Which layer should import `pypdf`?
6. Which layer records a `FailedDocument`?
7. Why is a skipped file not a failed file?
8. What does `skip_existing` protect against?
9. Why are PDF metadata fields only hints?
10. What is the syllabus-named integration test?
11. Why do service tests use fakes?
12. Why is a manual `papers failed` command useful?
13. What future-week feature should not be implemented now?
14. Draw the happy path.
15. Draw the failure path.

## Explain-it-aloud prompts

- Explain why PDFs are harder than plain text files.
- Explain how one PDF path becomes `ParsedDocument`.
- Explain why `FailedDocument` is data, not just an error.
- Explain why the service coordinates but does not parse.
- Explain why the CLI wires concrete objects but should not contain SQL.
- Explain the difference between parser tests and service tests.
- Explain why the integration test matters even if unit tests pass.
- Explain how idempotency affects a second ingest run.
- Explain how this week prepares later search.
- Explain why Week 6 stays sequential.

## What to memorize

- Pipeline order: discover -> parse -> clean -> extract metadata -> save or record failure -> summarize.
- Main files: parser, cleaner, metadata extractor, ingestion service, ingest CLI, SQLite repository.
- Main models: `ParsedDocument`, `Paper`, `FailedDocument`, `IngestionResult`.
- Install command: `python -m pip install -e ".[dev,parsing,storage]"`.
- Syllabus validation commands: ingest sample papers, list papers, list failures, run integration test.
- Phrase: failures are data.
- Rule: `extract_text()` can return `None`.
- Rule: metadata is a hint.
- Rule: no Week 8 worker behavior in Week 6.

## What to understand deeply

- Understand deeply: Why a parser returning a domain object makes later stages safer.
  You should be able to give a concrete ResearchOps example, not just define the phrase.
- Understand deeply: Why recording failures is more trustworthy than printing errors.
  You should be able to give a concrete ResearchOps example, not just define the phrase.
- Understand deeply: Why service orchestration is separate from infrastructure.
  You should be able to give a concrete ResearchOps example, not just define the phrase.
- Understand deeply: Why fakes make service tests deterministic.
  You should be able to give a concrete ResearchOps example, not just define the phrase.
- Understand deeply: Why real fixtures still matter.
  You should be able to give a concrete ResearchOps example, not just define the phrase.
- Understand deeply: Why repeated commands should not create accidental duplicates.
  You should be able to give a concrete ResearchOps example, not just define the phrase.
- Understand deeply: Why ingestion quality affects every later AI feature.
  You should be able to give a concrete ResearchOps example, not just define the phrase.
- Understand deeply: Why clear boundaries help beginners debug.
  You should be able to give a concrete ResearchOps example, not just define the phrase.

## What not to worry about yet

- Do not worry about multiprocessing yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about async ingestion yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about OCR yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about perfect title extraction yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about perfect author extraction yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about citation parsing yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about semantic search yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about RAG prompts yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about remote fetching yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about web APIs yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about elaborate progress dashboards yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about every obscure PDF edge case yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.
- Do not worry about perfect performance yet.
  Keep the Week 6 local PDF parsing pipeline correct, visible, and teachable.

## Bridge to next week

Week 6 fills the database with paper text that later features can use.
The stored text becomes the input for search and analysis.
The stored metadata becomes context for human-facing results.
The stored failures become a repair list for data quality.
Future chapters will add more sophisticated processing, but they depend on this foundation.
Carry forward the input-owner-transformation-proof habit.
Carry forward the failures-are-data habit.
Do not move forward until you can explain both the happy path and the failure path aloud.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
