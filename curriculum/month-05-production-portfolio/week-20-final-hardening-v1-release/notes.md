<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 20 — Final Hardening and v1 Release:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 20 Notes: Final Hardening and v1.0 Release

## Chapter overview
Week 20 is the final hardening and v1.0 release chapter.
The goal is not to make ResearchOps bigger.
The goal is to make ResearchOps shippable.
Shippable means a careful reader can clone the repository, install the package, run the CLI, run the API or worker pieces that exist, execute the tests, read the documentation, and understand what is supported.
In earlier weeks you learned how to build pieces.
This week teaches the professional skill of proving that the pieces belong together.
You will use `RELEASE_CHECKLIST.md` as the source of truth for release readiness.
You will audit tests, errors, documentation, security assumptions, version numbers, changelog entries, and demo steps.
You will practice saying no to new features even when they sound exciting.
A v1.0 release is a promise about the current system, not a promise that the system is perfect forever.
ResearchOps v1.0 means the portfolio version is coherent, explainable, and safe to demonstrate.
The final artifact is a release candidate that could become `v1.0.0` after every checklist item is verified.

## What you already know from previous weeks
Week 1 gave you the project skeleton, `src/` layout, `pyproject.toml`, pytest, Ruff, and the first `researchops scan` command.
Week 2 taught that errors are information, so hardening starts by checking whether failures are clear instead of mysterious.
Week 3 gave ResearchOps domain models such as papers, parsed documents, ingestion results, and search results.
Week 4 turned the project into installable software with command entry points and CLI tests.
Week 5 added SQLite persistence, which means release validation must check schema behavior and real database integration.
Week 6 added PDF parsing, which means final tests must include bad files, missing files, and realistic paper text.
Week 7 added keyword search and data quality gates, so v1.0 must prove search is predictable and empty results are handled cleanly.
Week 8 added multiprocessing ingestion, so final hardening must watch for CPU-heavy work and worker failure paths.
Week 9 introduced protocols and clean architecture, so the release audit must check import direction and dependency inversion.
Week 10 made tests a quality gate, so v1.0 cannot rely on manual confidence alone.
Week 11 added classical ML topic classification, which needs documented limitations and reproducible behavior.
Week 12 added experiment tracking, so release notes must explain what is recorded and why it matters.
Week 13 added embeddings and semantic search, which means performance, deterministic tests, and dependency size all matter.
Week 14 added FastAPI, so release validation includes HTTP behavior, status codes, and service delegation.
Week 15 added async I/O and network fetching, so final review must separate I/O-bound work from CPU-bound work.
Week 16 added a local worker job system, so release readiness includes job state transitions and retry/error behavior.
Week 17 added a RAG assistant, so release notes must be honest about retrieval context, prompt construction, and hallucination limits.
Week 18 added Docker and environment configuration, so v1.0 must be runnable outside your personal shell.
Week 19 polished documentation and portfolio presentation, so Week 20 checks whether that story matches the actual code.

## What problem this week solves
The problem is release risk.
Release risk appears when a project works only on the author's machine.
Release risk appears when a command is documented but no longer exists.
Release risk appears when a test suite passes while an important manual workflow is broken.
Release risk appears when errors expose confusing tracebacks instead of actionable messages.
Release risk appears when a version number says one thing and the changelog says another.
Release risk appears when a demo depends on hidden local files.
This week converts scattered confidence into evidence.
The evidence comes from commands, tests, checklists, manual walkthroughs, architecture checks, and written release notes.
By the end of the week, you should be able to answer: what exactly is included in v1.0, what is excluded, how to run it, how to test it, and what you would improve next.

## Beginner mental model
Think of a release like packing a research instrument for another lab.
The instrument may work perfectly on your bench.
That is not enough.
Another person needs instructions, labels, calibration steps, safety notes, and a way to tell whether the instrument is functioning.
ResearchOps v1.0 is the packed instrument.
The code is the instrument.
The tests are calibration checks.
The CLI help text is the label on the buttons.
The README is the quick-start card.
The changelog is the history of modifications.
The release checklist is the packing list.
The git tag is the sealed box label that says exactly which version was shipped.
If one of those pieces is missing, the project may still be interesting, but it is not release-ready.

