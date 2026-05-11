---
type: source
raw_file: "note/openai-api-timeline.md"
date_ingested: 2026-05-10
tags: [openai, api, timeline, history]
---

# Source: OpenAI API Timeline

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** historical reference

## Summary

This note documents OpenAI's API and model release timeline from 2020 to 2024. 2020.06: GPT-3 API launched with davinci/curie/babbage/ada, text completion format, r50k_base encoding. 2022.01: Instruct models (text-davinci-002/003) launched, p50k_base encoding. 2022.11: ChatGPT web interface launched with gpt-3.5-turbo + RLHF, cl100k_base encoding, messages format—but no API yet. 2023.03: gpt-3.5-turbo API launched (4 months after ChatGPT web), and GPT-4 released same day (web + API, but API waitlisted). 2023.07: GPT-4 API opened to all paid developers. 2024.05: GPT-4o launched with o200k_base, multimodal.

The encoding-to-era mapping is: r50k_base = 2020 GPT-3 text completion, p50k_base = 2021 instruct models, cl100k_base = 2022 ChatGPT + GPT-4, o200k_base = 2024 GPT-4o + GPT-5.x. The note explains why ChatGPT launched without an API: RLHF safety testing was insufficient, the messages format was a new protocol requiring backward compatibility design, and capacity was constrained by ChatGPT's rapid user growth (1M users in first week).

## Key claims

- OpenAI API history: 2020 GPT-3 → 2022 instruct → 2022 ChatGPT (web only) → 2023 ChatGPT API + GPT-4 → 2024 GPT-4o
- ChatGPT web launched 4 months before its API due to safety testing, protocol design, and capacity constraints
- GPT-4 web and API launched simultaneously in March 2023, but API was waitlisted until July 2023
- Each API era corresponds to a specific encoding: r50k, p50k, cl100k, o200k
- Before ChatGPT API, developers used text-davinci-003 (instruct model, not chat model)

## Entities mentioned

- [[OpenAI]] — all models and APIs
- [[ChatGPT]] — launched Nov 2022 web, API March 2023
- [[GPT-4]] — launched March 2023
- [[GPT-4o]] — launched May 2024

## Concepts touched

- [[API Timeline]] — chronological release of models and APIs
- [[RLHF]] — reason for ChatGPT API delay
- [[Text Completion vs Chat Format]] — evolution of API input formats
- [[Waitlist]] — GPT-4 API's initial restricted access

## Notes

This timeline is crucial for understanding why the project's tokenizer selector includes deprecated models—users need to compare token efficiency across historical encodings, not just current ones. The 4-month gap between ChatGPT web and API is a notable historical detail that explains the continued relevance of text-davinci-003 during that period.