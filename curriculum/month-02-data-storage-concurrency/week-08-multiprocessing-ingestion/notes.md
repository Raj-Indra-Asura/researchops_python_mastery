<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 08 — Multiprocessing Ingestion:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 08 Notes — Multiprocessing Ingestion

## 1. Chapter overview

Week 8 is the chapter where ResearchOps learns to ingest a directory of research papers faster without making the ingestion result less trustworthy.
The milestone is `researchops ingest ./papers --workers 4`: the same ingestion pipeline from earlier weeks can now parse more than one PDF at a time by using worker processes.
This is not a generic speed chapter. It is specifically about CPU-bound PDF parsing, process pools, picklability, worker failures, and safe parent-process database writes.
The important phrase is **doing many things at once, safely**.
A faster command is a regression if it drops papers, hides failures, corrupts SQLite state, or produces different records from the single-worker path.

Use this chapter as a single unified path:
- Read the mental model before the implementation details.
- Understand why PDF parsing is CPU-bound before choosing a tool.
- Learn why Python threads are not the right tool for this CPU-heavy parse stage.
- Treat `ProcessPoolExecutor` as a carefully bounded parser fan-out tool, not as permission to parallelize every line of ingestion.
- Keep workers simple: receive a path, parse one PDF, return a success or failure payload.
- Keep the parent process responsible for skip checks, saving papers, recording failures, and final summaries.
- Validate with the real Week 8 command and the real Week 8 test file from the syllabus.

By the end of the chapter, you should be able to explain the GIL, the reason worker functions must be module-level, the meaning of picklability, the parent-write pattern, and the test evidence that proves parallel ingestion is still correct.

## 2. What you already know from previous weeks

ResearchOps is not starting from nothing this week.
Week 1 gave you the project layout, first CLI command, test discovery, and the habit of validating behavior from the command line.
Week 2 taught file handling, custom exceptions, and logging, which matters because a parallel ingestion batch must make failures visible instead of hiding them inside a worker.
Week 3 named the domain objects: `Paper`, `ParsedDocument`, `IngestionResult`, and `FailedDocument` are part of the language of the system.
Week 4 made the CLI installable and testable, so `researchops ingest` is a real user-facing command rather than a one-off script.
Week 5 introduced SQLite and repository boundaries, which is why storage decisions should stay controlled in one place.
Week 6 built the PDF parsing pipeline and taught that one bad file should be recorded, not ignored.
Week 7 added search and data-quality thinking, which makes ingestion quality even more important because search can only be as trustworthy as the stored text.

Before learning multiprocessing, you should be able to trace the single-worker ingestion path:
- A directory path enters from the CLI.
- The service discovers PDF paths.
- The service skips already-known papers when skip behavior is enabled.
- One PDF is parsed into document data or a parse failure.
- A successful parse becomes a `Paper` record.
- A failed parse becomes a `FailedDocument` record.
- The final `IngestionResult` reports successes, failures, and skipped files.

If that older path is unclear, multiprocessing will feel random. Parallelism should speed up a known workflow, not hide a workflow you do not understand.

## 3. What problem this week solves

Sequential ingestion is correct but slow for large paper folders.
If every PDF takes even a few seconds to parse, a few hundred PDFs can turn into a long wait.
Each PDF is mostly independent during parsing: parsing `paper_a.pdf` does not require the text from `paper_b.pdf`.
That independence is the opportunity for worker processes.

The hard part is that not every stage is equally safe to parallelize.
Parsing can be distributed because each worker can operate on one file path and return plain data.
Saving to SQLite should remain coordinated because persistent state, duplicate checks, and failure recording are easier to reason about from the parent process.
So the problem is not "make ingestion parallel everywhere."
The real problem is: **parallelize CPU-heavy parsing while preserving the exact storage and failure semantics of the original ingestion workflow.**

This week closes these gaps:
- The CLI needs a `--workers` option.
- The ingestion service needs to accept and use a worker count.
- A process-pool helper needs to run parse work in child processes.
- The worker function must be module-level so child processes can import it.
- Worker inputs and outputs must be picklable.
- One bad PDF must return a failure payload instead of crashing the whole batch.
- The parent process must save successes and record failures after parsing payloads return.
- Tests must prove single-worker and multi-worker paths agree logically.

## 4. Beginner mental model

Think of the parent process as a library desk and worker processes as assistants.
The desk owns the catalog. The assistants do not edit the catalog.
The desk hands each assistant a card containing one PDF path.
An assistant opens that PDF, extracts what it can, and returns a report card.
If the assistant cannot parse the PDF, it returns a failure report card rather than stopping all other assistants.
The desk reads the returned report cards and updates the catalog in one controlled place.

This model gives you four simple questions:
- What crosses from the parent to a worker? A simple PDF path string.
- What happens inside a worker? CPU-heavy parsing for one PDF.
- What crosses back to the parent? A simple success or failure payload.
- Who writes to SQLite? The parent process only.

A process boundary is like a doorway that only plain, packed data can pass through.
A string fits through. A dictionary of strings and numbers fits through. An open database connection does not fit through. A nested function does not fit through because the child process cannot import it by a stable module-level name.

## 5. Core vocabulary

