# Exercises - Week 05 SQLite Storage Layer

## Warm-up exercises
1. Create a SQLite database file and connect with `sqlite3`.
2. Write a table with a text primary key and insert one row.
3. Query rows and print them using column names.
4. Experiment with a transaction that rolls back after an exception.

## Project exercises
1. Design and implement the ResearchOps schema for papers and parsed documents.
2. Add a repository with `save`, `get_by_id`, and `list_recent` methods.
3. Map database rows back into `Paper` and `ParsedDocument` objects.
4. Write an integration test that proves a full save-and-load round trip.

## Stretch exercises
1. Add a `failed_documents` table for parse errors.
2. Add a unique constraint that prevents duplicate source paths.
3. Add a migration helper that can evolve the schema safely.

## Writing questions
1. Why is a transaction necessary for multi-table writes?
2. What logic belongs in the repository versus the model?
3. Which schema decision felt hardest?
4. What bug would a round-trip test catch that a mock would miss?
