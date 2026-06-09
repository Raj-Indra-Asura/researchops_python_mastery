# Exercises - Week 03 OOP and Domain Modeling

## Warm-up exercises
1. Open `src/researchops/core/models.py` and read the `Paper` dataclass. Create a `Paper` instance in a Python REPL and call `word_count()` on it.
2. Create a `ParsedDocument` with whitespace-only `raw_text` and assert `is_empty()` returns `True`.
3. Read `core/value_objects.py`. Try constructing a `Query` with an empty string and confirm it raises `EmptyQueryError`.
4. Compare two `PaperId` objects created from the same path — confirm they are equal.

## Project exercises
1. Study `tests/unit/test_models.py`. Run it with `pytest tests/unit/test_models.py -v` and read every test case. Understand why each assertion exists.
2. Add a `display_summary()` method to `IngestionResult` that returns a human-readable string like `"Run abc123: 5 ok / 2 failed / 1 skipped (80.0%)"`. Write a test for it in `tests/unit/test_models.py`.
3. Add a `slug` property to `Paper` that lowercases the title and replaces spaces with hyphens (e.g. `"Graph Search"` → `"graph-search"`). Write a test.
4. Study `tests/fakes/fake_repository.py`. Understand how it implements the `PaperRepository` and `FailureRepository` protocols. Write a new test in `tests/unit/test_models.py` that uses the fake repo to confirm `IngestionResult.success_rate` is calculated correctly after adding one success and one failure.

## Stretch exercises
1. Make `PaperId` fully `frozen=True` (it already is — read `core/models.py` and confirm). Try to mutate one after creation and observe the `FrozenInstanceError`.
2. Add a `to_dict()` method to `Paper` that returns a dictionary suitable for JSON serialisation using `utils/serialization.py`'s `to_json()`. Write a test.
3. Add a `IngestionStatus` enum value to model the state of an ingestion attempt (it already exists as `IngestionStatus(StrEnum)` in `core/models.py` — read it and write a test that confirms all four states).

## Writing questions
1. Why is a dataclass better than a loose dictionary here?
2. Which fields feel essential versus optional?
3. What invariant did you enforce, and why?
4. Where should behavior live: on the model or in a service?
