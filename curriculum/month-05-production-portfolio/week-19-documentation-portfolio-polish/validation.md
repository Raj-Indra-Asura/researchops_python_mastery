# Validation — Week 19 Documentation and Portfolio Polish

## 1. Pre-validation checklist

- [ ] The full suite passes and `ruff` is clean before you touch docs.
- [ ] Every command in the README has been run **exactly as written**.
- [ ] Architecture docs and diagrams match the code as it actually is.
- [ ] `docs/demo.md` has been followed step by step from a clean state.

## 2. Exact commands

```bash
# Fresh-clone test (simulates a stranger using your repo)
cd /tmp
rm -rf fresh_test
git clone <your-repo-url> fresh_test
cd fresh_test
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
researchops --help

# Quality still green
pytest
ruff check src tests
```

## 3. Expected behavior

- The README renders correctly on GitHub (code blocks, tables, Mermaid diagrams).
- A fresh clone installs and `researchops --help` works with no extra steps.
- Following `docs/demo.md` produces the documented output.

## 4. Tests that must pass

- `pytest` (whole suite) in the fresh clone.
- Every documented command runs successfully (the docs are themselves a test).

## 5. Manual checks

- Open the README on GitHub; confirm images, tables, and Mermaid diagrams render.
- Walk `docs/demo.md` line by line; fix anything that does not match reality.
- Read the architecture docs against the code; reconcile any contradiction.

## 6. Architecture checks

- Diagrams reflect the real module dependencies (no arrows the code does not
  have).
- Documented data flows (ingest, search, RAG) match the implemented flows.

## 7. Documentation checks

- README, architecture docs, and `docs/demo.md` are accurate and current.
- `docs/retrospective.md` is written honestly.
- Every README command has been executed and verified this week.

## 8. Do-not-proceed warnings

**Do not proceed to Week 20 if:**

- **README commands are not tested** — untested setup instructions are how fresh
  clones fail for everyone but you.
- **Architecture docs contradict the code** — the docs must describe what exists,
  not what you intended.

## 9. Ruthless mentor checkpoint

- "On a fresh clone, did `pip install -e` + `researchops --help` work with no
  undocumented steps?"
- "Point at one architecture diagram and the code it describes. Do they agree?"
- "Did you actually run every README command this week, or assume they still
  work?"

## 10. Definition of done

- [ ] README renders correctly on GitHub.
- [ ] Mermaid diagrams render and match the code.
- [ ] `docs/demo.md` produces correct output when followed.
- [ ] Fresh clone + install + `researchops --help` works.
- [ ] `pytest` passes and `ruff` is clean in a fresh clone.
- [ ] `docs/retrospective.md` is written and honest.
- [ ] Every documented command has been verified.
