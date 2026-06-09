# Break It - Week 03 OOP and Domain Modeling

## Intentional failure experiments
1. Construct a `Paper` with an empty title and confirm the model rejects it.
2. Put both successful and failed parse data in one object and notice how many `None` checks appear.
3. Remove `default_factory=list` from a list field and observe the mutable default bug.
4. Rename one field in the model but not in the tests and read the resulting failure carefully.
5. Store a raw string path in some places and a `Path` in others; compare the confusion this causes.

## Debugging tasks
- Inspect the generated `__repr__` to see whether model instances are readable.
- Add assertions about equality to reveal missing or extra fields.
- Step through `__post_init__` rules with a debugger or print statements.

## Edge cases to explore
- Blank titles with surrounding whitespace.
- Documents with empty extracted text.
- Duplicate papers pointing to the same file path.
- Very large keyword lists.

## What did you learn?
- Which model boundary reduced complexity the most?
- What did mutable defaults teach you?
- Which fields need validation immediately versus later?
