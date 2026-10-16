# -*- coding: utf-8 -*-
"""生成 JavaScript 从零基础教程（ES5 + ES6）结构化数据。
依据 MDN JavaScript 指南（权威来源）编写，内容为中文教学，含讲解/示例/小结/练习/参考链接。
输出: data/js_course.json  -> list of {slug, title, md}
"""
import json, os

OUT = r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\data"
os.makedirs(OUT, exist_ok=True)

MDN = "https://developer.mozilla.org/zh-CN/docs/Web/JavaScript"

def ch(slug, title, md):
    return {"slug": slug, "title": title, "md": md}

course = []
course.append(ch("intro", "第1章 · 认识 JavaScript 与运行环境", r"""# 第1章 · 认识 JavaScript 与运行环境

## 1.1 JavaScript 是什么
JavaScript（简称 JS）是一种**轻量、解释型、基于原型**的脚本语言，最初用于浏览器中为网页添加交互，现在也能在服务器端（Node.js）、桌面、移动端甚至手环/手表的「快应用」里运行。

> 权威说明：JavaScript 是 ECMAScript 规范的一种实现。我们常说的 ES5（2009）、ES6（2015，官方称 ES2015）都是 ECMAScript 的不同版本。Vela 快应用运行的就是 ECMAScript 5/6 子集。

## 1.2 JavaScript 与 Java 的关系
**毫无关系**。名字相似只是历史营销原因。Java 是静态类型、编译型语言；JavaScript 是动态类型、解释执行的语言。

## 1.3 如何运行第一段代码
Vela 快应用里代码写在 `.ux` 文件的 `<script>` 中。学习语法时，你可以用浏览器最快验证：
1. 打开浏览器，按 F12 打开「开发者工具」。
2. 切换到 Console（控制台）面板。
3. 输入 `console.log("Hello, Vela")`，回车。

```js
console.log("Hello, Vela");
```

控制台会打印出 `Hello, Vela`。`console.log` 是调试时最常用的方法，作用是把内容输出到控制台。

## 1.4 本章小结
- JS 是动态、弱类型脚本语言，遵循 ECMAScript 规范。
- ES5 / ES6 是两套重要的语法版本，本课程都会覆盖。
- 用浏览器 Console 即可快速验证语法。

## 1.5 练习
1. 在控制台运行 `console.log(1 + 1)`，观察结果。
2. 把 `Hello, Vela` 改成你的名字再运行一次。

## 参考
- MDN · JavaScript 指南：什么是 JavaScript """ + f"({MDN}/Guide/Introduction)"))

course.append(ch("syntax-basics", "第2章 · 语法基础：变量、注释与语句", r"""# 第2章 · 语法基础：变量、注释与语句

## 2.1 语句与分号
JS 中每条「语句」通常用分号 `;` 结束。现代引擎会自动插入分号（ASI），但**显式写分号更稳妥**，能避免歧义。

```js
var a = 1;
var b = 2;
```

## 2.2 注释
注释不会被运行，用于给人看。

```js
// 这是单行注释

/* 这是
   多行注释 */
```

## 2.3 变量声明：var（ES5）
ES5 用 `var` 声明变量：

```js
var name = "小米手环";
var price;
price = 249;
```

`var` 的特点（坑点）：
- **函数作用域**而非块级作用域（后面会讲）。
- **变量提升**：声明会被提升到函数顶部（见第7章）。
- 允许重复声明，不会报错。

## 2.4 变量声明：let / const（ES6，推荐）
ES6 引入 `let` 和 `const`，解决了 `var` 的缺陷：

```js
let count = 0;      // 可重新赋值
count = 1;

const PI = 3.14;    // 常量，不可重新赋值
// PI = 3;          // 报错：Assignment to constant variable
```

- `let`：块级作用域，不可重复声明。
- `const`：块级作用域，声明时必须赋值，且不能重新绑定（但对象内部属性可改）。

> 现代开发最佳实践：**默认用 `const`，需要重新赋值时才用 `let`，几乎不用 `var`。**

## 2.5 标识符命名规则
- 可由字母、数字、下划线 `_`、美元符 `$` 组成，不能以数字开头。
- 区分大小写：`name` 与 `Name` 不同。
- 不能用关键字（如 `var`、`if`、`function`）。
- 推荐小驼峰：`userName`、`fetchWeather()`。

## 2.6 本章小结
- 语句以 `;` 结尾，注释用 `//` 或 `/* */`。
- `var`（ES5）有提升与函数作用域问题；`let`/`const`（ES6）更安全。
- 命名用小驼峰，避开关键字。

## 2.7 练习
1. 用 `let` 声明一个变量 `score` 并赋值为 90，再改成 95。
2. 用 `const` 声明 `appName = "Vela"`，尝试重新赋值看报错。

## 参考
- MDN · 语法与数据类型：声明 """ + f"({MDN}/Guide/Grammar_and_types)"))

