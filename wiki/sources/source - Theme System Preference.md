---
type: source
raw_file: "note/theme-system-preference.md"
date_ingested: 2026-05-10
tags: [css, theme, dark-mode, implementation]
---

# Source: Theme System Preference Implementation

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** implementation note

## Summary

This note documents the three-state theme system (light / dark / follow system) implementation using CSS custom properties, prefers-color-scheme media query, and JavaScript. The CSS architecture defines two sets of color variables: default :root for light theme and [data-theme="dark"] for dark theme override. All elements use these variables rather than hardcoded colors, so switching themes only requires changing the root element's data-theme attribute.

The key design insight: default :root equals light theme; [data-theme="dark"] equals forced dark; absence of data-theme means "follow system" (JS detects prefers-color-scheme and dynamically applies). The JavaScript uses matchMedia('(prefers-color-scheme: dark)') to read system preference. The toggleTheme() function cycles through three modes: light → dark → system → light. When in "system" mode, the page responds to OS theme changes automatically. The note explains why CSS @media (prefers-color-scheme) was not used: it would force-follow the system and prevent manual override. The chosen approach keeps CSS simple (:root + [data-theme="dark"] only) and lets JS handle the "follow system" logic.

## Key claims

- Three-state theming requires JS control, not pure CSS media queries, to allow manual override of system preference
- The data-theme attribute approach cleanly separates: explicit light, explicit dark, and system-follow
- matchMedia().addEventListener('change') enables automatic response to OS theme changes when in "follow system" mode
- No localStorage persistence is currently implemented; page refreshes revert to "follow system"

## Entities mentioned

- (none)

## Concepts touched

- [[CSS Custom Properties]] — CSS variables for dynamic theming
- [[prefers-color-scheme]] — CSS media feature detecting system color preference
- [[Three-State Theme]] — light / dark / follow system toggle
- [[matchMedia API]] — JavaScript API for detecting and responding to CSS media queries

## Notes

The note mentions optional localStorage persistence but the current implementation does not include it. Browser compatibility is excellent (Chrome 76+, Firefox 67+, Safari 12.1+, Edge 79+). IE is not supported but not required for this project.