---
type: source
raw_file: "note/font-choice.md"
date_ingested: 2026-05-10
tags: [design, fonts, typography, cjk]
---

# Source: Font Choice

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** design decision note

## Summary

This note documents the font stack selection for the project. The global UI uses system fonts first (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto) for English/numbers, with Noto Sans SC and Noto Serif SC as Chinese fallbacks. Card body text uses Noto Sans SC + Noto Serif SC + serif. The rationale: system fonts render English and numbers best without extra loading; Noto Sans SC (Source Han Sans) and Noto Serif SC (Source Han Serif) are free, open-source (SIL OFL), globally available via Google Fonts CDN, and cover CJK characters comprehensively including Classical Chinese characters.

The note explains why dedicated ancient text fonts (like Wen Zheng Ming style or FangZheng fonts) were not used: they are mostly commercial with complex licensing, typically lack Western character support for mixed排版, and have large file sizes (5-20MB per font). Noto Serif SC's Song-style (serif) appearance is sufficiently classical while coordinating well with its Western serif counterpart. The note also explains the preconnect strategy for Google Fonts CDN and the display=swap parameter to avoid FOIT (Flash of Invisible Text).

## Key claims

- System fonts are preferred for English/numbers; Noto fonts for Chinese
- Noto Sans SC + Noto Serif SC cover CJK comprehensively and are free/open-source
- Dedicated ancient Chinese fonts were rejected due to licensing, lack of Western support, and large file sizes
- Serif fonts (Song/Ming style) are more readable for long Classical Chinese text
- Google Fonts CDN with preconnect and display=swap optimizes loading

## Entities mentioned

- [[Google Fonts]] — CDN for Noto Sans SC and Noto Serif SC

## Concepts touched

- [[Font Stack]] — ordered list of fallback fonts
- [[CJK Fonts]] — fonts covering Chinese, Japanese, and Korean characters
- [[FOIT]] — Flash of Invisible Text, avoided via font-display: swap
- [[Typography for Classical Chinese]] — readability considerations for ancient text

## Notes

The note references a bug where fonts were declared in CSS but not loaded, causing inconsistency between local dev (where fonts were installed) and github.io deployment. See [[source - Bug - Font Loading]].