# Week 06 - PDF Parsing Pipeline

## Learning objectives
- Read PDFs with `pypdf` and extract text page by page.
- Design an ingestion service that coordinates scanning, parsing, and storage.
- Decide what counts as a parse failure versus a parse warning.
- Preserve source metadata while extracting normalized text.
- Add the `researchops ingest` command.
- Test parsing logic with sample files and fakes.
- Track ingestion summaries using your result models.

## Project milestone
Build the first end-to-end ingestion pipeline: scan PDFs, parse text, save results, and expose the workflow through `researchops ingest`.

## Files to modify/create
- `src/researchops/parsing/pdf_parser.py`
- `src/researchops/services/ingestion.py`
- `src/researchops/cli/ingest.py`
- `tests/unit/test_pdf_parser.py`
- `tests/integration/test_ingest_pipeline.py`

## Concepts covered
PDF parsing, service orchestration, page extraction, failure handling, pipeline design, and end-to-end testing.

## Expected deliverables
- A parser that extracts text from a PDF.
- An ingestion service that returns `IngestionResult`.
- A CLI command that ingests a folder into SQLite.
- Tests for parse success and parse failure paths.

## Definition of done
- [ ] `pypdf` integration works.
- [ ] Text extraction handles multiple pages.
- [ ] Empty or broken PDFs are handled intentionally.
- [ ] Ingestion service composes scanner, parser, and repository.
- [ ] CLI `ingest` command exists.
- [ ] Integration test covers the full pipeline.
- [ ] Logs or summary output show counts.
- [ ] Persisted data can be queried after ingestion.
