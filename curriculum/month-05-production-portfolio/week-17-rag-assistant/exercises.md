# Exercises - Week 17 RAG Assistant

## Warm-up exercises

These exercises build individual concepts before you integrate them. Do them in order.

### 1. Build a context block from chunks

Given two chunk strings, produce the numbered context block that would appear in a RAG prompt:

```python
chunks = [
    "Attention mechanisms allow each token to attend to all others.",
    "Self-attention uses query, key, and value projections.",
]
# Expected output:
# [1] Attention mechanisms allow each token to attend to all others.
# [2] Self-attention uses query, key, and value projections.
```

Write a function `format_context(chunks: list[str]) -> str` that produces this.

### 2. Write the FakeTextGenerator class

Implement `FakeTextGenerator` so it satisfies the `TextGenerator` protocol. The `generate` method must accept a prompt string and return:

```python
"This is a test answer based only on the provided context. [source: chunk-1]"
```

regardless of what the prompt contains. Verify that it has the correct method signature and that calling `generate("any prompt")` returns the expected string.

### 3. Build a prompt from template

Write a `PromptBuilder` class with a `build(question: str, chunks: list[str]) -> str` method. The returned string must contain:
- The instruction text (`"Answer only from the provided context."`)
- A numbered context block
- The question

Test it with one question and two chunks. Print the result and inspect it manually before writing tests.

### 4. Handle empty context

Add a check to `PromptBuilder.build`: if `chunks` is an empty list, return an empty string (or raise `ValueError` — choose one, document it, and test it).

### 5. Build a RagAnswer dataclass

Define a `RagAnswer` dataclass with these fields:
- `answer: str`
- `citations: list[str]` (default empty list)
- `used_chunk_ids: list[str]` (default empty list)
- `sufficient_evidence: bool` (default `True`)

Construct an example with text and two citations. Construct an example with `sufficient_evidence=False`. Print both and confirm the fields are correct.

### 6. Read an API key from the environment

Write a tiny script that reads `OPENAI_API_KEY` from the environment and prints either `"key found"` or `"key not set"` without printing the key value. Use `os.environ.get`. Run it with the variable unset and then with it set to a dummy value.

---

## Project exercises

These are the main deliverables for the week.

### 1. Implement PromptBuilder

In `src/researchops/rag/prompting.py`, implement `PromptBuilder` fully. It must:
- Accept a question string and a list of chunk strings.
- Return a correctly structured prompt with instruction, numbered context, and question.
- Return an empty string (or raise `ValueError`) when `chunks` is empty.

Write unit tests in `tests/unit/test_rag_prompting.py` that verify:
- The question appears in the output.
- Each chunk appears with the correct `[N]` label.
- Changing one chunk changes the output correctly.
- The empty-chunks case is handled as documented.

### 2. Implement the TextGenerator protocol and FakeTextGenerator

In `src/researchops/rag/assistant.py`, define the `TextGenerator` protocol and the `FakeTextGenerator` class. The protocol must have a `generate(self, prompt: str) -> str` method. `FakeTextGenerator` must satisfy it.

### 3. Implement RagAnswer

In `src/researchops/rag/assistant.py`, implement the `RagAnswer` dataclass with the fields described above.

### 4. Implement RagAssistant

In `src/researchops/rag/assistant.py`, implement `RagAssistant.answer(question: str) -> RagAnswer`. The method must:
- Call the retriever to get chunks.
- Filter chunks below a minimum cosine score (default `0.3`).
- If no chunks pass the filter, return a `RagAnswer` with `sufficient_evidence=False`.
- Otherwise, build the prompt, call the generator, and return a `RagAnswer` with citations.

### 5. Implement citation formatting

In `src/researchops/rag/citations.py`, implement a function `format_citations(hits: list[SearchHit]) -> list[str]` that returns a list of citation strings like `["paper-7 chunk-2", "paper-12 chunk-5"]`.

### 6. Write integration tests

In `tests/integration/test_rag_answering.py`, write tests for the full `RagAssistant.answer` pipeline using `FakeTextGenerator` and a fake retriever. Tests must verify:
- An answer object is returned with `sufficient_evidence=True` when chunks are found.
- Citations contain the expected source IDs.
- When the fake retriever returns no results, the answer has `sufficient_evidence=False` and the answer text is the insufficient-evidence message.

---

## Stretch exercises

### 1. Add evidence strength field

Add an `evidence_strength: float` field to `RagAnswer`, calculated as the average cosine score of the used chunks. Add a test that verifies the score is between 0.0 and 1.0.

### 2. Hybrid retrieval

Before building the prompt, combine keyword search results (from Week 13's keyword path) with semantic search results. Deduplicate and re-rank. Test that the combined result is not longer than `top_k`.

### 3. API route for the assistant

Add a `POST /api/ask` route to the FastAPI app. The request body contains a `question` field. The response returns the `RagAnswer` as JSON. Test it with the fake generator.

### 4. Implement an OllamaGenerator

Create an `OllamaGenerator` class that calls a locally running Ollama instance. Gate it with a check: if the Ollama server is not reachable, skip the test with `pytest.skip`. Do not let this test run in CI.

---

## Writing questions

Answer these in your `reflection.md`:

1. In your own words, explain why retrieval must happen before generation. What goes wrong if you skip retrieval?
2. What is the difference between grounding and hallucination? Give an example of each from your own testing.
3. Why does the fake generator make tests more reliable than a real generator?
4. If your RAG system gives a wrong answer, how would you determine whether the problem is in retrieval, prompt construction, or generation?
5. Why should API keys never be committed to source code? What are the consequences if they are?