course.append(ch("types", "第3章 · 数据类型与类型转换", r"""# 第3章 · 数据类型与类型转换

## 3.1 原始类型（Primitive）
JS 有 7 种原始类型：
- `Number`：数字（整数与浮点统一）。
- `String`：字符串。
- `Boolean`：true / false。
- `Undefined`：声明了但未赋值。
- `Null`：空值。
- `Symbol`（ES6）：唯一值，后面进阶讲。
- `BigInt`（ES2020）：大整数。

```js
var n = 10;
var s = "hello";
var b = true;
var u;            // undefined
var empty = null; // null
```

## 3.2 对象类型（Object）
除原始类型外，一切皆对象（数组、函数、日期都是对象）。

```js
var user = { name: "word", age: 18 };
var list = [1, 2, 3];
```

## 3.3 typeof 运算符
```js
typeof 10;        // "number"
typeof "hi";      // "string"
typeof true;      // "boolean"
typeof undefined; // "undefined"
typeof null;      // "object"  (历史 bug)
typeof {};        // "object"
typeof function(){}; // "function"
```

## 3.4 类型转换
弱类型语言经常自动转换（**隐式转换**），但容易出错，建议**显式转换**。

```js
// 转数字
Number("123");    // 123
parseInt("10px"); // 10
parseFloat("3.14"); // 3.14

// 转字符串
String(123);      // "123"
(123).toString(); // "123"

// 转布尔
Boolean("");      // false
Boolean("hi");    // true
```

> 经典坑：`"3" - 1` 结果是 `2`（字符串被转数字），但 `"3" + 1` 结果是 `"31"`（数字被转字符串拼接）。比较运算中 `==` 会做类型转换，`===` 不会。

## 3.5 == 与 ===
- `==` 宽松相等：先转换类型再比较。
- `===` 严格相等：类型和值都要相同。**永远优先用 `===`。**

```js
1 == "1";   // true
1 === "1";  // false
null == undefined; // true
null === undefined; // false
```

## 3.6 本章小结
- 7 种原始类型 + 对象类型。
- 用 `typeof` 查看类型（注意 `null` 的坑）。
- 优先用 `===` 与显式类型转换。

## 3.7 练习
1. `console.log(1 + "2" + 3)` 结果是什么？为什么？
2. 用 `===` 判断 `0` 与 `false` 是否相等。

## 参考
- MDN · 语法与数据类型：数据结构与类型 """ + f"({MDN}/Guide/Grammar_and_types)"))

course.append(ch("operators", "第4章 · 运算符与表达式", r"""# 第4章 · 运算符与表达式

## 4.1 算术运算符
```js
+  -  *  /  %  **
```
```js
5 % 2;   // 1  取余
2 ** 3;  // 8  幂（ES6）
```

## 4.2 赋值运算符
```js
=  +=  -=  *=  /=
x += 3;  // 等价于 x = x + 3
```

## 4.3 比较运算符
```js
>  <  >=  <=  ==  ===  !=  !==
```

## 4.4 逻辑运算符
```js
&&  (与)   true && false  -> false
||  (或)   true || false  -> true
!   (非)   !true          -> false
```
逻辑运算符会返回**其中一个操作数**（短路求值）：
```js
var name = input || "匿名";   // input 为假时用默认值
```

## 4.5 三元（条件）运算符
```js
var age = 20;
var tip = age >= 18 ? "成年" : "未成年";
```

## 4.6 自增自减
```js
var i = 1;
i++;   // 2
++i;   // 前缀/后缀在表达式中顺序不同
```

## 4.7 本章小结
- 算术、赋值、比较、逻辑、三元运算符覆盖了日常计算。
- `&&` / `||` 返回操作数本身，常用于设置默认值。
- 比较一律用 `===` / `!==`。

## 4.8 练习
1. 用三元运算符判断一个数是奇数还是偶数。
2. `var a = 1; var b = a++ + a;` 求 `b` 与 `a`。

## 参考
- MDN · 表达式与运算符 """ + f"({MDN}/Guide/Expressions_and_operators)"))

