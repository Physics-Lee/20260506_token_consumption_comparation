#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokenizer Comparison Test
Tests token counts for Classical Chinese, Modern Chinese, English, and Spanish
using OpenAI (GPT) and DeepSeek tokenizers.
"""

import os
import json
from pathlib import Path

# Try importing tiktoken for OpenAI models
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print("Warning: tiktoken not installed. Run: pip install tiktoken")

# Try importing transformers for DeepSeek tokenizer
try:
    from transformers import AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers not installed. Run: pip install transformers")

# File paths
FILES = {
    "Classical Chinese (左传 - 晋文公流亡)": "classical_chinese.txt",
    "Modern Chinese (杨振宁)": "modern_chinese.txt",
    "English (Paul Graham)": "english.txt",
    "Spanish (Allende)": "spanish.txt",
}


def read_file(filepath):
    """Read file and return content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def count_chars(text):
    """Count characters (excluding whitespace for CJK, including for others)."""
    # For Chinese (both classical and modern), count all characters including punctuation
    # For English and Spanish, count letters + numbers + punctuation (excluding spaces)
    return len(text)


def test_openai_tokenizers(texts):
    """Test with OpenAI tokenizers via tiktoken."""
    if not TIKTOKEN_AVAILABLE:
        return {}
    
    results = {}
    
    # Test different OpenAI encodings
    encodings = {
        "GPT-3.5/4 (cl100k_base)": "cl100k_base",
        "GPT-4o (o200k_base)": "o200k_base",
    }
    
    for enc_name, enc_id in encodings.items():
        print(f"\n{'='*60}")
        print(f"Testing: {enc_name}")
        print(f"{'='*60}")
        
        try:
            enc = tiktoken.get_encoding(enc_id)
            encoding_results = {}
            
            for name, text in texts.items():
                tokens = enc.encode(text)
                token_count = len(tokens)
                char_count = len(text)
                
                # Calculate efficiency: chars per token (higher = more efficient)
                efficiency = char_count / token_count if token_count > 0 else 0
                
                encoding_results[name] = {
                    "tokens": token_count,
                    "characters": char_count,
                    "chars_per_token": round(efficiency, 2)
                }
                
                print(f"\n{name}:")
                print(f"  Characters: {char_count}")
                print(f"  Tokens: {token_count}")
                print(f"  Chars/Token: {efficiency:.2f}")
            
            results[enc_name] = encoding_results
            
        except Exception as e:
            print(f"Error with {enc_name}: {e}")
    
    return results


def test_deepseek_tokenizer(texts):
    """Test with DeepSeek tokenizer."""
    if not TRANSFORMERS_AVAILABLE:
        return {}
    
    results = {}
    
    print(f"\n{'='*60}")
    print("Testing: DeepSeek Tokenizer")
    print(f"{'='*60}")
    
    try:
        # Load DeepSeek tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            "deepseek-ai/deepseek-llm-7b-base",
            trust_remote_code=True
        )
        
        for name, text in texts.items():
            tokens = tokenizer.encode(text)
            token_count = len(tokens)
            char_count = len(text)
            
            # Calculate efficiency: chars per token
            efficiency = char_count / token_count if token_count > 0 else 0
            
            results[name] = {
                "tokens": token_count,
                "characters": char_count,
                "chars_per_token": round(efficiency, 2)
            }
            
            print(f"\n{name}:")
            print(f"  Characters: {char_count}")
            print(f"  Tokens: {token_count}")
            print(f"  Chars/Token: {efficiency:.2f}")
            
    except Exception as e:
        print(f"Error loading DeepSeek tokenizer: {e}")
        print("Note: DeepSeek tokenizer requires 'transformers' and model download.")
        print("Alternative: Use HuggingFace tokenizers library directly.")
    
    return {"DeepSeek": results}


def print_comparison_table(all_results, texts):
    """Print a comparison table."""
    print(f"\n\n{'='*80}")
    print("SUMMARY COMPARISON TABLE")
    print(f"{'='*80}")
    
    # Prepare table
    headers = ["Text", "Chars"]
    for tokenizer_name in all_results.keys():
        headers.extend([f"{tokenizer_name} (Tokens)", "Chars/Token"])
    
    # Print header
    header_line = " | ".join([f"{h:^30}" for h in headers])
    print(header_line)
    print("-" * len(header_line))
    
    # Print data rows
    for text_name in texts.keys():
        row = [text_name, str(len(texts[text_name]))]
        
        for tokenizer_name, results in all_results.items():
            if text_name in results:
                data = results[text_name]
                row.append(str(data["tokens"]))
                row.append(f"{data['chars_per_token']:.2f}")
            else:
                row.extend(["N/A", "N/A"])
        
        print(" | ".join([f"{cell:^30}" for cell in row]))
    
    print(f"\n{'='*80}")
    print("INTERPRETATION:")
    print("- Higher 'Chars/Token' = MORE EFFICIENT (fewer tokens needed)")
    print("- Classical Chinese expected to have highest efficiency due to information density")
    print(f"{'='*80}")


def save_results(all_results, texts, filename="token_results.json"):
    """Save results to JSON file."""
    output = {
        "texts": {name: len(text) for name, text in texts.items()},
        "results": all_results
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nResults saved to: {filename}")


def main():
    """Main function."""
    print("="*80)
    print("TOKENIZER COMPARISON TEST")
    print("Comparing Classical Chinese, Modern Chinese, English, Spanish")
    print("="*80)
    
    # Read all texts
    texts = {}
    for name, filename in FILES.items():
        filepath = Path(__file__).parent / filename
        if filepath.exists():
            texts[name] = read_file(filepath)
            print(f"✓ Loaded: {name} ({len(texts[name])} chars)")
        else:
            print(f"✗ Missing: {filename}")
    
    if not texts:
        print("No text files found! Please ensure .txt files are in the same directory.")
        return
    
    all_results = {}
    
    # Test OpenAI tokenizers
    if TIKTOKEN_AVAILABLE:
        openai_results = test_openai_tokenizers(texts)
        all_results.update(openai_results)
    else:
        print("\nSkipping OpenAI tests (tiktoken not installed)")
        print("Install with: pip install tiktoken")
    
    # Test DeepSeek tokenizer
    if TRANSFORMERS_AVAILABLE:
        deepseek_results = test_deepseek_tokenizer(texts)
        all_results.update(deepseek_results)
    else:
        print("\nSkipping DeepSeek tests (transformers not installed)")
        print("Install with: pip install transformers")
    
    # Print comparison
    if all_results:
        print_comparison_table(all_results, texts)
        save_results(all_results, texts)
    else:
        print("\nNo tokenizers available. Please install required libraries.")
        print("\nQuick start:")
        print("  pip install tiktoken transformers")


if __name__ == "__main__":
    main()
