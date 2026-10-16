# -*- coding: utf-8 -*-
import json
d = json.load(open(r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\data\pages.json", encoding="utf-8"))
md = d["/vela/quickapp/zh/samples/"]["md"]
print("== total chars:", len(md))
print(md[:4000])
