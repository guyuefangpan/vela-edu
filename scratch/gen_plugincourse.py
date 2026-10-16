# -*- coding: utf-8 -*-
"""生成《Vela 插件开发》教学章节：data/plugin_course.json
来源：oronbox.zxor.org/plugins 全站（已抓取清洗）
- 去除 OronBox 自身软件/推广/商店/市场等主观信息
- 每章补充官方 Vela 快应用 @system.* 文档作为权威参考
- 以 OronBox 宿主的插件 SDK 作为可运行的示例实现（其 OronBox 全局对象即宿主能力入口）
"""
import json, os

ROOT = r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51"
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

OFF = "https://iot.mi.com/vela/quickapp/zh"
REF = {
    "components": f"{OFF}/components/",
    "storage": f"{OFF}/features/data/storage.html",
    "file": f"{OFF}/features/data/file.html",
    "fetch": f"{OFF}/features/network/fetch.html",
    "request": f"{OFF}/features/network/request.html",
    "interconnect": f"{OFF}/features/network/interconnect.html",
    "device": f"{OFF}/features/basic/device.html",
    "bluetooth": f"{OFF}/features/system/bluetooth.html",
    "app": f"{OFF}/features/basic/app.html",
    "router": f"{OFF}/features/basic/router.html",
    "sensor": f"{OFF}/features/system/sensor.html",
    "features": f"{OFF}/features/",
    "guide": f"{OFF}/guide/",
    "tools": f"{OFF}/tools/",
    "zml": "https://zepp-health.github.io/zml/zh/getting-started",
}

def ref(label, url):
    return f"- 权威参考（Vela 官方）：[{label}]({url})"

def box(title, body):
    return f"> **{title}**　{body}"

course = []

