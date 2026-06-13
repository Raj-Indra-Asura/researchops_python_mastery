<!-- NAV_START -->
---
[🏠 Home](README.md) · [🗺 Roadmap](ROADMAP.md) · [📋 Syllabus](SYLLABUS.md) · [📐 Project Spec](PROJECT_SPEC.md) · [🏛 Architecture](ARCHITECTURE.md) · [🤝 Contributing](CONTRIBUTING.md) · **✅ Release Checklist** · [🗂 Curriculum Map](curriculum/NAVIGATION.md)

---
<!-- NAV_END -->

# ResearchOps — Release Checklist

This document tracks the checklist for each versioned release. Complete every item before tagging.

When you complete a release: update CHANGELOG.md, bump the version in `pyproject.toml` and `src/researchops/__init__.py`, then tag.

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

---

## v0.1 — Scanner Release (Week 1 milestone)

**What is included:** project scaffold, CLI entry point, PDF directory scanner.

### Code
- [ ] `researchops scan PATH` prints discovered PDF paths
- [ ] `researchops scan PATH --recursive` descends into subdirectories
- [ ] Empty directory prints a clear message, does not crash
- [ ] Invalid path raises a `ScanError` with a useful message

### Tests
- [ ] `tests/unit/test_paths.py` — `find_pdfs()` passes
- [ ] `tests/e2e/test_cli.py` — `researchops scan` exits 0
- [ ] `pytest -q` — all tests pass

### Quality
- [ ] `ruff check src tests` — zero errors
- [ ] `researchops --help` — responds with usage text

### Documentation
- [ ] `ROADMAP.md` Week 1 row marked ✅
- [ ] `CHANGELOG.md` `[0.1.0]` entry written
- [ ] `pyproject.toml` version set to `0.1.0`

---

## v0.2 — Storage and Ingestion Release (Weeks 2–6 milestone)

**What is included:** custom exceptions, logging, domain models, CLI packaging, SQLite storage, PDF parsing pipeline.

### Code
- [ ] `researchops ingest PATH` parses PDFs and stores them in SQLite
- [ ] `researchops papers list` shows stored papers
- [ ] `researchops papers failed` shows documents that failed to ingest
- [ ] `researchops papers stats` shows paper count and failure count
- [ ] Custom exceptions (`ScanError`, `ParseError`, `StorageError`) are raised on error
- [ ] All log messages use `logging`, not `print()`

### Tests
- [ ] `tests/unit/test_models.py` — all domain models pass
- [ ] `tests/unit/test_exceptions.py` — exception hierarchy correct
- [ ] `tests/integration/test_sqlite_repository.py` — save, retrieve, list pass
- [ ] `tests/integration/test_ingestion_service.py` — full pipeline with sample PDF
- [ ] `pytest -q` — all tests pass

### Quality
- [ ] `ruff check src tests` — zero errors
- [ ] Coverage ≥ 50% (target grows each release)

### Documentation
- [ ] `ROADMAP.md` Weeks 2–6 rows marked ✅
- [ ] `CHANGELOG.md` `[0.2.0]` entry written
- [ ] `pyproject.toml` version set to `0.2.0`

---

## v0.3 — Search and Multiprocessing Release (Weeks 7–8 milestone)

**What is included:** keyword search, text normalisation, data quality reporting, parallel ingestion.

### Code
- [ ] `researchops search "query"` returns ranked results
- [ ] `researchops ingest PATH --workers N` uses N parallel worker processes
- [ ] Ingestion failure in one worker does not crash the batch
- [ ] `researchops papers stats` includes failure rate

### Tests
- [ ] `tests/unit/test_search_service.py` — search with fake repository passes
- [ ] `tests/unit/test_process_pool.py` — parallel execution tests pass
- [ ] `pytest -q` — all tests pass

### Quality
- [ ] `ruff check src tests` — zero errors
- [ ] Coverage ≥ 55%

### Documentation
- [ ] `ROADMAP.md` Weeks 7–8 rows marked ✅
- [ ] `CHANGELOG.md` `[0.3.0]` entry written
- [ ] `pyproject.toml` version set to `0.3.0`

---

## v0.4 — Architecture and Testing Release (Weeks 9–10 milestone)

**What is included:** Protocols in `core/interfaces.py`, dependency inversion enforced, fake repositories, coverage gate at 70%.

