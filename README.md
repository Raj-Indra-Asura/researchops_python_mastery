# ResearchOps — Python Mastery Through a Real Project

> **Build a research paper processing platform. Master Python. Build a portfolio.**

---

## What is this?

**ResearchOps** is simultaneously:

1. **A production-style Python project** — a research paper processing and experiment-tracking platform that ingests PDFs, extracts text, runs ML classifiers, generates embeddings, performs semantic search, exposes a REST API, and supports a RAG assistant.

2. **A 20-week Python mastery curriculum** — every week adds a real feature to the project while teaching a specific set of Python and software engineering concepts through notes, exercises, tests, and deliberate failure experiments.

---

## Who is this for?

You are a **computer science student** aiming for a career in **AI engineering** and **ML research**. You already know the basics of Python but want to master clean architecture, professional CLI and API development, ML engineering, embeddings, semantic search, RAG, testing, CI/CD, and Docker.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Raj-Indra-Asura/researchops_python_mastery.git
cd researchops_python_mastery

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install (development mode)
pip install -e ".[dev]"

# 4. Verify installation
researchops --help

# 5. Scan a directory for PDFs (Week 1 deliverable)
researchops scan ./examples/sample_papers

# 6. Run tests
pytest
```

---

## Current Status

| Week | Topic | Status |
|------|-------|--------|
| 1 | Python foundations, repo setup, `scan` command | ✅ Done |
| 2–20 | See [ROADMAP.md](ROADMAP.md) | 🔜 Upcoming |

---

## 20-Week Learning Journey Overview

### Month 1 — Python Core and Project Foundation
| Week | Focus |
|------|-------|
| 1 | Python foundations, repo setup, CLI scaffold |
| 2 | Files, pathlib, exceptions, logging |
| 3 | OOP, dataclasses, domain modeling |
| 4 | CLI packaging, entry points |

### Month 2 — Storage, Search, Multiprocessing
| Week | Focus |
|------|-------|
| 5 | SQLite storage layer |
| 6 | PDF parsing pipeline |
| 7 | Keyword search and data quality |
| 8 | Multiprocessing ingestion |

### Month 3 — Advanced Python and ML Engineering
| Week | Focus |
|------|-------|
| 9 | Protocols, interfaces, clean architecture |
| 10 | Testing discipline and quality gates |
| 11 | Classical ML topic classification |
| 12 | Experiment tracking |

### Month 4 — AI Engineering, API, Async, Workers
| Week | Focus |
|------|-------|
| 13 | Embeddings and semantic search |
| 14 | FastAPI layer |
| 15 | Async I/O network fetching |
| 16 | Local worker and job system |

### Month 5 — RAG, Production, Portfolio
| Week | Focus |
|------|-------|
| 17 | RAG assistant |
| 18 | Docker and environment configuration |
| 19 | Documentation and portfolio polish |
| 20 | Final hardening and v1.0 release |

---

## Repository Map

```
researchops_python_mastery/
├── README.md              ← You are here
├── ROADMAP.md             ← 20-week milestone map
├── SYLLABUS.md            ← Learning objectives per week
├── PROJECT_SPEC.md        ← Full feature specification
├── ARCHITECTURE.md        ← Design decisions and module boundaries
├── CONTRIBUTING.md        ← How to contribute / self-study conventions
├── CHANGELOG.md           ← Version history
├── pyproject.toml         ← Project config, dependencies, entry points
│
├── .github/
│   ├── copilot-instructions.md   ← AI assistant rules
│   └── workflows/ci.yml          ← Lint + test on every push
│
├── curriculum/            ← 20 weeks × 6 files each
│   ├── month-01-python-core/
│   │   ├── week-01-foundations/
│   │   │   ├── README.md      ← Week overview, objectives, deliverables
│   │   │   ├── notes.md       ← Concept explanations with examples
│   │   │   ├── exercises.md   ← Warm-up, project, stretch exercises
│   │   │   ├── break_it.md    ← Intentional failure experiments
│   │   │   ├── validation.md  ← Exact commands and expected outputs
│   │   │   └── reflection.md  ← Template for your weekly journal
│   │   └── week-02 … week-04/
│   └── month-02 … month-05/
│
├── src/
│   └── researchops/       ← Core package
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fakes/
│
├── examples/
├── scripts/
└── docs/
```

---

## How to Use the Curriculum

1. **Start at Week 1.** Don't skip weeks.
2. **Each week has 6 files:** README, notes, exercises, break_it, validation, reflection.
3. **Read `notes.md` first**, then do `exercises.md`, then implement, then `validation.md`.
4. **Fill in `reflection.md` every week.** If you can't explain what you built, you haven't learned it.
5. **Commit your work every day**, even if it's broken.

---

## How to Run Tests

```bash
pytest                                        # all tests
pytest tests/unit/ -v                        # unit tests only
pytest --cov=researchops --cov-report=term   # with coverage
```

---

## ⚠️ Warning: Do Not Skip Weeks

The architecture decisions made in Week 3 determine what's possible in Week 13. The test habits built in Week 10 prevent the bugs you'll encounter in Week 17. Mastery is built linearly. Trust the process.

---

## License

MIT
