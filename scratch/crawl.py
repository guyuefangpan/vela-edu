import urllib.request, re, json, os, time, sys
from bs4 import BeautifulSoup
from html2text import HTML2Text
from urllib.parse import urlparse

BASE = "https://iot.mi.com"
OUT = r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\data"
os.makedirs(OUT, exist_ok=True)

SEED = [
    "/vela/quickapp/zh/guide/",
    "/vela/quickapp/zh/components/",
    "/vela/quickapp/zh/features/",
    "/vela/quickapp/zh/samples/",
    "/vela/quickapp/zh/tools/",
]

h2t = HTML2Text()
h2t.body_width = 0
h2t.baseurl = BASE
h2t.ignore_links = False
h2t.ignore_images = False
h2t.single_line_break = False

def fetch(url):
    req = urllib.request.Request(BASE+url, headers={"User-Agent":"Mozilla/5.0","Accept-Language":"zh-CN,zh;q=0.9"})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8","ignore")

def norm(u):
    u = u.split("#")[0]
    if u.startswith("//"):
        return u
    if not u.startswith("/"):
        return None
    if "/zh/" not in u:
        return None
    if ".." in u:
        return None
    # ensure trailing slash for directory links (no .html extension)
    if not u.endswith(".html") and not u.endswith("/"):
        u = u + "/"
    return u

def content_md(soup):
    c = soup.select_one("div.theme-default-content") or soup.select_one("main.page")
    if not c:
        return ""
    for a in c.select("a.header-anchor"):
        a.decompose()
    # remove edit-page / last-updated footer if inside
    return h2t.handle(str(c))

def title_of(soup, url):
    c = soup.select_one("div.theme-default-content") or soup
    h1 = c.find("h1")
    if h1:
        return h1.get_text(strip=True).lstrip("# ").strip()
    if soup.title:
        t = soup.title.get_text(strip=True)
        return t.split("|")[0].strip()
    return url

visited = set()
queue = list(SEED)
pages = {}  # url -> {title, md}

# also extract sidebar tree per top-level section
def sidebar_tree(soup):
    aside = soup.select_one("aside.sidebar")
    root = aside if aside else soup
    tree = []
    def walk(ul, depth):
        items=[]
        for li in ul.find_all("li", recursive=False):
            a = li.find("a", recursive=False) or li.find("a")
            if not a or not a.get("href"):
                continue
            href = norm(a["href"])
            if not href:
                continue
            node = {"title": a.get_text(strip=True), "url": href, "children": []}
            sub = li.find("ul")
            if sub:
                node["children"] = walk(sub, depth+1)
            items.append(node)
        return items
    top = root.select_one("ul.sidebar-links")
    if top:
        tree = walk(top, 0)
    return tree

nav_by_section = {}

def section_of(url):
    m = re.match(r"/vela/quickapp/zh/([^/]+)/", url)
    return m.group(1) if m else "other"

count=0
while queue:
    url = queue.pop(0)
    url = norm(url)
    if not url or url in visited:
        continue
    visited.add(url)
    try:
        html = fetch(url)
    except Exception as e:
        print("FETCH_FAIL", url, repr(e)[:100], file=sys.stderr)
        continue
    soup = BeautifulSoup(html, "lxml")
    md = content_md(soup)
    ttl = title_of(soup, url)
    pages[url] = {"title": ttl, "md": md}
    count += 1
    sec = section_of(url)
    if sec not in nav_by_section:
        nav_by_section[sec] = sidebar_tree(soup)
    # discover links from sidebar + content
    for a in soup.select("aside.sidebar a[href]") + soup.select("div.theme-default-content a[href]"):
        h = norm(a.get("href",""))
        if h and h not in visited and h not in queue:
            queue.append(h)
    time.sleep(0.15)
    if count % 20 == 0:
        print("crawled", count, "visited", len(visited), file=sys.stderr)

print("TOTAL_PAGES", len(pages), file=sys.stderr)

# save
with open(os.path.join(OUT,"pages.json"),"w",encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=1)
with open(os.path.join(OUT,"nav.json"),"w",encoding="utf-8") as f:
    json.dump(nav_by_section, f, ensure_ascii=False, indent=1)

# section summary
summary = {}
for url,p in pages.items():
    summary.setdefault(section_of(url),[]).append((url, p["title"], len(p["md"])))
with open(os.path.join(OUT,"summary.txt"),"w",encoding="utf-8") as f:
    for sec, lst in summary.items():
        f.write(f"=== {sec} ({len(lst)}) ===\n")
        for u,t,l in lst:
            f.write(f"  {u}  | {t} | {l}c\n")
print("SAVED", file=sys.stderr)
