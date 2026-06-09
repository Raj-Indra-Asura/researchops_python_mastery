# Exercises — Week 08 Multiprocessing Ingestion

---

## Easy exercises

### E1 — ProcessPoolExecutor basics

Write a function `square(n: int) -> int` that returns `n * n`.
Use `ProcessPoolExecutor(max_workers=2)` to apply it to `[1, 2, 3, 4, 5]`.
Print the results.
Verify they are `[1, 4, 9, 16, 25]` (same order as input).

### E2 — Timing a CPU-bound function

Write a function that computes the sum of all integers from 1 to 10,000,000.
Time it once with `time.perf_counter()`.
Run it 4 times sequentially and record total time.
Run it 4 times with `ProcessPoolExecutor(max_workers=4)` and record total time.
Compare.

On a multi-core machine, the parallel version should be significantly faster.

### E3 — Worker count

Write a function `default_worker_count() -> int` that:
1. Gets `os.cpu_count()`.
2. Returns `1` if `cpu_count` is `None`.
3. Returns `min(4, cpu_count)`.

Write tests for:
- Machine with 8 CPUs → returns 4.
- Machine with 2 CPUs → returns 2.
- Machine with unknown CPUs (mock `os.cpu_count` to return `None`) → returns 1.

### E4 — A simple pickling experiment

Try to pickle a `lambda`:
```python
import pickle
f = lambda x: x * 2
pickle.dumps(f)  # Will raise PicklingError
```

Try to pickle a top-level function:
```python
def double(x):
    return x * 2

pickle.dumps(double)  # Should succeed
pickle.loads(pickle.dumps(double))(5)  # Should return 10
```

Try to pickle a `sqlite3.Connection`:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
pickle.dumps(conn)  # Will raise
```

Document each result.

### E5 — Return a dataclass from a worker

Define a simple dataclass:
```python
from dataclasses import dataclass

@dataclass
class ParseResult:
    path: str
    word_count: int
    ok: bool
```

Write a worker function that returns a `ParseResult`.
Use `ProcessPoolExecutor` to process 5 fake paths.
Verify the results.

### E6 — Catch a worker exception

Write a worker function that raises `ValueError("bad file")` for any path containing `"bad"`.
Use `executor.map` to process `["good1.pdf", "bad2.pdf", "good3.pdf"]`.
When collecting `list(executor.map(...))`, the `ValueError` from `"bad2.pdf"` will propagate.
Catch it with a `try/except` around the `list(...)` call.

Then rewrite the worker to catch the exception internally and return a failure dict.
Show that with the internal catch, `list(executor.map(...))` succeeds for all 3 paths.

---

## Medium exercises

### M1 — Worker function for ResearchOps

Write `_parse_worker(path_str: str) -> dict` following the pattern in the notes.
The worker should:
1. Convert the string to a Path.
2. Call `parse_pdf(path)`.
3. Return a success dict with `"ok": True` and all relevant fields.
4. Catch all exceptions and return a failure dict with `"ok": False` and error info.

Write tests using a real small PDF from `examples/` or a fake file.

### M2 — Parallel parsing

Implement `parse_all_parallel(pdf_paths: list[Path], max_workers: int) -> list[dict]` that:
1. Converts paths to strings.
2. Runs `_parse_worker` in a `ProcessPoolExecutor`.
3. Returns all results (success and failure dicts) in input order.

### M3 — Main-process result saving

Write `save_results(results: list[dict], repo: SQLitePaperRepository) -> tuple[int, int]` that:
1. Iterates results.
2. For success dicts: builds a `Paper` and calls `repo.save(paper)`.
3. For failure dicts: builds a `FailedDocument` and calls `repo.record_failure(failure)`.
4. Returns `(success_count, failure_count)`.

Test with a mix of success and failure dicts.

### M4 — ParallelIngestionService

Implement `ParallelIngestionService` with:
```python
def __init__(self, paper_repo, failure_repo, max_workers=1)
def ingest_directory(self, directory, *, skip_existing=True) -> IngestionResult
```

Use your `parse_all_parallel` and `save_results` functions internally.

### M5 — CLI integration

Add `--workers INTEGER` to the `researchops ingest` command.
Default to 1.
Pass the value to `ParallelIngestionService`.

Test the CLI with `--workers 1` and `--workers 4` on a sample directory.
Both should produce the same stored papers.

### M6 — as_completed with progress

Rewrite `parse_all_parallel` using `executor.submit` and `as_completed` instead of `executor.map`.
After each completion, print a progress line: `[3/10] ok: paper.pdf`.

Write a test that:
1. Runs the function on 5 fake paths.
2. Captures stdout.
3. Asserts the final count line appears.

---

## Hard exercises

### H1 — Equivalence test

Write a test that proves:
1. Sequential ingestion of 10 files produces a set of paper IDs S1.
2. Parallel ingestion of the same 10 files (workers=4) produces a set of paper IDs S2.
3. S1 == S2.

Use a `FakeParser` that returns controlled results so the test does not depend on real PDFs.

### H2 — Partial failure test

Create 5 fake PDF files.
Configure a worker that fails for exactly 2 of them (files containing `"broken"` in the name).
Run parallel ingestion.
Assert:
- `result.successes` has 3 entries.
- `result.failures` has 2 entries.
- `repo.list_failures()` has 2 entries with correct error messages.

### H3 — Worker that cannot be pickled

Create a class:
```python
class UnpicklableWorker:
    def __init__(self, conn):
        self.conn = conn  # sqlite3.Connection is not picklable
    
    def parse(self, path_str):
        return {"ok": True, "path": path_str}
