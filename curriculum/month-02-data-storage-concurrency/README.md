# Month 2 — Data Storage and Concurrency

> **Book section 2 of 5.** This month the scanner stops forgetting. You turn a
> one-shot tool into a **local research library** that ingests papers, stores
> them, searches them, and parses them in parallel.

---

## The big idea of the month

Month 1 gave you a tool that *finds* PDFs but remembers nothing. This month you
add **memory** and **throughput**. You will learn how a program persists data to
disk with SQLite, how to keep storage code cleanly separated from the rest of the
app, how to extract text from real PDFs, and how to make the slow parts fast with
multiprocessing.

The theme that governs everything: **correctness comes before performance.** You
make it *right*, then you make it *fast* — never the other way around.

## What you already know before this month

From Month 1 you can:

- Lay out and install a `src/` package and run its CLI.
- Use `pathlib`, custom exceptions, logging, and dataclasses.
- Model a small domain entity (e.g. `Paper`) and write pytest tests.

You do **not** yet need any SQL, database, or concurrency experience.

## What you will learn this month

- **SQLite** — an embedded, file-based relational database built into Python.
- **Schema design** — tables, primary keys, foreign keys, constraints.
- **Transactions** — making groups of writes all-or-nothing.
- **The repository pattern** — hiding raw SQL behind a clean interface so the
  rest of the app never sees a database.
- **PDF parsing** — extracting text and metadata from real PDF files.
- **The ingestion pipeline** — `scan → parse → store` wired into one flow.
- **Text cleaning** — normalising messy extracted text.
- **Keyword search** — querying stored papers by terms.
- **Duplicate detection** — recognising the same paper ingested twice.
- **Multiprocessing** — using `ProcessPoolExecutor` to parse many PDFs across
  CPU cores.
- **Why correctness comes before performance** — and how to prove correctness
  first with tests.

## What ResearchOps capability will exist by the end

A working local research library. You will be able to:

```bash
researchops ingest ./examples/sample_papers   # parse + store
researchops search "machine learning"          # query stored text
```

Papers are parsed, stored durably in SQLite, de-duplicated, searchable by
keyword, and ingested in parallel for speed.

## Week-by-week chapter flow

| Week | Chapter | What it adds |
|---|---|---|
| **Week 5 — SQLite Storage** | "The system gains memory" | Schema, transactions, and a repository layer that hides SQL. |
| **Week 6 — PDF Parsing Pipeline** | "From bytes to text" | A PDF parser and the `scan → parse → store` ingestion pipeline. |
| **Week 7 — Keyword Search & Data Quality** | "Finding and trusting data" | Keyword search, text cleaning, duplicate detection, stats. |
| **Week 8 — Multiprocessing Ingestion** | "Now make it fast" | `ProcessPoolExecutor` parallel parsing — performance, safely. |

## How each week connects to the previous week

- **Week 5 → 6:** once there is a *place to store* parsed papers (the schema and
  repository), Week 6 produces the *thing to store* by parsing PDFs and wiring
  the full ingestion pipeline.
- **Week 6 → 7:** once parsed text is stored, Week 7 makes it *useful* —
  searchable — and *trustworthy* by cleaning text and detecting duplicates.
- **Week 7 → 8:** once ingestion is correct and search works, Week 8 makes it
  *fast* by parsing in parallel — performance added only after correctness.

## What not to skip

- **The repository pattern.** If SQL leaks into services or the CLI, Month 3's
  architecture work becomes painful. Keep SQL behind the repository.
- **Transactions.** A half-written record is worse than no record. Learn how
  commit/rollback protect you.
- **Tests against a temporary database.** Always test storage against a throwaway
  DB in `tmp_path`, never your real one.
- **Correctness-first discipline in Week 8.** Do not parallelise until the
  single-process path is proven correct.

## What concepts must be understood before moving on

Be able to explain aloud:

- This pipeline in one breath: `scan → parse → store → search → parallelize`.
- What a primary key and a foreign key are, and why constraints matter.
- What a transaction guarantees and when a rollback happens.
- Why the repository pattern exists and what it hides from the rest of the app.
- Why PDF parsing is **CPU-bound** and therefore uses **processes**, not threads
  (see [ADR-0002](../../docs/decisions/0002-multiprocessing-vs-asyncio.md)).
- Why arguments to process-pool workers must be *picklable*.

## Month-end self-assessment

Rate yourself 1–10 and note evidence:

- [ ] I can create a SQLite schema with sensible keys and constraints.
- [ ] I can implement repository methods that return domain models, not rows.
- [ ] I can wrap writes in a transaction and roll back on failure.
- [ ] I can parse a PDF into clean text and metadata.
- [ ] I can describe the ingestion pipeline end to end.
- [ ] I can run a keyword search over stored papers.
- [ ] I can detect a duplicate ingestion.
- [ ] I can parallelise parsing with `ProcessPoolExecutor` and explain the
      picklability constraint.

## Month-end mini capstone

Ingest a folder of papers and prove the library works:

1. Run `researchops ingest ./examples/sample_papers` and confirm rows land in
   SQLite.
2. Run `researchops search "<a term you know is present>"` and get a hit that
   points back to its source paper.
3. Re-ingest the same folder and show duplicates are detected, not duplicated.
4. Switch ingestion to the multiprocessing path and show it produces the **same**
   stored result as the single-process path, only faster.

Done when the single-process and parallel paths agree, tests pass, and `ruff` is
clean.

## Bridge to Month 3

The library *works* — but "works on my machine" is not the same as
"engineered." Month 3 hardens it: **protocols and clean architecture**, a real
**test pyramid** and **CI quality gates**, then your first **classical ML**
model (TF-IDF topic classification) with **model artifacts** and **experiment
tracking**. The pipeline becomes a structured, testable, reproducible ML system.

## Warning signs you are not ready to move on

- SQL strings appear in your CLI commands or services.
- Tests touch your real database instead of a temporary one.
- You parallelised before the single-process path was proven correct.
- You cannot explain why parsing uses processes rather than threads.
- A crash mid-ingest leaves partial, inconsistent data (transactions missing).

## Suggested weekly study rhythm

~8–10 hours/week:

- **Read** week README + notes (~1 hr).
- **Build** the milestone in small commits (~4–6 hrs) — storage and parsing take
  more hands-on time than Month 1.
- **Break it** with `break_it.md` (~1 hr) — corrupt a PDF, kill a transaction.
- **Test** until correct, *then* optimise (~1–2 hrs).
- **Reflect** in `reflection.md` and the weekly report (~30 min).

## Suggested Git milestone at end of month

```bash
git add .
git commit -m "Month 2 complete: SQLite-backed research library with search + parallel ingest"
git tag month-2-complete
```

Your repo should now ingest, store, de-duplicate, search, and parse in parallel —
all with passing tests and clean lint.