| Term | Beginner meaning | Why it matters in Week 8 |
|---|---|---|
| CPU-bound work | Work limited mostly by calculation speed. | PDF parsing spends time decoding and reconstructing document content. |
| I/O-bound work | Work limited mostly by waiting for disk, network, or another external resource. | Waiting-friendly techniques are not the main solution for CPU-heavy parsing. |
| Concurrency | Multiple tasks are in progress during the same period. | A program can be concurrent without using multiple CPU cores at the same instant. |
| Parallelism | Multiple tasks execute at the same instant. | ResearchOps wants different PDFs parsed on different CPU cores. |
| GIL | The Global Interpreter Lock in CPython. | It explains why Python threads do not speed up this CPU-heavy parse stage. |
| Process | A running program with its own memory space. | Each worker process has its own Python interpreter state. |
| Thread | A unit of execution inside one process that shares memory with other threads. | Threads are not the Week 8 tool for CPU-heavy parsing. |
| ProcessPoolExecutor | Standard-library helper for running function calls in worker processes. | It is the main Week 8 implementation tool. |
| Worker function | Function executed in a child process. | It should parse one PDF and return plain data. |
| Module-level function | Function defined at the top level of a Python module. | Child processes can import it by name. |
| Pickling | Python serialization for sending values between processes. | Worker arguments and results must be picklable. |
| Picklable value | A value that can be serialized and rebuilt. | Strings, ints, lists, dicts, and simple data shapes are safe choices. |
| Unpicklable value | A value tied to live state or a local definition. | Open connections, open files, lambdas, and nested functions cause failures. |
| Failure isolation | Keeping one bad item from destroying the whole batch. | One corrupt PDF should become one recorded failure. |
| Batch write | Saving collected parse results from the parent process. | It protects SQLite and keeps storage rules centralized. |
| Worker count | Number of child processes allowed to run work. | `--workers 2` asks for two parser workers. |
| Startup overhead | Cost of creating worker processes and moving data. | Tiny folders may not speed up with more workers. |
| Parity test | Test proving two paths produce the same logical result. | Single-worker and multi-worker ingestion must agree. |

## 6. Concept explanations from first principles

This section contains the detailed teaching for the chapter. Read it slowly: it moves from correctness, to workload type, to the GIL, to processes, to pickling, to safe ResearchOps ingestion.


### Deep dive: Chapter overview

You now have a complete local research library.
ResearchOps can scan directories, parse PDFs, store papers, and search them.

There is one remaining engineering problem: performance.

If you have 500 PDFs, the current sequential implementation processes them one at a time.
PDF parsing is CPU-intensive.
It can take several seconds per file.
Five hundred files might take 20-30 minutes.

This week you learn to process multiple PDFs simultaneously using **multiprocessing**.

But performance comes last.
You learn the "why performance matters only after correctness" principle, then the theory (concurrency vs parallelism, CPU-bound vs I/O-bound), then the tools (`ProcessPoolExecutor`), then the safe patterns for a database-backed system.

By the end of this week, ResearchOps will support a `--workers` flag that can multiply throughput by the number of CPU cores.

---

### Deep dive: Correctness before speed

A cardinal rule in software engineering: **make it work, then make it fast**.

This is not just a stylism.
It reflects a practical reality.

A slow but correct program can be improved.
A fast but incorrect program corrupts data, drops failures silently, writes duplicates, or produces wrong results.
Speeding up an incorrect program makes the incorrectness harder to observe.

The sequential ingestion from Week 6 is correct.
Every paper is processed.
Every failure is recorded.
The order is predictable.
Tests cover all edge cases.

Multiprocessing adds complexity:
- Worker processes can crash independently.
- Results arrive in unpredictable order.
- Shared state (the database) requires careful coordination.
- Serialization errors can appear that never existed in single-process code.

All of this is manageable — but you must start from a correct foundation.
If your single-process code had bugs, multiprocessing would amplify them.

---

### Deep dive: Concurrency vs parallelism

These terms are often used interchangeably but mean different things.

**Concurrency** means: multiple tasks are in progress at the same time.
They may not literally be executing at the same instant.
The system switches between them.

Imagine a chef cooking multiple dishes.
While the pasta boils (waiting), the chef chops vegetables (working).
Both dishes are in progress simultaneously, but the chef is doing only one thing at each instant.
This is concurrency.

**Parallelism** means: multiple tasks are literally executing at the same instant.
This requires multiple CPUs or CPU cores.

Imagine two chefs in the same kitchen, each working on a different dish simultaneously.
Both dishes are being actively worked on at the same instant.
This is parallelism.

For software:
- **Concurrency** is about dealing with many tasks. It is a design property.
- **Parallelism** is about doing many tasks at once. It is an execution property.

Python's `waiting-oriented concurrency` provides concurrency (many tasks in progress, but only one runs at a time in the event loop).
Python's `multiprocessing` provides parallelism (multiple processes, each on a separate CPU core).

---

### Deep dive: CPU-bound vs I/O-bound

Performance problems fall into two categories:

**I/O-bound**: the program spends most of its time waiting for external operations.
- Waiting for a network response.
- Waiting for a database query to return.
- Waiting for a file to be read from disk.

For I/O-bound work, `waiting-oriented concurrency` or threading is often effective.
While one task waits for a response, another task can run.

**CPU-bound**: the program spends most of its time computing.
- PDF text extraction (parsing font tables, reconstructing character positions).
- Large numerical processing.
- Image processing.
- Compression/decompression.
- Hashing large files.

For CPU-bound work, `waiting-oriented concurrency` is not useful because the event loop cannot run other tasks while Python is executing code.
Threading is also mostly unhelpful due to the Global Interpreter Lock (covered next).

**PDF parsing is CPU-bound.**

The `pypdf` library reads the binary PDF structure, decodes character tables, and reconstructs the text.
This is mostly computation, not waiting.
Each core can independently parse a different PDF.
Multiprocessing is the right tool.

---

### Deep dive: The Global Interpreter Lock (GIL)

This is one of the most important Python-specific concepts for performance.

CPython (the standard Python interpreter) has a **Global Interpreter Lock (GIL)**.
The GIL is a mutex (mutual exclusion lock) that only allows one thread to execute Python bytecode at a time.

### Why the GIL exists

Python manages memory with reference counting.
Each object tracks how many references point to it.
When the count drops to 0, the object is deallocated.

Reference counting with multiple threads is not safe without coordination.
Two threads could simultaneously increment or decrement a reference count, corrupting memory.
The GIL prevents this by ensuring only one thread runs Python code at a time.

### What the GIL means for threads

Python threads do NOT run in parallel for CPU-bound work.

```python
import threading

def cpu_work():
    total = 0
    for i in range(10_000_000):
        total += i

# This does NOT run twice as fast as one thread
t1 = threading.Thread(target=cpu_work)
t2 = threading.Thread(target=cpu_work)
t1.start()
t2.start()
t1.join()
t2.join()
```

