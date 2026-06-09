# ResearchOps — Architecture

This document explains how the codebase is organised, why it is organised that way, and what rules you must follow when adding code. Read this before modifying any source file.

---

## The Big Picture: Modular Monolith

ResearchOps is a **modular monolith**.

**What that means:**
All code lives in a single Python package (`researchops`). There is no network boundary between parts of the system. You import code directly — you do not make HTTP calls between internal components.

**Why not microservices?**
Microservices are an operational choice, not an architectural virtue. At this scale:
- A single package is easier to understand, test, and change
- You can enforce architecture rules through import analysis instead of network contracts
- Refactoring across modules is trivial (rename a symbol, update imports)
- You can extract a module into a separate service when you have a real reason to — but you do not pay that cost upfront

**Why not a flat pile of scripts?**
A flat structure becomes unmanageable when modules grow. Clean architecture gives you:
- **Testability** — services that depend on interfaces can be tested with fakes, no real DB required
- **Replaceability** — you can swap SQLite for Postgres by writing a new class that implements the same protocol
- **Readability** — any engineer can look at the directory structure and understand where to find any concept

---

## Dependency Direction

This is the single most important architectural rule. Read it until you can draw it from memory.

```
┌─────────────────────────────────────────────────────────┐
│              Entry Points                               │
│     cli/          api/          workers/                │
│  (Typer CLI)  (FastAPI routes) (job runner)             │
└───────────────────────┬─────────────────────────────────┘
                        │  imports ↓
┌───────────────────────▼─────────────────────────────────┐
│              Services / Use Cases                       │
│                    services/                            │
│   ingestion_service   search_service   paper_service    │
│   experiment_service  fetch_service    job_service      │
│   qa_service                                            │
│                                                         │
│  ↳ Services import ONLY from core/interfaces.py         │
│    They never import sqlite_repository or pdf_parser    │
└───────────────────────┬─────────────────────────────────┘
                        │  imports ↓
┌───────────────────────▼─────────────────────────────────┐
│              Core Domain                                │
│                    core/                                │
│   models.py          interfaces.py       exceptions.py  │
│   value_objects.py                                      │
│                                                         │
│  ↳ core/ imports NOTHING from within researchops/       │
│    Only Python stdlib allowed here                      │
└───────────────────────┲─────────────────────────────────┘
                        ┃  implemented by ↑
┌───────────────────────┸─────────────────────────────────┐
│              Infrastructure                             │
│  storage/     parsing/     ml/     search/     ai/      │
│                                                         │
│  ↳ These implement core protocols                       │
│  ↳ These may import third-party libraries               │
│  ↳ These are wired together in cli/ and api/            │
└─────────────────────────────────────────────────────────┘
```

**Read the arrows as: "this layer may import from the layer it points to."**

An arrow pointing down means: upper layers import lower layers.
Infrastructure implements up into core (shown with ┲).

---

## Allowed Imports

| Layer | May import from |
|-------|----------------|
| `cli/` | `services/`, `core/`, `config/` |
| `api/` | `services/`, `core/`, `config/` |
| `workers/` | `services/`, `core/`, `config/` |
| `services/` | `core/` only (`models`, `interfaces`, `exceptions`, `value_objects`) |
| `storage/` | `core/`, Python stdlib, third-party (e.g. sqlite3) |
| `parsing/` | `core/`, Python stdlib, third-party (e.g. pypdf) |
| `ml/` | `core/`, Python stdlib, third-party (e.g. scikit-learn) |
| `search/` | `core/`, Python stdlib, third-party (e.g. sentence-transformers) |
| `ai/` | `core/`, Python stdlib |
| `core/` | Python stdlib only — no researchops imports |
| `config/` | Python stdlib, third-party (pydantic-settings) |

---

## Forbidden Imports

These violate the architecture and must never appear:

```python
# FORBIDDEN — service importing concrete infrastructure
from researchops.storage.sqlite_repository import SqlitePaperRepository  # in services/
from researchops.parsing.pdf_parser import PdfParser                     # in services/
from researchops.ml.topic_classifier import TopicClassifier              # in services/

# FORBIDDEN — core importing anything from researchops
from researchops.storage import anything  # in core/
from researchops.services import anything # in core/

# FORBIDDEN — business logic in CLI/API routes
# All logic must be in services, not in command handlers or route functions

# FORBIDDEN — asyncio event loop blocked by CPU work
async def bad_ingest(path):
    result = parse_pdf(path)   # CPU-bound — blocks the event loop
    ...
```

---

## Module Responsibilities

### `core/` — The Domain Heart

