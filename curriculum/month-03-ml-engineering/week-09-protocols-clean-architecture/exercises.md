<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises — Week 09: Protocols, Interfaces, and Clean Architecture

> This is the hardest *conceptual* week of the entire program. Protocols,
> dependency inversion, and architecture boundaries are abstract — so this
> workbook is deliberately long and hands-on. You do not "read" this week; you
> *do* it. Type the code, run it, break it, and explain it aloud.

All file paths are relative to the repository root. Real project names used here
match the actual code: protocols live in `src/researchops/core/interfaces.py`,
fakes live in `tests/fakes/fake_repository.py`, and services live in
`src/researchops/services/`.

---

## How to use this workbook

1. **Work top to bottom.** The sections build on each other. The warm-ups create
   the vocabulary the project exercises assume.
2. **Type everything by hand.** Do not copy-paste. Muscle memory is the point.
3. **Run after every exercise.** Use a scratch file in `/tmp/` (so it is never
   committed) or a REPL. Verify, do not assume.
4. **Keep the rule visible.** Pin this sentence where you can see it:
   *core depends on nothing; services depend only on core protocols; only the CLI
   wires concrete adapters.*
5. **Answer the written prompts in full sentences.** If you cannot write it, you
   do not understand it.
6. **Use the completion checklist (Section 20) as your gate.** Do not start
   Week 10 until every box is honestly ticked.

A scratch workflow you will reuse all week:

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,parsing,storage]"
# put throwaway experiments here so they are never committed:
mkdir -p /tmp/w9
$EDITOR /tmp/w9/scratch.py
python /tmp/w9/scratch.py
```

---

## Warm-up exercises

A **concrete dependency** is a place where code reaches directly for a specific
implementation (a class, a library, a file, a connection) instead of asking for a
*capability*. Concrete dependencies are what make code hard to test and hard to
change.

**Exercise W9-1.** For each line below, write "concrete" or "abstract", and if
concrete, name what it is glued to:

```python
self.repo = SQLiteRepository(sqlite3.connect("researchops.db"))   # (a)
def __init__(self, repo: PaperRepository) -> None: ...            # (b)
parser = PyMuPDFParser()                                          # (c)
def save_all(self, repo: PaperRepository) -> None: ...            # (d)
results = sklearn.linear_model.LogisticRegression().fit(X, y)     # (e)
```

**Exercise W9-2.** In one sentence each, explain *why* every concrete dependency
above makes a unit test slower or harder.

**Exercise W9-3.** Write down three questions you can ask about any line of code
to decide if it is a concrete dependency. (Hint: "Could I swap this for a fake in
a test without changing the caller?")

---

## Code-reading exercises

Open `src/researchops/core/interfaces.py`. It defines these protocols:
`DocumentParser`, `PaperRepository`, `FailureRepository`, `SearchEngine`,
`EmbeddingModel`, `ExperimentRepository`.

**Exercise W9-4.** Build a table with one row per protocol and these columns:

| Protocol | What capability it represents | Methods | Concrete adapter (in `storage/` or `parsing/`) | Fake (in `tests/fakes/`) |
|---|---|---|---|---|

Fill in every cell. For the adapter and fake columns, actually open the files and
confirm — do not guess.

**Exercise W9-5.** `PaperRepository.get` is documented as raising
`PaperNotFoundError` when missing (it does **not** return `None`). Find where
`PaperNotFoundError` and `DuplicatePaperError` are defined
(`src/researchops/core/exceptions.py`). Write one sentence on why returning an
error object beats returning `None` here.

**Exercise W9-6.** Note that `interfaces.py` imports only from
`researchops.core.models`. Write one sentence explaining why it is *critical* that
this file imports no `sqlite3`, no `pymupdf`, and nothing from `storage/`.

---

## Implementation exercises

### Before/after constructor refactor exercise

Here is a service written the **wrong** way — it builds its own dependencies:

```python
# BEFORE — concrete, untestable
import sqlite3
from researchops.storage.sqlite_repository import SQLiteRepository
from researchops.parsing.pdf_parser import PyMuPDFParser

class IngestionService:
    def __init__(self) -> None:
        conn = sqlite3.connect("researchops.db")
        self._paper_repo = SQLiteRepository(conn)
        self._parser = PyMuPDFParser()
```

**Exercise W9-7.** Rewrite it the **right** way: accept dependencies through the
constructor, typed as protocols. Compare your answer with the real
`IngestionService.__init__` in `src/researchops/services/ingestion_service.py`,
which takes `parser: DocumentParser`, `paper_repo: PaperRepository`, and
`failure_repo: FailureRepository`.

**Exercise W9-8.** In writing, answer: after the refactor, *who* now creates the
SQLite connection and the parser? (Name the layer and the file.)

---

### Protocol design exercise

The spec for a repository protocol often looks like this minimal shape:

```python
from typing import Protocol
from researchops.core.models import Paper

