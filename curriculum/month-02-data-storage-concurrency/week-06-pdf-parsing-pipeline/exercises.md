# Exercises - Week 06 PDF Parsing Pipeline

## Warm-up exercises
1. Open a sample PDF with `PdfReader` and print the number of pages.
2. Extract text from one page and inspect spacing artifacts.
3. Handle a `None` page extraction result safely.
4. Raise a custom parse error when extracted text is blank.

## Project exercises
1. Implement `pdf_parser.py` with an `extract_text` function.
2. Build an ingestion service that scans, parses, and stores documents.
3. Add `researchops ingest <path> --db <file>`.
4. Write an integration test for a successful ingest and one failing PDF.

## Stretch exercises
1. Store page counts and extraction timing.
2. Add an option to skip already-ingested source paths.
3. Add a parse quality warning when text is suspiciously short.

## Writing questions
1. Why are PDFs harder than plain text files?
2. Which boundary in the pipeline felt most useful?
3. What should the ingestion summary report to a user?
4. What failure deserves a retry versus a permanent skip?
