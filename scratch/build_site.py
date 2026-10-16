# -*- coding: utf-8 -*-
"""构建教学站数据：site/assets/content.js
合并 pages.json(官方站) + js_course.json(从零教程) + 学习路径，生成完整侧边栏树。
"""
import json, os, re
from urllib.parse import urljoin

ROOT = r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51"
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "site")
ASSETS = os.path.join(SITE, "assets")
os.makedirs(ASSETS, exist_ok=True)

BASE = "https://iot.mi.com"
pages = json.load(open(os.path.join(DATA, "pages.json"), encoding="utf-8"))
js_course = json.load(open(os.path.join(DATA, "js_course.json"), encoding="utf-8"))

# ---------- 1. 修正官方页内相对链接为绝对地址 ----------
link_re = re.compile(r'\]\(([^)\s]+)\)')
def fix_links(md, abs_url):
    def repl(m):
        href = m.group(1)
        if href.startswith("http://") or href.startswith("https://") or href.startswith("#") or href.startswith("mailto:"):
            return m.group(0)
        new = urljoin(abs_url, href)
        return "](" + new + ")"
    return link_re.sub(repl, md)

content = {}  # key -> {title, md, kind}

# ---------- 1b. 编程示例索引页重排为卡片网格 ----------
SAMPLES_KEY = "/vela/quickapp/zh/samples/"

def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))

def rebuild_samples_md(md):
    """把官方 samples 索引页(封面图+名称描述+GitHub/Gitee 图标链接)
    解析为结构化数据,重排为卡片网格 HTML。"""
    items = []
    cur = None
    state = "cover"  # cover -> text -> links
    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            continue
        m_cover = re.match(r'!\[[^\]]*\]\(([^)]+)\)$', line)
        if m_cover:
            cur = {"cover": m_cover.group(1), "name": "", "desc": "", "links": []}
            items.append(cur)
            state = "text"
            continue
        if cur is None:
            continue
        if state == "text" and not line.startswith("[!["):
            name, _, desc = line.partition(" ")
            cur["name"], cur["desc"] = name, desc.strip()
            state = "links"
        elif state == "links":
            for u in re.findall(r'\[!\[[^\]]*\]\([^)]*\)\]\(([^)]+)\)', line):
                cur["links"].append(u)
    if not items:
        return md  # 解析失败时保留原样兜底
    cards = ['<h1>编程示例 Samples</h1>',
             '<p>以下示例均为开源的 Vela 快应用，可直接克隆源码对照学习；点击卡片下方按钮跳转对应代码仓库。</p>',
             '<div class="samples-grid">']
    for it in items:
        links = "".join(
            '<a class="repo-link" href="%s" target="_blank" rel="noopener">%s 源码</a>'
            % (_esc(u), "GitHub" if "github.com" in u else "Gitee")
            for u in it["links"])
        cards.append(
            '<div class="sample-card">'
            '<img class="sample-cover" src="%s" alt="%s" loading="lazy">'
            '<div class="sample-body">'
            '<h3 class="sample-name">%s</h3>'
            '<p class="sample-desc">%s</p>'
            '<div class="sample-links">%s</div>'
            '</div></div>'
            % (_esc(it["cover"]),
               _esc(it["name"] or "示例封面"),
               _esc(it["name"]),
               _esc(it["desc"]),
               links))
    cards.append('</div>')
    return "\n".join(cards)

if SAMPLES_KEY in pages and isinstance(pages[SAMPLES_KEY].get("md"), str):
    rebuilt = rebuild_samples_md(pages[SAMPLES_KEY]["md"])
    if rebuilt != pages[SAMPLES_KEY]["md"]:
        pages[SAMPLES_KEY]["md"] = rebuilt
        print("samples index rebuilt as card grid (%d chars)" % len(rebuilt))

for url, p in pages.items():
    abs_url = BASE + url
    md = fix_links(p["md"], abs_url)
    content[url] = {"title": p["title"], "md": md, "kind": "vela"}

# ---------- 2. 由 URL 路径重建完整侧边栏树 ----------
SECTION_TITLES = {
    "guide": "教程 Guide",
    "components": "组件 Components",
    "features": "JS 接口 Features",
    "samples": "编程示例 Samples",
    "tools": "工具 Tools",
}
PREFIX = "/vela/quickapp/zh/"

def section_pages(sec):
    out = []
    for url, p in pages.items():
        if url.startswith(PREFIX + sec + "/") or url == PREFIX + sec + "/":
            out.append((url, p["title"]))
    return out

def build_section_tree(sec):
    urls = section_pages(sec)
    # 先处理目录索引页(以/结尾)，保证分组标题正确
    urls.sort(key=lambda x: (not x[0].endswith("/"), x[0]))
    top = []
    def find(nodes, seg):
        for n in nodes:
            if n["_seg"] == seg:
                return n
        return None
    def insert(nodes, parts, url, title):
        seg = parts[0]
        last = len(parts) == 1
        node = find(nodes, seg)
        if node is None:
            node = {"_seg": seg, "title": title, "key": url, "children": []}
            nodes.append(node)
        if not last:
            insert(node["children"], parts[1:], url, title)
        else:
            node["title"] = title
            node["key"] = url
    for url, title in urls:
        rel = url[len(PREFIX):]            # guide/start/use-ide.html
        parts = rel.rstrip("/").split("/") # ['guide','start','use-ide.html']
        if len(parts) == 1:
            # 章节首页（如 /guide/）→ 作为顶部「概述」节点
            top.append({"_seg": sec + "__index", "title": title, "key": url, "children": []})
        else:
            insert(top, parts[1:], url, title)
    return top

