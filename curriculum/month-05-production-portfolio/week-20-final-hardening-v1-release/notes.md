# Week 20 Notes: Final Hardening and v1.0 Release

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › [Week 20 — Final Hardening & v1.0 Release](./README.md) › **notes.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## What "done" actually means

There is no perfect software. "Done" for a v1.0 release means:

1. The stated requirements are met.
2. The tests pass.
3. The documentation is accurate.
4. The project can be demonstrated end-to-end.
5. You can talk about it confidently.

None of these say "all possible features are built" or "all edge cases are handled". Software is never complete. "Done" is a decision, not a state.

The most common failure mode for side projects is **infinite polish**. This is the loop where you never release because there is always one more thing to fix or add. Breaking this loop requires explicitly deciding that the current state is version 1.0 and committing to that decision.

The discipline of finishing is as important as the discipline of building. Employers care whether you can ship, not just whether you can code.

---

## Why not to add features forever

Every new feature added to an unreleased project:
- Increases the scope of what must be tested before release.
- Introduces new bugs that delay release further.
- Makes the codebase harder to understand in an interview.
- Dilutes your portfolio story (if it does five things adequately, it does none of them memorably).

The right time to stop adding features to v1.0 is when the core feature set is complete and working. All future features belong in v1.1 or later.

Before finalising v1.0, write down everything you want to add. Then move every item to a `ROADMAP.md` entry labelled v1.1 or later. This is not giving up. It is scope management, which is a professional skill.

---

## Release

A **release** is a named, versioned snapshot of your software that has been tested and documented. It is a statement: "This version, at this point in time, is intentionally made available."

For an open-source project on GitHub, a release consists of:
1. A version number (e.g., `1.0.0`).
2. A git tag pointing to the release commit.
3. A GitHub Release (on the Releases page) with release notes.
4. An updated changelog.

The act of creating a release forces you to:
- Verify the version number is correct everywhere.
- Write release notes that explain what changed.
- Confirm the tests pass one final time.
- Make a public statement that this version works.

---

## Version

A **version number** is a label that identifies a specific state of the software. The standard format is `MAJOR.MINOR.PATCH`, known as **semantic versioning** (SemVer).

- **MAJOR**: incremented when you make a breaking change. Existing users must update their code to use the new version.
- **MINOR**: incremented when you add new functionality in a backward-compatible way. Existing users do not need to change anything.
- **PATCH**: incremented when you fix bugs without adding new functionality. Always backward-compatible.

For v1.0.0:
- This is the first intentional public release.
- There is no previous version to break compatibility with.
- All previous versions were development versions (0.x.x).

Version numbers must be consistent across three places:
1. `pyproject.toml`: `version = "1.0.0"`
2. `src/researchops/__init__.py`: `__version__ = "1.0.0"`
3. `CHANGELOG.md`: `[1.0.0] — YYYY-MM-DD`

If any of these are out of sync, the release is incomplete.

---

## Changelog

A **changelog** is a human-readable file that lists what changed between versions. It is written for users, not for Git.

The standard format (keepachangelog.com):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.0.0] — 2026-06-09

### Added
- RAG assistant with grounded Q&A and citations (Week 17)
- Docker packaging and environment configuration (Week 18)
- Complete documentation and portfolio polish (Week 19)
- v1.0.0 release with pre-release checklist (Week 20)

### Changed
- Settings module refactored to use pydantic-settings

### Fixed
- Vector index returns insufficient-evidence response when no relevant chunks found

## [0.9.0] — 2026-05-12

### Added
- FastAPI REST layer (Week 14)
- Async ingestion pipeline (Week 15)
- Background job runner (Week 16)
```

The changelog should not duplicate commit messages. Commit messages are for developers. The changelog is for users. Describe what changed from the user's perspective, not how you implemented it.

---

## Release notes

**Release notes** are a summary of the changes in a specific release, written for the GitHub Releases page. They are shorter than the full changelog and focus on the most important changes.

Template:

```markdown
## ResearchOps v1.0.0

This is the first production-ready release of ResearchOps.

### What's included

- **RAG assistant**: ask questions about your research papers and receive
  grounded answers with citations.
- **Docker packaging**: run the app, API, and worker in containers with
  docker compose.
- **Complete documentation**: README, architecture diagrams, demo script,
  and retrospective.

### How to install

\```bash
pip install researchops==1.0.0
\```

Or clone the repository:

\```bash
git clone https://github.com/YOUR_USERNAME/researchops_python_mastery.git
cd researchops_python_mastery
pip install -e ".[all]"
\```

### Known limitations

See README.md for the full list of known limitations.
```