class PaperRepository(Protocol):
    def save(self, paper: Paper) -> None: ...
    def get_by_id(self, paper_id: str) -> Paper | None: ...
```

**Exercise W9-9.** Compare this teaching sketch with the **real**
`PaperRepository` in `interfaces.py`. List every difference (method names, return
types, error behavior, extra methods like `exists`, `list_all`, `delete`). Which
design — `get_by_id -> Paper | None` or `get -> Paper` (raises) — does this project
use, and why might a project prefer raising over returning `None`?

**Exercise W9-10.** Design a brand-new protocol of your own called
`TextSummarizer` with a single method `summarize(text: str) -> str`. Put it in a
scratch file. Then write **two** classes that satisfy it *without inheritance*:
`TruncatingSummarizer` (first 100 chars) and `FirstSentenceSummarizer`. Verify
structural typing works at runtime:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class TextSummarizer(Protocol):
    def summarize(self, text: str) -> str: ...

assert isinstance(TruncatingSummarizer(), TextSummarizer)
```

**Exercise W9-11.** Explain in writing why you did **not** write
`class TruncatingSummarizer(TextSummarizer)`. What does structural subtyping give
you that nominal inheritance does not?

---

### Fake repository exercise

**Exercise W9-12.** Without looking at `tests/fakes/fake_repository.py`, write
your own `MyFakePaperRepository` from scratch that satisfies the real
`PaperRepository` protocol (`save`, `get`, `list_all`, `exists`, `delete`). Use an
in-memory `dict[str, Paper]`. Make `save` raise `DuplicatePaperError` on a
duplicate id and `get` raise `PaperNotFoundError` when missing — matching the
protocol's documented behavior.

**Exercise W9-13.** Now open the real `FakePaperRepository` and diff it against
yours. Did you miss the duplicate check? The not-found error? Write down each
difference. Then verify your fake satisfies the protocol:

```python
from researchops.core.interfaces import PaperRepository
assert isinstance(MyFakePaperRepository(), PaperRepository)
```

**What to avoid:** a fake that silently overwrites on duplicate `save`, or returns
`None` from `get`. A fake must honor the *contract*, not just the method names —
otherwise tests pass against the fake but the real adapter behaves differently.

---

### Fake parser exercise

**Exercise W9-14.** Study `FakeDocumentParser` in `tests/fakes/`. It is
*configurable*: you can `set_result(path, doc)` or `set_error(path, exc)`. Write a
scratch test that:

1. Creates a `FakeDocumentParser`.
2. Configures one path to return a `ParsedDocument` and another path to raise a
   `ParsingError`.
3. Calls `.parse(path)` for both and asserts the success path returns the doc and
   the failure path raises.

**Exercise W9-15.** In writing: why is a *configurable* fake parser more useful in
tests than a fake that always returns the same document? Name one ingestion
behavior you can only test if the parser can be made to fail on demand.

---

## Testing exercises

### Test double exercise

The words *stub*, *fake*, and *mock* are not interchangeable.

- **Stub:** returns canned answers; no logic.
- **Fake:** a real working implementation, simplified (e.g. in-memory dict).
- **Mock:** records calls so the test can assert *how* it was called.

**Exercise W9-16.** Classify each of the project's test doubles
(`FakePaperRepository`, `FakeFailureRepository`, `FakeDocumentParser`) as stub,
fake, or mock, and justify each in one sentence.

**Exercise W9-17.** Describe one test where a **mock** (asserting a method was
called exactly once) would be more appropriate than a fake. Then describe why
fakes should still be your default choice most of the time.

---

### Import-boundary exercise

The architecture rule, as code:

- `core/` imports **nothing** from `services/`, `storage/`, `parsing/`, `ml/`,
  `ai/`, `api/`, `cli/`.
- `services/` imports **only** from `core/` (protocols + models + exceptions).
- `cli/` (the composition root) may import everything to wire it together.

**Exercise W9-18.** Run these audits and record the output (expected: no output =
zero violations):

```bash
# services must not import infrastructure
grep -rn "import sqlite3\|from researchops.storage\|from researchops.parsing\|import sklearn\|import pymupdf" \
  src/researchops/services/ --include="*.py"

# core must not import infrastructure or services
grep -rn "from researchops.storage\|from researchops.parsing\|from researchops.services\|import sqlite3" \
  src/researchops/core/ --include="*.py"
```