## Core vocabulary
**Release candidate:** a version you believe could ship if final checks pass.
**v1.0.0:** the first stable public version of the project.
**Semantic versioning:** a version format written as MAJOR.MINOR.PATCH.
**MAJOR:** the number that changes when users must change how they use the software.
**MINOR:** the number that changes when new backward-compatible capability is added.
**PATCH:** the number that changes when a backward-compatible bug fix is made.
**Changelog:** a human-readable history of important changes.
**Release notes:** the short explanation attached to a specific release.
**Regression:** something that used to work but now fails.
**Smoke test:** a quick command that proves the most basic path still works.
**End-to-end test:** a test that exercises a complete user workflow across multiple layers.
**Hardening:** improving reliability, clarity, safety, and edge-case behavior without expanding scope.
**Scope freeze:** the rule that no new features enter the release candidate.
**Known limitation:** an honest statement about behavior the project does not support yet.
**Distribution:** the way a user installs or runs the project, such as editable install, wheel, Docker image, or source clone.
**Artifact:** a produced thing from a release process, such as a tag, wheel, container image, changelog, or demo script.
**Security review:** a deliberate check for secrets, unsafe defaults, over-broad file access, and risky dependency behavior.
**Performance review:** a deliberate check that common workflows are fast enough and heavy work is in the correct layer.
**Definition of done:** the exact conditions that must be true before work is considered complete.

