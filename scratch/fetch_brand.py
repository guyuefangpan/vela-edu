import urllib.request, re, os

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
BASE = "https://iot.mi.com"

# 1) 下载 favicon（小船图标）
os.makedirs(r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\site\assets", exist_ok=True)
try:
    data = urllib.request.urlopen(urllib.request.Request(BASE + "/vela/quickapp/favicon.ico", headers=UA), timeout=25).read()
    p = r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\site\assets\favicon.ico"
    open(p, "wb").write(data)
    print("favicon saved:", len(data), "bytes ->", p)
except Exception as e:
    print("favicon ERR:", repr(e)[:160])

# 2) 抓 CSS 找主题色
css = urllib.request.urlopen(urllib.request.Request(BASE + "/vela/quickapp/assets/css/0.styles.a3d28e0e.css", headers=UA), timeout=25).read().decode("utf-8", "ignore")
print("\n== CSS color tokens ==")
for m in re.findall(r'(--[a-z-]+|--theme-color|theme-color|color-primary|\$[a-z-]+):\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))', css):
    print(m)
# 也找 #3eaf7c 或类似 accent
print("\n== possible accent hex near navbar/link ==")
for m in re.findall(r'(#[0-9a-fA-F]{6})\b', css):
    if m.lower() not in ("#ffffff", "#000000", "#f6f6f6", "#f6f8fa"):
        pass
# 去重统计出现次数高的色值
from collections import Counter
cnt = Counter(re.findall(r'#[0-9a-fA-F]{6}', css))
for c, n in cnt.most_common(15):
    print(c, n)
