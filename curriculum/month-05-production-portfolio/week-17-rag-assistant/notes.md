# Notes - Week 17 RAG Assistant

## What RAG means

RAG stands for Retrieval-Augmented Generation. It is a system architecture that answers questions by first retrieving relevant text from a document collection, then passing that text to a language model to produce an answer.

The two words describe two distinct operations:

- **Retrieval**: searching your own stored documents to find passages relevant to the question.
- **Generation**: using a language model to turn those passages into a readable answer.

Neither step alone is sufficient. Retrieval without generation gives you raw text chunks, not an answer. Generation without retrieval gives you a language model answering from its training data, with no reference to your specific documents.

Combined, they give you a system that answers from your documents specifically.

---

## Why retrieval comes before generation

A language model knows only what it learned during training. It cannot know about:
- papers you ingested last week
- internal reports you uploaded
- any document that post-dates the model's training cutoff

If you ask a language model "what does the Smith 2023 paper say about attention?" it will either confess ignorance or, worse, invent a plausible-sounding but fabricated answer. That fabrication is called **hallucination**.

Retrieval solves this by fetching the actual relevant passages from your document collection before asking the model to generate. You are giving the model the evidence it needs. The model's job is now to summarise and explain what the evidence says, not to invent.

The order matters: retrieve first, then generate. You cannot retrieve after generating, because the generation step needs the context to be present in the prompt.

---

## Why semantic search from Week 13 matters here

In Week 13 you built a semantic search system: it embedded documents as vectors, computed cosine similarity, and returned the most relevant chunks for a query.

That system is now the retrieval step in your RAG pipeline.

When a user asks "what are the failure modes of contrastive learning?", your Week 13 semantic search finds the chunks most semantically related to that question, even if the chunks do not contain the exact words "failure modes" or "contrastive learning" verbatim.

This matters because natural language is inconsistent. A paper might call the same concept "negative sample collapse", "representation collapse", or "mode collapse". Semantic search finds all of them. Keyword search would miss two of them.

Good retrieval is the foundation of good RAG. If your search returns irrelevant chunks, the answer will be wrong or confusing no matter how capable the language model is. The model can only work with what you give it.

---

## What context is

In a RAG system, **context** is the set of retrieved text chunks that you include in the prompt to the language model.

Think of it as the model's "reading material" for this specific question. You are not asking the model to answer from memory. You are giving it a small reading packet and asking it to answer from that packet.

Context is limited. Language models can only read a certain number of words at once. This limit is called the **context window**. Common limits range from a few thousand words to hundreds of thousands of words. You must decide how many chunks to retrieve and whether the total fits in the context window.

When context is empty — when retrieval finds nothing relevant — the model has no reading material. You must handle this case explicitly. The correct response is not "I don't know" from model memory. The correct response is "I do not have enough evidence in the indexed documents to answer this question."

---

## What a prompt template is

A **prompt template** is a pre-written text structure with slots that you fill in at runtime.

Rather than constructing prompts by ad-hoc string concatenation, you define a template once and fill in the variable parts (the context, the question) for each request.

A simple example:

```text
You are a research assistant. Answer only using the provided context.
If the context does not support the answer, say: "Insufficient evidence."

Context:
{context_block}

Question:
{question}

Answer:
```

At runtime you replace `{context_block}` with the retrieved chunks (formatted and numbered) and `{question}` with the user's question.

Why templates?

1. **Testability**: you can test that the template produces the correct structure before ever calling a model.
2. **Consistency**: every call uses the same format. The model behaves more predictably.
3. **Maintainability**: if the format needs to change, you change one template, not every call site.

---

## What grounding means

**Grounding** means that every claim in the generated answer is supported by the retrieved context.

An answer is grounded when:
- It only describes things that appear in the context.
- It does not add details from the model's training memory.
- Citations point to the specific chunk that supports each claim.

An answer is ungrounded when:
- It states things that are not in the retrieved chunks.
- It elaborates beyond what the evidence shows.
- It asserts facts that sound plausible but come from model memory, not your documents.

Grounding is not automatic. You must explicitly instruct the model to answer only from context. Without that instruction, language models naturally mix context with training knowledge.

Your prompt template must contain a clear instruction: "Answer only from the provided context." Even with that instruction, some models will occasionally drift. Grounding is a best-effort guarantee, not a perfect one.

---

