# Week 19 Exercises: Documentation and Portfolio Polish

## Warm-up exercises

### 1. Find excellent READMEs

Find three open-source Python projects on GitHub with excellent READMEs. Study each one and answer:
- Does it have a one-paragraph description at the top?
- Does it have a working Quick Start section?
- Does it have architecture documentation?
- Does it have a limitations or known issues section?
- What do all three have in common?

Suggested starting points: `fastapi/fastapi`, `pydantic/pydantic`, `tiangolo/sqlmodel`.

### 2. Explain ResearchOps in one paragraph

Write one paragraph explaining ResearchOps to someone who has never heard of it and has no ML background. Constraints:
- No jargon in the first two sentences.
- Must include: what it does, who it is for, and one concrete example of using it.
- Must be under 100 words.

Then write a second version for a technical interviewer. Allow jargon. Mention the architectural choices briefly.

### 3. Draw the module dependency diagram from memory

On paper (or in a text editor), draw the module dependency diagram. Do not look at the code first. Then compare your drawing to the actual imports in `src/researchops/`. Note every module you forgot, every dependency you got wrong, and every unexpected coupling you find.

---

## Project exercises

### 1. Write the final README

Write a complete `README.md` for ResearchOps following the structure from notes.md. Spend at least 90 minutes on it. Include:
- One-paragraph description.
- One-sentence audience statement.
- Quick Start section (test it from a fresh directory).
- Features list.
- Architecture section with a Mermaid diagram.
- At least two usage examples with commands and expected output.
- How to run tests.
- Project status section.
- Known limitations.
- Future work.

Do not submit the README until you have tested the Quick Start commands yourself.

### 2. Create a Mermaid diagram for the ingestion pipeline

In `docs/diagrams/ingestion.md` or inline in `ARCHITECTURE.md`, create a Mermaid diagram showing:

```
directory → scan → parse → chunk → embed → store
```

Label each step with the actual Python module or function name from the codebase. Verify that the diagram matches the code by tracing the actual call stack.

### 3. Create a Mermaid diagram for the RAG pipeline

In `docs/diagrams/rag.md` or inline in `ARCHITECTURE.md`, create a Mermaid diagram showing the 7-step RAG pipeline from Week 17 notes. Label each step with the class or method that implements it.

### 4. Write docs/demo.md

Write a `docs/demo.md` file following the 2-minute demo template from notes.md. The script must:
- Start from a fresh clone (with no existing `.venv` or `data/`).
- Include all five sections: setup, ingest, search, ask, API.
- Show exact commands.
- Show expected output (copy actual output from a real run).

Run through the script from start to finish in a fresh directory before calling it done. Fix every command that does not produce the expected output.

### 5. Write docs/retrospective.md

Write a `docs/retrospective.md` covering 19 weeks of learning. Answer all five questions from notes.md:
1. What is the most important design decision you made? Why?
2. What would you do differently if you started over?
3. What is the hardest concept you encountered?
4. What are you most proud of?
5. What would you build in the next 5 weeks?

This document is for you. Write it honestly.

### 6. Update ARCHITECTURE.md

Ensure `ARCHITECTURE.md` accurately describes the current state of the codebase. Update or add:
- A module overview listing each package in `src/researchops/` with a one-sentence description.
- The ingestion diagram.
- The RAG pipeline diagram.
- A section on design decisions: why SQLite, why editable install, why Protocol-based interfaces.

---

## Stretch exercises

### 1. Record a screen capture

Record a 2-minute demo using Loom, OBS, QuickTime, or any screen recorder. Follow `docs/demo.md` exactly. Link the recording URL from the README. Even a rough recording shows employers that the project actually works.

### 2. GitHub Pages site

Enable GitHub Pages on the repository. Point it to the `docs/` directory. Verify that the site renders correctly and that all Mermaid diagrams display.

### 3. Write a draft blog post

Write a draft blog post titled "What I learned building a RAG assistant in 20 weeks". Sections:
- The project in one paragraph
- Three things I got wrong at first
- One architectural decision I am proud of
- What I would do differently
- What I would build next

This does not need to be published. Writing it sharpens your interview narrative.

---

## Writing questions

Answer these in your `reflection.md`:

1. After the fresh clone test: what broke? What did you assume would be documented that was not?
2. Who is the most important reader of your README? What do they need to know in the first 30 seconds?
3. What is one tradeoff you made in this project? Write the explanation using the four-part structure from notes.md.
4. What is the one sentence summary of your portfolio story?
5. Which part of the documentation took longer than expected? Why?
