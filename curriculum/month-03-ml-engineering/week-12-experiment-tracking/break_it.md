# Break It - Week 12 Experiment Tracking

## Intentional failure experiments
1. Train a model without recording the artifact path and see how quickly the run becomes less useful.
2. Overwrite the same artifact filename for multiple runs and lose history on purpose.
3. Save a non-JSON-serializable value in params and inspect the failure.
4. Delete one experiment file and decide how list or compare commands should react.
5. Use the wrong metric name in one run and observe comparison confusion.

## Debugging tasks
- Print the full run record after training.
- Verify that the artifact path stored in the record exists on disk.
- Run `pytest -k experiment_tracker -v` after tracker changes.

## Edge cases to explore
- Multiple runs in quick succession.
- Training failure after artifact write but before record write.
- Empty metrics dictionary.
- Very long parameter dictionaries.

## What did you learn?
- What minimum metadata makes a run valuable?
- How can versioning mistakes erase evidence?
- What comparison would you automate next?