## What hallucination means

**Hallucination** is when a language model states something false or unsupported with apparent confidence.

The term comes from the idea that the model is "seeing" information that is not actually there. It generates fluent, confident-sounding text that does not correspond to any real fact or retrieved document.

Examples of hallucination:
- Inventing a citation to a paper that does not exist.
- Fabricating a statistic that sounds plausible.
- Confabulating an author's conclusion not present in their paper.

Hallucination is more dangerous than "I don't know" because it is harder to detect. A user who receives a confident wrong answer may act on it.

RAG reduces hallucination by giving the model real evidence. But it does not eliminate it. A model can still drift from the context. The best defences are:
1. An explicit instruction to answer only from context.
2. Citations that let the user verify every claim.
3. An "insufficient evidence" fallback when retrieval returns nothing relevant.
4. Integration tests with a fake generator that verifies the context flows through correctly.

---

## Why citations matter

**Citations** are references from the generated answer back to the specific source chunks that support each claim.

They serve several purposes:

**User trust**: a user can verify that the answer is real and not invented. If the citation points to a real chunk that says what the answer claims, the answer is credible.

**Debugging**: citations help you trace failures. If the answer is wrong but the citation is correct, the model may have misread the evidence. If the citation is wrong (pointing to an unrelated chunk), the retrieval step is the problem.

**Accountability**: in research contexts, every claim should be traceable to a source. Citations make that tracing mechanical.

A citation should include at minimum:
- The chunk identifier (e.g., `chunk-3`)
- The source document identifier (e.g., `paper-42`)
- Optionally: the chunk text or a summary of it

Example answer with citations:

```text
Attention mechanisms allow models to weigh the importance of different input
positions [source: paper-7, chunk-2]. This is more efficient than processing
all positions equally [source: paper-12, chunk-5].
```

---

## Source chunks

A **source chunk** is a piece of text retrieved from the document index that the answer is based on.

When you retrieve top-k chunks from your Week 13 semantic search, each chunk carries:
- The chunk text itself
- A `chunk_id` (e.g., the index position)
- A `source_id` pointing to the original document
- A `score` indicating how relevant it was to the query

You will pass these chunks into the prompt and attach them to the answer as citations. The chunk metadata (source_id, chunk_id) becomes the citation reference.

---

## Insufficient evidence response

Not every question has a good answer in the indexed documents. When retrieval returns no relevant chunks, or when all retrieved chunks are weakly related to the question, the system should respond with an "insufficient evidence" message rather than generating a speculative answer.

This is not a failure. It is a feature. Knowing when not to answer is as important as knowing when to answer.

How to implement this:
- Set a minimum relevance threshold (e.g., cosine similarity above 0.3).
- If no chunk meets the threshold, skip generation and return a standard "insufficient evidence" message.
- If some chunks are below threshold, optionally include a warning that evidence is weak.

Example:

```python
INSUFFICIENT_EVIDENCE_RESPONSE = (
    "I do not have enough evidence in the indexed documents to answer this question. "
    "Please ingest more relevant papers or rephrase the question."
)
```

---

## The generator interface

The generator is the component that takes a prompt string and returns a text response. This is the layer that talks to a language model, whether local or remote.

Define an interface (Protocol) so that different generators are interchangeable:

```python
from typing import Protocol


class TextGenerator(Protocol):
    def generate(self, prompt: str) -> str:
        ...
```

Any class with a `generate(self, prompt: str) -> str` method satisfies this protocol. This means you can write:
- `FakeTextGenerator` for tests (deterministic, no network, no cost)
- `OllamaGenerator` for local Ollama-based generation
- `OpenAIGenerator` for OpenAI-compatible API generation

Your RAG assistant accepts a `TextGenerator` and does not care which implementation is used. This is called **dependency injection** and is a key principle of testable design.

---

## Fake generator for tests

```python
class FakeTextGenerator:
    def generate(self, prompt: str) -> str:
        return "This is a test answer based only on the provided context. [source: chunk-1]"
```

Line by line:

`class FakeTextGenerator:` — defines a class that satisfies the `TextGenerator` protocol because it has a `generate` method with the right signature.

`def generate(self, prompt: str) -> str:` — takes the full prompt string. The fake ignores the prompt content entirely. It does not call any model.