## Concept explanations from first principles
### 1. A release is a communication event, not only a technical event.
When you tag `v1.0.0`, you are communicating to future users and future you.
You are saying: this exact commit is meaningful.
You are saying: the documented commands were checked.
You are saying: known limitations are written down instead of hidden.
You are saying: if a future change breaks behavior, we can compare it against this stable point.
Beginners often think a release is something that happens after the real work.
In production work, release preparation is part of the real work.
Poor release preparation creates support cost later.
Good release preparation reduces confusion for users, reviewers, collaborators, and interviewers.
### 2. Semantic versioning is a contract about change.
`1.0.0` has three numbers.
The first number is MAJOR.
The second number is MINOR.
The third number is PATCH.
If ResearchOps changes `researchops search` so existing scripts must be rewritten, that is a MAJOR change.
If ResearchOps adds `researchops export` while existing commands keep working, that is a MINOR change.
If ResearchOps fixes a crash when a PDF has no text, that is a PATCH change.
The exact version number is less important than the honesty behind it.
For this curriculum, v1.0.0 means the capstone portfolio version is stable enough to present.
### 3. A changelog is not a git log.
A git log records commits.
A changelog explains user-visible changes.
`fix stuff` is not a useful changelog entry.
`Fixed ingestion error reporting for unreadable PDFs so failed files appear in the ingestion result instead of crashing the run` is useful.
A good changelog groups changes by release.
A good changelog uses categories such as Added, Changed, Fixed, Documentation, and Known limitations.
A good changelog helps a reader understand the story without reading every commit.
### 4. A release checklist prevents emotional decision-making.
Near the end of a project, you may feel tired.
You may also feel tempted to polish forever.
A checklist protects you from both problems.
If a checklist item fails, you fix or document it.
If a new idea is not on the checklist, it waits for v1.1.
`RELEASE_CHECKLIST.md` is therefore a discipline tool.
It turns vague confidence into observable facts.
### 5. Hardening is different from feature development.
Feature development asks: what new capability can the system perform?
Hardening asks: can the existing capability survive realistic use?
Feature development adds surface area.
Hardening reduces surprise.
Feature development often creates new tests.
Hardening often strengthens existing tests, error messages, docs, and boundaries.
In Week 20, adding a new ML model is not hardening.
Checking that the current model has clear limitations is hardening.
Adding a new API endpoint is not hardening.
Checking that current endpoints return useful errors is hardening.
### 6. End-to-end testing follows the user story.
A unit test checks one small unit in isolation.
An integration test checks two or more real pieces together.
An end-to-end test checks a complete user path.
For ResearchOps, an end-to-end path might be: install package, scan sample papers, ingest documents, search, ask a question, and review output.
End-to-end tests are valuable because they catch wiring mistakes.
End-to-end tests are expensive because failures can come from many layers.
The v1.0 mindset uses both: unit tests for precise confidence and end-to-end tests for workflow confidence.
### 7. Security review starts with boring questions.
Does the repository contain secrets?
Does configuration encourage hard-coded credentials?
Do examples accidentally include private paths?
Do commands write outside intended project or data directories?
Does the API expose debug tracebacks in normal user-facing responses?
Do dependencies match what the curriculum intentionally introduced?
Boring security questions matter because most release mistakes are ordinary oversights.
### 8. Performance review starts with the common path.
Do not optimize imaginary workloads first.
Check the workflows the learner and demo will actually run.
For ResearchOps, those workflows include scanning paper directories, parsing sample PDFs, storing records, keyword search, semantic search, API calls, worker jobs, and RAG answer construction.
If common paths are slow, ask whether the algorithm is wasteful, whether CPU work is in a process pool, whether I/O is blocking an async path, or whether a test fixture is too large.
Performance hardening does not require perfect speed.
It requires that performance is acceptable and limitations are honest.
### Release checklist walkthrough
- Check 1: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 2: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 3: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 4: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 5: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 6: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 7: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 8: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 9: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 10: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 11: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 12: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 13: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 14: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 15: verify the release checklist walkthrough item with an actual command, file inspection, or documented manual observation before marking it complete.
### Error-handling audit checklist
- Check 1: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 2: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 3: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 4: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 5: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 6: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 7: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 8: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 9: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 10: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 11: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 12: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 13: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 14: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 15: verify the error-handling audit checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
### Performance and edge-case audit
- Check 1: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 2: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 3: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 4: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 5: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 6: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 7: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 8: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 9: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 10: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 11: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 12: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 13: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 14: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 15: verify the performance and edge-case audit item with an actual command, file inspection, or documented manual observation before marking it complete.
### Security review checklist
- Check 1: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 2: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 3: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 4: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 5: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 6: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 7: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 8: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 9: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 10: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 11: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 12: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 13: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 14: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 15: verify the security review checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
### Packaging and distribution checklist
- Check 1: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 2: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 3: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 4: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 5: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 6: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 7: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 8: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 9: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 10: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 11: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 12: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 13: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 14: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 15: verify the packaging and distribution checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
### CHANGELOG finalization checklist
- Check 1: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 2: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 3: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 4: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 5: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 6: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 7: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 8: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 9: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 10: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 11: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 12: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 13: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 14: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 15: verify the changelog finalization checklist item with an actual command, file inspection, or documented manual observation before marking it complete.
### Definition of shippable for ResearchOps
- Check 1: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 2: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 3: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 4: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 5: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 6: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 7: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 8: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 9: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 10: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 11: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 12: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 13: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 14: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.
- Check 15: verify the definition of shippable for researchops item with an actual command, file inspection, or documented manual observation before marking it complete.