Both threads compete for the GIL.
While `t1` runs, `t2` waits.
While `t2` runs, `t1` waits.
On a wall-clock basis, this is no faster than one thread — and slightly slower due to context switching.

### What the GIL does NOT affect

The GIL is released during I/O operations.
When a thread is waiting for a disk read or network response, it releases the GIL so other threads can run Python code.
This is why threading is effective for I/O-bound work.

The GIL is also released during many C extension operations.
`numpy` releases the GIL during computation.
`pypdf`'s C extensions may release it during some operations.
But for pure-Python PDF parsing, the GIL applies.

### Multiprocessing bypasses the GIL

Each Python process has its own GIL.
Multiple processes run truly in parallel on separate CPU cores.
There is no shared GIL between processes.

This is why multiprocessing is the correct solution for CPU-bound work like PDF parsing.

---

### Deep dive: Process vs Thread

| Property              | Thread                          | Process                         |
|-----------------------|---------------------------------|---------------------------------|
| Memory                | Shared with parent              | Separate (copy-on-write)        |
| GIL                   | Constrained by parent's GIL     | Independent GIL                 |
| Parallelism           | Not for CPU-bound (GIL)         | Yes, for CPU-bound               |
| Communication         | Shared variables (needs locking)| Serialized messages (pickling)  |
| Startup cost          | Low                             | Higher                          |
| Database connections  | Can share (carefully)           | Must create per-process          |
| Use case              | I/O-bound tasks                 | CPU-bound tasks                  |

---

### Deep dive: ProcessPoolExecutor

`ProcessPoolExecutor` from the `concurrent.futures` module provides a high-level interface for process-based parallelism.

```python
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


def parse_one_pdf(path_str: str) -> tuple[str, str]:
    """Worker function: parse one PDF and return (path, text)."""
    path = Path(path_str)
    from researchops.parsing.pdf_parser import parse_pdf
    doc = parse_pdf(path)
    return path_str, doc.raw_text


def parse_all_pdfs_parallel(pdf_paths: list[Path], max_workers: int = 4) -> list[tuple[str, str]]:
    """Parse PDFs in parallel. Returns list of (path_str, text) tuples."""
    path_strings = [str(p) for p in pdf_paths]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(parse_one_pdf, path_strings))

    return results
```

Let us read every line.

`from concurrent.futures import ProcessPoolExecutor` — Imports the executor class from the standard library.
No third-party dependencies needed.

`def parse_one_pdf(path_str: str) -> tuple[str, str]:` — This is the **worker function**.
It runs in a subprocess.
Everything it returns must be serializable.

`path = Path(path_str)` — The worker receives a string (not a Path) because strings are trivially serializable.
We reconstruct the Path inside the worker.

`from researchops.parsing.pdf_parser import parse_pdf` — The import happens inside the worker.
This is a common pattern: the worker imports what it needs locally rather than relying on everything being imported in the parent process.

`with ProcessPoolExecutor(max_workers=max_workers) as executor:` — Creates a pool of `max_workers` subprocess workers.
The `with` block ensures the pool is cleanly shut down when done.
The `executor` object manages the worker pool.

`results = list(executor.map(parse_one_pdf, path_strings))` — `executor.map` applies `parse_one_pdf` to each element of `path_strings`.
The work is distributed across the worker pool.
`list(...)` collects all results.
The results are returned **in the same order as the input list**.

When the `with` block exits, the executor waits for all workers to finish before continuing.

---

### Deep dive: Pickling: the serialization requirement

Worker functions and their arguments must be **picklable**.

**Pickling** is Python's serialization mechanism.
`pickle.dumps(obj)` converts an object to bytes.
`pickle.loads(bytes)` reconstructs the object.

`ProcessPoolExecutor` uses pickling to send arguments to workers and receive results.

Things that ARE picklable:
- Strings, integers, floats, booleans
- Lists, tuples, dictionaries (if their contents are picklable)
- Simple dataclasses
- Most standard library objects

Things that are NOT picklable:
- Open file handles
- Open database connections (`sqlite3.Connection`)
- Lambda functions
- Nested functions (functions defined inside other functions)
- Most objects with active system resources

### Why this matters for ResearchOps

The following would FAIL:

```python
# WRONG: passing a database connection to a worker
def parse_and_save(path_str: str, conn: sqlite3.Connection) -> None:
    doc = parse_pdf(Path(path_str))
    conn.execute("INSERT INTO ...")  # Can't pass conn to a worker!
```

The `sqlite3.Connection` object cannot be pickled.
The worker subprocess cannot receive it.

The following would also FAIL:

```python
# WRONG: using a lambda as the worker function
with ProcessPoolExecutor() as executor:
    results = executor.map(lambda path: parse_pdf(Path(path)), paths)
```

Lambda functions cannot be pickled.

The safe pattern: **workers only parse, the main process saves**.

---

### Deep dive: The safe architecture: parse in parallel, save sequentially

```text
Main process:
  1. Scan directory → list of PDF paths
  2. Submit all paths to ProcessPoolExecutor
  3. Collect ParsedDocument results from workers
  4. For each result:
     - Build Paper
     - Save to SQLite repository

Worker processes (multiple, in parallel):
  - Receive one path
  - Call parse_pdf(path)
  - Return ParsedDocument (or error)
  - Nothing else (no database, no logging to shared resources)
```

This architecture is safe because:

**Workers are pure functions.**
They receive a path string.
They return a `ParsedDocument` (or an indication of failure).
They have no shared state.

**The database is touched only from the main process.**
One process, one connection, sequential writes.
No concurrent write contention.
No WAL locking issues.

**Failures are isolated.**
If worker #3 crashes while parsing a corrupt PDF, it does not affect workers #1, #2, #4.
The main process catches the exception from that future and records a failure.

---

### Deep dive: Complete parallel ingestion implementation

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime
import uuid

