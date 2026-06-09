# Architecture Decision Log

Record important decisions here as you make them throughout the 20 weeks.

## Format

**ADR-NNN: Short Title**
- Date: YYYY-MM-DD
- Status: Accepted / Superseded / Deprecated
- Context: Why did this decision need to be made?
- Decision: What was decided?
- Consequences: What are the tradeoffs?

---

## ADR-001: Use modular monolith instead of multiple packages

- Date: Week 1
- Status: Accepted
- Context: Should we create separate Python packages for core, storage, services, etc.?
- Decision: Keep everything in a single `researchops` package with strict import rules enforced by convention (and eventually import-linter).
- Consequences: Easier to develop and refactor. Import rules must be followed manually until automated. Can be split later if needed.

## ADR-002: Use raw sqlite3 instead of SQLAlchemy (initially)

- Date: Week 5
- Status: Accepted
- Context: Should we introduce SQLAlchemy ORM from the beginning?
- Decision: Start with raw `sqlite3` to understand what ORMs are solving. Introduce SQLAlchemy as an optional refactor in Week 5.
- Consequences: More boilerplate initially, but better understanding of SQL. Easy to migrate to SQLAlchemy later.

## ADR-003: Use ProcessPoolExecutor for PDF parsing (not ThreadPoolExecutor)

- Date: Week 8
- Status: Accepted
- Context: PDF parsing is CPU-bound. Should we use threads or processes?
- Decision: Use `ProcessPoolExecutor` because Python's GIL prevents true CPU parallelism with threads.
- Consequences: Better CPU utilisation for parsing. Requires all worker arguments/returns to be picklable.
