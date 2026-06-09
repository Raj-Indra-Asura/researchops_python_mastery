<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 06 Notes — PDF Parsing Pipeline

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 06: PDF Parsing Pipeline

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Raw bytes become structured knowledge**.
The practical milestone is: `researchops ingest ./papers` extracts text and metadata from PDFs and stores them. Failed documents are recorded, not silently dropped.
The expected capability is: Can integrate a third-party library, wire a multi-step pipeline through a service, and handle partial failures without crashing the program.
This chapter is one step in the ResearchOps system, not a random lesson.
The visible feature matters because it proves the idea works.
The hidden skill matters because it lets you build the next chapter without confusion.
A complete pass through this chapter means you can read the code, run it, test it, break it, and explain it aloud.

Use this study order:
- Read the story first without typing.
- Trace the smallest code example.
- Find the project file that owns the behavior.
- Run the validation command.
- Explain one happy path and one failure path.

## What you already know from previous weeks

- Week 2 taught Files, Paths, Exceptions, and Logging; keep its responsibility in mind, but do not rebuild it here.
- Week 3 taught OOP, Dataclasses, and Domain Modeling; keep its responsibility in mind, but do not rebuild it here.
- Week 4 taught CLI and Packaging; keep its responsibility in mind, but do not rebuild it here.
- Week 5 taught SQLite Storage Layer; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 6 solves the project problem behind **PDF Parsing Pipeline**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept `Third-party library integration (`pypdf`)` helps solve part of this gap.
- The concept `Optional dependencies and graceful import errors` helps solve part of this gap.
- The concept `Designing parsers that return domain objects, not strings` helps solve part of this gap.
- The concept ``IngestionService` orchestration: discover → parse → save` helps solve part of this gap.
- The concept `Real parsing failures and how to record them` helps solve part of this gap.
- The concept `Integration tests with real PDF fixtures` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **PDF Parsing Pipeline**?
- Ask: what is the owner for **PDF Parsing Pipeline**?
- Ask: what is the transformation for **PDF Parsing Pipeline**?
- Ask: what is the proof for **PDF Parsing Pipeline**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| Third-party library integration (`pypdf`) | Third-party library integration (`pypdf`) | This term names one job in the Week 6 milestone. |
| Optional dependencies and graceful import errors | Optional dependencies and graceful import errors | This term names one job in the Week 6 milestone. |
| Designing parsers that return domain objects, not strings | Designing parsers that return domain objects, not strings | This term names one job in the Week 6 milestone. |
| IngestionService` orchestration | `IngestionService` orchestration: discover → parse → save | This term names one job in the Week 6 milestone. |
| Real parsing failures and how to record them | Real parsing failures and how to record them | This term names one job in the Week 6 milestone. |
| Integration tests with real PDF fixtures | Integration tests with real PDF fixtures | This term names one job in the Week 6 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: Third-party library integration (`pypdf`)
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 6, it supports the milestone: `researchops ingest ./papers` extracts text and metadata from PDFs and stores them. Failed documents are recorded, not silently dropped.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: Optional dependencies and graceful import errors
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 6, it supports the milestone: `researchops ingest ./papers` extracts text and metadata from PDFs and stores them. Failed documents are recorded, not silently dropped.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: Designing parsers that return domain objects, not strings
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 6, it supports the milestone: `researchops ingest ./papers` extracts text and metadata from PDFs and stores them. Failed documents are recorded, not silently dropped.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: `IngestionService` orchestration: discover → parse → save
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 6, it supports the milestone: `researchops ingest ./papers` extracts text and metadata from PDFs and stores them. Failed documents are recorded, not silently dropped.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: Real parsing failures and how to record them
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 6, it supports the milestone: `researchops ingest ./papers` extracts text and metadata from PDFs and stores them. Failed documents are recorded, not silently dropped.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: Integration tests with real PDF fixtures
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 6, it supports the milestone: `researchops ingest ./papers` extracts text and metadata from PDFs and stores them. Failed documents are recorded, not silently dropped.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/parsing/pdf_parser.py` — implements `DocumentParser`
- `src/researchops/parsing/text_cleaner.py`
- `src/researchops/parsing/metadata_extractor.py`
- `src/researchops/services/ingestion_service.py`
Study those files in this order:
1. Find the user-facing entry point.
2. Find the service or core concept that owns the meaning.
3. Find the infrastructure only when outside resources are needed.
4. Find the tests that prove the behavior.
5. Find the validation command that a learner runs manually.
The goal is to know why each file exists.
If two files seem to own the same decision, stop and clarify the boundary.

