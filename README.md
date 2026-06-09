<!-- NAV_START -->
---
**🏠 Home** · [🗺 Roadmap](ROADMAP.md) · [📋 Syllabus](SYLLABUS.md) · [📐 Project Spec](PROJECT_SPEC.md) · [🏛 Architecture](ARCHITECTURE.md) · [🤝 Contributing](CONTRIBUTING.md) · [✅ Release Checklist](RELEASE_CHECKLIST.md) · [🗂 Curriculum Map](curriculum/NAVIGATION.md)

---
<!-- NAV_END -->

# ResearchOps — Python Mastery Through a Real Project

> **Build a research paper processing platform. Master Python. Build a portfolio.**

---

## ► Start Here

This is not a tutorial. It is a **20-week structured programme** that teaches professional Python engineering by having you build a real, working software system from scratch — one week at a time.

Read this file first. Then open `curriculum/month-01-python-core/week-01-foundations/README.md` and begin Week 1.

---

## Learner Profile

**You are the right person for this if:**

- You know basic Python (variables, loops, functions, imports)
- You want to work as an AI engineer, ML researcher, or backend Python developer
- You have not yet built a project larger than a few hundred lines
- You are prepared to spend 8–12 hours per week for 20 weeks
- You want to finish with something you can show to a hiring manager

**You do not need** prior experience with:
- virtual environments or packaging
- SQL databases
- machine learning
- REST APIs
- Docker
- concurrent or async programming

All of that is taught, in order, from first principles.

---

## What is ResearchOps?

**ResearchOps** is a Python-based research paper processing and experiment-tracking platform.

At v1.0 it can:
- Scan a directory and discover PDF files
- Parse PDFs and extract text and metadata
- Store papers in a SQLite database
- Search papers by keyword and by semantic similarity
- Train a topic classifier using TF-IDF and scikit-learn
- Track ML experiment parameters and metrics
- Generate embeddings and answer questions with a RAG pipeline
- Expose all features over a REST API built with FastAPI
- Download papers from arXiv asynchronously
- Run expensive jobs in a background worker queue
- Deploy the full stack with `docker-compose up`

**ResearchOps is also a curriculum.** Every week you add a real feature to this platform while learning a specific set of Python and software engineering concepts through textbook-style notes, graded exercises, intentional failure experiments, strict validation checklists, and weekly journal prompts.

By the end you have both: the skills and the project.

---

## What This Repository Teaches

| Month | Theme | Skills |
|-------|-------|--------|
| 1 | Python Core + Project Foundation | Packaging, CLI, OOP, domain modeling, pathlib, logging |
| 2 | Storage, Search, Multiprocessing | SQLite, PDF parsing, keyword search, ProcessPoolExecutor |
| 3 | Advanced Python + ML Engineering | Protocols, clean architecture, pytest, TF-IDF, experiment tracking |
| 4 | AI Engineering, API, Async, Workers | Embeddings, FastAPI, asyncio, job queues |
| 5 | RAG, Production, Portfolio | RAG pipeline, Docker, documentation, v1.0 release |

---

## Setup — Exact Commands

Run these once. In order. Do not skip any.

```bash
# 1. Clone the repository
git clone https://github.com/Raj-Indra-Asura/researchops_python_mastery.git
cd researchops_python_mastery

# 2. Create a virtual environment (Python 3.11 or newer required)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install the project in development mode with dev dependencies
pip install -e ".[dev]"

# 5. Confirm the CLI is installed and responds
researchops --help

# 6. Run the first command (your Week 1 deliverable)
researchops scan ./examples/sample_papers

# 7. Confirm tests pass
pytest -q

# 8. Confirm linting is clean
ruff check src tests
```

If all of those work without errors, your environment is correct. If any step fails, read the error message carefully before searching for help.

---

## First Command

```bash
researchops scan ./examples/sample_papers
```

This is the first thing you build in Week 1. It scans a directory, finds PDF files, and prints their paths. It sounds small. It is not — it teaches project structure, packaging, CLI entry points, pathlib, and your first test.

