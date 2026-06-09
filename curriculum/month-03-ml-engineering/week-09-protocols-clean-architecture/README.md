# Week 09 - Protocols and Clean Architecture

## Learning objectives
- Use `typing.Protocol` to define behavior-based interfaces.
- Apply dependency inversion so services depend on abstractions, not concrete SQLite classes.
- Introduce fake repositories for fast tests.
- Separate domain, application, and infrastructure concerns.
- Recognize tight coupling and refactor it out.
- Make services easier to test and swap.
- Describe clean architecture in practical terms.

## Project milestone
Refactor ResearchOps so ingestion and search services depend on protocols and can run against fake or real repositories.

## Files to modify/create
- `src/researchops/ports.py`
- `src/researchops/services/ingestion.py`
- `src/researchops/services/search.py`
- `tests/fakes/fake_repository.py`
- `tests/unit/test_service_with_fake_repo.py`

## Concepts covered
Protocols, dependency inversion, clean boundaries, ports and adapters, fakes, and architecture refactoring.

## Expected deliverables
- Protocols for repositories or parsers.
- Services rewritten to accept abstractions.
- Fast tests that use fakes instead of SQLite.
- Clearer architecture boundaries.

## Definition of done
- [ ] At least one repository protocol exists.
- [ ] Services accept protocol-typed dependencies.
- [ ] Fake repositories support unit tests.
- [ ] Infrastructure code remains outside core services.
- [ ] Coupling to SQLite is reduced.
- [ ] Tests prove services work with fakes.
- [ ] You can explain dependency inversion with an example from this repo.