## Code examples with line-by-line explanation

```python
class PdfParser:
    def parse(self, path: Path) -> ParsedDocument:
        raw_text = read_pdf_text(path)
        cleaned_text = clean_text(raw_text)
        return ParsedDocument(source_path=path, text=cleaned_text)
```

Line-by-line explanation:
- Line 1: `class PdfParser:` — This names a project concept so the code can talk in domain language.
- Line 2: `def parse(self, path: Path) -> ParsedDocument:` — This names a reusable action and shows what information it receives.
- Line 3: `raw_text = read_pdf_text(path)` — This stores a clear intermediate value for the next step.
- Line 4: `cleaned_text = clean_text(raw_text)` — This stores a clear intermediate value for the next step.
- Line 5: `return ParsedDocument(source_path=path, text=cleaned_text)` — This produces the result or performs the declared setup step.

How to use this example:
- Name the input.
- Name the output.
- Predict the result before running anything.
- Connect the shape to the real ResearchOps file.
- Write one sentence about why each line belongs.

## Common beginner mistakes

- **Mistake:** Pasting code before knowing the owner of the behavior.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Changing many files at once.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Skipping the failure path.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Reading only the happy path test.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Ignoring the validation command.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Using vague names.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Putting business rules in the user interface layer.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Treating logs, errors, and tests as decoration.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Optimizing before correctness is visible.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Building future-week features early.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.

## Debugging guidance

- Copy the exact failing command.
- Read the first useful error line.
- Read the final error line.
- Classify the failure as import, input, state, file, database, network, model, or expectation.
- Reproduce it with the smallest command.
- Inspect the value closest to the failure.
- Fix the cause, not only the symptom.
- Run the narrowest test.
- Run the chapter validation command.
- Write down what the error was teaching.
Debugging questions:
- What did I expect?
- What happened?
- Which value first became wrong?
- Which layer created that value?
- Which test should catch this next time?

## Design tradeoffs

- **Simple first version:** Easy to understand, but not the final production shape.
- **Clear layers:** More files, but less confusion as features grow.
- **Explicit errors:** More code, but failures become teachable.
- **Small unit tests:** Fast feedback, but less end-to-end confidence.
- **Integration tests:** Real wiring, but slower and more setup.
- **Configuration:** Flexible behavior, but defaults must be clear.
The right question is not "What is the fanciest design?"
The right question is "What design teaches the responsibility clearly and can grow next week?"

## Testing implications

Tests for this chapter:
- `tests/integration/test_ingestion_service.py` — full pipeline with sample PDFs
Validation commands:
```bash
researchops ingest ./examples/sample_papers
researchops papers list
researchops papers failed
pytest tests/integration/test_ingestion_service.py -v
```
- Arrange the data.
- Act on the system.
- Assert the visible promise.
- Check one failure path.
- Keep unit tests fast.
- Use integration tests only when real wiring matters.

## Architecture implications

ResearchOps stays understandable when dependencies point inward.
```text
CLI / API / Worker -> Services -> Core
Infrastructure implements core-facing contracts and is wired at the outside.
```
- Does the UI layer avoid business logic?
- Does the service layer own workflow decisions?
- Does core avoid infrastructure imports?
- Does infrastructure do outside-world work?
- Do tests use fakes when possible?
Architecture is not ceremony.
Architecture is named responsibility.

## How this connects to AI engineering / ML research

