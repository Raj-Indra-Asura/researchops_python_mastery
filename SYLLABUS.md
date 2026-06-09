<!-- NAV_START -->
---
[🏠 Home](README.md) · [🗺 Roadmap](ROADMAP.md) · **📋 Syllabus** · [📐 Project Spec](PROJECT_SPEC.md) · [🏛 Architecture](ARCHITECTURE.md) · [🤝 Contributing](CONTRIBUTING.md) · [✅ Release Checklist](RELEASE_CHECKLIST.md) · [🗂 Curriculum Map](curriculum/NAVIGATION.md)

---
<!-- NAV_END -->

# ResearchOps — Syllabus

A 20-week Python mastery curriculum. Each entry is one chapter of the book.

---

## How to use this file

This is the table of contents. For every week it tells you:
- what chapter you are in
- what concepts the chapter teaches
- what milestone you must reach before moving on
- which source files you will create or modify
- which test files will grow
- the exact validation command
- what you should be able to do by the end of the week

---

## Month 1 — Python Core and Project Foundation

---

### Week 1: Python Foundations and Repository Setup

**Chapter title:** The project comes alive

**Concepts:**
- Python src-layout and `pyproject.toml`
- Virtual environments and `pip install -e`
- Functions, collections, comprehensions, modules
- `pathlib.Path` for file discovery
- Typer CLI basics: app, command, arguments
- `pytest` test discovery and first assertions
- `ruff` lint checks

**Project milestone:**
`researchops scan ./papers` prints discovered PDF paths. Tests pass. Lint is clean.

**Main files:**
- `src/researchops/utils/paths.py` — `find_pdfs()`
- `src/researchops/cli/main.py` — `scan` command
- `pyproject.toml` — entry point, dev deps
- `src/researchops/__init__.py`

**Tests:**
- `tests/unit/test_paths.py` — `find_pdfs()` returns expected list
- `tests/e2e/test_cli.py` — `researchops scan` exits 0

**Validation command:**
```bash
researchops scan ./examples/sample_papers
pytest tests/unit/test_paths.py tests/e2e/test_cli.py -v
ruff check src tests
```

**Expected learner capability:**
Can set up a Python project from scratch, explain the src layout, run tests with pytest, and run lint with ruff.

---

### Week 2: Files, Paths, Exceptions, and Logging

**Chapter title:** Errors are information, not failures

**Concepts:**
- `pathlib.Path` API: `.exists()`, `.glob()`, `.suffix`, `.stat()`
- `open()` and context managers (`with` statement)
- Custom exception hierarchy (`class ScanError(ResearchOpsError)`)
- `try / except / finally`
- `logging` module: levels, formatters, handlers
- Structured log output

**Project milestone:**
PDF discovery uses `pathlib` throughout. Custom exceptions wrap file errors. Log messages include level, name, and message.

**Main files:**
- `src/researchops/core/exceptions.py` — custom exceptions
- `src/researchops/config/logging.py` — logging setup
- `src/researchops/utils/paths.py` — improved with error handling

**Tests:**
- `tests/unit/test_exceptions.py` — exception hierarchy and messages
- `tests/unit/test_paths.py` — updated to cover error paths

**Validation command:**
```bash
pytest tests/unit/test_exceptions.py tests/unit/test_paths.py -v
ruff check src tests
```

**Expected learner capability:**
Can define and raise custom exceptions, configure logging, and handle file-not-found errors without crashing.

---

### Week 3: OOP, Dataclasses, and Domain Modeling

**Chapter title:** Naming the things in our world

**Concepts:**
- Classes, `__init__`, instance methods
- `@dataclass` and `frozen=True`
- Type hints: `str`, `int`, `list[T]`, `Optional[T]`
- Value objects (`PaperId`, `Query`)
- Domain models vs. data bags
- Immutability and why it matters

**Project milestone:**
`Paper`, `ParsedDocument`, `IngestionResult`, `FailedDocument`, `SearchResult` are defined, type-annotated, and tested.

