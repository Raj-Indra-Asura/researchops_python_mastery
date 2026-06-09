# Break It - Week 17 RAG Assistant

## Intentional failure experiments
1. Build a prompt without any context and see how your assistant responds.
2. Provide irrelevant retrieved chunks and inspect citation quality.
3. Let the model answer unsupported questions without a fallback rule.
4. Shuffle citations so they no longer match the quoted chunks.
5. Exceed a prompt length budget and decide how to truncate context.

## Debugging tasks
- Print the final prompt for one question.
- Compare retrieved chunks with cited chunks in the answer.
- Run `pytest -k rag_ -v` after prompt or answer changes.

## Edge cases to explore
- No retrieved results.
- Highly similar duplicate chunks.
- Conflicting evidence across sources.
- Very long user questions.

## What did you learn?
- Which failure came from retrieval versus prompting?
- What makes a citation trustworthy?
- When should the assistant say "I don't know"?
