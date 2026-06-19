#!/usr/bin/env python3
"""render_illustration.py — 解释型配图：HTML 片段 → 高清 PNG。

illustrate 配图框架的「渲染层主力」。把模型按统一 CSS 约定写出的
`.illustration` HTML 片段，包进一个带成套样式的完整文档，再交给
同目录的 html_to_png.js（Playwright/Chromium）截图成 PNG。

为什么 HTML 优先（而非 AI 生图）：中文用系统字体永远正确、数字精确、
CSS 像素级布局、多图共用一套 CSS 变量 → 整篇文章配图风格统一、可复现。

用法（独立调用）:
    python3 render_illustration.py <fragment.html> <out.png> [--width 1100] [--scale 2]
    # fragment.html 里只要有 <div class="illustration">…</div> 即可，
    # 缺少外层和 <style> 时本脚本自动补齐统一样式。

退出码:
    0 — 成功    2 — 浏览器不可用（可降级）    1 — 其它失败
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Optional

_HERE = Path(__file__).resolve().parent
_RENDERER = _HERE / "html_to_png.js"


@lru_cache(maxsize=1)
def _node_env() -> dict:
    """让 node 能 require 全局安装的 playwright：把全局 node_modules 加进 NODE_PATH。

    本地环境 playwright 常是全局安装（npm root -g），而 Node 默认不搜索全局目录；
    CI 上若改成本地安装也无妨——本地 node_modules 仍会被自动解析。
    """
    env = dict(os.environ)
    try:
        root = subprocess.run(
            ["npm", "root", "-g"], capture_output=True, text=True, timeout=15
        ).stdout.strip()
    except Exception:
        root = ""
    if root:
        existing = env.get("NODE_PATH", "")
        env["NODE_PATH"] = root + (os.pathsep + existing if existing else "")
    return env

# §4 统一 CSS 约定：一篇文章所有解释型配图共用，保证「成套感」。
# 字体优先系统 CJK（PingFang/雅黑），CI 上回退 WenQuanYi/Noto CJK。
ILLUSTRATION_CSS = """
:root{
  --primary:#3B5BDB; --accent:#E8590C; --good:#2B8A3E;
  --ink:#1A1B2E; --sub:#6B7280; --line:#E5E7EB; --bg-soft:#F4F6FB;
  --font:"PingFang SC","Microsoft YaHei","WenQuanYi Zen Hei","Noto Sans CJK SC","Noto Sans SC",sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:transparent}
.illustration{
  width:1100px; background:#fff; border-radius:20px; padding:48px;
  color:var(--ink); font-family:var(--font); line-height:1.6;
  box-shadow:0 8px 40px rgba(26,27,46,.08);
}
.illustration h2{font-size:30px;font-weight:800;letter-spacing:.5px;margin-bottom:6px}
.illustration .sub{font-size:16px;color:var(--sub);margin-bottom:28px}
.illustration .row{display:flex;align-items:stretch;gap:16px}
.illustration .col{flex:1}
.illustration .step{
  background:var(--bg-soft);border:1px solid var(--line);border-radius:14px;
  padding:20px 22px;flex:1;
}
.illustration .step .n{
  display:inline-flex;align-items:center;justify-content:center;
  width:34px;height:34px;border-radius:50%;background:var(--primary);
  color:#fff;font-weight:800;font-size:17px;margin-bottom:12px;
}
.illustration .arrow{align-self:center;color:var(--primary);font-size:30px;font-weight:800}
.illustration .label{font-size:18px;font-weight:700;margin-bottom:4px}
.illustration .desc{font-size:15px;color:var(--sub)}
.illustration .vs{
  display:flex;gap:18px;
}
.illustration .vs > div{
  flex:1;border-radius:14px;padding:22px 24px;border:1px solid var(--line);
}
.illustration .vs .think{background:#FFF4E6}
.illustration .vs .fact{background:#EBFBEE}
.illustration .tag{
  display:inline-block;font-size:13px;font-weight:700;padding:3px 10px;
  border-radius:999px;margin-bottom:10px;
}
.illustration .tag.think{background:var(--accent);color:#fff}
.illustration .tag.fact{background:var(--good);color:#fff}
.illustration .bar-row{display:flex;align-items:center;gap:14px;margin:10px 0}
.illustration .bar-row .name{width:160px;font-size:15px;font-weight:600}
.illustration .bar{height:26px;border-radius:8px;background:var(--primary)}
.illustration .bar-row .val{font-size:16px;font-weight:800;color:var(--ink)}
.illustration .note{margin-top:24px;font-size:14px;color:var(--sub);border-top:1px dashed var(--line);padding-top:14px}
"""


def wrap_fragment(fragment: str) -> str:
    """把 `.illustration` 片段包成带统一样式的完整 HTML 文档。

    若 fragment 已含 <style> 或完整 <html>，原样使用（让模型可覆盖默认样式）。
    """
    low = fragment.lower()
    if "<html" in low:
        return fragment
    has_style = "<style" in low
    style_block = "" if has_style else f"<style>{ILLUSTRATION_CSS}</style>"
    # 没有 .illustration 外层就补一个，保证截图选择器命中
    if 'class="illustration"' not in fragment and "class='illustration'" not in fragment:
        fragment = f'<div class="illustration">{fragment}</div>'
    return (
        "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
        f"{style_block}</head><body>{fragment}</body></html>"
    )


def render(fragment_html: str, out_png: Path, *, width: int = 1100,
           scale: float = 2.0) -> Optional[str]:
    """渲染片段为 PNG。成功返回 None；失败返回原因字符串（"browser_unavailable" 可降级）。"""
    if not _RENDERER.exists():
        return "renderer_missing"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    full = wrap_fragment(fragment_html)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(full)
        tmp_path = tf.name
    try:
        proc = subprocess.run(
            ["node", str(_RENDERER), tmp_path, str(out_png),
             "--width", str(width), "--scale", str(scale)],
            capture_output=True, text=True, timeout=90, env=_node_env(),
        )
    except FileNotFoundError:
        return "node_missing"
    except subprocess.TimeoutExpired:
        return "timeout"
    finally:
        try:
            Path(tmp_path).unlink()
        except OSError:
            pass

    if proc.returncode == 0 and out_png.exists() and out_png.stat().st_size > 2048:
        return None
    if proc.returncode == 2:
        return "browser_unavailable"
    return f"render_failed: {proc.stderr.strip()[:200]}"


def main() -> int:
    ap = argparse.ArgumentParser(description="解释型配图 HTML 片段 → PNG")
    ap.add_argument("fragment", help="含 .illustration 的 HTML 片段文件")
    ap.add_argument("out", help="输出 PNG 路径")
    ap.add_argument("--width", type=int, default=1100)
    ap.add_argument("--scale", type=float, default=2.0)
    args = ap.parse_args()

    fragment = Path(args.fragment).read_text(encoding="utf-8")
    reason = render(fragment, Path(args.out), width=args.width, scale=args.scale)
    if reason is None:
        print(f"OK: {args.out}")
        return 0
    print(f"FAIL: {reason}", file=sys.stderr)
    return 2 if reason in ("browser_unavailable", "renderer_missing", "node_missing") else 1


if __name__ == "__main__":
    sys.exit(main())
