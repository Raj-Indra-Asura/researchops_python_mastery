# ResearchOps — Syllabus

A 20-week Python mastery curriculum built around ResearchOps.

---

## Month 1 — Python Core and Project Foundation

### Week 1: Python Foundations + Repository Setup
**Learning objectives:**
- Set up a professional Python project with `src/` layout and `pyproject.toml`
- Understand virtual environments, modules, and import system
- Use functions, collections, conditionals, and loops fluently
- Build a minimal working CLI with a single command

**Concepts:** functions, lists/dicts/sets, comprehensions, modules, imports, venvs, src layout, Typer CLI basics

---

### Week 2: Files, Paths, Exceptions, Logging
**Learning objectives:**
- Use `pathlib.Path` for all file operations
- Define and raise custom exceptions
- Configure structured logging with appropriate levels
- Handle file I/O errors gracefully

**Concepts:** `pathlib`, `open()`, context managers, exception hierarchy, `logging`, `try/except/finally`

---

### Week 3: OOP, Dataclasses, Domain Modeling
**Learning objectives:**
- Model the problem domain with Python classes and dataclasses
- Use type hints on all public APIs
- Understand immutability and value objects
- Write unit tests for domain models

**Concepts:** `@dataclass`, `frozen=True`, `Optional`, `list[T]`, value objects, domain modeling

---

### Week 4: CLI and Packaging
**Learning objectives:**
- Create an installable Python package with entry points
- Understand `pyproject.toml` dependency groups
- Test CLI commands with `typer.testing.CliRunner`
- Add shell completion to the CLI

**Concepts:** `pyproject.toml`, `[project.scripts]`, Typer sub-apps, `CliRunner`, optional dependencies

---

## Month 2 — Storage, Search, Multiprocessing

### Week 5: SQLite Storage Layer
**Learning objectives:**
- Design a SQL schema for the paper domain
- Implement the repository pattern with raw `sqlite3`
- Handle transactions and rollbacks
- Write integration tests against a real (tmp) database

**Concepts:** SQL DDL/DML, `sqlite3`, context manager connections, repository pattern, WAL mode

---

### Week 6: PDF Parsing Pipeline
**Learning objectives:**
- Integrate a third-party parsing library (`pypdf`)
- Design a parser that returns domain objects (not strings)
- Wire the IngestionService end-to-end
- Handle real parsing failures gracefully

**Concepts:** third-party libraries, parser design, service orchestration, integration tests with real PDFs

---

### Week 7: Keyword Search and Data Quality
**Learning objectives:**
- Implement in-memory keyword search over stored papers
- Normalise text for consistent matching
- Track and display ingestion failures
- Report library statistics

**Concepts:** text normalisation, inverted index basics, scoring/ranking, data quality gates

---

### Week 8: Multiprocessing Ingestion
**Learning objectives:**
- Identify CPU-bound vs I/O-bound work
- Use `ProcessPoolExecutor` for parallel PDF parsing
- Handle worker failures without crashing the whole run
- Understand pickling constraints

**Concepts:** `concurrent.futures.ProcessPoolExecutor`, GIL, pickling, worker failure isolation, batch writes

---

## Month 3 — Advanced Python and ML Engineering

### Week 9: Protocols, Interfaces, Clean Architecture
**Learning objectives:**
- Define abstract contracts with `typing.Protocol`
- Apply dependency inversion throughout the service layer
- Detect and eliminate import boundary violations
- Use fake repositories in all service tests

**Concepts:** `typing.Protocol`, `runtime_checkable`, dependency inversion, import boundaries, test doubles

---

### Week 10: Testing Discipline and Quality Gates
**Learning objectives:**
- Write fixtures that cover common test setups
- Use `monkeypatch` for environment and dependency substitution
- Configure `pytest-cov` with a minimum coverage threshold
- Make CI fail on coverage regressions

**Concepts:** `pytest` fixtures, `tmp_path`, `monkeypatch`, `conftest.py`, coverage configuration, CI gates

---

### Week 11: Classical ML — Topic Classification
**Learning objectives:**
- Build a TF-IDF + classifier pipeline with scikit-learn
- Evaluate a model with precision, recall, and F1
- Persist and load a trained model
- Expose training and prediction through CLI commands

**Concepts:** TF-IDF, `Pipeline`, `LogisticRegression`, `train_test_split`, `classification_report`, `joblib`

---

### Week 12: Experiment Tracking
**Learning objectives:**
- Record params, metrics, and artifacts for every training run
- Compare experiment runs to select the best model
- Persist experiment data in SQLite
- Understand reproducibility requirements

**Concepts:** experiment tracking, params vs metrics, artifacts, model versioning, reproducibility

---

## Month 4 — AI Engineering, API, Async, Workers

### Week 13: Embeddings and Semantic Search
**Learning objectives:**
- Chunk paper text for embedding
- Generate embeddings with a local model
- Implement cosine similarity search
- Cache embeddings to avoid recomputation

**Concepts:** chunking strategies, sentence-transformers, cosine similarity, embedding cache, retrieval evaluation

---

### Week 14: FastAPI Layer
**Learning objectives:**
- Build REST endpoints over the existing service layer
- Use FastAPI dependency injection
- Validate requests/responses with Pydantic
- Test the API with `httpx.AsyncClient`

**Concepts:** FastAPI, `Depends`, Pydantic response models, HTTP status codes, `TestClient`, API design

---

### Week 15: Async I/O Network Fetching
**Learning objectives:**
- Write async functions that fetch papers from the web
- Apply timeouts and retry logic
- Never block the event loop with CPU-bound work
- Test async code with `pytest-asyncio`

**Concepts:** `asyncio`, `httpx.AsyncClient`, `async def`, `await`, timeouts, retries, I/O vs CPU

---

### Week 16: Local Worker and Job System
**Learning objectives:**
- Design a job state machine (pending → running → done/failed)
- Build a persistent job queue in SQLite
- Write a worker loop that processes jobs
- Handle retries and idempotency

**Concepts:** job states, retry logic, idempotency, background workers, worker failure recovery

---

## Month 5 — RAG, Production, Portfolio

### Week 17: RAG Assistant
**Learning objectives:**
- Implement the retrieve-then-generate pipeline
- Construct prompts that ground answers in retrieved chunks
- Include source citations in every answer
- Detect and handle cases where no relevant chunks exist

**Concepts:** RAG, retrieval grounding, prompt engineering, hallucination control, source attribution

---

### Week 18: Docker and Environment Configuration
**Learning objectives:**
- Write a minimal, production-ready Dockerfile
- Compose the API and worker as separate services
- Manage environment-specific configuration with `.env`
- Test the full stack in Docker

**Concepts:** Dockerfile, `docker-compose`, multi-stage builds, env var management, volume mounts

---

### Week 19: Documentation and Portfolio Polish
**Learning objectives:**
- Write an architecture document that explains every design decision
- Create diagrams for the module dependency graph and data flow
- Write a demo script for a 5-minute walkthrough
- Make the README impressive enough for a hiring manager

**Concepts:** technical writing, architecture communication, Mermaid diagrams, portfolio storytelling

---

### Week 20: Final Hardening and v1.0 Release
**Learning objectives:**
- Complete all validation checklists
- Pass CI end-to-end with zero failures
- Tag a `v1.0.0` release with a changelog
- Record or write a demo you're proud to share

**Concepts:** release discipline, scope control, final validation, retrospective, portfolio presentation
