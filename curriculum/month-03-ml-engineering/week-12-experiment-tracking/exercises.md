# Exercises - Week 12 Experiment Tracking

## Warm-up exercises
1. Generate a unique run ID from a timestamp or UUID.
2. Save a JSON file containing params and metrics.
3. Load a saved run record and print one metric.
4. Compare two dictionaries of metrics side by side.

## Project exercises
1. Implement an `ExperimentRun` model and tracker.
2. Update training code to record params, metrics, and artifact paths.
3. Store run files under `artifacts/experiments/`.
4. Write tests that prove training produces both a model artifact and a run record.

## Stretch exercises
1. Add a command to list recent runs.
2. Add a simple comparison table for two run IDs.
3. Store a dataset hash or label-distribution summary in the record.

## Writing questions
1. Which parameter changes are most important to track?
2. What information makes a run reproducible?
3. How would you compare runs fairly?
4. What experiment-tracking shortcut would be dangerous later?
