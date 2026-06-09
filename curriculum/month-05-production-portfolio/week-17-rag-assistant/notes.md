# Notes - Week 17 RAG Assistant

A retrieval-augmented generation (RAG) system combines two ideas: retrieve relevant context, then generate an answer using that context. The retrieval step reduces the chance that the model answers from vague memory alone. The generation step turns evidence into a useful response.

A simple RAG flow is:
1. receive user question
2. run keyword or semantic retrieval
3. select top relevant chunks
4. build a prompt with instructions and context
5. call a language model
6. return an answer plus citations

Prompt structure matters. A good prompt clearly separates the system instruction, retrieved evidence, and user question.

```text
You are a research assistant. Answer only from the provided context.
If the answer is unsupported, say you do not have enough evidence.

Context:
[1] ...chunk text...
[2] ...chunk text...

Question:
What are common failure modes in semantic search?
```

This style gives the model both a behavior rule and evidence. It also creates a natural place for citations like `[1]` or `[2]`.

Grounding means the answer should be supported by retrieved context. A grounded assistant should refuse to invent details not present in the evidence. That is why empty or weak retrieval results need explicit handling. Sometimes the best answer is: "I do not have enough evidence in the indexed documents."

Citations are not decoration. They help users verify claims and let you debug retrieval quality. If an answer is weak but citations point to irrelevant chunks, the retrieval step may be the problem. If citations are good but the answer still drifts, the prompt or generation step may need work.

Your answer object should separate final text from evidence metadata.

```python
@dataclass
class RagAnswer:
    answer: str
    citations: list[str]
    used_chunk_ids: list[str]
```

Evaluation this week is partly qualitative. Ask: Did the answer use the right chunks? Were citations clear? Did the system decline unsupported questions? These are product questions as much as technical ones.

Prompting should stay explicit and testable. Even if you later change models, a prompt builder can still be unit-tested for structure, ordering, citation labels, and fallback behavior. Integration tests can use a fake model to confirm that retrieved chunks flow into the generation step.

A practical warning: RAG does not magically fix bad retrieval. If your chunking or semantic search is poor, the assistant will still be weak. RAG quality depends on the whole pipeline.

This week marks a high-level synthesis of the curriculum so far. Storage, search, embeddings, and APIs all become useful inputs to a final user-facing assistant. The core engineering lesson is not just "call an LLM." It is to build a system that can justify its answers.
