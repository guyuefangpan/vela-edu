// 把站点 content.js 全站内容拍平成单一 Markdown 文档（按导航树顺序，层级对齐）
const fs = require('fs');
const ROOT = 'C:\\Users\\Administrator\\WorkBuddy\\2026-10-11-12-57-51';
const contentJs = fs.readFileSync(ROOT + '\\site\\assets\\content.js', 'utf8');

const sandbox = {};
new Function('window', contentJs + '\nreturn window.SITE;')(sandbox);
const SITE = sandbox.SITE;
const pages = SITE.pages;

// 把 markdown 内部最高标题对齐到 targetLevel，其余相对顺延（跳过代码围栏）
function shiftAlign(md, targetLevel) {
  const lines = md.split('\n');
  let inFence = false;
  const levels = [];
  for (const line of lines) {
    if (/^```/.test(line)) { inFence = !inFence; continue; }
    if (inFence) continue;
    const m = line.match(/^(#{1,6})\s/);
    if (m) levels.push(m[1].length);
  }
  if (!levels.length) return md;
  const minH = Math.min(...levels);
  let offset = targetLevel - minH;
  if (offset < 0) offset = 0;
  let inF2 = false;
  const out2 = lines.map(line => {
    if (/^```/.test(line)) { inF2 = !inF2; return line; }
    if (inF2) return line;
    const m = line.match(/^(#{1,6})\s+(.*)$/);
    if (m) return '#'.repeat(Math.min(m[1].length + offset, 6)) + ' ' + m[2];
    return line;
  });
  return out2.join('\n');
}

const h = (lvl, text) => '#'.repeat(Math.min(lvl, 6)) + ' ' + text;
const out = [];

// 前言
out.push('# XiaoMi Vela 开发零基础教学站 · 全站离线文档');
out.push('');
out.push('> 本文档是站点全部内容的离线 Markdown 版本，章节结构与线上站完全一致，可作为开源仓库的随附资料。');
out.push('>');
out.push('> 内容来源：小米 Vela 官方文档（iot.mi.com/vela）、MDN JavaScript 指南，以及依据官方与权威资料二次编排的教学章节。');
out.push('>');
out.push('> 教学站在线版：将 `site/` 目录整体部署为静态站点即可（详见仓库说明）。');
out.push('');

// 站点导读（学习路径落地页），对齐到二级标题
if (pages['lp:start']) {
  out.push(shiftAlign(pages['lp:start'].md, 2).trim());
  out.push('');
}

// 递归遍历导航树
function walkTree(nodes, level) {
  for (const n of nodes) {
    const isPage = n.key && pages[n.key];
    if (isPage) {
      // 页面节点：不加单独标题，内容最高标题对齐到本层
      out.push('');
      out.push(shiftAlign(pages[n.key].md, level).trim());
      out.push('');
    } else {
      // 分组节点：输出标题
      out.push('');
      out.push(h(level, n.title));
      out.push('');
    }
    if (n.children && n.children.length) walkTree(n.children, level + 1);
  }
}

for (const g of SITE.groups) {
  out.push('');
  out.push(h(1, g.title)); // 大标题 #（一级）
  out.push('');
  for (const s of g.sections) {
    out.push('');
    out.push(h(2, s.title)); // 章节 ##（二级）
    out.push('');
    walkTree(s.tree, 3); // 树节点从三级起
  }
}

const md = out.join('\n').replace(/\n{3,}/g, '\n\n').trim() + '\n';
const dest = ROOT + '\\site\\全站文档.md';
fs.writeFileSync(dest, md, 'utf-8');

console.log('pages in SITE.pages:', Object.keys(pages).length);
console.log('total groups:', SITE.groups.length);
console.log('output bytes:', Buffer.byteLength(md, 'utf-8'));
console.log('output file:', dest);
