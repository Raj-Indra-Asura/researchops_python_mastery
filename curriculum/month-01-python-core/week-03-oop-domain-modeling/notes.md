<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 03 — OOP and Domain Modeling:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 03 Notes - OOP and Domain Modeling
## 1. Chapter overview
Week 3 is where the codebase stops feeling like a collection of utility functions and starts feeling like a system.
In Week 1, you learned how to set up the project and run Python code reliably.
In Week 2, you worked with paths, exceptions, and logging.
Those were essential foundations.
Now you need a better language for the things the system actually cares about.
ResearchOps is not really about files.
It is about papers.
It is not really about strings.
It is about titles, authors, queries, tags, failures, and ingestion runs.
It is not really about random containers.
It is about domain concepts.
This week introduces object-oriented programming through a practical lens.
We are not studying classes because classes are fashionable.
We are studying classes because the code needs nouns with meaning.
A path to a PDF is one fact.
A parsed document is another fact.
A stored paper is another fact.
A failed ingestion attempt is another fact.
A query entered by a user is another fact.
If all of these are represented as loose dictionaries or unrelated strings, the program becomes harder to read, harder to test, and harder to extend.
If they are represented as explicit domain models, the code becomes more honest.
The key idea of this chapter is simple.
The code should speak the language of the problem domain.
That is what domain modeling means.
## 2. What you already know from Weeks 1 and 2
You already know how to create and activate a virtual environment.
You already know how to install dependencies.
You already know how to run a Python file or a test command.
You already know how imports work at a basic level.
You already know how to read function definitions.
You already know how to return values from functions.
You already know how to use `pathlib.Path` instead of stringly file manipulation.
You already know that exceptions make failure explicit.
You already know that logging records what the program did.
Those ideas are still active this week.
In fact, Week 3 depends on them.
`PaperId.from_path()` uses `Path`.
`FailedDocument` stores failure information clearly, which connects to exception handling and logging.
`Query` and `Tag` enforce rules at construction time, which is another form of defensive programming.
So Week 3 is not a brand-new universe.
It is a new layer built on the tools you already learned.
The difference is that earlier weeks focused on operations.
This week focuses on meaning.
## 3. What problem this week solves
Imagine building ResearchOps with only dictionaries.
A parsed paper might look like this:
```python
paper = {
    "id": "abc123",
    "title": "Attention Is All You Need",
    "source_path": "papers/attention.pdf",
    "text": "...",
    "num_pages": 15,
    "file_size_bytes": 912345,
}
```
At first glance, this seems fine.
Python dictionaries are flexible.
They are easy to type.
They are easy to print.
They are easy to pass around.
That flexibility is exactly the problem.
A dictionary does not tell you what fields are required.
A dictionary does not tell you what fields are optional.
A dictionary does not tell you what operations belong with the data.
A dictionary does not stop another function from using a slightly different key name.
One part of the code may use `source_path`.
Another may use `path`.
Another may use `file_path`.
A dictionary will not complain until much later.
A dictionary also does not express the difference between concepts.
Is this a raw parsed document?
Is it a stored paper?
Is it a failed document?
Is it a summary row for the UI?
The data may look similar, but the meanings are not the same.
That is why we need domain types.
A class lets you say, `This thing is a Paper.`
Another class lets you say, `This thing is a FailedDocument.`
Another class lets you say, `This thing is a Query.`
Now the code can be honest about what it is handling.
This reduces confusion.
This also improves design conversations.
It is easier to discuss `IngestionResult.success_rate` than `result_tuple[3]`.
It is easier to say `ParsedDocument.is_empty()` than `len(doc["raw_text"].strip()) == 0`.
This is the central problem Week 3 solves.
We are moving from unstructured containers to named domain models.
## 4. Beginner mental model
If object-oriented programming feels abstract, use this mental model.
A class is a plan for a kind of thing.
An instance is one actual thing created from that plan.
A class describes what data the thing has.
A class can also describe what behavior belongs to that thing.
For example, a `Paper` class says that every paper has an id, a title, a source path, some text, a page count, and a file size.
A `Paper` instance is one particular paper with actual values filled in.
Think of a spreadsheet template.
The template says what columns exist.
One row is an instance of the template.
Now improve the analogy.
A class is not just a row shape.
It can also have behavior.
A `Paper` can count its own words.
A `FailedDocument` can format its own summary.
An `IngestionResult` can compute its own total.
That is why classes are more than data containers.
They combine structure with meaning.
A second mental model is this.
A dictionary is like a cardboard box with labels taped on it.
A class is like a designed tool with named compartments and instructions.
You can put anything into a cardboard box.
That freedom is sometimes useful.
But a designed tool gives you consistency.
Consistency is what large codebases need.
## 5. Core vocabulary
### class
A class is a definition for a kind of object.
It describes attributes and methods.
It is written once and used to create many instances.
### instance
An instance is one concrete object created from a class.
If `Paper` is the class, then a specific research paper record is an instance.
### attribute
An attribute is a named piece of data stored on an object.
Examples on `Paper` include `title`, `text`, and `num_pages`.
### method
A method is a function defined inside a class.
It usually operates on the object's own data through `self`.
Examples include `word_count()` and `is_empty()`.
### dataclass
A dataclass is a Python class decorated with `@dataclass`.
Python generates common methods such as `__init__`, `__repr__`, and equality methods automatically.
Dataclasses reduce boilerplate for data-rich models.
### field
A field is a declared dataclass attribute.
You can customize its defaults with `field(...)`.
This is especially useful for timestamps and mutable containers.
### frozen
`frozen=True` makes a dataclass immutable after construction.
You cannot normally assign to its fields later.
This is a strong fit for value objects.
### immutable
An immutable object does not change after it is created.
Immutability makes equality, hashing, and reasoning easier.
### value object
A value object is defined by its value, not by identity.
Two `Tag("nlp")` objects should be considered the same if their normalized value is the same.
### domain model
A domain model is a type that represents a real concept in the problem space.
`Paper`, `FailedDocument`, and `IngestionResult` are domain models.
### invariant
An invariant is a rule that should always be true for valid objects.
For example, a query should not be empty or whitespace-only.
### `__post_init__`
`__post_init__` is a method dataclasses call immediately after the generated `__init__` finishes.
It is the right place for validation and normalization.
### `@property`
A property lets a method be accessed like an attribute.
It is useful for computed values such as `total` and `success_rate`.
### `__str__`
`__str__` defines the human-friendly string form of an object.
It is used by `print()` and f-strings.
### `__repr__`
`__repr__` defines the developer-oriented representation of an object.
Dataclasses generate a helpful one automatically.
### `StrEnum`
`StrEnum` is an enum whose members also behave like strings.
It is useful when you want symbolic names with string compatibility.
### composition
Composition means building an object out of other objects.
`IngestionResult` contains lists of `Paper` and `FailedDocument`.
### inheritance
Inheritance means one class extends another class.
It creates an `is-a` relationship.
This week mostly favors composition instead.
## 6. First principles: what is a class?
A class is a tool for giving shape and behavior to data.
It is not required for every problem.
It is useful when the same idea appears repeatedly in your code.
It is especially useful when the idea has both fields and behavior.
Here is a minimal class:
```python
class Counter:
    def __init__(self, start: int) -> None:
        self.value = start

    def increment(self) -> None:
        self.value += 1
```
This says that every `Counter` has a `value`.
It also says that a counter knows how to increment itself.
The important design question is not `Can I make a class?`
The important question is `Does a named type make the code clearer?`
A class is a good choice when:
- you have a concept that appears in many places
- you want consistent field names
- you want behavior close to the data it uses
- you want readers to understand the domain quickly
A class is not always the best choice.
A class may be overkill when:
- the data is trivial and local
- the structure is temporary and only used once
- you are just passing raw JSON across a boundary before conversion
The key is intentionality.
Do not use classes because they feel advanced.
Use them because they reduce ambiguity.
## 7. Class versus dictionary
This comparison matters because beginners often overuse one or the other.
A dictionary is best when the shape is dynamic or temporary.
A class is best when the shape is stable and meaningful.
Compare these two styles.
Dictionary style:
```python
paper = {
    "title": "Graph Search",
    "text": "...",
    "num_pages": 8,
}
```
Class style:
```python
paper = Paper(
    id="abc123",
    title="Graph Search",
    source_path="papers/graph-search.pdf",
    text="...",
    num_pages=8,
    file_size_bytes=4096,
)
```
The class version tells you more.
It says what the object is.
It says what fields are expected.
It makes autocomplete and type checking better.
It gives you methods such as `paper.word_count()`.
It also tells your teammates what language the system uses.
Use a dict when flexibility is the goal.
Use a class when clarity is the goal.
In application cores, clarity usually wins.
## 8. What is a dataclass?
Python classes can be written manually.
That often leads to boilerplate.
If a class mainly stores data, you would otherwise have to write an `__init__` that assigns every argument.
You might also want a readable `__repr__` and equality behavior.
Dataclasses automate this.
Example:
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```
Python expands this conceptually into something like:
```python
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other: object) -> bool:
        ...
