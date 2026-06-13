# Beginner Code Walkthrough

This guide explains the current ResearchOps codebase file by file. It is intentionally beginner-friendly: each section says what the file is for, why it exists, and how it fits into the larger project.

Read this alongside `ARCHITECTURE.md`. The architecture explains the rules; this walkthrough explains the current files.

---

## Big picture

ResearchOps is a Python package under `src/researchops`. The package is split into layers:

- `core/` defines the project language: models, value objects, exceptions, and protocols.
- `services/` contains use cases and business workflows.
- `storage/`, `parsing/`, `ml/`, `search/`, `ai/`, and `workers/` contain infrastructure details.
- `cli/` and `api/` are entry points that connect users to the services.
- `tests/` proves behavior with unit, integration, and end-to-end tests.

The most important rule: inner layers should not depend on outer layers. Core stays small and independent so everything else can build on it safely.

---

## `src/researchops/core/`

### `core/models.py`

Defines the main data shapes used by the project, such as papers, parsed documents, failed documents, ingestion results, search results, experiments, and jobs. These models are plain Python objects that describe what ResearchOps knows about research papers and processing work.

A beginner should think of this file as the project dictionary. When another file says “Paper” or “SearchResult,” this is where that word gets its exact meaning.

### `core/value_objects.py`

Defines small validated wrappers such as IDs, queries, and tags. A value object protects the code from passing around vague strings when the string has a specific meaning.

For example, a search query is not just any text. It should be non-empty and safe to use as a query. Putting that rule in one value object keeps the rest of the project simpler.

### `core/exceptions.py`

Defines project-specific error types. Instead of every failure being a generic `Exception`, ResearchOps can raise names such as scan, parse, storage, and search errors.

This helps beginners learn that errors are part of the design. A good project does not only handle the happy path; it gives failures clear names.

### `core/interfaces.py`

Defines protocol contracts for things the project needs, such as repositories, parsers, search engines, experiment storage, and job storage. A protocol describes what methods an object must provide without saying which concrete class must provide them.

This is what lets services depend on ideas instead of specific tools. For example, a service can depend on a paper repository protocol without knowing whether the data is stored in SQLite, memory, or a future database.

### `core/__init__.py`

Marks `core` as a package. It usually stays small because the important definitions live in the specific files above.

---

## `src/researchops/config/`

### `config/settings.py`

Centralizes application settings. Settings are values that may change between machines or environments, such as paths, environment names, or feature configuration.

Beginners should notice that configuration is kept separate from business logic. This prevents hard-coded local paths from leaking into the code.

### `config/logging.py`

Configures logging for the application. Logging is how production code records what happened without using random `print()` statements everywhere.

A beginner mental model: logging is the application’s notebook. It helps you understand what the program did when something succeeds or fails.

### `config/__init__.py`

Marks `config` as a package.

---

## `src/researchops/utils/`

### `utils/paths.py`

Contains reusable path helpers such as finding PDF files, creating directories safely, and resolving paths. This file uses `pathlib`, which works across Windows, macOS, and Linux.

This is one of the first practical files learners meet. It teaches that file handling should be explicit, testable, and cross-platform.

### `utils/hashing.py`

Contains helpers for producing stable hashes. Hashes are useful when the project needs a repeatable fingerprint for content, files, or identifiers.

A beginner can think of a hash as a short label calculated from data. If the data changes, the label changes.

### `utils/serialization.py`

Contains helpers for converting project objects into serializable forms and back. Serialization matters when data must be saved, logged, returned from an API, or compared in tests.

### `utils/__init__.py`

Marks `utils` as a package.

---

## `src/researchops/cli/`

### `cli/main.py`

Defines the Typer command-line application. This is where the `researchops` command begins when a learner runs it from a terminal.

The CLI should collect user input, call services or helpers, and display results. It should not become the place where business logic grows.

### `cli/commands/ingest.py`

Contains ingestion-related CLI commands. Ingestion means taking paper files, extracting useful information, and saving or reporting the result.

### `cli/commands/papers.py`

Contains paper-related CLI commands, such as listing, showing, or summarizing papers. These commands are user-facing entry points for paper data.

### `cli/commands/search.py`

Contains search-related CLI commands. It connects user text input to the project’s search behavior.

### `cli/commands/experiments.py`

Contains experiment-tracking CLI commands. These commands become important when the curriculum reaches ML training and needs to record parameters and metrics.

### `cli/__init__.py` and `cli/commands/__init__.py`

Mark CLI directories as packages.

---

## `src/researchops/services/`

### `services/ingestion_service.py`

Coordinates the ingestion workflow. A service like this decides the order of operations: discover input, parse documents, store successes, and record failures.

The service layer is where beginner scripts start becoming professional workflows. It keeps orchestration out of the CLI.

### `services/paper_service.py`

Provides paper-related use cases. It can sit between entry points and repositories so CLI/API code does not need to know storage details.

### `services/search_service.py`

Provides search use cases. It receives a query, asks a search implementation for results, and returns results in a project-friendly form.

### `services/experiment_service.py`

Provides experiment-tracking use cases. It helps create runs, log parameters and metrics, and compare outcomes.

### `services/fetch_service.py`

Provides network-fetching behavior for downloading papers or metadata. Network work belongs in a service so command handlers remain thin.

### `services/job_service.py`

Provides job queue use cases, such as creating jobs, updating status, retrying failures, and managing background work.

### `services/qa_service.py`

Provides question-answering use cases for the later RAG assistant. It connects retrieval results to prompt construction and answer generation.

### `services/__init__.py`

Marks `services` as a package.

---

## `src/researchops/storage/`