No external imports. No researchops imports. Python stdlib only.

- **`models.py`** — `Paper`, `ParsedDocument`, `IngestionResult`, `FailedDocument`, `SearchResult`
- **`exceptions.py`** — Exception hierarchy: `ResearchOpsError`, `ScanError`, `ParseError`, `StorageError`, `SearchError`
- **`interfaces.py`** — All `typing.Protocol` definitions: `PaperRepository`, `DocumentParser`, `FailureRepository`, `SearchEngine`, `ExperimentRepository`, `JobRepository`
- **`value_objects.py`** — `PaperId`, `Query`, `Tag` — small, immutable, type-safe wrappers

**Key file:** `src/researchops/core/interfaces.py`

If you want to know what the system can do, read `interfaces.py`. It is the contract that every layer respects.

### `config/` — Configuration and Logging

- **`settings.py`** — `AppSettings` loaded from environment variables via `pydantic-settings`
- **`logging.py`** — Logging configuration: Rich handler for development, plain handler for production

### `parsing/` — PDF Infrastructure

Implements `DocumentParser` protocol. May import `pypdf`.

- **`pdf_parser.py`** — Wraps pypdf; extracts raw text per page
- **`text_cleaner.py`** — Unicode normalisation, punctuation stripping
- **`metadata_extractor.py`** — Extracts title, author, abstract from raw text

### `storage/` — Persistence Infrastructure

Implements `PaperRepository`, `FailureRepository`, `ExperimentRepository`, `JobRepository`. May import `sqlite3`.

- **`sqlite_repository.py`** — All paper and failure CRUD operations
- **`schema.sql`** — DDL for all tables (papers, failures, experiments, runs, jobs)
- **`experiment_repository.py`** — Experiment run storage (Week 12)
- **`job_repository.py`** — Job queue storage (Week 16)

### `services/` — Use Cases

**Import rule: only from `core/`. Never from infrastructure.**

- **`ingestion_service.py`** — Discover → parse → save pipeline
- **`search_service.py`** — Keyword search with text normalisation
- **`paper_service.py`** — Paper listing, retrieval, stats
- **`experiment_service.py`** — Create/log/compare experiment runs
- **`fetch_service.py`** — Async HTTP fetching with retry
- **`job_service.py`** — Job creation, state transitions, retry
- **`qa_service.py`** — Retrieve-then-generate RAG pipeline

### `workers/` — Execution Infrastructure

- **`process_pool.py`** — `ProcessPoolExecutor` wrapper for CPU-bound parsing (Week 8)
- **`job_runner.py`** — Polling worker loop for the job queue (Week 16)

### `ml/` — ML Infrastructure

Implements ML logic. May import scikit-learn, numpy, joblib.

- **`preprocessing.py`** — TF-IDF vectorisation pipeline
- **`topic_classifier.py`** — Training and prediction with scikit-learn
- **`evaluation.py`** — `classification_report` wrapping and model comparison

### `search/` — Embedding Infrastructure

**Key path:** `src/researchops/search/`

Implements vector search. May import sentence-transformers (Week 13+).

- **`chunking.py`** — Splits long texts into overlapping chunks suitable for embedding
- **`embeddings.py`** — Generates and caches embeddings using a local sentence-transformers model
- **`vector_search.py`** — Cosine similarity ranking over stored embeddings

### `ai/` — Prompt Templates

- **`prompts.py`** — RAG prompt templates: grounding instructions, citation format, no-result fallback

### `cli/` — Entry Points (Command-Line)

**Rule:** CLI commands contain no business logic. All work is delegated to services.

- **`main.py`** — Root Typer app; registers sub-apps; wires infrastructure → services
- **`commands/papers.py`** — `papers list`, `papers show`, `papers stats`, `papers failed`
- **`commands/ingest.py`** — `ingest`, `fetch-url`, `fetch-arxiv`, `jobs` commands
- **`commands/search.py`** — `search`, `semantic-search` commands
- **`commands/experiments.py`** — `experiment` command group

### `api/` — Entry Points (HTTP)

**Rule:** Route handlers contain no business logic. All work is delegated to services.

- **`main.py`** — FastAPI app factory; lifespan for resource setup/teardown
- **`routes/papers.py`** — `GET /papers`, `GET /papers/{id}`, `POST /papers/ingest`
- **`routes/search.py`** — `GET /papers/search?q=`, `POST /search/semantic`

---

## CLI vs Service vs Storage

A common beginner confusion: "where does this code go?"

