import json
nav = json.load(open(r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\data\nav.json", encoding="utf-8"))
alltitles = []
def walk(ns):
    for n in ns:
        alltitles.append((n.get("title", ""), n.get("url", "")))
        walk(n.get("children", []))
for sec, items in nav.items():
    walk(items)
hits = [t for t in alltitles if any(w in (t[0] + t[1]).lower() for w in ["watch", "表盘", "face", "watchface"])]
print("官方Vela站含 '表盘/watchface' 的导航项:", len(hits))
for t in hits:
    print("   ", t)
print("导航项总数:", len(alltitles))
