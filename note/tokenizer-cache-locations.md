# Tokenizer 文件缓存位置

`AutoTokenizer.from_pretrained()` 下载的文件存放在 HuggingFace 默认缓存目录。

## 缓存根目录

```
C:\Users\Dell\.cache\huggingface\hub\
```

## 已缓存模型

| 模型 ID | 本地路径 | tokenizer.json |
|---------|---------|:---:|
| `Qwen/Qwen-7B` | `models--Qwen--Qwen-7B\snapshots\ef3c...` | 0B（缺主文件） |
| `Qwen/Qwen2.5-72B` | `models--Qwen--Qwen2.5-72B\snapshots\efba...` | ✅ 7.0MB |
| `Qwen/Qwen3.5-27B` | `models--Qwen--Qwen3.5-27B\snapshots\fc05...` | ✅（镜像站下成） |
| `deepseek-ai/DeepSeek-V2-Lite` | `models--deepseek-ai--DeepSeek-V2-Lite\snapshots\604d...` | ✅ 4.6MB |
| `deepseek-ai/DeepSeek-V3` | `models--deepseek-ai--DeepSeek-V3\snapshots\e815...` | ✅ 7.8MB |
| `microsoft/phi-2` | `models--microsoft--phi-2\snapshots\810d...` | ✅ 2.1MB |
| `gpt2` | `models--gpt2\snapshots\607a...` | ✅ vocab.json 1.0MB |

## 命名规则

`models--{org}--{repo}\snapshots\{commit_hash}\`

- `/` 替换为 `--`
- snapshots 下每个 commit 一个子目录
- `.no_exist` 目录记录"文件存在但大小为 0"（下载失败的标记）

## 镜像站

```
$env:HF_ENDPOINT = "https://hf-mirror.com"
```

墙内下载走镜像，文件最终仍存在同一缓存目录。