```

Try to submit `unpicklable.parse` as the worker function.
Observe the error.
Compare with the top-level `_parse_worker` function, which is picklable.

Write a comment explaining why the module-level function works but the method does not.

### H4 — Benchmark and report

Write a benchmark script at `scripts/benchmark_ingestion.py` that:
1. Creates a temporary database.
2. Generates or uses existing sample PDFs (at least 10).
3. Runs ingestion with `--workers 1` and records time.
4. Runs ingestion with `--workers 4` and records time.
5. Prints a report:
   ```
   Sequential (1 worker):  12.3s
   Parallel   (4 workers):  4.1s
   Speedup:                 3.0x
   ```

### H5 — Safe concurrent writes experiment

Demonstrate the danger of concurrent SQLite writes:
1. Write a script that spawns 4 threads, each inserting 100 rows into the same SQLite database.
2. Observe intermittent `OperationalError: database is locked` errors.
3. Add WAL mode: `conn.execute("PRAGMA journal_mode = WAL")`.
4. Observe the errors may reduce but not disappear under heavy concurrent write load.
5. Conclude that for correctness, writes should always happen in a single thread/process.

---

## Brutal exercises

### B1 — Full test suite for parallel ingestion

Write `tests/integration/test_parallel_ingest.py` with at least 12 tests:
- 1 worker produces same result as the sequential `IngestionService`.
- 4 workers produces same set of paper IDs as 1 worker.
- All successes recorded correctly.
- All failures recorded correctly.
- skip_existing works in parallel mode.
- Empty directory returns empty result with no crash.
- Worker exception is caught and recorded as failure.
- Progress reporting does not crash.
- `result.total` is correct.
- `result.success_rate` is correct.
- Repeated ingestion with `skip_existing=True` does not duplicate papers.
- `list_all()` after parallel ingest returns correct count.

### B2 — Worker pool stress test

Create a script that:
1. Generates 100 fake PDF paths.
2. Makes 10 of them "fail" (the worker returns failure for filenames ending in `_fail.pdf`).
3. Runs parallel ingestion with `max_workers=8`.
4. Asserts 90 successes and 10 failures.
5. Runs it 3 times and asserts the same counts each time (stability test).

### B3 — Auto-detect worker count

Implement a `SmartIngestionService` that:
1. Measures the time to parse the first PDF in the directory.
2. If parsing took more than 1 second, uses `default_worker_count()` workers.
3. If parsing took less than 0.1 seconds, uses 1 worker (overhead not worth it).

This is a heuristic, not a guarantee.
Write a test for each branch.

---

## Written explanation exercises

### W1 — GIL explanation

Write a paragraph explaining the Global Interpreter Lock to a Python beginner.
Use an analogy.
Do NOT use words like "mutex" or "bytecode" — find everyday language.

### W2 — When not to use multiprocessing

Write a list of 5 scenarios where multiprocessing would NOT help (or would make things worse):
1. ...
2. ...
3. ...
4. ...
5. ...

For each, explain why.

### W3 — Design justification

Write a paragraph justifying the "workers parse, main process saves" architecture.
Address: why is it safer, what bugs does it prevent, and what does it give up?

---

## Testing exercises

### T1 — Test worker isolation

```python
def test_one_failing_worker_does_not_stop_others(tmp_path):
    paths = [tmp_path / f"paper_{i}.pdf" for i in range(5)]
    for p in paths:
        p.write_bytes(b"fake")
    
    # Make paper_2 fail
    (tmp_path / "paper_2.pdf").write_bytes(b"")  # empty file causes parse error
    
    results = parse_all_parallel(paths, max_workers=4)
    successes = [r for r in results if r["ok"]]
    failures = [r for r in results if not r["ok"]]
    
    assert len(successes) == 4
    assert len(failures) == 1
