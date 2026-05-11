---
type: source
raw_file: "note/pipeline-diagnosis.md"
date_ingested: 2026-05-10
tags: [pipeline-fix, json2html, build-process]
---

# Source: Pipeline Diagnosis and Fix

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** troubleshooting note

## Summary

This note diagnoses three breakage points in the original build pipeline and proposes a fix. Breakpoint 1: all .txt translation source files were deleted, rendering generate_json.py unable to run. Breakpoint 2: json2html.py had a path error (line 11 checked Path(filename).exists() in the current directory, but data files are in the data/ subdirectory) and outdated styling (missing CSS variables, dark theme data-theme attribute, three-state theme toggle JS, and theme-toggle button). Breakpoint 3: corpus_reader.html was a hardcoded artifact—adding new articles required manually editing 1000+ lines of HTML, and style updates also required hand-editing.

The proposed fix is to rewrite json2html.py to generate the new HTML directly from data/*.json. Changes include: reading from data/*.json instead of current directory, upgrading the template with CSS custom properties (root light + data-theme="dark" dark), language color adaptations, three-state theme toggle button and JS logic. The output remains pure static HTML with zero runtime dependencies. Since .txt files are lost, generate_json.py is no longer used; existing HTML content can be reverse-extracted to supplement JSON if needed.

## Key claims

- The original pipeline had three breakpoints: missing .txt sources, wrong JSON path in json2html.py, and hardcoded HTML output
- json2html.py needs to read from data/ subdirectory, not current directory
- The HTML template needs CSS custom properties and three-state theme switching
- With .txt sources gone, the pipeline must work purely from data/*.json

## Entities mentioned

- (none)

## Concepts touched

- [[Build Pipeline]] — the sequence of scripts generating project outputs
- [[Static HTML Generation]] — generating complete HTML files without runtime dependencies
- [[CSS Custom Properties]] — CSS variables for theming

## Notes

This fix was implemented before the decision to consolidate to a single pipeline. The diagnosis of hardcoded HTML and template drift between generators remains relevant even after consolidation.