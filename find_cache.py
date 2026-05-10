import os
cache = os.path.expanduser("~/.cache/huggingface/hub")
for root, dirs, files in os.walk(cache):
    for f in files:
        if f.endswith(".json"):
            fp = os.path.join(root, f)
            size = os.path.getsize(fp)
            print(f"{size:>10}  {fp}")