```

### T2 — Test result order

```python
def test_results_in_input_order(tmp_path):
    paths = [tmp_path / f"paper_{i}.pdf" for i in range(10)]
    for p in paths:
        p.write_bytes(b"fake")
    
    results = parse_all_parallel(paths, max_workers=4)
    
    for i, r in enumerate(results):
        assert f"paper_{i}" in r["path"]
```

### T3 — Test default worker count

```python
from unittest.mock import patch

def test_default_worker_count_caps_at_4():
    with patch("os.cpu_count", return_value=16):
        assert default_worker_count() == 4

def test_default_worker_count_uses_cpu_count_when_small():
    with patch("os.cpu_count", return_value=2):
        assert default_worker_count() == 2
```

---

## Debugging exercises

### D1 — Diagnose the pickling error

The following code raises a `PicklingError`.
Identify the cause and fix it.

```python
class Parser:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
    
    def parse(self, path_str):
        return {"path": path_str, "ok": True}

parser = Parser()
with ProcessPoolExecutor(max_workers=2) as executor:
    list(executor.map(parser.parse, ["a.pdf", "b.pdf"]))
```

### D2 — Diagnose the nested function

This code raises a `PicklingError` too.
Why?

```python
def process_directory(paths):
    def worker(path_str):
        return {"ok": True, "path": path_str}
    
    with ProcessPoolExecutor(max_workers=2) as executor:
        return list(executor.map(worker, [str(p) for p in paths]))
```

Fix it by moving `worker` to module level.

### D3 — Diagnose the race condition

The following parallel implementation has a race condition.
Identify it.

```python
def ingest_parallel(pdfs, repo):
    def worker(path_str):
        paper_id = str(PaperId.from_path(Path(path_str)))
        if not repo.exists(paper_id):   # <-- check
            doc = parse_pdf(Path(path_str))
            paper = build_paper(doc)
            repo.save(paper)            # <-- and save
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(worker, [str(p) for p in pdfs]))
```

Explain: why can two workers both pass the `exists()` check for the same paper, and both try to call `save()`?

---

## Mini project task

### P1 — Multiprocessing milestone

Complete the parallel ingestion for ResearchOps:

1. Implement `_parse_worker` as a top-level function in `workers/process_pool.py`.
2. Implement `ParallelIngestionService` in `services/ingestion_service.py` or a new file.
3. Add `--workers INTEGER` (default `1`) to the `ingest` CLI command.
4. Write `tests/integration/test_parallel_ingest.py` with at least 8 tests.
5. Run `pytest` and confirm all tests pass.
6. Run `ruff check src tests` and confirm no lint errors.
7. Run `researchops ingest examples/sample_papers/ --workers 4 --db /tmp/test_parallel.db`.
8. Compare the result with `--workers 1` on the same directory.
9. Write a comment in the code explaining why the database writes happen in the main process.

Deliverable: a parallel ingest command with equivalent correctness to sequential mode.
