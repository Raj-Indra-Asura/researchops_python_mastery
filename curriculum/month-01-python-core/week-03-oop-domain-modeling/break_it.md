# Week 03 Break It - Failure Lab

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 1](../README.md) › [Week 3 — OOP & Domain Modeling](./README.md) › **break_it.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->
## How to use this lab
This lab is for controlled failure.
You will intentionally break ideas from Week 3 so the design reasons become visible.
Do not leave the codebase broken.
Make one experiment at a time, observe the failure, then restore the original code.
The goal is not chaos.
The goal is sharper understanding.
## Safety rules
- Work on a throwaway branch or restore changes immediately after each experiment.
- Run the smallest relevant test after each break.
- Read the error message fully before fixing anything.
- Write down what assumption the failure violated.
## Experiment 1 - Shared list bug from `tags: list[str] = []`
### Concept under test
Mutable defaults are shared when created once at class definition time.
### What to change
In `Paper`, replace:
```python
tags: list[str] = field(default_factory=list)
```
with:
```python
tags: list[str] = []
```
### What to do next
Create two `Paper` instances.
Append one tag to the first paper.
Inspect the second paper.
### Expected failure or surprise
Both instances now appear to share the same list.
A change in one leaks into the other.
### Why this happens
The empty list was created once and reused.
That means the class-level default becomes shared state.
### What it teaches
`field(default_factory=list)` is not decorative.
It is a correctness tool.
### Recovery
Restore `field(default_factory=list)`.
Run the model tests again.
## Experiment 2 - Mutating a frozen dataclass
### Concept under test
`frozen=True` blocks attribute reassignment after construction.
### What to do
Open a REPL and run:
```python
from researchops.core.models import PaperId
pid = PaperId(value="abc123")
pid.value = "changed"
```
### Expected failure
You should see a `FrozenInstanceError` or a closely related attribute mutation error.
### Why this happens
A frozen dataclass protects value semantics.
If a `PaperId` could change after creation, it would stop being a reliable identity value.
### What it teaches
Immutability is part of the contract, not just an implementation detail.
### Recovery
No code restore needed if you only used the REPL.
## Experiment 3 - Forgetting `object.__setattr__` inside `__post_init__`
### Concept under test
Frozen dataclasses cannot assign to fields normally, even inside `__post_init__`.
### What to change
Temporarily edit a frozen value object such as `Tag` so its `__post_init__` contains:
```python
self.value = self.value.lower()
```
instead of using `object.__setattr__`.
### Expected failure
Object creation now raises a frozen-instance mutation error.
### Why this happens
`__post_init__` runs after the generated `__init__`.
If the dataclass is frozen, normal assignment is still blocked.
### What it teaches
Frozen dataclasses can still normalise values, but they must do so through `object.__setattr__`.
### Recovery
Restore the original mutation helper.
Re-run the value object tests.
## Experiment 4 - Passing wrong types to dataclass fields
### Concept under test
Type hints are not strict runtime validators by default.
### What to do
In a REPL, try constructing a `Paper` like this:
```python
from researchops.core.models import Paper
paper = Paper(
    id=123,
    title=["not", "a", "string"],
    source_path=None,
    text=99,
    num_pages="ten",
    file_size_bytes="big",
)
print(paper)
```
### Expected surprise
Python may allow construction even though the types are wrong.
A later method call may fail in a confusing place.
### Why this happens
Dataclasses use annotations for readability, tooling, and static checking.
They do not automatically perform deep runtime validation.
### Compare with Pydantic
A Pydantic model would typically validate, coerce, or reject these values at runtime.
That is one reason Pydantic is popular at system boundaries.
### What it teaches
Type hints improve design, but they are not magic runtime guards.
### Recovery
Discard the bad REPL object.
Do not keep invalid code changes.
## Experiment 5 - Breaking `__str__`
### Concept under test
`__str__` must return a string.
### What to change
Temporarily replace `PaperId.__str__` with:
```python
def __str__(self) -> str:
    print(self.value)
```
### What to do next
Create a `PaperId` and call `str(pid)`.
### Expected failure
Python raises a `TypeError` because `__str__` returned `None`.
### Why this happens
`print()` performs output but does not return the string you need.
The `__str__` contract is explicit: return a `str`.
### What it teaches
Representation methods are tiny, but they still have strict behavioral contracts.
### Recovery
Restore `return self.value`.
Run the relevant tests.
## Experiment 6 - Inheriting from the wrong exception class
### Concept under test
Exception hierarchy affects what callers can catch reliably.
### What to change
If you have a custom exception in the core layer, temporarily make it inherit from an unrelated built-in or from something that is not appropriate for your error domain.
For example, pretend an empty query error inherited from `TypeError` instead of a domain-specific exception or `ValueError`-like semantic.
### What to do next
Run the test that expects the original exception behavior.
### Expected failure
The test either fails to catch the exception or communicates the wrong meaning.
### Why this happens
Inheritance is about meaning as much as mechanics.
A bad exception parent makes the error contract misleading.
### What it teaches
Exception type is part of API design.
### Recovery
Restore the intended exception hierarchy.
## Experiment 7 - Using `Paper` as a dict key versus `PaperId`
### Concept under test
Hashability often fits immutable value objects better than mutable entities.
### What to do
In a REPL, try this:
```python
from researchops.core.models import Paper, PaperId
paper = Paper(id="abc", title="T", source_path="p.pdf", text="x", num_pages=1, file_size_bytes=1)
pid = PaperId(value="abc")
lookup = {pid: "stored"}
print(lookup[pid])
```
Now try:
```python
bad_lookup = {paper: "stored"}
```
### Expected result
`PaperId` works naturally as a key because it is frozen and value-like.
`Paper` is usually unhashable by default because it is mutable.
### Why this happens
Hash-based collections rely on stable values.
Mutable objects are poor keys because their equality-relevant state can change.
### What it teaches
This is a practical reason value objects are often immutable.
### Recovery
No restore needed if you only used the REPL.
## Experiment 8 - Creating a circular dependency from the wrong layer
### Concept under test
Architecture boundaries protect the domain from infrastructure coupling.
### What to change
Temporarily add an import in `core/` from `storage/`, `cli/`, or `api/`.
For example, imagine `core/models.py` importing a repository implementation or CLI command.
### Expected failure
You may see import cycles, harder testing, or conceptually backwards dependency flow.
Even if the import technically works, the architecture is now wrong.
### Why this happens
The core layer should be the stable center.
Outer layers depend inward.
If the core depends outward, everything becomes harder to reuse and reason about.
### What it teaches
Architecture rules are not folder decoration.
They prevent real coupling problems.
### Recovery
Remove the bad import immediately.
Run the affected tests.
## Experiment 9 - Corrupting the success-rate calculation
### Concept under test
Computed properties should derive from authoritative state.
### What to change
Temporarily rewrite `success_rate` incorrectly.
Examples:
```python
return len(self.successes) / len(self.failures)
```
or:
```python
return len(self.successes) / self.total * 100
```
if the rest of the system expects a 0.0 to 1.0 ratio.
### Expected failure
Tests around empty results or mixed outcomes should fail.
### Why this happens
A property is only as trustworthy as its formula.
### What it teaches
A short computed property still deserves focused tests.
### Recovery
Restore the original implementation.
Run `pytest tests/unit/test_models.py -v`.
## Experiment 10 - Removing failure tracking entirely
### Concept under test
Modeling failures explicitly preserves visibility.
### What to change
Imagine deleting `FailedDocument` and replacing failures with plain strings.
Do not keep this change.
Just sketch it mentally or try it briefly in a local edit.
### Expected design loss
You lose structure such as `source_path`, `error_type`, timestamp, and reusable formatting.
### Why this matters
A string is easy now and expensive later.
You cannot query, sort, or present rich failure data cleanly.
### What it teaches
A failure is domain data, not just a side effect.
## Debugging checklist for all experiments
After any break, ask these questions:
1. What assumption did the code rely on?
2. Which test noticed first?
3. Was the failure immediate or delayed?
4. Did the error message point to the real cause or only the symptom?
5. Would a beginner misread this failure?
6. What design rule does this reinforce?
## Reflection prompts after the lab
- Which failure taught you the most?
- Which failure felt most unfair until you understood it?
- Which design rule now feels earned rather than arbitrary?
- Which bug would be hardest to diagnose in a large codebase?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 1 — Python Core and Project Foundation · **Week 3 — OOP & Domain Modeling** · *break_it.md — the failure lab* (step 4 of 6 this week).

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
