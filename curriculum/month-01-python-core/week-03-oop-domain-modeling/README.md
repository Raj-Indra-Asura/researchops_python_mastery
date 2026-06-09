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
- `src/researchops/models.py`
- `src/researchops/ingestion/types.py`
- `tests/unit/test_models.py`
- `tests/unit/test_ingestion_result.py`
- `tests/fakes/factory.py`

## Concepts covered
Classes, dataclasses, immutability trade-offs, composition, validation, representation methods, and domain vocabulary.

## Expected deliverables
- Domain models with clear field names.
- Constructors or factory helpers that enforce basic validity.
- Tests covering normal, partial, and failed document cases.
- Refactored code that passes models instead of loose dictionaries where possible.

## Definition of done
- [ ] `Paper` captures source metadata.
- [ ] `ParsedDocument` captures extracted content.
- [ ] `FailedDocument` captures why parsing failed.
- [ ] `IngestionResult` aggregates outcomes cleanly.
- [ ] Dataclasses are used where helpful.
- [ ] Tests cover equality or representation behavior.
- [ ] Invalid state is blocked early.
- [ ] Names match the research domain.
- [ ] Existing code reads more clearly than last week.
