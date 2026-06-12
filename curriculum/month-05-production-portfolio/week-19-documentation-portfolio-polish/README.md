<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 19 — Documentation and Portfolio Polish:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 18 Reflection](../week-18-docker-environment-config/reflection.md) · ➡️ [Notes →](notes.md)

---
<!-- NAV_END -->

# Week 19: Documentation and Portfolio Polish

## 1. Story of the week

ResearchOps works. It ingests papers, searches them three different ways, answers questions with citations, serves an API, runs background jobs, and ships in a container. Nineteen weeks of engineering — and right now, every bit of it is invisible to anyone who is not you.

This week you build the layer that makes the work *legible*: docstrings the tooling can read, diagrams the code can verify, a README a recruiter can skim in 30 seconds and an engineer can trust in ten minutes, a demo script that cannot fail in an interview, and a retrospective that turns nineteen weeks of effort into a portfolio story. No new runtime behaviour ships this week. What ships is the difference between "a repo I made" and "a project I can hand to anyone".

## 2. What you already know

- The complete system you are documenting: models and CLI (Weeks 1–4), storage and pipelines (Weeks 5–8), protocols and testing (Weeks 9–10), ML and tracking (Weeks 11–12), embeddings, API, async, workers (Weeks 13–16), RAG and Docker (Weeks 17–18).
- The architecture rules in `ARCHITECTURE.md` and why the import graph points the way it does.
- Markdown, from nineteen weeks of curriculum files and reflections.
- The repository discipline that documentation follows behaviour: `validation.md` updates whenever CLI output changes.

## 3. What this week adds

- **Docstring conventions**: PEP 257 mechanics and Google-style `Args:`/`Returns:`/`Raises:` sections; contracts on protocols, mechanisms on implementations.
- **Documentation architecture**: the four-layer zoom model (README → docs/ → ARCHITECTURE → docstrings) and the Diátaxis split (tutorial / how-to / reference / explanation), structured the way MkDocs/Sphinx expect — without installing either.
- **Diagrams-as-code**: Mermaid syntax, GitHub rendering, and deriving diagrams from the real import graph.
- **Reader personas**: writing one README that serves a recruiter, an engineer, future you, and a professor in order of impatience.
- **The demo script**: exact commands + copy-pasted expected outputs, rehearsed until it cannot fail.
- **Portfolio narrative**: limitations sections, four-part tradeoff explanations, and the problem/solution/learning story.

## 4. Why this week matters

The README is the interface to your portfolio: reviewers read it before any code and decide in under a minute whether to continue. Documentation is also the highest-leverage habit for future you — the rationale you write down this week is the rationale you will not have to re-derive (or re-break) in six months. And professionally, architecture communication and honest tradeoff narratives are exactly the skills that separate engineers who build systems from engineers who own them.

## 5. Learning objectives

By the end of this week you can:

1. Write PEP 257 / Google-style docstrings and explain where Python stores them and which tools read them.
2. Structure a `docs/` folder along Diátaxis lines, ready for MkDocs or Sphinx adoption later.
3. Author Mermaid diagrams for module dependencies, the ingestion pipeline, and the RAG pipeline — derived from imports, not memory.
4. Write a ten-section README that serves all four reader personas.
5. Produce and rehearse a 2-minute demo script with verified expected outputs.
6. Write honest limitations, four-part tradeoffs, and a portfolio narrative — and deliver them aloud.
7. Detect and fix documentation rot with the fresh clone test, demo rehearsal, and link/diagram verification.

## 6. Project milestone

> **The repository README is employer-ready and tells the full project story — verified by a fresh clone test with an empty deviation log.**

## 7. Files / modules touched

- `README.md` (repo root) — rewritten to the ten-section structure
- `ARCHITECTURE.md` — verified against code; diagrams + design-decisions section added
- `docs/demo.md` — new: rehearsed 2-minute demo script
- `docs/retrospective.md` — new: 19-week retrospective
- `docs/diagrams/modules.md`, `docs/diagrams/ingestion.md`, `docs/diagrams/rag.md` — new: one focused Mermaid diagram each
- `src/researchops/core/interfaces.py` — Google-style docstrings on every protocol and method
- `src/researchops/services/` — docstring pass on public entry points
- `tests/unit/test_documentation.py` — new: docstring presence test

## 8. Commands introduced

```bash
python -m pydoc researchops.core.interfaces          # render module docs in the terminal
python -c "import researchops.core.interfaces as i; print(i.PaperRepository.__doc__)"
grep -rn "^from researchops\|^import researchops" src/researchops/   # derive the import graph
cd /tmp && git clone <repo-url> researchops_fresh    # the fresh clone test
```

