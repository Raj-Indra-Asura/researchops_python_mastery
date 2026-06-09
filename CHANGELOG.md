# Changelog

All notable changes to ResearchOps are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [Unreleased]

### Added
- Complete root documentation synchronisation: README.md, SYLLABUS.md, ARCHITECTURE.md, CONTRIBUTING.md, RELEASE_CHECKLIST.md, CHANGELOG.md, .github/copilot-instructions.md all updated to reflect the fully expanded 20-week curriculum

---

## [0.1.0] — Initial scaffold

### Added
- Project scaffold with `src/` layout and `pyproject.toml`
- Core domain models: `Paper`, `ParsedDocument`, `IngestionResult`, `FailedDocument`, `SearchResult`
- Custom exception hierarchy: `ResearchOpsError`, `ScanError`, `ParseError`, `StorageError`, `SearchError`
- `typing.Protocol` interfaces for `PaperRepository`, `DocumentParser`, `SearchEngine` in `core/interfaces.py`
- Value objects: `PaperId`, `Query`, `Tag`
- `researchops scan PATH` CLI command using Typer
- `find_pdfs()` utility in `src/researchops/utils/paths.py`
- `pytest` test setup with `tests/unit/`, `tests/integration/`, `tests/e2e/`, `tests/fakes/`
- `ruff` lint configuration
- GitHub Actions CI workflow (lint + test on every push)
- 20-week curriculum scaffold with all 20 week directories and 6 files each
- `ROADMAP.md`, `SYLLABUS.md`, `PROJECT_SPEC.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`
- `src/researchops/config/settings.py` — Pydantic Settings
- `src/researchops/config/logging.py` — Rich + plain logging configuration

### Planned for v0.2.0
- `SqlitePaperRepository` implementing `PaperRepository` protocol
- `IngestionService` — PDF discovery → parse → save pipeline
- `researchops ingest PATH` CLI command
- `researchops papers list`, `papers show`, `papers stats`, `papers failed` commands

### Planned for v0.3.0
- `SearchService` with keyword search and text normalisation
- `researchops search QUERY` CLI command
- `ProcessPoolExecutor`-based parallel ingestion
- `researchops ingest --workers N` option

### Planned for v0.4.0
- All services refactored to depend on `core/interfaces.py` protocols only
- `tests/fakes/` fake implementations for all protocols
- Coverage gate at 70% enforced in CI

### Planned for v0.5.0
- TF-IDF + logistic regression topic classifier
- `researchops train-topic-model` and `researchops classify PAPER_ID` commands

### Planned for v0.6.0
- `ExperimentRepository` and `ExperimentService`
- `researchops experiment` command group

### Planned for v0.7.0
- Text chunking, local embeddings, cosine similarity search
- `researchops semantic-search QUERY` command

### Planned for v0.8.0
- FastAPI REST API
- Async HTTP fetching with retry
- `researchops fetch-arxiv QUERY` command

### Planned for v0.9.0
- Job queue and background worker
- RAG question-answering assistant
- `researchops ask QUESTION` command

### Planned for v1.0.0
- Docker and docker-compose deployment
- Complete documentation and portfolio-ready README
- `v1.0.0` git tag

---

[Unreleased]: https://github.com/Raj-Indra-Asura/researchops_python_mastery/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Raj-Indra-Asura/researchops_python_mastery/releases/tag/v0.1.0
