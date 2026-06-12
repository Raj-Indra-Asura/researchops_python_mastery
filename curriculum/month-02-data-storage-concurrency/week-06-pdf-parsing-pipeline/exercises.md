<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises — Week 06 PDF Parsing Pipeline

## How to use this workbook

Use this workbook to turn Week 6 from “I can open a PDF” into “ResearchOps can ingest a directory, store successes, and record failures.” Start with tiny parser experiments, then move into the real parsing and ingestion files. Whenever an exercise mentions a fake parser or fake repository, remember the reason: unit tests should prove orchestration logic without depending on a real PDF file or a real SQLite database.

For every implementation task, write down the pipeline stage you are practicing: discover file, parse file, extract metadata, clean text, save paper, or record failure. That habit helps you debug real ingestion runs because you can name exactly which stage broke. Keep the work Week-6 sized: no parallel workers, no web API, no OCR system, and no future retrieval features.

---

## Warm-up exercises

### E1 — Open a real PDF

Install `pypdf` (already in dev dependencies).
Find or create a small PDF file.
Open it with `PdfReader` and print the number of pages.

### E2 — Extract and inspect text

From the PDF in E1, extract the text of each page.
Print the length of each page's text.
Print the first 200 characters of the full joined text.
Notice any whitespace artifacts or spacing problems.

### E3 — Handle None pages

Some pages return `None` from `extract_text()`.
Write a function that extracts text from a list of pages and returns an empty string for any page that returns `None`.
Test it by passing a mock page object whose `extract_text` method returns `None`.

### E4 — Read metadata

Open a PDF with `PdfReader`.
Print `reader.metadata`.
Note which fields are present and which are `None`.
Try with several different PDFs.

### E5 — Write `is_empty` logic

Write a standalone function `is_extractable(text: str) -> bool` that returns `True` if the text has more than 20 non-whitespace characters, `False` otherwise.
Test it with empty string, whitespace-only string, and a short real sentence.

### E6 — Custom parsing error

Write a `parse_pdf(path: Path) -> ParsedDocument` function that raises `ParsingError` for non-PDF files and `EmptyDocumentError` when extraction yields no text.
Test it with a file named `"not_a_pdf.txt"` that you create in `/tmp`.

---

## Code-reading exercises

### C1 — Read the parser boundary

Open `src/researchops/parsing/pdf_parser.py` and answer:

1. Why does `parse_pdf` import `pypdf` inside the function instead of at the top of the file?
2. Which checks happen before `PdfReader` is constructed?
3. Why does the page loop use `page.extract_text() or ""`?
4. How is PDF metadata converted into a plain `dict[str, str]`?
5. Which exceptions should a caller expect for unreadable or empty documents?

Explain why the parser returns `ParsedDocument` instead of directly saving a `Paper`.

### C2 — Trace metadata extraction

Open `src/researchops/parsing/metadata_extractor.py`. Read `extract_title`, `extract_author`, and `extract_abstract`, then answer:

1. Which metadata key is trusted first for the title?
2. What fallback is used when the PDF has no title metadata?
3. Why does the fallback ignore very short lines?
4. Why does `extract_author` return `None` instead of an empty string?
5. What text range does `extract_abstract` search, and why might that be enough for Week 6?

Write one example of a PDF where these heuristics would work well and one where they might fail.

### C3 — Read the ingestion service as a pipeline map

Open `src/researchops/services/ingestion_service.py` and follow `ingest_directory` into `_ingest_one`. Answer:

1. Which function discovers PDF files?
2. Where is a stable paper ID produced from the file path?
3. Where does `skip_existing` prevent duplicate work?
4. Which lines convert a `ParsedDocument` into a `Paper`?
5. Which lines record a `FailedDocument` when parsing fails?

Draw a short arrow diagram from directory path to stored paper. Include the failure path too.

---

## Implementation exercises

### M1 — Full parse_pdf function

Implement a complete `parse_pdf(path: Path) -> ParsedDocument` function that:
1. Verifies the file exists.
2. Verifies the suffix is `.pdf`.
3. Opens with `PdfReader`.
4. Extracts text from all pages with the `or ""` guard.
5. Extracts available metadata.
6. Returns a `ParsedDocument`.
7. Raises `ParsingError` on file open failure.
8. Raises `EmptyDocumentError` if no text was extracted.

### M2 — Metadata extraction heuristics

Implement `extract_title(doc: ParsedDocument) -> str` that:
1. Tries `doc.metadata.get("Title")` first.
2. Falls back to the first non-empty line of text.
3. Truncates to 200 characters.
4. Returns `"Untitled"` if nothing is found.

