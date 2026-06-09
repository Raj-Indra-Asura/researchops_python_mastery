<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 03 — OOP and Domain Modeling:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 2 Reflection](../week-02-files-errors-logging/reflection.md) · ➡️ [Notes →](notes.md)

---
<!-- NAV_END -->

# Week 03 README - OOP and Domain Modeling
## Chapter story
The scanner works.
It can walk a directory and discover PDF files.
That is useful, but it is still a low-level view of the world.
A file path is not the same thing as a research paper.
A tuple of values is not the same thing as an ingestion run.
A plain string is not the same thing as a validated search query.
This week is where the codebase starts speaking the language of the problem.
Instead of passing around loose dictionaries and vaguely named variables, we model the real concepts in ResearchOps.
We create a `Paper`.
We distinguish a `ParsedDocument` from a persisted `Paper`.
We record a `FailedDocument` instead of losing an exception in a log message.
We collect the outcome of a full scan in an `IngestionResult`.
This is the week where the project begins to feel like a system instead of a script.
## Chapter objectives
By the end of this chapter, you should be able to:
- explain what a class is in plain language
- explain how an instance differs from a class definition
- use `@dataclass` to reduce boilerplate in data-rich models
- recognise when a domain concept should be a value object
- describe the difference between an entity and a value object
- use `field(default_factory=...)` to avoid shared mutable defaults
- explain why `frozen=True` is useful for small immutable concepts
- use `__post_init__` to enforce invariants after dataclass initialisation
- read and write `@property` methods for computed values
- explain when `__str__` improves user-facing output
- explain why `StrEnum` is safer than ad-hoc string constants
- model a pipeline with composition instead of inheritance
- read unit tests as executable explanations of model behavior
- describe why `core/` must stay independent from CLI, API, storage, and ML layers
## Week 3 milestone
Your milestone is to understand and confidently explain the Week 3 domain layer:
- `PaperId` as a stable identifier
- `Paper` as the central entity
- `ParsedDocument` as parser output before persistence
- `FailedDocument` as explicit failure tracking
- `IngestionResult` as the summary of one ingestion run
- `Query` and `Tag` as small value objects with invariants
If you can explain why each of these exists, what fields it owns, and what behavior belongs on it, you have reached the chapter milestone.
## Files in this chapter
Read these files closely:
- `src/researchops/core/models.py`
- `src/researchops/core/value_objects.py`
- `tests/unit/test_models.py`
- `tests/unit/test_value_objects.py`
Use these chapter notes while you read:
- `curriculum/month-01-python-core/week-03-oop-domain-modeling/notes.md`
- `curriculum/month-01-python-core/week-03-oop-domain-modeling/exercises.md`
- `curriculum/month-01-python-core/week-03-oop-domain-modeling/break_it.md`
- `curriculum/month-01-python-core/week-03-oop-domain-modeling/validation.md`
- `curriculum/month-01-python-core/week-03-oop-domain-modeling/reflection.md`
## Recommended commands
Set up the environment and run the tests that define this chapter:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest tests/unit/test_models.py -v
pytest tests/unit/test_value_objects.py -v
```
Useful code-reading commands:
```bash
sed -n '1,220p' src/researchops/core/models.py
sed -n '1,220p' src/researchops/core/value_objects.py
sed -n '1,220p' tests/unit/test_models.py
sed -n '1,220p' tests/unit/test_value_objects.py
```
## Suggested study plan
### Session 1 - Build the mental model
- Read `notes.md` sections on classes, instances, dataclasses, and value objects.
- Open `models.py` and identify every class.
- For each class, answer: what real-world concept does this represent?
- Do not code yet.
- Focus on naming and meaning.
### Session 2 - Trace the pipeline
- Read the ResearchOps-specific pipeline section in `notes.md`.
- Draw the flow from file path -> parsed document -> paper or failure -> ingestion result.
- Explain out loud why `ParsedDocument` and `Paper` are not the same object.
### Session 3 - Study invariants
- Read the sections on `frozen=True`, `__post_init__`, and `field(default_factory=...)`.
- Work through the workbook exercises.
- Reproduce the mutable default list bug from `break_it.md`.
### Session 4 - Study the tests as documentation
- Read every test in `tests/unit/test_models.py`.
- Read every test in `tests/unit/test_value_objects.py`.
- For each test, say what behavior it protects.
- Ask yourself what bug would appear if that test did not exist.
### Session 5 - Validate and reflect
- Run the commands in `validation.md`.
- Complete the prompts in `reflection.md`.
- If you cannot explain the difference between entity and value object from memory, repeat Sessions 1 to 3.
## Time estimate
Plan for about 6 to 9 hours total.
A reasonable breakdown is:
- 1.5 hours reading the notes
- 1.5 hours reading the source files slowly
- 1 to 2 hours doing exercises
- 1 hour running break-it experiments
- 30 minutes validating
- 30 to 60 minutes reflecting and summarising aloud
If you are new to classes and dataclasses, take longer.
Depth matters more than speed this week.
## Stuck signals
You are probably stuck if:
- you can describe fields, but not why the class exists
- you keep saying "it is just data" about every object
- you are unsure why `field(default_factory=list)` matters
- you are unsure why `PaperId` is frozen
- you cannot explain why `total` and `success_rate` are properties
- you think `ParsedDocument` and `Paper` are duplicates
- you cannot tell whether validation belongs in `__post_init__` or somewhere else
- you think architecture boundaries are only about folder names
If any of those are true, pause and re-read the relevant section in `notes.md` before moving on.
## Definition of done
You are done with Week 3 when you can truthfully say:
- [ ] I can explain class, instance, attribute, and method without reading notes.
- [ ] I understand what `@dataclass` generates for me.
- [ ] I know why mutable defaults are dangerous.
- [ ] I can explain why `PaperId`, `Query`, and `Tag` are value objects.
- [ ] I can explain why `Paper` is an entity.
- [ ] I can explain what invariant means in this chapter.
- [ ] I can explain what `__post_init__` is for.
- [ ] I can explain what `@property` is for.
- [ ] I can explain how `IngestionResult` composes other domain objects.
- [ ] I can read the Week 3 tests and tell what each one is protecting.
- [ ] I understand why `core/` must not import infrastructure code.
- [ ] I can connect these ideas to future features like storage, search, and ML.
## Bridge to Week 4
Week 4 takes these domain ideas and wires them into packaging and CLI structure.
That means Week 3 is foundational.
If the domain model is vague, the CLI will feel awkward.
If the domain language is clear, the CLI becomes easier to design because commands can talk in the same vocabulary.
Next week, you will care more about entry points, packaging, and command structure.
This week, you are making sure the nouns and concepts underneath that interface are solid.
Learn the language now.
You will reuse it for the rest of the course.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 2 Reflection](../week-02-files-errors-logging/reflection.md) · ➡️ [Notes →](notes.md)

**Week 03 — OOP and Domain Modeling:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