**Exercise W9-19.** Open `src/researchops/cli/commands/ingest.py`. Confirm it is
allowed to import concrete adapters. Write one sentence explaining why the *same*
import that is forbidden in `services/` is *correct* here.

---

### Circular import investigation

Circular imports usually mean a boundary has been crossed.

**Exercise W9-20.** In a scratch package under `/tmp/w9/`, deliberately create a
cycle: `module_a.py` imports `module_b`, and `module_b` imports `module_a` at the
top level. Run it and capture the exact `ImportError`/`partially initialized
module` traceback.

**Exercise W9-21.** Now explain: if `core/models.py` ever imported
`services/ingestion_service.py`, why would that risk a cycle? Which direction is
the import *supposed* to flow, and how does respecting that direction make cycles
structurally impossible?

**Exercise W9-22.** List two legitimate fixes for a real circular import (e.g.
move the shared type into `core/`, or use a local/deferred import) and say which
one is preferred in this codebase and why.

---

### Architecture diagram exercise

**Exercise W9-23.** Draw (on paper or in `docs/diagrams/`) the dependency graph
for the ingestion feature. Use boxes for modules and arrows for "depends on."
Include: `cli/commands/ingest.py`, `services/ingestion_service.py`,
`core/interfaces.py`, `core/models.py`, `storage/sqlite_repository.py`,
`parsing/pdf_parser.py`.

**Exercise W9-24.** On your diagram, verify two invariants and mark any violation
in red:

1. No arrow points *out* of `core/`.
2. No arrow points from `services/` to `storage/` or `parsing/` (services point
   only to `core/` protocols; the concrete adapters point *up* to those
   protocols).

Write one sentence describing where the "ports and adapters" boundary sits in your
drawing.

---

### Service-layer refactor exercise

**Exercise W9-25.** Imagine a new `TopicService` that needs to read papers and
classify them. Sketch its constructor so it depends only on protocols (e.g.
`PaperRepository` and a new `Classifier` protocol you define) — never on
`SQLiteRepository` or `sklearn` directly. Show the constructor signature only.

**Exercise W9-26.** Explain where the real `LogisticRegression`-based classifier
and the real `SQLiteRepository` get constructed and injected. (Name the layer.)
Why does keeping `sklearn` out of `TopicService` make the service unit-testable
without training a model?

---

### Testing exercise using a fake repository

**Exercise W9-27.** Create a scratch test file (you may later promote it to
`tests/unit/`) named `test_search_service_with_fake.py`. The real
`KeywordSearchService.__init__` takes `paper_repo: PaperRepository`. Using
`FakePaperRepository` (no SQLite, no files), write at least three tests:

1. `test_search_empty_repository_returns_no_results`
2. `test_search_finds_paper_by_keyword`
3. `test_search_is_case_insensitive` (or another real behavior you verify)

Each test must construct the service with a fake repository and assert on the
returned `SearchResult` list. No database file may be created.

**Exercise W9-28.** Run `pytest` for your file and confirm that no `*.db` file
appears in the project directory afterwards. Why is "no database file created" the
single clearest signal that this is a true unit test?

---

## Debugging exercises

### Protocol mismatch

**Exercise W9-29.** Create a class that *looks* like it satisfies
`PaperRepository` but has a subtly wrong method — e.g. spell `save` as `store`, or
give `get` the wrong arity:

```python
class BrokenRepo:
    def store(self, paper) -> None: ...   # wrong name
    def get(self, paper_id): ...
    def list_all(self): ...
    def exists(self, paper_id): ...
    def delete(self, paper_id): ...
```

Run `isinstance(BrokenRepo(), PaperRepository)` (the protocol is
`@runtime_checkable`). Record the result. Then try to use it where the service
expects a real repo and capture the failure.

**Exercise W9-30.** Explain what `@runtime_checkable` *does* and does **not**
check. (It checks method *names* exist, not their signatures or types.) Why does
this mean a passing `isinstance` check is necessary but **not** sufficient — and
why does a static type checker like `mypy` catch what `isinstance` misses?

---

## Refactoring exercises

### Remove a direct SQLite dependency

**Exercise W9-31.** Here is an offending snippet. Refactor it so the service no
longer imports or constructs SQLite:

```python
# BEFORE
import sqlite3
class StatsService:
    def __init__(self) -> None:
        self._conn = sqlite3.connect("researchops.db")
    def paper_count(self) -> int:
        cur = self._conn.execute("SELECT COUNT(*) FROM papers")
        return cur.fetchone()[0]
```

Your refactor must: (a) define what capability the service truly needs, (b) depend
on a protocol that provides it (hint: `PaperRepository.list_all`), and (c) move
the SQLite construction to the composition root.

**Exercise W9-32.** After your refactor, write the unit test that proves
`paper_count()` works using `FakePaperRepository` — with no SQLite at all.

