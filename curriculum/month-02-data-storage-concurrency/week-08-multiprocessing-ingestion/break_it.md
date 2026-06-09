# Break It — Week 08 Multiprocessing Ingestion

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 2](../README.md) › [Week 8 — Multiprocessing Ingestion](./README.md) › **break_it.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

---

## Scenario 1 — Pass a database connection to a worker

**Setup:** Modify a worker function to accept a `sqlite3.Connection` parameter.

```python
def bad_worker(path_str: str, conn: sqlite3.Connection) -> dict:
    doc = parse_pdf(Path(path_str))
    conn.execute("INSERT INTO papers ...")  # this never runs
    return {}
```

**Break it:**
```python
import sqlite3
conn = sqlite3.connect(":memory:")
with ProcessPoolExecutor(max_workers=2) as executor:
    list(executor.map(bad_worker, ["paper.pdf", "paper2.pdf"], [conn, conn]))
```

**Expected error:**
```
_pickle.PicklingError: Can't pickle <class 'sqlite3.Connection'>
```

Or similar pickling-related error.

**What to observe:**
- The error occurs when `executor.map` tries to serialize the arguments to send to the worker.
- The `sqlite3.Connection` cannot cross process boundaries.
- The error message tells you exactly what went wrong.

**Fix:** Remove the connection from the worker arguments.
Have the worker return data.
Save in the main process.

---

## Scenario 2 — Use a lambda as the worker function

**Setup:**
```python
with ProcessPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(
        lambda path: {"ok": True, "path": path},
        ["paper1.pdf", "paper2.pdf"]
    ))
```

**Expected error:**
```
_pickle.PicklingError: Can't pickle <function <lambda> at 0x...>
```

**What to observe:**
- Lambda functions are anonymous and cannot be pickled.
- The error occurs before any work is done.

**Fix:** Move the function to module level:
```python
def _worker(path: str) -> dict:
    return {"ok": True, "path": path}
```

---

## Scenario 3 — Define the worker inside another function

**Setup:**
```python
def ingest_files(paths):
    def worker(path_str):   # nested function
        return {"ok": True, "path": path_str}
    
    with ProcessPoolExecutor(max_workers=2) as executor:
        return list(executor.map(worker, paths))
```

**Break it:** Call `ingest_files(["a.pdf", "b.pdf"])`.

**Expected error:**
```
AttributeError: Can't pickle local object 'ingest_files.<locals>.worker'
```

**What to observe:**
- Nested functions are not accessible at module level.
- `pickle` looks up the function by module path.
- A nested function has no module-level path.

**Fix:** Move `worker` to module level.

---

## Scenario 4 — Force one worker to crash with an uncaught exception

**Setup:** Write a worker that raises an uncaught exception for a specific path:
```python
def crashing_worker(path_str: str) -> dict:
    if "crash" in path_str:
        raise RuntimeError("Catastrophic failure")
    return {"ok": True, "path": path_str}
```

**Break it:**
```python
paths = ["good1.pdf", "crash_me.pdf", "good2.pdf"]
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(crashing_worker, paths))
```

**Expected behavior:**
- `executor.map` re-raises the exception in the main process when it hits the failed result.
- `list(...)` raises `RuntimeError: Catastrophic failure`.
- Results for `"good1.pdf"` and `"good2.pdf"` are LOST.

**Fix:** Catch all exceptions INSIDE the worker and return a failure dict.
This is the key design principle of `_parse_worker`.

---

## Scenario 5 — Set workers to 0

**Setup:**
```python
with ProcessPoolExecutor(max_workers=0) as executor:
    list(executor.map(some_worker, paths))
```

**Expected error:**
```
ValueError: max_workers must be greater than 0
```

**What to observe:**
- `ProcessPoolExecutor` validates the `max_workers` parameter.
- Your CLI should validate `--workers` before passing it to the executor.

**Fix:**
```python
if args.workers < 1:
    raise click.BadParameter("--workers must be at least 1", param_hint="workers")
```

---

## Scenario 6 — Workers greater than file count

**Setup:** Ingest a directory with 3 PDFs using `--workers 100`.

**What to observe:**
- `ProcessPoolExecutor` creates 100 worker processes.
- Only 3 of them receive work.
- The other 97 start up and immediately shut down.
- This is wasteful but NOT incorrect.
- Startup overhead is significant.

**Measure:** Time the ingestion.
Compare with `--workers 3` (matching files).
The 100-worker version is likely slower due to process startup overhead.

**Fix:** Cap workers at `min(max_workers, len(paths))` if you want to avoid unnecessary processes.
But do not over-optimize; `ProcessPoolExecutor` handles this gracefully.

---

## Scenario 7 — Concurrent write experiment

**Setup:** Write a script that spawns 4 threads, each writing 50 rows to the same SQLite file.