## ResearchOps-specific application
ResearchOps processes research papers through a modular monolith.
The final release must respect that architecture.
The CLI and API are delivery layers.
They should wire services, not contain business rules.
Services coordinate use cases.
Services should depend on protocols from `core/interfaces.py`.
Infrastructure modules such as storage, parsing, search, ML, and workers implement those protocols.
The final audit should follow real ResearchOps workflows:
- Can a learner discover PDFs with the CLI?
- Can a parsed paper be saved and retrieved?
- Can keyword search return understandable results?
- Can semantic search use embeddings without hiding dependency assumptions?
- Can classifier and experiment features explain what they did?
- Can the API expose service behavior without duplicating business logic?
- Can worker jobs transition through states predictably?
- Can RAG assemble retrieved context and prompt text in a way that can be tested?
- Can Docker and environment files run without relying on private machine state?
- Can the portfolio documentation explain the project in five minutes?
The release is not only about whether each feature exists.
It is about whether the features form one coherent system.
- Workflow audit: `scan sample papers` must have a clear command, expected result, failure behavior, and documentation pointer.
- Workflow audit: `ingest parsed documents` must have a clear command, expected result, failure behavior, and documentation pointer.
- Workflow audit: `run keyword search` must have a clear command, expected result, failure behavior, and documentation pointer.
- Workflow audit: `run semantic search` must have a clear command, expected result, failure behavior, and documentation pointer.
- Workflow audit: `classify a topic` must have a clear command, expected result, failure behavior, and documentation pointer.
- Workflow audit: `record an experiment` must have a clear command, expected result, failure behavior, and documentation pointer.
- Workflow audit: `serve API request` must have a clear command, expected result, failure behavior, and documentation pointer.
- Workflow audit: `process worker job` must have a clear command, expected result, failure behavior, and documentation pointer.
- Workflow audit: `draft RAG answer` must have a clear command, expected result, failure behavior, and documentation pointer.
- Workflow audit: `run Docker demo` must have a clear command, expected result, failure behavior, and documentation pointer.

## Code examples with line-by-line explanation
### Example 1: version consistency check
```python
from pathlib import Path

package_init = Path("src/researchops/__init__.py")
pyproject = Path("pyproject.toml")

init_text = package_init.read_text()
project_text = pyproject.read_text()

expected = "1.0.0"

assert f'__version__ = "{expected}"' in init_text
assert f'version = "{expected}"' in project_text
```
Line 1 imports `Path`, the beginner-friendly object for filesystem paths.
Line 3 points to the package initialization file where Python code usually exposes `__version__`.
Line 4 points to `pyproject.toml`, the packaging metadata file.
Line 6 reads the package file into a string.
Line 7 reads the project metadata into a string.
Line 9 stores the release version once so the check does not repeat a magic value.
Line 11 asserts that `src/researchops/__init__.py` advertises the same version.
Line 12 asserts that `pyproject.toml` advertises the same version.
This is a release-hardening example because mismatched versions confuse users and release tools.
### Example 2: release checklist command runner
```python
import subprocess

commands = [
    ["researchops", "--help"],
    ["pytest", "-q"],
    ["ruff", "check", "src", "tests"],
]

for command in commands:
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"Release check failed: {command}")
```
Line 1 imports Python's standard subprocess module for running external commands.
Line 3 creates a list of commands.
Line 4 checks that the installed CLI exposes help text.
Line 5 runs the test suite quietly.
Line 6 runs Ruff against source and test code.
Line 9 loops over each command.
Line 10 runs the command and records its exit status.
Line 11 checks whether the command failed.
Line 12 exits with a message that names the failed command.
This example teaches automation, but the curriculum validation file should remain the main source of exact commands.
### Example 3: honest changelog entry
```markdown
## [1.0.0] - 2026-06-09

### Added
- Portfolio-ready ResearchOps workflow from paper discovery through RAG answer drafting.
- Release checklist covering tests, lint, documentation, versioning, and demo readiness.

### Fixed
- Clarified final validation steps so release commands match the documented CLI.

### Known limitations
- Local-first demo data is intentionally small and does not prove large-scale production throughput.
```
Line 1 names the release and date.
Line 3 starts the Added category.
Line 4 describes a user-visible capability, not an internal commit.
Line 5 describes the release process artifact.
Line 7 starts the Fixed category.
Line 8 explains the user benefit of the fix.
Line 10 starts Known limitations.
Line 11 is honest about scale without apologizing for the project.
### Example 4: annotated tag command
```bash
git tag -a v1.0.0 -m "ResearchOps v1.0.0"
git show v1.0.0 --no-patch
```
Line 1 creates an annotated tag named `v1.0.0`.
`-a` means annotated, so the tag stores its own metadata and message.
`-m` supplies the message without opening an editor.
Line 2 shows the tag without printing the full patch.
This confirms the tag points to the intended commit.
In this assignment you are learning the command; do not create the tag until the release checklist is actually complete.

