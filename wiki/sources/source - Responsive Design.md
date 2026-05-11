---
type: source
raw_file: "note/responsive-design.md"
date_ingested: 2026-05-10
tags: [css, responsive-design, mobile]
---

# Source: Responsive Design

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** implementation note

## Summary

This note documents the responsive design implementation using CSS media queries. The core mechanism is the browser's viewport width, detected via @media (max-width: Npx) rules. The project uses three breakpoints: max-width: 1200px (narrow desktop / landscape tablet, switches 2x2 card grid to single column), max-width: 768px (tablet / large phone, reduces padding/font size and reorganizes navigation), and max-width: 480px (small phone, further compresses, theme button becomes inline).

The viewport meta tag (<meta name="viewport" content="width=device-width, initial-scale=1.0">) is essential: without it, mobile browsers treat the page as 980px wide desktop, and media queries never trigger. The note emphasizes that CSS media queries are preferred over JavaScript window.innerWidth detection because they work without JS, have better performance (native browser optimization), respond in real-time to window resizing and device rotation without event listeners, and require less code.

## Key claims

- CSS media queries detect viewport width (CSS pixels, not physical pixels) for responsive layout
- Three breakpoints are used: 1200px, 768px (iPad portrait), and 480px (small phones)
- The viewport meta tag is mandatory for mobile media queries to work
- CSS media queries are superior to JavaScript width detection for responsiveness

## Entities mentioned

- (none)

## Concepts touched

- [[CSS Media Queries]] — responsive design based on viewport characteristics
- [[Viewport Meta Tag]] — telling mobile browsers the actual device width
- [[CSS Pixels]] — logical pixel units used by media queries (not physical screen pixels)
- [[Mobile-First vs Desktop-First]] — this project uses desktop-first with max-width breakpoints

## Notes

The note includes debugging guidance (Chrome DevTools device toolbar, Safari responsive design mode) and common pitfalls (forgetting viewport meta, confusing physical vs CSS pixels, wrong ordering of max-width rules). The breakpoint values are grounded in real device widths (768px = iPad portrait, 480px = iPhone SE).