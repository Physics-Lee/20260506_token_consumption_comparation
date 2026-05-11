---
type: source
raw_file: "note/update-workflow.md"
date_ingested: 2026-05-10
tags: [workflow, build-process, github-pages]
---

# Source: Project Update Workflow

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** workflow documentation

## Summary

This note documents the complete project update workflow, from adding new articles to deploying to GitHub Pages. The project follows a data-driven generation model: resource/*.md (source markdowns) → data/*.json (structured data) → optionally precompute_tokens.py → corpus_reader.html and index.html via json2html.py and build_index.py → git push → github.io deployment.

The golden rule is that corpus_reader.html and index.html should never be manually edited—all changes must go through data or Python scripts, then be regenerated. The note covers five scenarios: adding a new article (prepare markdown, generate JSON skeleton via md2json.py or create manually, translate, regenerate HTML, optionally precompute tokens, commit and push); modifying existing articles (edit JSON, regenerate HTML, optionally recompute tokens); updating page styles or functionality (modify script templates, regenerate both HTML files); updating token precomputation data (modify model list in precompute_tokens.py, run, regenerate index.html); and updating README/docs (direct edit, no regeneration needed).

The file change matrix maps each modification type to required build steps and generated files. Common errors documented include: unescaped quotes in JSON (always use json.dump()), forgetting to run precompute_tokens.py (shows "needs precomputation" in index.html), forgetting to sync changes across both HTML generators (template code is ~80% duplicated between json2html.py and build_index.py), and GitHub Pages not updating after push.

## Key claims

- corpus_reader.html and index.html must never be manually edited; always regenerate from scripts
- Two Python generators (json2html.py and build_index.py) share ~80% template code, creating maintenance duplication
- Adding a new article requires: prepare markdown → generate JSON → translate → generate HTML → optionally precompute tokens → commit
- JSON files must be generated with json.dump(), never hand-written, to avoid quote escaping issues

## Entities mentioned

- [[GitHub Pages]] — deployment platform for the project
- [[HuggingFace]] — source for tokenizer models requiring authentication for some models

## Concepts touched

- [[Data-Driven Generation]] — generating HTML from structured JSON data
- [[Static Site Deployment]] — deploying via GitHub Pages
- [[Token Precomputation]] — running precompute_tokens.py to generate token_counts.json

## Notes

This workflow predates the decision to drop json2html.py and corpus_reader.html in favor of a single pipeline (build_index.py → index.html). See [[source - Why Single Pipeline]]. The duplication between json2html.py and build_index.py was a key motivation for consolidation.