---

## Written explanation exercises

Answer each in 3–5 sentences, in your own words.

1. A colleague says: "Just import `SQLiteRepository` directly in the service —
   it's faster to write." How do you respond, and what would you *show* them?
2. What is the difference between a fake and a mock, and when do you prefer each?
3. You add a sixth method `search_by_title` to `PaperRepository`. What else must
   you update, and what could break?
4. A junior dev says "protocols are just documentation — the program runs without
   them." Correct this, specifically mentioning `mypy` and `@runtime_checkable`.
5. Where is the *composition root* in ResearchOps, and why does it matter that
   wiring happens there and not inside a service?
6. Explain the Dependency Inversion Principle using `IngestionService` and
   `PaperRepository` as your only example.

---

## Stretch exercises

**Exercise W9-S1 — Clock protocol.** Time-dependent code is hard to test. Define a
`Clock` protocol with `now() -> datetime`. Write `RealClock` (calls the system
clock) and `FixedClock` (always returns a set time). Show how you would inject a
`Clock` into a service that timestamps records, and write a test using
`FixedClock`.

**Exercise W9-S2 — Full architecture map.** Draw the dependency graph for the
*entire* `researchops` package, not just ingestion. Verify the two invariants from
Section 11 hold everywhere. Note any module you are unsure about and resolve it by
reading imports.

**Exercise W9-S3 — Fake for `ExperimentRepository`.** Read the
`ExperimentRepository` protocol (`create_run`, `log_metric`, `get_run`,
`list_runs`). Write a `FakeExperimentRepository` that stores runs in memory. Then
write a test that creates a run, logs two metrics, and reads them back.

---

## Brutal exercises

These are meant to be uncomfortable. Do them without notes.

**Exercise W9-B1.** Close every project file. From a blank scratch file, write the
`PaperRepository` protocol, a conforming fake, and a passing unit test for a
service that uses it — entirely from memory. Only then reopen the real files and
score yourself.

**Exercise W9-B2.** Take the existing `IngestionService` and, on paper, list every
line that would have to change if you swapped SQLite for Postgres. The honest
answer should be **zero lines in the service**. If you think otherwise, find your
misunderstanding.

**Exercise W9-B3.** Justify *deleting* an abstraction. Find (or invent) a protocol
with exactly one implementation that will never have a second. Argue whether it
earns its keep or is overengineering. Defend your verdict in writing — there is a
real cost to needless indirection.

---

## Mini project task

Deliver a complete, self-contained vertical slice that proves you own this week:

1. **Define** a new protocol of genuine value to ResearchOps (e.g. `Clock`, or a
   `Classifier` capability) in the appropriate `core/` location.
2. **Implement** one real adapter for it (may be trivial) in an infrastructure
   module, and one **fake** in `tests/fakes/`.
3. **Consume** it from a service via constructor injection — the service must not
   import the concrete adapter.
4. **Wire** the real adapter in the CLI composition root.
5. **Test** the service using only the fake — no DB, no files, no network.
6. **Document** the decision: add a short note (or ADR entry) explaining why the
   abstraction exists and when you would remove it.

Definition of success: `pytest tests/unit/ -q` passes, no database file is
created during unit tests, `ruff check src tests` is clean, and your service file
contains zero infrastructure imports.

---

## Completion checklist

Do not advance to Week 10 until every box is honestly true.

- [ ] I can state the Dependency Inversion Principle from memory.
- [ ] I can explain, with the real code, why `IngestionService.__init__` takes
      `PaperRepository` rather than `SQLiteRepository`.
- [ ] I built a table covering all six protocols in `interfaces.py` (capability,
      methods, real adapter, fake).
- [ ] I wrote `PaperRepository`, a conforming fake, and a passing unit test
      entirely from memory (Exercise W9-B1).
- [ ] I can explain the difference between `get -> Paper` (raises) and
      `get_by_id -> Paper | None`, and why this project chose the former.
- [ ] I ran the import-boundary audits and got zero violations.
- [ ] I reproduced a circular import and can explain how import direction
      prevents one.
- [ ] I can explain what `@runtime_checkable` checks and what only `mypy` catches.
- [ ] I refactored a direct-SQLite service to depend on a protocol and tested it
      with a fake.
- [ ] I drew the ingestion dependency graph and verified both architecture
      invariants.
- [ ] I completed the mini project: new protocol + adapter + fake + injected
      service + unit test.
- [ ] `pytest tests/unit/ -q` passes with **no** database file created.
- [ ] `ruff check src tests` exits clean.
- [ ] I can explain one scenario in Month 4 or 5 where these abstractions save me
      real work.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
