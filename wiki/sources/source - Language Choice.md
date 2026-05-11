---
type: source
raw_file: "note/language-choice.md"
date_ingested: 2026-05-10
tags: [architecture-decision, python, javascript]
---

# Source: Language Choice - Python vs JavaScript

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** architecture decision note

## Summary

This note records the decision to keep the code/ directory pure Python, with browser JS only in HTML <script> tags. The core work is token analysis (analyze_tokens.py, test_tokenizer.py), which requires Python because tiktoken (OpenAI tokenizer) and transformers (HuggingFace tokenizer) only have Python bindings. HTML generation (json2html.py) is an auxiliary build step not worth introducing Node.js for.

The note clarifies that even if the project adopts a "browser-side dynamic rendering" approach (HTML shell that fetches data/*.json at runtime), that JS would still be browser JS in <script> tags—not Node.js in the code/ directory. The conclusion: don't create unnecessary language mixing. code/ = Python, HTML <script> = JS, each serving its purpose.

## Key claims

- code/ directory should remain pure Python
- tiktoken and transformers only have Python bindings, making Python essential for token analysis
- HTML generation is an auxiliary build step not worth introducing Node.js
- Browser JS in <script> tags and Node.js build scripts are two different layers

## Entities mentioned

- [[OpenAI]] — tiktoken library
- [[HuggingFace]] — transformers library

## Concepts touched

- [[Language Choice]] — selecting appropriate programming languages for different tasks
- [[Build Scripts]] — scripts that generate project artifacts

## Notes

This decision remains valid after the pipeline consolidation. The precompute_tokens.py script (and its planned JS counterpart precompute_tokens.js) would be an exception if the JS path is ever implemented, but that script would be for the browser environment, not the code/ directory.