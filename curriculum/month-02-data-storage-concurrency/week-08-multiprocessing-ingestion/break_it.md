# Break It - Week 08 Multiprocessing Ingestion

## Intentional failure experiments
1. Try to pass a live SQLite connection into a worker and inspect the serialization failure.
2. Use a worker function nested inside another function and see whether it can be pickled.
3. Set `--workers 0` and define how your CLI should respond.
4. Force one worker to raise an exception on a known file.
5. Compare output ordering between two multi-worker runs.

## Debugging tasks
- Log worker input paths and returned statuses.
- Time sequential and parallel runs with the same dataset.
- Run `pytest -k ingest_workers -v` after concurrency changes.

## Edge cases to explore
- One-file ingest.
- Worker count larger than file count.
- Mixed success and failure in the same batch.
- Re-running ingest with existing stored records.

## What did you learn?
- What can and cannot be safely sent to a worker?
- When did parallel mode help most?
- Which concurrency bug would be hardest to notice without tests?
