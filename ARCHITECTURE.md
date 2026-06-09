# ResearchOps — Architecture

## Overview

ResearchOps uses a **modular monolith** architecture. All code lives in a single Python package (`researchops`), divided into focused modules with strict dependency rules.

This approach is intentional: it gives us the benefits of clean architecture (testability, separation of concerns, replaceable implementations) without the operational overhead of microservices.

---

## Dependency Direction

```
┌─────────────────────────────────────────────┐
│     CLI / API / Workers                     │
│  (cli/, api/, workers/)                     │
└──────────────────┬──────────────────────────┘
                   │ imports
┌──────────────────▼──────────────────────────┐
│     Services / Use Cases                    │
│  (services/)                                │
│  depends on: Core Protocols only            │
└──────────────────┬──────────────────────────┘
                   │ imports
┌──────────────────▼──────────────────────────┐
│     Core Models + Protocols                 │
│  (core/models.py, core/interfaces.py)       │
│  NO external imports                        │
└──────────────────┬──────────────────────────┘
                   │ implemented by
┌──────────────────▼──────────────────────────┐
│     Infrastructure                          │
│  (storage/, parsing/, ml/, search/)         │
│  implements core protocols                  │
└─────────────────────────────────────────────┘
```

---

## Module Responsibilities

### `core/`
The heart of the domain. Contains:
- **`models.py`** — `Paper`, `ParsedDocument`, `IngestionResult`, `FailedDocument`, `SearchResult`
- **`exceptions.py`** — Custom exception hierarchy
- **`interfaces.py`** — `typing.Protocol` definitions for `PaperRepository`, `DocumentParser`, `SearchEngine`, etc.
- **`value_objects.py`** — `PaperId`, `Query`, `Tag`

**Rule:** `core/` must not import from any other subpackage. It may only use Python stdlib.

### `config/`
- **`settings.py`** — Pydantic Settings loaded from environment variables
- **`logging.py`** — Logging configuration (Rich for dev, plain for prod)

### `parsing/` (Infrastructure)
- **`pdf_parser.py`** — Wraps `pypdf`; implements `DocumentParser` protocol
- **`metadata_extractor.py`** — Extracts title, author, abstract
- **`text_cleaner.py`** — Unicode normalisation, punctuation stripping

### `storage/` (Infrastructure)
- **`sqlite_repository.py`** — Implements `PaperRepository` and `FailureRepository` protocols
- **`schema.sql`** — DDL for all tables
- **`experiment_repository.py`** — Implements `ExperimentRepository` (Week 12)
- **`job_repository.py`** — Implements `JobRepository` (Week 16)

### `services/` (Use Cases)
- **`ingestion_service.py`** — Orchestrates PDF discovery → parse → save
- **`search_service.py`** — Keyword search over stored papers
- **`paper_service.py`** — Paper listing, retrieval, stats
- **`experiment_service.py`** — Create/log/compare experiment runs (Week 12)
- **`fetch_service.py`** — Async HTTP fetching (Week 15)
- **`job_service.py`** — Background job management (Week 16)
- **`qa_service.py`** — RAG question answering (Week 17)

### `workers/` (Infrastructure)
- **`process_pool.py`** — `ProcessPoolExecutor` wrapper for CPU-bound parsing (Week 8)
- **`job_runner.py`** — Background worker loop (Week 16)

### `ml/` (Infrastructure)
- **`preprocessing.py`** — TF-IDF vectorisation pipeline (Week 11)
- **`topic_classifier.py`** — scikit-learn classifier (Week 11)
- **`evaluation.py`** — Metrics and reporting (Week 11)

### `search/` (Infrastructure)
- **`chunking.py`** — Text chunking for embeddings (Week 13)
- **`embeddings.py`** — Embedding generation (Week 13)
- **`vector_search.py`** — Cosine similarity search (Week 13)

### `ai/`
- **`prompts.py`** — RAG prompt templates (Week 17)

### `cli/` (Entry Point)
- **`main.py`** — Typer app with top-level `scan` command
- **`commands/`** — One file per command group: `ingest`, `papers`, `search`, `experiments`, `jobs`, `ask`

**Rule:** CLI commands must not contain business logic. All work is delegated to service classes.

### `api/` (Entry Point)
- **`main.py`** — FastAPI app factory (Week 14)
- **`routes/`** — One file per route group

**Rule:** Route handlers must not contain business logic.

---

## Why Modular Monolith (Not Microservices)?

At this stage:
- A single Python package is easier to understand and test
- We can enforce architecture rules through import analysis without network boundaries
- Refactoring across modules is trivial (rename a symbol, update imports)
- We can extract a service into a separate package later if needed — but we don't pay that cost upfront

---

## Why ProcessPoolExecutor for PDF Parsing?

Python's GIL means `ThreadPoolExecutor` does not help for CPU-bound work. PDF text extraction is CPU-intensive (decompressing PDF streams, running parsing algorithms). We use `ProcessPoolExecutor` to get true parallelism by spawning separate interpreter processes.

**Constraint:** everything passed to/from worker processes must be picklable. This means:
- Worker functions must be module-level (not lambdas or closures)
- Arguments and return values must be simple types or dataclasses

---

## Why Async Only for I/O?

`asyncio` is excellent for I/O-bound concurrency: many requests to the same thread without blocking. It is **not** useful for CPU-bound work — `await` inside a CPU-heavy function still blocks the event loop.

ResearchOps uses `async` only for:
- HTTP fetching (Week 15)
- FastAPI request handling (Week 14)

PDF parsing, ML training, and embedding generation are CPU-bound. They run in `ProcessPoolExecutor`, not in the event loop.

---

## Future Evolution Path

When the project is mature enough:
1. Extract the storage layer into a separate service (Postgres + pgvector)
2. Extract the ML layer into a separate inference service
3. Move the job queue to Redis or a proper message broker
4. Deploy the API and worker as separate containers (already partially done in Week 18)

But none of this happens before v1.0. We build a working monolith first.
