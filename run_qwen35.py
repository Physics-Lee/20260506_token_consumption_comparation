import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["PYTHONIOENCODING"] = "utf-8"
import sys
sys.argv = ["precompute_tokens.py"]
exec(open("code/precompute_tokens.py", encoding="utf-8").read())
