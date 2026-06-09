# GitHub Copilot Instructions for ResearchOps

This repository is a **self-contained 20-week Python mastery textbook, guided lab, and
project workbook** built around a production-style research paper processing platform
called ResearchOps.

## Curriculum philosophy — READ THIS FIRST

This is a **book-like learning system**, not a project roadmap.

Each week is a full chapter. The learner starts knowing only Python basics and reaches
production ML-engineering skills by week 20. The curriculum must be self-contained:
the learner must not need outside resources for the core material.

### Required depth for every weekly file

| File | Purpose | Target depth |
|---|---|---|
| `README.md` | Chapter roadmap | Full chapter overview with study plan |
| `notes.md` | Textbook chapter | 800–1500+ lines, beginner explanations + code walkthroughs |
| `exercises.md` | Workbook | Warm-up → implementation → stretch → brutal tasks |
| `break_it.md` | Failure/debugging lab | Intentional breaks with expected errors and recovery |
| `validation.md` | Strict completion checkpoint | Exact commands + expected outputs |
| `reflection.md` | Guided self-review | Prompts only, no answers |

### Required sections for every notes.md

1. Chapter overview
2. What you already know from previous weeks
3. What problem this week solves
4. Beginner mental model
5. Core vocabulary
6. Concept explanations from first principles
7. ResearchOps-specific application
8. Code examples with line-by-line explanation
9. Common beginner mistakes
10. Debugging guidance
11. Design tradeoffs
12. Testing implications
13. Architecture implications
14. How this connects to AI engineering / ML research
15. Mini quizzes
16. Explain-it-aloud prompts
17. What to memorize
18. What to understand deeply
19. What not to worry about yet
20. Bridge to next week

### Required sections for every exercises.md

1. How to use this workbook
2. Warm-up exercises
3. Code-reading exercises
4. Implementation exercises
5. Testing exercises
6. Debugging exercises
7. Refactoring exercises (where relevant)
8. Written explanation exercises
9. Stretch exercises
10. Brutal exercises
11. Mini project task
12. Completion checklist

### Required sections for every break_it.md

1. Purpose of failure practice
2. Failure lab rules
3. Intentional break experiments (each with: how to cause it, expected error, how to inspect, how to fix, test that should catch it, what this teaches, common wrong fixes)
4. Debugging checklist
5. Reflection after breaking

### Required sections for every validation.md

1. Pre-validation checklist
2. Commands to run
3. Expected outputs
4. Tests that must pass
5. Manual checks
6. Architecture checks
7. Documentation checks
8. Do-not-proceed warnings
9. Ruthless mentor checkpoint
10. Definition of done

### Required sections for every reflection.md

Prompts only — no answers, no examples. Must include prompts for:
- what I built / what I learned / what broke / what I misunderstood
- how I fixed it / what tests helped / what tests were missing
- what I overengineered / what I underengineered
- what I can explain aloud / what still feels weak
- confidence score / whether I am allowed to move forward

---

## Architecture boundaries — NEVER violate these

1. **`core/`** must not import from `cli/`, `api/`, `storage/`, `ml/`, `workers/`, or `search/`.
   Core contains only: models, exceptions, interfaces (protocols), and value objects.

2. **`services/`** depends on `core/` protocols (interfaces), not concrete implementations.
   Services must never import `sqlite_repository`, `pdf_parser`, or `fastapi` directly.

3. **`cli/`** and `api/`** wire concrete implementations to service protocols.
   CLI/API must not contain business logic — delegate everything to services.

4. **`storage/`**, **`parsing/`**, **`ml/`**, **`search/`** are infrastructure layers.
   They implement core protocols and may import third-party libraries.

5. **No CPU-heavy work inside asyncio event loops.**
   PDF parsing and ML inference belong in `ProcessPoolExecutor` (workers/process_pool.py).
   `async`/`await` is for I/O-bound operations only (HTTP, file I/O).

6. **No Docker before local CLI works.**
   No FastAPI before the CLI/service layer works.
   No RAG before keyword and semantic search work.

## Code quality rules

- **Add tests for every new feature.** No feature without at least one unit test.
- **Prefer small, incremental changes.** One concern per commit.
- **Update weekly curriculum files** when code behaviour changes.
  - If you change a CLI command, update the relevant `validation.md`.
  - If you change a service interface, update `notes.md` for the relevant week.
- **Update `validation.md` commands** when expected CLI output changes.
- **Never introduce unrequested heavy dependencies.** Ask first.
  - Do not add `torch`, `transformers`, `sentence-transformers` before Week 13.
  - Do not add `openai`, `langchain`, `llama-index` before Week 17.
- **Keep code beginner-readable but production-respectful.**
  - Use type hints everywhere.
  - Prefer descriptive variable names over clever one-liners.
  - Add comments only when the *why* is not obvious from the code.
- **Explain tradeoffs in comments only when useful.**
  - "Why ProcessPoolExecutor and not ThreadPoolExecutor?" — useful comment.
  - "This increments i" — useless comment.

## Testing conventions

- Test file naming: `test_<module>.py` mirrors `src/researchops/<module>.py`.
- Use `pytest` fixtures, `tmp_path`, and `monkeypatch` — never hard-coded paths.
- Fake implementations live in `tests/fakes/` and implement core protocols.
- Unit tests must not touch the filesystem, network, or real database.
- Integration tests may use `tmp_path` for a real SQLite DB.
- E2E tests use `typer.testing.CliRunner` or `httpx.AsyncClient` for the API.

## Dependency direction (import graph)

```
CLI / API / Worker
    ↓ imports
Services / Use Cases
    ↓ imports
Core Models + Protocols
    ↑ implemented by
Infrastructure (storage, parsing, ml, search)
```

## Current project status (update this as weeks complete)

- [x] Week 1: repo scaffold, core models, CLI scaffold, scan command
- [ ] Week 2: files, pathlib, exceptions, logging
- [ ] Week 3: OOP, dataclasses, domain modeling (already partly done in Week 1)
- [ ] Week 4: CLI packaging, entry points
- [ ] Week 5–20: see ROADMAP.md

## Key files to read before making changes

- `ARCHITECTURE.md` — dependency rules, modular monolith rationale
- `PROJECT_SPEC.md` — full feature specification
- `src/researchops/core/interfaces.py` — all protocol definitions
- `src/researchops/core/models.py` — all domain models
- `pyproject.toml` — dependency groups, entry points
