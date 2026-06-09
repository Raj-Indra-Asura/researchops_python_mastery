# Break It - Week 09 Protocols and Clean Architecture

## Intentional failure experiments
1. Make a fake repository miss one required method and inspect the type or runtime failure.
2. Import SQLite directly inside the service after defining protocols and notice the coupling return.
3. Change a protocol method signature without updating adapters.
4. Build a fake that behaves differently than the real repository and compare test confidence.
5. Let the service instantiate its own repository and note how tests become harder.

## Debugging tasks
- Search for concrete infrastructure imports inside service modules.
- Run unit tests with fakes first, then integration tests with SQLite.
- Compare constructor signatures before and after the refactor.

## Edge cases to explore
- Fake repository storing duplicate records.
- Parser fake that raises deterministic failures.
- Adapters with optional extra methods beyond the protocol.

## What did you learn?
- Which coupling was hardest to remove?
- How did fake-based tests change your speed?
- What makes an abstraction useful instead of ceremonial?