Implement `extract_author(doc: ParsedDocument) -> str | None` that:
1. Tries `doc.metadata.get("Author")`.
2. Returns `None` if not found or empty.

Write tests for each edge case.

### M3 — Fake parser for testing

Write a `FakePdfParser` class with a `parse(path: Path) -> ParsedDocument` method.
The fake should accept a `ParsedDocument` in its constructor and return it for any path.
Write a second fake `AlwaysFailingParser` that always raises `ParsingError`.
Both should satisfy the `DocumentParser` protocol from `core/interfaces.py`.

### M4 — IngestionService with fakes

Using your `FakePdfParser` and a real `SQLitePaperRepository` (backed by `tmp_path`):
1. Create an `IngestionService`.
2. Create a temp directory with two fake `.pdf` files (they do not need real PDF content — the fake parser ignores the content).
3. Call `ingest_directory`.
4. Assert `result.successes` has 2 entries.
5. Assert `repo.list_all()` returns 2 papers.

### M5 — Failure recording

Using `AlwaysFailingParser`:
1. Create a service.
2. Put 3 fake `.pdf` files in a temp directory.
3. Call `ingest_directory`.
4. Assert `result.failures` has 3 entries. (Note: depending on implementation, failures may be recorded via `failure_repo`.)
5. Assert `repo.list_failures()` has 3 entries.
6. Assert each `FailedDocument` has a non-empty `error_message`.

### M6 — Skip existing

1. Save a paper to the repository with a known `paper_id`.
2. Create a temp directory with a corresponding `.pdf` file.
3. Configure `PaperId.from_path` to produce that `paper_id` (you may need to create the file at the same path that was used for the original ID, or use `tmp_path` to control this).
4. Run `ingest_directory(skip_existing=True)`.
5. Assert the file appears in `result.skipped`.
6. Assert no duplicate paper was saved.

---

## Stretch exercises

### H1 — PdfParserAdapter class

Wrap `parse_pdf` in a class:

```python
class PdfParserAdapter:
    def parse(self, path: Path) -> ParsedDocument:
        return parse_pdf(path)
```

Verify it satisfies `DocumentParser` with `isinstance(PdfParserAdapter(), DocumentParser)`.
Write a test that uses the real adapter with a real small PDF from `examples/`.

### H2 — Clean text pipeline

After parsing, apply `clean_text` from `parsing/text_cleaner.py` to the raw text.
Write a test that:
1. Creates a `ParsedDocument` with raw text containing multiple blank lines and control characters.
2. Applies `clean_text`.
3. Asserts the result has no triple newlines and no control characters.

### H3 — Ingestion result summary

After calling `ingest_directory` on a mixed directory (some good PDFs, some corrupt), implement a function `format_summary(result: IngestionResult) -> str` that returns a human-readable summary:

```
Ingestion run abc12345
  Processed: 10 files
  Success:   7 (70.0%)
  Failed:    2 (20.0%)
  Skipped:   1 (10.0%)
  Duration:  2.3s
```

Write tests for the summary format.

### H4 — Idempotency test

Prove that running `ingest_directory` twice on the same directory is safe.
Write a test that:
1. Ingests a directory of files.
2. Ingests the same directory again with `skip_existing=True`.
3. Asserts `repo.list_all()` has the same number of papers after both runs.
4. Asserts no duplicates exist.

Then test with `skip_existing=False` (your implementation should handle the duplicate `paper_id` gracefully).

### H5 — Partial batch failure

Create a directory with 5 fake PDF files.
Configure your fake parser to fail for files named `broken_*.pdf` and succeed for others.
Name 2 files `broken_1.pdf` and `broken_2.pdf`.
Run ingestion.
Assert exactly 3 successes and 2 failures.
Assert the `FailedDocument` error types are correct.

---

## Brutal exercises

### B1 — Full end-to-end test suite

Write `tests/integration/test_ingest_pipeline.py` with at least 12 tests:
- Successful ingest of 1 file.
- Successful ingest of 5 files.
- All failures in a batch.
- Mixed successes and failures.
- Skip existing behavior.
- Non-PDF files ignored by scanner.
- Empty directory produces empty result.
- `IngestionResult.success_rate` is correct.
- `list_all()` after ingest returns correct count.
- `list_failures()` after failed batch returns correct count.
- Two ingestion runs do not duplicate papers.
- `IngestionResult.total` equals `len(successes) + len(failures) + len(skipped)`.

