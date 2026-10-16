/* Vela 快应用教学站 · 前端渲染逻辑 */
(function () {
  "use strict";
  var SITE = window.SITE || { sections: [], pages: {} };
  var sidebar = document.getElementById("sidebar");
  var content = document.getElementById("content");
  var searchInput = document.getElementById("searchInput");
  var searchResults = document.getElementById("searchResults");
  var search = searchInput.closest(".search");
  var overlay = document.createElement("div");
  overlay.className = "sidebar-overlay";
  document.body.appendChild(overlay);
  var isMobile = function () { return window.matchMedia("(max-width: 860px)").matches; };

  // 扁平化页面顺序（用于上下页）
  var flatKeys = [];
  SITE.sections.forEach(function (sec) {
    (function walk(nodes) {
      nodes.forEach(function (n) {
        if (n.key) flatKeys.push(n.key);
        if (n.children && n.children.length) walk(n.children);
      });
    })(sec.tree);
  });

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  // ---------- 侧边栏 ----------
  function renderNode(node, depth) {
    var hasKids = node.children && node.children.length;
    if (!hasKids) {
      var a = el("a", "nav-link", node.title);
      a.href = "#" + node.key;
      a.dataset.key = node.key;
      return a;
    }
    var grp = el("div", "nav-group");
    var label = el("div", "group-label");
    label.appendChild(el("span", null, node.title));
    var caret = el("span", "arrow", "▶");
    label.appendChild(caret);
    if (node.key) label.dataset.key = node.key;
    label.addEventListener("click", function (e) {
      if (e.target === caret) {
        grp.classList.toggle("collapsed");
      } else if (node.key) {
        location.hash = node.key;
      } else {
        grp.classList.toggle("collapsed");
      }
    });
    grp.appendChild(label);
    var kids = el("div", "group-children");
    node.children.forEach(function (c) { kids.appendChild(renderNode(c, depth + 1)); });
    grp.appendChild(kids);
    // 分类节点默认折叠，点击标题展开
    grp.classList.add("collapsed");
    return grp;
  }

  function renderSidebar() {
    sidebar.innerHTML = "";
    SITE.groups.forEach(function (g) {
      // 顶层可折叠大标题（默认收起）
      var topGrp = el("div", "nav-group nav-topgroup");
      topGrp.classList.add("collapsed");
      var topLabel = el("div", "group-label top-label");
      topLabel.appendChild(el("span", null, g.title));
      var topCaret = el("span", "arrow", "▶");
      topLabel.appendChild(topCaret);
      topLabel.addEventListener("click", function () { topGrp.classList.toggle("collapsed"); });
      topGrp.appendChild(topLabel);
      var topKids = el("div", "group-children");
      g.sections.forEach(function (sec) {
        // 每个板块本身也是可折叠分组
        var secGrp = el("div", "nav-group");
        var secLabel = el("div", "group-label sec-label");
        secLabel.appendChild(el("span", null, sec.title));
        var secCaret = el("span", "arrow", "▶");
        secLabel.appendChild(secCaret);
        secLabel.addEventListener("click", function () { secGrp.classList.toggle("collapsed"); });
        secGrp.appendChild(secLabel);
        var secKids = el("div", "group-children");
        sec.tree.forEach(function (n) { secKids.appendChild(renderNode(n, 0)); });
        secGrp.appendChild(secKids);
        secGrp.classList.add("collapsed"); // 板块默认折叠
        topKids.appendChild(secGrp);
      });
      topGrp.appendChild(topKids);
      sidebar.appendChild(topGrp);
    });
  }

  // ---------- 内容渲染 ----------
  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function render(key) {
    var page = SITE.pages[key];
    if (!page) {
      content.innerHTML = "<h1>页面未找到</h1><p>该章节可能未抓取或已迁移。</p>";
      return;
    }
    var html = "";
    if (page.kind === "vela") {
      html += '<div class="teach-callout">📘 <b>本节要点</b>：本页为 Vela 官方参考文档（章节与官网完全一致）。零基础同学建议先学左侧《JavaScript 从零基础教程》；开发时涉及的变量、函数、Promise / 异步、fetch 等都可在该教程查到对应章节。</div>';
    } else if (page.kind === "js") {
      html += '<div class="teach-callout">🟧 <b>JavaScript 从零基础</b>：本节依据 MDN JavaScript 指南编写，含讲解、可运行示例、小结、练习与权威参考链接。建议按顺序学习。</div>';
    }
    try {
      html += marked.parse(page.md);
    } catch (err) {
      html += "<pre>" + escapeHtml(page.md) + "</pre>";
    }
    content.innerHTML = html;
    content.querySelectorAll("pre code").forEach(function (b) {
      try { window.hljs.highlightElement(b); } catch (e) {}
    });
    setActive(key);
    renderPager(key);
    window.scrollTo(0, 0);
    document.title = page.title + " · XiaoMi Vela 开发教学站";
  }

  function setActive(key) {
    sidebar.querySelectorAll(".active").forEach(function (e) { e.classList.remove("active"); });
    var node = sidebar.querySelector('[data-key="' + cssEscape(key) + '"]');
    if (node) {
      node.classList.add("active");
      var p = node.parentElement;
      while (p && p !== sidebar) {
        if (p.classList && p.classList.contains("nav-group")) p.classList.remove("collapsed");
        p = p.parentElement;
      }
      if (node.scrollIntoView) node.scrollIntoView({ block: "nearest" });
    }
  }

  function cssEscape(s) {
    return String(s).replace(/"/g, '\\"');
  }

  function renderPager(key) {
    var idx = flatKeys.indexOf(key);
    var prev = idx > 0 ? flatKeys[idx - 1] : null;
    var next = idx >= 0 && idx < flatKeys.length - 1 ? flatKeys[idx + 1] : null;
    var pager = el("div", "pager");
    if (prev) {
      var pa = el("a", "prev");
      pa.href = "#" + prev;
      pa.innerHTML = '<div class="plabel">← 上一页</div><div class="ptitle">' + escapeHtml(SITE.pages[prev] ? SITE.pages[prev].title : "") + "</div>";
      pager.appendChild(pa);
    } else {
      pager.appendChild(el("span"));
    }
    if (next) {
      var na = el("a", "next");
      na.href = "#" + next;
      na.innerHTML = '<div class="plabel">下一页 →</div><div class="ptitle">' + escapeHtml(SITE.pages[next] ? SITE.pages[next].title : "") + "</div>";
      pager.appendChild(na);
    } else {
      pager.appendChild(el("span"));
    }
    content.appendChild(pager);
  }

  // ---------- 路由 ----------
  function route() {
    var key = location.hash ? decodeURIComponent(location.hash.slice(1)) : "";
    if (!key || !SITE.pages[key]) key = "lp:start";
    render(key);
  }
  window.addEventListener("hashchange", route);

  // ---------- 搜索 ----------
  function doSearch(q) {
    q = q.trim().toLowerCase();
    if (!q) { searchResults.classList.remove("show"); return; }
    var hits = [];
    SITE.sections.forEach(function (sec) {
      (function walk(nodes) {
        nodes.forEach(function (n) {
          var p = SITE.pages[n.key];
          if (p) {
            var hay = (p.title + " " + (p.md || "")).toLowerCase();
            var i = hay.indexOf(q);
            if (i >= 0 && hits.length < 30) {
              var ex = p.md ? p.md.substr(Math.max(0, i - 20), 60).replace(/\n/g, " ") : "";
              hits.push({ sec: sec.title, title: p.title, key: n.key, ex: ex });
            }
          }
          if (n.children) walk(n.children);
        });
      })(sec.tree);
    });
    searchResults.innerHTML = "";
    if (!hits.length) {
      searchResults.innerHTML = '<div class="sr-item">无匹配结果</div>';
    } else {
      hits.forEach(function (h) {
        var it = el("div", "sr-item");
        it.innerHTML = '<div class="sec">' + escapeHtml(h.sec) + '</div><div class="tt">' + escapeHtml(h.title) + '</div><div class="ex">' + escapeHtml(h.ex) + "…</div>";
        it.addEventListener("click", function () {
          location.hash = h.key;
          searchResults.classList.remove("show");
          searchInput.value = "";
        });
        searchResults.appendChild(it);
      });
    }
    searchResults.classList.add("show");
  }
  searchInput.addEventListener("input", function () { doSearch(searchInput.value); });
  search.addEventListener("click", function (e) {
    if (isMobile() && !search.classList.contains("expanded")) {
      search.classList.add("expanded");
      searchInput.focus();
      e.stopPropagation();
    }
  });
  document.addEventListener("click", function (e) {
    var inSearch = e.target.closest(".search");
    if (!inSearch) {
      searchResults.classList.remove("show");
      if (isMobile()) search.classList.remove("expanded");
    }
  });

  // ---------- 主题：跟随系统（无手动切换）----------
  function applySystemTheme() {
    var dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    var t = dark ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", t);
    document.getElementById("hljs-light").disabled = dark;
    document.getElementById("hljs-dark").disabled = !dark;
  }
  applySystemTheme();
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var onChange = function (e) { applySystemTheme(); };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  // ---------- 移动端菜单 ----------
  document.getElementById("menuBtn").addEventListener("click", function (e) {
    e.stopPropagation();
    var open = sidebar.classList.toggle("open");
    overlay.classList.toggle("show", open);
  });
  overlay.addEventListener("click", function () {
    sidebar.classList.remove("open");
    overlay.classList.remove("show");
  });
  sidebar.addEventListener("click", function (e) {
    if (e.target.closest(".nav-link") && isMobile()) {
      sidebar.classList.remove("open");
      overlay.classList.remove("show");
    }
  });

  // ---------- 启动 ----------
  renderSidebar();
  route();
})();