---

## Weekly Study Loop

Every week follows the same rhythm. Do not skip any step.

```
1. Read   curriculum/month-XX/week-NN-NAME/README.md        — understand the goal
2. Read   curriculum/month-XX/week-NN-NAME/notes.md         — learn the concepts
3. Do     curriculum/month-XX/week-NN-NAME/exercises.md     — practise in isolation
4. Build  the deliverable described in the week README
5. Write  tests before or while you code — not after
6. Run    curriculum/month-XX/week-NN-NAME/validation.md    — must pass completely
7. Run    pytest -q && ruff check src tests                  — CI must be green
8. Fill   curriculum/month-XX/week-NN-NAME/reflection.md    — your learning journal
9. Commit git commit -m "week-NN: <what you built>"
```

**If you cannot fill in `reflection.md` in your own words, you have not learned it yet.** Go back.

---

## How to Read Weekly Files

Each week directory contains exactly 6 files:

| File | Purpose | How to use it |
|------|---------|---------------|
| `README.md` | Chapter overview, objectives, deliverables | Read first. Know the destination before you start. |
| `notes.md` | Textbook chapter (800–1500+ lines) | Read slowly. Annotate. Do not skim. |
| `exercises.md` | Graded workbook | Do all warm-ups and implementation exercises. Stretch exercises are optional but valuable. |
| `break_it.md` | Intentional failure lab | Run every experiment. Read every error message. This is where real debugging skill is built. |
| `validation.md` | Completion checkpoint | Run every command. Match every expected output. Do not move to the next week until all pass. |
| `reflection.md` | Weekly journal template | Write your own answers. No copy-paste. No Copilot. Your words only. |

---

## Month-by-Month Map

### Month 1 — Python Core and Project Foundation (Weeks 1–4)

You start with nothing and end with an installable Python package, a working CLI, and a domain model that can represent a research paper.

| Week | Title | Milestone | Builds on |
|------|-------|-----------|-----------|
| 1 | Python Foundations | `researchops scan ./papers` works; tests pass | — |
| 2 | Files, Errors, Logging | PDF discovery with structured logging and custom exceptions | Week 1 |
| 3 | OOP and Domain Modeling | `Paper`, `ParsedDocument`, `IngestionResult` defined and tested | Week 2 |
| 4 | CLI and Packaging | `pip install -e .` produces a working `researchops` command | Weeks 1–3 |

### Month 2 — Storage, Search, Multiprocessing (Weeks 5–8)

Builds on Month 1's installable package and domain models (`Paper`, `ParsedDocument`, `IngestionResult`). You persist data, parse real PDFs, search them, and parallelise expensive work.

| Week | Title | Milestone | Builds on |
|------|-------|-----------|-----------|
| 5 | SQLite Storage Layer | Papers persist and retrieve from SQLite | Week 3 domain models |
| 6 | PDF Parsing Pipeline | `researchops ingest ./papers` extracts and stores text | Week 5 storage |
| 7 | Keyword Search + Data Quality | `researchops search "query"` returns ranked results | Week 6 ingestion |
| 8 | Multiprocessing Ingestion | `--workers 4` parallelises ingestion via ProcessPoolExecutor | Weeks 6–7 |

### Month 3 — Advanced Python and ML Engineering (Weeks 9–12)

Builds on Month 2's storage and ingestion pipeline. You formalise the architecture by introducing clean interfaces, enforce test coverage, add a topic classifier, and track every experiment run.

| Week | Title | Milestone | Builds on |
|------|-------|-----------|-----------|
| 9 | Protocols and Clean Architecture | Services depend on protocols; fake repos in tests | Weeks 5–8 |
| 10 | Testing Discipline and CI | 70%+ coverage; CI passes on every push | Week 9 |
| 11 | Classical ML: Topic Classification | `researchops classify PAPER_ID` returns a topic | Week 10 testing |
| 12 | Experiment Tracking | `researchops experiment list` shows run history | Week 11 ML |

