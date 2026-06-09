# ResearchOps — 20-Week Roadmap

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](README.md) › **🗺️ Roadmap** › [📚 Syllabus](SYLLABUS.md)
>
> 📘 Part of the ResearchOps book-like learning platform. Front door: [root README](README.md) · Begin: [Week 1](curriculum/month-01-python-core/week-01-foundations/README.md).
<!-- NAV:TOP:END -->

This document tracks the project milestone for each week. Update the status column as you complete each week.

## Status Key

- 🔜 Not started
- 🚧 In progress
- ✅ Complete
- ⏭️ Skipped (document why)

---

## Month 1 — Python Core and Project Foundation

| Week | Title | Milestone | Status |
|------|-------|-----------|--------|
| 1 | Python Foundations | `researchops scan ./papers` works; tests pass | ✅ |
| 2 | Files, Errors, Logging | PDF discovery with custom exceptions and structured logging | 🔜 |
| 3 | OOP and Domain Modeling | All core models defined and tested | 🔜 |
| 4 | CLI and Packaging | `pip install -e .` produces a working `researchops` command | 🔜 |

## Month 2 — Storage, Search, Multiprocessing

| Week | Title | Milestone | Status |
|------|-------|-----------|--------|
| 5 | SQLite Storage Layer | Papers persist and retrieve from SQLite | 🔜 |
| 6 | PDF Parsing Pipeline | `researchops ingest ./papers` extracts and stores text | 🔜 |
| 7 | Keyword Search + Data Quality | `researchops search "query"` returns ranked results | 🔜 |
| 8 | Multiprocessing Ingestion | `--workers 4` parallelises ingestion | 🔜 |

## Month 3 — Advanced Python and ML Engineering

| Week | Title | Milestone | Status |
|------|-------|-----------|--------|
| 9 | Protocols and Clean Architecture | Services depend on protocols; fake repos in tests | 🔜 |
| 10 | Testing Discipline and CI | 70%+ coverage; CI passes on every push | 🔜 |
| 11 | Classical ML: Topic Classification | `researchops classify PAPER_ID` returns a topic | 🔜 |
| 12 | Experiment Tracking | `researchops experiment list` shows run history | 🔜 |

## Month 4 — AI Engineering, API, Async, Workers

| Week | Title | Milestone | Status |
|------|-------|-----------|--------|
| 13 | Embeddings and Semantic Search | `researchops semantic-search "query"` uses cosine similarity | 🔜 |
| 14 | FastAPI Layer | `GET /papers` and `GET /papers/search?q=` work | 🔜 |
| 15 | Async I/O Network Fetching | `researchops fetch-arxiv QUERY` downloads papers | 🔜 |
| 16 | Local Worker and Job System | `researchops jobs run` processes a background queue | 🔜 |

## Month 5 — RAG, Production, Portfolio

| Week | Title | Milestone | Status |
|------|-------|-----------|--------|
| 17 | RAG Assistant | `researchops ask "question"` returns cited answer | 🔜 |
| 18 | Docker | `docker-compose up` starts the full stack | 🔜 |
| 19 | Documentation and Portfolio Polish | README, diagrams, demo script complete | 🔜 |
| 20 | Final Hardening and v1.0 Release | CI green, `v1.0.0` tag, changelog, demo ready | 🔜 |

---

## Final Vision: What v1.0 Can Do

```bash
researchops ingest ./papers --workers 4
researchops search "transformer attention"
researchops semantic-search "efficient transformers"
researchops train-topic-model
researchops classify paper_id_here
researchops ask "What are the main approaches to efficient attention?"
uvicorn researchops.api.main:app --reload
docker-compose up
```
