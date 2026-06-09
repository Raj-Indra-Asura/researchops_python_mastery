# ADR-0002: Multiprocessing for CPU Work, Asyncio for I/O Waiting

- **Status:** Accepted
- **Date:** Week 8
- **Source:** Expands ADR-003 in [`adr-log.md`](./adr-log.md)

> Beginner note: this ADR is about *concurrency* — doing more than one thing at
> a time. Python gives you several ways to do it, and picking the wrong one
> makes code slower, not faster. The whole decision rests on one distinction:
> **is the work waiting, or is the work computing?**

## Decision title

Use **multiprocessing** (`concurrent.futures.ProcessPoolExecutor`) for CPU-bound
work such as PDF parsing, and reserve **asyncio** for I/O-bound work such as
network fetching and serving API requests.

## Context

Concurrency in Python is shaped by the **GIL** (Global Interpreter Lock — a lock
that lets only one thread run Python bytecode at a time inside a single
process). This single fact decides everything below.

There are three common tools:

- **Threads (`ThreadPoolExecutor`):** multiple threads in one process. Because
  of the GIL, only one runs Python code at a time. Great for waiting on I/O,
  useless for speeding up pure computation.
- **Processes (`ProcessPoolExecutor`):** multiple OS processes, each with its
  own Python interpreter and its own GIL. True parallel CPU use across cores.
  Cost: data must be *pickled* (serialised) to cross the process boundary.
- **Asyncio:** a single thread running an *event loop* that interleaves many
  tasks while they wait. Excellent for thousands of concurrent waits, but it
  runs Python on one core — it does **not** speed up computation.

ResearchOps has both kinds of work:

- **CPU-bound:** parsing PDFs, computing embeddings, training ML models. These
  *burn CPU*; the bottleneck is the processor.
- **I/O-bound:** downloading paper metadata/files, serving HTTP. These *wait*;
  the bottleneck is the network.

## CPU-bound vs I/O-bound

This is the heart of the decision.

| Question | CPU-bound | I/O-bound |
|---|---|---|
| What is the program doing? | Computing (parsing, math) | Waiting (network, disk) |
| What is the bottleneck? | The CPU core | The remote service / device |
| Does adding threads help? | No (GIL serialises Python) | Yes (waiting overlaps) |
| Right tool | **Processes** | **Asyncio** (or threads) |

A quick test: if you unplug the network, does the task get faster? If it does
nothing without the network, it is I/O-bound. If it would happily run at 100% CPU
on an island with no network, it is CPU-bound.

## Decision

- **PDF parsing → `ProcessPoolExecutor`.** Parsing is CPU-bound; processes give
  real multi-core parallelism that threads cannot.
- **Network fetching and API I/O → `asyncio`** (e.g. `httpx.AsyncClient`,
  FastAPI). Waiting overlaps cheaply on the event loop.
- **CPU-heavy work stays off the event loop.** PDF parsing, embedding
  computation, and ML training must never run directly inside an async
  coroutine.

## Why PDF parsing uses multiprocessing / `ProcessPoolExecutor`

- Parsing a PDF is pure computation; with threads the GIL would serialise it and
  a 4-core machine would parse at 1-core speed.
- `ProcessPoolExecutor` spreads parse jobs across cores, so ingesting a folder of
  papers scales roughly with core count.
- The price is the *pickle boundary*: arguments and return values must be
  picklable. We pass simple data (file paths, parsed-text dataclasses), not open
  database connections or file handles.

## Why async is reserved for network fetching and API I/O

- Fetching dozens of URLs is mostly *waiting*. One event-loop thread can have
  many requests in flight at once, finishing far faster than sequential fetches —
  without spawning processes.
- FastAPI is async-native: an async handler can serve other requests while one is
  waiting on a downstream call.
- Async adds **no** speed to computation, so we use it only where the work is
  waiting.

## Why CPU-heavy work must not run inside the event loop

The event loop is **cooperative**: a coroutine keeps the single loop thread until
it hits an `await`. CPU-heavy code (a 2-second PDF parse, an embedding batch, a
training loop) has no `await` in its hot path, so it **blocks the whole loop**.
Every other request and fetch freezes until it finishes. The application appears
to hang under load.

Correct pattern: keep the loop for waiting, and **offload** CPU work to a process
pool (e.g. `loop.run_in_executor(process_pool, parse_pdf, path)`), so the loop
stays responsive while cores do the heavy lifting.

## Consequences

**Positive**

- Each workload uses the model that actually makes it faster.
- Parsing scales with cores; fetching scales with concurrency; the API stays
  responsive.
- Clear rule for reviewers: *CPU → process pool, waiting → async, never mix.*

**Negative / costs**

- Process pools add overhead: process startup and pickling. Worth it for heavy
  parsing, wasteful for tiny tasks.
- Async code is a different mental model (coroutines, `await`, cancellation) and
  is easy to get subtly wrong.
- Accidentally calling blocking CPU code from a coroutine is a real, recurring
  bug; it must be guarded by review and tests.

## Alternatives considered

1. **Threads for everything.** Rejected: the GIL means threads cannot speed up
   CPU-bound parsing. Threads remain a fine fallback for simple blocking I/O.
2. **Asyncio for everything, including parsing.** Rejected: parsing has no
   `await` points and would block the event loop, hurting throughput.
3. **An external task queue (Celery/RQ) from the start.** Rejected as premature
   infrastructure for a learning project; a local `ProcessPoolExecutor` plus a
   simple job system (Week 16) teaches the concepts without the operational
   weight.

## Related curriculum weeks

- **Week 8 — Multiprocessing Ingestion:** introduces `ProcessPoolExecutor` for
  parallel PDF parsing and the picklability constraint.
- **Week 13 — Embeddings & Semantic Search:** embedding computation is CPU-bound
  and must be kept off the event loop, reinforcing this ADR.
- **Week 15 — Async I/O & Network Fetching:** introduces `asyncio`/`httpx` for
  concurrent fetching — async is for waiting, not computing.
- **Week 16 — Local Worker & Job System:** combines the two worlds, offloading
  long CPU jobs so request/response paths stay responsive.
