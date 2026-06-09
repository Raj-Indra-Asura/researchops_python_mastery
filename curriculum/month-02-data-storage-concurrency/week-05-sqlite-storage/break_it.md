# Break It - Week 05 SQLite Storage Layer

## Intentional failure experiments
1. Insert the same paper twice and inspect the unique-constraint failure.
2. Fail the second statement inside a transaction and verify the first write is rolled back.
3. Query a column name that does not exist and read the error carefully.
4. Store `Path` objects directly without converting to string and observe the mismatch.
5. Skip schema initialization and run repository methods against an empty database file.

## Debugging tasks
- Print the actual rows in SQLite after a failed write.
- Run only integration storage tests with `pytest -k storage_roundtrip -v`.
- Compare database contents before and after rollback.

## Edge cases to explore
- Empty parsed text.
- Very long document text.
- Duplicate titles with different file paths.
- Missing related rows between tables.

## What did you learn?
- Which constraint saved you from bad data?
- What did transactions protect you from?
- How will you keep SQL readable as the schema grows?
