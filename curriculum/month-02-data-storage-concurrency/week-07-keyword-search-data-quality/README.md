# Week 07 - Keyword Search and Data Quality

## Learning objectives
- Normalize text for reliable keyword matching.
- Tokenize and rank simple search results.
- Design a `researchops search` command over stored data.
- Identify data-quality issues such as empty text, duplicates, and noisy extraction.
- Compare exact matching with normalized matching.
- Write tests for ranking and edge cases.
- Treat search quality as a measurable engineering problem.

## Project milestone
Add keyword search over ingested documents and build the first text-quality checks for parsed content.

## Files to modify/create
- `src/researchops/search/normalize.py`
- `src/researchops/search/keyword.py`
- `src/researchops/cli/search.py`
- `tests/unit/test_normalize.py`
- `tests/unit/test_keyword_search.py`
- `tests/integration/test_search_command.py`

## Concepts covered
Text normalization, tokenization, ranking heuristics, basic IR concepts, data quality checks, and searchable CLI workflows.

## Expected deliverables
- A normalization layer for lowercase, whitespace cleanup, and punctuation handling.
- A keyword search function that returns ranked results.
- A CLI command to query SQLite-backed documents.
- Tests covering result order and edge cases.

## Definition of done
- [ ] Search works against stored documents.
- [ ] Normalization is consistent and tested.
- [ ] Ranking is deterministic.
- [ ] Empty or low-quality documents are handled.
- [ ] Search CLI prints useful snippets or counts.
- [ ] Integration tests cover realistic queries.
- [ ] You can explain the limits of keyword search.