`return "This is a test answer based only on the provided context. [source: chunk-1]"` — returns a fixed string. This string is realistic enough to test that the rest of the pipeline (citation parsing, answer formatting) works correctly without ever making a real model call.

Why is this valuable?

1. **No cost**: no API tokens are consumed.
2. **No latency**: returns instantly.
3. **No network**: works offline, including in CI.
4. **Deterministic**: the same prompt always produces the same output, making tests reproducible.
5. **Isolated**: tests for the pipeline structure can pass or fail based on pipeline logic, not model quality.

The fake is honest about what it does not test: it does not test that a real model gives good answers. Those tests require real models and are expensive to run. Keep them separate and optional.

---

## Local Ollama option

Ollama is a tool that runs language models locally on your machine. It exposes a simple API similar to OpenAI's.

Install Ollama from https://ollama.com, then pull a model:

```bash
ollama pull gemma3
```

Use it in Python:

```python
from ollama import chat                          # line 1

response = chat(                                 # line 2
    model="gemma3",                              # line 3
    messages=[                                   # line 4
        {"role": "user", "content": "Summarize this context: ..."}   # line 5
    ],
)

print(response["message"]["content"])           # line 6
```

Line 1: import `chat` from the `ollama` Python package. This package talks to the Ollama server running locally on your machine.

Line 2–5: call the `chat` function. `model` is the name of the locally installed model. `messages` is a list of message objects, each with a `role` ("user", "assistant", or "system") and `content` (the text).

Line 6: the response is a dictionary. `response["message"]["content"]` is the text the model produced.

**Why Ollama?** It runs entirely on your machine. No data leaves your computer. No API key required. No cost per call. The tradeoff is that you need a reasonably fast machine (preferably with a GPU or Apple Silicon) and disk space for the model weights.

For this project, Ollama is the recommended local option. The fake generator is used for tests, and Ollama is used for manual testing and interactive development.

---

## OpenAI-compatible option

Many language model providers offer an API that follows the OpenAI format. You can use the `openai` Python package to talk to them.

```python
import os                                              # line 1
from openai import OpenAI                              # line 2

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))   # line 3

response = client.responses.create(                    # line 4
    model="gpt-5.5",                                   # line 5
    instructions="Answer using only the provided context.",  # line 6
    input="Context: ...\n\nQuestion: What is efficient attention?",  # line 7
)

print(response.output_text)                            # line 8
```

Line 1: import the standard library `os` module, which provides `os.environ` for reading environment variables.

Line 2: import `OpenAI` from the `openai` package. This is the client class.

Line 3: create a client instance. `os.environ.get("OPENAI_API_KEY")` reads the API key from the environment. If the variable is not set, this returns `None`, and the first API call will fail with a clear authentication error. **Never hard-code the API key in source code.**

Line 4: call `client.responses.create(...)`. This sends an HTTP request to the OpenAI API.

Line 5: `model` specifies which model to use.

Line 6: `instructions` provides the system-level behaviour instruction (answer only from context).

Line 7: `input` is the actual content — the context block and the user question combined into one string.

Line 8: `response.output_text` is the model's answer as a plain string.

**Important**: this code costs real money if you use OpenAI's API. The fake generator and Ollama should be used for development and testing. Reserve API calls for manual validation of real answer quality.

---

## Provider abstraction

The generator interface (`TextGenerator`) hides which provider you are using. This means:

- Tests always use `FakeTextGenerator`.
- Local development can use `OllamaGenerator`.
- Optional production use can use `OpenAIGenerator`.

The RAG assistant class does not know or care which is injected:

```python
class RagAssistant:
    def __init__(
        self,
        retriever: ...,
        generator: TextGenerator,
        prompt_builder: ...,
    ) -> None:
        self._retriever = retriever
        self._generator = generator
        self._prompt_builder = prompt_builder
```

To switch providers, you change which object you pass in at construction time. No other code changes.

---

## Local vs API generation

| Property | Local (Ollama) | API (OpenAI-compatible) |
|---|---|---|
| **Cost** | Free after hardware | Pay per token |
| **Latency** | Seconds on CPU, faster on GPU | ~1–5 seconds |
| **Privacy** | Text stays on your machine | Text sent to provider |
| **Internet** | Not required | Required |
| **Model quality** | Depends on hardware and model choice | Generally higher on large models |
| **Best for** | Development, testing, privacy-sensitive use | Production, high-quality answers |