### Month 4 — AI Engineering, API, Async, Workers (Weeks 13–16)

Builds on Month 3's clean protocols and test suite. You add vector search, expose everything over a REST API, add async HTTP fetching, and build a background job system — the platform's first distributed-computing layer.

| Week | Title | Milestone | Builds on |
|------|-------|-----------|-----------|
| 13 | Embeddings and Semantic Search | `researchops semantic-search "query"` uses cosine similarity | Week 9 protocols |
| 14 | FastAPI Layer | `GET /papers` and `GET /papers/search?q=` work | Weeks 9–12 services |
| 15 | Async I/O Network Fetching | `researchops fetch-arxiv QUERY` downloads papers | Week 14 API |
| 16 | Local Worker and Job System | `researchops jobs run` processes a background queue | Weeks 13–15 |

### Month 5 — RAG, Production, Portfolio (Weeks 17–20)

Builds on all four prior months: the semantic search from Month 4, the experiment tracking from Month 3, and the storage layer from Month 2, all composed into a RAG assistant. You containerise the complete stack, write production documentation, and ship v1.0.

| Week | Title | Milestone | Builds on |
|------|-------|-----------|-----------|
| 17 | RAG Assistant | `researchops ask "question"` returns cited answer | Weeks 13 + 16 |
| 18 | Docker and Environment Config | `docker-compose up` starts the full stack | Weeks 14–17 |
| 19 | Documentation and Portfolio Polish | README, diagrams, demo script complete | All prior weeks |
| 20 | Final Hardening and v1.0 Release | CI green, `v1.0.0` tag, changelog, demo ready | Week 19 |

---

## How to Validate Each Week

Every week has a `validation.md`. It contains:
- A pre-flight checklist (read before you start)
- Exact shell commands to run
- Exact expected outputs to match
- Tests that must pass
- Manual checks
- Architecture checks
- A ruthless mentor checkpoint: "would you let a colleague review this?"

**Do not move to the next week until your `validation.md` is completely green.**

Quick validation loop for any week:

```bash
pytest -q                          # all tests must pass
ruff check src tests               # no lint errors
researchops --help                 # CLI must respond
```

---

## ⚠️ Do Not Skip Weeks

Every week builds on the previous one. This is not a warning about difficulty. It is a warning about architecture.

- The domain models defined in Week 3 are imported in every subsequent week
- The protocol contracts introduced in Week 9 are what make Weeks 11–17 testable
- The storage layer built in Week 5 is extended in Weeks 6, 12, and 16
- The embedding module built in Week 13 is a prerequisite for Week 17's RAG pipeline

Skipping a week means building on a foundation you do not understand. The project will break in ways you cannot diagnose.

---

## How to Use AI Assistance Responsibly

Copilot and ChatGPT are permitted. They are also dangerous for learning.

**Use AI to:**
- Understand an error message you have already read and thought about
- Check whether your approach is idiomatic
- Explain a Python concept after you have formed your own hypothesis
- Review code you have already written

**Do not use AI to:**
- Write your implementation before you understand the concept
- Skip exercises because AI can do them
- Generate your `reflection.md` answers
- Write tests you do not understand

**The test:** after completing a week, close your laptop and explain what you built and why, out loud, to yourself or someone else. If you can do that, you learned it. If you cannot, AI did the week for you.

---

## Repository Map