### `storage/sqlite_repository.py`

Implements repository behavior using SQLite. SQLite stores data in a local `.db` file, which is ideal for a single-user learning project.

This file is infrastructure: it knows SQL and database details so services do not have to.

### `storage/experiment_repository.py`

Stores and retrieves experiment tracking data. This supports later ML weeks where learners compare model runs.

### `storage/job_repository.py`

Stores and retrieves background job data. This supports worker behavior in later weeks.

### `storage/__init__.py`

Marks `storage` as a package.

---

## `src/researchops/parsing/`

### `parsing/pdf_parser.py`

Extracts text from PDF files. PDF parsing is infrastructure because it depends on file formats and third-party libraries.

### `parsing/text_cleaner.py`

Cleans raw text after extraction. This can include normalizing whitespace, removing unwanted characters, or preparing text for search and ML.

### `parsing/metadata_extractor.py`

Attempts to find structured metadata such as title, authors, and abstract from raw paper text.

### `parsing/__init__.py`

Marks `parsing` as a package.

---

## `src/researchops/ml/`

### `ml/preprocessing.py`

Prepares text for machine learning. Preprocessing turns raw text into a form that models can consume.

### `ml/topic_classifier.py`

Contains topic classification behavior. A classifier predicts a label or topic for a paper based on its text.

### `ml/evaluation.py`

Contains helpers for evaluating ML results. Evaluation answers the question: how well did the model perform?

### `ml/__init__.py`

Marks `ml` as a package.

---

## `src/researchops/search/`

### `search/chunking.py`

Splits long documents into smaller chunks. Chunking is necessary because search and embedding systems usually work better on smaller pieces of text.

### `search/embeddings.py`

Creates or manages vector representations of text. An embedding is a list of numbers that captures meaning well enough for similarity search.

### `search/vector_search.py`

Searches over vectors, usually by comparing similarity. This supports semantic search, where results are based on meaning rather than exact keyword matches.

### `search/__init__.py`

Marks `search` as a package.

---

## `src/researchops/ai/`

### `ai/prompts.py`

Stores prompt templates for the RAG assistant. Keeping prompts in one file makes them easier to review, test, and improve.

### `ai/__init__.py`

Marks `ai` as a package.

---

## `src/researchops/workers/`

### `workers/process_pool.py`

Contains multiprocessing helpers for CPU-heavy work. PDF parsing and ML inference can be expensive, so later weeks move that work away from the main process.

### `workers/job_runner.py`

Runs background jobs from the local job queue. A job runner lets ResearchOps process long-running work without forcing every action to happen immediately in the CLI or API request.

### `workers/__init__.py`

Marks `workers` as a package.

---

## `src/researchops/api/`

### `api/main.py`

Defines the FastAPI application for the later REST API layer. The API lets other programs call ResearchOps over HTTP.

### `api/routes/__init__.py`

Marks the routes directory as a package. Route modules are where API endpoint groups can live as the project grows.

### `api/__init__.py`

Marks `api` as a package.

---

## `src/researchops/__init__.py`

Marks `researchops` as the top-level package. This is what makes imports such as `import researchops` possible after installation.

---

## `tests/`

### Unit tests

Files under `tests/unit/` test small pieces of behavior in isolation. Examples include path helpers, value objects, serialization, hashing, text cleaning, metadata extraction, services, models, and exceptions.

Unit tests should be fast and focused. They should not require a real database, network connection, or hard-coded local path.

Current unit test files:

- `tests/unit/test_paths.py` checks file and directory helpers.
- `tests/unit/test_value_objects.py` checks validated wrappers such as queries, IDs, and tags.
- `tests/unit/test_search_service.py` checks search use cases without needing real search infrastructure.
- `tests/unit/test_serialization.py` checks conversion between project objects and serializable data.
- `tests/unit/test_metadata_extractor.py` checks metadata extraction from text.
- `tests/unit/test_hashing.py` checks stable hash behavior.
- `tests/unit/test_ingestion_service.py` checks the ingestion workflow with fake dependencies.
- `tests/unit/test_text_cleaner.py` checks text normalization and cleanup.
- `tests/unit/test_exceptions.py` checks the project exception hierarchy.
- `tests/unit/test_paper_service.py` checks paper-related use cases.
- `tests/unit/test_sanity.py` provides a simple proof that the test setup works.
- `tests/unit/test_models.py` checks domain model behavior.

### Integration tests

Files under `tests/integration/` test behavior that crosses a boundary, such as SQLite persistence. These tests may use temporary files or a temporary database because the point is to verify that the infrastructure really works.

Current integration test files:

- `tests/integration/test_sqlite_repository.py` checks that the SQLite repository really saves and loads data.

### End-to-end tests

Files under `tests/e2e/` test the CLI the way a learner or user would run it. These tests prove that command wiring, output, and exit codes work together.

Current end-to-end test files:

- `tests/e2e/test_cli.py` checks the `researchops` command, help output, scan behavior, and CLI exit codes.

### Fakes

Files under `tests/fakes/` provide simple in-memory implementations of core protocols. Fakes make service tests easier because they avoid real infrastructure while still behaving like the needed dependency.

Current fake files:

- `tests/fakes/fake_repository.py` provides in-memory repository behavior for service tests.

---

## How to read a new file in this project

When you open any source file, ask these beginner questions:

1. Which layer is this file in?
2. Is it defining a data shape, a use case, infrastructure, or an entry point?
3. What other modules does it import?
4. Does the import direction match `ARCHITECTURE.md`?
5. What tests prove this file works?
6. What would break if this file changed?

Those questions matter more than memorizing code. They teach you how to navigate a professional Python project from first principles.
