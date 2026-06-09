<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 08 — Multiprocessing Ingestion:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 08 Notes — Multiprocessing Ingestion

## 1. Chapter overview

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

## 2. Correctness before speed

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

## 3. Concurrency vs parallelism

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

Python's `asyncio` provides concurrency (many tasks in progress, but only one runs at a time in the event loop).
Python's `multiprocessing` provides parallelism (multiple processes, each on a separate CPU core).

---

## 4. CPU-bound vs I/O-bound

Performance problems fall into two categories:

**I/O-bound**: the program spends most of its time waiting for external operations.
- Waiting for a network response.
- Waiting for a database query to return.
- Waiting for a file to be read from disk.

For I/O-bound work, `asyncio` or threading is often effective.
While one task waits for a response, another task can run.

**CPU-bound**: the program spends most of its time computing.
- PDF text extraction (parsing font tables, reconstructing character positions).
- Machine learning inference.
- Image processing.
- Compression/decompression.
- Hashing large files.

For CPU-bound work, `asyncio` is not useful because the event loop cannot run other tasks while Python is executing code.
Threading is also mostly unhelpful due to the Global Interpreter Lock (covered next).

**PDF parsing is CPU-bound.**

The `pypdf` library reads the binary PDF structure, decodes character tables, and reconstructs the text.
This is mostly computation, not waiting.
Each core can independently parse a different PDF.
Multiprocessing is the right tool.

---

## 5. The Global Interpreter Lock (GIL)

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

## 6. Process vs Thread

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

## 7. ProcessPoolExecutor

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

## 8. Pickling: the serialization requirement

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

## 9. The safe architecture: parse in parallel, save sequentially

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

## 10. Complete parallel ingestion implementation

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

## 11. The worker function in detail

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

## 12. Result aggregation

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

## 13. Progress reporting

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

## 14. Benchmarking

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

## 15. Architecture diagram

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

## 16. Choosing the number of workers

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
More workers means more memory usage (each process loads its own copy of `pypdf`, models, etc.).
For a learning tool, 4 is a reasonable maximum until you have profiled the actual workload.

The CLI flag:
```bash
researchops ingest examples/ --workers 4
researchops ingest examples/ --workers 1  # sequential (default, safest)
```

---

## 17. Testing parallel ingestion

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

## 18. Why database writes from workers are dangerous

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

## 19. Connecting to previous weeks

Week 8 depends on everything that came before it.

**From Week 5**: The `SQLitePaperRepository` that workers must NOT use directly.
The safe architecture keeps the repository in the main process.

**From Week 6**: The `parse_pdf` function that workers call.
It was designed as a single-responsibility function — pure, stateless, easily parallelizable.

**From Week 7**: The cleaned text from `clean_text` is applied by the main process after collecting worker results.
Workers return raw text; the main process applies all post-processing.

The key insight of Week 8: the good design decisions from earlier weeks (pure functions, repository pattern, protocol-based service layer) make multiprocessing possible without rewriting the entire codebase.

---

## 20. Review questions and self-checks

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
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 08 — Multiprocessing Ingestion:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