from researchops.core.models import (
    FailedDocument, IngestionResult, Paper, PaperId
)
from researchops.core.interfaces import PaperRepository, FailureRepository
from researchops.parsing.metadata_extractor import extract_title, extract_author
from researchops.parsing.text_cleaner import clean_text
from researchops.utils.paths import find_pdfs


def _parse_worker(path_str: str) -> dict:
    """Run in a subprocess. Parse one PDF and return serializable result."""
    from researchops.parsing.pdf_parser import parse_pdf
    from researchops.core.exceptions import ParsingError, EmptyDocumentError
    path = Path(path_str)
    try:
        doc = parse_pdf(path)
        return {
            "ok": True,
            "path": path_str,
            "raw_text": doc.raw_text,
            "num_pages": doc.num_pages,
            "file_size_bytes": doc.file_size_bytes,
            "metadata": doc.metadata,
        }
    except Exception as exc:
        return {
            "ok": False,
            "path": path_str,
            "error_message": str(exc),
            "error_type": type(exc).__name__,
        }


class ParallelIngestionService:
    def __init__(
        self,
        paper_repo: PaperRepository,
        failure_repo: FailureRepository,
        max_workers: int = 1,
    ) -> None:
        self._paper_repo = paper_repo
        self._failure_repo = failure_repo
        self._max_workers = max_workers

    def ingest_directory(
        self,
        directory: Path,
        *,
        skip_existing: bool = True,
    ) -> IngestionResult:
        run_id = str(uuid.uuid4())[:8]
        result = IngestionResult(
            run_id=run_id,
            directory=directory,
            started_at=datetime.utcnow(),
        )

        pdfs = find_pdfs(directory)
        paths_to_process = []

        for pdf_path in pdfs:
            paper_id = str(PaperId.from_path(pdf_path))
            if skip_existing and self._paper_repo.exists(paper_id):
                result.skipped.append(pdf_path)
            else:
                paths_to_process.append(pdf_path)

        # Parallel parse stage
        raw_results = self._parse_parallel(paths_to_process)

        # Sequential save stage (main process only)
        for raw in raw_results:
            if raw["ok"]:
                self._save_parsed(raw, result)
            else:
                self._save_failure(raw, result)

        result.finished_at = datetime.utcnow()
        return result

    def _parse_parallel(self, paths: list[Path]) -> list[dict]:
        """Submit all paths to workers. Collect results in original order."""
        path_strings = [str(p) for p in paths]
        with ProcessPoolExecutor(max_workers=self._max_workers) as executor:
            return list(executor.map(_parse_worker, path_strings))

    def _save_parsed(self, raw: dict, result: IngestionResult) -> None:
        from researchops.core.models import ParsedDocument
        doc = ParsedDocument(
            source_path=Path(raw["path"]),
            raw_text=raw["raw_text"],
            num_pages=raw["num_pages"],
            file_size_bytes=raw["file_size_bytes"],
            metadata=raw["metadata"],
        )
        paper_id = str(PaperId.from_path(Path(raw["path"])))
        paper = Paper(
            id=paper_id,
            title=extract_title(doc),
            source_path=raw["path"],
            text=clean_text(doc.raw_text),
            num_pages=doc.num_pages,
            file_size_bytes=doc.file_size_bytes,
            author=extract_author(doc),
            abstract=None,
        )
        try:
            self._paper_repo.save(paper)
            result.successes.append(paper)
        except Exception:
            pass  # duplicate or other save error

    def _save_failure(self, raw: dict, result: IngestionResult) -> None:
        failure = FailedDocument(
            source_path=Path(raw["path"]),
            error_message=raw["error_message"],
            error_type=raw["error_type"],
        )
        self._failure_repo.record_failure(failure)
        result.failures.append(failure)
```

---

### Deep dive: The worker function in detail

```python
def _parse_worker(path_str: str) -> dict:
    from researchops.parsing.pdf_parser import parse_pdf
    from researchops.core.exceptions import ParsingError, EmptyDocumentError
    path = Path(path_str)
    try:
        doc = parse_pdf(path)
        return {
            "ok": True,
            "path": path_str,
            "raw_text": doc.raw_text,
            "num_pages": doc.num_pages,
            "file_size_bytes": doc.file_size_bytes,
            "metadata": doc.metadata,
        }
    except Exception as exc:
        return {
            "ok": False,
            "path": path_str,
            "error_message": str(exc),
            "error_type": type(exc).__name__,
        }
```

`def _parse_worker(path_str: str) -> dict:` — A top-level function.
It must be top-level (not a lambda, not a nested function, not a method) for pickling.

`from researchops.parsing.pdf_parser import parse_pdf` — Lazy import inside the worker.
When a new process starts, it runs a fresh Python interpreter.
Imports you rely on must be available.
Importing lazily inside the function makes the dependency explicit.

`return {...}` — Returns a plain dictionary.
A plain dict is trivially picklable.
An alternative would be to return a `ParsedDocument` dataclass — which is also picklable if it contains only simple types.

`except Exception as exc:` — Catches ALL exceptions inside the worker.
If the worker raises an uncaught exception, `executor.map` re-raises it in the main process when collecting results.
Catching it here and returning a failure-shaped dict is cleaner:
- The main process sees `raw["ok"] == False`.
- The error message is available for `FailedDocument` recording.
- The exception does not propagate and stop the entire batch.

---

### Deep dive: Result aggregation

`executor.map(f, items)` returns results in the same order as `items`.
If you submit 10 paths, you get 10 results in the same order.

An alternative is `executor.submit` with `as_completed`:

```python
from concurrent.futures import as_completed

futures = {executor.submit(_parse_worker, str(p)): p for p in paths}

for future in as_completed(futures):
    path = futures[future]
    try:
        result = future.result()
    except Exception as exc:
        # Worker raised an uncaught exception
        print(f"Worker failed for {path}: {exc}")
```

`as_completed(futures)` yields futures in the order they COMPLETE, not the order they were submitted.
If the first path is a slow 100-page PDF and the second is a 2-page paper, the second completes first.

Use `executor.map` when you want results in input order.
Use `as_completed` when you want to process results as soon as they arrive (for progress reporting or early stopping).

---

### Deep dive: Progress reporting

A batch of 500 PDFs should show progress, not silence.

With `executor.map`, progress is hard to show because results all arrive at the end.
With `as_completed`, you can update a progress counter after each completion:

```python
import sys