### Code
- [ ] All services depend only on `core/interfaces.py` protocols
- [ ] No service imports from `storage/`, `parsing/`, `ml/`, or `search/` directly
- [ ] `tests/fakes/` contains fake implementations of all protocols
- [ ] `isinstance(fake, PaperRepository)` returns `True` for all fakes

### Tests
- [ ] All service unit tests use fakes
- [ ] `pytest --cov=researchops --cov-report=term-missing -q` — coverage ≥ 70%
- [ ] CI workflow passes on push

### Quality
- [ ] `ruff check src tests` — zero errors
- [ ] Coverage gate `fail_under = 70` in `pyproject.toml`

### Documentation
- [ ] `ROADMAP.md` Weeks 9–10 rows marked ✅
- [ ] `CHANGELOG.md` `[0.4.0]` entry written
- [ ] `pyproject.toml` version set to `0.4.0`

---

## v0.5 — ML Classifier Release (Week 11 milestone)

**What is included:** TF-IDF + logistic regression topic classifier, training CLI, prediction CLI.

### Code
- [ ] `researchops train-topic-model` trains a classifier and saves it to disk
- [ ] `researchops classify PAPER_ID` returns the predicted topic label
- [ ] `researchops topics` lists all known topic labels
- [ ] Classifier is saved with `joblib` to a configured artifacts directory

### Tests
- [ ] `tests/unit/test_topic_classifier.py` — train, predict, evaluate pass
- [ ] `pytest -q` — all tests pass, coverage ≥ 70%

### Quality
- [ ] `ruff check src tests` — zero errors

### Documentation
- [ ] `ROADMAP.md` Week 11 row marked ✅
- [ ] `CHANGELOG.md` `[0.5.0]` entry written
- [ ] `pyproject.toml` version set to `0.5.0`

---

## v0.6 — Experiment Tracking Release (Week 12 milestone)

**What is included:** experiment run persistence in SQLite, params/metrics logging, run comparison CLI.

### Code
- [ ] `researchops experiment create NAME` creates a new experiment run
- [ ] `researchops experiment log-param RUN_ID KEY VALUE` records a param
- [ ] `researchops experiment log-metric RUN_ID KEY VALUE` records a metric
- [ ] `researchops experiment list` shows all runs with params and metrics
- [ ] `researchops experiment compare` shows the run with the best F1

### Tests
- [ ] `tests/unit/test_experiment_service.py` — CRUD operations with fake repo pass
- [ ] `tests/integration/test_experiment_repository.py` — SQLite persistence pass
- [ ] `pytest -q` — all tests pass, coverage ≥ 70%

### Quality
- [ ] `ruff check src tests` — zero errors

### Documentation
- [ ] `ROADMAP.md` Week 12 row marked ✅
- [ ] `CHANGELOG.md` `[0.6.0]` entry written
- [ ] `pyproject.toml` version set to `0.6.0`

---

## v0.7 — Semantic Search Release (Week 13 milestone)

**What is included:** text chunking, local embedding generation, cosine similarity search.

### Code
- [ ] `researchops semantic-search "query"` returns papers ranked by vector similarity
- [ ] Embeddings are cached to avoid recomputation
- [ ] `search/chunking.py`, `search/embeddings.py`, `search/vector_search.py` all in place
- [ ] `core/interfaces.py` has `SearchEngine` protocol for semantic search

### Tests
- [ ] `tests/unit/test_chunking.py` — chunk size and overlap tests pass
- [ ] `tests/unit/test_vector_search.py` — cosine similarity with known vectors passes
- [ ] `pytest -q` — all tests pass, coverage ≥ 70%

### Quality
- [ ] `ruff check src tests` — zero errors

### Documentation
- [ ] `ROADMAP.md` Week 13 row marked ✅
- [ ] `CHANGELOG.md` `[0.7.0]` entry written
- [ ] `pyproject.toml` version set to `0.7.0`

---

## v0.8 — API and Async Release (Weeks 14–15 milestone)

**What is included:** FastAPI REST API, async HTTP fetching with retry.

### Code
- [ ] `GET /health` responds with `{"status": "ok"}`
- [ ] `GET /papers` returns a list of stored papers as JSON
- [ ] `GET /papers/{id}` returns a single paper or 404
- [ ] `GET /papers/search?q=QUERY` returns search results
- [ ] `POST /papers/ingest` triggers ingestion
- [ ] `researchops fetch-url URL` fetches a paper asynchronously
- [ ] `researchops fetch-arxiv QUERY` fetches papers from arXiv API

