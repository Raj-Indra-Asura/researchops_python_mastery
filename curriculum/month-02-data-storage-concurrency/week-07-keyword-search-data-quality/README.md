# Week 07 — Keyword Search and Data Quality

> **Chapter title: "Finding signal in stored text."**
> The week ResearchOps becomes searchable — and learns to distrust its own data.

---

## 1. Week title

Week 7 — Keyword Search and Data Quality (Month 2, Chapter 3 of 4).

## 2. Story of the week

You can ingest papers and store clean text — but right now the only way to find
anything is to read every row. This week you make the library *queryable*. You
build keyword search with simple normalisation and ranking, return results as
`SearchResult` domain objects, and add data-quality checks and statistics so you
can see, at a glance, how healthy your corpus is. Crucially, you do all of this
with **unit tests backed by fake repositories** — no database required — proving
the architecture you have been building actually pays off.

## 3. What you already know

- From Week 6: ingested, cleaned, stored paper text and failure records.
- From Week 5: the repository pattern and `PaperRepository`.
- From Month 1: text handling, dataclasses, pytest.
- The idea of fakes (you will lean on `FakePaperRepository` heavily).

## 4. What this week adds

- An **in-memory inverted index** and the basics of how search works.
- **Text normalisation**: lowercasing, punctuation stripping, stopwords.
- Simple **scoring and ranking** of results.
- **Data-quality gates**: detecting and reporting bad/empty/suspect data.
- `SearchService`, `PaperService` (stats/list/show), and the `SearchResult`
  domain object.
- **Unit testing with fakes** — fast tests that never touch SQLite.

## 5. Why this week matters

Search is the first feature a *user* actually cares about, and it is the first one
you can test entirely with fakes — because `SearchService` depends on the
`PaperRepository` protocol, not on SQLite. That makes its tests fast and pure, and
proves the Week-5 repository boundary was worth it. Data-quality gates teach a
mindset that becomes essential in ML and RAG: **garbage in, garbage out** — you
must measure and guard your data before you trust any result built on it.

## 6. Learning objectives

By the end of the week you can:

- Implement basic keyword search with normalisation and ranking.
- Return search results as domain objects with relevance ordering.
- Define and apply a data-quality gate.
- Compute corpus statistics (counts, failures, coverage).
- Write fast **unit** tests using `FakePaperRepository` — no database.
- Explain why search logic belongs in a service, not the CLI.

## 7. Project milestone

`researchops search "transformer attention"` returns ranked results from stored
papers, and `researchops papers stats` summarises the corpus.

## 8. Files / modules touched

- `src/researchops/services/search_service.py` — keyword search + ranking.
- `src/researchops/services/paper_service.py` — stats, list, show.
- `src/researchops/core/models.py` — `SearchResult` (already present; study it).
- `src/researchops/cli/commands/search.py` and `.../papers.py` — thin wiring.

## 9. Commands introduced

```bash
researchops search "machine learning"   # ranked keyword results
researchops papers stats                  # corpus statistics
researchops papers show <id>             # inspect one paper
```

## 10. Tests involved

- `tests/unit/test_search_service.py` — search via `FakePaperRepository`.
- `tests/unit/test_paper_service.py` — stats/list/show via fakes.

```bash
pytest tests/unit/test_search_service.py -v
```

## 11. Study plan for the week

1. **Day 1 — Normalisation.** Build lowercasing, punctuation stripping, and a
   small stopword list; test each in isolation.
2. **Day 2 — Index + scoring.** Build a simple inverted index and a ranking
   function; understand why ranking order matters.
3. **Day 3 — SearchService with fakes.** Implement search against
   `PaperRepository`; unit-test with `FakePaperRepository`.
4. **Day 4 — PaperService + data quality.** Stats, list, show; add a quality gate
   that flags empty or suspect text.
5. **Day 5 — Wire CLI + milestone + report.**

## 12. Estimated time breakdown

| Activity | Time |
|---|---|
| Reading + normalisation | ~1.5 hrs |
| Index + scoring/ranking | ~2.5 hrs |
| SearchService + unit tests with fakes | ~2.5 hrs |
| PaperService + data-quality gate | ~2 hrs |
| Reflection + report | ~1 hr |

## 13. How to know the learner is stuck

- Your search tests construct a real SQLite database (they should use a fake).
- Results come back in arbitrary order (no ranking applied).
- Search logic lives inside the CLI command instead of `SearchService`.
- "Stats" counts rows but ignores failed/empty documents.

## 14. Definition of done

- [ ] `search` returns ranked `SearchResult` objects.
- [ ] Text normalisation (lowercase, punctuation, stopwords) is applied.
- [ ] `SearchService` depends only on `PaperRepository`, not SQLite.
- [ ] Unit tests use `FakePaperRepository` and create no database file.
- [ ] `papers stats` reports meaningful corpus health (incl. failures).
- [ ] A data-quality gate flags at least one class of bad data.
- [ ] CLI commands stay thin; logic lives in services.

## 15. Ruthless mentor checkpoint

- "Run your search unit tests. Did any `.db` file appear? If yes, they are not
  unit tests."
- "Search for the same term twice with different casing. Same results?"
- "What does `papers stats` tell me that I could not see by eyeballing the rows?"

If search ranking is arbitrary or your 'unit' tests hit SQLite, you are not done.

## 16. What not to do this week

- Do **not** test `SearchService` against a real database — use the fake.
- Do **not** put search/ranking logic in the CLI handler.
- Do **not** over-engineer scoring; a simple, explainable ranking beats a clever
  one you cannot reason about.
- Do **not** ignore empty/garbled text — that is exactly what the quality gate is
  for.

## 17. Bridge to next week

Ingestion and search both work and are well tested — but ingesting a large folder
is slow because PDFs are parsed one at a time. **Week 8** keeps the behavior
identical while making it **fast**: parallel parsing with `ProcessPoolExecutor`.
Because this week's logic is correct and covered by tests, you can change *how*
ingestion runs next week and prove the result is unchanged — performance added
only after correctness.