course.append(ch("control-flow", "第5章 · 控制流：条件判断", r"""# 第5章 · 控制流：条件判断

## 5.1 if / else if / else
```js
var score = 85;
if (score >= 90) {
  console.log("优秀");
} else if (score >= 60) {
  console.log("及格");
} else {
  console.log("不及格");
}
```
条件用 `()` 包裹，代码块用 `{}` 包裹。**即使只有一行，也建议写 `{}`**，避免日后加代码出错。

## 5.2 switch
当同一个变量要匹配多个固定值时用 `switch` 更清晰：
```js
var day = 1;
switch (day) {
  case 1:
    console.log("周一");
    break;
  case 2:
    console.log("周二");
    break;
  default:
    console.log("其他");
}
```
**每个 `case` 末尾要写 `break`**，否则会「穿透」执行下一个 case。

## 5.3 三元运算符（复习）
简单二选一可用 `条件 ? A : B`。

## 5.4 本章小结
- `if/else` 处理范围判断，`switch` 处理多固定值匹配。
- `case` 记得 `break`，否则穿透。
- 总是用 `{}` 包裹代码块。

## 5.5 练习
写一个函数，根据分数返回 "A/B/C/D" 等级。

## 参考
- MDN · 控制流与错误处理 """ + f"({MDN}/Guide/Control_flow_and_error_handling)"))

course.append(ch("loops", "第6章 · 循环与迭代", r"""# 第6章 · 循环与迭代

## 6.1 for 循环
```js
for (var i = 0; i < 5; i++) {
  console.log(i);
}
```
三段式：`初值; 条件; 步进`。

## 6.2 while / do...while
```js
var i = 0;
while (i < 3) {
  console.log(i);
  i++;
}

do {
  console.log("至少执行一次");
} while (false);
```

## 6.3 break / continue
- `break`：跳出整个循环。
- `continue`：跳过本次，进入下一轮。

```js
for (var i = 0; i < 5; i++) {
  if (i === 2) continue;
  if (i === 4) break;
  console.log(i);   // 0 1 3
}
```

## 6.4 for...in（遍历对象键 / 数组下标，ES5）
```js
var obj = { a: 1, b: 2 };
for (var k in obj) {
  console.log(k, obj[k]);
}
```
> 遍历数组建议用 `for...of` 或普通 `for`，`for...in` 会遍历到原型链上的可枚举属性。

## 6.5 for...of（ES6，遍历可迭代值）
```js
var arr = [10, 20, 30];
for (var v of arr) {
  console.log(v);   // 10 20 30
}
```
`for...of` 可遍历数组、字符串、Map、Set、arguments 等「可迭代对象」。

## 6.6 本章小结
- `for` 计数，`while` 条件循环，`for...of` 遍历值，`for...in` 遍历键。
- `break` 跳出，`continue` 跳过。

## 6.7 练习
用 `for` 循环打印 1~100 中能被 3 整除的数。

## 参考
- MDN · 循环与迭代 """ + f"({MDN}/Guide/Loops_and_iteration)"))

course.append(ch("functions", "第7章 · 函数（含作用域、提升、闭包）", r"""# 第7章 · 函数（含作用域、提升、闭包）

## 7.1 函数声明与调用
```js
function add(a, b) {
  return a + b;
}
add(1, 2);   // 3
```

## 7.2 函数表达式
```js
var mul = function (a, b) { return a * b; };
mul(2, 3);   // 6
```

## 7.3 作用域
- 全局作用域 / 函数作用域 / 块级作用域（`let`/`const` 才有）。
- 内部可访问外部变量，外部不能访问内部变量。

## 7.4 变量提升（Hoisting）
`var` 与函数声明会被提升到作用域顶部：
```js
console.log(x);   // undefined（不报错）
var x = 5;
```
等价于 `var x; console.log(x); x = 5;`。函数声明整体提升，因此可以先调用后定义。

## 7.5 arguments 对象
ES5 用 `arguments` 获取所有实参：
```js
function sum() {
  var total = 0;
  for (var i = 0; i < arguments.length; i++) {
    total += arguments[i];
  }
  return total;
}
sum(1, 2, 3);  // 6
```

## 7.6 闭包（Closure）
函数记住了它的词法作用域：
```js
function counter() {
  var n = 0;
  return function () {
    n++;
    return n;
  };
}
var c = counter();
c(); // 1
c(); // 2
```
闭包是模块化、私有变量的基础，在 Vela 里常用于封装状态。

## 7.7 箭头函数（ES6，先了解，第14章详讲）
```js
var add = (a, b) => a + b;
```

## 7.8 本章小结
- 函数声明会整体提升；`var` 只提升声明不提升赋值。
- `arguments` 收集实参（ES5）；ES6 用 rest 参数更优雅。
- 闭包 = 函数 + 它定义时的作用域。

## 7.9 练习
用闭包实现一个「只能加、不能改」的计数器。

## 参考
- MDN · 函数 """ + f"({MDN}/Guide/Functions)"))

