const marked = require("C:/Users/Administrator/WorkBuddy/2026-10-11-12-57-51/site/assets/marked.min.js");
const fs = require("fs");
const raw = fs.readFileSync("C:/Users/Administrator/WorkBuddy/2026-10-11-12-57-51/site/assets/content.js","utf8");
global.window={};
eval(raw.replace(/^window\.SITE=/,"global.window.SITE="));
const SITE = global.window.SITE;
function test(key){
  const p = SITE.pages[key];
  const html = marked.parse(p.md);
  const h2=(html.match(/<h2/g)||[]).length, code=(html.match(/<pre/g)||[]).length;
  console.log(key, "=> h2:",h2,"code:",code,"len:",html.length, "| 权威参考Links:", (html.match(/权威参考/g)||[]).length);
}
["plugin:overview","plugin:manifest","plugin:runtime","plugin:permissions","plugin:ui","plugin:network","plugin:distribution","plugin:appside"].forEach(test);
console.log("plugin pages total:", Object.keys(SITE.pages).filter(k=>k.startsWith("plugin:")).length);
