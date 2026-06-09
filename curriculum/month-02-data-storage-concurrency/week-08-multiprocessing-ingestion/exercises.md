# Exercises - Week 08 Multiprocessing Ingestion

## Warm-up exercises
1. Use `ProcessPoolExecutor` to square a list of numbers.
2. Compare runtime of a CPU-heavy loop with one worker versus multiple workers.
3. Return a simple dataclass from a worker process.
4. Capture one worker exception without crashing the whole program.

## Project exercises
1. Refactor parsing into a worker-safe function.
2. Add `--workers` to the ingest CLI.
3. Collect worker results in the main process and persist them there.
4. Write tests proving sequential and parallel ingestion produce equivalent outcomes.

## Stretch exercises
1. Auto-pick a worker count from `os.cpu_count()` with a safe cap.
2. Add progress reporting while futures complete.
3. Add a benchmark script that prints sequential versus parallel timings.

## Writing questions
1. Why should SQLite writes stay in the parent process?
2. What overhead makes multiprocessing slower on tiny inputs?
3. Which result guarantees matter more than exact ordering?
4. How will you decide a sensible default worker count?