futures = {executor.submit(_parse_worker, str(p)): p for p in paths}
done = 0
total = len(futures)

for future in as_completed(futures):
    done += 1
    result = future.result()
    status = "ok" if result["ok"] else "FAILED"
    print(f"\r[{done}/{total}] {status}: {result['path']}", end="", flush=True)

print()  # newline after progress line
```

`"\r"` is a carriage return that moves the cursor to the beginning of the current line without advancing to a new line.
Combined with `end=""` and `flush=True`, this creates an in-place progress display.

---

### Deep dive: Benchmarking

Performance work requires measurement.
Do not assume multiprocessing is faster.
Measure it.

```python
import time
from pathlib import Path

pdf_paths = list(find_pdfs(Path("examples/sample_papers")))

# Sequential
start = time.perf_counter()
for path in pdf_paths:
    _parse_worker(str(path))
sequential_time = time.perf_counter() - start

# Parallel (4 workers)
start = time.perf_counter()
with ProcessPoolExecutor(max_workers=4) as executor:
    list(executor.map(_parse_worker, [str(p) for p in pdf_paths]))
parallel_time = time.perf_counter() - start

print(f"Sequential: {sequential_time:.2f}s")
print(f"Parallel (4 workers): {parallel_time:.2f}s")
print(f"Speedup: {sequential_time / parallel_time:.1f}x")
```

`time.perf_counter()` is a high-resolution timer.
It is better than `time.time()` for benchmarking because it is not affected by clock adjustments.

### What to expect

On a machine with 4 CPU cores and 20 medium-sized PDFs:
- Sequential: ~10 seconds
- Parallel (4 workers): ~3-4 seconds
- Speedup: ~2.5-3x (not exactly 4x due to startup overhead and uneven work distribution)

On very small inputs (1-5 PDFs), multiprocessing may be SLOWER than sequential because:
- Each subprocess startup takes ~0.1-0.5 seconds.
- Pickling/unpickling arguments and results takes time.
- 5 PDFs might parse in 0.5s sequentially but 1.5s in parallel (3s startup + faster parse that doesn't offset the startup).

This is why the default should be `--workers 1` (sequential) until the user opts in to parallel processing.

---

### Deep dive: Architecture diagram

```text
CLI: researchops ingest examples/ --workers 4
        |
        v
ParallelIngestionService.ingest_directory()
        |
        |-- scan: find_pdfs(directory) --> [path_1, path_2, ..., path_N]
        |
        |-- skip_existing check --> [path_3, path_5, path_7, path_N] (filtered)
        |
        |-- _parse_parallel([path_3, path_5, path_7, path_N])
        |       |
        |       |-- ProcessPoolExecutor(max_workers=4)
        |       |       |
        |       |       +-- Worker 1: parse_pdf(path_3) --> result_3
        |       |       +-- Worker 2: parse_pdf(path_5) --> result_5
        |       |       +-- Worker 3: parse_pdf(path_7) --> result_7
        |       |       +-- Worker 4: parse_pdf(path_N) --> result_N
        |       |
        |       +-- collect results [result_3, result_5, result_7, result_N]
        |
        |-- (back in main process) sequential save loop:
        |       for raw in results:
        |           if raw["ok"]: repo.save(paper)
        |           else: repo.record_failure(failure)
        |
        v
IngestionResult (successes=..., failures=..., skipped=...)
        |
        v
CLI: print summary
```

---

### Deep dive: Choosing the number of workers

A reasonable default is `min(4, os.cpu_count() or 1)`.

```python
import os

def default_worker_count() -> int:
    cpu_count = os.cpu_count() or 1
    return min(4, cpu_count)
```

`os.cpu_count()` returns the number of logical CPUs on the machine.
On a 2-core laptop with hyperthreading, it might return 4.
On a 16-core workstation, it returns 16.

The cap of 4 is conservative.
More workers means more memory usage (each process loads its own copy of `pypdf`, parsing libraries, etc.).
For a learning tool, 4 is a reasonable maximum until you have profiled the actual workload.

The CLI flag:
```bash
researchops ingest examples/ --workers 4
researchops ingest examples/ --workers 1  # sequential (default, safest)
```

---

### Deep dive: Testing parallel ingestion

Testing concurrent code requires thinking about what guarantees you are testing.

**Do NOT test ordering.** Workers return in any order.
Tests that assert `result.successes[0].id == "abc"` will fail intermittently.

**DO test counts and membership:**

```python
def test_parallel_ingest_same_count_as_sequential(tmp_path):
    """Parallel mode produces same papers as sequential mode."""
    pdf_paths = [tmp_path / f"paper_{i}.pdf" for i in range(5)]
    for p in pdf_paths:
        p.write_bytes(b"fake")  # placeholder files

    # Build sequential result
    sequential_repo = SQLitePaperRepository(tmp_path / "seq.db")
    sequential_service = IngestionService(
        parser=FakeParser(sample_doc),
        paper_repo=sequential_repo,
        failure_repo=sequential_repo,
    )
    seq_result = sequential_service.ingest_directory(tmp_path)

    # Build parallel result
    parallel_repo = SQLitePaperRepository(tmp_path / "par.db")
    parallel_service = ParallelIngestionService(
        paper_repo=parallel_repo,
        failure_repo=parallel_repo,
        max_workers=4,
    )
    par_result = parallel_service.ingest_directory(tmp_path)

    # Same counts
    assert len(par_result.successes) == len(seq_result.successes)
    assert len(par_result.failures) == len(seq_result.failures)

    # Same paper IDs (sets, not ordered)
    seq_ids = {p.id for p in seq_result.successes}
    par_ids = {p.id for p in par_result.successes}
    assert seq_ids == par_ids
