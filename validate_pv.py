import json, re
html = open("index.html", encoding="utf-8").read()
m = re.search(r"PVALUES = ({.*?});\s*</script>", html, re.DOTALL)
if m:
    try:
        d = json.loads(m.group(1))
        print("VALID JSON, keys:", list(d.keys()))
    except Exception as e:
        print("INVALID JSON:", e)