**Main files:**
- `src/researchops/core/models.py` — all domain dataclasses
- `src/researchops/core/value_objects.py` — `PaperId`, `Query`, `Tag`

**Tests:**
- `tests/unit/test_models.py` — construction, equality, immutability

**Validation command:**
```bash
pytest tests/unit/test_models.py -v
python -c "from researchops.core.models import Paper; print('models ok')"
```

**Expected learner capability:**
Can model a real-world problem domain with dataclasses, explain immutability, and write unit tests for data models.

---

### Week 4: CLI and Packaging

**Chapter title:** Software that users can install and run

**Concepts:**
- `[project.scripts]` entry points in `pyproject.toml`
- Typer sub-apps and command groups
- `typer.testing.CliRunner` for CLI tests
- Optional dependency groups `[project.optional-dependencies]`
- Editable installs and import paths
- Shell completion

**Project milestone:**
`pip install -e .` produces a working `researchops` command with sub-command groups: `scan`, `papers`, `search`. CLI tests use `CliRunner`.

**Main files:**
- `src/researchops/cli/main.py` — sub-app registration
- `src/researchops/cli/commands/papers.py` — `papers` command group
- `src/researchops/cli/commands/search.py` — `search` command group
- `pyproject.toml` — script entry, optional dep groups

**Tests:**
- `tests/e2e/test_cli.py` — expanded with CliRunner tests for each command group

**Validation command:**
```bash
researchops --help
researchops papers --help
researchops search --help
pytest tests/e2e/ -v
```

**Expected learner capability:**
Can install a Python package with an entry point, write CLI tests with CliRunner, and explain how `pyproject.toml` wires a command to a function.

---

## Month 2 — Storage, Search, Multiprocessing

---

### Week 5: SQLite Storage Layer

**Chapter title:** Data that survives a restart

**Concepts:**
- SQL DDL: `CREATE TABLE`, primary keys, nullable columns
- `sqlite3` Python standard library: `connect`, `cursor`, `execute`, `fetchall`
- Context manager connections and transaction control
- Repository pattern: interface → concrete implementation
- WAL journal mode for safe writes
- Integration tests with `tmp_path`

**Project milestone:**
`researchops papers list` shows papers stored in SQLite. `PaperRepository` protocol implemented by `SqlitePaperRepository`.

**Main files:**
- `src/researchops/storage/schema.sql` — DDL for all tables
- `src/researchops/storage/sqlite_repository.py` — `SqlitePaperRepository`
- `src/researchops/core/interfaces.py` — `PaperRepository` protocol

**Tests:**
- `tests/integration/test_sqlite_repository.py` — save, retrieve, list with real (tmp) DB

**Validation command:**
```bash
researchops papers list
pytest tests/integration/test_sqlite_repository.py -v
```

**Expected learner capability:**
Can design a SQL schema, implement a repository, write integration tests, and explain the difference between a protocol and its implementation.

---

### Week 6: PDF Parsing Pipeline

**Chapter title:** Raw bytes become structured knowledge

**Concepts:**
- Third-party library integration (`pypdf`)
- Optional dependencies and graceful import errors
- Designing parsers that return domain objects, not strings
- `IngestionService` orchestration: discover → parse → save
- Real parsing failures and how to record them
- Integration tests with real PDF fixtures

**Project milestone:**
`researchops ingest ./papers` extracts text and metadata from PDFs and stores them. Failed documents are recorded, not silently dropped.

**Main files:**
- `src/researchops/parsing/pdf_parser.py` — implements `DocumentParser`
- `src/researchops/parsing/text_cleaner.py`
- `src/researchops/parsing/metadata_extractor.py`
- `src/researchops/services/ingestion_service.py`

**Tests:**
- `tests/integration/test_ingestion_service.py` — full pipeline with sample PDFs

**Validation command:**
```bash
researchops ingest ./examples/sample_papers
researchops papers list
researchops papers failed
pytest tests/integration/test_ingestion_service.py -v
```

**Expected learner capability:**
Can integrate a third-party library, wire a multi-step pipeline through a service, and handle partial failures without crashing the program.

---

### Week 7: Keyword Search and Data Quality

