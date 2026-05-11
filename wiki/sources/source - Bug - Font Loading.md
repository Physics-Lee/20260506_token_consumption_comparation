---
type: source
raw_file: "note/bug-font-loading.md"
date_ingested: 2026-05-10
tags: [bug, fonts, github-pages, cdn]
---

# Source: Bug - Font Loading on github.io

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** bug report / fix note

## Summary

This note documents a bug where fonts displayed correctly locally but appeared differently on github.io. The root cause: CSS font-family declarations alone do not load font files—they only tell the browser "use this font if available." The local development machine had Noto fonts installed (possibly from other projects), so they rendered correctly. github.io visitors (99% without Noto fonts installed) fell back to system defaults (Microsoft YaHei on Windows, PingFang on macOS).

The fix adds Google Fonts CDN links in the HTML <head>: two preconnect links (to fonts.googleapis.com and fonts.gstatic.com) and the actual CSS link with display=swap. Key improvements: preconnect saves 100-300ms of TCP/TLS handshake time; crossorigin is required for fonts.gstatic.com due to CORS; display=swap prevents FOIT by showing fallback fonts immediately and seamlessly switching when Noto loads. The fix was applied to code/json2html.py's HTML template and corpus_reader.html was regenerated.

## Key claims

- CSS font-family declarations do NOT load font files—fonts must be explicitly loaded via @font-face or CDN
- Local development can mask font loading issues if fonts are already installed on the developer's machine
- Google Fonts CDN with preconnect and display=swap is the adopted solution
- crossorigin="anonymous" is required for fonts.gstatic.com due to CORS requirements

## Entities mentioned

- [[Google Fonts]] — CDN providing Noto Sans SC and Noto Serif SC
- [[GitHub Pages]] — deployment platform where the bug manifested

## Concepts touched

- [[Font Loading]] — the mechanics of how browsers acquire and apply fonts
- [[FOIT]] — Flash of Invisible Text
- [[CORS]] — Cross-Origin Resource Sharing, relevant for font loading
- [[CDN]] — using Content Delivery Networks for asset loading

## Notes

This is a classic "works on my machine" bug. The lesson ("declaring font-family ≠ loading font files") is broadly applicable to web development. The fix template should be applied consistently across all HTML-generating scripts.