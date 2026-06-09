# Validation - Week 08 Multiprocessing Ingestion

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,parsing,storage]"
researchops ingest examples/sample_papers --db researchops.db --workers 1
researchops ingest examples/sample_papers --db researchops.db --workers 4
pytest tests/unit/test_parallel_ingestion.py -v
pytest tests/integration/test_ingest_workers.py -v
```

## Expected outputs
- Both ingest commands complete successfully.
- Multi-worker mode reports the same logical results as single-worker mode.
- Parallel ingestion tests pass.

## Pytest commands and expected results
```bash
pytest -k "parallel_ingestion or ingest_workers" -v
pytest -q
```

Expected result: worker-based parsing is stable, failures are captured, and the parent process persists consistent results regardless of worker count.

## Completion checklist
- [ ] Worker-safe parse function exists.
- [ ] CLI accepts `--workers`.
- [ ] Worker count validation exists.
- [ ] Parent process owns database writes.
- [ ] Success and failure aggregation works.
- [ ] Sequential and parallel tests agree on totals.
- [ ] A benchmark or timing note exists.
- [ ] No hidden ordering assumption breaks tests.
- [ ] `pytest -q` passes.
- [ ] You can explain why this workload is CPU-bound.