**Chapter title:** Finding signal in stored text

**Concepts:**
- In-memory inverted index basics
- Text normalisation: lowercasing, punctuation stripping, stopwords
- Basic scoring and ranking
- Data quality gates: detecting and reporting bad data
- `SearchService` and `SearchResult` domain objects

**Project milestone:**
`researchops search "transformer attention"` returns ranked results from stored papers.

**Main files:**
- `src/researchops/services/search_service.py`
- `src/researchops/services/paper_service.py` — stats, list, show

**Tests:**
- `tests/unit/test_search_service.py` — search with FakePaperRepository
- `tests/unit/test_paper_service.py`

**Validation command:**
```bash
researchops search "machine learning"
researchops papers stats
pytest tests/unit/test_search_service.py -v
```

**Expected learner capability:**
Can implement basic text search with ranking, use fake repositories in unit tests, and explain what a data quality gate is.

---

### Week 8: Multiprocessing Ingestion

**Chapter title:** Doing many things at once, safely

**Concepts:**
- CPU-bound vs I/O-bound work
- Python GIL and why `ThreadPoolExecutor` does not help for CPU-heavy tasks
- `concurrent.futures.ProcessPoolExecutor`
- Pickling constraints: worker functions must be module-level
- Worker failure isolation: one bad PDF must not crash the batch
- Batch writes after parallel parsing

**Project milestone:**
`researchops ingest ./papers --workers 4` ingests using 4 parallel worker processes.

**Main files:**
- `src/researchops/workers/process_pool.py` — `ProcessPoolExecutor` wrapper
- `src/researchops/services/ingestion_service.py` — updated with `workers` parameter
- `src/researchops/cli/commands/ingest.py` — `--workers` option

**Tests:**
- `tests/unit/test_process_pool.py`
- `tests/integration/test_ingestion_service.py` — updated for parallel mode

**Validation command:**
```bash
researchops ingest ./examples/sample_papers --workers 2
pytest tests/unit/test_process_pool.py -v
```

**Expected learner capability:**
Can explain the GIL, implement CPU-bound parallelism with ProcessPoolExecutor, and handle worker failures without crashing the batch.

---

## Month 3 — Advanced Python and ML Engineering

---

### Week 9: Protocols, Interfaces, and Clean Architecture

**Chapter title:** Depending on shapes, not implementations

**Concepts:**
- `typing.Protocol` and structural subtyping
- `@runtime_checkable` and `isinstance` checks
- Dependency inversion principle
- Import boundary rules: services import protocols, not concrete classes
- Detecting import violations with `grep` or `import-linter`
- Fake repositories implementing core protocols

**Project milestone:**
All services depend on protocols from `core/interfaces.py`. No service imports from `storage/`, `parsing/`, or `ml/` directly. Fake repositories in `tests/fakes/` pass protocol `isinstance` checks.

**Main files:**
- `src/researchops/core/interfaces.py` — `PaperRepository`, `DocumentParser`, `SearchEngine`, `ExperimentRepository` protocols
- `tests/fakes/fake_paper_repository.py`
- `tests/fakes/fake_document_parser.py`

**Tests:**
- All service tests updated to use fakes
- `tests/unit/test_interfaces.py` — `isinstance` checks on fakes

**Validation command:**
```bash
pytest tests/unit/ -v
python -c "from researchops.core.interfaces import PaperRepository; print('interfaces ok')"
```

**Expected learner capability:**
Can define a Protocol, implement it in both a real class and a test fake, and explain why services should depend on interfaces rather than concrete implementations.

---

### Week 10: Testing Discipline and Quality Gates

**Chapter title:** Tests that give you confidence

**Concepts:**
- `pytest` fixture scopes: `function`, `module`, `session`
- `tmp_path` for temporary file system fixtures
- `monkeypatch` for environment variables and dependency substitution
- `conftest.py` for shared fixtures
- `pytest-cov` and minimum coverage threshold
- CI failure on coverage regression
- Parametrised tests with `@pytest.mark.parametrize`

**Project milestone:**
Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.

