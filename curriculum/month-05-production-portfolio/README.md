# Month 5 — Production and Portfolio

> **Book section 5 of 5.** The final month. You turn a working AI platform into a
> **credible, presentable portfolio project**: grounded RAG answers, containers,
> documentation, a demo, and a real release.

---

## The big idea of the month

Everything works — now make it **trustworthy, runnable by strangers, and worth
showing.** This month you build the RAG assistant that answers questions with
**citations** and refuses to make things up, you make it **testable without a real
LLM** (a fake generator) while keeping **optional real providers**, you containerise
and configure it with Docker and environment variables, and you write the
documentation, demo, and release discipline that make ResearchOps a portfolio
piece rather than a folder of code.

The theme: **a project is not done when it works — it is done when someone else
can run it, trust it, and understand it.**

## What you already know before this month

From Months 1–4 you can:

- Build clean, layered, tested Python applications.
- Persist, parse, search (keyword and semantic), and parallelise.
- Train and track ML models.
- Serve services over FastAPI, fetch asynchronously, and run background jobs.
- Retrieve semantically relevant, source-tagged context.

You do **not** need prior experience with RAG, Docker, or releasing software.

## What you will learn this month

- **RAG (Retrieval-Augmented Generation)** — combining retrieval with a generator
  to answer questions from your own corpus.
- **Citations** — tying every answer back to the chunks that support it.
- **Hallucination control** — making the system say "insufficient evidence"
  instead of inventing answers.
- **A fake generator for tests** — deterministic answers so the test suite needs
  no network or real model.
- **Optional real model providers** — pluggable real LLMs behind the same
  interface, off by default.
- **Docker** — containerising the app for reproducible runs.
- **Environment config** — settings via environment variables and `.env`, with
  secrets kept out of Git.
- **Documentation** — a README, architecture docs, and a runnable demo.
- **Demo design** and **release checklist** — presenting and shipping v1.0.0.
- **Final validation** and **portfolio storytelling** — proving and narrating the
  work.

## What ResearchOps capability will exist by the end

The ability to **present ResearchOps as a coherent AI engineering portfolio
project**:

```bash
researchops ask "What methods does the corpus use for low-resource NLP?"
# → an answer grounded in retrieved chunks, with citations,
#   or an honest "insufficient evidence" when the corpus cannot support it
docker compose up --build      # the whole platform, reproducibly, in containers
```

Backed by tested RAG, documentation, a demo, and a tagged `v1.0.0` release.

## Week-by-week chapter flow

| Week | Chapter | What it adds |
|---|---|---|
| **Week 17 — RAG Assistant** | "Grounded answers" | Retrieval + generation, citations, fallback, a fake generator for tests. |
| **Week 18 — Docker & Environment Config** | "Runs anywhere" | Dockerfile, compose, settings from env, secret hygiene. |
| **Week 19 — Documentation & Portfolio Polish** | "Tell the story" | README, architecture docs, runnable demo, retrospective. |
| **Week 20 — Final Hardening & v1.0.0 Release** | "Ship it" | Final validation, changelog, version bump, the release tag. |

## How each week connects to the previous week

- **Week 17 → 18:** once the RAG assistant works and is tested with a fake
  generator, Week 18 packages it so anyone can run it the same way you do.
- **Week 18 → 19:** once the app runs reproducibly in a container, Week 19
  documents *how and why*, with a demo someone can actually follow.
- **Week 19 → 20:** once the docs and demo are honest and tested, Week 20 does the
  final hardening, writes an accurate changelog, and cuts the `v1.0.0` release.

## What not to skip

- **Citations and the "insufficient evidence" path (Week 17).** A RAG system that
  cannot cite or cannot refuse is not trustworthy.
- **The fake generator (Week 17).** Tests must not require a real LLM or network.
- **Secret hygiene (Week 18).** `.env` with real secrets must never be committed;
  commit only `.env.example`.
- **Testing the README commands (Week 19).** Untested setup instructions are how
  fresh clones fail for everyone but you.
- **Honest changelog and passing final validation (Week 20).** Do not claim
  features that are not done.

## What concepts must be understood before moving on

Be able to explain aloud:

- The full RAG pipeline: `question → retrieve chunks → build prompt → generate →
  answer with citations`.
- How citations are produced and why every answer must trace to its sources.
- How the system decides it has insufficient evidence and declines to answer.
- Why a fake generator makes RAG testable, and how a real provider plugs in
  behind the same interface.
- The difference between an image and a container, and build-time vs runtime
  config.
- Why secrets belong in the environment, not in the repository.
- What a release checklist guarantees and why the changelog must match reality.

## Month-end self-assessment

Rate yourself 1–10 with evidence:

- [ ] I can trace a RAG answer from question to cited chunks.
- [ ] My assistant says "insufficient evidence" when the corpus cannot support an
      answer.
- [ ] My test suite exercises RAG with a fake generator — no network required.
- [ ] I can swap in a real provider behind the same interface without changing
      services.
- [ ] I can build and run the app with Docker and configure it via environment
      variables.
- [ ] I keep secrets out of Git and ship only `.env.example`.
- [ ] My README commands work on a fresh clone.
- [ ] My changelog accurately reflects what v1.0.0 actually does.

## Month-end mini capstone (the final capstone)

Ship ResearchOps v1.0.0:

1. Ask a question the corpus *can* answer; get a grounded answer **with
   citations.**
2. Ask a question the corpus *cannot* answer; get an honest "insufficient
   evidence" response.
3. Run the entire test suite — including RAG — with **no** network and **no** real
   model, using the fake generator.
4. `docker compose up --build` and exercise the app exactly as documented.
5. Follow `docs/demo.md` end to end; fix anything that does not match reality.
6. Bump the version, write the `[1.0.0]` changelog entry, run final validation,
   and tag the release.

Done when a stranger could clone, run, and understand the project from your docs
alone.

## Bridge to "next" (after v1.0.0)

There is no Month 6 — but a good portfolio project invites a *next chapter*. With
v1.0.0 shipped, candidate directions include: a richer evaluation harness for RAG
quality, a real vector database, a hosted deployment, or splitting a heavy module
into its own package (revisit
[ADR-0001](../../docs/decisions/0001-modular-monolith.md) for when that is
justified). Capture these as roadmap items — not unfinished claims in v1.0.0.

## Warning signs you are not ready to "ship"

- Answers do not cite their supporting chunks.
- The system confidently answers questions the corpus cannot support.
- Tests require a real LLM or network access.
- Docker "works" but hides a broken local setup, or `.env` secrets are committed.
- README commands are untested, or architecture docs contradict the code.
- The changelog claims features that are not finished, or final validation fails.

## Suggested weekly study rhythm

~8–10 hours/week (more writing, less new code than earlier months):

- **Read** week README + notes (~1 hr).
- **Build/polish** in small commits (~4–5 hrs).
- **Break it** with `break_it.md` (~1 hr) — ask an unanswerable question, commit a
  fake secret and catch it.
- **Test and document** (~2 hrs) — docs and demos count as deliverables here.
- **Reflect** in `reflection.md` and the weekly report (~30–45 min).

## Suggested Git milestone at end of month

The capstone milestone of the whole journey — a real release tag:

```bash
git add .
git commit -m "v1.0.0: ResearchOps final release"
git tag -a v1.0.0 -m "ResearchOps v1.0.0"
```

Your repository should now present as a complete, runnable, documented,
portfolio-grade AI engineering project — and you should be able to tell its story
with confidence.