```
You do not need to write all of that manually.
That is why dataclasses are powerful.
They make the important part of the class more visible.
The important part is the field list.
The field list is the model.
In Week 3, dataclasses are a perfect fit because our models are mostly data plus a few small methods.
## 9. What `@dataclass` generates
By default, `@dataclass` can generate:
- `__init__`
- `__repr__`
- `__eq__`
It can also influence ordering and hashing behavior depending on options.
The generated `__init__` turns your fields into constructor parameters.
The generated `__repr__` helps when printing objects during debugging.
The generated equality method compares objects by their fields.
This is especially useful for tests.
If two dataclass instances have the same relevant field values, they compare equal.
That means you can write expressive assertions.
You should still understand what is generated.
Dataclasses are not magic.
They are a code generation convenience built into Python.
## 10. `__init__` versus explicit constructors
When people first meet dataclasses, they sometimes think constructors have disappeared.
They have not.
The `__init__` still exists.
Python just writes it for you.
Sometimes you still want other constructors.
That is where `@classmethod` can help.
`PaperId.from_path()` is a good example.
The primary constructor for `PaperId` accepts a value.
The alternate constructor accepts a `Path` and derives the value.
This is a common pattern.
Let the normal constructor accept the already valid data.
Add named constructors for common creation workflows.
This improves readability.
`PaperId.from_path(path)` says more than manually calling hash functions in many places.
## 11. The mutable default trap
This is one of the most important beginner bugs in Python dataclasses.
Suppose you write this:
```python
from dataclasses import dataclass

@dataclass
class Paper:
    tags: list[str] = []
```
This looks harmless.
It is a bug.
That empty list is created once when the class definition runs.
Every instance then reuses the same list.
So if one paper appends a tag, another paper may unexpectedly see that tag too.
That is shared mutable state.
Shared mutable state is dangerous because it creates spooky action at a distance.
The fix is:
```python
from dataclasses import dataclass, field

@dataclass
class Paper:
    tags: list[str] = field(default_factory=list)
```
Now each new `Paper` gets its own fresh list.
`default_factory=list` means, `Call list() each time a new instance is created.`
The same idea applies to dictionaries and sets.
Use `field(default_factory=dict)` for dictionaries.
Use `field(default_factory=set)` for sets.
This is not a style preference.
It is a correctness rule.
## 12. Why `field(default_factory=...)` exists
`field()` is a helper for customizing dataclass fields.
It is how you express dynamic defaults.
A static default is fine for immutable values such as `None`, `0`, or `"pending"`.
A dynamic default is needed when a fresh object should be created for each instance.
Two common examples in ResearchOps are:
- timestamps
- containers
For timestamps, `field(default_factory=datetime.utcnow)` means `Call datetime.utcnow when the object is created.`
For containers, `field(default_factory=list)` means `Give each instance its own list.`
Without `default_factory`, many innocent-looking dataclasses become subtly wrong.
## 13. What does `frozen=True` mean?
A frozen dataclass is meant to be immutable.
After construction, direct assignment to fields is blocked.
Example:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Tag:
    value: str
```
After creating `Tag("ml")`, this should fail:
```python
tag.value = "ai"
```
Why is this useful?
Because some concepts should not change once created.
A paper's tag label as a value object should be stable.
A paper's identifier should be stable.
A query object that has been validated should not silently mutate into invalid input.
Immutability makes reasoning easier.
If you pass a `Tag` somewhere, you know it will remain that tag.
Immutability also enables hashing behavior in many cases.
Hashing requires stable values.
If values can change after being used as dictionary keys, lookups become unreliable.
That is why value objects are strong candidates for `frozen=True`.
## 14. Frozen dataclasses and hashing
Hashing is the process of turning a value into an integer-like fingerprint used by dictionaries and sets.
Python needs hashable objects for dictionary keys and set members.
Immutable objects are good candidates for hashing because their hash does not change during their lifetime.
That matters.
If an object's value changed after being placed in a dictionary, the dictionary could become inconsistent.
`PaperId` is a good example of a hash-friendly object.
It is small.
It is immutable.
It represents identity by value.
`Paper`, by contrast, is mutable and richer.
A mutable entity is usually not a great dictionary key.
That is why using `PaperId` as a key often makes more sense than using `Paper` itself.
## 15. `__post_init__`: what it is
Dataclasses generate `__init__` for you.
Sometimes you need to do more work right after initialization.
That is what `__post_init__` is for.
It runs automatically after the generated `__init__` finishes.
Typical uses include:
- validation
- normalization
- derived field cleanup
Here is a simple example:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Query:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("Query must not be empty or whitespace.")
```
The object is created only if the value is meaningful.
This is powerful.
It pushes invalid states out of the system early.
Now every caller can trust that a `Query` contains something real.
That is an invariant.
## 16. `__post_init__` with frozen dataclasses
A tricky detail appears when the dataclass is frozen.
Suppose you want to normalize a tag by lowercasing it and replacing spaces.
You cannot simply write `self.value = normalised` inside `__post_init__`.
The object is frozen.
Normal assignment is blocked.
Instead, you use:
```python
object.__setattr__(self, "value", normalised)
```
This is the sanctioned escape hatch for initialization-time normalization in frozen dataclasses.
Why is this allowed?
Because the object is still being finalized.
You are not mutating it later as normal program behavior.
You are completing construction.
This detail is important enough to remember.
If you forget it, your frozen value object will raise a `FrozenInstanceError` during creation.
## 17. `@property`: computed attributes
A property is a method that is accessed like an attribute.
Example:
```python
class Example:
    @property
    def total(self) -> int:
        return 3
