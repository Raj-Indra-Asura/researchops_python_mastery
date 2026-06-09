# GitHub Copilot Instructions for ResearchOps

This repository is a 20-week Python mastery curriculum built around a production-style
research paper processing platform called ResearchOps.

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
