---
type: concept
source_count: 3
last_updated: 2026-05-10
tags: [css, theme, dark-mode, frontend, implementation]
---

# CSS Custom Properties

CSS variables that enable dynamic theming by allowing values to be defined once and referenced throughout a stylesheet.

## Overview

The project uses CSS custom properties (variables) to implement its three-state theme system (light / dark / follow system). Two sets of color variables are defined: default :root for light theme, and [data-theme="dark"] for dark theme override. All UI elements reference these variables rather than hardcoded colors, so switching themes only requires changing a single attribute on the root element.

This approach was chosen over CSS @media (prefers-color-scheme) because the latter would force the page to always follow the system preference, preventing manual override. The project's solution uses CSS only for the two explicit states (:root = light, [data-theme="dark"] = dark) and JavaScript to handle the "follow system" mode by dynamically setting or removing the data-theme attribute.

## Key perspectives

- **Variables over hardcoding**: Changing one variable updates all elements that reference it
- **JS-controlled system mode**: matchMedia API detects system preference and applies it dynamically
- **No @media needed**: The three-state requirement (light/dark/system) cannot be satisfied with pure CSS media queries

## Evidence and data

Light theme variables:
- --bg-body: #f8f9fa
- --bg-card: #ffffff
- --text-primary: #374151
- --accent: #2563eb

Dark theme variables:
- --bg-body: #0d1117
- --bg-card: #161b22
- --text-primary: #c9d1d9
- --accent: #58a6ff

## Sources

- [[source - Theme System Preference]] — full implementation details
- [[source - Pipeline Diagnosis and Fix]] — template upgrade to CSS variables

## Related

- [[prefers-color-scheme]] — CSS media feature for detecting system theme
- [[Three-State Theme]] — light / dark / follow system toggle
- [[matchMedia API]] — JavaScript API for responding to media query changes
