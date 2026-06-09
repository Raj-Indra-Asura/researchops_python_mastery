<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 03 — OOP and Domain Modeling:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · **Reflection**

⬅️ [← Validation](validation.md) · ➡️ [📝 Week 03 Report](../../../docs/weekly-reports/README.md) · [Week 4 →](../week-04-cli-packaging/README.md)

---
<!-- NAV_END -->

# Week 03 Reflection Prompts
## Looking back at the chapter
- What changed in your understanding of object-oriented programming this week?
- At the start of the week, what did you think a class was?
- What do you think a class is now?
- Which idea felt most abstract at first?
- Which idea became concrete once you saw it in ResearchOps?
## Domain language
- Which class name in Week 3 feels most meaningful to you?
- Which class name took the longest to understand?
- Why is `Paper` a better name than a generic container like `Record` or `Item`?
- Why is `IngestionResult` a better name than a tuple of lists?
- Where did naming improve your own thinking?
## Classes and instances
- How would you explain the difference between a class and an instance to a beginner?
- What is one example of a class from this week?
- What is one example of an instance from this week?
- When do you now think a plain dictionary is enough?
- When do you now think a class is clearly better?
## Dataclasses
- What work does `@dataclass` save you from writing manually?
- Which generated method do you appreciate most right now?
- What part of dataclasses still feels confusing?
- What part now feels simple?
- How did dataclasses make the code easier to read?
## Invariants and validation
- What invariant stood out most this week?
- Why should some invalid states be blocked at construction time?
- What is one example of a value object that should reject bad input immediately?
- What is one example of data that may be allowed to stay flexible for now?
- How do invariants reduce later bugs?
## Value objects versus entities
- How would you explain the difference between a value object and an entity?
- Why does `PaperId` feel value-like?
- Why does `Tag` feel value-like?
- Why does `Paper` feel entity-like?
- Which distinction here still feels fuzzy?
## Mutable versus immutable
- What did the shared-list bug teach you?
- Why is `field(default_factory=list)` memorable now?
- Why does `frozen=True` fit `PaperId` better than `IngestionResult`?
- What dangers come from mutating identity-like values?
- Where is mutability still useful in this chapter?
## Behavior on models
- Which method from Week 3 felt the most natural to place on the model?
- Why does `word_count()` belong on `Paper`?
- Why does `summary()` belong on `FailedDocument`?
- Why do `total` and `success_rate` make sense as computed values?
- What behavior would not belong on these models yet?
## Tests as documentation
- Which test explained the model design most clearly?
- Which test exposed a bug pattern you want to remember?
- What did the tests teach you that the class definitions alone did not?
- How did reading tests change your understanding of the code?
- What new test would you want to add later?
## Architecture boundaries
- Why must `core/` stay independent from `storage/`, `cli/`, and `api/`?
- What would go wrong if core models imported infrastructure code directly?
- How does a clean core help testing?
- How does a clean core help future refactoring?
- Why is dependency direction a design choice, not just a folder convention?
## Debugging and mistakes
- Which beginner mistake are you now least likely to make again?
- Which beginner mistake could still trick you under time pressure?
- Which error message from the break-it lab taught you the most?
- What did you learn from intentionally breaking `__str__`, `__post_init__`, or `frozen=True`?
- What debugging habit do you want to keep?
## Personal learning process
- Where did you slow down and benefit from it?
- Where did you rush and miss meaning?
- What study method helped most this week: reading, running code, writing, or speaking aloud?
- Which explanation from your own words are you proud of?
- What do you want to explain more clearly next time?
## Confidence and readiness
- Week 3 confidence score from 1 to 10:
- What evidence supports that score?
- What would raise your score by one point?
- What topic needs one more review before moving on?
- What concept now feels solid enough to teach someone else?
## Bridge to Week 4
- How will a stronger domain model help when building CLI packaging and entry points next week?
- Which Week 3 concept do you expect to reuse immediately in Week 4?
- What do you want to carry forward from this chapter?
- What do you want to review once more before starting the next week?
- Write one sentence that captures the main lesson of Week 3 in your own words.

<!-- WEEKLY_REPORT -->
---

## Weekly Report

When you have completed this reflection, write your [Week 03 report](../../../docs/weekly-reports/README.md).

Store it at `docs/weekly-reports/week-03-report.md` (see the [weekly reports guide](../../../docs/weekly-reports/README.md) for the template).

Once your report is committed, advance to [Week 4 →](../week-04-cli-packaging/README.md).
<!-- WEEKLY_REPORT_END -->

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Validation](validation.md) · ➡️ [📝 Week 03 Report](../../../docs/weekly-reports/README.md) · [Week 4 →](../week-04-cli-packaging/README.md)

**Week 03 — OOP and Domain Modeling:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · **Reflection**

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
