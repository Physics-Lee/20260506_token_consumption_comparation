from pathlib import Path
cache = Path.home() / ".cache" / "huggingface" / "hub" / "models--Qwen--Qwen3.5-27B"
if cache.exists():
    for f in cache.rglob("*"):
        if f.is_file():
            print(f"{f.stat().st_size:>10}  {f}")
else:
    print("No cache found for Qwen3.5-27B")