## 9. Tests involved

- New docstring presence test asserting every public protocol class/method exposes a non-empty `__doc__`.
- README-command coverage check: every command shown in the README has a `CliRunner` E2E test.
- The standing suite must stay green: `ruff check src tests` and `pytest --cov=researchops --cov-report=term-missing -q`.
- Manual but defined tests: the fresh clone test, the full demo rehearsal, the GitHub diagram-render check, the link-click pass.

## 10. Study plan for the week

- **Day 1** — Read [notes.md](notes.md) in full. Do warm-ups W1–W4 and code-reading R1–R4 from [exercises.md](exercises.md). You now have the docstring worklist and the verified import graph.
- **Day 2** — Docstring pass (I1) plus the presence test (T1). Build the three diagrams (I2) and verify they render on GitHub.
- **Day 3** — Write the final README (I3) and update ARCHITECTURE.md (I4). Run break-it Experiments 4–6 against your own drafts.
- **Day 4** — Demo script (I5) and retrospective (I6). Rehearse the demo end to end. Run break-it Experiments 1–2 (fresh clone, output verification).
- **Day 5** — Remaining break-it experiments, testing exercises T2–T3, at least one brutal exercise, then [validation.md](validation.md) and [reflection.md](reflection.md).

## 11. Estimated time breakdown

| Activity | Hours |
|---|---|
| Notes (reading + REPL verification) | 2.5 |
| Docstring pass + presence test | 2 |
| Diagrams (derive, write, verify rendering) | 1.5 |
| README + ARCHITECTURE.md | 3 |
| Demo script + retrospective + rehearsal | 2 |
| Break-it lab (incl. fresh clone passes) | 2.5 |
| Validation + reflection | 1 |
| **Total** | **~14.5** |

## 12. How to know you are stuck

- You have been polishing README wording for an hour without having run the fresh clone test once — verification beats wordsmithing; clone first.
- Your diagram has more than ~10 nodes — you are drawing everything at once; split by question (modules / ingestion / RAG).
- You cannot write a docstring for a method — you do not understand its contract; read its tests, then its callers, then write.
- The demo rehearsal keeps failing at different steps — your environment has state; restart from an actual fresh clone, not a cleaned working copy.
- You cannot name a single limitation — you are in salesmanship mode; re-read notes section 6.8 and list what broke during the break-it labs of Weeks 13–18.

## 13. Definition of done

- [ ] Final README with all ten sections; opening paragraph passes the no-jargon test
- [ ] Quick Start verified by a fresh clone test with an **empty deviation log**
- [ ] ARCHITECTURE.md accurate against the code, with three Mermaid diagrams and ≥3 four-part tradeoffs
- [ ] All diagrams render correctly on GitHub
- [ ] `docs/demo.md` rehearsed end to end with zero script/reality deviations
- [ ] `docs/retrospective.md` answers all five questions with specifics
- [ ] Every public protocol method documented; docstring presence test in the suite and passing
- [ ] `ruff check src tests` and `pytest --cov=researchops --cov-report=term-missing -q` pass

## 14. Ruthless mentor checkpoint

Hand the repository URL to someone — or simulate it without mercy — and require: they run the Quick Start without asking you anything; they explain back what the project does after reading only paragraph one; they follow `docs/demo.md` to a working `ask` command. Then answer aloud, cold: "Walk me through the architecture", "Why SQLite?", "What are the limitations?". If any answer rambles past two minutes or names no specifics, you are not done.

## 15. What not to do this week

- Do not install MkDocs, Sphinx, or any documentation dependency — structure for them, adopt them only on explicit request.
- Do not add features, refactor working code, or "quickly improve" anything beyond what documentation work uncovers as a genuine bug.
- Do not write expected outputs from memory — run, then paste.
- Do not inflate: no "production-ready", no "blazing fast". Precision plus a limitations section beats adjectives.
- Do not draw diagrams from intention — derive them from imports.
- Do not skip the second fresh-clone pass after fixing the first round of deviations.

## 16. Bridge to next week

Week 20 is final hardening and the v1.0.0 release. Everything you wrote this week becomes release collateral: the demo script becomes the release-acceptance test, the README is what the tag points to, and the limitations section seeds the post-v1 roadmap. Polish this week; ship next week.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 18 Reflection](../week-18-docker-environment-config/reflection.md) · ➡️ [Notes →](notes.md)

**Week 19 — Documentation and Portfolio Polish:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