course.append(ch("arrays", "第8章 · 数组（ES5 常用方法）", r"""# 第8章 · 数组（ES5 常用方法）

## 8.1 创建与访问
```js
var arr = [1, 2, 3];
arr[0];      // 1
arr.length;  // 3
```

## 8.2 常用 ES5 方法
```js
arr.push(4);            // 末尾添加 -> [1,2,3,4]
arr.pop();              // 末尾删除
arr.unshift(0);         // 开头添加
arr.shift();            // 开头删除
arr.indexOf(2);         // 1（找不到返回 -1）
arr.slice(1, 3);        // 浅拷贝 [2,3]
arr.splice(1, 1, 9);    // 增删改
arr.join("-");          // "1-2-3"
```

## 8.3 遍历三剑客
```js
arr.forEach(function (v, i) { console.log(i, v); });
var doubled = arr.map(function (v) { return v * 2; });      // 映射
var evens = arr.filter(function (v) { return v % 2 === 0; }); // 过滤
var sum = arr.reduce(function (acc, v) { return acc + v; }, 0); // 累积
```
`map/filter/reduce` 是函数式编程核心，写业务首选，比手写 `for` 更清晰。

## 8.4 排序
```js
var nums = [3, 1, 2];
nums.sort(function (a, b) { return a - b; });  // [1,2,3]
```

## 8.5 本章小结
- 改变原数组：`push/pop/shift/unshift/splice/sort/reverse`。
- 返回新数组：`map/filter/slice/concat`。
- 聚合：`reduce/forEach/indexOf/join`。

## 8.6 练习
用 `filter` 取出数组中大于 10 的数，再用 `map` 把它们翻倍。

## 参考
- MDN · 索引集合（数组） """ + f"({MDN}/Guide/Indexed_collections)"))

course.append(ch("strings", "第9章 · 字符串（ES5 方法）", r"""# 第9章 · 字符串（ES5 方法）

## 9.1 定义
```js
var s = "Vela";
var s2 = '快应用';
```
字符串不可变：所有方法都返回新字符串，不改原串。

## 9.2 常用方法
```js
s.length;            // 4
s.charAt(0);         // "V"
s.indexOf("e");      // 1
s.substring(0, 2);   // "Ve"
s.slice(1);          // "ela"
s.toUpperCase();     // "VELA"
s.split("");         // ["V","e","l","a"]
" a ".trim();        // "a"
"ab".concat("cd");   // "abcd"
```

## 9.3 转义字符
```js
var t = "他说：\"你好\"";   // 双引号需转义
var path = 'C:\\tmp';       // 反斜杠转义
```

## 9.4 模板字符串（ES6，第15章详讲）
```js
var name = "Vela";
var msg = `你好，${name}`;   // 反引号 + ${}
```

## 9.5 本章小结
- 字符串不可变，方法返回新串。
- `indexOf/slice/substring/split/trim/toUpperCase` 最常用。
- 拼接优先用 ES6 模板字符串。

## 9.6 练习
把 `"hello world"` 的首字母转大写（提示：charAt + slice + toUpperCase）。

## 参考
- MDN · 数字与字符串 """ + f"({MDN}/Guide/Numbers_and_strings)"))

