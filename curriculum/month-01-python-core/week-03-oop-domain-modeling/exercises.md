# Exercises - Week 03 OOP and Domain Modeling

## Warm-up exercises
1. Convert a dictionary-based paper record into a `@dataclass`.
2. Add a method that returns a paper slug from its title.
3. Write a `__post_init__` check that rejects blank titles.
4. Compare two dataclass instances for equality in a test.

## Project exercises
1. Implement `Paper`, `ParsedDocument`, `IngestionResult`, and `FailedDocument`.
2. Refactor scanner output so it can become `Paper` objects.
3. Add factory helpers in tests for creating sample papers and parsed documents.
4. Write tests for success counts, failure counts, and invalid initialization.

## Stretch exercises
1. Make one model immutable with `frozen=True` and note the trade-offs.
2. Add a method that returns a dictionary suitable for JSON serialization.
3. Add a domain-specific `display_name()` method for CLI output.

## Writing questions
1. Why is a dataclass better than a loose dictionary here?
2. Which fields feel essential versus optional?
3. What invariant did you enforce, and why?
4. Where should behavior live: on the model or in a service?
