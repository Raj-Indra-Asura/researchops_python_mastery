# ResearchOps — Project Specification

## Goal

Build ResearchOps: a Python-based research paper processing and experiment-tracking platform.

## Core capabilities (by v1.0)

1. **PDF Ingestion** — scan a directory, extract text + metadata, store in SQLite
2. **Keyword Search** — search stored papers by keyword with basic ranking
3. **Failure Tracking** — record and display documents that failed to ingest
4. **Parallel Processing** — use multiprocessing for CPU-bound PDF parsing
5. **ML Classification** — train a TF-IDF topic classifier on stored papers
6. **Experiment Tracking** — log params and metrics for every training run
7. **Semantic Search** — generate embeddings and search by vector similarity
8. **REST API** — expose all features over HTTP with FastAPI
9. **Async Fetching** — download papers from URLs and arXiv asynchronously
10. **Background Jobs** — offload expensive tasks to a persistent job queue
11. **RAG Assistant** — answer questions over the paper library with citations
12. **Docker** — run the complete stack with `docker-compose up`
13. **CI/CD** — lint and test on every push

## CLI command reference (final state)

```bash
# Discovery
researchops scan PATH [--recursive]

# Ingestion
researchops ingest PATH [--workers N] [--recursive]

# Papers
researchops papers list
researchops papers show PAPER_ID
researchops papers stats
researchops papers failed

# Search
researchops search QUERY [--limit N]
researchops semantic-search QUERY [--limit N]

# ML
researchops train-topic-model
researchops classify PAPER_ID
researchops topics

# Experiments
researchops experiment create NAME
researchops experiment log-param RUN_ID KEY VALUE
researchops experiment log-metric RUN_ID KEY VALUE
researchops experiment list
researchops experiment compare

# Network
researchops fetch-url URL
researchops fetch-arxiv QUERY

# Jobs
researchops jobs list
researchops jobs run
researchops jobs retry JOB_ID

# RAG
researchops ask QUESTION
```

## API endpoint reference (Week 14+)

```
GET  /health
GET  /papers
GET  /papers/{id}
GET  /papers/search?q=QUERY
POST /papers/ingest
GET  /experiments
GET  /experiments/{id}
POST /search/semantic
```

## Non-goals

- Multi-user / authentication (keep it single-user local)
- Cloud storage (SQLite + local filesystem only in v1.0)
- Real-time collaborative features
- Mobile/web UI (CLI + REST API only)
