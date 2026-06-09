# Validation - Week 15 Async I/O and Network Fetching

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,api]"
pytest tests/unit/test_async_fetch.py -v
pytest tests/integration/test_fetch_command.py -v
```

## Expected outputs
- Async fetch tests pass.
- Integration fetch command test passes.
- Timeouts, retries, and partial failures behave as designed.

## Pytest commands and expected results
```bash
pytest -k "async_fetch or fetch_command" -v
pytest -q
```

Expected result: concurrent fetches complete faster than naive sequential execution on test fixtures, timeout and retry policies are applied, and failures do not erase successful results.

## Completion checklist
- [ ] Async fetcher exists.
- [ ] Timeout is configured.
- [ ] Retry count is bounded.
- [ ] Concurrency limit exists.
- [ ] Success and failure result shapes are clear.
- [ ] CLI fetch command exists.
- [ ] Async unit tests pass.
- [ ] Integration fetch test passes.
- [ ] `pytest -q` passes.
- [ ] You can explain the event loop at a practical level.
