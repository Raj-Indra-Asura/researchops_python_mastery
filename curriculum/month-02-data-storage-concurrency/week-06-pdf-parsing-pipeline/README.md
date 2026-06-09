<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 06 — PDF Parsing Pipeline:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 5 Reflection](../week-05-sqlite-storage/reflection.md) · ➡️ [Notes →](notes.md)

---
<!-- NAV_END -->

# Week 06 — PDF Parsing Pipeline

> **Chapter title: "Raw bytes become structured knowledge."**
> The week the database stops being empty and starts holding real papers.

---

## 1. Week title

Week 6 — PDF Parsing Pipeline (Month 2, Chapter 2 of 4).

## 2. Story of the week

Last week you built a place to store papers, but you had to put data in by hand —
the database had a schema and no real content. This week you build the machine
that *fills* it. You integrate a third-party PDF library, write a parser that
returns a domain object (not a blob of string), and orchestrate the whole flow —
discover files, parse each one, store the good ones, record the failures — inside
an `IngestionService`. Real PDFs are messy; some will fail. This week you learn to
handle that without crashing the batch.

## 3. What you already know

- From Week 5: a SQLite schema, the repository pattern, and `papers list`.
- From Month 1: `pathlib` discovery, custom exceptions, logging, dataclasses.
- The `Paper` and (new this month) `ParsedDocument` / `FailedDocument` models.

You have not yet integrated an external library or built a multi-step service.

## 4. What this week adds

- **Third-party integration** with a PDF library (`pypdf`) behind the
  `DocumentParser` protocol.
- **Optional dependencies** and graceful import errors (parsing extras).
- A parser that returns **domain objects**, plus text cleaning and metadata
  extraction.
- The **`IngestionService`**: `discover → parse → save`, the project's first real
  orchestration layer.
- **Failure recording** — bad PDFs become `FailedDocument` rows, not silent
  losses.

## 5. Why this week matters

This is the first time several layers cooperate: discovery, parsing,
persistence, and failure handling all meet in one service. It teaches the single
most important production habit — **partial failure is normal**. A research
library that crashes on the first corrupt PDF is worthless; one that ingests 99
papers and *records* the 1 that failed is trustworthy. The orchestration pattern
you build here is reused for embeddings, jobs, and RAG later.

## 6. Learning objectives

By the end of the week you can:

- Integrate a third-party library behind a protocol so it stays swappable.
- Make a parser return structured domain objects, not raw strings.
- Wire a multi-step pipeline through a service.
- Distinguish a recoverable per-file failure from a fatal error.
- Record failures as data and continue the batch.
- Test the full pipeline with real PDF fixtures.

## 7. Project milestone

`researchops ingest ./papers` extracts text and metadata from PDFs and stores
them. Failed documents are recorded (visible via `researchops papers failed`),
not silently dropped.

## 8. Files / modules touched

- `src/researchops/parsing/pdf_parser.py` — implements `DocumentParser`.
- `src/researchops/parsing/text_cleaner.py` — normalises extracted text.
- `src/researchops/parsing/metadata_extractor.py` — pulls title/metadata.
- `src/researchops/services/ingestion_service.py` — the orchestration.
- `src/researchops/cli/commands/ingest.py` — wires real adapters (composition
  root).

## 9. Commands introduced

```bash
researchops ingest ./examples/sample_papers   # discover → parse → store
researchops papers failed                       # list documents that failed parsing
```

## 10. Tests involved

- `tests/integration/test_ingestion_service.py` — runs the full pipeline against
  real sample PDFs, including at least one file designed to fail.

```bash
pytest tests/integration/test_ingestion_service.py -v
```

## 11. Study plan for the week

1. **Day 1 — Library spike.** In `/tmp`, open a PDF with `pypdf` and extract raw
   text. Notice how ugly it is.
2. **Day 2 — Parser behind a protocol.** Implement `pdf_parser.py` returning a
   `ParsedDocument`; add `text_cleaner` and `metadata_extractor`.
3. **Day 3 — IngestionService.** Wire `discover → parse → save`; inject the
   parser and repositories (constructor injection).
4. **Day 4 — Failure handling.** Make one bad PDF produce a `FailedDocument`
   instead of a crash; expose `papers failed`.
5. **Day 5 — Integration tests + milestone + report.**

## 12. Estimated time breakdown

| Activity | Time |
|---|---|
| Reading + library spike | ~1.5 hrs |
| Parser + cleaner + metadata | ~3.5 hrs |
| IngestionService orchestration | ~2 hrs |
| Failure handling + integration tests | ~2 hrs |
| Break-it + reflection + report | ~1 hr |

## 13. How to know the learner is stuck

- One corrupt PDF aborts the entire ingest run (failures not isolated).
- Your parser returns a `str` and the service has to re-parse it.
- `pdf_parser.py` is imported by a *service* (infrastructure leaking upward).
- You cannot tell which papers failed or why after a run.

## 14. Definition of done

- [ ] `pdf_parser.py` implements `DocumentParser` and returns `ParsedDocument`.
- [ ] Missing optional dependency raises a clear, friendly error.
- [ ] `IngestionService` orchestrates discover → parse → save via injected
      dependencies.
- [ ] A failing PDF produces a `FailedDocument`, and the batch continues.
- [ ] `researchops ingest ./examples/sample_papers` stores parsed papers.
- [ ] `researchops papers failed` lists failures with reasons.
- [ ] Integration test covers both success and failure paths.

## 15. Ruthless mentor checkpoint

- "Run ingest on a folder where one PDF is garbage. Did the other papers still
  land in the database?"
- "Point to where the parser is *constructed*. Is it inside the service, or in the
  CLI?" (It must be the CLI.)
- "Show me the failure record for the bad file. What does it tell a human?"

If a single bad file can sink the batch, you are not done.

## 16. What not to do this week

- Do **not** swallow parsing errors silently — record them as `FailedDocument`.
- Do **not** let the service import `pypdf` or construct the concrete parser;
  inject it.
- Do **not** return raw strings from the parser; return domain objects.
- Do **not** parallelise yet — that is Week 8. Make it correct first.

## 17. Bridge to next week

You can now ingest real papers and trust the data — failures are visible, not
hidden. But a pile of stored text is only useful if you can *find* things in it.
**Week 7** turns stored parsed text into **keyword search** with ranking, and adds
**data-quality** gates and paper statistics. The clean, stored text you produce
this week is exactly what next week's search indexes.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 5 Reflection](../week-05-sqlite-storage/reflection.md) · ➡️ [Notes →](notes.md)

**Week 06 — PDF Parsing Pipeline:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