**Main files:**
- `tests/conftest.py` — shared fixtures
- `pyproject.toml` — `fail_under = 70`
- `.github/workflows/ci.yml` — coverage gate

**Tests:**
- Coverage of all service modules ≥ 70%

**Validation command:**
```bash
pytest --cov=researchops --cov-report=term-missing -q
ruff check src tests
```

**Expected learner capability:**
Can write `conftest.py` fixtures, use `monkeypatch`, explain test coverage, and configure a minimum threshold in CI.

---

### Week 11: Classical ML — Topic Classification

**Chapter title:** Teaching the machine to label papers

**Concepts:**
- TF-IDF vectorisation: what term frequency and inverse document frequency mean
- scikit-learn `Pipeline` — chaining transformers and estimators
- `LogisticRegression` as a baseline classifier
- `train_test_split`, `classification_report`, precision/recall/F1
- `joblib.dump` / `joblib.load` for model persistence
- Exposing training and prediction through CLI

**Project milestone:**
`researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.

**Main files:**
- `src/researchops/ml/preprocessing.py` — TF-IDF pipeline
- `src/researchops/ml/topic_classifier.py` — training and prediction
- `src/researchops/ml/evaluation.py` — metrics reporting
- `src/researchops/cli/commands/papers.py` — `classify`, `train-topic-model` commands

**Tests:**
- `tests/unit/test_topic_classifier.py` — train, predict, evaluate with small fixture data

**Validation command:**
```bash
researchops train-topic-model
researchops classify PAPER_ID
pytest tests/unit/test_topic_classifier.py -v
```

**Expected learner capability:**
Can build a TF-IDF + classifier pipeline, evaluate it with classification_report, persist the model, and wire it to a CLI command.

---

### Week 12: Experiment Tracking

**Chapter title:** Remembering what you tried

**Concepts:**
- Experiment tracking concepts: params, metrics, artifacts, runs
- `ExperimentRepository` protocol and SQLite implementation
- Model versioning: linking a saved model artifact to a run
- Reproducibility requirements: recording random seeds, data splits
- `ExperimentService` orchestration

**Project milestone:**
`researchops experiment list` shows all training runs with params and metrics. `researchops experiment compare` shows which run had the best F1.

**Main files:**
- `src/researchops/storage/experiment_repository.py`
- `src/researchops/services/experiment_service.py`
- `src/researchops/cli/commands/experiments.py`
- `src/researchops/storage/schema.sql` — experiment tables

**Tests:**
- `tests/unit/test_experiment_service.py` — log, list, compare with fake repo
- `tests/integration/test_experiment_repository.py`

**Validation command:**
```bash
researchops experiment list
researchops experiment compare
pytest tests/unit/test_experiment_service.py -v
```

**Expected learner capability:**
Can implement a tracking system that persists experiment metadata, retrieve and compare runs, and explain why reproducibility matters in ML.

---

## Month 4 — AI Engineering, API, Async, Workers

---

### Week 13: Embeddings and Semantic Search

**Chapter title:** Meaning as a vector

**Concepts:**
- What embeddings are: a dense numeric representation of meaning
- Chunking text for embedding: why long documents need to be split
- `sentence-transformers` local models: no API key, no network call needed
- Cosine similarity: angle between vectors as a measure of semantic closeness
- Embedding cache: don't recompute what you already have
- Retrieval evaluation: does the top result make sense?

**Project milestone:**
`researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.

**Main files:**
- `src/researchops/search/chunking.py` — text chunker
- `src/researchops/search/embeddings.py` — embedding generation and cache
- `src/researchops/search/vector_search.py` — cosine similarity ranking
- `src/researchops/core/interfaces.py` — `SearchEngine` protocol updated

**Tests:**
- `tests/unit/test_chunking.py`
- `tests/unit/test_vector_search.py` — cosine similarity with known vectors

**Validation command:**
```bash
researchops semantic-search "machine learning"
pytest tests/unit/test_chunking.py tests/unit/test_vector_search.py -v
```