```

This test proves that parallel mode produces equivalent outcomes to sequential mode.
It does not care about ordering.
It uses sets for comparison.

---

### Deep dive: Why database writes from workers are dangerous

Imagine if workers each had their own database connection and wrote directly:

```python
def bad_worker(path_str: str, db_path: str) -> None:
    conn = sqlite3.connect(db_path)  # EACH WORKER GETS ITS OWN CONNECTION
    doc = parse_pdf(Path(path_str))
    conn.execute("INSERT INTO papers ...")
    conn.commit()
    conn.close()
```

Problems:
1. **WAL contention**: Multiple processes writing to SQLite simultaneously causes write conflicts.
   One process must wait while another holds the write lock.
   In the worst case, you get `sqlite3.OperationalError: database is locked`.

2. **Duplicate detection is broken**: The `exists()` check before `save()` in one process may not see rows inserted by another process (due to transaction isolation).
   Two workers might both try to save the same paper.

3. **Partial commits**: If two workers commit at the same time, one might succeed and one might fail.
   You have no way to correlate the failed commit with the paper that was parsed.

The safe rule: **workers only parse, main process only writes**.

---

### Deep dive: Connecting to previous weeks

Week 8 depends on everything that came before it.

**From Week 5**: The `SQLitePaperRepository` that workers must NOT use directly.
The safe architecture keeps the repository in the main process.

**From Week 6**: The `parse_pdf` function that workers call.
It was designed as a single-responsibility function — pure, stateless, easily parallelizable.

**From Week 7**: The cleaned text from `clean_text` is applied by the main process after collecting worker results.
Workers return raw text; the main process applies all post-processing.

The key insight of Week 8: the good design decisions from earlier weeks (pure functions, repository pattern, protocol-based service layer) make multiprocessing possible without rewriting the entire codebase.

---

### Deep dive: Review questions and self-checks

**Conceptual questions:**

1. What is the difference between concurrency and parallelism?
   Give a one-sentence definition of each.

2. What is the GIL?
   Does it prevent all forms of parallelism?

3. When should you choose threading over multiprocessing?
   When should you choose multiprocessing over threading?

4. Why is PDF parsing CPU-bound rather than I/O-bound?

5. What does "pickling" mean?
   Give three examples of things that cannot be pickled.

6. Why must worker functions be top-level (not lambdas or nested functions)?

7. What is the difference between `executor.map` and `executor.submit` with `as_completed`?

8. Why does multiprocessing sometimes make small inputs SLOWER than sequential?

**Architecture questions:**

9. Draw the safe parallel ingestion architecture.
   Label which operations run in workers and which run in the main process.

10. Why is it dangerous to pass a `sqlite3.Connection` to a worker?
    What happens if you try?

11. What is the maximum benefit you can expect from 4 workers on a 2-core machine?
    Why?

**Code-reading questions:**

12. Look at `_parse_worker`.
    Why does it catch ALL exceptions and return a failure dict rather than re-raising?

13. Look at `_parse_parallel`.
    What would happen if one worker raises an exception that is NOT caught inside `_parse_worker`?
    (Hint: `executor.map` re-raises it in the main process when the result is collected.)

14. Why does `_parse_worker` use `path_str: str` instead of `path: Path`?

**Practice tasks:**

15. Write a benchmark that compares sequential vs parallel parsing of 10 sample PDFs.
    Report the speedup.

16. Implement `default_worker_count()` using `os.cpu_count()` with a cap of 4.
    Write a test that it returns at most 4.

17. Write a test that verifies parallel mode produces the same set of paper IDs as sequential mode.



## 7. ResearchOps-specific application

Week 8 belongs to three main project areas named in the syllabus:
- `src/researchops/workers/process_pool.py` — the process-pool wrapper or helper.
- `src/researchops/services/ingestion_service.py` — the ingestion workflow, now with a worker-count path.
- `src/researchops/cli/commands/ingest.py` — the user-facing `--workers` option.

The real test names from the syllabus are:
- `tests/unit/test_process_pool.py`
- `tests/integration/test_ingestion_service.py` — updated for parallel mode.

The service-level flow should remain understandable:
1. The CLI receives a directory and a worker count.
2. The CLI wires concrete objects and calls the ingestion service.
3. The service discovers PDF paths.
4. The service checks skip rules in the parent process.
5. The service sends only selected path strings to the process-pool helper.
6. Workers parse PDFs and return success or failure payloads.
7. The parent process saves papers and records failures.
8. The CLI displays a summary.

If a design makes the worker responsible for storage, it has crossed the Week 8 boundary.
If a design makes the CLI responsible for parsing details, it has crossed the Week 8 boundary.
If a design makes the process-pool helper responsible for deciding business rules, it has crossed the Week 8 boundary.

## 8. Code examples with line-by-line explanation

```python
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


def parse_one_pdf(path_string: str) -> dict[str, object]:
    path = Path(path_string)
    try:
        from researchops.parsing.pdf_parser import parse_pdf

        document = parse_pdf(path)
        return {
            "ok": True,
            "path": path_string,
            "raw_text": document.raw_text,
            "num_pages": document.num_pages,
            "file_size_bytes": document.file_size_bytes,
            "metadata": document.metadata,
        }
    except Exception as error:
        return {
            "ok": False,
            "path": path_string,
            "error_type": type(error).__name__,
            "error_message": str(error),
        }


def parse_many(path_strings: list[str], workers: int) -> list[dict[str, object]]:
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(parse_one_pdf, path_strings))
```

Line-by-line explanation:
- `from concurrent.futures import ProcessPoolExecutor` imports the standard-library class that manages worker processes.
- `from pathlib import Path` lets the worker rebuild a `Path` from the string it receives.
- `def parse_one_pdf(...)` is defined at module level, not inside another function.
- `path_string: str` is used because strings are easy to pickle and send to child processes.
- `path = Path(path_string)` reconstructs a richer path object inside the worker.
- `try:` starts the protected parse region so failures can become data.
- The `parse_pdf` import happens inside the worker so the child process can load what it needs.
- `document = parse_pdf(path)` performs the CPU-heavy parsing for one PDF.
- The success dictionary contains only plain data the parent can understand.
- `except Exception as error:` keeps one bad PDF from crashing the whole batch.
- The failure dictionary includes the path, error type, and message for recording.
- `parse_many` is parent-side orchestration for the process pool.
- The `with` block creates and cleans up the pool.
- `executor.map` sends each path string to the module-level worker.
- `list(...)` collects payloads for parent-side saving.

Unsafe example:

```python
# Wrong for Week 8.
def parse_and_save(path_string: str, database_connection) -> None:
    document = parse_pdf(Path(path_string))
    database_connection.execute("INSERT INTO papers ...")