For this project: use fake generator in all tests. Use Ollama for hands-on exploration. Keep the OpenAI option as an optional integration path.

---

## Secrets and environment variables

An **environment variable** is a named value that your operating system makes available to running programs. It is external to your source code.

```python
import os
api_key = os.environ.get("OPENAI_API_KEY")
```

This reads a variable named `OPENAI_API_KEY` from the environment. The value is not in the source file. Different machines or deployment environments can have different values.

A **secret** is any sensitive value: an API key, a password, a token. Secrets must never appear in source code or committed files.

**Why?** Because:
- Source code is often shared publicly on GitHub.
- Git history is permanent. Even if you delete the key in a later commit, it remains in the history.
- Automated scanners search public repos for secrets and exploit them within minutes.

Store secrets in:
- Your shell's environment (set in `~/.bashrc` or `~/.zshrc`)
- A `.env` file that is listed in `.gitignore`
- A secrets manager (AWS Secrets Manager, GitHub Actions secrets, etc.)

The `.env.example` file shows what variables are needed, with placeholder values:

```bash
OPENAI_API_KEY=your-api-key-here
```

Never put a real key in `.env.example`.

---

## Not committing API keys

The `.gitignore` file lists patterns of files that Git should never track. Always include:

```
.env
*.env
```

Verify before committing:

```bash
git status          # .env should not appear in the list
git diff --staged   # scan the staged diff for any key-like strings
```

If you accidentally commit a key:
1. Immediately revoke the key at the provider's dashboard.
2. Remove it from the code.
3. Use `git filter-repo` or `BFG Repo Cleaner` to remove it from history.
4. Force-push the cleaned history.

Revoking and rotating the key is more important than cleaning history. Do the revocation first.

---

## The full RAG pipeline

Here is the complete data flow, with each step explained:

```text
question
  -> embed question
  -> retrieve chunks
  -> build context
  -> create prompt
  -> call generator
  -> attach citations
  -> return answer or insufficient evidence
```

**Step 1: embed question**
Convert the user's question into a vector using the same embedding model used during indexing. The question must use the same model, otherwise the vector spaces are incompatible.

**Step 2: retrieve chunks**
Run cosine similarity between the question vector and all stored chunk vectors. Return the top-k most similar chunks. These are the pieces of evidence.

**Step 3: build context**
Format the retrieved chunks into a numbered block of text. Each chunk gets a label like `[1]`, `[2]`, etc. This block becomes the "evidence" section of the prompt.

```text
[1] Attention allows each token to attend to all other tokens...
[2] Self-attention computes query, key, and value projections...
```

**Step 4: create prompt**
Fill the prompt template with the context block and the user question.

```text
You are a research assistant. Answer only from the provided context.
If the answer is unsupported, say "Insufficient evidence."

Context:
[1] Attention allows each token to attend to all other tokens...
[2] Self-attention computes query, key, and value projections...

Question:
What is the difference between attention and self-attention?

Answer:
```

**Step 5: call generator**
Pass the complete prompt string to the generator. The generator returns a text string.

**Step 6: attach citations**
Collect the chunk identifiers and source document identifiers from the retrieved chunks. Attach them to the answer object as citations.

**Step 7: return answer or insufficient evidence**
If relevant chunks were found: return an answer object with the generated text and citations.
If no relevant chunks were found: return the "insufficient evidence" message without calling the generator.

---

## Answer data structure

The answer should be a typed data object, not a raw string:

```python
from dataclasses import dataclass, field


@dataclass
class RagAnswer:
    answer: str
    citations: list[str] = field(default_factory=list)
    used_chunk_ids: list[str] = field(default_factory=list)
    sufficient_evidence: bool = True
```

`answer`: the generated text. For insufficient-evidence cases, this is the standard fallback message.

`citations`: human-readable citation strings, e.g., `["paper-7 chunk-2", "paper-12 chunk-5"]`.

`used_chunk_ids`: machine-readable chunk identifiers. Useful for debugging: you can look up the exact chunk that was used.

`sufficient_evidence`: a boolean. `False` means retrieval found nothing useful and the answer is a fallback. Callers can use this flag to display a warning or present results differently.

---

## Prompt builder

Separate the prompt construction logic into its own class:

