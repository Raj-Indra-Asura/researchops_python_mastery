# Week 20 Break-It: Final Testing and Release Discipline

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › [Week 20 — Final Hardening & v1.0 Release](./README.md) › **break_it.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Why break it in the final week?

In the final week, you run the same experiments that professional teams run before a major release. The difference between a hobby project and a production release is this: production releases fail safely and fail knowingly. You discover the failures before your users do.

---

## Experiment 1: The nuclear test

This is the most important experiment. Do it before tagging v1.0.0.

```bash
# Delete the virtual environment and all runtime data
rm -rf .venv data/

# Start completely fresh
cd /tmp
git clone <your-repo-url> nuclear_test
cd nuclear_test
python -m venv .venv
source .venv/bin/activate
pip install -e ".[all]"

# Run every CLI command
researchops --help
researchops ingest ./examples/sample_papers
researchops search "attention mechanism"
researchops ask "what is the main contribution of the attention paper?"
```

**What typically breaks**:
- A dependency that you have installed globally but not in `pyproject.toml`.
- A path that works on your machine but is not documented.
- An example file that is listed in the README but not in the repository.
- A required environment variable that has a default on your machine but not a documented default.

Fix every failure. The nuclear test is the gold standard for release readiness.

---

## Experiment 2: The CI simulation

Run exactly what CI runs — nothing more, nothing less:

```bash
pip install -e ".[dev]"
ruff check src tests
pytest --cov=researchops --cov-report=term-missing -q
```

**What to look for**: any failure that CI would catch but you have been ignoring locally. A test that passes on your machine but might fail on a clean machine due to environment differences.

If CI is currently failing on GitHub, check the workflow logs with:

```bash
# Get the most recent workflow run
# (use the GitHub Actions UI or gh CLI)
gh run list --limit 5
gh run view <run-id> --log-failed
```

Fix every CI failure before tagging.

---

## Experiment 3: The edge case tour

Run every CLI command with bad input. For each, record: does it produce a useful error message, or does it crash with a traceback?

```bash
researchops scan /nonexistent
researchops search ""
researchops ask ""
researchops ingest /dev/null
```

**Standard**: a command that receives bad input should print a clear, human-readable error message and exit with a non-zero exit code. It should never print a Python traceback to a non-developer user.

Fix any command that produces a raw exception traceback on invalid input.

---

## Experiment 4: Release checklist failure

Go through the release checklist from notes.md. For each item, deliberately skip it, then observe what breaks:

**Skip the changelog update**: tag the release without updating `CHANGELOG.md`. Now look at the GitHub Releases page. There are no release notes. An interested developer has no way to know what changed.

**Skip the version bump in `__init__.py`**: keep `pyproject.toml` at 1.0.0 but leave `__init__.py` at 0.9.0. Run `python -c "import researchops; print(researchops.__version__)"`. The output is 0.9.0, not 1.0.0. Any code that checks the version will report the wrong version.

**Skip the version bump in `pyproject.toml`**: install the package in a new environment. `pip show researchops` will report the old version.

**Lesson**: each checklist item exists because a specific silent failure occurs if you skip it. The checklist is not bureaucracy. It is accumulated experience.

---

## Experiment 5: Fresh clone failure

Ask a friend or family member to clone your repository and follow the README Quick Start. Do not help them. Watch what happens.

If no one is available, do this yourself in an incognito environment or a VM.

**What to look for**:
- The first command in the Quick Start that does not work.
- Any step they skip because it is unclear.
- Any assumption in the documentation that is not documented.

Every failure is a documentation bug or a missing default. Fix it.

---

## Experiment 6: README contradiction test

Read the README and the code simultaneously. Find three places where the README describes something that no longer matches the code. Examples:
- A module path mentioned in the README that was renamed.
- A feature listed in the Features section that is not yet implemented.
- An example command that produces a different output than shown.
- A version number that is inconsistent between README and code.

Fix all contradictions before tagging.

---

## Experiment 7: Scope creep test

During Week 20, you will have ideas for improvements. They will feel urgent. List every improvement idea you have during the week on paper. At the end of the week, look at the list. For each idea:

- Would it take more than 30 minutes?
- Would it require changing any test?
- Would it add a new dependency?

If any answer is yes: this is a v1.1 item. Add it to `ROADMAP.md`. Do not implement it.

The discipline of not implementing features during a release week is the discipline of shipping.

---

## Debugging commands for final week

```bash
# Run specific test file
pytest tests/unit/test_settings.py -v

# Run tests with verbose output
pytest -v --tb=short

# Check coverage for specific module
pytest --cov=researchops.rag --cov-report=term-missing

# Check ruff for specific file
ruff check src/researchops/rag/assistant.py

# Verify CLI entry points
pip show researchops

# Check installed version
python -c "import researchops; print(researchops.__version__)"

# Verify git tag exists
git tag -l "v1.0.0"

# Verify tag is pushed
git ls-remote --tags origin
```

---

## What did you learn?

Answer these in your final `reflection.md`:

1. What broke in the nuclear test that you did not expect?
2. Which edge case produced the worst error message? What did you fix?
3. How long did it take to complete the full pre-release checklist?
4. What is the one thing you would not skip on a future release, having now experienced the consequence of skipping it?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 20 — Final Hardening & v1.0 Release** · *break_it.md — the failure lab* (step 4 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [exercises.md](./exercises.md)
- ▶ **Next:** [validation.md](./validation.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. **➡ [break_it.md](./break_it.md) ← you are here**
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. 🎉 You have reached the final week — see the [Release Checklist](../../../RELEASE_CHECKLIST.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Finish: Release Checklist](../../../RELEASE_CHECKLIST.md) and the [portfolio outcome](../../../README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 5 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 5 overview](../README.md) · [📄 Week 20 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