```python
import sqlite3
import threading

def write_rows(thread_id: int, db_path: str, n: int) -> None:
    conn = sqlite3.connect(db_path)
    for i in range(n):
        conn.execute(
            "INSERT INTO items (thread_id, value) VALUES (?, ?)",
            (thread_id, i)
        )
        conn.commit()
    conn.close()

# Run 4 threads
threads = [threading.Thread(target=write_rows, args=(i, "test.db", 50)) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

**What to observe:**
- With WAL mode disabled, you may see `OperationalError: database is locked`.
- With WAL mode enabled (`conn.execute("PRAGMA journal_mode = WAL")`), errors reduce but concurrent commits under heavy load may still fail.
- Count the rows after: do you have exactly 200 rows?

**Lesson:** SQLite was designed for single-writer use cases.
While it handles concurrent reads well, concurrent writes require careful design.
The safe design: one writer, many readers.

---

## Scenario 8 — Process startup overhead measurement

**Setup:** Create 5 files and time two approaches:
1. Sequential (no overhead): `time.perf_counter()` around a simple loop.
2. ProcessPoolExecutor: `time.perf_counter()` around the entire pool operation.

```python
import time
from concurrent.futures import ProcessPoolExecutor

def identity(x):
    return x

paths = [f"paper_{i}.pdf" for i in range(5)]

start = time.perf_counter()
results = [identity(p) for p in paths]
print(f"Sequential: {time.perf_counter() - start:.4f}s")

start = time.perf_counter()
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(identity, paths))
print(f"Parallel: {time.perf_counter() - start:.4f}s")
```

**What to observe:**
- The sequential version is near-instant (0.0001s).
- The parallel version takes 0.3-2.0s due to process startup.

**Lesson:** Multiprocessing overhead is real.
For very fast tasks (< 0.1s each), sequential processing is faster.
For slow tasks (> 1s each), parallel processing wins.

---

## Scenario 9 — Ordering guarantee with executor.map

**Setup:** Create a worker that sleeps for varying durations to simulate different parse times:

```python
import time

def variable_speed_worker(n: int) -> int:
    duration = (5 - n) * 0.5  # n=0 sleeps 2.5s, n=4 sleeps 0s
    time.sleep(duration)
    return n
```

**Run:**
```python
inputs = [0, 1, 2, 3, 4]
with ProcessPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(variable_speed_worker, inputs))
print(results)
```

**What to observe:**
- Even though worker 4 (0s sleep) finishes before worker 0 (2.5s sleep), `results` is `[0, 1, 2, 3, 4]`.
- `executor.map` preserves input order in the output.
- The total time is approximately 2.5s (dominated by the slowest worker), not 7.5s (sequential).

**Compare with `as_completed`:**
```python
from concurrent.futures import as_completed

futures = [executor.submit(variable_speed_worker, n) for n in inputs]
for future in as_completed(futures):
    print(future.result())  # prints in completion order: 4, 3, 2, 1, 0
```

---

## Scenario 10 — Memory usage

**Setup:** Modify the worker to return a very large result (e.g., 10 MB of text for each PDF).

**Break it:** Process 8 workers simultaneously.

**What to observe:**
- Each worker process holds the result in memory.
- The main process receives and holds all results.
- With 8 workers each returning 10 MB: 80 MB for worker processes + 80 MB collected in main = 160 MB.
- If each PDF has 50 MB of text, this becomes 800 MB.

**Discuss:**
- Should the worker return the full raw text, or just a summary?
- Could you stream results back instead of collecting them all at once?
- What is the memory implication of `list(executor.map(...))`?

---

## Edge cases to explore

1. **Empty path list:** `parse_all_parallel([], max_workers=4)`.
   Should return `[]` without creating any workers.
   Verify this works.

2. **workers=1 vs sequential:** With 1 worker, `ProcessPoolExecutor` still starts a separate process.
   Is there a performance difference vs purely sequential code (no executor)?
   Measure it.
   Discuss when you would use workers=1 explicitly.

3. **Non-PDF files in the directory:** Your scanner only finds `.pdf` files.
   What happens if a `.docx` file is accidentally passed to `_parse_worker`?
   The worker should return a failure dict, not crash.

4. **Keyboard interrupt during parallel ingestion:**
   Press Ctrl+C while parallel ingestion is running.
   What happens to the worker processes?
   Are the already-saved results kept?

5. **Re-running with skip_existing:** Run parallel ingestion twice.
   The second run should skip all already-ingested papers.
   Verify that `result.skipped` equals the count of successfully ingested papers from the first run.

---

## What did you learn?

1. What was the most surprising behavior you discovered about `ProcessPoolExecutor`?
2. Which error message was most helpful for diagnosing a pickling problem?
3. Why should performance optimization always come after correctness?
4. What is the most important design rule you will apply to future parallel code?
5. How did the GIL explanation change your understanding of Python threading?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 2 — Data Storage and Concurrency · **Week 8 — Multiprocessing Ingestion** · *break_it.md — the failure lab* (step 4 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [exercises.md](./exercises.md)
- ▶ **Next:** [validation.md](./validation.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. **➡ [break_it.md](./break_it.md) ← you are here**
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 9](../../../curriculum/month-03-ml-engineering/week-09-protocols-clean-architecture/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 9 — Protocols & Clean Architecture](../../../curriculum/month-03-ml-engineering/week-09-protocols-clean-architecture/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 2 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 2 overview](../README.md) · [📄 Week 8 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
