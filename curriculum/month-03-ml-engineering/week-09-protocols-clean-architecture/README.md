<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 09 — Protocols and Clean Architecture:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 8 Reflection](../../month-02-data-storage-concurrency/week-08-multiprocessing-ingestion/reflection.md) · ➡️ [Notes →](notes.md)

**📐 Relevant Decisions:** [ADR-0001: Modular Monolith](../../../docs/decisions/0001-modular-monolith.md)

---
<!-- NAV_END -->

# Week 09 — Protocols, Interfaces, and Clean Architecture

## Theme

Month 2 gave you a working pipeline: scan → parse → store → search. Now you discover what happens as code grows: tangled dependencies, slow tests, and resistance to change. This week teaches you why that happens and how to fix it using Python protocols and clean architecture principles.

## Learning objectives

By the end of this week you will be able to:

- Explain coupling, dependency, and abstraction in plain language.
- Use `typing.Protocol` to define behavior-based interfaces without inheritance.
- Apply dependency inversion so services depend on abstractions, not concrete SQLite classes.
- Read and explain every line of `src/researchops/core/interfaces.py`.
- Write a fake repository that satisfies a protocol for use in unit tests.
- Distinguish service layer from infrastructure layer.
- Describe ports and adapters architecture using ResearchOps examples.
- Explain why dependency injection at the constructor is the right composition pattern.
- Know when an abstraction is useful versus overengineering.

## Project milestone

Understand how `IngestionService` and `KeywordSearchService` are already decoupled from SQLite, and practice extending that pattern by writing your own protocol, fake, and service test.

## Key source files to study

| File | What it teaches |
|---|---|
| `src/researchops/core/interfaces.py` | All protocol definitions for the project |
| `src/researchops/services/ingestion_service.py` | Service that depends only on protocols |
| `src/researchops/services/search_service.py` | Another example of protocol-dependent service |
| `tests/fakes/fake_repository.py` | Fake implementations for unit testing |
| `tests/unit/test_ingestion_service.py` | Full service test suite using fakes |
| `src/researchops/storage/sqlite_repository.py` | The real adapter that implements `PaperRepository` |
| `src/researchops/cli/commands/ingest.py` | The composition root that wires real implementations |

## Concepts covered

Coupling, dependency, concrete class, abstraction, interface, Python Protocol, structural subtyping, dependency inversion, dependency injection, constructor injection, fake, test double, ports and adapters, service layer, infrastructure layer, composition root, modular monolith, allowed imports, forbidden imports.

## Expected deliverables

- Written explanation of each protocol in `interfaces.py` in your own words.
- A new protocol you define yourself for a simple capability.
- A fake that satisfies your new protocol.
- A unit test that uses the fake — no database, no files.
- A diagram (drawn or described in words) of the dependency graph for `IngestionService`.

## Definition of done

- [ ] You can recite the dependency inversion principle from memory.
- [ ] You can explain why `IngestionService.__init__` takes `PaperRepository` instead of `SQLiteRepository`.
- [ ] You can write a fake repository from scratch without looking at the existing one.
- [ ] You understand what `@runtime_checkable` does and why it is on the protocols.
- [ ] You can identify which layer every source file in ResearchOps belongs to.
- [ ] You can explain what the CLI does that the services cannot.
- [ ] You can explain one scenario where these abstractions save work in Month 4 or 5.
- [ ] `pytest tests/unit/ -q` passes.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 8 Reflection](../../month-02-data-storage-concurrency/week-08-multiprocessing-ingestion/reflection.md) · ➡️ [Notes →](notes.md)

**📐 Relevant Decisions:** [ADR-0001: Modular Monolith](../../../docs/decisions/0001-modular-monolith.md)

**Week 09 — Protocols and Clean Architecture:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