| Concern | Belongs in | Example |
|---------|-----------|---------|
| Parsing CLI arguments | `cli/commands/` | `--workers 4` argument definition |
| Orchestrating a workflow | `services/` | "find PDFs, parse each one, save to DB" |
| Talking to a database | `storage/` | `INSERT INTO papers ...` |
| Generating embeddings | `search/embeddings.py` | calling sentence-transformers |
| Validating a response shape | `api/routes/` | Pydantic response model |
| Domain rules | `core/models.py` | `PaperId` must be non-empty string |

**Simple test:** if your code would need to change when you switch from CLI to API, it belongs in a service, not in the CLI or API layer.

---

## API Route Rules

- Route handlers must not import from `storage/`, `parsing/`, `ml/`, or `search/` directly
- All infrastructure is injected via `Depends` from a factory function
- Routes return Pydantic models, not raw domain models
- Routes do not catch business exceptions — a global exception handler in `api/main.py` converts them to HTTP responses

---

## Async vs Multiprocessing

| Use case | Use this | Why |
|----------|----------|-----|
| HTTP fetching (many URLs) | `asyncio` + `httpx.AsyncClient` | I/O-bound: waiting for network |
| FastAPI request handling | `asyncio` (FastAPI is async) | I/O-bound: waiting for DB, disk |
| PDF text extraction | `ProcessPoolExecutor` | CPU-bound: bypasses the GIL |
| ML model training | `ProcessPoolExecutor` | CPU-bound: bypasses the GIL |
| Embedding generation | `ProcessPoolExecutor` | CPU-bound: bypasses the GIL |

**Never** run CPU-bound code inside an `async def` function. It blocks the event loop and defeats the purpose of async.

```python
# WRONG — CPU work in async context
async def ingest_async(path):
    text = extract_pdf_text(path)   # blocks event loop
    ...

# CORRECT — CPU work in process pool, async for I/O
async def ingest_async(paths):
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(process_pool, parse_batch, paths)
    ...
```

---

## Key Paths Reference

| Concept | File path |
|---------|-----------|
| All protocol definitions | `src/researchops/core/interfaces.py` |
| All domain models | `src/researchops/core/models.py` |
| Embedding and vector search | `src/researchops/search/` |
| RAG prompt templates | `src/researchops/ai/prompts.py` |
| App settings (env vars) | `src/researchops/config/settings.py` |
| DB schema DDL | `src/researchops/storage/schema.sql` |
| Fake test implementations | `tests/fakes/` |

---

## How Architecture Evolves by Month

The architecture does not appear all at once. It grows as the project grows.

### Month 1 (Weeks 1–4): Foundations

```
cli/ → utils/
```

No services yet. No storage. The CLI calls utility functions directly. This is intentional — learn the structure before adding complexity.

### Month 2 (Weeks 5–8): Storage + Services emerge

```
cli/ → services/ → core/
                 ← storage/ (implements core protocols)
```

`IngestionService` and `SearchService` appear. They depend on `PaperRepository` protocol. `SqlitePaperRepository` implements that protocol. The CLI wires them together.

### Month 3 (Weeks 9–12): Clean Architecture enforced

```
cli/ → services/ → core/
                 ← storage/
                 ← ml/
tests/ → fakes/ (implement core protocols)
```

All services are refactored to depend only on protocols. Fakes are introduced. Coverage gate is added. ML layer appears.

### Month 4 (Weeks 13–16): API + Search + Async + Workers

```
cli/     → services/ → core/
api/     →           ← storage/
workers/ →           ← search/
                     ← ml/
                     ← parsing/
```

FastAPI routes mirror CLI commands. The `search/` module is introduced. Async and worker layers appear. Entry points multiply but dependency rules stay the same.

### Month 5 (Weeks 17–20): RAG + Docker + v1.0

```
cli/ → services/ → core/ ← all infrastructure
api/ →
      ai/ (prompt templates)
Docker: api container + worker container
```

The `ai/` module provides prompts. `QAService` uses `search/` to retrieve and `ai/prompts.py` to generate. Docker introduces deployment boundaries that mirror the logical boundaries.

---

## Why This Architecture Is Right for Learning

1. **One pattern, applied consistently** — once you understand the dependency direction, every new module fits the same template
2. **Testable by construction** — services that depend on protocols can always be tested with fakes
3. **Readable by strangers** — a new engineer can open the repo and immediately see where to find any concept
4. **Evolvable** — infrastructure can be swapped (e.g. SQLite → Postgres) without changing service logic
5. **Portfolio-worthy** — interviewers ask "how did you structure this?" — this architecture has a clear, defensible answer
