# Notes - Week 08 Multiprocessing Ingestion

Not all slow code benefits from the same optimization. If your program spends most of its time waiting on network or disk, async I/O may help. If it spends time doing CPU-heavy work such as PDF parsing, text cleanup, or feature extraction, multiprocessing is often a better tool. That is because Python threads share one interpreter lock for Python bytecode, while separate processes can truly run on multiple CPU cores.

`concurrent.futures.ProcessPoolExecutor` provides a convenient interface for process-based parallelism.

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(parse_one_path, pdf_paths))
```

Each worker process runs `parse_one_path` for a subset of inputs. The key rule is that arguments and return values must be serializable, usually via `pickle`. That means you should pass simple values or well-behaved dataclasses, not open database connections or logger objects with complex state.

A common design is to parse in parallel but write to SQLite in the parent process. SQLite supports concurrent reads well enough, but concurrent writes from many processes can introduce locking issues. So a safer flow is:
1. main process scans paths
2. worker processes parse documents
3. main process collects results
4. main process persists results

That boundary keeps persistence deterministic.

```python
def parse_task(path_str: str) -> tuple[str, str]:
    path = Path(path_str)
    text = extract_text(path)
    return path_str, text
```

Keep worker tasks small and pure. Pure functions are easier to serialize, test, and retry.

Error handling changes in a pool. A failure in one worker does not have to destroy the whole batch, but you need to decide how to capture it. One strategy is to catch errors inside the worker and return a failure-shaped result. Another is to let the future fail and handle exceptions when collecting results.

```python
for future in futures:
    try:
        result = future.result()
    except Exception as exc:
        failures.append(str(exc))
```

Performance work should be measured, not assumed. Use `time.perf_counter()` around sequential and multi-worker runs, then compare elapsed time. Small inputs may actually be slower in multiprocessing because process startup and serialization add overhead.

A `--workers` CLI flag gives the user control:

```bash
researchops ingest examples/sample_papers --db researchops.db --workers 4
```

Good defaults matter. Often `1` is the safest default while parallel mode is opt-in until the implementation is mature.

Testing concurrency can feel tricky, so focus on stable guarantees. The exact processing order may vary, but the final counts and stored outputs should not. Write tests that compare sets of ingested paths, success counts, and failure counts rather than assuming a specific ordering unless your code explicitly sorts results.

This week teaches a broader lesson: scaling code is not only about making it faster. It is about preserving correctness while changing execution strategy. If the multi-worker version is faster but drops failures, duplicates writes, or corrupts data, it is not an improvement. Correctness first, then speed.
