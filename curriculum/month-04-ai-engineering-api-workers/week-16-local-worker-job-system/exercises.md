# Exercises - Week 16 Local Worker and Job System

## Warm-up exercises
1. Model a job with ID, state, and payload.
2. Write a simple state transition from `queued` to `running`.
3. Count attempts and stop retrying after a maximum.
4. Simulate one successful and one failing job handler.

## Project exercises
1. Implement persistent job records in SQLite or another local store.
2. Build a worker loop that claims and executes queued jobs.
3. Add retry logic with a maximum attempt count.
4. Write tests for success, failure, and idempotent re-run behavior.

## Stretch exercises
1. Add scheduled backoff before retrying.
2. Add a command to list or inspect current jobs.
3. Add a cancel state for queued jobs.

## Writing questions
1. Why must job states be explicit?
2. What makes a handler idempotent?
3. Which failure should be retried versus left failed?
4. How would this design change with multiple workers?
