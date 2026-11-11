#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告渲染验证：把一份 HTML 报告按章节拆开、逐章截图、跨视口宽度检查。

存在的理由（这些坑都是实际踩过的，不要重写一遍）：

1. Edge/Chrome 无头截图对**中文文件名**会做 URL 编码，直接截会报
   ERR_NAME_NOT_RESOLVED。解法：先复制成 ASCII 临时副本再截。
2. 无头模式下 `window.scrollTo()` **不生效**——脚本里滚动后截出来是空白页。
   解法：不用滚动，改为按 `<h2 id=...>` 把正文切成独立章节页分别截。
3. Edge 无头有**最小窗口宽度约 500px**的限制，截更窄会出现"内容溢出"的
   假象。解法：窄屏验证用 >=560px 宽度，不要用 375/420px。
4. Windows 应用商店版python.exe 是占位符，PIL 可能装不上。
   解法：本脚本**不依赖 PIL**，只用标准库 + 浏览器；图片尺寸用文件头解析。

用法：
    python render_check.py <报告.html> [--out 临时目录] [--keep]

输出：每个章节一张 PNG + 一份控制台小结。
退出码：0 = 全部生成成功；1 = 有章节截图失败。
"""

import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.parse

BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

# Edge/Chrome 无头的最小窗口宽度。低于此值截出来的溢出是假象。
MIN_WIDTH = 560

VIEWPORTS = [
    ("desktop", 1440, 1000),
    ("narrow", MIN_WIDTH, 1100),
]


def find_browser():
    for p in BROWSER_CANDIDATES:
        if os.path.isfile(p):
            return p
    return None


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def png_size(path):
    """不依赖 PIL，从 PNG 文件头读尺寸。"""
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if head[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        w, h = struct.unpack(">II", head[16:24])
        return (w, h)
    except Exception:
        return None


def split_sections(html):
    """按 <h2 id="..."> 把 <main> 内容切成若干段。

    返回 [(section_id, html_fragment), ...]；正文在第一个 h2 之前的内容
    （hero / 摘要）单独作为 ('__head__', fragment)。
    """
    m = re.search(r"<main\b[^>]*>(.*)</main>", html, re.S | re.I)
    if not m:
        # 没有 main 标签就整体当一段
        return [("__whole__", html)]
    body = m.group(1)
    # 兼容 <h2 id="x"> 与 <h2 class="..." id="x"> 两种属性顺序。
    parts = re.split(r'(?=<h2\b(?=[^>]*\bid=["\'])[^>]*>)', body, flags=re.I)
    out = []
    for p in parts:
        if not p.strip():
            continue
        hm = re.match(r'<h2\b[^>]*\bid="([^"]+)"', p, re.I)
        if hm:
            out.append((hm.group(1), p))
        elif out:
            out[-1] = (out[-1][0], out[-1][1] + p)
        else:
            out.append(("__head__", p))
    return out


def build_page(template, wrapper_open, side_html, fragment, main_open="<main>"):
    """用模板 + 原布局容器 + 侧栏 + 单章节正文，生成独立测试页。"""
    head = template + "\n" + wrapper_open + "\n"
    return (
        head
        + side_html
        + "\n"
        + main_open
        + "\n"
        + fragment
        + "\n</main>\n</div>\n</body>\n</html>\n"
    )


def shoot(browser, url, out_png, width, height, timeout_ms=9000):
    """调用无头浏览器截图。

    注意：--screenshot 的值不能带引号（subprocess 不会像 shell 那样拆引号，
    整个 '--screenshot="C:\\path\\x.png"' 会被当成一个字面路径 → 截图落盘失败）。
    """
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=%d,%d" % (width, height),
        "--screenshot=%s" % out_png,
        "--virtual-time-budget=%d" % timeout_ms,
        url,
    ]
    try:
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=90,
        )
    except subprocess.TimeoutExpired:
        return False
    return os.path.isfile(out_png) and os.path.getsize(out_png) > 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    src = os.path.abspath(sys.argv[1])
    if not os.path.isfile(src):
        print("[FAIL] 找不到报告文件: %s" % src)
        return 1

    keep = "--keep" in sys.argv
    out_dir = None
    if "--out" in sys.argv:
        i = sys.argv.index("--out")
        if i + 1 < len(sys.argv):
            out_dir = os.path.abspath(sys.argv[i + 1])

    browser = find_browser()
    if not browser:
        print("[FAIL] 未找到 Edge/Chrome，无法截图。")
        return 1
    print("[INFO] 浏览器: %s" % browser)

    html = read_text(src)
    side_m = re.search(r"<aside\b.*?</aside>", html, re.S)
    side_html = side_m.group(0) if side_m else ""
    body_m = re.search(r"<body\b[^>]*>", html, re.I)
    template = html[:body_m.end()] if body_m else html.split("<body>")[0] + "<body>"
    body_tail = html[body_m.end():] if body_m else html.split("<body>", 1)[-1]
    wrapper_m = re.match(r"\s*(<div\b[^>]*>)", body_tail, re.I)
    wrapper_open = wrapper_m.group(1) if wrapper_m else '<div class="wrap">'
    main_m = re.search(r"<main\b[^>]*>", html, re.I)
    main_open = main_m.group(0) if main_m else "<main>"

    sections = split_sections(html)
    print("[INFO] 切出 %d 个章节: %s" % (len(sections), ", ".join(s[0] for s in sections)))

    work = out_dir or tempfile.mkdtemp(prefix="_render_check_")
    os.makedirs(work, exist_ok=True)

    # 坑 1：中文文件名 -> URL 编码失败。用 ASCII 文件名 + file:// + 百分号编码路径。
    ascii_html = os.path.join(work, "page.html")
    with open(ascii_html, "w", encoding="utf-8") as f:
        f.write(html)
    base_url = "file:///" + urllib.parse.quote(ascii_html.replace("\\", "/"), safe="/")

    results = []
    for sid, frag in sections:
        page = os.path.join(work, "sec_%s.html" % re.sub(r"\W+", "_", sid))
        with open(page, "w", encoding="utf-8") as f:
            f.write(build_page(template, wrapper_open, side_html, frag, main_open))
        url = "file:///" + urllib.parse.quote(page.replace("\\", "/"), safe="/")

        for vp_name, w, h in VIEWPORTS:
            out_png = os.path.join(work, "shot_%s_%s.png" % (vp_name, re.sub(r"\W+", "_", sid)))
            ok = shoot(browser, url, out_png, w, h)
            size = png_size(out_png) if ok else None
            if ok and size and size[0] < 100:
                # 截出来是极窄的一条 = 内容被压扁，属于真实布局问题
                results.append((sid, vp_name, out_png, size, "布局异常：截图宽度异常"))
                continue
            results.append(
                (sid, vp_name, out_png, size, "OK" if ok else "截图失败")
            )

    print("\n=== 渲染验证结果 ===")
    bad = 0
    for sid, vp, png, size, status in results:
        flag = "OK  " if status == "OK" else "FAIL"
        if status != "OK":
            bad += 1
        dim = "%dx%d" % size if size else "无"
        print("[%s] %-8s %-10s %-10s %s" % (flag, sid, vp, dim, status))
    print("\n截图目录: %s" % work)

    if bad:
        print("[FAIL] %d 项异常。现场已保留（--keep 效果同此），请查看上面的 PNG。" % bad)
        # 失败时**必须**保留现场，否则无法排查
        return 1

    print("[PASS] 全部章节渲染正常。")
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
        print("[INFO] 临时文件已清理（加 --keep 可保留）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
