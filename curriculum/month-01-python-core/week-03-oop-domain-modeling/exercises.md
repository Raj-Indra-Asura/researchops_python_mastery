# Week 03 Exercises - OOP and Domain Modeling Workbook

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 1](../README.md) › [Week 3 — OOP & Domain Modeling](./README.md) › **exercises.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->
## How to use this workbook
This workbook is for slow thinking.
Do not rush through it like a checklist.
The point of Week 3 is not to memorise syntax.
The point is to make domain modeling feel natural.
Read the code, answer in writing, and run small experiments.
If an exercise asks you to explain something aloud, actually do it.
Speaking clearly is a strong test of understanding.
## Preparation
Before starting, open these files side by side:
- `src/researchops/core/models.py`
- `src/researchops/core/value_objects.py`
- `tests/unit/test_models.py`
- `tests/unit/test_value_objects.py`
Keep `notes.md` open.
Use the validation commands only after you have worked through the ideas.
## Section 1 - Orientation drills
### Exercise 1.1 - Name the concepts
Read every class name in `models.py` and `value_objects.py`.
For each one, write a one-sentence answer to both questions:
1. What real thing does this class represent?
2. Why is a plain dictionary not enough here?
### Exercise 1.2 - Sort by kind
Make a two-column table.
Column A is `Entity`.
Column B is `Value Object`.
Place each of these names into one of the columns:
- `Paper`
- `PaperId`
- `ParsedDocument`
- `FailedDocument`
- `IngestionResult`
- `Query`
- `Tag`
Then justify every choice in one sentence.
### Exercise 1.3 - Trace the pipeline
Without looking at notes, draw this pipeline from memory:
`Path -> ParsedDocument -> Paper or FailedDocument -> IngestionResult`
Now annotate each arrow with the kind of work that happens there.
For example, one arrow may represent parsing.
Another may represent validation.
Another may represent aggregation.
### Exercise 1.4 - Read the nouns before the verbs
List every field on `Paper`.
Then answer:
- which fields describe identity?
- which fields describe content?
- which fields describe metadata?
- which fields are optional?
- which field is intentionally stored as `str` instead of `Path`?
Why does that last decision matter?
## Section 2 - Beginner mental model practice
### Exercise 2.1 - Blueprint language
Write three sentences that begin with `A class is...`.
Write three sentences that begin with `An instance is...`.
Do not use the words "blueprint" or "object" in at least one sentence.
This forces you to explain the idea from another angle.
### Exercise 2.2 - Dictionary versus class
Imagine representing a paper like this:
```python
paper = {
    "id": "abc123",
    "title": "Transformers",
    "text": "...",
    "num_pages": 12,
}
```
Write down five problems that can emerge when a codebase uses this style everywhere.
At least two of your answers must involve team communication, not syntax.
### Exercise 2.3 - When a dict is still okay
Now be fair.
Write three situations where a plain dictionary is perfectly acceptable.
Example categories:
- quick throwaway scripts
- raw JSON from an API boundary
- logging payloads
The goal is to avoid turning "classes are good" into a superstition.
## Section 3 - Dataclass drills
### Exercise 3.1 - Generated methods
Without opening Python documentation, write down what `@dataclass` usually generates for you.
Then check your answer in `notes.md`.
After checking, answer this follow-up question:
Why is generated `__repr__` especially useful during testing?
### Exercise 3.2 - Field defaults
Look at these fields on `Paper`:
- `created_at: datetime = field(default_factory=datetime.utcnow)`
- `tags: list[str] = field(default_factory=list)`
Explain why both use `default_factory`, but for different reasons.
### Exercise 3.3 - Constructor thinking
Write the exact constructor call you would use to create a `Paper` with:
- id `abc`
- title `Attention Is All You Need`
- source path `papers/attention.pdf`
- text `hello world`
- 1 page
- 2048 bytes
Then answer:
Which fields can you omit?
Why can you omit them?
### Exercise 3.4 - Equality thinking
If two `Tag("machine learning")` objects normalise to the same value, should they compare equal?
Why?
If two `Paper` objects have the same title but different IDs, should they represent the same entity?
Why or why not?
## Section 4 - Line-by-line code reading
### Exercise 4.1 - PaperId reading
Read `PaperId.from_path()` and explain each operation in order:
1. `path.resolve()`
2. `str(...)`
3. `.encode()`
4. `hashlib.sha256(...)`
5. `.hexdigest()`
6. `[:16]`
7. `cls(value=digest)`
If you cannot explain one step, revisit the chapter notes before continuing.
### Exercise 4.2 - Paper behavior reading
Explain why `word_count()` is a method rather than a stored field.
Then explain why `is_empty()` belongs on the model instead of forcing every caller to repeat `len(self.text.strip()) == 0`.
### Exercise 4.3 - ParsedDocument reading
Write two reasons `ParsedDocument` should exist even if `Paper` already exists.
One answer must mention pipeline stages.
One answer must mention data shape or responsibility.
### Exercise 4.4 - FailedDocument reading
Suppose the codebase only logged failed file paths and did not model failures explicitly.
List four capabilities you would lose.
At least one answer must mention debugging.
At least one answer must mention reporting.
### Exercise 4.5 - IngestionResult reading
Why is `IngestionResult.total` a property rather than a manually maintained integer field?
What bug becomes more likely if you store `total` separately and forget to keep it in sync?
## Section 5 - Value object exercises
### Exercise 5.1 - Query invariants
In your own words, define the invariant for `Query`.
Now answer:
- Why is whitespace-only input invalid?
- Why is validation done at construction time?
- What later code becomes simpler because of this choice?
### Exercise 5.2 - Tag normalisation
Take each raw input and write the normalised tag you expect:
- `Machine Learning`
- `  NLP  `
- `deep-learning`
- `Graph   Search`
- `!!!data science!!!`
Then compare your reasoning with the implementation in `value_objects.py` and the explanation in `notes.md`.
### Exercise 5.3 - Frozen value objects
Write a short paragraph answering:
Why does immutability fit `Query`, `Tag`, and `PaperId` better than it fits `IngestionResult`?
Your answer must mention mutation over time.
### Exercise 5.4 - Use value objects in speech
Say these sentences aloud until they feel natural:
- `PaperId` is a value object because identity is its value.
- `Tag` is a value object because normalisation matters more than object identity.
- `Paper` is an entity because it represents a stored document in the system.
If any sentence feels fuzzy, fix the idea before moving on.
## Section 6 - Properties and string representations
### Exercise 6.1 - Property or method?
Classify each as better expressed by a property or a method:
- the total number of processed documents
- whether a paper is empty
- a long-running reparse action
- the ratio of successful ingestions
- a formatted summary string for display
There may be more than one reasonable answer.
What matters is your reasoning.
### Exercise 6.2 - `__str__` versus default representation
What is the difference between these two outputs?
```python
print(PaperId(value="abc123"))
print(str(PaperId(value="abc123")))
```
Now explain why overriding `__str__` helps in logs, CLI output, and f-strings.
## Section 7 - Test reading as design reading
### Exercise 7.1 - Map each test to behavior
Open `tests/unit/test_models.py`.
For every test function, write:
- what behavior it checks
- what bug it prevents
- whether it is checking a normal case, edge case, or regression risk
### Exercise 7.2 - Read test names as English
Rewrite three test names into full English sentences.
Example pattern:
`test_success_rate_zero_when_empty` -> `The success rate should be 0.0 when no documents were processed.`
### Exercise 7.3 - Missing tests discussion
Identify three tests you might add later, but do not write code yet.
Good candidates include:
- title validation if introduced later
- `PaperId` differences for different paths
- `Tag` handling of repeated punctuation
For each idea, explain why the test matters.
## Section 8 - Architecture exercises
### Exercise 8.1 - Dependency direction
Explain why `core/` must not import from:
- `storage/`
- `cli/`
- `api/`
- `ml/`
Your answer should mention portability, testability, and dependency direction.
### Exercise 8.2 - Good and bad imports
Label each imagined import as `Allowed` or `Not allowed`.
Then explain why.
- `from pathlib import Path`
- `from datetime import datetime`
- `from researchops.storage.sqlite_repository import SqlitePaperRepository`
- `from researchops.cli.main import app`
- `import hashlib`
- `from fastapi import FastAPI`
### Exercise 8.3 - Boundary thinking
A parser library returns raw text and metadata.
Which layer should turn that into `ParsedDocument`?
Which layer should turn `ParsedDocument` into `Paper` or `FailedDocument`?
Which layer should present the result to a user?
Use the architecture diagram to justify your answer.
## Section 9 - Guided REPL practice
Run these commands in a Python REPL after installing dev dependencies.
Read the result before moving on.
```python
from pathlib import Path
from researchops.core.models import Paper, PaperId, ParsedDocument, FailedDocument, IngestionResult
from researchops.core.value_objects import Query, Tag
from datetime import datetime
```
### Exercise 9.1 - Create a paper ID
```python
pid = PaperId.from_path(Path("sample.pdf"))
print(pid)
print(type(pid))
```
Write down what surprised you, if anything.
### Exercise 9.2 - Create a paper
```python
paper = Paper(
    id=str(pid),
    title="Example Paper",
    source_path="sample.pdf",
    text="graph neural networks are useful",
    num_pages=1,
    file_size_bytes=256,
)
print(paper.word_count())
print(paper.is_empty())
```
Explain why the result of `word_count()` is derived instead of stored.
### Exercise 9.3 - Create a parsed document
```python
doc = ParsedDocument(
    source_path=Path("sample.pdf"),
    raw_text="   ",
    num_pages=1,
    file_size_bytes=256,
)
print(doc.is_empty())
```
Why is emptiness still worth checking at this stage?
### Exercise 9.4 - Create a failure
```python
failure = FailedDocument(
    source_path=Path("broken.pdf"),
    error_message="PDF stream was corrupted",
    error_type="ParseError",
)
print(failure.summary())
```
Why is a summary method useful when teaching CLI or API design later?
### Exercise 9.5 - Create an ingestion result
```python
result = IngestionResult(
    run_id="run-001",
    directory=Path("papers"),
    started_at=datetime.utcnow(),
)
result.successes.append(paper)
result.failures.append(failure)
print(result.total)
print(result.success_rate)
```
Explain why the success rate is `0.5` in this example.
## Section 10 - Short writing prompts
Write 3 to 5 sentences for each prompt.
### Exercise 10.1
Why is naming a software design tool, not just a style choice?
### Exercise 10.2
Why is `IngestionResult` more expressive than returning `(successes, failures, skipped)`?
### Exercise 10.3
Why is a value object strongest when it becomes impossible to create an invalid one?
### Exercise 10.4
What is the difference between storing data and modeling meaning?
## Section 11 - Bug-spotting exercises
For each snippet, identify the bug before reading the explanation.
### Exercise 11.1 - Shared mutable default
```python
from dataclasses import dataclass

@dataclass
class Paper:
    tags: list[str] = []
```
What bug appears when two instances are created?
Why?
How does `field(default_factory=list)` fix it?
### Exercise 11.2 - Missing frozen mutation helper
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Tag:
    value: str

    def __post_init__(self) -> None:
        self.value = self.value.lower()