**Expected learner capability:**
Can explain what an embedding is, implement cosine similarity search, chunk text for a retrieval pipeline, and explain why caching matters.

---

### Week 14: FastAPI Layer

**Chapter title:** Your work, available over HTTP

**Concepts:**
- FastAPI app factory pattern
- Route handlers that delegate to services (no business logic in routes)
- `Depends` for dependency injection
- Pydantic response models: validating what you return
- HTTP status codes: 200, 201, 404, 422, 500
- Testing with `httpx.AsyncClient` / `TestClient`

**Project milestone:**
`GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.

**Main files:**
- `src/researchops/api/main.py` — FastAPI app factory
- `src/researchops/api/routes/papers.py` — papers routes
- `src/researchops/api/routes/search.py` — search routes

**Tests:**
- `tests/e2e/test_api.py` — endpoint tests with TestClient

**Validation command:**
```bash
uvicorn researchops.api.main:app --reload &
curl http://localhost:8000/health
pytest tests/e2e/test_api.py -v
```

**Expected learner capability:**
Can define REST endpoints with FastAPI, inject dependencies, validate responses with Pydantic, and test the API without running a real server.

---

### Week 15: Async I/O Network Fetching

**Chapter title:** Waiting without blocking

**Concepts:**
- `asyncio` event loop: one thread, many concurrent waits
- `async def` and `await`: what they actually do
- `httpx.AsyncClient` for async HTTP requests
- Timeouts and retry logic: exponential backoff
- Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor
- `pytest-asyncio` for testing async code

**Project milestone:**
`researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.

**Main files:**
- `src/researchops/services/fetch_service.py` — async fetching with retry
- `src/researchops/cli/commands/ingest.py` — `fetch-url`, `fetch-arxiv` commands

**Tests:**
- `tests/unit/test_fetch_service.py` — mocked HTTP with monkeypatch

**Validation command:**
```bash
researchops fetch-arxiv "attention is all you need"
pytest tests/unit/test_fetch_service.py -v
```

**Expected learner capability:**
Can write async functions, apply timeouts and retries, avoid blocking the event loop, and test async code with pytest-asyncio.

---

### Week 16: Local Worker and Job System

**Chapter title:** Work that happens in the background

**Concepts:**
- Job state machine: pending → running → done / failed
- Persistent job queue in SQLite
- Worker loop: poll → claim → execute → update state
- Retry logic and idempotency
- Worker failure recovery without data corruption
- `JobService` and `JobRepository`

**Project milestone:**
`researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.

**Main files:**
- `src/researchops/storage/job_repository.py`
- `src/researchops/services/job_service.py`
- `src/researchops/workers/job_runner.py`
- `src/researchops/cli/commands/ingest.py` — `jobs list`, `jobs run`, `jobs retry` commands

**Tests:**
- `tests/unit/test_job_service.py` — state transitions with fake repo
- `tests/integration/test_job_repository.py`

**Validation command:**
```bash
researchops jobs list
researchops jobs run
pytest tests/unit/test_job_service.py -v
```

**Expected learner capability:**
Can implement a state machine, build a polling worker loop, design idempotent job processing, and explain how to recover from worker crashes safely.

---

## Month 5 — RAG, Production, Portfolio

---

### Week 17: RAG Assistant

**Chapter title:** Answers grounded in evidence

**Concepts:**
- Retrieve-then-generate: why generation without retrieval hallucinates
- Chunked retrieval: finding the right text fragments before generating
- Prompt engineering: grounding instructions, source citation requirements
- Hallucination detection: what happens when no relevant chunks exist
- `QAService` orchestration: retrieve → prompt → call LLM → return citations
- `ai/prompts.py`: where prompt templates live

**Project milestone:**
`researchops ask "What is attention?"` returns a cited answer based on retrieved paper chunks.

**Main files:**
- `src/researchops/services/qa_service.py`
- `src/researchops/ai/prompts.py`
- `src/researchops/cli/main.py` — `ask` command

**Tests:**
- `tests/unit/test_qa_service.py` — retrieval + prompt construction tested with fake search engine

**Validation command:**
```bash
researchops ask "What are transformers used for?"
pytest tests/unit/test_qa_service.py -v
```

**Expected learner capability:**
Can implement a retrieve-then-generate pipeline, write a grounding prompt, detect hallucination risk, and explain why citations matter in an AI assistant.

---

### Week 18: Docker and Environment Configuration

**Chapter title:** Shipping the whole system

**Concepts:**
- Dockerfile: `FROM`, `COPY`, `RUN`, `CMD`, layer caching
- Multi-stage builds: separate build and runtime layers
- `docker-compose.yml`: API and worker as separate services
- Volume mounts for the SQLite database
- Environment variable management: `.env`, `pydantic-settings`
- Testing the full stack in containers

**Project milestone:**
`docker-compose up` starts the API and worker. `curl http://localhost:8000/health` responds.