## Common beginner mistakes
1. Adding a feature during release week because it feels small.
2. Marking a checklist item complete without running the command.
3. Updating `pyproject.toml` but forgetting `src/researchops/__init__.py`.
4. Writing a changelog that lists commits instead of user-facing changes.
5. Creating a lightweight tag when the project standard asks for an annotated tag.
6. Assuming Docker works because local Python works.
7. Assuming the API works because service unit tests pass.
8. Assuming services are clean without checking imports.
9. Leaving private absolute paths in documentation or demo scripts.
10. Ignoring a flaky test instead of investigating whether it reveals nondeterminism.
11. Confusing known limitations with excuses.
12. Writing release notes that overclaim production readiness.
13. Optimizing rare workloads while common demo commands are slow.
14. Changing validation commands without updating docs.
15. Running commands from the wrong directory and trusting the result.

## Debugging guidance
Start every release bug by naming the failing layer: documentation, packaging, CLI, service, infrastructure, API, worker, search, ML, or environment.
If a command is missing, inspect `pyproject.toml` entry points and CLI registration before editing service code.
If imports fail, check editable install status and source layout before changing module names.
If tests fail only together, look for shared state, database files, global configuration, random seeds, or environment variables.
If an API endpoint returns the wrong status code, trace from route handler to service method to protocol implementation.
If worker behavior is confusing, draw the job state transition before changing code.
If RAG output is weak, separate retrieval failure from prompt construction failure.
If semantic search behaves strangely, inspect chunking, embedding dimensions, and similarity ranking separately.
If Docker fails, compare environment variables, installed extras, paths, and exposed commands with local execution.
If performance is poor, measure the slow step before rewriting architecture.
If documentation and behavior disagree, decide which is correct, then update the other immediately.
If a release checklist item is ambiguous, rewrite the checklist item so the next learner can verify it concretely.
Release debugging habit 1: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 2: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 3: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 4: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 5: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 6: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 7: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 8: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 9: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 10: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 11: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 12: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 13: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 14: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 15: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 16: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 17: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 18: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 19: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 20: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 21: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 22: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 23: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 24: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 25: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 26: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 27: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 28: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 29: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 30: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 31: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 32: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 33: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 34: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 35: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 36: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 37: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 38: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 39: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.
Release debugging habit 40: change one variable at a time, rerun the smallest relevant check, and write down whether the evidence moved closer to the expected behavior.

## Design tradeoffs
### Scope freeze versus last-minute improvement
Scope freeze protects reliability.
A last-minute improvement may be valuable, but it can invalidate tests and documentation.
For v1.0, prefer deferring new ideas to the roadmap unless they fix a release-blocking defect.
### Manual checklist versus automated checks
Automated checks are repeatable and fast.
Manual checks catch documentation, demo flow, and human comprehension issues.
Use both.
### Detailed release notes versus short release notes
Detailed notes help future maintainers.
Short notes help busy reviewers.
A good release uses a concise summary plus links or sections for detail.
### Honest limitations versus marketing polish
Overclaiming makes a portfolio weaker because experienced reviewers notice.
Honest limitations show judgment.
### Local-first distribution versus cloud deployment
ResearchOps v1.0 is allowed to be local-first if that is what the project supports.
A broken cloud story is worse than a clear local story.

## Testing implications
Final testing should not be random.
It should map to the release checklist.
Unit tests prove small decisions.
Integration tests prove real infrastructure boundaries.
End-to-end tests prove user workflows.
CLI tests prove command registration and output behavior.
API tests prove HTTP contracts.
Worker tests prove state transitions.
Search tests prove ranking behavior on known inputs.
ML tests prove training, prediction, and evaluation paths without requiring huge datasets.
RAG tests prove retrieval and prompt assembly, not magical answer truth.
Documentation checks prove commands in the docs still match the code.
For v1.0, a failing test is either a bug, an outdated test, or an unclear requirement.
Do not ignore it.

