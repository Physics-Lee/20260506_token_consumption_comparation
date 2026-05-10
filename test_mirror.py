import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from transformers import AutoTokenizer
t = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B", trust_remote_code=True)
print("vocab:", t.vocab_size)
print("cn:", len(t.encode("你好世界")))
print("en:", len(t.encode("hello world")))