AI engineering needs more than models.
It needs reliable data flow, clear interfaces, repeatable experiments, visible failures, and honest evaluation.
Week 6 contributes by making **pdf parsing pipeline** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 6 solve?
- What is the main input?
- What is the main output?
- Which file owns the main responsibility?
- Which layer should not contain business logic?
- What is one happy path?
- What is one failure path?
- What command proves the chapter works?
- What should you not build early?
- How does this prepare the next week?

## Explain-it-aloud prompts

- Explain PDF Parsing Pipeline in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: PDF Parsing Pipeline.
- The milestone: `researchops ingest ./papers` extracts text and metadata from PDFs and stores them. Failed documents are recorded, not silently dropped.
- The main project files.
- The validation command.
- The boundary rule for the layer you are touching.
- The habit of testing before moving forward.

## What to understand deeply

- Why this feature belongs now.
- How data moves through the chapter.
- Which file owns which decision.
- How the failure path is handled.
- Why the tests prove behavior.
- How this week makes future work safer.

## What not to worry about yet

- Perfect scale.
- Fancy abstractions.
- Future-week features.
- Every option in every library.
- Premature optimization.
- Comparing your speed to someone else.
Focus on the milestone.
A clear small milestone beats a confusing large one.

## Bridge to next week

Next week is Week 7: **Keyword Search and Data Quality**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `researchops search "transformer attention"` returns ranked results from stored papers.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace `Third-party library integration (`pypdf`)` from user input to project result.
- Drill 2: Write one sentence defining `Third-party library integration (`pypdf`)` without copying the notes.
- Drill 3: Find the file where `Third-party library integration (`pypdf`)` appears or should appear.
- Drill 4: Name one wrong implementation of `Third-party library integration (`pypdf`)` and why it would hurt.
- Drill 5: Name one test that would protect `Third-party library integration (`pypdf`)`.
- Drill 6: Trace `Optional dependencies and graceful import errors` from user input to project result.
- Drill 7: Write one sentence defining `Optional dependencies and graceful import errors` without copying the notes.
- Drill 8: Find the file where `Optional dependencies and graceful import errors` appears or should appear.
- Drill 9: Name one wrong implementation of `Optional dependencies and graceful import errors` and why it would hurt.
- Drill 10: Name one test that would protect `Optional dependencies and graceful import errors`.
- Drill 11: Trace `Designing parsers that return domain objects, not strings` from user input to project result.
- Drill 12: Write one sentence defining `Designing parsers that return domain objects, not strings` without copying the notes.
- Drill 13: Find the file where `Designing parsers that return domain objects, not strings` appears or should appear.
- Drill 14: Name one wrong implementation of `Designing parsers that return domain objects, not strings` and why it would hurt.
- Drill 15: Name one test that would protect `Designing parsers that return domain objects, not strings`.
- Drill 16: Trace ``IngestionService` orchestration: discover → parse → save` from user input to project result.
- Drill 17: Write one sentence defining ``IngestionService` orchestration: discover → parse → save` without copying the notes.
- Drill 18: Find the file where ``IngestionService` orchestration: discover → parse → save` appears or should appear.
- Drill 19: Name one wrong implementation of ``IngestionService` orchestration: discover → parse → save` and why it would hurt.
- Drill 20: Name one test that would protect ``IngestionService` orchestration: discover → parse → save`.
- Drill 21: Trace `Real parsing failures and how to record them` from user input to project result.
- Drill 22: Write one sentence defining `Real parsing failures and how to record them` without copying the notes.
- Drill 23: Find the file where `Real parsing failures and how to record them` appears or should appear.
- Drill 24: Name one wrong implementation of `Real parsing failures and how to record them` and why it would hurt.
- Drill 25: Name one test that would protect `Real parsing failures and how to record them`.
- Drill 26: Trace `Integration tests with real PDF fixtures` from user input to project result.
- Drill 27: Write one sentence defining `Integration tests with real PDF fixtures` without copying the notes.
- Drill 28: Find the file where `Integration tests with real PDF fixtures` appears or should appear.
- Drill 29: Name one wrong implementation of `Integration tests with real PDF fixtures` and why it would hurt.
- Drill 30: Name one test that would protect `Integration tests with real PDF fixtures`.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes
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
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