course.append(ch("objects", "第10章 · 对象与 JSON", r"""# 第10章 · 对象与 JSON

## 10.1 对象字面量
```js
var user = {
  name: "word",
  age: 18,
  sayHi: function () { console.log("hi"); }
};
```

## 10.2 访问属性
```js
user.name;       // 点语法
user["age"];     // 方括号（键为变量或含特殊字符时用）
```

## 10.3 增删改
```js
user.city = "北京";   // 增/改
delete user.age;      // 删
```

## 10.4 this
`this` 指向「调用函数的对象」：
```js
var obj = {
  name: "Vela",
  show: function () { console.log(this.name); }
};
obj.show();   // "Vela"
```

## 10.5 JSON
JSON 是数据交换格式，和对象很像但有规则：键必须双引号，值只能是字符串/数字/布尔/null/数组/对象。
```js
var json = '{"name":"word","age":18}';
var obj = JSON.parse(json);   // 字符串 -> 对象
var str = JSON.stringify(obj); // 对象 -> 字符串
```
Vela 快应用读写文件、网络传输都大量用到 JSON。

## 10.6 本章小结
- 对象用 `{ key: value }`，方法也是属性。
- `this` 绑定到调用者。
- `JSON.parse` / `JSON.stringify` 转换数据。

## 10.7 练习
把 `var p = {x:1, y:2}` 转成 JSON 字符串，再解析回来修改 `x=10`。

## 参考
- MDN · 处理对象 """ + f"({MDN}/Guide/Working_with_objects)"))

course.append(ch("date-regex", "第11章 · 日期 Date 与正则 RegExp", r"""# 第11章 · 日期 Date 与正则 RegExp

## 11.1 Date
```js
var now = new Date();          // 当前时间
var d = new Date(2026, 0, 1);  // 2026-01-01（月份 0 起）
now.getFullYear();
now.getMonth();                // 0~11
now.getDate();
now.getTime();                 // 时间戳（毫秒）
```

## 11.2 正则 RegExp
用于匹配/校验字符串：
```js
var re = /^\d{6}$/;            // 6 位数字
re.test("123456");             // true

"apple banana".match(/a\w+/g); // ["apple","anana"]
"a-b-c".split(/-/);            // ["a","b","c"]
```
常用元字符：`\d` 数字、`\w` 单词、`+` 1+、`*` 0+、`.` 任意、`^` 开头、`$` 结尾、`g` 全局。

## 11.3 本章小结
- `Date` 月份从 0 开始，注意坑。
- 正则用于校验（手机号、邮箱）和提取。

## 11.4 练习
写一个正则校验中国大陆手机号（1 开头，11 位）。

## 参考
- MDN · 表示日期与时间：https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Representing_dates_times
- MDN · 正则表达式：https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Regular_expressions
""" ))

course.append(ch("error", "第12章 · 错误处理 try/catch", r"""# 第12章 · 错误处理 try/catch

## 12.1 基本用法
```js
try {
  var data = JSON.parse(badStr);
} catch (e) {
  console.log("解析失败:", e.message);
} finally {
  console.log("无论成功失败都执行");
}
```
`try` 里抛错会跳到 `catch`，`finally` 总会执行（常用于释放资源）。

## 12.2 主动抛错
```js
function divide(a, b) {
  if (b === 0) throw new Error("除数不能为0");
  return a / b;
}
```

## 12.3 本章小结
- `try/catch` 防止程序因异常崩溃。
- `throw` 主动抛错，`Error` 携带信息。

## 12.4 练习
给除法函数加 try/catch，调用 `divide(1,0)` 时优雅提示。

## 参考
- MDN · 控制流与错误处理（异常处理） """ + f"({MDN}/Guide/Control_flow_and_error_handling)"))

course.append(ch("es6-let-const", "第13章 · ES6(1)：let/const 与块级作用域", r"""# 第13章 · ES6(1)：let/const 与块级作用域

ES6 最重要的一批改进就是让变量声明更安全。

## 13.1 块级作用域
```js
if (true) {
  let x = 1;
  const y = 2;
}
// 此处 x, y 都无法访问（块外不可见）
```

## 13.2 暂时性死区（TDZ）
`let/const` 声明前访问会报错（不像 `var` 返回 undefined）：
```js
console.log(a); // ReferenceError
let a = 1;
```

## 13.3 不可重复声明
```js
let b = 1;
let b = 2;   // SyntaxError
```

## 13.4 const 与对象
`const` 锁定的是「绑定」，对象内部仍可改：
```js
const user = { name: "Vela" };
user.name = "Xiaomi"; // OK
// user = {};          // 报错
```

## 13.5 本章小结
- `let/const` 有块级作用域、TDZ、不可重复声明。
- 默认 `const`，需重赋值才 `let`。

## 13.6 练习
用 `let` 在 `for` 循环里声明计数器，对比 `var` 在异步回调里的差异。

## 参考
- MDN · let / const """ + f"({MDN}/Reference/Statements/let)"))

