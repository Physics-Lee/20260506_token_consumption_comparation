---
type: source
raw_file: "note/how-to-change-card-order.md"
date_ingested: 2026-05-10
tags: [implementation, json2html, ui]
---

# Source: How to Change Card Display Order

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** implementation note

## Summary

This note documents a UI change in json2html.py: switching language card display from "original first, then by language order" to a fixed order of Classical Chinese → Modern Chinese → English → Spanish. The original code (lines 39-41) sorted by a tuple of (role_priority, lang_order) where role_priority put the original language first. The new code sorts purely by lang_order, eliminating the role-based priority.

The change affects both the comparison table row order and the 2x2 text card grid arrangement. Using "Jing Ke Assassinates the King of Qin" (originally Classical Chinese) as an example, both old and new orders appear identical because the original happens to be Classical Chinese. But for "Allende's Last Speech" (originally Spanish), the old order would show Spanish first, while the new order always shows Classical Chinese first regardless of original language.

## Key claims

- Language cards now display in fixed order: Classical Chinese, Modern Chinese, English, Spanish
- This change affects both the comparison table and the 2x2 card grid
- The original "original first" logic was replaced with pure language-order sorting
- Regeneration requires running: python code/json2html.py

## Entities mentioned

- (none)

## Concepts touched

- [[UI Ordering]] — controlling display order of language variants
- [[Sorting Logic]] — Python sorted() with custom key functions

## Notes

This change was made before the consolidation to a single pipeline. The same ordering logic would apply to build_index.py.