```
Why does this fail?
What tool does a frozen dataclass require instead?
### Exercise 11.3 - No validation
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Query:
    value: str
```
What invalid states are now possible?
Why does that matter for every caller downstream?
### Exercise 11.4 - Wrong property math
```python
@property
def success_rate(self) -> float:
    return len(self.successes) / len(self.failures)
```
List two logical problems in this implementation.
## Section 12 - Design comparison questions
### Exercise 12.1 - Dataclass or Pydantic?
Write a short comparison of dataclasses and Pydantic models.
You do not need to choose a winner.
Instead, answer:
- what job does each tool do well?
- why are dataclasses a good Week 3 teaching tool?
- when might Pydantic become useful later?
### Exercise 12.2 - Frozen or mutable?
For each object, choose `frozen` or `mutable` and justify your choice:
- `PaperId`
- `Tag`
- `Query`
- `Paper`
- `IngestionResult`
### Exercise 12.3 - Inheritance or composition?
Why is `IngestionResult` better modeled as an object that contains lists of `Paper` and `FailedDocument` than as some inheritance hierarchy?
Your answer must mention the phrase `has-a` or `is-a`.
## Section 13 - Explain-it-aloud practice
Give a one-minute explanation for each prompt.
Do not read your notes.
### Exercise 13.1
Explain `@dataclass` to a beginner.
### Exercise 13.2
Explain the mutable default list bug to a beginner.
### Exercise 13.3
Explain why `PaperId.from_path()` uses hashing.
### Exercise 13.4
Explain the difference between `ParsedDocument` and `Paper`.
### Exercise 13.5
Explain why tests are part of the documentation for a model.
## Section 14 - Stretch challenges
These are optional, but powerful.
### Exercise 14.1 - Design a new value object on paper
Invent a `RunId` value object.
Do not implement it in code.
Answer these questions:
- what invariant would it enforce?
- should it be frozen?
- what methods would it expose?
- would it be overkill at this stage?
### Exercise 14.2 - Design a future ML output
Imagine Week 11 introduces a classifier result.
Sketch a dataclass for `TopicPrediction`.
Include:
- paper ID
- predicted label
- score
- model version
Then explain why modeling typed outputs will matter for ML reliability.
### Exercise 14.3 - Rewrite a bad API mentally
Suppose a service returned this:
```python
("abc123", "paper title", 0.84, "snippet text")
```
Rewrite it mentally as a named model.
Explain why the named version is easier to maintain.
## Section 15 - Self-check checklist
Mark each item honestly.
- [ ] I can define class, instance, attribute, and method.
- [ ] I can explain when a dict is enough and when a class is better.
- [ ] I can explain what `@dataclass` generates.
- [ ] I know why `field(default_factory=list)` exists.
- [ ] I know why `frozen=True` matters for value objects.
- [ ] I can explain `__post_init__`.
- [ ] I can explain `@property`.
- [ ] I can explain `__str__` and why `PaperId` overrides it.
- [ ] I understand why `IngestionResult` uses composition.
- [ ] I understand why `core/` must stay independent.
## Section 16 - Optional answer discussion prompts
Use these with a study partner or by writing paragraphs in your notebook.
1. What design decision in Week 3 most increases clarity for future contributors?
2. Which object would be the most painful to replace with a raw dict, and why?
3. Which invariant feels most important to enforce immediately?
4. Which part of Week 3 feels like software design rather than syntax practice?
5. Where do you see these ideas showing up outside ResearchOps?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 1 — Python Core and Project Foundation · **Week 3 — OOP & Domain Modeling** · *exercises.md — the workbook* (step 3 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [notes.md](./notes.md)
- ▶ **Next:** [break_it.md](./break_it.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. **➡ [exercises.md](./exercises.md) ← you are here**
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 4](../../../curriculum/month-01-python-core/week-04-cli-packaging/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 4 — CLI & Packaging](../../../curriculum/month-01-python-core/week-04-cli-packaging/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 1 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 1 overview](../README.md) · [📄 Week 3 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
