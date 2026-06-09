# Week 19 Break-It: Documentation

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › [Week 19 — Documentation & Portfolio Polish](./README.md) › **break_it.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Why break documentation?

Documentation failures are not compiler errors. They are silent. A user follows your README, hits an error, and gives up. You never find out. Documentation break-it exercises train you to find the failures before your reader does.

---

## Experiment 1: The fresh clone test

This is the most important documentation test. Do it every time you write a new README section.

```bash
cd /tmp
git clone <your-repo-url> researchops_fresh
cd researchops_fresh
```

Now follow your own README from start to finish. Do not use any knowledge you have that is not written in the README. Pretend you are a developer who has never seen this project.

**What typically breaks**:
- Missing prerequisite (Python version, system library, poppler for PDF parsing).
- Wrong install command (wrong extras, missing `dev` group).
- Command that was renamed between Week 10 and Week 19 but the README was not updated.
- Data directory that does not exist yet (`./examples/sample_papers` might not exist in a fresh clone).
- Environment variable that the app needs but `.env.example` does not document.

**What to do with each failure**: fix the README. If the problem is in the code (a missing directory, a non-optional dependency), fix the code and document it.

---

## Experiment 2: The 5-minute test

Read your README introduction aloud to yourself. Or, better, read it to someone who is not a software engineer and ask them to explain back to you what the project does.

**What to look for**:
- Did they understand what the project does? (If not: rewrite the opening paragraph.)
- Did they understand who it is for? (If not: add or clarify the audience statement.)
- Were there words they did not understand in the first two paragraphs? (If so: move jargon to later sections.)

A README introduction that requires domain knowledge to understand fails the recruiter persona.

---

## Experiment 3: The diagram accuracy test

Draw the architecture diagram from memory, without looking at the code. Then open the codebase and compare:

- Modules you forgot to include in the diagram.
- Arrows pointing the wrong direction (a service calling a CLI component instead of the other way around).
- A module that exists in the diagram but has been deleted or renamed.
- A coupling that exists in the code but is not shown in the diagram.

Update the diagram to match reality. Architecture diagrams that do not match the code are worse than no diagram, because they actively mislead the reader.

---

## Experiment 4: The stale documentation test

Search the entire `docs/` directory and all Markdown files for:
- Version numbers or dates that are no longer accurate.
- File paths that have been renamed.
- Commands that no longer work.
- Feature descriptions for features that were removed or not yet built.
- Promises in the README that the project does not keep.

Fix all of them. Stale documentation erodes trust faster than missing documentation. A reader who follows a command and gets a different result than the README shows will question everything else in the documentation.

---

## Experiment 5: README contradiction test

Read your README and find at least one place where two sections contradict each other. For example:
- The Features section says "supports PostgreSQL" but the Quick Start uses SQLite.
- The Architecture section shows a `worker` module but the Features section does not mention background processing.
- The Project Status says "alpha" but the README title says "v1.0.0".

Fix the contradiction. Usually the Quick Start and the Architecture section are most likely to drift from each other.

---

## Experiment 6: The "no context" test

Remove yourself from the context. Pretend you know nothing about this project. Read the first paragraph of the README. Now answer:
- What problem does this solve?
- Who built it and why?
- Is it production-ready or a learning project?
- What technologies does it use?

If you cannot answer all four questions from the first paragraph alone, revise until you can.

---

## Experiment 7: The demo script failure test

Follow `docs/demo.md` exactly in a fresh environment. Before each command, predict the expected output. Then run it.

For each mismatch between predicted and actual output:
- Was it a documentation error (wrong expected output)?
- Was it a code error (the command does not work)?
- Was it an environment error (missing dependency, wrong path)?

Fix all three types of mismatches. A demo that shows wrong expected output in the script is worse than a demo with no expected output shown.

---

## Edge cases to check

| Documentation element | What to check |
|---|---|
| Code blocks | Every code block is syntax-highlighted with the correct language tag |
| Commands | Every command works on a fresh clone |
| File paths | Every referenced file path exists |
| Mermaid diagrams | All diagrams render on GitHub (test by pushing to a branch) |
| Links | Every internal and external link resolves |
| Version numbers | Consistent across README, CHANGELOG, pyproject.toml, and `__init__.py` |
| Limitations | Accurate and honest — not overstated, not understated |

---

## What did you learn?

Answer these in your `reflection.md`:

1. How long did the fresh clone test take to complete without errors?
2. Which section of the README was most confusing to an outside reader?
3. How many stale or incorrect statements did you find?
4. What is the one thing you were most wrong about in your initial documentation?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 19 — Documentation & Portfolio Polish** · *break_it.md — the failure lab* (step 4 of 6 this week).

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
8. [Next week → Week 20](../../../curriculum/month-05-production-portfolio/week-20-final-hardening-v1-release/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 20 — Final Hardening & v1.0 Release](../../../curriculum/month-05-production-portfolio/week-20-final-hardening-v1-release/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 5 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 5 overview](../README.md) · [📄 Week 19 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
