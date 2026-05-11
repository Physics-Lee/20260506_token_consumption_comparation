import json, re
html = open("index.html", encoding="utf-8").read()
m = re.search(r"PVALUES = ({.*?});", html, re.DOTALL)
if m:
    d = json.loads(m.group(1))
    print("cc has r50k:", "r50k_base" in d["cc"])
    print("cc has o200k:", "o200k_base" in d["cc"])
    print("other has r50k:", "r50k_base" in d["other"])
    if "o200k_base" in d["cc"]:
        print("o200k cc entries:", list(d["cc"]["o200k_base"].keys()))