**Main files:**
- `Dockerfile`
- `docker-compose.yml`
- `.env.example` — documented environment variables
- `src/researchops/config/settings.py` — all config from env vars

**Tests:**
- `tests/e2e/test_docker.py` (optional) — smoke test against running container

**Validation command:**
```bash
docker-compose build
docker-compose up -d
curl http://localhost:8000/health
docker-compose down
```

**Expected learner capability:**
Can write a Dockerfile, compose multi-service applications, manage environment configuration with pydantic-settings, and explain layer caching.

---

### Week 19: Documentation and Portfolio Polish

**Chapter title:** Making your work legible to others

**Concepts:**
- Technical writing: what an architecture document must explain
- Mermaid diagrams: module dependency graph and data flow
- README as a portfolio artefact: what a hiring manager needs to see
- Demo script: a 5-minute walkthrough of the complete system
- Docs-as-code: keeping documentation in sync with behaviour

**Project milestone:**
README is portfolio-quality. Architecture document explains every design decision. A demo script exists.

**Main files:**
- `README.md` — polished, portfolio-ready
- `ARCHITECTURE.md` — complete with diagrams
- `docs/diagrams/` — at least one Mermaid diagram
- `scripts/demo.sh` — end-to-end demo script

**Tests:**
- All existing tests must still pass (no regressions)

**Validation command:**
```bash
pytest -q
ruff check src tests
researchops --help
```

**Expected learner capability:**
Can write a clear architecture document, create a Mermaid diagram, write a README a hiring manager would find compelling.

---

### Week 20: Final Hardening and v1.0 Release

**Chapter title:** Finishing is a skill

**Concepts:**
- Semantic versioning: MAJOR.MINOR.PATCH and what each number means
- Release checklist discipline: scope control, no new features before release
- Changelog writing: what changed, for whom, and why
- Git tagging: `git tag -a v1.0.0 -m "..."`
- Final retrospective: 20 weeks in review

**Project milestone:**
`v1.0.0` is tagged. CI is green. Every ROADMAP.md row is ✅. A demo exists. The project is portfolio-ready.

**Main files:**
- `CHANGELOG.md` — complete version history
- `ROADMAP.md` — all weeks marked ✅
- `pyproject.toml` — version bumped to `1.0.0`
- `src/researchops/__init__.py` — `__version__ = "1.0.0"`

**Tests:**
- All existing tests pass (no regressions introduced)
- End-to-end: `researchops --help`, full pipeline commands

**Validation command:**
```bash
pytest --cov=researchops --cov-report=term-missing -q
ruff check src tests
researchops --help
git tag v1.0.0
```

**Expected learner capability:**
Can apply semantic versioning, write a changelog, create a git tag, and explain what v1.0 means for a software project.
<!-- NAV_BOTTOM_START -->
---
[🏠 Home](README.md) · [🗺 Roadmap](ROADMAP.md) · **📋 Syllabus** · [📐 Project Spec](PROJECT_SPEC.md) · [🏛 Architecture](ARCHITECTURE.md) · [🤝 Contributing](CONTRIBUTING.md) · [✅ Release Checklist](RELEASE_CHECKLIST.md) · [🗂 Curriculum Map](curriculum/NAVIGATION.md)
---
<!-- NAV_BOTTOM_END -->