```
researchops_python_mastery/
├── README.md                    ← You are here. Start here.
├── ROADMAP.md                   ← 20-week milestone tracker (update as you go)
├── SYLLABUS.md                  ← Full table of contents: all 20 chapters
├── PROJECT_SPEC.md              ← Complete feature specification and CLI/API reference
├── ARCHITECTURE.md              ← Module boundaries, dependency rules, design rationale
├── CONTRIBUTING.md              ← Learner workflow: branch names, commits, testing, Copilot rules
├── RELEASE_CHECKLIST.md         ← Per-release checklists v0.1 → v1.0
├── CHANGELOG.md                 ← Version history
├── pyproject.toml               ← Package config, dependencies, entry points
│
├── .github/
│   ├── copilot-instructions.md  ← AI assistant rules for this repository
│   └── workflows/ci.yml         ← Lint + test on every push
│
├── curriculum/                  ← 20 weeks × 6 files each
│   ├── month-01-python-core/
│   │   ├── week-01-foundations/
│   │   │   ├── README.md        ← Chapter overview, objectives, deliverables
│   │   │   ├── notes.md         ← Textbook chapter (800–1500+ lines)
│   │   │   ├── exercises.md     ← Warm-up → implementation → stretch
│   │   │   ├── break_it.md      ← Intentional failure experiments
│   │   │   ├── validation.md    ← Exact commands and expected outputs
│   │   │   └── reflection.md    ← Weekly journal prompts
│   │   ├── week-02-files-errors-logging/
│   │   ├── week-03-oop-domain-modeling/
│   │   └── week-04-cli-packaging/
│   ├── month-02-data-storage-concurrency/
│   ├── month-03-ml-engineering/
│   ├── month-04-ai-engineering-api-workers/
│   └── month-05-production-portfolio/
│
├── src/
│   └── researchops/             ← Main package
│       ├── core/                ← Domain models, protocols, exceptions (no external imports)
│       ├── config/              ← Settings and logging configuration
│       ├── parsing/             ← PDF parser, text cleaner, metadata extractor
│       ├── storage/             ← SQLite repositories
│       ├── services/            ← Use-case orchestration layer
│       ├── workers/             ← ProcessPoolExecutor, background job runner
│       ├── ml/                  ← TF-IDF, topic classifier, evaluation
│       ├── search/              ← Chunking, embeddings, vector search
│       ├── ai/                  ← RAG prompt templates
│       ├── cli/                 ← Typer CLI commands
│       └── api/                 ← FastAPI routes
│
├── tests/
│   ├── unit/                    ← Pure function and service tests (no I/O)
│   ├── integration/             ← Tests that use a real (tmp) SQLite database
│   ├── e2e/                     ← CLI and API tests via CliRunner / httpx
│   └── fakes/                   ← In-memory fake implementations of core protocols
│
├── examples/
│   ├── sample_papers/           ← PDF fixtures for manual testing
│   └── sample_outputs/          ← Example command outputs
├── scripts/
└── docs/
    ├── decisions/               ← Architecture decision records
    └── diagrams/                ← Module dependency and data flow diagrams
```

---

## Final Portfolio Outcome

After 20 weeks you will have:

1. **A working software system** — ResearchOps v1.0, installable, testable, and containerised
2. **A portfolio README** — explains the architecture, demonstrates every feature, includes a demo
3. **Demonstrated skills** — clean Python architecture, REST API, ML pipeline, semantic search, RAG, Docker, CI/CD
4. **20 weeks of commit history** — proof of consistent engineering discipline

The project is designed to answer the exact questions a hiring manager asks: "Can you build something real? Can you test it? Can you explain the architecture? Can you ship it?"

---

## How to Run Tests

```bash
pytest                                              # all tests
pytest tests/unit/ -v                              # unit tests only
pytest tests/integration/ -v                       # integration tests
pytest --cov=researchops --cov-report=term-missing # with coverage (must be ≥ 70%)
ruff check src tests                               # lint check
```

---

## License

MIT
<!-- NAV_BOTTOM_START -->
---
**🏠 Home** · [🗺 Roadmap](ROADMAP.md) · [📋 Syllabus](SYLLABUS.md) · [📐 Project Spec](PROJECT_SPEC.md) · [🏛 Architecture](ARCHITECTURE.md) · [🤝 Contributing](CONTRIBUTING.md) · [✅ Release Checklist](RELEASE_CHECKLIST.md) · [🗂 Curriculum Map](curriculum/NAVIGATION.md)
---
<!-- NAV_BOTTOM_END -->