```
You use it like this:
```python
example.total
```
not like this:
```python
example.total()
```
Why use a property?
Because some values behave conceptually like attributes even though they are computed.
`IngestionResult.total` is a great example.
A user of the class should think, `This object has a total.`
That total is derived from the three lists.
The user should not care that code runs behind the scenes.
Properties improve ergonomics when the value feels like state rather than an action.
Use a property for cheap, side-effect-free, derived values.
Use a regular method for actions, expensive work, or behavior that reads like a verb.
## 18. Why `total` and `success_rate` are properties
Consider `IngestionResult.total`.
We could store a `total` integer field and manually update it whenever a success, failure, or skipped path is added.
That would be fragile.
You would need to remember to update it everywhere.
Someone would forget.
Now `total` is wrong.
That is a synchronization bug.
A computed property avoids this.
It always derives from the actual lists.
The same reasoning applies to `success_rate`.
Its value is a function of the current state.
So it should be computed from the current state.
That keeps the model honest.
It also makes tests simpler.
## 19. `__str__` and `__repr__`
These two methods are easy to confuse.
`__str__` is for human-friendly output.
`__repr__` is for developer-friendly representation.
If you do nothing, a dataclass gives you a decent `__repr__`.
That is usually enough.
Example default repr:
```python
PaperId(value='abc123')
```
That is great for debugging.
But sometimes you want a cleaner display string.
For example, if you print a `PaperId` in logs, CLI output, or a summary, you may only want the raw identifier:
```python
abc123
```
That is why overriding `__str__` on `PaperId` helps.
It preserves the helpful dataclass `repr` while making user-facing output cleaner.
`__str__` should always return a string.
If you accidentally `print()` inside `__str__` and forget to return, Python raises a `TypeError`.
That is one of the break-it experiments this week.
## 20. Value objects versus entities
This distinction is one of the most important modeling ideas in the chapter.
An entity is something you track by identity over time.
A value object is something you understand entirely by its value.
A `Paper` is an entity.
Why?
Because it represents a specific paper stored in the system.
It has an identity.
Even if two papers had the same title, they might still be different papers.
A `Tag` is a value object.
Why?
Because a tag is just its normalized value.
If two tags both normalize to `machine-learning`, they are the same tag value.
A `Query` is also a value object.
A `PaperId` is a value object that acts as identity material.
That sounds paradoxical at first.
The important distinction is this.
The `Paper` entity is tracked as a thing in the system.
The `PaperId` is the value used to identify it.
Entity questions usually sound like:
- Which paper is this?
- Has this paper already been stored?
- Did this specific record change over time?
Value object questions usually sound like:
- Is this tag valid?
- Is this query empty?
- Are these two IDs equal?
## 21. What is an invariant?
An invariant is a rule that should always hold for valid objects.
If the invariant is broken, the object should not exist in that form.
Examples:
- A `Query` must not be empty or whitespace-only.
- A `Tag` should normalize to a usable value.
- A `PaperId` should contain a valid identifier string.
An invariant is not the same as a business workflow rule.
It is more basic.
It is about object validity.
If your object can exist in a nonsensical state, every other piece of code has to defend against that nonsense.
That spreads complexity everywhere.
If the object enforces its own invariant at creation time, the rest of the code becomes simpler.
This is one of the main reasons value objects are powerful.
They concentrate correctness near the boundary where data enters the domain.
## 22. StrEnum from first principles
Enums give names to a small set of allowed values.
Instead of using loose strings like `"pending"`, `"success"`, and `"failed"` everywhere, you can define an enum.
`StrEnum` is useful because each enum member also behaves like a string.
That means it plays nicely with serialization, comparisons, and display.
Example:
```python
from enum import StrEnum