def clean(nodes):
    res = []
    for n in nodes:
        ch = clean(n.get("children", []))
        res.append({"title": n["title"], "key": n["key"], "children": ch})
    return res

ref_sections = []
for sec in ["components", "features", "samples", "tools"]:
    tree = clean(build_section_tree(sec))
    ref_sections.append({"id": sec, "title": SECTION_TITLES[sec], "tree": tree})
# 教程 Guide 作为合并后的「XiaoMi Vela 教学」大标题下的第一个章节
guide_section = {"id": "guide", "title": "教程 Guide", "tree": clean(build_section_tree("guide"))}

# ---------- 3. JavaScript 从零基础教程 树 ----------
js_tree = [
    {"title": "第一部分 · JS 基础（ES5）", "key": None, "children": [
        {"title": c["title"], "key": "js:" + c["slug"], "children": []}
        for c in js_course if c["slug"] in [
            "intro","syntax-basics","types","operators","control-flow","loops",
            "functions","arrays","strings","objects","date-regex","error"]
    ]},
    {"title": "第二部分 · ES6 新特性", "key": None, "children": [
        {"title": c["title"], "key": "js:" + c["slug"], "children": []}
        for c in js_course if c["slug"] in [
            "es6-let-const","es6-arrow","es6-template","es6-destructuring","es6-rest-spread",
            "es6-class","es6-modules","es6-promise","es6-collections","es6-iterators","es6-advanced"]
    ]},
    {"title": "第三部分 · 实战衔接", "key": None, "children": [
        {"title": c["title"], "key": "js:" + c["slug"], "children": []}
        for c in js_course if c["slug"] == "practice-vela"
    ]},
]
js_sections = []
for c in js_course:
    content["js:" + c["slug"]] = {"title": c["title"], "md": c["md"], "kind": "js"}
js_sections.append({"id": "js", "title": "JavaScript 从零基础教程", "tree": js_tree})

# ---------- 3b. 插件开发 树（清洗 OronBox 站内容 + 官方权威参考）----------
plugin_course = json.load(open(os.path.join(DATA, "plugin_course.json"), encoding="utf-8"))
plugin_tree = [{"title": c["title"], "key": "plugin:" + c["slug"], "children": []} for c in plugin_course]
for c in plugin_course:
    content["plugin:" + c["slug"]] = {"title": c["title"], "md": c["md"], "kind": "plugin"}
plugin_section = {"id": "plugin", "title": "插件开发", "tree": plugin_tree}

# ---------- 4. 学习路径 landing ----------
lp_md = """# 如何高效学习本教程

欢迎来到 **XiaoMi Vela 开发零基础教学站**。本教程覆盖 XiaoMi Vela（快应用）的官方文档（教程 / 组件 / JS 接口 / 编程示例 / 工具），并补充了**从零开始的系统化教学**；后续还会补充**插件开发与表盘开发**的专项内容。

## 建议的学习顺序
1. **先补 JavaScript 基础**：如果你完全没写过代码，务必从《JavaScript 从零基础教程》第 1 章开始。Vela 快应用的页面逻辑全部用 JS 编写。
2. **再学 XiaoMi Vela 教程**：按「快速入门 → 基础功能（框架）→ 进阶功能 → 设计/最佳实践 → 发布」顺序学习。
3. **随用随查组件 / JS 接口**：开发时遇到某个 UI 组件或系统能力（蓝牙、传感器、网络…），直接查对应章节。
4. **工具章节**帮你装好 AIoT-IDE、跑模拟器、真机调试与打包。

## 两大内容来源
- 📘 **JavaScript 从零基础教程**：作者依据 [MDN JavaScript 指南](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide) 编写的 ES5/ES6 系统课，含讲解、示例、小结、练习与权威参考链接。
- 📗 **XiaoMi Vela 官方文档**：教程、组件、JS 接口、编程示例、工具，章节结构与官方站完全一致，内容 faithfully 搬运，并在每页顶部加了「本节要点」教学提示。

## 小目标
跟着「快速入门」写一个天气预报卡片，再用 JS 课程里的 `fetch` + `Promise`/`async` 把它接上真实数据——你就真正入门了。

> 提示：右上角可切换深色模式；左侧搜索框可全文检索；导航栏两大板块（JavaScript 教学 / XiaoMi Vela 教学）均可点击展开或收起。
"""
content["lp:start"] = {"title": "如何高效学习", "md": lp_md, "kind": "lp"}

# ---------- 5. 顶层分组（导航栏可折叠大标题，默认收起）----------
# 顺序：JavaScript 教学 → XiaoMi Vela 教学(教程 + 组件 + JS接口 + 编程示例 + 工具)
groups = [
    {"id": "js", "title": "JavaScript 教学", "sections": js_sections},
    {"id": "xiaomi", "title": "XiaoMi Vela 教学", "sections": [guide_section, plugin_section] + ref_sections},
]
# 学习路径(lp)仅作为落地页，不进入导航/搜索
all_sections = js_sections + [guide_section, plugin_section] + ref_sections

# ---------- 6. 写出 content.js ----------
out = {"groups": groups, "sections": all_sections, "pages": content}
with open(os.path.join(ASSETS, "content.js"), "w", encoding="utf-8") as f:
    f.write("window.SITE=")
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";")

print("groups:", len(groups))
print("sections:", len(all_sections))
print("pages in content:", len(content))
print("js chapters:", len(js_course))
total_nodes = sum(len(s["tree"]) for s in all_sections)
print("top-level nav groups:", total_nodes)
