import urllib.request, re
from bs4 import BeautifulSoup
url="https://iot.mi.com/vela/quickapp/zh/guide/start.html"
req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0","Accept-Language":"zh-CN"})
html=urllib.request.urlopen(req,timeout=30).read().decode("utf-8","ignore")
soup=BeautifulSoup(html,"lxml")
print("TITLE:", soup.title.string if soup.title else None)
# content
for sel in ["div.theme-default-content","main.page","div.content","article"]:
    el=soup.select_one(sel)
    print("SEL",sel,"->", "FOUND" if el else "none")
# sidebar
for sel in ["aside.sidebar","nav.sidebar-nav","ul.sidebar-links","div.sidebar"]:
    el=soup.select_one(sel)
    print("SIDEBAR_SEL",sel,"->","FOUND" if el else "none")
# sample content h1
c=soup.select_one("div.theme-default-content") or soup.select_one("main")
if c:
    h1=c.find("h1")
    print("H1:", h1.get_text(strip=True) if h1 else None)
    # count code blocks
    print("PRE count:", len(c.find_all("pre")))
    print("First 300 text:", c.get_text("\n",strip=True)[:300])
# nav links (top sections)
nav=soup.select_one("nav")
if nav:
    for a in nav.find_all("a",href=True)[:20]:
        print("NAV-A:", a["href"], a.get_text(strip=True))