## Architecture implications
Week 20 is the architecture honesty check.
`core/` must remain independent of CLI, API, storage, parsing, ML, workers, and search.
`services/` must use protocols, not concrete infrastructure implementations.
`cli/` and `api/` should wire dependencies and delegate business behavior.
Infrastructure modules should implement protocols and keep external details contained.
CPU-heavy work should not run inside asyncio event loops.
Docker and packaging should not become excuses to bypass clean architecture.
If a release fix requires violating dependency direction, pause and find the correct layer.
Architecture is not decoration in this project.
It is what makes the 20-week system understandable and testable.

## How this connects to AI engineering / ML research
AI engineering projects often fail at the handoff point.
A notebook result may be impressive but not reproducible.
A demo may work only with one private environment.
A model may produce outputs without a clear test strategy.
ResearchOps teaches that AI features need normal software discipline.
Embeddings need storage and ranking tests.
RAG needs retrieval checks and prompt transparency.
Classifiers need experiment tracking and honest metrics.
Workers need observable job states.
APIs need stable contracts.
Releases need versioning and changelogs.
Final hardening turns an AI-flavored prototype into an engineering artifact.

## Mini quizzes
1. What does the MAJOR number mean in semantic versioning?
2. When should ResearchOps use a PATCH release?
3. Why is a changelog different from a git log?
4. What is one example of a release-blocking bug?
5. What is one example of a v1.1 idea that should not enter v1.0?
6. Why do end-to-end tests not replace unit tests?
7. Why should known limitations appear in release notes?
8. What file is the source of release checklist truth?
9. Why should services depend on protocols?
10. What does an annotated git tag add compared with an unannotated label?

## Explain-it-aloud prompts
- Explain what ResearchOps v1.0 includes in two minutes.
- Explain why Week 20 forbids new features.
- Explain the difference between hardening and polishing.
- Explain how you would verify the CLI from a fresh clone.
- Explain how an API route should delegate to a service.
- Explain how the release checklist protects future maintainers.
- Explain one known limitation without sounding defensive.
- Explain why a portfolio project needs a changelog.
- Explain what you would do if a final validation command fails.
- Explain what life after v1.0 should look like.

## What to memorize
`MAJOR.MINOR.PATCH` is the shape of semantic versioning.
Breaking change means MAJOR.
Backward-compatible feature means MINOR.
Backward-compatible bug fix means PATCH.
`CHANGELOG.md` explains user-visible changes.
`RELEASE_CHECKLIST.md` is the release readiness source of truth.
`git tag -a v1.0.0 -m "ResearchOps v1.0.0"` creates an annotated release tag.
Never call a release done just because the code looks finished.

## What to understand deeply
Done is a relationship between code, tests, documentation, packaging, and user expectations.
A release is a promise about a specific commit.
Good error handling is part of user experience.
Good tests are part of design, not paperwork.
Architecture boundaries make final hardening possible because each layer has a job.
Honest limitations increase trust.
Saying no is an engineering skill.

## What not to worry about yet
Do not worry about building a SaaS platform.
Do not worry about Kubernetes.
Do not worry about distributed tracing.
Do not worry about million-document scale unless the project claims to support it.
Do not worry about replacing every local component with managed cloud services.
Do not worry about inventing a perfect release process.
Do not worry about adding advanced model providers after the scope freeze.
Your job is to make v1.0 honest, coherent, and demonstrable.

## Where to go from here / continuing the journey
After v1.0, the next journey is maintenance.
Maintenance means triaging issues, planning v1.1, protecting tests, and improving documentation when users get confused.
A strong v1.1 might add one focused capability, not ten random features.
A strong v1.1 might improve evaluation datasets, export workflows, authentication, deployment documentation, or observability.
Choose the next step based on evidence from v1.0 users and demos.
Keep the architecture boundaries that made the capstone understandable.
Keep writing changelog entries as you work, not only at release time.
Keep tests close to every behavior change.
Keep known limitations honest.
The point of this 20-week curriculum was never only to finish ResearchOps.
The point was to learn how to build, explain, test, harden, and ship a real Python system.
Carry that rhythm into every future project.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 20 — Final Hardening and v1 Release:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
