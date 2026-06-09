# Week 09 — Protocols, Interfaces, and Clean Architecture

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › **Week 9 — Protocols & Clean Architecture**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 9 — Protocols & Clean Architecture** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 8 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 10](../../../curriculum/month-03-ml-engineering/week-10-testing-quality-gates/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 10 — Testing & Quality Gates](../../../curriculum/month-03-ml-engineering/week-10-testing-quality-gates/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 9 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