course.append(ch("es6-arrow", "第14章 · ES6(2)：箭头函数", r"""# 第14章 · ES6(2)：箭头函数

## 14.1 语法
```js
// 单参数可省略 ()
var f = x => x * 2;

// 多参数
var add = (a, b) => a + b;

// 多行需 {}
var calc = (a, b) => {
  var r = a + b;
  return r;
};

// 返回对象需加 ()
var make = () => ({ name: "Vela" });
```

## 14.2 this 绑定（关键区别）
箭头函数**没有自己的 `this`**，它继承外层 `this`：
```js
var obj = {
  name: "Vela",
  timers: function () {
    setTimeout(() => {
      console.log(this.name);  // "Vela"，箭头继承 timers 的 this
    }, 100);
  }
};
```
普通函数里 `this` 会指向 `window`/全局，箭头函数解决了这个经典坑。

## 14.3 不适用的场景
- 不能用 `new`（无构造能力）。
- 不能用 `arguments`（用 rest 参数代替）。
- 需要动态 `this` 的方法（如事件监听想拿到元素）慎用。

## 14.4 本章小结
- 箭头函数更简洁，且继承外层 `this`。
- 无 `this`/`arguments`/构造能力。

## 14.5 练习
用箭头函数改写第7章的 `add`，并观察 `this` 差异。

## 参考
- MDN · 箭头函数 """ + f"({MDN}/Reference/Functions/Arrow_functions)"))

course.append(ch("es6-template", "第15章 · ES6(3)：模板字符串", r"""# 第15章 · ES6(3)：模板字符串

## 15.1 基本用法
用反引号 `` ` `` 包裹，支持换行和 `${}` 插值：
```js
var name = "Vela";
var msg = `你好，${name}！
今天是 ${new Date().getFullYear()} 年`;
```

## 15.2 表达式
`${}` 里可放任意表达式：
```js
var a = 10, b = 20;
console.log(`${a} + ${b} = ${a + b}`);  // 10 + 20 = 30
```

## 15.3 标签模板（进阶）
```js
function tag(strings, ...values) {
  return strings.join("-");
}
tag`a${1}b${2}`;  // "a-b-"
```

## 15.4 本章小结
- 反引号支持多行与 `${}` 插值，告别字符串拼接。
- 比 `'...' + x + '...'` 可读性高得多。

## 15.5 练习
用模板字符串拼出一句话：「用户 word 的步数是 8000」。

## 参考
- MDN · 模板字符串 """ + f"({MDN}/Reference/Template_literals)"))

course.append(ch("es6-destructuring", "第16章 · ES6(4)：解构赋值", r"""# 第16章 · ES6(4)：解构赋值

## 16.1 数组解构
```js
var [a, b, c] = [1, 2, 3];
var [x, , z] = [10, 20, 30];   // x=10, z=30
var [first, ...rest] = [1, 2, 3]; // rest=[2,3]
```

## 16.2 对象解构
```js
var user = { name: "word", age: 18 };
var { name, age } = user;        // 同名提取
var { name: n } = user;          // 重命名
```

## 16.3 函数参数解构
```js
function show({ name, age }) {
  console.log(name, age);
}
show({ name: "Vela", age: 1 });
```

## 16.4 默认值
```js
var { name = "匿名" } = {};
```

## 16.5 本章小结
- 解构让「从数组/对象中提取值」一行搞定。
- 配合 rest `...` 与默认值非常灵活。

## 16.6 练习
从 `{a:1,b:2,c:3}` 中解构出 `a` 和其余部分 `rest`。

## 参考
- MDN · 解构赋值 """ + f"({MDN}/Reference/Operators/Destructuring_assignment)"))

course.append(ch("es6-rest-spread", "第17章 · ES6(5)：默认参数 / Rest / Spread", r"""# 第17章 · ES6(5)：默认参数 / Rest / Spread

## 17.1 默认参数
```js
function greet(name = "朋友") {
  console.log("你好，" + name);
}
greet();          // 你好，朋友
```

## 17.2 Rest 参数（替代 arguments）
```js
function sum(...nums) {
  return nums.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3);     // 6
```

## 17.3 Spread 展开
```js
var a = [1, 2], b = [3, 4];
var all = [...a, ...b];        // [1,2,3,4]
var obj2 = { ...user, age: 20 }; // 对象浅拷贝+覆盖
Math.max(...[1, 5, 3]);        // 5
```

## 17.4 本章小结
- 默认参数让函数更健壮。
- `...` 在参数位是 rest（收集合并），在值位是 spread（展开）。

## 17.5 练习
用 rest 实现一个可接收任意个数并返回平均值的函数。

## 参考
- MDN · 剩余参数 / 展开语法 """ + f"({MDN}/Reference/Functions/rest_parameters)"))

