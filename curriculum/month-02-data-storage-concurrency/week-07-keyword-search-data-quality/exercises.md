# Exercises - Week 07 Keyword Search and Data Quality

## Warm-up exercises
1. Normalize a sentence with mixed case and punctuation.
2. Count how many times a query term appears in a document.
3. Return an empty list when the query is blank.
4. Build a short snippet around the first keyword match.

## Project exercises
1. Implement `normalize_text` and token helpers with tests.
2. Create a ranked keyword search over stored parsed documents.
3. Add `researchops search "query" --db researchops.db`.
4. Add data-quality checks that flag empty or suspiciously short documents.

## Stretch exercises
1. Ignore common stop words such as `the`, `and`, and `of`.
2. Add phrase matching that boosts exact consecutive terms.
3. Highlight matched terms in CLI output.

## Writing questions
1. Which normalization choice mattered most for your results?
2. What data-quality issue hurt search relevance the most?
3. How would you explain ranking to a non-technical user?
4. Where does keyword search obviously fall short?