```python
class PromptBuilder:
    def build(self, question: str, chunks: list[str]) -> str:
        if not chunks:
            return ""
        context_block = "\n".join(
            f"[{i + 1}] {chunk}" for i, chunk in enumerate(chunks)
        )
        return (
            "You are a research assistant. Answer only from the provided context.\n"
            "If the answer is unsupported, say 'Insufficient evidence.'\n\n"
            f"Context:\n{context_block}\n\n"
            f"Question:\n{question}\n\n"
            "Answer:"
        )
```

This class has no external dependencies. You can test it without any model, retriever, or network connection. Test cases should verify:
- The question appears in the output.
- Each chunk appears with its correct `[N]` label.
- An empty chunks list returns an empty string (or a defined fallback behaviour).
- The instruction text is present.

---

## Integration with the RAG assistant

A minimal RAG assistant class:

```python
class RagAssistant:
    def __init__(
        self,
        retriever,       # anything with a search(query: str) -> list[SearchHit]
        generator: TextGenerator,
        prompt_builder: PromptBuilder,
        min_score: float = 0.3,
    ) -> None:
        self._retriever = retriever
        self._generator = generator
        self._prompt_builder = prompt_builder
        self._min_score = min_score

    def answer(self, question: str) -> RagAnswer:
        hits = self._retriever.search(question)
        relevant = [h for h in hits if h.score >= self._min_score]

        if not relevant:
            return RagAnswer(
                answer=INSUFFICIENT_EVIDENCE_RESPONSE,
                sufficient_evidence=False,
            )

        chunks = [h.chunk_text for h in relevant]
        prompt = self._prompt_builder.build(question, chunks)
        text = self._generator.generate(prompt)
        citations = [f"{h.source_id} chunk-{h.chunk_index}" for h in relevant]

        return RagAnswer(
            answer=text,
            citations=citations,
            used_chunk_ids=[str(h.chunk_index) for h in relevant],
            sufficient_evidence=True,
        )
```

This is the integration point. Every component is injected. The class itself has no knowledge of which model, which retriever implementation, or which prompt style is used. All of those are controlled by the caller.

---

## Testing strategy

**Unit tests** (use fakes, run in milliseconds):
- Test `PromptBuilder` produces correctly structured prompts.
- Test `RagAnswer` dataclass field defaults.
- Test `FakeTextGenerator` returns the expected string.
- Test the insufficient-evidence path (when `relevant` is empty).

**Integration tests** (use fake retriever + fake generator, still fast):
- Test the full `answer` pipeline from question to answer object.
- Test that citations contain the expected source IDs.
- Test that a low-score retrieval triggers the insufficient evidence response.

**Do not test with real models in unit or integration tests.** Real models are slow, cost money, and produce non-deterministic output. If you want to validate answer quality, create a separate manual test or smoke test that you run by hand.

---

## Why this pipeline is testable

Every component has a narrow interface:
- The retriever has a `search` method.
- The generator has a `generate` method.
- The prompt builder has a `build` method.

Each can be tested in isolation. Each can be replaced with a fake for testing. The `RagAssistant` class wires them together, and the integration test proves that the wiring is correct using fakes.

This design means you can write comprehensive tests without ever making a network call or loading a model. That makes CI fast and reliable.

---

## File locations for this week

The problem statement specifies these paths. Use exactly these:

```
src/researchops/rag/prompting.py      # PromptBuilder, context formatting
src/researchops/rag/assistant.py      # RagAssistant, RagAnswer, TextGenerator
src/researchops/rag/citations.py      # citation formatting helpers
tests/unit/test_rag_prompting.py      # unit tests for PromptBuilder
tests/integration/test_rag_answering.py  # integration tests for full pipeline
```

---

## Summary

- RAG = retrieval + generation. Retrieve first, then generate.
- Retrieval uses Week 13 semantic search to find relevant chunks.
- Context is the set of retrieved chunks placed into the prompt.
- A prompt template separates instruction, context, and question.
- Grounding means the answer uses only the retrieved context, not model memory.
- Hallucination is when a model states unsupported facts with false confidence.
- Citations link every claim back to a source chunk for verification and debugging.
- Insufficient evidence is the correct response when retrieval finds nothing useful.
- The generator interface makes the pipeline testable with a fake.
- Secrets (API keys) must never be committed. Read them from environment variables.
- Tests use the fake generator. Manual and integration exploration can use Ollama or an API.
- RAG quality depends on retrieval quality. Good chunking and embeddings matter.
