# ADR-0003: Build the CLI Before the HTTP API

- **Status:** Accepted
- **Date:** Week 4
- **Source:** New ADR required by the project spec; complements ADR-001/003 in
  [`adr-log.md`](./adr-log.md)

> Beginner note: "CLI" means *command-line interface* — the program you run in a
> terminal, like `researchops scan ./papers`. "API" here means an *HTTP API* — a
> web server other programs talk to over the network (built with FastAPI in
> Week 14). This ADR explains why ResearchOps grows a terminal tool first and a
> web server later.

## Decision title

Deliver ResearchOps features through a **command-line interface first**, and add
the **FastAPI HTTP layer later** (Week 14), once the underlying service logic
already works locally.

## Context

Every ResearchOps feature has two parts:

1. **The logic** — ingest papers, search, classify, answer questions. This lives
   in the **service layer** and knows nothing about *how* it is called.
2. **The transport** — the way a user triggers the logic. A CLI command and an
   HTTP route are both just *transports* in front of the same service.

A common beginner trap is to start with the web server because it looks
impressive. But an HTTP API adds a whole stack of incidental complexity —
servers, ports, request/response schemas, status codes, serialization,
async handlers — *before* the actual feature works. You end up debugging HTTP
plumbing instead of the problem you care about.

A CLI is the **thinnest possible transport**: parse a couple of arguments, call a
service function, print the result. It lets you prove the logic with almost no
ceremony.

## Decision

Adopt a strict ordering: **logic → CLI → API.**

- Implement each capability in a **service** that takes its dependencies via
  constructor injection and returns plain Python objects.
- Expose it first through a **Typer CLI command** that does nothing but parse
  input, call the service, and render output.
- Only after the service is proven locally, add a **FastAPI route** that calls the
  *same* service. The API introduces no new business logic.

The CLI's command layer also serves as the **composition root** — the single
place where concrete adapters (SQLite repository, PDF parser) are constructed and
wired into services.

## Why CLI comes before FastAPI

- **Fastest feedback loop.** `researchops scan ./papers` runs instantly; no
  server to boot, no HTTP client to script.
- **Smallest surface area.** A CLI command is a few lines, so bugs are almost
  always in the logic, not the transport.
- **Forces clean layering.** If the CLI can drive a feature with a plain function
  call, the service is genuinely decoupled from transport — which is exactly what
  makes adding HTTP later trivial.

## Why local service logic must work before HTTP

- HTTP multiplies failure modes: a broken result is now also a serialization
  question, a status-code question, and an async question. Debugging through that
  stack is slow.
- If the service is correct locally, the HTTP route becomes a thin adapter:
  validate the request, call the service, map the result to a response. Nothing
  interesting can break there.
- Tests stay fast and focused: service logic is unit-tested directly; the API
  layer only needs a few thin integration tests.

## Why this prevents "platform cosplay"

*Platform cosplay* is building things that **look** like a serious platform — a
web server, routes, Docker, dashboards — while the **core capability underneath
does not actually work.** Starting with the API encourages this: you get a nice
`/search` endpoint that returns fake or hardcoded data.

Forcing a working CLI first means the capability must be **real** before it is
ever dressed up in HTTP. The terminal output is the proof. Only genuine,
working logic is allowed to graduate to an API.

## Consequences

**Positive**

- Each feature is validated end to end before any HTTP exists.
- The service layer stays transport-agnostic and reusable by CLI, API, and jobs.
- The composition root is established early and reused by the API later.
- Onboarding is easy: a new contributor can exercise everything from a terminal.

**Negative / costs**

- Users who only want an HTTP API wait until Week 14.
- Some output rendering work is done twice (terminal formatting, then JSON
  schemas) — but the *logic* is never duplicated.
- Discipline required: it is tempting to sneak logic into a route handler later;
  ADR-0001's layering rules must be upheld.

## Alternatives considered

1. **API-first (FastAPI from Week 1).** Rejected: maximises incidental
   complexity early and invites platform cosplay with hollow endpoints.
2. **Library-only (no CLI, importable functions only).** Rejected: gives no
   runnable, demoable artifact for a learner and makes manual validation
   awkward.
3. **CLI and API together from the start.** Rejected: doubles the transport
   surface before any feature is proven, slowing the core feedback loop.

## Related curriculum weeks

- **Week 4 — CLI & Packaging:** establishes Typer commands and the composition
  root this ADR depends on.
- **Week 6 — PDF Parsing Pipeline:** ingestion is driven and validated through
  the CLI before any API exists.
- **Week 7 — Keyword Search & Data Quality:** search ships as a CLI command
  first, proving the service end to end.
- **Week 14 — FastAPI Layer:** the API is finally added as a *thin* transport
  over the already-working services.
- **Week 18 — Docker & Environment Config:** packages the API for deployment —
  appropriate only because the logic behind it is already proven, not cosplay.
