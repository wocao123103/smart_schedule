# 智能日程助手 · 网页版源码（v2.1.1）

这是单文件网页版的**可维护源码**，不是压缩后的 `index.html`。

- 源码目录：`智能日程助手网页版-源码/`
- 构建产物：`dist/index.html`（约 **5.47 MB**）
- 构建依赖：Python 3.9+，只用标准库，**不需要 npm / pip**
- 应用：纯 HTML + CSS + 原生 JS，无前端框架

---

## 一、快速构建

```bash
cd 智能日程助手网页版-源码
python build.py
```

构建成功后：

```
dist/
├─ index.html               # 5.47 MB 单文件，可直接双击或上传
├─ sw.js                    # 系统通知 / PWA
├─ manifest.webmanifest
├─ icon-192.png
├─ icon-512.png
├─ apple-touch-icon.png
├─ .nojekyll
├─ serve.py                 # 本地/局域网服务器
└─ README.md
```

本地预览：

```bash
cd dist
python serve.py
# 浏览器打开 http://127.0.0.1:8000/
```

部署：把 `dist/` 里的文件全部上传到 GitHub Pages 仓库根目录。

> 如果只改了一个 JS 文件，重新执行 `python build.py` 即可；不要直接改 `dist/index.html`，它会被覆盖。

---

## 二、目录说明

```
智能日程助手网页版-源码/
├─ build.py                 # 构建脚本：拼装 + 内嵌资源
├─ serve.py                 # 本地/局域网服务器
├─ README.md
├─ src/
│  ├─ template.html         # HTML 外壳，含 __APP__ / __PDF__ 等占位符
│  ├─ app.css               # 全部布局、四主题、移动端、弹窗样式
│  └─ js/
│     ├─ 01-core.js         # 工具、常量、state、localStorage、自动规则、主题
│     ├─ 02-ui.js           # 侧栏/顶栏/搜索/四视图/卡片/批量/主题菜单
│     ├─ 03-form-settings.js# 新建编辑弹窗、设置抽屉 6 页签
│     ├─ 04-ai-agent.js     # AI 五页签、截图/文件识别、简易 Agent
│     ├─ 05-import.js       # JSON/CSV/TXT/MD/Word/Excel/图片导入
│     └─ 06-export-reminders.js # 导出、通知、闹钟、启动
├─ assets/
│  ├─ sora.woff2            # 字体子集
│  ├─ tut-*.jpg             # 5 张教程截图
│  ├─ th-*.jpg              # 4 张主题预览
│  └─ 智能日程助手-源码解析.pdf
├─ libs/
│  ├─ xlsx.full.min.js      # SheetJS 0.18.5
│  └─ mammoth.browser.min.js# mammoth 1.8.0
├─ icons/                   # 58 个 Lucide SVG，构建时生成 ICONS
├─ pwa/                     # sw.js / manifest / 图标 / .nojekyll
└─ dist/                    # build.py 生成的部署目录（已附带一份）
```

---

## 三、加载架构（手机白屏修复的关键）

`index.html` 不是简单的“样式 + 一个巨大脚本”，而是按下面的顺序：

```html
<style>CSS + 字体</style>
<div id="boot-loading">正在加载…</div>
<div id="app">外壳</div>

<script>const ICONS = {...}</script>
<script>应用代码（约 94 KB 开始，约 238 KB 结束）</script>

<!-- 以下重资源在应用脚本之后，不阻塞首屏 -->
<script type="text/plain" id="lib-xlsx">...</script>
<script type="text/plain" id="lib-mammoth">...</script>
<script type="application/json" id="assets-json">{教程/主题图片}</script>
<script type="text/plain" id="pdf-data">...</script>
```

因此：

- 手机只需要先拿到约 **240 KB**，界面就能渲染
- 5 MB 图片/PDF/Office 解析库在后台继续加载
- 教程图片在打开「教程与关于」时才 `JSON.parse`
- Word/Excel 库在真正导入文件时才 `ensureLib()` 执行
- PDF 在点击下载时才读取 `#pdf-data`

对应代码：

- `getAssets()` / `getPDFDataURI()` / `ensureLib()`：`src/js/01-core.js`
- 应用先启动、隐藏 loading：`src/js/06-export-reminders.js` 的 `boot()`
- 重资源占位符：`src/template.html` + `build.py`

如果修改了加载顺序，请保持“应用脚本在 `lib-*` 之前”，否则手机可能再次白屏。

---

## 四、常用改动位置

| 想改什么 | 文件 |
|---|---|
| 侧栏、顶栏、搜索、卡片 | `src/js/02-ui.js` |
| 新建/编辑日程表单 | `src/js/03-form-settings.js` |
| 设置抽屉页签 | `src/js/03-form-settings.js` |
| AI 五页签、文件/截图识别 | `src/js/04-ai-agent.js` |
| 简易 Agent | `src/js/04-ai-agent.js` |
| 导入 JSON/CSV/Word/Excel | `src/js/05-import.js` |
| 导出 PNG/PDF/JSON/iCal | `src/js/06-export-reminders.js` |
| 通知、全屏闹钟 | `src/js/06-export-reminders.js` |
| 自动规则（30 天/5 天/课程） | `src/js/01-core.js` |
| 颜色、四主题、手机断点 | `src/app.css` |
| HTML 外壳 | `src/template.html` |
| 教程/主题截图 | `assets/` + `build.py` |
| PWA | `pwa/` |

修改后执行：

```bash
python build.py
```

---

## 五、v2.1.1 重点改动

### 1. 手机白屏修复

- 应用脚本前置：首屏约 240 KB，不再等整包 5 MB
- 重资源后置：Word/Excel 库、PDF、教程图片放到文档末尾
- `localStorage` 安全封装：被 WebView/隐私模式禁用时退回内存
- 启动兜底、加载提示、可读错误页
- 老旧 WebView API 兼容补丁
- 320 / 360 / 390 px 窄屏适配

### 2. 设置精简

- 移除「手机访问」页签、二维码、复制地址、qrcode 库
- 设置现在 6 页签：大模型接入 / 教学周历 / 提醒 / 外观 / 导出与分享 / 教程与关于

### 3. AI 智能添加支持文件

「AI 助手 → 智能添加」新增 **从文件填入**：

- Word `.docx`：mammoth 提取正文 → AI / 本地解析
- Excel `.xlsx/.xls`：SheetJS 读取表格 → 表头映射成日程
- TXT / Markdown：逐行 + 日期/标签/优先级解析
- CSV / TSV：表头映射
- JSON：数组、`{todos}`、`{entries}`、`{items}`
- 图片：调用视觉模型识别（需配置 gpt-4o / qwen-vl-max / glm-4v-plus 等）

选择文件后会自动填入并解析，勾选后点「添加选中项」。

---

## 六、资源与体积

`index.html` 约 **5.47 MB**，主要来自：

- 51 页《源码解析》PDF
- 5 张教程图 + 4 张主题预览
- SheetJS + mammoth
- Sora 字体子集
- 58 个图标
- 应用代码

符合 5–10 MB 要求，同时通过“应用前置”保证手机首屏速度。

---

## 七、说明

- 这是纯静态前端，数据保存在浏览器 `localStorage`
- AI 调用为浏览器直连模型；CORS 受限时在设置里填代理
- 浏览器完全关闭后无法定时提醒；页面在后台标签页可提醒
- 导出 PDF 使用浏览器打印
- 图片识别需要支持视觉的模型
- 教程图/PDF/字体等资源仅用于本应用展示，二次分发请确认相应授权
