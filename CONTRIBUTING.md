# Contributing to ResearchOps

This document describes the self-study conventions for this project.
Since this is a personal learning repository, "contributing" means
following your own weekly discipline.

---

## Weekly workflow

```
Week N:
1. Read curriculum/month-XX/week-NN-*/notes.md
2. Do curriculum/month-XX/week-NN-*/exercises.md (warm-ups first)
3. Implement the deliverables listed in the week README
4. Run the commands in validation.md — all must pass
5. Run pytest — all tests must pass
6. Fill in reflection.md
7. Commit: git commit -m "week-NN: <short description>"
8. Push: git push
```

---

## Commit message conventions

```
week-01: add scan command
week-02: add custom exceptions and logging setup
week-05: implement SQLite paper repository
fix: handle empty PDF gracefully in parser
docs: update week-06 validation.md with ingest command
```

Format: `<type>: <short description>` where type is one of:
- `week-NN` — weekly deliverable
- `fix` — bug fix
- `docs` — documentation only
- `test` — test-only change
- `refactor` — code change without behaviour change

---

## Code style

- All code formatted and linted with `ruff`
- Type hints on all public functions and methods
- Test coverage ≥ 70% (enforced in CI after Week 10)
- No bare `except:` — always catch a specific exception type
- No print statements in production code — use `logging`

---

## Import rules

See ARCHITECTURE.md. Summary:
- `core/` imports nothing from within `researchops/`
- `services/` imports from `core/` only (not infrastructure)
- CLI/API/workers wire infrastructure to services

---

## Running the project locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
researchops --help
pytest
ruff check src tests
```