course.append(ch("es6-class", "第18章 · ES6(6)：类 class", r"""# 第18章 · ES6(6)：类 class

ES6 引入 `class` 语法糖，本质仍是原型继承，但更易读。

## 18.1 定义类
```js
class Animal {
  constructor(name) {
    this.name = name;
  }
  speak() {
    console.log(this.name + " 叫");
  }
}
var dog = new Animal("狗");
dog.speak();
```

## 18.2 继承
```js
class Dog extends Animal {
  speak() {
    console.log(this.name + " 汪汪");
  }
}
```

## 18.3 静态方法 / getter-setter
```js
class Utils {
  static now() { return Date.now(); }
}
Utils.now();

class Person {
  constructor(age) { this._age = age; }
  get age() { return this._age; }
  set age(v) { this._age = v; }
}
```

## 18.4 本章小结
- `class` 是原型继承的语法糖，比 ES5 手写构造函数清晰。
- `extends` 继承，`static` 静态方法，`get/set` 访问器。

## 18.5 练习
写一个 `Rectangle` 类，有 `width/height` 和求面积的方法。

## 参考
- MDN · 使用类 """ + f"({MDN}/Guide/Using_classes)"))

course.append(ch("es6-modules", "第19章 · ES6(7)：模块 import / export", r"""# 第19章 · ES6(7)：模块 import / export

> 注意：Vela 快应用并非浏览器 ES Module，它用 `.ux` 里的 `export default` / `import` 语法（框架自带模块系统），概念与 ES6 模块一致。

## 19.1 导出
```js
// math.js
export const PI = 3.14;
export function add(a, b) { return a + b; }
export default function sub(a, b) { return a - b; }
```

## 19.2 导入
```js
import sub, { PI, add } from "./math.js";
import * as m from "./math.js";   // 命名空间
```

## 19.3 意义
模块让代码按职责拆分、互不污染全局，是大型项目基础。

## 19.4 本章小结
- `export` 导出，`import` 导入，`default` 默认导出。
- Vela 的 `.ux` 模块语法与之同源。

## 19.5 练习
把第18章的 `Animal`、`Dog` 拆成两个模块互相引用。

## 参考
- MDN · JavaScript 模块 """ + f"({MDN}/Guide/Modules)"))

course.append(ch("es6-promise", "第20章 · ES6(8)：Promise 与异步", r"""# 第20章 · ES6(8)：Promise 与异步

## 20.1 为什么需要 Promise
JS 是单线程，网络请求等耗时操作不能阻塞。回调写法容易「回调地狱」，Promise 让异步更清晰。

## 20.2 创建 Promise
```js
var p = new Promise(function (resolve, reject) {
  setTimeout(function () {
    resolve("成功");
    // reject(new Error("失败"));
  }, 1000);
});
```

## 20.3 then / catch
```js
p.then(function (val) {
  console.log(val);
}).catch(function (err) {
  console.log(err);
});
```

## 20.4 链式调用
```js
fetchData()
  .then(parse)
  .then(show)
  .catch(handleError);
```

## 20.5 async/await（ES2017，进阶）
```js
async function load() {
  try {
    var data = await fetchData();
    show(data);
  } catch (e) {
    handleError(e);
  }
}
```
Vela 的 `fetch` 返回 Promise，用 `await` 写最直观。

## 20.6 本章小结
- Promise 代表「未来的值」，用 `then/catch` 处理结果。
- `async/await` 是 Promise 的语法糖，写起来像同步。

## 20.7 练习
用 Promise 封装一个「1 秒后返回数字 42」的函数。

## 参考
- MDN · Promise """ + f"({MDN}/Guide/Using_promises)"))

