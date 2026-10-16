const fs = require("fs");
const raw = fs.readFileSync("C:/Users/Administrator/WorkBuddy/2026-10-11-12-57-51/site/assets/content.js", "utf8");
global.window = {};
eval(raw.replace(/^window\.SITE=/, "global.window.SITE="));
const S = global.window.SITE;
console.log("groups:", S.groups.map(g => g.title + " (" + g.sections.length + " sections)"));
S.groups.forEach(g => {
  console.log(" -", g.title);
  g.sections.forEach(s => console.log("     *", s.title, "->", s.tree.length, "top nodes"));
});
console.log("flat sections:", S.sections.length, "pages:", Object.keys(S.pages).length);
