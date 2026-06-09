# Break It - Week 06 PDF Parsing Pipeline

## Intentional failure experiments
1. Try to parse a non-PDF file renamed with a `.pdf` suffix.
2. Use a zero-byte PDF and decide how the parser should report it.
3. Force `extract_text()` to return empty strings and inspect downstream behavior.
4. Disconnect the repository or point it at a bad database path during ingest.
5. Ingest the same directory twice and note duplicate-handling behavior.

## Debugging tasks
- Print page counts before extraction.
- Log the source path for every parse failure.
- Run only pipeline tests with `pytest -k ingest_pipeline -v`.

## Edge cases to explore
- Multi-page PDFs.
- PDFs with image-only pages.
- PDFs with unusual Unicode text.
- Duplicate source paths across runs.

## What did you learn?
- Which pipeline stage failed most often?
- What information made parse failures actionable?
- How would you extend the system for OCR later?
