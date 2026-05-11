---
type: source
raw_file: "note/why-single-pipeline.md"
date_ingested: 2026-05-10
tags: [architecture-decision, pipeline-consolidation]
---

# Source: Why Single Pipeline

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** architecture decision note

## Summary

This note records the decision to delete json2html.py and corpus_reader.html, consolidating the project into a single pipeline: build_index.py → index.html. Four reasons support this decision. First, build_index.py is a strict superset of json2html.py—all features in the latter (theme switching, four-language parallel reading, character counting) exist in the former, plus additional features (tokenizer switching, real-time token calculation, precomputed open-source token counts, footer links). Second, users who don't care about tokens can simply ignore the tokenizer dropdown; the page works identically as a corpus reader. Third, maintaining two HTML templates inevitably causes drift—identical CSS variables, class names, and theme-switching JS duplicated across files lead to inconsistencies when one is updated and the other forgotten. Fourth, a single pipeline reduces cognitive overhead for new contributors, eliminating the need to understand the distinction between two HTML outputs and their generation scripts.

## Key claims

- build_index.py is a strict superset of json2html.py with no feature loss
- Users uninterested in token comparison can ignore the tokenizer dropdown
- Two parallel HTML templates will inevitably drift and become inconsistent
- A single pipeline reduces cognitive overhead and maintenance burden

## Entities mentioned

- (none)

## Concepts touched

- [[Pipeline Consolidation]] — merging multiple build pipelines into one
- [[Template Drift]] — divergence between parallel template files over time
- [[Cognitive Overhead]] — mental burden of understanding multiple systems

## Notes

This decision simplifies the project significantly but also means the "corpus_reader" name becomes somewhat misleading—the single index.html serves both audiences (readers and researchers). The workflow note should be updated to reflect this change.