### B2 — Protocol conformance tests

Write tests that:
1. Assert `isinstance(SQLitePaperRepository(tmp_path / "t.db"), PaperRepository)`.
2. Assert `isinstance(PdfParserAdapter(), DocumentParser)`.
3. Assert your `FakePdfParser` also satisfies `DocumentParser`.

### B3 — Ingestion with real PDFs

If `examples/sample_papers/` contains real PDFs:
1. Run the ingestion service on that directory.
2. Print the result summary.
3. Assert at least one paper was stored.
4. Inspect the stored text and metadata.
5. Write assertions about the structure of the first stored paper.

---

## Written explanation exercises

### W1 — Explain a pipeline

Write a paragraph explaining what a pipeline is to someone who has never heard the term.
Use a non-software metaphor.

### W2 — Explain dependency injection

Write two versions of the same code:
- Version A: `IngestionService` creates its parser and repository internally.
- Version B: `IngestionService` receives them through the constructor.

Write a paragraph explaining which version is easier to test and why.

### W3 — Failure recording philosophy

Write a short essay (4-6 sentences) answering:
"Why is it better to record a failure as a `FailedDocument` than to simply log it and continue?"

---

## Testing exercises

### T1 — Test the fake parser satisfies the protocol

```python
def test_fake_parser_satisfies_protocol():
    from researchops.core.interfaces import DocumentParser
    fake = FakePdfParser(document=...)
    assert isinstance(fake, DocumentParser)
```

### T2 — Test that failures do not stop successes

```python
def test_one_failure_does_not_stop_other_ingestions(tmp_path):
    # Create 3 files, configure parser to fail for index 1
    ...
    result = service.ingest_directory(tmp_path)
    assert len(result.successes) == 2
    assert len(result.failures) == 1
```

### T3 — Test IngestionResult.success_rate

```python
def test_success_rate_is_correct(tmp_path):
    # Ingest 4 files, 3 succeed, 1 fails
    result = ...
    assert abs(result.success_rate - 0.75) < 0.001
```

---

## Debugging exercises

### D1 — Trace the pipeline

Add `print()` statements (for debugging only) to each stage:
- Before calling `parser.parse()`
- After successful parse
- After successful save
- On failure

Run the ingestion on a real directory.
Remove all `print()` statements after observing the flow.

### D2 — Inspect stored data

After a real ingestion run, open the database with the `sqlite3` CLI:
```bash
sqlite3 researchops.db
.headers on
SELECT id, title, num_pages, length(text) FROM papers;
```

Do the titles look correct?
Are there any obviously wrong titles (random characters, empty, or numbers)?
What would cause a bad title?

### D3 — Parse a bad PDF

Create a file `broken.pdf` with contents `"this is not a valid PDF"`.
Run `parse_pdf(Path("broken.pdf"))`.
What exception is raised?
What is the error message?
Is the error message helpful for debugging?

---

## Mini project task

### P1 — Ingestion pipeline milestone

Complete the ingestion pipeline for ResearchOps:

1. Implement or verify `parsing/pdf_parser.py` (parse_pdf function + PdfParserAdapter class).
2. Implement or verify `parsing/metadata_extractor.py` (extract_title, extract_author).
3. Implement or verify `services/ingestion_service.py` (IngestionService class).
4. Wire up `cli/commands/ingest.py` to accept `<directory>` and `--db`.
5. Run `researchops ingest examples/sample_papers/ --db /tmp/test.db`.
6. Run `researchops papers list --db /tmp/test.db` to verify storage.
7. Write at least 8 integration tests in `tests/integration/test_ingest_pipeline.py`.
8. Run `pytest` and confirm all tests pass.
9. Run `ruff check src tests` and confirm no lint errors.

Deliverable: a working ingest command that stores papers and records failures.
## Completion checklist

- [ ] I can run a small `pypdf` experiment and explain each observed failure.
- [ ] I read `pdf_parser.py`, `metadata_extractor.py`, and `ingestion_service.py` before changing pipeline code.
- [ ] I can explain the difference between `ParsedDocument`, `Paper`, `FailedDocument`, and `IngestionResult`.
- [ ] I tested successful ingestion with fakes and did not require real PDFs for unit tests.
- [ ] I tested at least one parse failure and verified it becomes a recorded failure.
- [ ] I can explain why the service receives parser and repository objects instead of constructing them internally.
- [ ] `pytest tests/unit/test_ingestion_service.py -v` passes.
- [ ] `pytest -q` and `ruff check src tests` pass before I mark Week 6 complete.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
