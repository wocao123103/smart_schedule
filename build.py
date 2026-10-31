#!/usr/bin/env python3
"""智能日程助手网页版 · 源码构建脚本

用法：
    python build.py

输出：
    dist/index.html          单文件应用（约 5.5 MB）
    dist/sw.js               系统通知 / PWA
    dist/manifest.webmanifest
    dist/icon-*.png
    dist/serve.py            本地服务器
    dist/README.md

不需要 npm，不依赖第三方 Python 包，只用标准库。
"""
from pathlib import Path
import base64
import json
import re
import shutil

BASE = Path(__file__).resolve().parent
SRC = BASE / "src"
ASSETS = BASE / "assets"
LIBS = BASE / "libs"
ICONS = BASE / "icons"
PWA = BASE / "pwa"
DIST = BASE / "dist"

APP_PARTS = [
    "01-core.js",
    "02-ui.js",
    "03-form-settings.js",
    "04-ai-agent.js",
    "05-import.js",
    "06-export-reminders.js",
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def build():
    shell = read_text(SRC / "template.html")
    css = read_text(SRC / "app.css")
    app = "\n".join(read_text(SRC / "js" / name) for name in APP_PARTS)

    # Sora 字体子集
    font_b64 = b64(ASSETS / "sora.woff2")
    font_css = (
        "@font-face{font-family:'Sora';font-style:normal;font-weight:400 700;"
        "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}" % font_b64
    )
    css = css.replace("/*__FONT__*/", font_css)

    # 小图标：必须在应用脚本之前，首屏才有图标
    icon_map = {}
    for path in sorted(ICONS.glob("*.svg")):
        raw = read_text(path)
        if "Not found" in raw:
            continue
        m = re.search(r"<svg[^>]*>(.*?)</svg>", raw, re.S)
        if not m:
            continue
        inner = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip()
        icon_map[path.stem] = inner
    aliases = {
        "chart-column": "bar-chart-3",
        "chart-no-axes-column": "bar-chart-3",
        "triangle-alert": "alert-triangle",
        "square-check": "check-square",
        "split": "split-square-horizontal",
        "wand-sparkles": "wand-2",
    }
    for src, dst in aliases.items():
        if src in icon_map and dst not in icon_map:
            icon_map[dst] = icon_map[src]
        if dst in icon_map and src not in icon_map:
            icon_map[src] = icon_map[dst]
    icons_js = "const ICONS = " + json.dumps(icon_map, ensure_ascii=False) + ";"

    # 教程截图 / 主题预览：放在文档末尾的 JSON 里，打开教程页才解析
    tutorial = [
        ("tut-board.jpg", "看板"),
        ("tut-list.jpg", "列表与搜索"),
        ("tut-calendar.jpg", "日历"),
        ("tut-stats.jpg", "统计"),
        ("tut-agent.jpg", "Agent 与今日简报"),
    ]
    themes = [
        ("th-standard.jpg", "标准版"),
        ("th-teen.jpg", "青少年版"),
        ("th-senior.jpg", "老年版"),
        ("th-anime.jpg", "二次元版"),
    ]
    asset_obj = {
        "tutorial": [
            {"src": "data:image/jpeg;base64," + b64(ASSETS / name), "title": title}
            for name, title in tutorial
        ],
        "themes": [
            {"src": "data:image/jpeg;base64," + b64(ASSETS / name), "title": title}
            for name, title in themes
        ],
    }
    assets_json = json.dumps(asset_obj, ensure_ascii=False)

    # 重资源：文本形式放在应用脚本之后，按需执行；不阻塞手机首屏
    pdf_b64 = b64(ASSETS / "智能日程助手-源码解析.pdf")
    xlsx_src = read_text(LIBS / "xlsx.full.min.js")
    mammoth_src = read_text(LIBS / "mammoth.browser.min.js")

    html = shell
    html = html.replace("/*__FONT__*/", font_css)
    html = html.replace("/*__CSS__*/", css)
    html = html.replace("/*__ICONS__*/", icons_js)
    html = html.replace("/*__APP__*/", app)
    html = html.replace("/*__XLSX__*/", xlsx_src)
    html = html.replace("/*__MAMMOTH__*/", mammoth_src)
    html = html.replace("/*__ASSETS_JSON__*/", assets_json)
    html = html.replace("/*__PDF__*/", pdf_b64)

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    out = DIST / "index.html"
    out.write_text(html, encoding="utf-8", newline="\n")

    # PWA / 部署文件
    for name in ["sw.js", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png", ".nojekyll"]:
        src = PWA / name
        if src.exists():
            shutil.copy2(src, DIST / name)
    if (BASE / "serve.py").exists():
        shutil.copy2(BASE / "serve.py", DIST / "serve.py")
    if (BASE / "README.md").exists():
        shutil.copy2(BASE / "README.md", DIST / "README.md")

    size = out.stat().st_size
    print("built", out)
    print("size", size, "bytes", round(size / 1048576, 2), "MB")
    print("icons", len(icon_map), "tutorial", len(tutorial), "themes", len(themes))
    print("app starts at byte", out.read_text(encoding="utf-8").find("const $ ="))


if __name__ == "__main__":
    build()
