import json
d = json.load(open("data/token_counts.json", encoding="utf-8"))
tc = d.get("open_source", {})
print("Token counts keys:", list(tc.keys())[:5])
# Check PVALUES in HTML
html = open("index.html", encoding="utf-8").read()
start = html.find("PVALUES =")
end = html.find("</script>", start)
print("PVALUES length:", end - start if start >= 0 else "NOT FOUND")
print("Has fisher_p:", "fisher_p" in html[start:end])
print("Has perm_p:", "perm_p" in html[start:end])