```

This is wrong because `database_connection` is live process state, not plain data.
It also gives storage responsibility to the worker.
The safe pattern is to return parsed data and let the parent save it.

## 9. Common beginner mistakes

- **Using threads for CPU-heavy parsing.** The GIL prevents threads in one CPython process from running Python bytecode truly in parallel for this workload. Use processes for the parse stage.
- **Passing a repository into a worker.** Repositories often hide connections or state. Pass simple path strings instead.
- **Passing an open SQLite connection into a worker.** Connections are not safe process-boundary payloads. Save from the parent.
- **Defining the worker inside a service method.** Nested functions cannot be imported by child processes. Move the worker to module level.
- **Using a lambda as the worker.** Lambdas do not have stable importable names. Use a named function.
- **Letting worker exceptions escape.** One bad PDF can interrupt result collection. Return a failure payload.
- **Assuming output order means completion order.** Parallel workers can finish at different times. Test counts and identities, not accidental timing.
- **Expecting tiny folders to speed up.** Process startup and pickling overhead may dominate small examples.
- **Writing to SQLite from every worker.** This risks lock contention and confusing duplicate behavior.
- **Treating speed as the only validation.** Correctness and parity are the first requirements.

## 10. Debugging guidance

Start by locating the failure phase:
- Did the CLI reject the worker count?
- Did process-pool creation fail?
- Did Python fail while pickling the worker function or arguments?
- Did parsing fail inside a worker?
- Did collecting results fail in the parent?
- Did saving payloads fail after parsing completed?

Common symptoms:
- `Can't pickle local object` usually means the worker is nested or locally defined.
- `Can't pickle <function <lambda>...>` usually means a lambda was used as the worker.
- `cannot pickle sqlite3.Connection` means live database state crossed the boundary.
- `max_workers must be greater than 0` means validation allowed zero or negative workers.
- `database is locked` suggests writes may be happening concurrently or a transaction is held too long.
- A batch stopping at the first corrupt PDF suggests exceptions are escaping the worker.

Debug with narrow evidence first:
1. Run `pytest tests/unit/test_process_pool.py -v`.
2. Inspect the worker function signature.
3. Print or log the payload shape before process submission in a local experiment.
4. Confirm returned payloads contain `ok`, `path`, and either parsed fields or error fields.
5. Run the integration test only after the process-pool contract is clear.

## 11. Design tradeoffs

- **Sequential default:** safer and simpler for tiny folders, but large folders need an opt-in worker count.
- **Module-level worker:** less visually contained than a nested helper, but required for process execution.
- **Dictionary payloads:** beginner-readable and picklable, but require consistent keys.
- **Parent-only writes:** safer for SQLite and duplicate rules, but saving happens after parsing payloads return.
- **Catching exceptions inside workers:** improves batch survival, but error payloads must contain enough detail.
- **Ordered collection with `executor.map`:** easy to understand, but less flexible for progress reporting than completed-future loops.
- **Worker cap:** avoids wasteful process counts, but a too-small cap may underuse a powerful machine.
- **Parity tests over timing tests:** stable and correctness-focused, but performance still requires separate measurement.

The right design is the one that a learner can explain and validate.

## 12. Testing implications

Week 8 tests must prove contracts, not lucky timing.
`tests/unit/test_process_pool.py` should prove the process-pool helper behavior.
`tests/integration/test_ingestion_service.py` should prove the service still ingests correctly with parallel mode.

A good Week 8 test suite checks:
- worker helper returns one payload per input path;
- success payloads contain enough data for saving;
- failure payloads contain path, error type, and message;
- invalid worker counts are rejected or handled clearly;
- one bad PDF does not erase other results;
- parent-side database writes happen after worker payloads return;
- single-worker and multi-worker ingestion agree logically;
- tests avoid hidden completion-order assumptions.

The official syllabus command is:

```bash
researchops ingest ./examples/sample_papers --workers 2
pytest tests/unit/test_process_pool.py -v
```

Use this additional service check when validating the full workflow:

```bash
pytest tests/integration/test_ingestion_service.py -v
```

## 13. Architecture implications

Week 8 is a boundary test for ResearchOps.
The CLI should expose `--workers`, not own parse logic.
The service should own ingestion workflow, not low-level process mechanics.
The process-pool helper should run CPU-heavy worker calls, not decide business rules.
The worker should parse one PDF, not write to storage.
The repository should save records without caring whether parsing was single-worker or multi-worker.

Safe direction:

```text
CLI command
  -> ingestion service
      -> process-pool helper
          -> module-level parse worker
              -> PDF parser for one path
      -> repository writes in parent process
```

Questions to ask:
- Does the CLI avoid business logic?
- Does the service own workflow decisions?
- Does the worker receive simple data?
- Do workers avoid database writes?
- Does the parent record failures?
- Do tests prove the boundary?

## 14. How this connects to AI engineering / ML research

Research systems depend on trustworthy data preparation.
A paper assistant cannot search, rank, summarize, or analyze papers that were silently dropped during ingestion.
Parallel ingestion teaches the production habit that performance improvements must preserve behavior.
Research folders are messy: they contain corrupt files, scanned PDFs, duplicates, odd metadata, and sometimes empty text extraction.
A useful ingestion system reports those problems and keeps working.

This chapter also teaches resource thinking.
CPU cores are finite.
Worker processes use memory.
Process startup costs time.
A well-designed pipeline splits independent CPU-heavy work while keeping shared state controlled.
That habit is useful long before any advanced research feature appears.