---

## Regression testing

A **regression** is a bug that was fixed in a previous version but reappears in a later version. The name comes from the idea of going backward (regressing) in quality.

**Regression testing** is running the full test suite before a release to ensure that previously working behaviour still works.

For v1.0.0, run:

```bash
pytest --cov=researchops --cov-report=term-missing -q
ruff check src tests
```

If any test fails that was passing before, that is a regression. Fix it before releasing. Do not adjust the tests to make them pass if the underlying code is wrong.

The purpose of the test suite is exactly this moment: to give you confidence that v1.0.0 works. If you have been maintaining tests throughout Weeks 1–20, this step is fast and reassuring.

---

## Final validation

Final validation is a structured, manual walkthrough of every major feature. It is not a substitute for automated tests, but a complement. Automated tests catch regressions; manual validation catches integration issues that are hard to automate.

Final validation flow for ResearchOps:

```
1. Start from a fresh clone (no .venv, no data/).
2. pip install -e ".[all]"
3. researchops --help                        → shows all commands
4. researchops ingest ./examples/sample_papers → ingests 3 papers
5. researchops search "attention mechanism"  → returns ranked results
6. researchops ask "what is attention?"      → returns answer with citations
7. uvicorn researchops.api.main:app &        → API starts
8. curl http://localhost:8000/papers         → returns paper list
9. docker build -t researchops:local .       → image builds
10. docker compose up api -d                 → API starts in container
11. curl http://localhost:8000/papers        → returns paper list
12. docker compose down                      → containers stop cleanly
```

Each step has an expected result. If any step fails, fix the code or documentation before tagging the release.

---

## Known limitations section

Write a `## Known Limitations` section in the README. This is mandatory for a production-grade project. Not because it makes the project look bad, but because:

1. It shows engineering maturity. Engineers who know their system's limits are trustworthy.
2. It prevents users from hitting a surprise failure that was known.
3. It gives you a clear v1.1 roadmap.

Known limitations for ResearchOps v1.0.0 (adapt to your actual state):

- In-memory vector index not persisted: rebuilds on every start.
- No authentication on the API.
- PDF parsing may fail on scanned or complex-layout PDFs.
- Single-user: concurrent writes to SQLite may produce errors.
- Fake generator is the default: real generation requires Ollama or an API key.

---

## Future roadmap

The roadmap distinguishes what you committed to in v1.0.0 from what you plan for future versions. A `ROADMAP.md` file in the repository root should list:

- ✅ Completed features (with week references)
- 🔜 v1.1 planned features
- 💡 v2.0 ideas (speculative)

Example v1.1 roadmap items:
- Persist vector index to SQLite
- Streaming API endpoint for RAG responses
- Hybrid search (keyword + semantic) with score fusion
- Authentication layer for the API
- OpenAI-compatible provider configuration

---

## Retrospective

A **retrospective** is a structured reflection on a completed project. It is not a performance review. It is a learning exercise.

Five honest questions:

1. **What did I build?** Be specific. List every major feature that actually works.

2. **What did I learn that I did not expect to learn?** This is usually something about tradeoffs, not about syntax.

3. **What would I do differently?** Pick one real thing. The best retrospectives are uncomfortable.

4. **What was hardest?** Not what was most complex, but what cost you the most time or caused the most doubt.

5. **What am I most proud of?** At least one thing should make you proud. If nothing does, the retrospective is not done.

6. **What would v1.1 look like?** What would you build next?

The retrospective in `docs/retrospective.md` is for you. Write it honestly. You will read it again in six months and be glad you did.

---

## Portfolio handoff

After tagging v1.0.0, the project is portfolio-ready. To hand it off to your portfolio:

1. **Pin the repository** on your GitHub profile.
2. **Update your LinkedIn** with a description of the project and a link.
3. **Add it to your CV/resume** in the Projects section with a one-sentence description and a link.
4. **Prepare the demo** from `docs/demo.md`. Practice it until it takes under two minutes.
5. **Prepare the verbal story** (two to three minutes): problem, solution, what you learned.

When someone asks "walk me through your portfolio", ResearchOps should be the first thing you mention. You have 20 weeks of work behind it. You can answer every technical question about it. You built every part of it yourself. That is rare and valuable.

---

## How to decide if the project is done

Use this decision tree before tagging:

