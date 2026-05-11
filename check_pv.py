import json, re
html = open("index.html", encoding="utf-8").read()
m = re.search(r"PVALUES = ({.*?});", html, re.DOTALL)
if m:
    d = json.loads(m.group(1))
    print("Top keys:", list(d.keys()))
    print("cc keys:", list(d.get("cc", {}).keys())[:3])
    print("other keys:", list(d.get("other", {}).keys())[:3])
    # Check one entry
    cc = d.get("cc", {})
    if cc:
        first = list(cc.keys())[0]
        print(f"Entry [{first}]:", list(cc[first].keys()))
else:
    print("PVALUES not found")
