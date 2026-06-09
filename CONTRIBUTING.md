# Contributing to ResearchOps

This is a personal learning repository. "Contributing" means following your own weekly discipline. This document is your workflow manual.

---

## Weekly Workflow

Every week, in this order:

```
1. Create a branch
   git checkout -b week-NN-short-description

2. Read the week's README.md
   curriculum/month-XX/week-NN-NAME/README.md

3. Read notes.md slowly
   curriculum/month-XX/week-NN-NAME/notes.md
   (Do not skim. Annotate. Ask yourself questions.)

4. Do exercises.md
   curriculum/month-XX/week-NN-NAME/exercises.md
   (Do all warm-ups and implementation exercises.)

5. Implement the week's deliverable
   (Write tests first or alongside — not after.)

6. Run validation.md
   (Every command. Every expected output. No shortcuts.)

7. Run CI checks locally
   pytest --cov=researchops --cov-report=term-missing -q
   ruff check src tests

8. Fill in reflection.md
   curriculum/month-XX/week-NN-NAME/reflection.md
   (Your words only. No AI assistance.)

9. Commit and push
   git add -A
   git commit -m "week-NN: <what you built>"
   git push origin week-NN-short-description
```

---

## Branch Names

Branch names follow this convention:

```
week-NN-short-description
```

Examples:
```
week-01-foundations
week-05-sqlite-storage
week-09-protocols-clean-arch
week-13-embeddings-semantic-search
```

For bug fixes not tied to a specific week:
```
fix-empty-pdf-handling
fix-test-coverage-regression
```

For documentation updates:
```
docs-update-architecture
docs-week-07-validation
```

---

## Commit Messages

Format: `<type>: <short description>`

```
week-01: add scan command and find_pdfs utility
week-02: add custom exceptions and structured logging
week-05: implement SqlitePaperRepository
week-09: add typing.Protocol interfaces and fake repos
week-11: add TF-IDF classifier and CLI train command
fix: handle empty PDF pages in text_cleaner
fix: guard against None title in metadata_extractor
docs: update week-06 validation.md with ingest command
test: add parametrised tests for paper service
refactor: extract ingestion pipeline into IngestionService
```

**Rules:**
- Type must be one of: `week-NN`, `fix`, `docs`, `test`, `refactor`
- Description is present tense, lowercase, no period
- Description must describe what changed, not how
- Maximum 72 characters for the first line
- One concern per commit — do not mix feature work and refactors

---

## Testing Routine

Run after every change, before every commit:

```bash
# Quick: run only the tests related to what you changed
pytest tests/unit/test_MODULE.py -v

# Full: run everything with coverage
pytest --cov=researchops --cov-report=term-missing -q

# Lint: must be zero errors
ruff check src tests
```

**Rules:**
- Never commit if `pytest` fails
- Never commit if `ruff check` reports errors
- Coverage must not drop below 70% (CI will fail if it does)
- Write tests for every new function, class, or service you add
- Unit tests must not touch the filesystem, network, or real database
- Integration tests may use `tmp_path` for a real SQLite database
- Use fakes from `tests/fakes/` in unit tests — not mock libraries

### Test file naming

Mirror the source file path:

| Source file | Test file |
|-------------|-----------|
| `src/researchops/services/search_service.py` | `tests/unit/test_search_service.py` |
| `src/researchops/storage/sqlite_repository.py` | `tests/integration/test_sqlite_repository.py` |
| `src/researchops/cli/main.py` | `tests/e2e/test_cli.py` |

---

## Documentation Routine

When you change behaviour, update documentation:

| What changed | What to update |
|-------------|----------------|
| CLI command output | `curriculum/month-XX/week-NN/validation.md` |
| Service interface | `curriculum/month-XX/week-NN/notes.md` |
| New module added | `ARCHITECTURE.md` module responsibilities section |
| New CLI command | `PROJECT_SPEC.md` CLI command reference |
| New API endpoint | `PROJECT_SPEC.md` API endpoint reference |
| Bug fix or feature | `CHANGELOG.md` unreleased section |

---

## Code Review Checklist

Before marking any week complete, ask yourself:

**Correctness**
- [ ] The deliverable described in the week README is implemented
- [ ] All commands in validation.md produce the expected output
- [ ] All tests pass: `pytest -q`
- [ ] Lint is clean: `ruff check src tests`
- [ ] Coverage has not dropped: `pytest --cov=researchops -q`

**Architecture**
- [ ] No service imports from infrastructure (`storage/`, `parsing/`, `ml/`, `search/`)
- [ ] No business logic in CLI commands or API routes
- [ ] `core/` has no imports from other researchops modules
- [ ] New protocols are in `core/interfaces.py`
- [ ] New fake implementations are in `tests/fakes/`

**Code quality**
- [ ] All public functions and methods have type hints
- [ ] No bare `except:` — always catch a specific exception type
- [ ] No `print()` in production code — use `logging`
- [ ] Variable names are descriptive, not abbreviated
- [ ] Comments explain *why*, not *what*

**Tests**
- [ ] Every new function has at least one test
- [ ] Unit tests use fakes, not real infrastructure
- [ ] Integration tests use `tmp_path`, not hard-coded paths
- [ ] E2E tests use `CliRunner` or `httpx.TestClient`

**Documentation**
- [ ] `reflection.md` is filled in, in your own words
- [ ] `validation.md` commands still produce the expected output
- [ ] If behaviour changed, documentation was updated

---

## ⚠️ Do Not Let Copilot Skip Your Learning

AI coding assistants are a tool. Used well, they accelerate your learning. Used badly, they replace it.

**What happens if you let Copilot do your week:**
- You get code that works but that you cannot explain
- You cannot answer "why did you structure it this way?" in an interview
- You skip the bugs that teach you the most
- Your `reflection.md` is empty or parroted from documentation
- You reach Week 17 not knowing why anything in Weeks 1–16 was built the way it was

**The discipline test:** after completing any week, close your laptop and explain — out loud, in plain English — what you built and why. If you cannot do this, you did not learn the week. Go back.

**Permitted uses of AI:**
- "I read this error message carefully and I think it means X. Is that right?"
- "I've written this code. What edge cases am I missing?"
- "I understand TF-IDF conceptually but I'm confused about this specific line. Can you explain it?"
- "I've implemented this. Is there a more idiomatic way to do it in Python?"

**Prohibited uses of AI:**
- "Write the Week 11 implementation for me"
- "Generate my reflection.md"
- "What should I build this week?" (the curriculum already tells you)
- "Explain how TF-IDF works" (the notes.md already does this)
- "Write tests for my code" (you must write tests first or alongside)

---

## Code Style Reference

- Format and lint: `ruff` (configured in `pyproject.toml`)
- Line length: 88 characters
- Type hints: required on all public functions and methods
- String style: double quotes (ruff enforces)
- Import order: `ruff` `isort` rules (`I` ruleset)
- No `print()` in production code — use `logging`
- No bare `except:` — always name the exception type
- No mutable default arguments (`def f(items=[])` is wrong)

---

## Running the Project Locally

```bash
# Initial setup
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e ".[dev]"

# Verify
researchops --help
pytest -q
ruff check src tests

# With optional dependencies
pip install -e ".[parsing]"      # adds pypdf
pip install -e ".[ml]"           # adds scikit-learn
pip install -e ".[api]"          # adds fastapi + httpx
pip install -e ".[all]"          # adds everything
```
