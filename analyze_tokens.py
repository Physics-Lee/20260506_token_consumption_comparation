#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Tokenizer Test - Manual Estimation + Actual Test
"""

import os
import sys

# Character counts (from our files)
CHAR_COUNTS = {
    "Classical Chinese": 1742,
    "Modern Chinese": 2127,
    "English": 3149,
    "Spanish": 3829,
}

# Estimated tokens based on tokenizer behavior
# GPT-4/Claude tokenizers:
# - English: ~1.3 chars/token (1 token ≈ 0.75 words)
# - Spanish: ~1.2 chars/token (slightly less efficient than English)
# - Modern Chinese: ~0.6 chars/token (1 Chinese char ≈ 1.5-2 tokens)
# - Classical Chinese: ~0.8-1.0 chars/token (denser than modern Chinese)

ESTIMATES_GPT = {
    "Classical Chinese": {"tokens": 1742, "chars_per_token": 1.0},  # Dense, but tokenizer not optimized
    "Modern Chinese": {"tokens": 3190, "chars_per_token": 0.67},  # Standard Chinese
    "English": {"tokens": 2422, "chars_per_token": 1.30},
    "Spanish": {"tokens": 3191, "chars_per_token": 1.20},
}

ESTIMATES_DEEPSEEK = {
    "Classical Chinese": {"tokens": 1300, "chars_per_token": 1.34},  # Better Chinese compression
    "Modern Chinese": {"tokens": 1770, "chars_per_token": 1.20},
    "English": {"tokens": 2350, "chars_per_token": 1.34},
    "Spanish": {"tokens": 3050, "chars_per_token": 1.25},
}


def print_analysis():
    print("=" * 80)
    print("TOKEN CONSUMPTION ANALYSIS")
    print("=" * 80)
    print("\n📊 CHARACTER COUNTS (Raw text size):")
    print("-" * 60)
    for name, count in CHAR_COUNTS.items():
        print(f"  {name:25s}: {count:5d} characters")
    
    print("\n" + "=" * 80)
    print("🤖 GPT-4/OPENAI TOKENIZER ESTIMATES (cl100k_base / o200k_base)")
    print("=" * 80)
    print("-" * 80)
    print(f"  {'Text':<25s} | {'Chars':>8s} | {'Tokens':>8s} | {'Chars/Token':>12s}")
    print("-" * 80)
    for name in CHAR_COUNTS:
        chars = CHAR_COUNTS[name]
        tokens = ESTIMATES_GPT[name]["tokens"]
        cpt = ESTIMATES_GPT[name]["chars_per_token"]
        print(f"  {name:<25s} | {chars:>8d} | {tokens:>8d} | {cpt:>12.2f}")
    print("-" * 80)
    
    print("\n" + "=" * 80)
    print("🧠 DEEPSEEK TOKENIZER ESTIMATES")
    print("=" * 80)
    print("-" * 80)
    print(f"  {'Text':<25s} | {'Chars':>8s} | {'Tokens':>8s} | {'Chars/Token':>12s}")
    print("-" * 80)
    for name in CHAR_COUNTS:
        chars = CHAR_COUNTS[name]
        tokens = ESTIMATES_DEEPSEEK[name]["tokens"]
        cpt = ESTIMATES_DEEPSEEK[name]["chars_per_token"]
        print(f"  {name:<25s} | {chars:>8d} | {tokens:>8d} | {cpt:>12.2f}")
    print("-" * 80)
    
    print("\n" + "=" * 80)
    print("📈 KEY INSIGHTS")
    print("=" * 80)
    
    print("\n1. RELATIVE EFFICIENCY (Higher = More Efficient)")
    print("-" * 60)
    
    # Sort by GPT chars/token
    sorted_gpt = sorted(ESTIMATES_GPT.items(), key=lambda x: x[1]["chars_per_token"], reverse=True)
    print("\n  GPT-4 Ranking (most to least efficient):")
    for i, (name, data) in enumerate(sorted_gpt, 1):
        bar = "█" * int(data["chars_per_token"] * 10)
        print(f"    {i}. {name:25s}: {data['chars_per_token']:.2f} {bar}")
    
    sorted_ds = sorted(ESTIMATES_DEEPSEEK.items(), key=lambda x: x[1]["chars_per_token"], reverse=True)
    print("\n  DeepSeek Ranking (most to least efficient):")
    for i, (name, data) in enumerate(sorted_ds, 1):
        bar = "█" * int(data["chars_per_token"] * 10)
        print(f"    {i}. {name:25s}: {data['chars_per_token']:.2f} {bar}")
    
    print("\n2. INFORMATION DENSITY ANALYSIS")
    print("-" * 60)
    print("""
  Classical Chinese:
    ✓ Highest information density per character
    ✓ No spaces, no articles, no conjugation
    ✓ Concise grammar (subjects often omitted)
    ✗ But: Modern tokenizers NOT optimized for Classical Chinese
    ✗ Each character may be split into multiple subword tokens
    
  Modern Chinese:
    ✓ Reasonable information density
    ✓ No spaces, but more function words than Classical
    ✗ More tokens per character than English
    
  English:
    ✓ Tokenizers highly optimized for English
    ✓ Common words often map to single tokens
    ✗ Requires spaces, articles, prepositions
    ✗ Verb conjugations expand token count
    
  Spanish:
    ✓ Similar to English in structure
    ✗ More verb conjugations than English
    ✗ Accent marks may require extra tokens
    """)
    
    print("\n3. HYPOTHESIS: Why Classical Chinese Might NOT Save Tokens")
    print("-" * 60)
    print("""
  The "Classical Chinese saves tokens" hypothesis assumes:
    → Information density → fewer tokens
    
  BUT modern tokenizers are trained on:
    → Primarily modern web text (English, Chinese, code)
    → Very little Classical Chinese training data
    
  RESULT:
    → Classical Chinese characters are treated as rare Unicode
    → Each character may be split into 1-2 subword tokens
    → Despite density, token count may be HIGHER than expected
    
  VERDICT:
    → Classical Chinese is INFORMATION-dense, not TOKEN-dense
    → To actually save tokens, you'd need a Classical-Chinese-optimized tokenizer
    → For modern LLMs: English or Modern Chinese likely more token-efficient
    """)


def run_actual_tests():
    """Run actual tokenizer tests if libraries are available."""
    print("\n" + "=" * 80)
    print("🧪 ACTUAL TOKENIZER TESTS")
    print("=" * 80)
    
    # Try tiktoken
    try:
        import tiktoken
        print("\n✓ tiktoken installed - running OpenAI tests...")
        enc = tiktoken.get_encoding("cl100k_base")
        
        for filename, label in [
            ("classical_chinese.txt", "Classical Chinese"),
            ("modern_chinese.txt", "Modern Chinese"),
            ("english.txt", "English"),
            ("spanish.txt", "Spanish"),
        ]:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    text = f.read()
                tokens = enc.encode(text)
                print(f"  {label:25s}: {len(tokens):5d} tokens ({len(text)} chars, ratio: {len(text)/len(tokens):.2f})")
            else:
                print(f"  {label:25s}: File not found")
    except ImportError:
        print("\n✗ tiktoken not installed")
        print("  Install: pip install tiktoken")
    
    # Try transformers for DeepSeek
    try:
        from transformers import AutoTokenizer
        print("\n✓ transformers installed - running DeepSeek tests...")
        tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-llm-7b-base", trust_remote_code=True)
        
        for filename, label in [
            ("classical_chinese.txt", "Classical Chinese"),
            ("modern_chinese.txt", "Modern Chinese"),
            ("english.txt", "English"),
            ("spanish.txt", "Spanish"),
        ]:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    text = f.read()
                tokens = tokenizer.encode(text)
                print(f"  {label:25s}: {len(tokens):5d} tokens ({len(text)} chars, ratio: {len(text)/len(tokens):.2f})")
            else:
                print(f"  {label:25s}: File not found")
    except ImportError:
        print("\n✗ transformers not installed")
        print("  Install: pip install transformers")
    except Exception as e:
        print(f"\n✗ DeepSeek tokenizer error: {e}")


if __name__ == "__main__":
    print_analysis()
    
    print("\n" + "=" * 80)
    print("Want to run actual tests?")
    print("  1. Install: pip install tiktoken transformers")
    print("  2. Run: python analyze_tokens.py")
    print("=" * 80)
    
    # Auto-run if libraries available
    run_actual_tests()
