# Weekly Reports

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../README.md) › [🗺️ Roadmap](../../ROADMAP.md) › **Weekly reports** (your lab notebook)
>
> 📓 You arrive here after finishing a week's `reflection.md`. Write the report, then move to the next week's README.
<!-- NAV:TOP:END -->

This folder is your **lab notebook** for the 20-week ResearchOps journey. At the
end of every week you write one short, honest report about what actually
happened — what you built, what broke, and whether you truly understand it.

If the curriculum is the *book*, weekly reports are the *margin notes you write
to your future self.*

---

## 1. Purpose of weekly reports

A weekly report is a structured record of one week of learning. It captures:

- what you built and why,
- what broke and how you fixed it,
- what you tested (and what you forgot to test),
- the decisions you made,
- and an honest judgement of whether you are ready to move on.

It is **not** a status update for someone else. It is a tool for you.

## 2. Why weekly reports matter for learning

- **Writing forces understanding.** If you cannot explain what you built in a few
  sentences, you do not understand it yet. The report exposes that gap *before*
  it compounds in the next week.
- **They surface false confidence.** "It works" is not the same as "I know why it
  works." The report makes you separate the two.
- **They build a debugging history.** Re-reading "what broke / how I debugged it"
  across weeks turns scattered struggles into reusable instincts.
- **They create portfolio evidence.** Twenty honest reports are a credible story
  of growth that a generic "I finished a course" claim can never match.
- **They protect the dependency chain.** Each week assumes the previous one is
  solid. The report is the gate that keeps you from building Week 10 on a
  misunderstood Week 9.

## 3. Where reports should be stored

Store every report in this folder:

```
docs/weekly-reports/
```

One Markdown file per week. Commit each report to Git in the same week you finish
the work, so your history shows steady, dated progress.

## 4. Recommended naming convention

Use a zero-padded week number so files sort correctly:

```text
docs/weekly-reports/week-01-report.md
docs/weekly-reports/week-02-report.md
docs/weekly-reports/week-03-report.md
...
docs/weekly-reports/week-20-report.md
```

Keep the name lowercase and hyphenated to match the rest of the repository.

## 5. Weekly report template

Copy this template into each new `week-XX-report.md` and fill every section.
Replace `XX` with the week number and `Title` with the week's theme.

```markdown
# Week XX Report — Title

## What I built

## What I learned

## What broke

## How I debugged it

## Tests I wrote

## Tests I should have written

## Architecture decisions I made

## What I overengineered

## What I underengineered

## Commands I ran

## Evidence of completion

## Confidence score

## Am I ready for next week?
```

Guidance for the trickier sections:

- **What broke / How I debugged it:** be specific. Paste the error, name the
  cause, describe the fix. "Fixed a bug" teaches you nothing later.
- **Tests I should have written:** this is the most valuable section. Honesty
  here is what turns you into an engineer.
- **Evidence of completion:** paste real command output (test summary, CLI
  result), not a claim.
- **Confidence score:** a number from 1–10, plus one sentence on *why*.

## 6. Example mini report (Week 1)

```markdown
# Week 01 Report — Python Foundations and Repository Setup

## What I built
A `researchops scan PATH` CLI command that walks a directory with `pathlib`
and prints every discovered PDF path. Set up the `src/` layout, the editable
install (`pip install -e ".[dev]"`), and the first pytest test.

## What I learned
How a `src/`-layout package is imported, why `pip install -e` matters for
development, and how Typer turns a function into a CLI command.

## What broke
`researchops: command not found` after install, and `scan` initially returned
zero files even though PDFs existed.

## How I debugged it
The command error was a stale shell PATH — reactivating the virtualenv fixed it.
The empty result was a `Path.glob("*.pdf")` call that did not recurse; switching
to `rglob("*.pdf")` found nested files. I confirmed with a temp folder of
fixture PDFs.

## Tests I wrote
`test_scan_finds_pdfs` over a tmp_path fixture; `test_scan_empty_dir_returns_nothing`.

## Tests I should have written
A test for non-PDF files being ignored, and one for a path that does not exist.

## Architecture decisions I made
Kept file discovery in a small function separate from the CLI command so it can
be tested without invoking Typer.

## What I overengineered
Nothing this week — kept it deliberately small.

## What I underengineered
Error handling for a missing directory; it raises a raw traceback instead of a
friendly message.

## Commands I ran
pip install -e ".[dev]"; ruff check src tests; pytest -q; researchops scan ./examples/sample_papers

## Evidence of completion
`2 passed in 0.10s`; `researchops scan ./examples/sample_papers` printed the
sample PDF paths.

## Confidence score
8/10 — comfortable with the layout and CLI; want more practice with pathlib edge
cases.

## Am I ready for next week?
Yes. Scanner runs, tests pass, lint is clean. Week 2 (files, errors, logging)
will let me replace that raw traceback with proper error handling.
```

## 7. Rule: do not proceed without a report

**Finishing the code is not finishing the week.** Do not start week `N+1` until
`week-NN-report.md` exists and every section is filled in. The report is the
checkpoint that confirms the previous week is actually solid — skipping it means
building on sand.

## 8. Rule: reports are for honest learning, not showing off

These reports are written to your future self, not to an audience.

- Write down what broke and what still feels weak. A report with no struggles is
  a report that is lying.
- A low confidence score is **useful information**, not a failure. It tells you
  exactly what to review.
- Do not polish away the mistakes — the mistakes are where the learning lives.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** The weekly-report hub — step 7 of every week's loop (after `reflection.md`, before the next week).

### Optional paths
- ⤴️ **Just finished a reflection?** Write that week's report using the template above.
- ▶️ **Report written?** Open the next week's `README.md` from the [Roadmap](../../ROADMAP.md).
- 🧭 **Not sure which week you are on?** Check the [Roadmap](../../ROADMAP.md) status column.

### Global navigation
[🏠 Home](../../README.md) · [🗺️ Roadmap](../../ROADMAP.md) · [📚 Syllabus](../../SYLLABUS.md) · [▶️ Start Week 1](../../curriculum/month-01-python-core/week-01-foundations/README.md)
<!-- NAV:BOTTOM:END -->
