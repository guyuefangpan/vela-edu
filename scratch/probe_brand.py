import urllib.request, re, os

BASE = "https://iot.mi.com/vela/quickapp/zh/guide/start.html"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")

html = get(BASE)
print("== HTML head links ==")
for m in re.findall(r'<link[^>]+>', html):
    if any(k in m.lower() for k in ["icon", "stylesheet", "logo"]):
        print(m[:300])

# 找所有 css 链接
css_links = re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', html)
print("\n== CSS files ==")
for c in css_links:
    print(c)
