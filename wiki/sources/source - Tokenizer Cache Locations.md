---
type: source
raw_file: "note/tokenizer-cache-locations.md"
date_ingested: 2026-05-11
tags: [huggingface, cache, filesystem, windows]
---

# Source: Tokenizer Cache Locations

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** system reference

## Summary

This note documents the local HuggingFace cache directory and its contents on the user's Windows machine. The cache root is `C:\Users\Dell\.cache\huggingface\hub\`. Files are organized as `models--{org}--{repo}\snapshots\{commit_hash}\` with `/` replaced by `--`.

Cached models and tokenizer.json status:
- Qwen/Qwen-7B: 0B (missing main file, has .no_exist marker)
- Qwen/Qwen2.5-72B: ✅ 7.0MB
- Qwen/Qwen3.5-27B: ✅ (downloaded via mirror)
- deepseek-ai/DeepSeek-V2-Lite: ✅ 4.6MB
- deepseek-ai/DeepSeek-V3: ✅ 7.8MB
- microsoft/phi-2: ✅ 2.1MB
- gpt2: ✅ vocab.json 1.0MB

The note explains that `.no_exist` directories mark "file exists but size is 0" (download failure). For downloads inside the firewall region, `HF_ENDPOINT=https://hf-mirror.com` redirects to a mirror while storing files in the same local cache.

## Key claims

- HuggingFace cache on Windows: `C:\Users\Dell\.cache\huggingface\hub\`
- Directory naming: `models--{org}--{repo}\snapshots\{commit_hash}\`
- `.no_exist` directories indicate failed downloads (0-byte files)
- `HF_ENDPOINT` environment variable redirects to hf-mirror.com for firewall regions
- Qwen-7B tokenizer.json is missing (0B), while Qwen2.5-72B and Qwen3.5-27B are cached

## Entities mentioned

- [[HuggingFace]] — cache system and model hub
- [[hf-mirror.com]] — Chinese mirror for HuggingFace downloads

## Concepts touched

- [[HuggingFace Cache]] — local filesystem storage for downloaded models
- [[Mirror Sites]] — regional workarounds for access restrictions

## Notes

This is a system-specific reference for the user's machine. The missing Qwen-7B tokenizer.json (0B) is notable—it may explain issues with that model's precomputation. The cache locations are useful for troubleshooting download issues and verifying which models are available locally.