# ---------------------------------------------------------------------------
course.append({
"slug": "overview",
"title": "插件开发概述",
"md": f"""# 插件开发概述

> **本节要点**　插件是运行在 Vela 设备「插件宿主（Host）」之上的扩展程序：以清单 `manifest.json` 描述自身、在独立沙箱中执行、通过宿主暴露的能力接口调用设备/文件/网络/应用间通信等。本教程以 OronBox 宿主的插件 SDK 作为**可运行的示例实现**（其全局对象 `OronBox` 即宿主能力入口）；不同宿主对全局对象的命名可能不同，但「清单驱动 + 沙箱运行时 + 权限声明 + 组件化 UI」这套插件模型是通用的。插件调用的每一项底层能力，均对应 Vela 官方快应用的 `@system.*` 接口（见各章「权威参考」）。

## 什么是插件

插件是**第三方代码**，在宿主提供的**独立沙箱**中运行，可以调用设备、文件系统、网络、应用间通信等接口。它不像快应用那样自带完整运行环境，而是寄生在宿主应用之内，由宿主统一调度权限与生命周期。

- 插件以 `.obp` 文件分发——本质是 **ZIP 压缩包**，根目录必须包含 `manifest.json`。
- 插件入口是一个全局函数 `activate(plugin)`，宿主在加载插件时调用它。
- 插件界面由宿主的 UI 模块以**组件树**方式渲染，而不是终端输出。

> ⚠️ 插件是第三方代码，**安装前请核对来源**。插件运行在沙箱中，但仍拥有你授予的权限——权限越小越安全。

## 最小插件

一个最小的 JS 插件只需要两个文件。

`manifest.json`：

```json
{{
  "api_level": 1,
  "id": "dev.example.hello",
  "name": "Hello",
  "version": "1.0.0",
  "author": "you",
  "runtime": "js",
  "entry": "main.js",
  "permissions": []
}}
```

`main.js`：

```js
// 插件加载后宿主会自动调用 activate
globalThis.activate = async (plugin) => {{
  let count = 0;

  const {{ Column, Text, Button }} = OronBox.ui;
  const render = () => OronBox.ui.render(
    Column({{ gap: 12, padding: 16 }}, [
      Text(`Count: ${{count}}`),
      Button('+1', {{
        onClick: OronBox.ui.action(() => count++, render),
      }}),
    ]),
  );

  await render();
}};
```

入口是全局函数 `activate(plugin)`，`plugin` 为 `{{id, name, version, runtimeVersion}}`。

界面用 `OronBox.ui.render()` 渲染组件树；组件事件直接传函数，异步状态变更用 `OronBox.ui.action(fn, render)`，`render()` 返回 `OronBox.ui.render()` 的 Promise。

## 打包与导入

把包内容压缩成 `.obp`：

```bash
zip hello.obp manifest.json main.js icon.png
```

然后通过宿主应用的**导入入口**选择 `hello.obp` 即可安装。安装后打开插件，你会看到界面上的计数按钮——插件的界面就是这些组件树，而不是终端输出。

## 小结

- 插件 = 清单 + 沙箱运行时 + 宿主能力接口；`.obp` 即 ZIP。
- 入口函数 `activate` 由宿主在加载时调用。
- UI 用组件树渲染，事件回调传函数，异步变更用 `action(fn, render)`。
- 下一步：阅读「包格式与 manifest」「运行时与沙箱」「权限模型」三章，建立完整心智模型。

{ref("Vela 快应用官方文档总入口", REF["guide"])}
{ref("Vela 官方组件库（插件 UI 的底层对应）", REF["components"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "manifest",
"title": "包格式与 manifest.json",
"md": f"""# 包格式与 manifest.json

> **本节要点**　`.obp` 是 ZIP 压缩包，根目录必须含 `manifest.json`；清单声明了插件的身份、入口、运行时与权限。解析器对包体积、文件数、路径安全性有强制限制。掌握字段含义是写出「能被宿主接受」的插件的第一步。

最小清单示例：

```json
{{
  "api_level": 1,
  "id": "dev.example.hello",
  "name": "Hello",
  "version": "1.0.0",
  "runtime": "js",
  "entry": "main.js",
  "permissions": ["ui"]
}}
```

## 包格式

`.obp` 是 ZIP 压缩包，根目录必须包含 `manifest.json`。入口文件和图标按 manifest 声明引用，其余文件可组织在任意子目录，运行时通过文件接口访问。

解析时强制校验：

| 限制项 | 值 |
| --- | --- |
| 压缩包大小 | ≤ 32 MiB |
| 单个文件大小 | ≤ 8 MiB |
| 展开后总大小 | ≤ 64 MiB |
| 文件数量 | ≤ 4096 |
| 路径安全 | 禁止 `..`、绝对路径、冒号与 NUL，统一 `/` 分隔 |

## manifest 字段

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `api_level` | 是 | 目前必须为 `1`；缺失（按 0 处理）或其它值直接拒绝 |
| `id` | 是（legacy 除外） | 如 `dev.example.hello`，小写字母开头，至少一个 `.` 或 `-` 分隔符，后续段可含连字符 |
| `name` | 是 | 插件名称 |
| `version` | 是 | 版本号 |
| `runtime` | 否 | `js` / `wasm` / `hybrid`；缺省视为 legacy，不存在的值会被拒绝 |
| `entry` | 否 | 入口文件，默认 `main.js` |
| `permissions` | 否 | 权限列表，仅允许下方 8 项（见「权限模型」） |
| `icon` | 否 | 图标路径 |
| `author` / `description` / `website` | 否 | 元信息 |

## 入口文件校验

- `runtime: "wasm"` 时，`entry` 必须是 `.wasm` 文件且带合法的 WASM 头。
- `runtime: "js"` / `"hybrid"` 时，`entry` 必须是 `.js` / `.mjs` / `.cjs` 文件。
- legacy 插件没有 `id`，安装时由 `name` 生成固定 ID。

## 小结

- 清单是插件与宿主之间的「契约」：身份、入口、运行时、权限缺一不可。
- `api_level` 必须声明为 `1`；`runtime` 决定沙箱类型。
- 包体积/文件数/路径都有硬限制，开发时尽早注意资源大小。

{ref("Vela 快应用项目与 manifest 概念（官方 guide）", REF["guide"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "runtime",
"title": "运行时与沙箱",
"md": f"""# 运行时与沙箱

> **本节要点**　`runtime` 字段决定插件用哪种引擎执行：js（QuickJS 沙箱）、wasm（WASI 沙箱）、hybrid（JS + WASM）、legacy（旧版兼容）。宿主通过**冻结的全局对象 `OronBox`** 暴露能力；调用受保护接口返回 Promise。插件有自己隔离的文件系统（四根目录），二进制统一用 base64 传递。

## 运行时类型

| `runtime` | 执行引擎 | 入口文件 |
| --- | --- | --- |
| `js` | 推荐；QuickJS 沙箱执行 JavaScript | `.js` / `.mjs` / `.cjs` |
| `wasm` | WebAssembly 插件，经 WASI 沙箱调用宿主能力 | `.wasm` |
| `hybrid` | JS 入口 + 同时加载 WASM 模块 | `.js`（缺省）与 WASM |
| legacy | 不写 `runtime` 字段的旧版兼容格式 | JS |

- `js` 插件：入口 JS 在 QuickJS 沙箱中执行，宿主能力通过 `OronBox` 全局对象暴露。
- `wasm` 插件：入口 `.wasm` 在 WASI 沙箱中执行，宿主调用走 wasm 导入函数；**没有** `setTimeout` / `setInterval` 等定时器接口。
- `hybrid` 插件：入口 JS 与 `js` 相同，但额外允许通过 `OronBox.wasm` 加载并调用 `.wasm` 模块。
- legacy 插件：入口仍由 JS 引擎执行，但注入的是旧版兼容层（全局对象为旧名而非 `OronBox`）。

## 沙箱与文件系统

插件存储按虚拟路径暴露为四个根目录：

| 根路径 | 区域 | 读写性 |
| --- | --- | --- |
| `/plugin` | package | 只读（安装时的包内容，含入口与资源文件） |
| `/data` | data | 可写 |
| `/cache` | cache | 可写 |
| `/temp` | temporary | 可写 |

`/plugin` 的只读性由宿主强制执行。WASI 沙箱只开放文件系统与标准输入输出能力，没有网络、时钟、环境变量等其他 WASI 能力。

## 宿主 API：`OronBox` 全局对象

JS 运行时（`js` / `hybrid`）注入一个冻结的全局对象 `OronBox`（不可写、不可配置），包含下列命名空间：

| 命名空间 | 主要方法 |
| --- | --- |
| `storage` | `get` `set` `remove` `clear` |
| `file` | `read` `write` `list` `stat` `mkdir` `copy` `move` `remove` `pick` `unload` |
| `network` | `fetch` `download` |
| `interconnect` | `send` `onMessage` |
| `provider` | `register` `unregister` |
| `device` | `list` `info` `connect` `disconnect` `apps.list` `apps.launch` `apps.uninstall` `install` |
| `protocol` | `send` `request` `observe` |
| `os` | `arch` `hostname` `locale` `platform` `version` `language` `appearance` `timezone` |
| `watchface` | `list` `set` |
| `appside` | `list` `start` `stop` `send` `inject` `sessions` `events` `clearEvents` `attach` |
| `ui` | `render` `update` `openPage` `openExternal` `getRenderSize` `dialog` `callback` `action` + 节点构造器 |
| `wasm` | `load` |

## 调用语义

宿主分发是异步的，JS 侧的返回值语义：

- 宿主返回非 Promise 的值：调用立即返回该值。
- 宿主返回 Promise：JS 侧得到 Promise，`.then` / `await` 可取得结果。

需要等待的结果（如 `network.fetch`、`device.connect`、`file.read`、`protocol.request`、`ui.dialog`）在 JS 侧都是 Promise。

## 调用示例

```js
// 宿主能力多为异步：用 await 取结果
globalThis.activate = async () => {{
  const info = await OronBox.device.info();
  const text = await OronBox.network.fetch('https://example.com/hello')
    .then(r => atob(r.body));
  await OronBox.storage.set('lastDevice', info.name);
  await OronBox.ui.render(OronBox.ui.Text(`${{info.name}}: ${{text}}`));
}};
```

## 二进制数据编码

宿主与 JS 之间不直接传二进制，统一用 **base64** 字符串，个别场景用 UTF-8 文本：

- `file.read`：默认返回 base64；`options.encoding` 为 `utf8`/`utf-8`/`text` 时返回解码后的字符串，支持 `offset`/`length` 切片。
- `file.write`：`data` 默认按 base64 解码；文本时按 UTF-8 编码，`append` 为 true 时追加。
- `protocol.request`：返回 `{{data: base64}}`（原始协议响应）。
- `protocol.send`：`data` 按 base64 解码为原始字节发送。
- `network.fetch`：响应返回 `{{status, headers, contentType, body}}`，其中 `body` 是 base64；响应体超过 16 MiB 时报错，需改用 `network.download`。
- `appside.send` / `inject`：`hexData` 为十六进制字符串。

## 定时器

`setTimeout` / `setInterval` / `clearTimeout` / `clearInterval` 在 JS 运行时中可用；定时器回调抛出的错误只记日志，不影响运行时。WASM 插件没有注入 JS 引导，因此没有定时器接口。

## 生命周期与错误处理

- **启动**：首次打开插件、触发 UI 回调或宿主调用插件时才创建运行时；入口脚本可定义可选的 `activate(plugin)` 启动函数，启动时会被调用。
- **关闭**（卸载、清除数据、安全模式、宿主关闭）：取消所有定时器，销毁运行时与 WASM 实例，同步沙箱数据。
- 未捕获的 Promise 拒绝会上报日志；可识别的瞬时错误（设备未就绪、传输断开、超时）只记日志。
- 不可恢复错误会记录插件失败状态，UI 层弹出错误对话框，提供「卸载 / 清除数据 / 启用安全模式」操作。

## 小结

- 四种运行时对应四种执行引擎；日常开发首选 `js`。
- 所有宿主能力挂在冻结的全局对象 `OronBox` 上，调用多为异步（返回 Promise）。
- 插件有隔离文件系统（四根目录），二进制一律 base64。

{ref("Vela 快应用框架与生命周期（官方 guide）", REF["guide"])}
{ref("Vela 官方组件库（UI 树底层对应）", REF["components"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "permissions",
"title": "权限模型",
"md": f"""# 权限模型

> **本节要点**　插件的权限分两层：**声明层**（manifest 的 `permissions` 白名单）与**运行时授权层**（每次调用受保护接口时按用户决策放行）。白名单只接受 8 个能力；授权有「允许本次 / 本次运行中 / 始终允许 / 拒绝」四档，并按风险等级决定是否需要询问。

## 能力白名单

`permissions` 只接受以下 8 个能力，其他值会导致包被拒绝：

| 能力 | 含义 | 受控操作 |
| --- | --- | --- |
| `ui` | 渲染界面、打开页面、对话框与外部链接 | `ui.render` `ui.openPage` `ui.openExternal` `ui.dialog` `ui.getRenderSize` |
| `file` | 读写插件沙箱内的文件 | `file.read` `file.write` `file.list` `file.stat` `file.mkdir` `file.copy` `file.move` `file.remove` `file.pick` `file.unload` |
| `network` | 发起 HTTP/HTTPS 请求或下载到沙箱 | `network.fetch` `network.download` |
| `interconnect` | 与设备上运行的应用收发消息 | `interconnect.send` `interconnect.observe` |
| `provider` | 注册/注销资源源 | `provider.register` `provider.unregister` |
| `device` | 读取已配对设备、连接/断开、安装/启动/卸载应用、切换表盘 | `device.*` `watchface.*` |
| `protocol` | 监听或发送原始协议帧 | `protocol.observe` `protocol.send` `protocol.request` |
| `appside` | 管理伴生服务生命周期、注入模拟消息 | `appside.*` |

不需要权限声明的接口：`log.*`（日志）、`storage.*`（键值配置）、`os.*`（系统信息）；`wasm.*` 只对 `hybrid` 运行时开放。

## 授权请求流程

每次插件调用受保护的宿主接口，都会先经过授权检查：

1. 校验能力是否已**声明**：未声明却调用，直接抛错 `permission_not_declared`，不弹窗。
2. 低风险操作直接放行，不询问。
3. 已存在授权（本次运行中或始终允许）直接放行。
4. 否则弹出授权请求，等待用户选择。
5. 同一授权点的并发请求会合并，只弹一次。

## 四档决策

| 决策 | 行为 |
| --- | --- |
| 允许本次 | 仅当前这次调用放行，不记录 |
| 本次运行中 | 在插件运行时存续期间不再询问 |
| 始终允许 | 写入持久授权，之后不再询问 |
| 拒绝 | 抛错 `permission_denied` |

弹窗不可通过点击外部关闭；关闭或未给出有效决策时按「拒绝」处理。「本次运行中」的授权在关闭插件、更新/卸载、开启安全模式时结束。

## 风险等级

每个受控操作都有风险等级（`low` / `medium` / `high`）：低风险免询问直接放行；中、高风险需用户授权。

- **低**：`ui.render` `ui.update` `ui.openPage` `ui.getRenderSize`；`file.read/write/list/stat/mkdir/copy/move/remove`
- **中**：`ui.dialog` `ui.openExternal`；`file.pick` `file.unload`；`network.*`；`interconnect.*`；`provider.*`；`device.list` `device.info` `device.apps.list` `watchface.list`；`protocol.observe`；`appside.list/sessions/events`
- **高**：`device.connect/disconnect/apps.launch/apps.uninstall/install` `watchface.set`；`protocol.send/request`；`appside.start/stop/send/inject/clearEvents` 及 `appside.zml.*`

## 授权粒度

授权精确到「能力 + 操作 + 目标」：

| 操作类别 | 作用域示例 |
| --- | --- |
| `network.*` `ui.openExternal` | 目标域名/主机名 |
| `interconnect.send` | 目标包名 |
| `device.connect/disconnect` | 设备地址 |
| `device.info/apps.list/install` `watchface.list` `protocol.*` | 当前设备名 |
| `device.apps.launch/uninstall` | 应用包名 |
| `watchface.set` | 表盘 ID |
| `appside.*` | 伴生服务应用 ID |

其余操作（如文件读写）不区分作用域，授权键为「能力:操作」。

## 授权持久化与撤销

- 「始终允许」会持久保存，插件更新后不丢失。
- 「本次运行中」只存在内存，运行时关闭即清空。
- 清除数据/卸载会清空授权。
- **安全模式**是全局开关：开启后立即关闭所有插件，调用时报错 `Plugins are disabled in safe mode`；开关状态持久化。

## 小结

- 先声明、后授权：没在 `permissions` 里写的能力，调用即报错。
- 给用户尽量少的权限；高风险操作会弹窗并标注风险。
- 「始终允许」跨更新保留，「本次运行中」随运行时结束清空。

{ref("Vela 官方 JS 接口总览（能力概念对应）", REF["features"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "ui",
"title": "UI 渲染与组件",
"md": f"""# UI 渲染与组件

> **本节要点**　插件通过**组件树**渲染界面，每个节点是 `{{type, props, children}}` 对象。用 `ui.render(tree)` 内联渲染、`ui.openPage(tree)` 打开全屏页。异步操作先等完成再重渲染；`ui.action(fn, render)` 是「执行 fn 后重渲染」的便捷封装。下面给出全部组件与通用属性。

## 渲染

```js
OronBox.ui.render(tree);      // 在插件详情页内联渲染
OronBox.ui.openPage(tree);    // 打开全屏页面
```

两者都接受一个根节点（通常是 `Column`）。异步操作应先等待完成，再重渲染界面。

`OronBox.ui.action(fn, render)` 返回包装函数：调用它时先执行 `fn`，完成后调用 `render`；异步完成前手动渲染会显示过期状态。

```js
const save = OronBox.ui.action(async () => {{
  await OronBox.storage.set('key', 'value');
  status = 'Saved';
}}, render);
```

- `update(nodes)`：`render` 的别名（兼容）。
- `openExternal(url)`：用系统浏览器打开外部链接，返回 `{{opened: true}}`。
- `callback(fn)`：注册回调并返回回调 ID；`action` 是它的便捷封装。
- `getRenderSize()`：返回 `{{width, height}}`。
- `dialog({{title, message, buttons}})`：原生对话框，返回 `{{clickedBtnId}}` 或 `{{cancelled: true}}`。

## 布局组件

```js
const {{ Column, Row, Spacer, Text }} = OronBox.ui;
Column({{ gap: 12, padding: 16, align: 'start' }}, [
  Text('Title', {{ size: 20, weight: 'bold' }}),
  Row({{ gap: 8 }}, [Text('Left'), Spacer(), Text('Right')]),
]);
```

| 组件 | 关键 props |
| --- | --- |
| `Column` / `Row` | `gap`(间距) `padding`(内边距) `align`(`start`/`center`/`end`) |
| `LazyColumn` | 可滚动列 `gap` |
| `Spacer` | 固定 16px 占位；在 `Row` 内弹性撑满，在 `Column` 内为固定间距 |
| `Text` | `value` `size` `color`(`#rgb`/`#rrggbb`) `weight`(`bold`/`medium`) `align` `maxLines` |
| `HtmlDocument` | `value`（HTML 片段，用于富文本） |

## 交互组件

```js
Button('Tap', {{ onClick: () => save() }});
Button('Primary', {{ primary: true, onClick: submit }});
TextField({{ value: 'default', placeholder: 'Input...', multiline: true, onChange: v => save(v) }});
Switch(true, {{ onChange: v => save('on', v) }});
Checkbox(false, {{ label: 'Remember me', onChange: v => save('remember', v) }});
Slider(0.5, {{ min: 0, max: 1, onChange: v => save('volume', v) }});
Dropdown('A', {{ options: ['A','B','C'], onChange: v => save('opt', v) }});
```

## 展示与容器组件

```js
Image('/data/icon.png', {{ width: 64, height: 64, radius: 12, fit: 'cover' }});
Divider({{ thickness: 1 }});
Badge({{ count: 3 }}, Button('Messages'));
Card({{}}, Row({{ gap: 8 }}, [Image('/plugin/icon.png', {{ width: 32 }}), Text('Content')]));
Modal({{ title: 'Settings', onDismiss: refresh }}, Text('Modal body'));
Tooltip({{ text: 'Help' }}, Text('Hover me'));
```

- `Image`：图片从插件沙箱路径读取，单张 ≤ 4 MiB；`fit` 支持 `cover`/`contain`/`fill`/`fitWidth`/`fitHeight`/`none`/`scaleDown`。
- `Tabs`：`tabs`(`[{{id,label}}]`)、`onChange`(选中 id)、`scrollable`；`TabContent` 的 `tabId` 等于 `activeId` 时才显示。

## 进度与通用属性

```js
CircularProgress({{ size: 24 }});
LinearProgress(45, {{ max: 100 }});
```

所有组件都支持通用属性：`visible`(false 不渲染)、`disabled`(拦截指针)、`opacity`(0–1)、`padding`(四周内边距)。

## 完整示例：设置页

```js
globalThis.activate = async (plugin) => {{
  const {{ Column, Row, Card, Text, Button, Switch, Slider, Dropdown, Divider, Spacer }} = OronBox.ui;
  let notify = true, brightness = 0.5, theme = 'auto';
  const submit = () => {{ /* 保存设置 */ }};

  const render = () => {{
    OronBox.ui.render(
      Column({{ padding: 16, gap: 12 }}, [
        Text('Settings', {{ size: 22, weight: 'bold' }}),
        Card({{}}, Column({{ gap: 8 }}, [
          Row({{ gap: 8 }}, [Text('Notifications'), Spacer(), Switch(notify, {{ onChange: v => {{ notify = v; render(); }} }})]),
          Divider(),
          Row({{ gap: 8 }}, [Text('Brightness'), Slider(brightness, {{ onChange: v => {{ brightness = v; render(); }} }})]),
          Divider(),
          Row({{ gap: 8 }}, [Text('Theme'), Spacer(), Dropdown(theme, {{ options: ['auto','light','dark'], onChange: v => {{ theme = v; render(); }} }})]),
        ])),
        Row({{ gap: 12 }}, [Button('Cancel'), Button('Save', {{ primary: true, onClick: submit }})]),
      ])
    );
  }};
  render();
}};
```

## 小结

- UI = 组件树；根通常是 `Column`。事件直接传函数，异步变更用 `action(fn, render)`。
- 组件分布局、交互、展示/容器、进度四类；通用属性 `visible/disabled/opacity/padding` 全支持。
- 图片从沙箱路径读取，注意 4 MiB 限制。

{ref("Vela 官方组件库（div/text/image/input/switch/slider…）", REF["components"])}
{ref("Vela 组件通用属性与事件（官方）", f"{OFF}/components/general/")}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "storage",
"title": "键值存储 Storage",
"md": f"""# 键值存储 Storage

> **本节要点**　`storage` 是持久化的键值对存储，卸载插件时一并清除；值可以是任意可 JSON 序列化的数据。适合保存配置、计数、最近访问等小数据。

## 方法

```js
const value = await OronBox.storage.get('lastVisit');
// 返回存储的值，从未设置过则为 undefined

await OronBox.storage.set('lastVisit', new Date().toISOString());
await OronBox.storage.set('theme', 'dark');
await OronBox.storage.set('prefs', {{ fontSize: 14, lineHeight: 1.5 }});

await OronBox.storage.remove('theme');
await OronBox.storage.clear();
```

## 完整示例：访问记录

```js
globalThis.activate = async (plugin) => {{
  let lastVisit = (await OronBox.storage.get('lastVisit')) || 'Never';
  let visitCount = (await OronBox.storage.get('visitCount')) || 0;
  const {{ Column, Text, Button }} = OronBox.ui;

  const recordVisit = async () => {{
    visitCount++;
    lastVisit = new Date().toLocaleString();
    await OronBox.storage.set('visitCount', visitCount);
    await OronBox.storage.set('lastVisit', lastVisit);
  }};

  const render = () => OronBox.ui.render(
    Column({{ gap: 8 }}, [
      Text(`Last visit: ${{lastVisit}}`),
      Text(`Visits: ${{visitCount}}`),
      Button('Record visit', {{ onClick: OronBox.ui.action(recordVisit, render) }}),
    ]),
  );
  render();
}};
```

## 小结

- `storage` 不需要权限声明，也不受沙箱文件系统限制。
- 值任意 JSON 序列化；卸载插件时清空。
- 大文件/二进制请用 `file` 能力。

{ref("Vela 官方数据存储 storage", REF["storage"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "file",
"title": "文件系统 File",
"md": f"""# 文件系统 File

> **本节要点**　插件有独立的沙箱文件系统，分四个区域（/plugin 只读，/data、/cache、/temp 可写）。二进制统一 base64。需声明 `file` 权限。

## 四区域

| 区域 | 前缀 | 权限 |
| --- | --- | --- |
| 包内 | `/plugin` | 只读 |
| 数据 | `/data` | 读写（持久） |
| 缓存 | `/cache` | 读写（可能被清） |
| 临时 | `/temp` | 读写（重启清空） |

## 读写

```js
// UTF-8 文本
const text = await OronBox.file.read('/data/note.txt', {{ encoding: 'utf8' }});
// Base64 二进制
const base64 = await OronBox.file.read('/data/image.png', {{ encoding: 'base64' }});
// 切片
const chunk = await OronBox.file.read('/data/large.bin', {{ encoding: 'base64', offset: 1024, length: 512 }});

await OronBox.file.write('/data/note.txt', 'Hello World', {{ encoding: 'utf8' }});
await OronBox.file.write('/data/image.png', base64data, {{ encoding: 'base64' }});
await OronBox.file.write('/data/log.txt', 'new line\\n', {{ encoding: 'utf8', append: true }});
```

## 目录操作

```js
const entries = await OronBox.file.list('/data');   // [{{name,path,size,isDirectory}}]
const stat = await OronBox.file.stat('/data/note.txt');
await OronBox.file.mkdir('/data/subdir');
await OronBox.file.copy('/data/a.txt', '/data/b.txt');
await OronBox.file.move('/temp/a.txt', '/data/a.txt');
await OronBox.file.remove('/data/old.txt');
```

## 与系统文件交互

```js
const picked = await OronBox.file.pick({{}});   // 打开系统选择器，导入 /temp/picker/...
// picked = {{ name, path, size }}；用户取消返回 null
const result = await OronBox.file.unload('/data/report.pdf', {{ suggestedName: 'Report.pdf' }});
// result = {{ exported: true, name }}
```

## 小结

- 用 `/data` 存持久文件、`/cache` 存可重建、`/temp` 存临时。
- `read`/`write` 默认 base64；文本用 `encoding: 'utf8'`。
- `pick`/`unload` 为中风险，需授权。

{ref("Vela 官方文件存储 file", REF["file"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "network",
"title": "网络请求 Network",
"md": f"""# 网络请求 Network

> **本节要点**　通过宿主发起 HTTP/HTTPS 请求，仅支持 `http://` 与 `https://`。`fetch` 响应体上限 16 MiB，更大的文件用 `download` 流式落盘。需声明 `network` 权限（中风险）。

## fetch

```js
const resp = await OronBox.network.fetch('https://httpbin.org/json', {{
  method: 'GET',
  headers: {{ 'Accept': 'application/json' }},
  body: base64data,   // 可选，Base64 请求体
}});
// resp = {{ status, headers, contentType, body: '<base64>' }}

const text = atob(resp.body);
const json = JSON.parse(text);
```

## download

```js
const result = await OronBox.network.download(
  'https://example.com/file.bin', '/data/file.bin',
  {{ method: 'GET', headers: {{}} }}
);
// result = {{ path: '/data/file.bin', bytesWritten: 1048576, status: 200 }}
```

## 完整示例：JSON 抓取

```js
globalThis.activate = async (plugin) => {{
  let url = 'https://httpbin.org/json';
  let result = 'Enter a URL and tap Fetch';
  const {{ Column, Text, TextField, Button }} = OronBox.ui;

  const fetchJson = async () => {{
    try {{
      const resp = await OronBox.network.fetch(url);
      const body = resp.body ? atob(resp.body) : '';
      try {{ result = JSON.stringify(JSON.parse(body), null, 2); }}
      catch (_) {{ result = body.substring(0, 500); }}
    }} catch (e) {{ result = `Error: ${{e.message}}`; }}
  }};

  const render = () => OronBox.ui.render(
    Column({{ gap: 8 }}, [
      TextField({{ value: url, onChange: v => {{ url = v; }} }}),
      Button('Fetch', {{ onClick: OronBox.ui.action(fetchJson, render) }}),
      Text(result),
    ]),
  );
  render();
}};
```

## 小结

- 响应 `body` 是 base64，用 `atob` 解码。
- 超过 16 MiB 用 `download` 直接写沙箱文件。
- 部分设备（如某些手环）按官方说明可能不支持网络请求，真机调试时注意。

{ref("Vela 官方数据请求 fetch", REF["fetch"])}
{ref("Vela 官方下载 request", REF["request"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "device",
"title": "设备管理 Device",
"md": f"""# 设备管理 Device

> **本节要点**　管理已配对设备：列出、连接、断开、应用管理、安装资源（快应用/表盘/固件）。除 `connect` 外各方法可省略 `deviceId` 作用于当前活动设备。需声明 `device` 权限；写操作为高风险。

## 设备列表与连接

```js
const devices = await OronBox.device.list();
// [{{ id, name, connectType, connected, current }}]

const info = await OronBox.device.info();
// {{ id, name, model, firmwareVersion, battery }}

await OronBox.device.connect('D4:17:61:14:18:6E');
await OronBox.device.disconnect();
```

## 应用管理

```js
const apps = await OronBox.device.apps.list();
// [{{ packageName, name, versionCode, canRemove }}]

await OronBox.device.apps.launch('com.example.app', {{ page: '' }});
await OronBox.device.apps.uninstall('com.example.app');
```

## 安装资源

```js
await OronBox.device.install('/data/app.bin', {{ type: 'app', fileName: 'app.bin' }});
await OronBox.device.install('/data/watchface.bin', {{ type: 'watchface', fileName: 'watchface.bin' }});
await OronBox.device.install('/data/firmware.fw', {{ type: 'firmware', fileName: 'firmware.fw' }});
// type: app | watchface | firmware
```

## 小结

- 只读操作（list/info/apps.list）中风险；连接/安装/启动/卸载高风险，按设备授权。
- `install` 可装快应用、表盘、固件三类资源。

{ref("Vela 官方设备信息 device", REF["device"])}
{ref("Vela 官方蓝牙 bluetooth（底层连接能力）", REF["bluetooth"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "interconnect",
"title": "应用间通信 Interconnect",
"md": f"""# 应用间通信 Interconnect

> **本节要点**　按包名向设备上的目标应用（快应用等）发送文本消息，或接收来自应用的消息。宿主只提供传输基础设施（文本消息，无文件传输/分片/确认协议）。需声明 `interconnect` 权限。

## 发送与接收

```js
await OronBox.interconnect.send('com.example.target', 'hello from plugin');

const stop = await OronBox.interconnect.onMessage(({{ packageName, data }}) => {{
  console.info(`Received from ${{packageName}}: ${{data}}`);
}});
await stop();   // 停止监听
```

## 完整示例：消息器

```js
globalThis.activate = async (plugin) => {{
  let target = '', message = '', received = '';
  const {{ Column, Text, TextField, Button }} = OronBox.ui;

  OronBox.interconnect.onMessage(({{ packageName, data }}) => {{
    received = `[${{packageName}}] ${{data}}`;
    render();
  }});

  const render = () => OronBox.ui.render(
    Column({{ gap: 8 }}, [
      TextField({{ value: target, placeholder: 'Target package', onChange: v => {{ target = v; }} }}),
      TextField({{ value: message, placeholder: 'Message', onChange: v => {{ message = v; }} }}),
      Button('Send', {{ onClick: () => OronBox.interconnect.send(target, message) }}),
      Text(received || 'Waiting...'),
    ]),
  );
  render();
}};
```

## 小结

- 仅传输文本；需要结构化数据请自行 JSON 序列化。
- 界面组件同时需要 `ui` 权限；示例 manifest 需声明 `interconnect` 与 `ui`。

{ref("Vela 官方设备通信 interconnect", REF["interconnect"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "provider",
"title": "资源源注册 Provider",
"md": f"""# 资源源注册 Provider

> **本节要点**　插件可把自己注册为「资源源」，向资源库提供可下载资源（社区仓库、私有目录等场景）。需声明 `provider` 权限（中风险）。

## register / unregister

```js
await OronBox.provider.register({{
  id: 'org.example.source',     // 唯一反向域名 ID
  name: 'Example Source',       // 显示名称
  categories: async () => [     // 可选分区
    {{ id: 'watch', name: 'Watchfaces' }},
    {{ id: 'app', name: 'Apps' }},
  ],
  query: async (query) => ({{   // 搜索/列表
    items: [{{ id: 'res-001', name: 'Classic Watchface', type: 'watchface',
               author: 'Author', version: '1.0', paidType: 'free' }}],
    hasMore: false, total: 1,
  }}),
  detail: async ({{ id }}) => ({{ id, name: 'Classic Watchface', type: 'watchface',
    version: '1.0', paidType: 'free', authors: ['Author'], description: '...',
    supportedDevices: [{{ name: 'Xiaomi Smart Band 9 Pro', codename: 'n67', platform: 'vela' }}],
    files: [{{ id: 'f1', name: 'file.bin', size: 102400, fileName: 'file.bin' }}],
    content: {{ format: 'plainText', value: 'Details...' }} }}),
  download: async ({{ id, fileId, targetDevice }}) =>
    ({{ path: '/cache/file.bin', fileName: 'file.bin' }}),
}});

await OronBox.provider.unregister('org.example.source');
```

## 小结

- `definition` 提供 `categories`/`query`/`detail`/`download` 四个异步回调。
- 资源 `type`：`quickApp` | `watchface` | `firmware` | `fontpack` | `iconpack`。

{ref("Vela 官方 JS 接口总览（资源/扩展能力概念）", REF["features"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "protocol",
"title": "原始协议 Protocol",
"md": f"""# 原始协议 Protocol

> **本节要点**　在当前设备上读写**原始蓝牙协议帧**，数据用 Base64 编码。需声明 `protocol` 权限；`observe` 中风险，`send`/`request` 高风险。

> ⚠️ 原始协议操作可能干扰正常的设备通信，请仅在调试/确需时启用。

## 发送与请求

```js
await OronBox.protocol.send(btoa('\\x01\\x00'));

const response = await OronBox.protocol.request(btoa('\\x01\\x00'));
```

## 被动观察

```js
const stop = await OronBox.protocol.observe(({{ data }}) => {{
  // data 是 Base64 编码的原始字节
  console.info('Protocol data:', data);
}});
await stop();
```

## 完整示例：协议监视器

```js
globalThis.activate = async (plugin) => {{
  let hexInput = '', output = '';
  const {{ Column, Text, TextField, Button }} = OronBox.ui;

  OronBox.protocol.observe(({{ data }}) => {{
    const raw = atob(data);
    let hex = '';
    for (let i = 0; i < raw.length; i++) hex += raw.charCodeAt(i).toString(16).padStart(2, '0');
    output = `Received: ${{hex}}`;
    render();
  }});

  const sendHex = async () => {{
    const bytes = hexInput.match(/../g)
      ?.map(b => String.fromCharCode(parseInt(b, 16))).join('') ?? '';
    await OronBox.protocol.send(btoa(bytes));
    output = `Sent: ${{bytes.length}} bytes`;
  }};

  const render = () => OronBox.ui.render(
    Column({{ gap: 8 }}, [
      TextField({{ value: hexInput, onChange: v => {{ hexInput = v; }} }}),
      Button('Send Hex', {{ onClick: OronBox.ui.action(sendHex, render) }}),
      Text(output || 'Waiting...'),
    ]),
  );
  render();
}};
```

## 小结

- 所有字节走 base64；用 `btoa`/`atob` 与十六进制互转。
- `observe` 只读、不打断正常分发；`send`/`request` 会真正写入设备。

{ref("Vela 官方蓝牙 bluetooth（原始协议底层能力）", REF["bluetooth"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "os",
"title": "系统信息 OS",
"md": f"""# 系统信息 OS

> **本节要点**　获取宿主环境信息（平台、架构、语言、时区、深浅色等）。`os.*` **不需要权限声明**。

## 方法

```js
const arch       = await OronBox.os.arch();       // 'x64'|'arm64'|'x86'|'riscv64'|'arm'|'unknown'
const hostname   = await OronBox.os.hostname();    // 仅桌面端
const locale     = await OronBox.os.locale();      // 'en_US'|'zh_CN'|...
const platform   = await OronBox.os.platform();    // 'linux'|'macos'|'windows'|'android'|'ios'
const version    = await OronBox.os.version();     // 仅桌面端
const language   = await OronBox.os.language();    // 'en'|'zh'|...
const appearance = await OronBox.os.appearance();  // 'light'|'dark'
const timezone   = await OronBox.os.timezone();    // UTC 偏移分钟，如 480 = UTC+8
```

## 完整示例

```js
globalThis.activate = async (plugin) => {{
  const lines = [
    `Platform: ${{await OronBox.os.platform()}}`,
    `Arch: ${{await OronBox.os.arch()}}`,
    `Language: ${{await OronBox.os.language()}}`,
    `Appearance: ${{await OronBox.os.appearance()}}`,
    `Timezone: UTC${{await OronBox.os.timezone() >= 0 ? '+' : ''}}${{await OronBox.os.timezone()/60}}h`,
  ];
  await OronBox.ui.render(OronBox.ui.Text(lines.join('\\n')));
}};
```

## 小结

- `os.*` 免权限，适合做环境自适应（如跟随深浅色）。
- 设备相关（型号/电量/蓝牙）请用 `device` 能力。

{ref("Vela 官方设备信息 device", REF["device"])}
{ref("Vela 官方网络信息 network（环境信息概念）", f"{OFF}/features/system/network.html")}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "watchface",
"title": "表盘管理 Watchface",
"md": f"""# 表盘管理 Watchface

> **本节要点**　列出当前设备的表盘并切换。需声明 `device` 权限（`list` 中风险、`set` 高风险）。表盘是 Vela 生态的重要扩展形态，后续本站会单独开设「表盘开发」章节。

## 方法

```js
const watchfaces = await OronBox.watchface.list();
// [{{ id, name, current }}]

await OronBox.watchface.set('67890');
```

## 完整示例：表盘切换器

```js
globalThis.activate = async (plugin) => {{
  let wfList = [], result = 'Tap to list watchfaces';
  const {{ Column, Text, Button }} = OronBox.ui;

  const render = () => {{
    const nodes = [
      Button('List', {{ onClick: OronBox.ui.action(async () => {{
        wfList = await OronBox.watchface.list();
        result = wfList.map(w => `${{w.name}} ${{w.current ? '←active' : ''}}`).join('\\n');
      }}, render) }}),
      Text(result),
    ];
    for (const wf of wfList) {{
      if (wf.current) continue;
      nodes.push(Button(`Switch to ${{wf.name}}`, {{
        onClick: OronBox.ui.action(async () => {{
          await OronBox.watchface.set(wf.id);
          result = `Switched to ${{wf.name}}`;
        }}, render),
      }}));
    }}
    return OronBox.ui.render(Column({{ gap: 8 }}, nodes));
  }};
  render();
}};
```

## 小结

- `list` 只读、`set` 写操作（高风险）。
- 与 `device.install({{type:'watchface'}})` 配合可实现「下载并切换表盘」的完整流程。

{ref("Vela 官方设备信息 device（安装表盘用 install）", REF["device"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "appside",
"title": "伴生服务 AppSide",
"md": f"""# 伴生服务 AppSide

> **本节要点**　管理 ZeppOS 设备的伴生服务（AppSide）：运行在手表小程序旁的远程 JS 执行通道，通过 `messaging.peerSocket` 与小程序实时通信。宿主内置自包含的 ZML 运行时，插件用 `attach()` 绑定到小程序即可使用官方 `BaseSideService` 风格 API。需声明 `appside` 权限。

## ZML 钩子

宿主内置自包含的 ZML AppSide 通信运行时，插件**不需要**自行打包 `@zeppos/zml`；用 `attach()` 把运行时绑定到小程序，即可在钩子里使用官方的 `this.request()` / `this.call()` / `onRequest` / `onCall` API。

```js
globalThis.activate = async () => {{
  const zml = await OronBox.appside.attach({{
    appId: 0x0010ee3b,
    onInit() {{ console.log('ZML App-side initialized'); }},
    async onRun() {{
      const result = await this.request({{ method: 'device.getData', params: {{ type: 'summary' }} }});
      console.log('Watch response:', JSON.stringify(result));
    }},
    onRequest(req, res) {{
      if (req.method === 'plugin.getState') {{ res(null, {{ ready: true }}); return; }}
      res({{ code: 'METHOD_NOT_FOUND', message: `Unknown method: ${{req.method}}` }});
    }},
    onCall(message) {{ console.log('Watch notification:', JSON.stringify(message)); }},
    onDestroy() {{ console.log('ZML App-side stopped'); }},
  }});

  await zml.request({{ method: 'device.getInfo', params: {{}} }});
  await zml.call({{ method: 'settings.changed', params: {{ theme: 'dark' }} }});
}};
```

每个 `appId` 只创建一个伴生服务会话，钩子不能另开蓝牙连接；`request()`/`call()` 仅在手表已连接、设备就绪且小程序已打开伴生服务后可用。

## 方法

```js
const ids = await OronBox.appside.list();          // [0x0010ee3b, ...]
await OronBox.appside.start(0x0010ee3b);           // 启动本地脚本运行时
await OronBox.appside.stop(0x0010ee3b);
await OronBox.appside.send(0x0010ee3b, '0100ff');   // 发送十六进制二进制（需活动会话）
await OronBox.appside.inject(0x0010ee3b, '48656c6c6f'); // 模拟手表消息（调试，不需会话）
const sessions = await OronBox.appside.sessions(); // 活动会话列表
const events = await OronBox.appside.events(0x0010ee3b); // 调试事件日志
await OronBox.appside.clearEvents(0x0010ee3b);
await zml.detach();                                // 移除钩子并释放上下文
```

## 小结

- `appside` 是「插件 ↔ 手表小程序」的双向通道，基于 ZML。
- 只读操作（`list`/`sessions`/`events`）中风险；控制操作高风险。
- `inject` 用于本地调试，不需要真实手表会话。

{ref("ZeppOS ZML 官方文档（伴生服务运行时）", REF["zml"])}
"""
})

# ---------------------------------------------------------------------------
course.append({
"slug": "distribution",
"title": "分发与导入",
"md": f"""# 分发与导入

> **本节要点**　本章去除具体宿主/商店/市场等运营信息，只保留**通用的包与导入机制**：包格式与扩展名、通用导入流程、legacy 兼容、覆盖安装即更新、卸载与数据清理。具体的发布渠道由你所使用的宿主应用决定。

## 包格式与扩展名

`.obp` 是 ZIP 压缩包，根目录必须有 `manifest.json`。解析器按内容识别包，不校验扩展名；常见扩展名约定：

| 扩展名 | 约定 |
| --- | --- |
| `.obp` | 插件包，manifest 含 `runtime` 与 `id` |
| `.abp` | 旧格式，即不含 `runtime` 字段的 legacy 插件 |
| `.zip` | 通用压缩包扩展名，导入与发布都接受 |

包解析与清单校验的限制见「包格式与 manifest.json」一章。

## 通用导入流程

- 通过宿主应用的**导入入口**选择 `.obp` / `.abp` / `.zip` 文件。
- 选择后先本地解析包与清单，弹出安装确认对话框：显示插件名、声明的权限列表；legacy 插件会额外显示旧版兼容警告。
- 确认后执行安装，写入插件存储。

## legacy 兼容机制

- legacy 插件 = manifest 中**没有 `runtime` 字段**的插件（`runtime` 支持 `js`/`wasm`/`hybrid`）。
- legacy 插件没有 `id`，安装时由 `name` 生成固定 ID（`name` 小写化并 slug 化后接 `-` 加 `sha256(name)` 前 12 位）。
- 运行时通过内置适配器把旧版全局 API 翻译成宿主 API（如旧 `network.fetch` → `network.fetch`、旧 `filesystem.*` → `file.*`、旧 `thirdpartyapp.*` → `device.apps.*`、旧 `debug.sendRaw` → `protocol.send`、旧 `ui.updatePluginSettingsUI` → `ui.update` 等）。
- 部分旧版 API 在新宿主中不可用并直接报错。
- 安装确认对话框会显示 legacy 兼容警告。

## 更新

- **覆盖安装即更新**：安装与已装插件同 ID 的包即为更新——关闭旧运行时、替换包内容，并保留原配置与「始终允许」授权。
- **发布者更新**：对发布者拥有的条目，上传同 ID 的新包即为更新（通常进入审核流程，由具体宿主决定）。

## 卸载与数据清理

- **卸载**：关闭运行时、清除授权、删除插件目录（含配置）。
- **清除数据**：关闭运行时、清除授权、删除数据与缓存，配置重置为空。

## 小结

- 包本质是 ZIP；扩展名只是约定，解析按内容。
- 同 ID 覆盖安装 = 更新，授权与配置保留。
- legacy 插件通过适配器兼容，但部分旧 API 不可用。

{ref("Vela 官方打包与发布工具（tools）", REF["tools"])}
"""
})

# ---------------------------------------------------------------------------
out = []
for c in course:
    out.append({"slug": c["slug"], "title": c["title"], "md": c["md"]})
with open(os.path.join(DATA, "plugin_course.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("plugin chapters:", len(out))
print("slugs:", [c["slug"] for c in out])
