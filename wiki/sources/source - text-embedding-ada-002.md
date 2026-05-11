---
type: source
raw_file: "note/text-embedding-ada-002.md"
date_ingested: 2026-05-10
tags: [embedding, ada, openai, vector, rag]
---

# Source: text-embedding-ada-002

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** reference note

## Summary

This note explains text-embedding-ada-002 and its relationship to GPT-3's ada model. They share only the "ada" brand name (indicating lowest cost tier)—model structure, purpose, tokenizer, and release time are completely different. text-embedding-ada-002 is an embedding model (outputs 1536-dimensional float vectors for semantic search, clustering, RAG), released December 2022, using cl100k_base encoding, priced at $0.0001/1K tokens. GPT-3 ada is a text generation model (350M parameters, r50k_base, released June 2020).

The note describes typical embedding use cases: semantic search (vectorize documents and queries, find nearest neighbors), RAG (retrieve relevant documents then generate answers), and clustering/classification (k-means on vectors to discover patterns). In January 2024, text-embedding-3-small and text-embedding-3-large replaced ada-002. The new series dropped the "ada" brand, added adjustable dimensions (256-3072), and improved pricing (3-small is 5x cheaper). The 3-series kept cl100k_base for backward compatibility—changing embedding tokenizer would invalidate all previously vectorized documents.

## Key claims

- text-embedding-ada-002 and GPT-3 ada share only a brand name; they are completely different models
- Embedding models output vectors, not text; used for semantic search, RAG, clustering
- text-embedding-ada-002: 1536-dim, cl100k_base, $0.0001/1K tokens
- text-embedding-3 series (2024) replaced ada-002 with adjustable dimensions and better pricing
- Embedding models keep the same tokenizer across versions to avoid invalidating vector databases

## Entities mentioned

- [[OpenAI]] — text-embedding-ada-002, text-embedding-3 series
- [[GPT-3]] — ada model (unrelated to embedding ada)

## Concepts touched

- [[Embedding Model]] — model that maps text to dense vector representations
- [[Semantic Search]] — finding similar documents via vector similarity
- [[RAG]] — Retrieval-Augmented Generation
- [[Vector Database]] — storage for high-dimensional embedding vectors
- [[Tokenizer Backward Compatibility]] — why embedding models don't change encodings

## Notes

This note is relevant to the project because the tokenizer selector includes text-embedding models. Understanding that embedding models use the same tokenizer as their contemporary generation models (cl100k_base for ada-002, same as GPT-3.5/GPT-4) explains why they appear in the comparison. The backward compatibility constraint on embedding tokenizers is an important design consideration for API providers.