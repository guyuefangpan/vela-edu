import urllib.request, re, sys
url = "https://iot.mi.com/vela/quickapp/zh/guide/start.html"
try:
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8","ignore")
    print("STATUS_OK len=", len(html))
    hrefs = re.findall(r'href="([^"]+)"', html)
    print("TOTAL_HREFS=", len(hrefs))
    for m in hrefs:
        if "guide" in m or "reference" in m or "api" in m or "vela" in m:
            print("HREF:", m)
    if "sidebar" in html.lower():
        print("SIDEBAR_KEYWORD_FOUND")
    idx = html.find("nav")
    if idx>0:
        print("NAV_SNIPPET:", html[idx:idx+800])
    else:
        print("NO_NAV_TAG")
        # try to find common doc frameworks
        for kw in ["vuepress","vitepress","docusaurus","__NUXT__","window.__","sidebar"]:
            if kw in html.lower():
                print("FRAMEWORK_HINT:", kw)
except Exception as e:
    print("ERR", repr(e))
