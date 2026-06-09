# Notes - Week 06 PDF Parsing Pipeline

A pipeline is a sequence of steps where the output of one step becomes the input of the next. In ResearchOps, the ingestion pipeline looks something like this: discover files, parse PDFs, build domain objects, store successful results, and record failures. Thinking in steps helps you debug because you can ask which stage is wrong instead of treating the whole system as one giant mystery.

`pypdf` is a practical library for extracting text from PDFs. PDFs are tricky because they were designed for visual layout, not clean text extraction. Some PDFs yield excellent text, while others produce broken spacing, missing characters, or empty output.

```python
from pathlib import Path
from pypdf import PdfReader


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    parts: list[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()
```

Notice the `or ""`. Some page extractors return `None`, so the parser must normalize that instead of crashing.

A parser should do one job: turn a file into parsed content or a domain failure. It should not directly talk to the CLI or database. That work belongs to a service layer.

```python
def parse_paper(paper: Paper) -> ParsedDocument:
    text = extract_text(paper.source_path)
    if not text:
        raise ValueError(f"No text extracted from {paper.source_path}")
    return ParsedDocument(paper_id=paper.id, title=paper.title, text=text)
```

The ingestion service coordinates multiple collaborators.

```python
class IngestionService:
    def __init__(self, scanner, parser, repository) -> None:
        self.scanner = scanner
        self.parser = parser
        self.repository = repository

    def ingest_directory(self, root: Path) -> IngestionResult:
        papers = self.scanner.scan(root)
        ...
```

This design keeps each component testable. You can test the parser with a sample PDF, the repository with SQLite, and the service with fakes or integration tests.

A useful service returns a summary object, not just side effects. `IngestionResult` can include parsed documents, failed documents, and counts. That allows the CLI to print a summary and allows tests to assert on outcomes without scraping logs.

You also need to decide how to classify failures. A corrupted PDF may be a hard failure. An empty text extraction may be a soft failure if you want to revisit OCR later. Capture that decision explicitly in `FailedDocument`.

End-to-end testing is especially valuable this week because multiple layers are now connected. A strong integration test might create a temporary SQLite database, run the ingestion service on a sample PDF directory, and then verify that the stored rows match the parsed content.

Be realistic about parser quality. PDF extraction is often messy. Your first goal is reliability and visibility, not perfect text quality. Record what happened, store enough context to debug, and avoid silent data loss.

Finally, remember that a pipeline is easier to evolve when each stage has a clear contract. The scanner finds candidate files. The parser extracts text. The service coordinates flow. The repository persists. The CLI displays results. If those boundaries stay clean now, later features like concurrency, search, and ML can plug in without requiring a rewrite.
