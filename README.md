# 智能日程助手 / Smart Schedule

一个**纯前端**的本地智能日程助手，整个应用就是根目录下的单个 `index.html`，无需服务器、无需后端。

## 功能
- 待办增删改查、状态切换（待办 / 进行中 / 已完成）
- **AI 助手**：一句话智能添加日程 + 多轮对话；浏览器直连 OpenAI 兼容接口，内置 DeepSeek / OpenAI / 豆包 / 通义千问 预设，可填 CORS 代理解决跨域
- 三种视图：看板 / 日历（月视图）/ 统计
- 回收站：恢复 / 彻底删除 / 清空
- 到点提醒 + 通知：优先系统通知，不支持时自动降级为页面内弹窗（不漏提醒）
- 数据导入 / 导出：JSON、iCal(.ics)、TXT/CSV
- 四套主题：标准 / 青少年 / 老年 / 二次元

## 在线使用（推荐，可解锁系统通知）
本项目已托管在 GitHub Pages，直接访问：

👉 **https://wocao123103.github.io/smart_schedule/**

> ⚠️ 手机浏览器**只有在 https 地址下**才会允许「系统通知」权限。
> 用手机 **QQ浏览器** 打开上面的 https 地址 → 点右上角「启用通知」→ 选允许；
> 并到手机「设置 → 应用 → QQ浏览器 → 通知」中把通知设为允许。
> 保持该标签页在后台打开，到点即可收到提醒。
> （浏览器被完全关闭时网页无法弹通知——这是 Web 方案的固有限制；如需息屏/关 App 也能弹，需要原生 App。）

## 本地使用
直接把 `index.html` 用任意浏览器打开即可，数据保存在浏览器本地（localStorage），不联网也能用。

## 维护者：启用 / 重新部署 GitHub Pages
1. 仓库 **Settings → Pages**（或 “Deployments → Pages”）
2. **Build and deployment → Source** 选 `Deploy from a branch`
3. **Branch** 选 `main`，目录选 `/ (root)`，保存
4. 等待约 1 分钟，即可通过上面的 https 地址访问。
5. 若修改了 `index.html`，`git push` 到 `main` 后 Pages 会自动更新（有时需几十秒）。

## 技术说明
- 纯静态单文件，所有逻辑用浏览器端 JavaScript + localStorage 实现
- AI 调用走浏览器 `fetch` 直连你配置的 OpenAI 兼容接口
- 通过运行时注入 PWA manifest 支持「添加到主屏幕」（Chrome 下可安装为全屏 App）
