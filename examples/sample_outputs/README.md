# Sample Outputs

This directory contains expected CLI/API output examples for reference.

These are used in Week 1-4 exercises to understand what correct output looks like
before you can generate real output from real PDFs.

## `scan` output example

```
           PDFs in ./examples/sample_papers
┌──┬──────────────────────────────────┬────────┐
│ #│ Filename                         │   Size │
├──┼──────────────────────────────────┼────────┤
│ 1│ attention_is_all_you_need.pdf    │ 1234.5 KB │
│ 2│ bert_paper.pdf                   │  890.2 KB │
└──┴──────────────────────────────────┴────────┘

2 PDF(s) found
```

## `search` output example (Week 7)

```
Search results for "transformer attention"

1. Attention Is All You Need (score: 47)
   …The Transformer model architecture relies entirely on attention mechanisms…

2. BERT: Pre-training of Deep Bidirectional Transformers (score: 23)
   …attention-based encoder from the Transformer architecture…
```