```
Does pytest pass with 0 failures?
  No → Fix failing tests first.
  Yes → continue.

Does ruff check src tests pass with 0 errors?
  No → Fix lint errors first.
  Yes → continue.

Does the demo script in docs/demo.md run end-to-end without errors?
  No → Fix the broken commands or update the expected output.
  Yes → continue.

Is the README accurate for the current state of the code?
  No → Update the README.
  Yes → continue.

Is the CHANGELOG up to date with a [1.0.0] section?
  No → Write the changelog entry.
  Yes → continue.

Is the version number 1.0.0 in pyproject.toml and __init__.py?
  No → Bump the version.
  Yes → continue.

TAG THE RELEASE.
```

If you complete this checklist and everything passes, the project is done. Do not add more features. Tag the release.

---

## Release checklist (copy to use)

Copy this checklist to your final commit message or a temporary file:

```
Code quality:
[ ] pytest passes: 0 failures, 0 errors
[ ] ruff check src tests: 0 errors
[ ] No hard-coded paths or credentials in source
[ ] No .env file committed

Functionality:
[ ] researchops --help works
[ ] researchops ingest ./examples/sample_papers works
[ ] researchops search "query" works
[ ] researchops ask "question" works
[ ] FastAPI server starts and responds
[ ] Docker image builds

Documentation:
[ ] README is accurate for the current code
[ ] Quick Start section works from a fresh clone
[ ] ARCHITECTURE.md matches current code
[ ] docs/demo.md produces correct output
[ ] Known limitations section is present and honest
[ ] Future work section is present

Release:
[ ] Version is 1.0.0 in pyproject.toml
[ ] Version is 1.0.0 in src/researchops/__init__.py
[ ] CHANGELOG.md has [1.0.0] section with today's date
[ ] git tag -a v1.0.0 -m "ResearchOps v1.0.0" created
[ ] git push --tags completed
[ ] GitHub Release created with release notes
```

---

## How to create a git release tag

```bash
# Commit all changes
git add .
git commit -m "v1.0.0: final release"

# Create an annotated tag
git tag -a v1.0.0 -m "ResearchOps v1.0.0 — 20-week build complete"

# Push the tag to GitHub
git push origin v1.0.0

# On GitHub: go to Releases → Draft a new release → choose tag v1.0.0
# Fill in the title and release notes from the template above
# Click "Publish release"
```

An **annotated tag** (created with `-a`) stores metadata: the tagger, the date, and a message. It is different from a lightweight tag (created with just `git tag v1.0.0`). For releases, always use annotated tags.

---

## What to say in a portfolio interview

**When asked "tell me about this project"**:

Open with the problem, not the technology. "I built a tool that lets researchers search and ask questions about their paper collections using retrieval-augmented generation." Then describe the pipeline briefly. Then mention one specific technical decision you made and why.

**When asked "how does the RAG pipeline work"**:

Walk through the 7 steps. Use the diagram. Emphasise that retrieval quality determines answer quality. Mention the fake generator and why it was the right choice for tests.

**When asked "what would you improve"**:

Use your known limitations list. Choose one that demonstrates systems thinking, not just more features. "I would persist the vector index to SQLite so users do not have to re-index on every startup. The challenge is updating specific chunks without invalidating the whole index."

**When asked "how did you ensure quality"**:

"I wrote unit tests for each component using dependency injection and fakes, so tests run in milliseconds without external dependencies. I added a CI pipeline that runs ruff and pytest on every push. Before the v1.0 release, I ran a final validation checklist end-to-end from a fresh clone."

**When asked "how long did this take"**:

"Twenty weeks, roughly five to ten hours per week. Each week built on the previous one: storage before search, search before RAG, RAG before packaging. The structured progression helped because I was never building on an unstable foundation."

---

## Summary

- "Done" is a decision, not a state. Make it explicitly.
- Infinite polish is the enemy of shipping. List future features in the roadmap and leave them there.
- A release is a named, tested, documented snapshot. v1.0.0 is the first public commitment.
- Semantic versioning: MAJOR breaks, MINOR adds, PATCH fixes.
- A changelog is for users. Commit messages are for developers.
- Regression testing is running the full test suite before tagging.
- Final validation is a manual end-to-end walkthrough from a fresh clone.
- Known limitations demonstrate engineering maturity, not weakness.
- A retrospective is a gift to future you.
- Portfolio handoff requires: a working demo, a verbal story, and confidence.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 20 — Final Hardening & v1.0 Release** · *notes.md — the textbook chapter* (step 2 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [README](./README.md)
- ▶ **Next:** [exercises.md](./exercises.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. **➡ [notes.md](./notes.md) ← you are here**
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
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