class IngestionStatus(StrEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
```
Why is this better than raw strings?
Because it centralizes the allowed values.
Because it prevents typos from spreading silently.
Because code completion improves.
Because the set of states becomes discoverable.
Because readers immediately see that these values form a closed vocabulary.
Enums are especially helpful for statuses, modes, and small state machines.
## 23. Composition versus inheritance
Composition means one object contains other objects.
Inheritance means one class extends another class.
This week mostly uses composition.
`IngestionResult` has lists of `Paper`, `FailedDocument`, and `Path`.
That is a `has-a` relationship.
An ingestion result has successes.
It has failures.
It has skipped files.
Inheritance would ask a different question.
It would ask whether one model is a specialized kind of another model.
That is usually not what we need here.
A `FailedDocument` is not a kind of `Paper`.
A `ParsedDocument` is not a kind of `Paper` either.
They are related concepts in a workflow, not a class hierarchy.
Composition is simpler and more honest.
It says, `This result contains these things.`
That matches the domain.
## 24. Domain language matters
Software design is partly a naming problem.
When the names are wrong, the design usually becomes blurry.
When the names are right, the design becomes easier to think about.
Compare these names:
- `data`
- `item`
- `record`
- `result`
These are generic.
Now compare:
- `Paper`
- `ParsedDocument`
- `FailedDocument`
- `IngestionResult`
These are specific.
Specific names carry domain meaning.
They tell new contributors how to think.
They also influence where behavior belongs.
`FailedDocument.summary()` makes sense.
`Item.summary()` tells you almost nothing.
This is why domain modeling is not just about data structure.
It is about creating a shared language for the team and the code.
## 25. Hashing with `hashlib.sha256`
A hash function takes some input and produces a fixed-size output.
For `sha256`, the output is a 256-bit digest, usually shown as 64 hexadecimal characters.
Hashes are useful because:
- the same input always gives the same output
- small input changes produce very different outputs
- the output length is fixed
In `PaperId.from_path()`, hashing serves a practical goal.
We want a stable identifier derived from the normalized path.
We do not want to store the entire path as the ID.
We also want the same path to produce the same identifier each time.
That is what hashing gives us.
The code uses `hexdigest()[:16]`.
That means it computes the full hexadecimal digest and keeps the first 16 characters.
This is shorter and easier to read while still being stable.
A shorter hash increases collision risk compared with the full digest, but for this learning-stage project and path-derived IDs it is a reasonable tradeoff.
The deeper lesson is not the exact hash length.
The deeper lesson is that an identifier can be derived from value in a reproducible way.
## 26. ResearchOps pipeline in domain terms
Let us describe the ingestion flow using domain language.
A user points ResearchOps at a directory.
The system discovers candidate PDF paths.
Each path is handed to a parser.
The parser returns a `ParsedDocument`.
A `ParsedDocument` is still an intermediate object.
It represents what the parser found.
It has not necessarily been accepted into the system as a clean, stored paper.
The ingestion service then decides what to do.
If the parsed document is valid and useful, it becomes a `Paper`.
If parsing fails or the result is unusable, we create a `FailedDocument`.
As the directory run continues, the system accumulates all of these outcomes into an `IngestionResult`.
That single object is then easy to hand to the CLI, an API response builder, or a logger.
This pipeline is a great example of why domain modeling matters.
Each stage has a distinct concept.
That clarity supports better architecture.
## 27. Where these models live in the architecture
These models live in `src/researchops/core/`.
That location matters.
The `core/` layer is the heart of the system.
It should only depend on stable concepts and the standard library.
It should not import from `cli/`.
It should not import from `api/`.
It should not import from `storage/`.
It should not import from `ml/`.
Why?
Because the domain should not know how users interact with it.
The domain should not know which database stores it.
The domain should not know which web framework exposes it.
The domain should describe the problem space.
Outer layers should adapt themselves to the domain, not the other way around.
If you violate this direction, the core becomes hard to reuse and hard to test.
## 28. ResearchOps-specific objects at a glance
Here is the Week 3 cast of characters.
`PaperId` is a stable ID value object.
`Paper` is the stored paper entity.
`ParsedDocument` is raw parser output.
`FailedDocument` is explicit failure tracking.
`IngestionResult` summarizes an entire run.
`SearchResult` represents one ranked hit.
`Query` represents a validated search query.
`Tag` represents a normalized label.
Together, these types give the codebase a shared vocabulary.
That is the big win.
## 29. Code deep dive: `PaperId`
Here is the chapter version we are studying.
```python
@dataclass(frozen=True)
class PaperId:
    """Value object: stable, content-derived identifier for a paper.
    Derived from the SHA-256 of the source file path (normalised).
    """
    value: str

    @classmethod
    def from_path(cls, path: Path) -> PaperId:
        digest = hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16]
        return cls(value=digest)

    def __str__(self) -> str:
        return self.value
```
Now we will explain every line.
### `@dataclass(frozen=True)`
This tells Python to generate dataclass behavior.
It also says the object should be immutable after creation.
That is appropriate because an identifier should not change.
### `class PaperId:`
This creates a named type for paper identifiers.
The name matters.
It tells readers that this string is not just any string.
It is a paper ID.
### docstring line 1
`Value object: stable, content-derived identifier for a paper.`
This explains both category and purpose.
It is a value object.
Its job is stable identification.
### docstring line 2
`Derived from the SHA-256 of the source file path (normalised).`
This tells you how it is produced.
It also signals a design choice.
The identifier is derived, not random.
### `value: str`
This is the one field.
The actual stored representation is a string.
The class wraps the string in a meaningful type.
That is often enough to justify a value object.
### `@classmethod`
This decorator means the method belongs to the class, not an instance.
It is used for alternate constructors.
### `def from_path(cls, path: Path) -> PaperId:`
This method says, `Given a path, build a PaperId.`
The return type makes the method self-documenting.
### `digest = ...`
This line performs the conversion from path to stable digest.
It is dense, so break it apart.
### `path.resolve()`
This normalizes the path to an absolute resolved version.
That reduces ambiguity.
Relative and absolute references to the same file become more consistent.
### `str(path.resolve())`
Hash functions operate on bytes, not `Path` objects.
So we first turn the path into a string.
### `.encode()`
A SHA-256 hash works on bytes.
Encoding converts the string into bytes.
By default, Python uses UTF-8.
### `hashlib.sha256(...)`
This constructs a SHA-256 hashing object for the bytes.
### `.hexdigest()`
This returns the digest as a hexadecimal string.
That string is deterministic.
The same input bytes produce the same hex string.
### `[:16]`
This slices the hex digest to its first 16 characters.
That makes the ID shorter and easier to display.
It is a tradeoff between brevity and collision resistance.
### `return cls(value=digest)`
This creates a new `PaperId` instance from the computed digest.
Using `cls` instead of the literal class name helps subclasses and keeps the method idiomatic.
### `def __str__(self) -> str:`
This defines the human-facing string form.
### `return self.value`
Now `str(paper_id)` returns the raw identifier, not `PaperId(value='...')`.
That is exactly what you want in logs, f-strings, and user-facing output.
## 30. Why `PaperId` is a value object
`PaperId` is tiny.
It has one job.
Its meaning is fully captured by its `value`.
Two `PaperId` objects with the same value should be considered equal.
You do not care which instance was created first.
You care about the value.
That is classic value-object behavior.
It is also why `frozen=True` fits.
An identifier that changes after construction is a design smell.
## 31. Code deep dive: `Paper`
Here is the Week 3 `Paper` model.
```python
@dataclass
class Paper:
    """Represents a research paper stored in the system."""
    id: str
    title: str
    source_path: str
    text: str
    num_pages: int
    file_size_bytes: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    author: str | None = None
    abstract: str | None = None
    tags: list[str] = field(default_factory=list)

    def word_count(self) -> int:
        return len(self.text.split())

    def is_empty(self) -> bool:
        return len(self.text.strip()) == 0
