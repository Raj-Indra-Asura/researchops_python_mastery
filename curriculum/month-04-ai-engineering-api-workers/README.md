# Month 4 — AI Engineering: APIs, Async, and Workers

> **Book section 4 of 5.** This month the engineered ML system becomes an **AI
> engineering platform.** You add semantic understanding, expose the system over
> HTTP, fetch data concurrently, and run long jobs in the background.

---

## The big idea of the month

A topic classifier is useful, but modern AI engineering is built on
**retrieval**: representing text as **embeddings** (vectors) so you can find
*semantically* relevant content, not just keyword matches. This month you add
embeddings and semantic search, then learn to *serve* the system (FastAPI), *feed*
it data concurrently (async network fetching), and *run long work* without
blocking (a job system).

The theme: **retrieval comes before generation.** Before any RAG assistant
(Month 5) can answer a question, it must reliably find the right context. You
build that retrieval backbone — and the platform that serves it — now.

## What you already know before this month

From Months 1–3 you can:

- Build clean, layered, well-tested Python applications behind a CLI.
- Persist and search data, parse PDFs, and parallelise CPU work.
- Train, evaluate, save, and track a classical ML model.
- Apply protocols and dependency inversion so new adapters slot in cleanly.

You do **not** need prior experience with embeddings, web frameworks, async, or
queues.

## What you will learn this month

- **Embeddings** — turning text into vectors that capture meaning.
- **Semantic search** — ranking by vector (cosine) similarity, not keywords.
- **Chunking** — splitting documents into retrievable pieces with source
  metadata.
- **FastAPI** — exposing services as validated HTTP endpoints.
- **HTTP basics** — methods, status codes, request/response models.
- **Async network fetching** — `asyncio` + `httpx` for concurrent I/O with
  timeouts, retries, and bounded concurrency.
- **Worker / job systems** — running long tasks in the background with explicit
  states, retries, and idempotency.
- **Why retrieval comes before RAG** — generation is only as good as the context
  it is given.

## What ResearchOps capability will exist by the end

The ability to **expose services over HTTP, retrieve semantically relevant
context, fetch data asynchronously, and run long tasks as jobs**:

```bash
researchops semantic-search "transfer learning for low-resource languages"
uvicorn researchops.api.main:app --reload    # serve the platform over HTTP
researchops fetch <urls...>                   # concurrent async fetching
```

Plus a local job system that queues and runs background work safely.

## Week-by-week chapter flow

| Week | Chapter | What it adds |
|---|---|---|
| **Week 13 — Embeddings & Semantic Search** | "Meaning, not just words" | Chunking, an embedder interface, vector indexing, cosine ranking. |
| **Week 14 — FastAPI Layer** | "Opening the doors" | A thin HTTP transport over existing services, with schemas. |
| **Week 15 — Async I/O & Network Fetching** | "Waiting efficiently" | `asyncio`/`httpx` concurrent fetching with retries and timeouts. |
| **Week 16 — Local Worker & Job System** | "Work that outlives a request" | Job states, retries, idempotency, a worker loop. |

## How each week connects to the previous week

- **Week 13 → 14:** once semantic retrieval works locally, Week 14 *exposes* it
  (and other services) over HTTP — the API is a thin door onto proven logic
  (see [ADR-0003](../../docs/decisions/0003-cli-before-api.md)).
- **Week 14 → 15:** an API often needs to *pull in* external data; Week 15 adds
  async fetching so the platform can gather many sources concurrently without
  blocking.
- **Week 15 → 16:** some work (bulk ingest, embedding a large corpus, many
  fetches) is too long for a single request; Week 16 moves it into a background
  job system with states and retries.

## What not to skip

- **Source metadata on every chunk (Week 13).** Without it, Month 5's citations
  are impossible. A chunk must always know where it came from.
- **Keeping route handlers thin (Week 14).** Handlers parse, call a service, and
  return — no business logic in the route.
- **Keeping CPU work off the event loop (Week 15).** Async is for *waiting*;
  parsing and embedding are CPU-bound and must not block the loop
  (see [ADR-0002](../../docs/decisions/0002-multiprocessing-vs-asyncio.md)).
- **Idempotency thinking (Week 16).** A retried job must not double-apply its
  effects.

## What concepts must be understood before moving on

Be able to explain aloud:

- What an embedding is and why cosine similarity ranks by meaning.
- Why documents are chunked, and why each chunk carries source metadata.
- The difference between keyword and semantic search, and when each wins.
- Why an API route should contain no business logic.
- The difference between **I/O-bound** (async) and **CPU-bound** (processes)
  work, and why mixing them on the event loop is a bug.
- Job states (queued → running → succeeded/failed), retries, and idempotency.
- Why retrieval must be solid *before* attempting RAG.

## Month-end self-assessment

Rate yourself 1–10 with evidence:

- [ ] I can chunk a document and attach source metadata to each chunk.
- [ ] I can rank results by cosine similarity and explain the math at a practical
      level.
- [ ] I can compare keyword vs semantic results and say which fits a query.
- [ ] I can add a FastAPI endpoint that calls a service and stays thin.
- [ ] I can fetch many URLs concurrently with timeouts and bounded retries.
- [ ] I can explain why PDF parsing must not run inside async code.
- [ ] I can model a job's state machine and make a handler idempotent.
- [ ] I can recover from a failed job without losing the error.

## Month-end mini capstone

Stand up the platform end to end:

1. Build a small semantic index from the sample papers and run a semantic query
   that returns chunks **with** their source documents.
2. Serve `semantic-search` (and a `/health` route) via FastAPI; hit it with an
   HTTP client and get validated JSON back.
3. Fetch several URLs concurrently with a timeout and a bounded retry policy;
   show that one failure does not erase the other successes.
4. Submit a long ingest/embedding task to the job system; show it moves through
   its states and is safe to retry.

Done when each layer calls the *same* services, tests pass, and `ruff` is clean.

## Bridge to Month 5

You can now retrieve relevant context and expose services over HTTP — the two
ingredients a RAG assistant needs. Month 5 finishes the story: **RAG** with
**citations** and **hallucination control**, a **fake generator** for tests plus
**optional real providers**, **Docker** and **environment config**, polished
**documentation** and **demo**, and a disciplined **release**. The platform
becomes a credible **portfolio** project.

## Warning signs you are not ready to move on

- Semantic search "works" only because of hardcoded or fake data.
- Chunks do not record their source document (citations will be impossible).
- A route handler contains business logic or talks straight to SQLite.
- CPU-bound parsing/embedding runs inside an async coroutine.
- A retried job double-applies effects, or a failed job's error is discarded.

## Suggested weekly study rhythm

~9–11 hours/week:

- **Read** week README + notes (~1–1.5 hrs).
- **Build** in small commits (~5–6 hrs) — new paradigms (vectors, async) need
  hands-on repetition.
- **Break it** with `break_it.md` (~1 hr) — block the event loop on purpose, kill
  a fetch mid-flight.
- **Test** including failure paths (~1.5–2 hrs).
- **Reflect** in `reflection.md` and the weekly report (~30–45 min).

## Suggested Git milestone at end of month

```bash
git add .
git commit -m "Month 4 complete: semantic search, FastAPI, async fetching, job system"
git tag month-4-complete
```

Your repo should now retrieve semantically, serve over HTTP, fetch
concurrently, and run background jobs — all tested and lint-clean.
