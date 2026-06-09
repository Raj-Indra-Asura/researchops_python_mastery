<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 17 — RAG Assistant:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It - Week 17 RAG Assistant

## Why break it?

Understanding failure modes is as important as making things work. Each experiment below produces a specific, real failure that you will encounter in production. Go through all of them.

---

## Experiment 1: Answer with no context (grounding failure)

Build a prompt with an empty context block and pass it to the fake generator. Observe that the fake returns an answer anyway (it ignores the prompt). Now run the same test with an Ollama or real generator if available. The real generator will likely produce a confident answer based on its training data, not your documents. This is hallucination in its simplest form.

**What to look for**: The answer claims to be grounded but has no citations. The `citations` field in `RagAnswer` is empty. The answer invents content.

**What to fix**: Add the minimum-score filter so that weak or zero retrieval triggers the insufficient-evidence path, not a generation call.

---

## Experiment 2: Irrelevant retrieved chunks

Retrieve chunks from a paper about "Byzantine fault tolerance" and ask a question about "attention mechanisms". The retrieval scores will be very low (near 0.0 or negative). Without a minimum-score filter, these irrelevant chunks get passed to the generator anyway.

**What to look for**: The answer either confabulates (invents a connection between the two topics) or produces nonsense. Citations point to chunks that have nothing to do with the question.

**What to fix**: Verify the minimum-score threshold is applied. Write a test: if all retrieved scores are below `0.3`, the answer must be insufficient evidence.

---

## Experiment 3: Prompt with no instruction text

Remove the instruction line ("Answer only from the provided context.") from the prompt template. Test with a real generator if available. Without the instruction, the model will often blend the context with its training memory, producing answers that go beyond the evidence.

**What to look for**: The answer mentions things not in the retrieved chunks. Citations still appear but the claims they supposedly support are not in the cited text.

**What to document**: Add a comment to `PromptBuilder` explaining why the instruction text must be present and what happens without it.

---

## Experiment 4: Citations shuffled to wrong chunks

Deliberately mismatch citations: when building the `RagAnswer`, assign each citation to the wrong chunk. For example, chunk-1's source gets cited as chunk-2 and vice versa.

**What to look for**: Users cannot verify the answer by following the citation. The cited chunk says something different from what the answer claims. This is a citation integrity failure.

**What to fix**: Write a test that verifies citation index N points to the Nth retrieved chunk, not to any other chunk.

---

## Experiment 5: Prompt too long (context window exceeded)

Create a list of 50 large chunks and build a prompt. For most local models the total prompt will exceed the context window. Observe the behaviour: some models silently truncate (answer only using the first N tokens), some raise an error, some produce garbled output.

**What to look for**: Answers that refer only to early chunks, or error messages from the generator client.

**What to fix**: Add a `max_chunks` limit to the `PromptBuilder` or `RagAssistant`. Decide how many chunks fit comfortably in your target model's context window and enforce that limit. Test that when you pass more chunks than the limit, the builder uses only the top-N.

---

## Experiment 6: Fake generator in an integration test fails

Remove `FakeTextGenerator` from an integration test and replace it with `None`. Observe the `AttributeError` or `TypeError` when the code tries to call `generator.generate(prompt)`.

**What to learn**: The type system helps here. If you annotate `generator: TextGenerator`, mypy will catch the `None` assignment. If you do not annotate, this bug appears only at runtime.

**What to fix**: Add the type annotation. Run mypy (if configured) to see it catch the error statically.

---

## Experiment 7: Missing environment variable

In your `OpenAIGenerator` (if you built it), do not set `OPENAI_API_KEY`. Observe what happens: the `OpenAI` client is initialised with `api_key=None` and raises an `AuthenticationError` on the first call.

**What to fix**: Add an early check at generator initialisation time:

```python
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY is not set. Cannot use OpenAI generator.")
```

Write a test that patches the environment variable to empty and asserts this error is raised before any API call is made.

---

## Experiment 8: `sufficient_evidence=False` path ignored by caller

In a test, make the retriever return no results. Confirm that `RagAnswer.sufficient_evidence` is `False`. Now imagine a UI caller that only reads `answer.answer` without checking `sufficient_evidence`. The user sees a message that says "insufficient evidence" but does not know it is a fallback, not a real answer.

**What to document**: Add a docstring to `RagAssistant.answer` explaining that callers must check `sufficient_evidence` before displaying the answer as definitive.

---

## Debugging tasks

- Print the complete prompt for one question before passing it to the generator. Read it as if you were the model. Does it make sense? Is the question clearly visible? Are the chunks numbered?
- After a test run, print `answer.citations` for one answer. Check that each citation string contains a source ID that matches a real document in your index.
- Run `pytest tests/unit/test_rag_prompting.py -v` and introduce a deliberate bug (swap the chunk numbering starting at 2 instead of 1). Read the test failure message. Is it clear enough to diagnose the bug without reading the source?

---

## Edge cases to handle explicitly

| Case | Expected behaviour |
|---|---|
| Empty question string | Raise `ValueError` or return insufficient evidence |
| No indexed documents at all | Return insufficient evidence immediately |
| Duplicate chunks in retrieval results | Deduplicate before building context; cite each source only once |
| Very long single chunk (thousands of words) | Truncate at a safe character limit before inserting into prompt |
| Generator returns empty string | Handle gracefully; do not return a `RagAnswer` with `answer=""` without warning |
| Generator raises exception | Catch, log, and raise a domain error with context, not a raw HTTP error |

---

## What did you learn?

Answer these questions in your `reflection.md` after completing the experiments:

1. Which failure was hardest to detect without a test?
2. At which step in the pipeline did most failures occur: retrieval, prompting, generation, or citations?
3. What is the most dangerous failure mode: irrelevant chunks, missing instruction, or citation mismatch? Why?
4. What is the minimum test coverage you need to feel confident this pipeline works correctly?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 17 — RAG Assistant:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
