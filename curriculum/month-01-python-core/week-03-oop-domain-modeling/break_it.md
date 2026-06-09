# Break It - Week 03 OOP and Domain Modeling

## Intentional failure experiments
1. Construct a `Paper` with an empty string for `text`. Confirm `is_empty()` returns `True`. Now add a `__post_init__` check that raises `ValueError` when `title.strip()` is empty — watch the existing test for non-empty title pass, then write a test that catches the error for an empty title.
2. Change a list field on `Paper` to `tags: list[str] = []` (without `field(default_factory=list)`). Create two `Paper` instances and append to one's `tags`. Observe that both share the same list. Then restore `default_factory`.
3. Try to assign a new value to a `PaperId.value` field — it is `frozen=True`, so you should get `FrozenInstanceError`.
4. Rename the `error_type` field on `FailedDocument` but do not update `summary()`. Run the test and read the `AttributeError`.
5. Store a `Path` in `Paper.source_path` in one test and a `str` in another. Notice how downstream code that calls `.name` on the field behaves differently.

## Debugging tasks
- Inspect the generated `__repr__` of `IngestionResult` to see whether it is readable when failures is a long list.
- Add assertions about equality to reveal missing or extra fields.
- Use `dataclasses.fields(Paper)` to inspect all declared fields at runtime.

## Edge cases to explore
- `Paper` with an empty `tags` list — confirm it does not share state with another instance.
- `IngestionResult` with zero items — confirm `success_rate` returns `0.0`.
- `FailedDocument.summary()` when `source_path.name` is unusual (e.g. a path with spaces).
- `PaperId.from_path()` called with a relative path versus an absolute path — are the IDs the same?

## What did you learn?
- Which model boundary reduced complexity the most?
- What did mutable defaults teach you?
- Which fields need validation immediately versus later?
