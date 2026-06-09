# Break It - Week 15 Async I/O and Network Fetching

## Intentional failure experiments
1. Remove the timeout and simulate a hanging request.
2. Retry indefinitely by mistake and inspect the runaway behavior.
3. Launch too many concurrent requests and watch resource usage rise.
4. Mix blocking code into the async path and see the event loop stall.
5. Cancel a task mid-run and decide how the batch should report it.

## Debugging tasks
- Log start and end times for each URL.
- Count retries per request.
- Run `pytest -k async_fetch -v` after changing timeout or retry logic.

## Edge cases to explore
- Empty URL list.
- One bad URL among many good ones.
- Slow responses that eventually succeed.
- `429` or `503` responses.

## What did you learn?
- Which failure mode required the clearest timeout policy?
- What hidden blocking call hurt concurrency?
- How will you explain partial success to a user?
