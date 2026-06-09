# Exercises - Week 09 Protocols and Clean Architecture

## Warm-up exercises
1. Write a tiny protocol for an object with a `save()` method.
2. Create two classes that satisfy the protocol without inheriting from anything.
3. Pass a fake dependency into a service and assert on captured state.
4. Identify one place where your code imports a concrete class unnecessarily.

## Project exercises
1. Define repository and parser protocols for the ResearchOps services.
2. Refactor ingestion and search services to depend on protocols.
3. Add an in-memory fake repository for unit tests.
4. Rewrite at least one service test to avoid SQLite entirely.

## Stretch exercises
1. Add a protocol for a clock or ID generator.
2. Add a fake parser that returns deterministic text for tests.
3. Draw a dependency diagram for domain, application, and infrastructure.

## Writing questions
1. What is dependency inversion in your own words?
2. Why are protocols different from concrete classes?
3. Which part of your architecture feels cleaner after this refactor?
4. Where might you be over-abstracting?
