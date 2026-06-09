# Week 20 Break-It: Final Testing

## Experiment 1: The Nuclear Test
Delete your `.venv` and `data/` directory. Start from scratch: `git clone` → `pip install -e ".[all]"` → run all commands. Does everything work?

## Experiment 2: The CI Simulation
Run exactly what CI runs:
```bash
pip install -e ".[dev]"
ruff check src tests
pytest --cov=researchops
```
Are there any surprises?

## Experiment 3: The Edge Case Tour
Run through every CLI command with bad input:
- `researchops scan /nonexistent`
- `researchops search ""`  (empty query)
- `researchops papers show totally-fake-id`
- `researchops ingest /dev/null`

Does every failure produce a useful error message?

## Experiment 4: The Scope Inventory
List every feature that is NOT in v1.0.0 but that you wanted to add. Consciously decide: is this v1.1 or never?

## What Did You Learn?
- What broke in the nuclear test?
- What edge cases produced unhelpful errors?
- How long did the full pre-release checklist take?
