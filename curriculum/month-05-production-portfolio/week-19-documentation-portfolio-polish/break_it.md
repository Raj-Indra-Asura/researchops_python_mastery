<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 19 — Documentation and Portfolio Polish:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It - Week 19 Documentation and Portfolio Polish

## Purpose of failure practice

Documentation failures are not compiler errors. They are silent. A reader follows your README, hits an error, and gives up — and you never find out. Worse, some documentation failures (a wrong expected output, a misleading diagram) actively teach the reader something false. This lab makes you cause those failures deliberately so that you can recognize their symptoms before a stranger does.

Unlike previous weeks, several "expected errors" here are human reactions, not stack traces. Treat "the reader is confused" as seriously as `ValueError`.

## Failure lab rules

- Break one thing at a time.
- Write down the exact symptom before fixing it.
- Use a scratch branch for experiments that modify committed documentation; restore after each experiment.
- For experiments needing a clean environment, work in `/tmp`, never inside your working copy.
- Prefer a defined check (rehearsal, fresh clone test, presence test) over a vague feeling that the docs are fine.
- A documentation experiment that uncovers a *code* bug graduates: fix the code bug with a test, in its own commit.

## Intentional break experiments

### Experiment 1 — The fresh clone test (the master experiment)

#### How to cause it
You do not need to break anything — your working machine already hides the breakage. Clone into a clean directory and follow your own README with zero improvisation:

```bash
cd /tmp
git clone <your-repo-url> researchops_fresh
cd researchops_fresh
# Now do ONLY what README.md says, top to bottom.
```

#### Expected error or symptom
Typically several of: a missing prerequisite (Python version, system library such as poppler), a wrong install command (missing extras group), a command renamed since the README was written, a data directory that does not exist in a fresh clone, an environment variable the app needs that nothing documents.

#### How to inspect the failure
Keep a deviation log: every command you had to alter, every step you performed that the README never mentioned, every output that differed from the documented one. The log *is* the inspection artifact.

#### How to fix it
Each deviation is either a docs fix (update the README) or a code fix (create the directory, make the dependency optional, add `.env.example`). Decide per item; never fix by memorizing "oh, you also have to…".

#### Test that should catch it
The fresh clone test itself, repeated until the deviation log is empty. Long-term: the E2E `CliRunner` tests cover the commands; only a clean-environment run covers the *install*.

#### What this failure teaches
"Works on my machine" is invisible state. The README is only true relative to a machine with no state, because that is the only machine your reader has.

#### Common wrong fixes
Adding "troubleshooting" notes instead of fixing the broken step; documenting your personal environment ("make sure your venv is at ~/.venvs/r"); telling the reader to "see the code" for setup.

### Experiment 2 — Wrong expected output in the demo script

#### How to cause it
In `docs/demo.md`, change one expected output from memory — for example, change `Ingested 3 papers.` to `Successfully ingested 3 documents.` Wait a day so you forget which line you altered. Then rehearse the demo.

#### Expected error or symptom
No exception anywhere. The command succeeds, but its real output does not match the script. In a live demo this is the moment an interviewer's trust drops: "is anything else in here wrong?"

#### How to inspect the failure
Rehearse with the script beside the terminal, comparing outputs line by line, not by gist. The mismatch is only visible under exact comparison.

#### How to fix it
Re-run the command and copy-paste its real output into the script. Apply the rule everywhere: documented output is always pasted, never typed.

#### Test that should catch it
A full demo rehearsal in a fresh directory before any occasion the script is used — and after any change to CLI output (the same trigger that mandates `validation.md` updates).

#### What this failure teaches
Documentation drifts in the gap between memory and reality. Exact expected outputs turn a script into a verifiable test; vague ones make it decoration.

#### Common wrong fixes
Softening the script ("you should see something like…") so it can never be wrong — which also makes it unable to catch real regressions; deleting expected outputs entirely.

### Experiment 3 — Docstring in the wrong place

#### How to cause it
In a scratch file, write the docstring *above* the function instead of inside it:

```python
"""Return the top-k results."""
def search(query: str) -> list[str]:
    return []
```

#### Expected error or symptom
No error at all. But `print(search.__doc__)` prints `None`, `help(search)` shows an empty description, and your editor's hover shows nothing. The string was silently absorbed as a module-level expression statement.

#### How to inspect the failure
Check `search.__doc__` in a REPL. Run `python -m pydoc <module>` and observe the function appears with no description.

#### How to fix it
Move the string to be the first statement inside the function body. Re-check `__doc__`.