```
Now unpack every field and choice.
### `@dataclass`
`Paper` is data-rich and behavior-light.
That makes dataclass a strong fit.
We want a generated initializer and readable representation.
### `class Paper:`
This is the central domain entity for stored research papers.
It is the thing later layers will retrieve, search, display, and analyze.
### `id: str`
This is the paper's identifier.
In practice it will often come from `PaperId`.
The field is stored as a string on the entity for convenience and serialization simplicity.
### `title: str`
This is the human-readable title.
It is central domain data.
A `Paper` without a meaningful title may still exist temporarily depending on ingestion stage, but titles are conceptually important.
### `source_path: str`
This stores where the paper came from.
It is intentionally a string, not a `Path`.
Why?
Because persisted objects often need JSON-friendly fields.
Strings serialize more naturally than `Path` objects.
This is a subtle but practical design choice.
### `text: str`
This is the extracted full text.
It is one of the most important fields for later search and ML features.
### `num_pages: int`
This stores the page count.
It is a structural attribute of the source document.
### `file_size_bytes: int`
This stores file size in bytes.
It is useful for diagnostics, reporting, and sanity checks.
### `created_at: datetime = field(default_factory=datetime.utcnow)`
The timestamp defaults to the moment the object is created.
`default_factory` ensures a fresh timestamp per instance.
If you wrote `datetime.utcnow()` directly in the class body, it would run once when the class is defined, which would be wrong.
### `author: str | None = None`
This is optional metadata.
Not every parser or document will yield a clean author value.
`None` communicates absence clearly.
### `abstract: str | None = None`
This is also optional.
Many real ingestion pipelines deal with partial metadata.
Optional fields let the model reflect that reality.
### `tags: list[str] = field(default_factory=list)`
This stores associated tags.
Using `default_factory=list` prevents shared mutable state.
Each paper gets its own list.
### `def word_count(self) -> int:`
This method computes a derived metric from the paper's own text.
It belongs on the model because it depends only on the model's data and is meaningful in domain language.
### `return len(self.text.split())`
This is a simple approximate word count.
`split()` breaks on whitespace.
It is not linguistically sophisticated, but it is a useful default.
### `def is_empty(self) -> bool:`
This asks whether the extracted text is meaningfully empty.
That is a valid domain question.
### `return len(self.text.strip()) == 0`
`strip()` removes leading and trailing whitespace.
If nothing remains, the content is effectively empty.
## 32. Why `Paper` is mutable
`Paper` is not frozen.
That is intentional.
Entities often evolve over time.
A paper might gain tags.
A paper might later gain an author field after metadata extraction improves.
A paper might be enriched with an abstract.
Mutability is not always bad.
Uncontrolled mutability is bad.
For entities, controlled mutability is often realistic.
That is why the design uses frozen value objects and mutable entities.
## 33. Code deep dive: `ParsedDocument`
Here is the model.
```python
@dataclass
class ParsedDocument:
    """Raw result of parsing a single PDF file.
    Intermediate object — not yet persisted.
    """
    source_path: Path
    raw_text: str
    num_pages: int
    file_size_bytes: int
    metadata: dict[str, str] = field(default_factory=dict)

    def is_empty(self) -> bool:
        return len(self.raw_text.strip()) == 0
```
Now explain it.
### Why this class exists at all
Beginners often ask, `Why not create a Paper immediately?`
Because pipeline stages matter.
`ParsedDocument` represents parser output.
Parser output is not the same thing as a stored domain entity.
The parser may return partial data.
The parser may return metadata that still needs cleaning.
The parser may produce empty or invalid text.
The system should be able to talk about that intermediate state explicitly.
That is what this class enables.
### `source_path: Path`
Unlike `Paper.source_path`, this uses `Path`.
That fits the stage.
At parse time, you are still dealing with filesystem-native values.
You have not crossed into a serialization-oriented representation yet.
### `raw_text: str`
This field is called `raw_text`, not just `text`.
That word matters.
It tells you the content is direct parser output.
It may still need cleaning.
### `num_pages: int`
Page count is known at parse time.
It belongs here too.
### `file_size_bytes: int`
File size also belongs here.
The parser knows which file it read.
### `metadata: dict[str, str] = field(default_factory=dict)`
Parsers often extract extra fields such as title or author.
A metadata dictionary allows flexible storage of those parser-level details.
`default_factory=dict` avoids the same shared mutable default bug we discussed for lists.
### `is_empty()`
This method checks whether the parser produced meaningful text.
That is useful before deciding whether to promote the object into a `Paper`.
## 34. Why `ParsedDocument` is separate from `Paper`
This separation is a design lesson worth repeating.
`ParsedDocument` and `Paper` may look similar.
They are not duplicates.
They live at different points in the workflow.
`ParsedDocument` says, `Here is what the parser found.`
`Paper` says, `Here is what the system stores as a paper.`
The first is transient and parser-facing.
The second is stable and domain-facing.
If you collapse them into one type too early, you blur stage boundaries.
That makes debugging harder.
It also makes later transformation logic less explicit.
## 35. Code deep dive: `FailedDocument`
Here is the model.
```python
@dataclass
class FailedDocument:
    """Tracks a document that failed during ingestion."""
    source_path: Path
    error_message: str
    error_type: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)

    def summary(self) -> str:
        return f"[{self.error_type}] {self.source_path.name}: {self.error_message}"
```
This class is deceptively important.
### Why model failure explicitly?
Many beginner programs treat failures as side effects.
They log an error and move on.
That loses structure.
If failures are real outcomes in your system, they deserve a real model.
Tracking failures explicitly means you can:
- report them cleanly
- inspect them in tests
- serialize them later
- count them
- analyze common failure types
That is why `FailedDocument` exists.
### `source_path: Path`
This identifies which file failed.
That is essential for diagnosis.
### `error_message: str`
This stores the human-readable error message.
### `error_type: str`
This stores a classification such as `ParseError` or `PermissionError`.
This is useful because a short type label is easier to aggregate than a full message.
### `occurred_at: datetime = field(default_factory=datetime.utcnow)`
A timestamp makes the failure a richer event.
It helps with debugging and operational visibility.
### `summary()`
This is a presentation-friendly method.
It belongs here because it is based entirely on the object's own fields and expresses a common view of the failure.
The summary string is also great for CLI output.
## 36. Why `summary()` belongs on `FailedDocument`
A helpful rule is this.
If formatting logic depends entirely on one object's own data and represents a common meaning of that object, it often belongs on the object.
`FailedDocument.summary()` fits this rule.
Callers should not have to rebuild this formatting pattern everywhere.
Putting the logic on the model keeps representation consistent.
## 37. Code deep dive: `IngestionResult`
Here is the core model.
```python
@dataclass
class IngestionResult:
    """Collects everything that happened during one ingest_directory run."""
    run_id: str
    directory: Path
    started_at: datetime
    finished_at: datetime | None = None
    successes: list[Paper] = field(default_factory=list)
    failures: list[FailedDocument] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.successes) + len(self.failures) + len(self.skipped)

    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return len(self.successes) / self.total
```
This object is an aggregation model.
It represents a whole run, not just one document.
### `run_id: str`
This identifies the run.
It lets logs, summaries, and future APIs refer to one ingestion session.
### `directory: Path`
This stores the directory that was ingested.
That is part of the run's identity and context.
### `started_at: datetime`
This records when the run began.
### `finished_at: datetime | None = None`
This may be absent at first.
That is why it is optional.
A running process often has a start time before it has an end time.
### `successes: list[Paper]`
These are the papers that were ingested successfully.
This is composition.
The run result contains `Paper` objects.
### `failures: list[FailedDocument]`
These are the failed outcomes.
Again, composition.
### `skipped: list[Path]`
These are paths that were intentionally skipped.
This is a third distinct category.
Not every non-success is a failure.
Sometimes the system chooses not to process a file.
### `total`
This property counts all outcome buckets.
### `success_rate`
This property returns the fraction of successful documents.
The guard for zero total avoids division-by-zero errors.
That is both mathematically necessary and semantically appropriate.
An empty run has a success rate of `0.0` in this design.
## 38. Composition in `IngestionResult`
`IngestionResult` is a clean composition example.
It does not inherit from `Paper`.
It does not inherit from `FailedDocument`.
That would be nonsense.
Instead, it contains collections of those objects.
This is how many real systems are designed.
Large workflows often need summary objects that group many other domain objects together.
Composition keeps the design simple.
## 39. Code deep dive: `Query` value object
A representative Week 3 version looks like this.
```python
@dataclass(frozen=True)
class Query:
    """A search query. Must not be empty."""
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("Query must not be empty or whitespace.")

    def __str__(self) -> str:
        return self.value
