---
type: source
raw_file: "note/how-character-counting-works.md"
date_ingested: 2026-05-10
tags: [implementation, character-counting, python]
---

# Source: How Character Counting Works

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** implementation note

## Summary

This note explains the character counting implementation in json2html.py (line 48). The count is simply Python's len() on the content string, which returns the number of Unicode code points. This means each Chinese character counts as 1, each English letter as 1, each emoji as 1, and each newline/space as 1. The note provides a comparison table showing examples: "hello" = 5, "你好" = 2, "こんにちは" = 5, "🙂" = 1.

The choice of character count over byte count is deliberate: the project's purpose is token consumption analysis, and character count is an intuitive text length metric. Using bytes would distort cross-language comparison because English is 1 byte/character while Chinese is 3 bytes/character in UTF-8. The count is displayed with comma thousand-separators using Python's :, format specifier (e.g., 1742 → "1,742").

## Key claims

- Character count uses Python len() which counts Unicode code points
- Character count is preferred over byte count for cross-language comparison
- One Chinese character = one English letter = one emoji = 1 unit
- Display uses comma thousand-separators for readability

## Entities mentioned

- (none)

## Concepts touched

- [[Unicode Code Points]] — the unit counted by Python len()
- [[Character Counting]] — measuring text length by visible characters
- [[Cross-Language Comparison]] — ensuring fair metrics across different writing systems

## Notes

This is a foundational implementation detail that affects how users interpret the comparison table. The choice of code points over grapheme clusters means complex emojis (like family emojis with ZWJ sequences) may count as multiple "characters" even though they render as one visual glyph. For this project's scope, this edge case is negligible.