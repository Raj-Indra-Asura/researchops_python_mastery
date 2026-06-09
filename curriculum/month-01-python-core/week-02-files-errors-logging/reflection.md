<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 02 — Files, Errors, Logging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · **Reflection**

⬅️ [← Validation](validation.md) · ➡️ [📝 Week 02 Report](../../../docs/weekly-reports/README.md) · [Week 3 →](../week-03-oop-domain-modeling/README.md)

---
<!-- NAV_END -->

# Reflection — Chapter 2

## Looking back at the week
- What part of the “50 PDFs dropped into a folder” story feels most real to you now?
- Which failure mode did you underestimate at the start of the week?
- Which concept from this chapter changed how you think about production Python code?

## Paths and filesystem thinking
- What is the biggest difference between a path string and a `Path` object in your own words?
- Which `Path` methods now feel natural to you?
- Which `Path` methods still feel easy to mix up?
- When you see a path in code now, what questions do you automatically ask about it?
- What filesystem edge case do you think you are now least likely to miss?

## Scanning and glob patterns
- How would you explain `*.pdf` to a total beginner?
- How would you explain `**/*.pdf` to a total beginner?
- Why does the choice between recursive and non-recursive search matter in real applications?
- Why is sorted output an important design decision rather than a cosmetic one?

## Exceptions and error messages
- Which custom exception from `core/exceptions.py` feels most useful to you?
- What makes an exception message actually helpful?
- Why is storing metadata like `path` or `paper_id` useful beyond the message text?
- What is one mistake you used to make with exceptions that you would now avoid?
- When should code raise an exception instead of returning a fallback value?

## Error handling flow
- What is the difference between preventing a failure and handling a failure well?
- Which clause in `try/except/else/finally` was hardest to internalize?
- What does “catch only what you understand” mean to you now?
- What kind of bug could `except Exception` accidentally hide in this project?
- Where should low-level failures stop, and where should user-facing messaging begin?

## Logging and observability
- How would you explain the difference between `print()` and logging to a future teammate?
- Which log level do you still have to think hardest about choosing?
- What makes a log message useful instead of noisy?
- What does `logging.getLogger(__name__)` buy you that a hard-coded logger name does not?
- When would you want `DEBUG` logs that users do not normally see?

## Tests and confidence
- Which test in `tests/unit/test_paths.py` do you appreciate the most now, and why?
- Which test in `tests/unit/test_exceptions.py` taught you something about API design?
- How did reading tests change your understanding of the implementation?
- What behavior would you add a test for if this chapter were one week longer?

## Architecture and design
- Why do the shared exceptions live in `core/` instead of inside the CLI?
- What architectural boundary from this repository feels more meaningful after this chapter?
- How does good error design make later service-layer work easier?
- How might careless filesystem code create problems for later ingestion, storage, or ML features?

## Personal debugging habits
- What do you do first now when a path-related bug appears?
- What do you do first now when a log message is missing?
- What do you do first now when an exception message is vague?
- What habit from this week do you want to keep using in every later chapter?

## Confidence check
- On a scale from 1 to 10, how confident are you with `pathlib`?
- On a scale from 1 to 10, how confident are you with custom exceptions?
- On a scale from 1 to 10, how confident are you with logging?
- Which score is lowest, and what exactly will you do to raise it?

## Looking forward
- What feels easier about entering Week 3 because of the work you did here?
- How do paths, exceptions, and logging prepare you for richer domain models?
- What one sentence would you tell your Week 1 self before they start this chapter?

<!-- WEEKLY_REPORT -->
---

## Weekly Report

When you have completed this reflection, write your [Week 02 report](../../../docs/weekly-reports/README.md).

Store it at `docs/weekly-reports/week-02-report.md` (see the [weekly reports guide](../../../docs/weekly-reports/README.md) for the template).

Once your report is committed, advance to [Week 3 →](../week-03-oop-domain-modeling/README.md).
<!-- WEEKLY_REPORT_END -->

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Validation](validation.md) · ➡️ [📝 Week 02 Report](../../../docs/weekly-reports/README.md) · [Week 3 →](../week-03-oop-domain-modeling/README.md)

**Week 02 — Files, Errors, Logging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · **Reflection**

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
