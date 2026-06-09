# Validation - Week 16 Local Worker and Job System

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,storage]"
pytest tests/unit/test_job_states.py -v
pytest tests/integration/test_local_worker.py -v
```

## Expected outputs
- Job state tests pass.
- Worker integration test shows queued work becoming completed or failed as expected.
- Retry behavior is bounded and visible.

## Pytest commands and expected results
```bash
pytest -k "job_states or local_worker" -v
pytest -q
```

Expected result: jobs move through explicit states, the worker processes them reliably, retries do not create unsafe duplicates, and test coverage captures failure recovery paths.

## Completion checklist
- [ ] Job model exists.
- [ ] Job states are defined.
- [ ] Queue persistence exists.
- [ ] Worker loop exists.
- [ ] Retry count is tracked.
- [ ] Failure reason is recorded.
- [ ] Idempotency rule is documented.
- [ ] Unit tests pass.
- [ ] Integration worker test passes.
- [ ] `pytest -q` passes.
- [ ] You can explain the state machine clearly.