course.append(ch("es6-collections", "第21章 · ES6(9)：Map / Set / WeakMap / WeakSet", r"""# 第21章 · ES6(9)：Map / Set / Weak* 集合

## 21.1 Set（去重）
```js
var s = new Set([1, 2, 2, 3]);
s.size;          // 3
s.add(4);
s.has(2);        // true
s.delete(1);
```

## 21.2 Map（键可为任意类型）
```js
var m = new Map();
m.set("a", 1);
m.set(obj, "值");   // 键可以是对象
m.get("a");         // 1
```

## 21.3 WeakMap / WeakSet
键是「弱引用」，不阻止垃圾回收，适合存私有数据。

## 21.4 与对象/数组对比
- 需要唯一值集合 → `Set`
- 需要键值对且键非字符串 → `Map`
- 普通配置数据 → 仍用对象/数组

## 21.5 本章小结
- `Set` 自动去重，`Map` 键更灵活。
- `Weak*` 用于私有/缓存，不影响 GC。

## 21.6 练习
用 `Set` 给数组 `[1,2,2,3,3,3]` 去重。

## 参考
- MDN · 带键集合 """ + f"({MDN}/Guide/Keyed_collections)"))

course.append(ch("es6-iterators", "第22章 · ES6(10)：迭代器与生成器", r"""# 第22章 · ES6(10)：迭代器与生成器

## 22.1 可迭代对象
数组、字符串、Map、Set 都是可迭代对象，可被 `for...of` 遍历。

## 22.2 生成器
`function*` 用 `yield` 暂停/继续：
```js
function* count() {
  yield 1;
  yield 2;
  yield 3;
}
var g = count();
g.next(); // {value:1, done:false}
g.next(); // {value:2, done:false}
```

## 22.3 用途
生成器适合「惰性序列」、状态机、协程式异步（早期 async 实现）。

## 22.4 本章小结
- `function*` + `yield` 产生可暂停的函数。
- 理解迭代协议有助于读懂 `for...of`。

## 22.5 练习
写生成器依次返回斐波那契前 5 项。

## 参考
- MDN · 迭代器与生成器 """ + f"({MDN}/Guide/Iterators_and_generators)"))

course.append(ch("es6-advanced", "第23章 · ES6(11)：Symbol / Proxy / Reflect 进阶", r"""# 第23章 · ES6(11)：Symbol / Proxy / Reflect 进阶

## 23.1 Symbol
唯一、不可变的值，常作对象「私有」键或内置行为的标识：
```js
var key = Symbol("id");
var obj = {};
obj[key] = 123;
```

## 23.2 Proxy（代理）
拦截对象操作：
```js
var target = {};
var p = new Proxy(target, {
  get: function (t, k) { return k in t ? t[k] : "默认值"; },
  set: function (t, k, v) { t[k] = v; return true; }
});
```

## 23.3 Reflect
与 Proxy 陷阱一一对应的工具方法，规范化对象操作。

## 23.4 小结
这三者偏进阶，框架底层常用（`defineProperty`/`Proxy` 实现响应式）。了解即可，初学不必深究。

## 参考
- MDN · 元编程 """ + f"({MDN}/Guide/Meta_programming)"))

course.append(ch("practice-vela", "第24章 · 把 JS 用进 Vela：第一个天气卡片", r"""# 第24章 · 把 JS 用进 Vela：第一个天气卡片

学完语法，我们用一个最小例子串起来。Vela 快应用的页面由 `.ux` 组成，里面 `<script>` 写的就是标准 JS（ES5/ES6 子集）。

## 24.1 数据驱动界面
```js
export default {
  data: {
    city: "北京",
    temp: 26
  },
  onInit() {
    // 生命周期：页面初始化
    console.log("欢迎来到", this.city);
  },
  update() {
    this.temp = 28;   // 改数据，界面自动刷新
  }
}
```
这里 `data` 是状态，`this.temp = 28` 改变后，模板绑定的 `{temp}` 会自动更新——这正是「数据驱动」思想，和 React/Vue 同源。

## 24.2 用 ES6 让代码更干净
```js
const API = "https://example.com/weather";
const fetchWeather = async (city) => {
  const res = await fetch(`${API}?city=${city}`);
  const json = await res.json();
  return json.temp;
};
```

## 24.3 小结
- Vela 的 `<script>` 就是 JS，你前面学的全部用得上。
- 状态放 `data`，改状态即改界面。
- 网络请求用 `fetch` + Promise / `await`。

## 24.4 下一步
进入「Vela 快应用教程」章节，系统学习项目结构、manifest、模板语法与组件。

## 参考
- Vela 官方 · 快速入门 """ + " (https://iot.mi.com/vela/quickapp/zh/guide/start.html)"))

with open(os.path.join(OUT, "js_course.json"), "w", encoding="utf-8") as f:
    json.dump(course, f, ensure_ascii=False, indent=1)

print("JS_COURSE_CHAPTERS", len(course))
