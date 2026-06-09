# Week 03 - OOP and Domain Modeling

## Learning objectives
- Understand when classes clarify a domain better than raw dictionaries.
- Use `@dataclass` to model paper processing entities with less boilerplate.
- Define invariants for domain objects such as required fields and valid states.
- Compare instance methods, class methods, and module-level helper functions.
- Model successful and failed ingestion outcomes separately.
- Write tests that assert object behavior, not only object creation.
- Refactor scanner output into typed domain models.

## Project milestone
Introduce core ResearchOps models: `Paper`, `ParsedDocument`, `IngestionResult`, and `FailedDocument`, and use them as the shared language of the codebase.

## Files to modify/create
- `src/researchops/core/models.py`
- `src/researchops/core/exceptions.py`
- `src/researchops/core/value_objects.py`
- `tests/unit/test_models.py`
- `tests/unit/test_value_objects.py`
- `tests/fakes/fake_repository.py`

## Concepts covered
Classes, dataclasses, immutability trade-offs, composition, validation, representation methods, domain vocabulary, and value objects.

## Expected deliverables
- Domain models in `core/models.py` with clear field names and behaviour methods.
- Value objects in `core/value_objects.py` that enforce invariants at construction time.
- Exception hierarchy in `core/exceptions.py` with sub-classes for each failure domain.
- Fake repository implementation in `tests/fakes/fake_repository.py` for use in service tests.
- Tests covering normal construction, property methods, failure summaries, and invalid state.

## Definition of done
- [ ] `Paper` captures id, title, source path, text, page count, and file size.
- [ ] `ParsedDocument` captures raw parser output before persistence.
- [ ] `FailedDocument` captures why a document could not be ingested.
- [ ] `IngestionResult` aggregates successes, failures, and skipped paths.
- [ ] `PaperId.from_path()` produces a stable 16-character hex ID.
- [ ] `Query` value object rejects empty queries.
- [ ] `Tag` value object normalises to lowercase-with-hyphens.
- [ ] Dataclasses are used for all models.
- [ ] Tests cover `word_count()`, `is_empty()`, `success_rate`, `summary()`.
- [ ] `pytest -q` passes.
