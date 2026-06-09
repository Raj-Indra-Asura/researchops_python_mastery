# Break It - Week 16 Local Worker and Job System

## Intentional failure experiments
1. Run the same job twice without idempotency protection and inspect duplicate effects.
2. Crash the worker after marking a job running but before completion.
3. Retry forever by mistake and observe why bounded policies matter.
4. Submit a job with an unknown type and define failure handling.
5. Corrupt one job payload and inspect validation behavior.

## Debugging tasks
- Print job states before and after each worker iteration.
- Force one handler exception and track attempts.
- Run `pytest -k local_worker -v` while refining state transitions.

## Edge cases to explore
- Empty queue.
- Multiple queued jobs.
- Recovered worker after a crash.
- Job payloads missing expected keys.

## What did you learn?
- Which state transition was easiest to get wrong?
- How did idempotency shape your design?
- What information is essential for job observability?