```
Explain each part.
### `@dataclass(frozen=True)`
A query value object should be stable once validated.
That makes immutability a good fit.
### `value: str`
The core content is just text.
Wrapping it in a type lets us enforce rules.
### `__post_init__`
The query validates itself immediately.
If the text is blank after trimming whitespace, the object is rejected.
That means the rest of the system can trust `Query` values.
### `self.value.strip()`
This ignores meaningless surrounding whitespace when deciding validity.
A string containing only spaces is not a meaningful query.
### `raise ValueError(...)`
This signals invalid construction.
Some codebases may later use a custom exception instead.
The teaching point is the same.
Invalid value objects should fail early.
### `__str__`
Returning the raw value keeps printing simple.
## 40. Code deep dive: `Tag` value object
A representative Week 3 version looks like this.
```python
@dataclass(frozen=True)
class Tag:
    """A normalised tag: lowercase, hyphens instead of spaces."""
    value: str

    def __post_init__(self) -> None:
        normalised = re.sub(r"[^a-z0-9-]", "-", self.value.lower().strip())
        normalised = re.sub(r"-+", "-", normalised).strip("-")
        if not normalised:
            raise ValueError(f"Invalid tag: {self.value!r}")
        object.__setattr__(self, "value", normalised)

    def __str__(self) -> str:
        return self.value
```
Now explain the logic slowly.
### Lowercasing
Tags should be normalized so `Machine Learning` and `machine learning` become the same canonical form.
Lowercasing is part of that normalization.
### `strip()`
Leading and trailing whitespace should not matter.
### `re.sub(r"[^a-z0-9-]", "-", ...)`
This replaces characters that are not lowercase letters, digits, or hyphens with `-`.
That means spaces and punctuation become separators.
### `re.sub(r"-+", "-", normalised)`
This collapses repeated hyphens into a single hyphen.
Without this, messy input could create ugly tags like `machine---learning`.
### `.strip("-")`
This removes hyphens from the beginning and end.
So `"!!!data science!!!"` becomes `"data-science"`, not `"---data-science---"`.
### `if not normalised:`
If everything collapses away, the tag is invalid.
For example, an input of only punctuation should not produce an empty tag silently.
### `object.__setattr__(...)`
Because the dataclass is frozen, we use the special low-level assignment helper during initialization.
### `__str__`
Printing a tag should produce the normalized value.
## 41. Why `Query` and `Tag` are excellent teaching examples
They are small.
They have clear invariants.
They show why `__post_init__` exists.
They show why `frozen=True` matters.
They show how validation and normalization can live on the model itself.
They also show a key design lesson.
Wrapping a primitive in a small type can create big clarity benefits.
This is often called avoiding primitive obsession.
A raw string can mean anything.
A `Query` or `Tag` means one specific thing.
## 42. `SearchResult` briefly
Even though the chapter focuses mainly on the ingestion models and value objects, `SearchResult` also teaches something useful.
A search hit is not just a paper.
It is a paper plus ranking information and often a snippet.
That is why a dedicated model exists.
Modeling search results explicitly prevents accidental confusion between stored paper data and retrieval-layer output.
Typed outputs matter here too.
## 43. How tests teach the model
Tests are not only about catching regressions.
They also document intended behavior.
When you read a good model test, you learn what the model promises.
That is why Week 3 asks you to read tests carefully.
The tests are tiny design documents.
Let us walk through the representative tests.
## 44. `test_word_count`
Representative test:
```python
def test_word_count(self) -> None:
    paper = Paper(id="abc", title="T", source_path="p.pdf", text="hello world foo", num_pages=1, file_size_bytes=100)
    assert paper.word_count() == 3
```
What does this verify?
It verifies that the method derives count from the text.
It also communicates the intended counting approach.
This is whitespace-based counting, not advanced NLP tokenization.
That matters because future contributors should not guess wrong.
## 45. `test_is_empty_true_for_whitespace`
Representative test:
```python
def test_is_empty_true_for_whitespace(self) -> None:
    paper = Paper(id="abc", title="T", source_path="p.pdf", text="   \n  ", num_pages=1, file_size_bytes=100)
    assert paper.is_empty()
```
This checks an edge case.
Empty content is not only the empty string.
Whitespace-only content should also count as empty.
That test protects against naive implementations such as `self.text == ""`.
## 46. `test_tags_default_to_empty_list`
Representative test:
```python
def test_tags_default_to_empty_list(self) -> None:
    p1 = Paper(id="a", title="T", source_path="p.pdf", text="x", num_pages=1, file_size_bytes=1)
    p2 = Paper(id="b", title="T", source_path="p.pdf", text="x", num_pages=1, file_size_bytes=1)
    p1.tags.append("ml")
    assert p2.tags == []
```
This test protects against the shared mutable default bug.
It is one of the most valuable small tests in the file.
Notice that the test is not checking syntax.
It is checking object independence.
## 47. `test_total_counts_all_buckets`
Representative test:
```python
def test_total_counts_all_buckets(self) -> None:
    result = IngestionResult(run_id="r", directory=Path("/tmp"), started_at=datetime.utcnow())
    result.successes.append(...)
    result.failures.append(...)
    result.skipped.append(Path("/tmp/skip.pdf"))
    assert result.total == 3
```
This confirms that `total` reflects all three categories.
That is a design statement.
A skipped file still counts as part of what happened during the run.
## 48. `test_success_rate_zero_when_empty`
Representative test:
```python
def test_success_rate_zero_when_empty(self) -> None:
    result = IngestionResult(run_id="r", directory=Path("/tmp"), started_at=datetime.utcnow())
    assert result.success_rate == 0.0
```
This protects against division by zero.
It also documents the chosen semantic behavior for an empty run.
The design says that no processed items means a success rate of `0.0`.
That is a clear contract.
## 49. `test_from_path_is_stable`
Representative test:
```python
def test_from_path_is_stable(self, tmp_path: Path) -> None:
    f = tmp_path / "paper.pdf"
    f.touch()
    id1 = PaperId.from_path(f)
    id2 = PaperId.from_path(f)
    assert id1 == id2
```
This checks determinism.
The same input path should produce the same ID.
If that failed, re-ingestion could create duplicates unpredictably.
## 50. `test_str_returns_value`
Representative test:
```python
def test_str_returns_value(self) -> None:
    pid = PaperId(value="abc123")
    assert str(pid) == "abc123"