#### Test that should catch it
The docstring presence test from exercises T1: assert every public method's `__doc__` is non-empty. It fails loudly the moment a docstring goes missing or is misplaced.

#### What this failure teaches
A docstring is a structural element with an exact required position, not a comment that merely needs to be nearby. Tooling sees only what `__doc__` holds.

#### Common wrong fixes
Converting the string to a `#` comment (still invisible to tooling); duplicating the text both above and inside (drifts apart over time).

### Experiment 4 — Broken Mermaid rendering

#### How to cause it
On a scratch branch, break `docs/diagrams/modules.md` three ways, one at a time: (a) delete the `mermaid` language tag from the fence; (b) use an unquoted node label containing parentheses, e.g. `Parse[parse_pdf()]`; (c) insert a blank-line split in the middle of the fenced block. Push and view on GitHub after each.

#### Expected error or symptom
(a) GitHub displays the raw diagram source as a plain code block — no error, just no diagram. (b) Mermaid shows an inline syntax-error box instead of the graph. (c) Half the diagram renders and the rest dumps as text below it.

#### How to inspect the failure
You must view the file on github.com — your local editor preview may render differently or not at all. The render target is the authority.

#### How to fix it
(a) Restore the ` ```mermaid ` tag. (b) Quote the label: `Parse["parse_pdf()"]`. (c) Rejoin the fence. Re-push, re-view.

#### Test that should catch it
A "diagrams render on GitHub" item in the validation checklist, checked after every diagram edit by viewing the pushed file.

#### What this failure teaches
Diagrams-as-code are code: they have syntax, a compiler (the renderer), and silent-failure modes. The render environment, not the source, is what the reader experiences.

#### Common wrong fixes
Replacing the diagram with a screenshot of a successful local render (now it can never be reviewed or updated as text); simplifying labels until they no longer name real code.

### Experiment 5 — The diagram that contradicts the code

#### How to cause it
Add a plausible-but-false arrow to the module diagram — for example `Services --> Storage` — and leave it for a reader to find.

#### Expected error or symptom
Nothing fails mechanically. But the diagram now teaches every reader an architecture violation as if it were the design. An interviewer who knows the codebase will ask: "why do your services import storage directly?" — and your own diagram testifies against you.

#### How to inspect the failure
Re-derive the arrows from imports and diff against the picture:

```bash
grep -rn "^from researchops\|^import researchops" src/researchops/services/
```

Every arrow must correspond to a grep hit; every hit to an arrow.

#### How to fix it
Delete the false arrow and re-verify the whole diagram against the grep output, not just the edge you planted.

#### Test that should catch it
The import-derivation procedure above, run whenever the diagram or the package structure changes. (Week 10's architecture tests guard the code side; nothing but this procedure guards the picture.)

#### What this failure teaches
A wrong diagram is worse than no diagram: absence makes the reader investigate, while wrongness makes them confidently mistaken.

#### Common wrong fixes
"Fixing" the code to match a wrong diagram; adding a disclaimer ("diagram may be out of date") instead of making it correct.

### Experiment 6 — The jargon wall (recruiter persona failure)

#### How to cause it
Rewrite your README's opening paragraph as: "ResearchOps implements a RAG pipeline over Protocol-mediated repositories with cosine-similarity retrieval against locally computed sentence embeddings."

#### Expected error or symptom
Read it to a non-engineer (or apply the no-context test honestly). The reaction is the symptom: they cannot say what the project *does*, who it is *for*, or why it *matters*. Every word is accurate; the paragraph fails anyway.

#### How to inspect the failure
The four-question test from the notes: from paragraph one alone, can a reader answer — what problem does this solve, who is it for, is it real and working, what does using it look like?

#### How to fix it
Restore a plain-language opening: the system's job in everyday words, jargon deferred to the Features and Architecture sections where the engineer persona expects it.

#### Test that should catch it
The read-aloud test with a non-technical listener, repeated whenever the opening changes.

#### What this failure teaches
Correctness is not communication. The first paragraph is written for the least technical reader who matters, because they decide whether anyone else ever reads paragraph two.

#### Common wrong fixes
Dumbing down the entire README (the engineer persona then finds nothing of substance); adding a separate "for non-technical readers" section nobody asked for.

### Experiment 7 — Stale docs after a real change

#### How to cause it
On a scratch branch, rename a CLI command or change its output format (for example, make `ingest` print `Ingested 3 papers (0 skipped).`). Update the code and tests — but deliberately "forget" the README, `docs/demo.md`, and the relevant `validation.md`.

#### Expected error or symptom
The suite is green; the docs are now fiction. The fresh clone test and demo rehearsal fail at the changed command. Anyone following validation.md gets an expected-output mismatch.

#### How to inspect the failure
Grep the documentation for the old command name / old output string:

```bash
grep -rn "Ingested 3 papers\." README.md docs/ curriculum/ --include="*.md"
```

#### How to fix it
Update every hit, in the same commit as the code change. Then revert the whole branch — this was a drill.

#### Test that should catch it
The repository's standing rule, applied as a self-check at commit time: if CLI behaviour or output changed, the diff must also touch README/demo/validation. A grep for the old output string before committing makes the check mechanical.

#### What this failure teaches
Documentation rot is not caused by laziness but by changes that *feel* code-only. The trigger ("output changed") must be wired to the habit ("grep the docs"), or rot is guaranteed.

#### Common wrong fixes
Scheduling a "docs cleanup week" later (the drift compounds); loosening documented outputs until they match anything.

### Experiment 8 — README self-contradiction

#### How to cause it
Introduce a contradiction between two README sections: claim "supports PostgreSQL and SQLite" in Features while the Quick Start and architecture mention only SQLite; or set Project Status to "alpha" while the title says "v1.0.0".

#### Expected error or symptom
No tool complains. A careful reader notices and — like the wrong expected output — begins doubting every other claim. An interviewer may probe the contradiction directly: "where is the PostgreSQL support?"

#### How to inspect the failure
Read the README in one sitting *backwards*, section by section, asking of each claim: which earlier section confirms or contradicts this? Backwards reading defeats the skimming that hides contradictions.

#### How to fix it
Make the weaker claim true everywhere: features list only what exists; status matches the version; architecture matches the features.

#### Test that should catch it
The backwards read after every substantial README edit, plus the F1 single-sourcing exercise for facts that appear in several places.

#### What this failure teaches
Long-form documents drift internally just as code and docs drift mutually. Consistency requires an explicit pass; it does not emerge from writing sections one at a time.

#### Common wrong fixes
Resolving toward the *stronger* claim ("I'll add PostgreSQL support, then") — scope creep disguised as a docs fix; deleting the status section so nothing can disagree with it.

### Experiment 9 — Broken relative links

#### How to cause it
In `docs/demo.md`, write a link to the architecture doc as `[architecture]` + `(ARCHITECTURE.md)` — a target resolved relative to `docs/`, where no such file exists. Push and click the link on GitHub.

#### Expected error or symptom
GitHub 404s. Locally, some editors helpfully resolve the link anyway, which is why the bug survives review.

#### How to inspect the failure
Click every link in the pushed file on github.com. For a systematic pass, list link targets and test each from the file's directory:

```bash
grep -on "](\([^)]*\.md[^)]*\))" docs/*.md
```

#### How to fix it
Use the correct relative path from the *file's* location: `../ARCHITECTURE.md`. Re-push, re-click.

#### Test that should catch it
A link-click pass over changed files as part of validation. (A link-checker tool could automate this later; this week, the manual pass builds the habit the tool would encode.)

#### What this failure teaches
Relative links resolve from the containing file, not the repository root — and the rendering environment, not the editor, decides what works.

#### Common wrong fixes
Switching every link to an absolute `https://github.com/...` URL (breaks for forks, clones, and offline reading); removing links instead of fixing paths.

## Debugging checklist

When any documentation problem surfaces, walk this list:

1. **Reproduce in the reader's environment** — fresh clone in `/tmp`, pushed file on github.com, never your stateful working copy or editor preview.
2. **Classify the failure**: docs wrong (fix the text), code wrong (fix the code, with a test, in its own commit), environment undocumented (document the prerequisite).
3. **Compare exactly, not by gist** — diff documented output against real output line by line.
4. **Re-derive, don't recall** — diagrams from `grep` on imports, expected outputs from real runs, link targets by clicking.
5. **Search for siblings** — one stale command usually has stale relatives; grep the old string across all `*.md`.
6. **Close the loop** — after fixing, identify which check (rehearsal, fresh clone, presence test, backwards read, link pass) *should* have caught it, and make that check part of your routine.

## Reflection after breaking

Answer in your `reflection.md`:

1. How many fresh-clone passes did it take to reach an empty deviation log, and what was the most surprising deviation?
2. Which experiment produced a failure with no error message at all? How would you notice that failure class in the wild?
3. Which documentation claim of yours turned out to be false before you started this lab?
4. Of the checks in the debugging checklist, which one will you realistically run every week — and which will you skip unless forced? What does that tell you about where your docs will rot first?
5. What is one habit from this lab you will carry into every future repository?

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 19 — Documentation and Portfolio Polish:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