## 15. Mini quizzes

1. What is the Week 8 milestone command?
2. What does CPU-bound mean?
3. Why is PDF parsing CPU-bound in this chapter?
4. What does the GIL prevent inside one CPython process?
5. Why does a process pool help with CPU-heavy parsing?
6. What is pickling?
7. Why should a worker receive a string path?
8. Why must the worker be module-level?
9. What happens if the worker is a lambda?
10. What should a success payload contain?
11. What should a failure payload contain?
12. Why should workers not write to SQLite?
13. What does parent-only saving protect?
14. Why might a tiny folder not get faster with multiple workers?
15. What does a parity test compare?
16. Why is output order a risky assumption?
17. Which unit test file is named in the Week 8 syllabus?
18. Which integration test file is updated for parallel mode?
19. What should happen when one PDF is corrupt?
20. What evidence says the chapter is complete?

## 16. Explain-it-aloud prompts

- Explain `researchops ingest ./papers --workers 4` to a beginner.
- Explain why PDF parsing belongs in a process pool.
- Explain the GIL without using vague phrases.
- Explain the difference between the parent process and a worker process.
- Explain what crosses the process boundary.
- Explain why open connections do not cross the process boundary.
- Explain how a bad PDF becomes a failure record.
- Explain why SQLite writes stay in the parent process.
- Explain how single-worker and multi-worker paths are compared.
- Explain why more workers may not help on tiny inputs.
- Explain what `tests/unit/test_process_pool.py` should prove.
- Explain what `tests/integration/test_ingestion_service.py` should prove.

## 17. What to memorize

- PDF parsing is CPU-bound in Week 8.
- The GIL limits CPU-heavy Python threads inside one CPython process.
- `ProcessPoolExecutor` is the Week 8 tool for CPU-bound parse parallelism.
- Worker functions should be module-level.
- Worker arguments and return values must be picklable.
- Strings, numbers, booleans, lists, dictionaries, and simple data shapes are safe payloads.
- Open database connections, open files, lambdas, and nested functions are unsafe payloads.
- Workers parse; the parent writes.
- One bad PDF should become one recorded failure.
- Parallel mode must match single-worker mode logically.
- The official Week 8 unit test is `tests/unit/test_process_pool.py`.

## 18. What to understand deeply

Understand that multiprocessing is not just a faster loop.
It changes memory, error handling, serialization, startup cost, and the shape of tests.
Understand that pickling errors are often design feedback: you tried to send behavior or live state where plain data belongs.
Understand that parent-only database writes preserve the repository boundary and reduce SQLite contention.
Understand that failure isolation is what makes batch ingestion useful on real research folders.
Understand that result parity matters more than impressive timing.
Understand that a process pool is chosen because of the workload, not because it is fashionable.
Understand that every worker should have one small responsibility: parse one file and report what happened.

Deep trace for a good file:
- scanner finds `paper_a.pdf`;
- service keeps it in the process list;
- parent sends its string path to a worker;
- worker parses it;
- worker returns a success payload;
- parent builds and saves a paper;
- result counts one success.

Deep trace for a bad file:
- scanner finds `broken.pdf`;
- parent sends its string path to a worker;
- parser raises inside the worker;
- worker catches the exception;
- worker returns a failure payload;
- parent records a failed document;
- result counts one failure while the batch continues.

## 19. What not to worry about yet

- Do not build later-month interface features in Week 8.
- Do not build later-month retrieval features in Week 8.
- Do not add later-month serving features in Week 8.
- Do not add distributed queues or clusters.
- Do not replace SQLite.
- Do not tune every possible worker-count strategy.
- Do not chase perfect benchmarks on sample PDFs.
- Do not parallelize database writes.
- Do not hide failures for cleaner output.
- Do not introduce future curriculum topics just to make the chapter feel bigger.

Week 8 is complete when parallel parsing is correct, bounded, tested, and explainable.

## 20. Bridge to next week

Week 8 finishes Month 2 by making ResearchOps more realistic.
The system can scan, parse, store, search, and now ingest with worker processes.
That amount of behavior makes architecture boundaries more important, not less important.
Next week focuses on cleaner interface thinking and dependency direction.
The bridge is direct: multiprocessing is easier because earlier responsibilities were separated.
The parser can run in a worker because it parses one file.
The repository can stay in the parent because storage is already a named boundary.
The service can coordinate the workflow because it already owns ingestion decisions.
The CLI can stay small because it only exposes user options and displays results.

Before moving forward, confirm you can explain:
- why CPU-bound parsing belongs in worker processes;
- why picklability shapes the worker function;
- why worker failures become payloads;
- why the parent writes to SQLite;
- why one-worker and multi-worker results must match;
- why future features should wait.

Additional mastery drills:
- Trace `paper_a.pdf` through the single-worker path, then trace it through the process-pool path and name what changed.
- Trace `broken.pdf` through the process-pool path and identify where the error becomes a failure payload.
- Write one sentence explaining why `Path` can be reconstructed inside the worker from a string.
- Write one sentence explaining why a database connection should not appear in a worker argument list.
- Compare `workers=1` and `workers=4` by correctness first, then by expected runtime behavior.
- Inspect a hypothetical pickling error and identify whether the function, argument, or return value caused it.
- Draw the parent process as one box and worker processes as separate boxes; label every value crossing between boxes.
- Explain why a malformed PDF should affect the failure count but not erase successes from other PDFs.
- Explain why tests should compare sets of paper identities rather than worker completion timing.
- Explain why process startup overhead makes tiny sample folders poor performance benchmarks.
- Identify the narrowest unit test that should fail if the worker stops catching parse exceptions.
- Identify the integration test that should fail if parallel ingestion saves different papers than single-worker ingestion.
- Review the CLI command and state which part is user interface and which part is service behavior.
- Review the service flow and state which part belongs before worker submission and which part belongs after result collection.
- Before Week 9, summarize the Week 8 boundary in one sentence: workers parse, parent writes, tests prove parity.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 08 — Multiprocessing Ingestion:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