```
This checks a small but useful representation contract.
It ensures CLI and logging code can rely on a clean string form.
## 51. `Query` tests
Representative tests include:
```python
def test_valid_query(self) -> None:
    q = Query("machine learning")
    assert str(q) == "machine learning"


def test_empty_query_raises(self) -> None:
    with pytest.raises(ValueError):
        Query("   ")
```
These tests verify the invariant.
They say valid queries are preserved and invalid empty queries are rejected.
Notice how the constructor itself is being tested.
That is appropriate for value objects.
## 52. `Tag` tests
Representative tests include:
```python
def test_normalises_to_lowercase(self) -> None:
    t = Tag("Machine Learning")
    assert t.value == "machine-learning"


def test_empty_raises(self) -> None:
    with pytest.raises(ValueError):
        Tag("  ")
```
These tests check two essential things.
First, normalization happens automatically.
Second, invalid final values are rejected.
That is exactly what a value-object test suite should do.
## 53. Common beginner mistake 1: treating classes as only OOP ceremony
Some beginners learn classes as syntax with little purpose.
That leads to two bad extremes.
One extreme is `I will put everything in classes.`
The other is `Classes are pointless; I can always use dicts.`
Both miss the point.
Classes are useful when they clarify domain meaning and localize behavior.
The right question is always, `Does this named type reduce ambiguity?`
## 54. Common beginner mistake 2: using mutable defaults directly
We already studied this, but it deserves repetition.
`tags: list[str] = []` is a bug.
`metadata: dict[str, str] = {}` is a bug.
The fix is `field(default_factory=...)`.
Memorize the rule.
## 55. Common beginner mistake 3: confusing entities and value objects
If you freeze everything, your entities become awkward.
If you make every primitive into a mutable entity, your design becomes noisy.
Ask what the concept is.
Does it have identity over time?
Then it may be an entity.
Is it fully described by its value?
Then it may be a value object.
## 56. Common beginner mistake 4: putting validation everywhere except the boundary
If `Query` can be blank, then every search function has to re-check for blank queries.
That spreads defensive code.
Better design is to reject invalid queries once at construction time.
Then downstream code becomes simpler.
## 57. Common beginner mistake 5: storing derived values that can go stale
If you store `total` as a field and forget to update it, it becomes wrong.
If you compute it from the source lists, it stays truthful.
Prefer derived properties when the value should always reflect current state.
## 58. Common beginner mistake 6: making `__str__` too clever
`__str__` should be simple.
It should return a meaningful string.
It should not print, mutate, or perform expensive work.
It is representation logic, not workflow logic.
## 59. Common beginner mistake 7: using inheritance because it feels advanced
Do not create inheritance hierarchies unless the `is-a` relationship is truly strong.
`ParsedDocument` is not a `Paper`.
`FailedDocument` is not a `Paper`.
For this chapter, composition is the cleaner choice.
## 60. Common beginner mistake 8: ignoring architecture boundaries
If core models import database code, the heart of your system becomes tied to infrastructure.
That makes tests heavier.
That makes refactoring harder.
That violates the direction of dependency.
## 61. Common beginner mistake 9: assuming type hints enforce runtime correctness automatically
Type hints help readers, IDEs, and static tools.
They do not automatically reject bad runtime values in plain dataclasses.
If runtime validation matters, you must add it explicitly or use a tool designed for it.
## 62. Reading tests as design documentation
Read tests like prose, not just as green-or-red gates.
A well-named test tells you what behavior matters and what regression it prevents.
## 63. Debugging guidance: start with the model question
When a model feels wrong, ask what real concept it represents, what stage it belongs to, and what invariant may be broken.
Those questions usually guide you faster than random edits.
## 64. Debugging guidance: inspect generated dataclass behavior
Use dataclass `repr` output and `dataclasses.fields(...)` to verify what the class actually contains.
Many model bugs become obvious once you inspect the real field values.
## 65. Debugging guidance: isolate invariants
Test the smallest input that should pass and the smallest input that should fail.
That pattern is especially effective for `Query`, `Tag`, and other value objects.
## 66. Debugging guidance: compare representations
If output is confusing, compare `str(obj)` and `repr(obj)`.
Representation bugs are often smaller and more local than data bugs.
## 67. Debugging guidance: follow the boundary
Ask where the invalid state first entered the system.
If bad input crossed the boundary, the value object or parser may need to reject it earlier.
## 68. Design tradeoff: dataclass versus plain class
Dataclasses are ideal here because the models are mostly data plus a little behavior.
Use a manual class only when initialization or behavior becomes complex enough to need the extra control.
## 69. Design tradeoff: dataclass versus Pydantic
Dataclasses teach the core modeling ideas clearly.
Pydantic is excellent later at boundaries when you need stronger runtime validation and parsing.
## 70. Design tradeoff: frozen versus mutable
Freeze small value objects whose meaning should not drift.
Keep entities and run-aggregation models mutable when their state naturally grows over time.
## 71. Design tradeoff: dict versus class
Use a dict for temporary or loose transport data.
Use a class when the concept is central, stable, and worth naming precisely.
## 72. Testing implications of domain models
Named models create cleaner tests because you can construct meaningful objects directly and assert against their behavior.
Dataclass representations also make failures easier to read.
## 73. Tests should verify behavior
The best tests check meaning, not just construction.
That is why Week 3 tests focus on `word_count()`, `is_empty()`, stable IDs, normalized tags, and computed properties.
## 74. Architecture implications of Week 3
The architecture rule for this course is strict.
`core/` must not import from `cli/`, `api/`, `storage/`, `ml/`, `workers/`, or `search/`.
This is not because the course loves arbitrary rules.
It is because the domain should stay portable and reusable.
If the core knows about SQLite, then switching storage becomes harder.
If the core knows about FastAPI, then the web framework leaks into the heart of the system.
If the core knows about CLI output formatting, the domain becomes presentation-aware.
The right direction is inward.
CLI, API, and storage all depend on the core concepts.
The core depends only on the standard library and other core concepts.
## 75. Why this matters for future service design
Later service objects should accept and return core models, not infrastructure details.
That only works if the domain language is clear now.
## 76. Connection to ML and AI
Machine learning does not reduce the need for good domain models.
It increases it, because predictions, feature rows, embeddings, and evaluation outputs all benefit from typed structures and stable identifiers.
## 77. ML-specific example: feature rows
Before data becomes arrays or tensors, it is often easiest to reason about as named records.
Clear typed rows make preprocessing easier to debug.
## 78. ML-specific example: model outputs
A tuple like `(paper_id, label, score)` works, but a named result model is clearer.
Week 3 is teaching the habit of replacing anonymous shapes with meaningful types.
## 79. Why beginner-readable code matters here
Short methods, descriptive names, and visible types make the domain easier to learn and maintain.
Beginner-readable does not mean simplistic; it means intentional.
## 80. Why behavior belongs near data
Methods such as `word_count()`, `summary()`, and properties such as `success_rate` belong near the fields they interpret.
That keeps discovery and reuse simple.
## 81. When behavior should not go on the model
Workflow logic involving I/O, repositories, network calls, or orchestration belongs in services, not in core models.
Week 3 is about placing small, local behavior on the right noun.
## 82. A note on serialization choices
`ParsedDocument.source_path` can stay as a `Path` during parsing, while `Paper.source_path` may be stored as `str` for persistence and transport convenience.
That difference reflects stage, not inconsistency.
## 83. A note on optional fields
Optional fields such as `author` and `abstract` reflect the reality of partial metadata.
A good model can represent incomplete but still valid information.
## 84. A note on approximate methods
`word_count()` is intentionally simple.
A useful approximate method is often better than overengineering too early.
## 85. Building a `Paper` reads like domain language
Constructing a `Paper` with named fields makes the call site self-explanatory.
That readability is one of the strongest practical arguments for explicit models.
## 86. Calling `word_count()` reads cleanly
`paper.word_count()` tells you both what is being measured and where the logic lives.
Good method names turn code into readable sentences.
## 87. Checking `is_empty()` reads cleanly
`paper.is_empty()` is easier to read and reuse than repeating string-trimming logic throughout the codebase.
That is encapsulation in a very practical form.
## 88. Readable call sites matter
A design is not only about how a class looks when defined.
It is also about how natural the object feels to use.
## 89. Factory methods improve consistency
`PaperId.from_path()` centralizes one canonical construction path.
That prevents hashing logic from drifting across callers.
## 90. Centralized rules prevent duplication
If every caller hand-built IDs, some would forget `resolve()`, slicing, or even the hash function.
A single constructor keeps the invariant in one place.
## 91. Think in stages, not only shapes
`ParsedDocument` and `Paper` can resemble each other structurally while still representing different workflow stages.
That distinction is a major domain-modeling lesson.
## 92. Failure tracking is first-class design
A structured `FailedDocument` preserves more meaning than a bare log line.
That makes debugging, reporting, and future APIs better.
## 93. The deeper lesson of Week 3
This week is really teaching you to identify the nouns of the system, decide which rules belong on them, and keep those rules close to the data they describe.
## 94. Mini quiz 1
Question:
What problem does `field(default_factory=list)` solve?
Answer:
It ensures each dataclass instance gets its own fresh list instead of sharing one list created at class definition time.
## 95. Mini quiz 2
Question:
Why is `PaperId` a good candidate for `frozen=True`?
Answer:
Because an identifier should be stable after creation, and immutability supports reliable equality, hashing, and reasoning.
## 96. Mini quiz 3
Question:
Why is `IngestionResult.total` a property instead of a stored integer field?
Answer:
Because it is derived from the current lists of successes, failures, and skipped files, and computing it avoids stale synchronization bugs.
## 97. Mini quiz 4
Question:
What is the difference between `ParsedDocument` and `Paper`?
Answer:
`ParsedDocument` is intermediate parser output, while `Paper` is the stored domain entity the system works with after successful ingestion.
## 98. Mini quiz 5
Question:
Why does `Query` validate in `__post_init__`?
Answer:
Because value objects should reject invalid states at construction time so downstream code can rely on their invariants.
## 99. Mini quiz 6
Question:
What is one advantage of `StrEnum` over loose string constants?
Answer:
It centralizes allowed values in a discoverable named type while still behaving like strings when needed.
## 100. Mini quiz 7
Question:
Why is composition a better fit than inheritance for `IngestionResult`?
Answer:
Because an ingestion result has papers and failures; it is not a specialized kind of either one.
## 101. Mini quiz 8
Question:
What is the purpose of overriding `__str__` on `PaperId`?
Answer:
To return the raw identifier string for clean user-facing output instead of the default dataclass representation.
## 102. Explain-it-aloud prompt 1
Explain to an imaginary beginner why classes are not just `fancy dicts`.
Do not mention inheritance.
Focus on naming, invariants, and behavior.
## 103. Explain-it-aloud prompt 2
Explain the shared mutable default bug without using the phrase `default_factory` until the end.
This forces you to explain the underlying idea first.
## 104. Explain-it-aloud prompt 3
Explain the difference between an entity and a value object using `Paper` and `Tag`.
Keep your explanation under one minute.
## 105. Explain-it-aloud prompt 4
Explain why `core/` cannot import from `storage/` or `cli/`.
Use the words `dependency direction` and `testability`.
## 106. Explain-it-aloud prompt 5
Explain why a future ML system still needs typed domain models.
Use the phrases `stable identifier` and `typed output`.
## 107. What to memorize
Memorize these rules exactly.
- Use `field(default_factory=list)` for list defaults.
- Use `field(default_factory=dict)` for dict defaults.
- Use `frozen=True` for small immutable value objects.
- Use `__post_init__` for validation and normalization.
- Use `object.__setattr__` inside frozen `__post_init__` when normalization changes values.
- Use `@property` for cheap derived values that read like attributes.
- Keep `core/` free from infrastructure imports.
These are worth memorizing because they prevent common bugs.
## 108. What to understand deeply
Do not stop at memorization.
Understand these ideas at a deeper level.
- Why named domain types reduce ambiguity.
- Why stage boundaries matter in modeling.
- Why value objects protect invariants.
- Why entity identity differs from value equality.
- Why composition often beats inheritance in workflow modeling.
- Why architecture boundaries protect future flexibility.
If you understand these deeply, you will be able to design new models, not just repeat old ones.
## 109. What not to worry about yet
Do not worry yet about advanced OOP patterns.
Do not worry yet about multiple inheritance.
Do not worry yet about metaclasses.
Do not worry yet about abstract base classes versus protocols in detail.
Do not worry yet about ORM models.
Do not worry yet about highly optimized hash collision analysis.
Those topics have their place.
They are not the main lesson of Week 3.
The main lesson is modeling meaning clearly.
## 110. Bridge to Week 4
Week 4 moves toward packaging and CLI structure.
That means you will soon care more about how the program is assembled and invoked.
But the CLI can only be clean if the domain nouns underneath it are clean.
A command like `researchops scan` becomes easier to design when you already have `Paper`, `FailedDocument`, and `IngestionResult` as stable concepts.
Week 3 gives names and shapes to the things Week 4 will manipulate.
That is why this chapter matters so much.
## 111. Final synthesis
The core lesson of Week 3 is simple.
Model the real concepts of the problem clearly.
In ResearchOps, that means papers, parsed documents, failures, ingestion results, queries, tags, and identifiers.
Once those concepts are explicit, the rest of the architecture gets easier.
## 112. Extra practice checklist
- define class and instance
- explain `@dataclass`
- explain `frozen=True`
- explain `__post_init__`
- explain `@property`
- explain `__str__`
- explain value object versus entity
- explain why `PaperId.from_path()` uses hashing
- explain why `ParsedDocument` is separate from `Paper`
- explain why `IngestionResult` uses composition
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 03 — OOP and Domain Modeling:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
