# Week 20 Exercises: Final Hardening and v1.0 Release

## Warm-up exercises

### 1. Define "done" in your own words

Write a definition of "done" for a software project in your own words. Include:
- What conditions must be true before you call it done.
- What "done" does not require.
- How you would know if someone else's project is done.

Then compare your definition to the one in notes.md. Where does it differ?

### 2. Scope inventory

List 10 things you wanted to add to ResearchOps but did not. For each item, decide:
- v1.1 candidate: would make the project meaningfully better without changing its core purpose.
- Future idea: interesting but out of scope.
- Never: you would not actually build this.

Resist the urge to add any of them to v1.0.0. Document the v1.1 candidates in `ROADMAP.md`.

### 3. Explain semantic versioning

Write a paragraph explaining MAJOR.MINOR.PATCH versioning without referencing the notes. Then:
- What version would you assign if you fixed a bug in the search ranking? (→ PATCH)
- What version would you assign if you added streaming API responses? (→ MINOR)
- What version would you assign if you renamed the `researchops search` command to `researchops find` (breaking change)? (→ MAJOR)

---

## Project exercises

### 1. Run the full pre-release checklist

Copy the checklist from notes.md into a temporary file. Work through every item. Fix anything that fails. Do not mark an item complete unless you have actually run the command and seen the expected output.

Pay special attention to:
- Starting from a **fresh clone** for the final validation.
- Verifying the Docker build works.
- Confirming that the demo script produces correct output.

### 2. Complete CHANGELOG.md

Write or update `CHANGELOG.md` to include a `[1.0.0]` section with today's date. List:
- All major features added across Weeks 17–20.
- Any significant changes made to previous features.
- Any bugs fixed during Week 20 hardening.

The changelog must be written for a user, not a developer. Do not list commit messages. Describe what the user can now do that they could not do before.

### 3. Bump the version to 1.0.0

Update the version in both required places:

```bash
# In pyproject.toml
version = "1.0.0"

# In src/researchops/__init__.py
__version__ = "1.0.0"
```

Verify they match:

```bash
python -c "import researchops; print(researchops.__version__)"
# Expected: 1.0.0
```

Also verify that `pyproject.toml` shows `1.0.0`:

```bash
grep '^version' pyproject.toml
# Expected: version = "1.0.0"
```

### 4. Run the demo script end to end

Follow `docs/demo.md` exactly, in order, from a fresh clone. If any command does not produce the expected output:
- Fix the command in the code if the code is wrong.
- Fix the expected output in the script if the output changed.
- Fix the environment documentation if a setup step is missing.

Do not adjust the expected output to match wrong behaviour. Fix the behaviour.

### 5. Create the v1.0.0 git tag

After all other checklist items pass:

```bash
git add .
git commit -m "v1.0.0: final release"
git tag -a v1.0.0 -m "ResearchOps v1.0.0 — 20-week build complete"
git push
git push --tags
```

Verify on GitHub that the tag exists and that the repository shows `v1.0.0` in the Releases or Tags section.

### 6. Write the final reflection.md

In `curriculum/month-05-production-portfolio/week-20-final-hardening-v1-release/reflection.md`, complete the final reflection. Answer every question in the template honestly.

The quality of this reflection is not judged by how good the project is. It is judged by how honestly you engage with what you learned.

---

## Stretch exercises

### 1. Create a GitHub Release

On GitHub:
1. Go to Releases → Draft a new release.
2. Choose the `v1.0.0` tag.
3. Write release notes using the template from notes.md.
4. Publish the release.

A published GitHub Release is more compelling in a portfolio than a bare git tag.

### 2. Write a LinkedIn post

Write a draft LinkedIn post (you do not need to publish it) announcing the completion of ResearchOps v1.0.0. Include:
- What the project is (one sentence).
- What you learned (two to three specific things).
- A link to the repository.
- One thing you would build next.

Keep it under 300 words. If you cannot describe the project and what you learned in 300 words, you do not yet understand it well enough to present it.

### 3. Update ROADMAP.md

Rewrite `ROADMAP.md` to clearly show:
- All 20 weeks marked as ✅ complete.
- A v1.1 section with the concrete features you would build next.
- A v2.0 section with longer-horizon ideas.

This is the document you hand to someone who asks "where is this project going?"

---

## Writing questions

Answer these in your final `reflection.md`:

1. What is the single most important technical decision you made in 20 weeks? Why was it important?
2. How is your understanding of Python different now compared to when you started? Be specific: name three things you understand now that you did not before.
3. What would you tell someone starting this curriculum? What would save them the most time?
4. Rate your confidence (1–10) in each area at the end of Week 20: Python fundamentals, clean architecture, testing, SQL/storage, ML engineering, async I/O, API development, Docker, AI engineering (embeddings, RAG).
5. What will you build next?
