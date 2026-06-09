# Week 08 - Multiprocessing Ingestion

## Learning objectives
- Understand why PDF parsing can be CPU-bound.
- Use `ProcessPoolExecutor` for parallel ingestion work.
- Decide what data is safe to pass between processes.
- Add a `--workers` flag to the ingest command.
- Preserve correctness while improving throughput.
- Handle worker failures and merge results cleanly.
- Measure before and after performance.

## Project milestone
Parallelize the ingestion pipeline so multiple documents can be parsed concurrently with a configurable worker count.

## Files to modify/create
- `src/researchops/services/parallel_ingestion.py`
- `src/researchops/cli/ingest.py`
- `tests/unit/test_parallel_ingestion.py`
- `tests/integration/test_ingest_workers.py`
- `scripts/benchmark_ingest.py`

## Concepts covered
CPU-bound work, multiprocessing, serialization, futures, worker pools, performance measurement, and deterministic result aggregation.

## Expected deliverables
- An ingestion path that uses `ProcessPoolExecutor`.
- CLI support for `--workers`.
- Tests for single-worker and multi-worker behavior.
- Benchmark notes comparing runtimes.

## Definition of done
- [ ] `--workers` flag exists.
- [ ] Worker count of 1 behaves like sequential mode.
- [ ] Multi-worker mode returns the same logical results.
- [ ] Parse failures from workers are captured.
- [ ] No database connection is shared unsafely across processes.
- [ ] Tests cover concurrency boundaries.
- [ ] Benchmark output is recorded.
- [ ] You can explain when multiprocessing helps and when it does not.