### Tests
- [ ] `tests/e2e/test_api.py` — all endpoints return correct status codes
- [ ] `tests/unit/test_fetch_service.py` — HTTP fetching with mocked network passes
- [ ] `pytest -q` — all tests pass, coverage ≥ 70%

### Quality
- [ ] `ruff check src tests` — zero errors

### Documentation
- [ ] `ROADMAP.md` Weeks 14–15 rows marked ✅
- [ ] `CHANGELOG.md` `[0.8.0]` entry written
- [ ] `pyproject.toml` version set to `0.8.0`

---

## v0.9 — Workers and RAG Release (Weeks 16–17 milestone)

**What is included:** persistent job queue, background worker, RAG question-answering assistant.

### Code
- [ ] `researchops jobs list` shows all jobs and their states
- [ ] `researchops jobs run` starts a worker that processes pending jobs
- [ ] `researchops jobs retry JOB_ID` retries a failed job
- [ ] `researchops ask "question"` returns a cited answer based on retrieved chunks
- [ ] RAG answer includes source paper titles

### Tests
- [ ] `tests/unit/test_job_service.py` — state machine transitions pass
- [ ] `tests/integration/test_job_repository.py` — persistence pass
- [ ] `tests/unit/test_qa_service.py` — retrieval + prompt construction pass
- [ ] `pytest -q` — all tests pass, coverage ≥ 70%

### Quality
- [ ] `ruff check src tests` — zero errors

### Documentation
- [ ] `ROADMAP.md` Weeks 16–17 rows marked ✅
- [ ] `CHANGELOG.md` `[0.9.0]` entry written
- [ ] `pyproject.toml` version set to `0.9.0`

---

## v1.0 — Production Release (Weeks 18–20 milestone)

**What is included:** Docker deployment, complete documentation, portfolio-ready README, v1.0.0 tag.

### Code
- [ ] `docker compose up` starts API and worker containers on Windows, macOS, or Linux; Windows requires Docker Desktop running. Use `docker-compose up` only on older Compose installations.
- [ ] `curl http://localhost:8000/health` responds with `{"status": "ok"}`
- [ ] All configuration is managed via environment variables, not hard-coded paths
- [ ] `.env.example` documents every required environment variable

### Tests
- [ ] `pytest --cov=researchops --cov-report=term-missing -q` — all tests pass, coverage ≥ 70%
- [ ] `ruff check src tests` — zero errors
- [ ] CI workflow on GitHub Actions is green

### Full pipeline validation
- [ ] `researchops ingest ./examples/sample_papers --workers 2` — completes without error
- [ ] `researchops papers list` — shows ingested papers
- [ ] `researchops search "machine learning"` — returns results
- [ ] `researchops semantic-search "transformers"` — returns results
- [ ] `researchops train-topic-model` — trains and saves model
- [ ] `researchops classify PAPER_ID` — returns a topic
- [ ] `researchops ask "What is attention?"` — returns a cited answer
- [ ] `uvicorn researchops.api.main:app` — starts without error after `python -m pip install -e ".[api]"` in the active virtual environment

### Documentation
- [ ] `README.md` is portfolio-quality — a hiring manager could understand the project in 5 minutes
- [ ] `ARCHITECTURE.md` explains every design decision
- [ ] `CHANGELOG.md` has complete version history from `[0.1.0]` to `[1.0.0]`
- [ ] `ROADMAP.md` — all 20 weeks marked ✅
- [ ] `docs/diagrams/` contains at least one architecture diagram
- [ ] `pyproject.toml` version set to `1.0.0`
- [ ] `src/researchops/__init__.py` has `__version__ = "1.0.0"`

### Release
- [ ] Git tag created: `git tag -a v1.0.0 -m "ResearchOps v1.0.0"`
- [ ] Tag pushed: `git push origin v1.0.0`
- [ ] GitHub release created with release notes
- [ ] Demo video or demo script exists and works end-to-end
<!-- NAV_BOTTOM_START -->
---
[🏠 Home](README.md) · [🗺 Roadmap](ROADMAP.md) · [📋 Syllabus](SYLLABUS.md) · [📐 Project Spec](PROJECT_SPEC.md) · [🏛 Architecture](ARCHITECTURE.md) · [🤝 Contributing](CONTRIBUTING.md) · **✅ Release Checklist** · [🗂 Curriculum Map](curriculum/NAVIGATION.md)
---
<!-- NAV_BOTTOM_END -->
