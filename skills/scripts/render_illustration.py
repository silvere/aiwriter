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

# §4 统一设计系统：一篇文章所有配图共用，保证「成套感」+ 编辑级质感。
# 设计基调：暖纸底 + 近黑墨字 + 单一强调色 + 灰阶中性 + 大留白 + 一个视觉焦点。
# 字体优先系统 CJK（PingFang/雅黑），CI 上回退 WenQuanYi/Noto CJK。
ILLUSTRATION_CSS = """
:root{
  --paper:#FBFAF7; --ink:#15171F; --sub:#717584; --hair:#ECE8E0;
  --accent:#E0792B; --accent-deep:#C75B12; --accent-soft:#FBEAD6;
  --neutral:#9AA4B2; --neutral-soft:#EAEDF1; --good:#2FA36B; --bad:#D14B4B;
  --font:"PingFang SC","Microsoft YaHei","WenQuanYi Zen Hei","Noto Sans CJK SC","Noto Sans SC",sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:transparent}
.illustration{
  width:1100px; padding:60px 64px; border-radius:24px; color:var(--ink);
  font-family:var(--font); line-height:1.6;
  background:radial-gradient(125% 125% at 82% -12%, #FFFFFF 0%, var(--paper) 55%);
  box-shadow:0 10px 50px rgba(21,23,31,.07);
}
/* ── 文头 ── */
.illustration .kicker{font-size:14px;font-weight:700;letter-spacing:4px;color:var(--accent);margin-bottom:14px;text-transform:uppercase}
.illustration h2{font-size:38px;font-weight:800;letter-spacing:-.5px;line-height:1.2;margin:0}
.illustration .sub{font-size:17px;color:var(--sub);margin:12px 0 36px;line-height:1.5;font-weight:500}
/* ── 大数字焦点（少量数据首选，替代裸柱）── */
.illustration .bignum{font-size:150px;font-weight:850;line-height:.9;letter-spacing:-5px;color:var(--accent)}
.illustration .bignum small{font-size:54px;font-weight:800;vertical-align:16px;margin-left:2px}
/* ── 单根比例条（占比/构成，替代多根柱）── */
.illustration .proportion{display:flex;height:34px;border-radius:9px;overflow:hidden;background:var(--neutral-soft)}
.illustration .proportion .seg{height:100%;display:flex;align-items:center;padding-left:14px;color:#fff;font-size:14px;font-weight:700}
.illustration .scale{display:flex;justify-content:space-between;margin-top:10px;font-size:13px;color:var(--sub)}
/* ── 图例 / 直接标注 ── */
.illustration .legend{display:flex;gap:32px;flex-wrap:wrap}
.illustration .lg{display:flex;gap:11px;align-items:flex-start}
.illustration .lg .dot{width:14px;height:14px;border-radius:4px;margin-top:6px;flex-shrink:0}
.illustration .lg .n{font-size:24px;font-weight:850;line-height:1}
.illustration .lg .t{font-size:14px;color:var(--sub);margin-top:5px}
/* ── 流程：编号 + 连接箭头 ── */
.illustration .row{display:flex;align-items:stretch;gap:18px}
.illustration .col{flex:1}
.illustration .step{background:#fff;border:1px solid var(--hair);border-radius:16px;padding:22px 24px;flex:1;box-shadow:0 2px 14px rgba(21,23,31,.04)}
.illustration .step .n{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;background:var(--accent);color:#fff;font-weight:800;font-size:18px;margin-bottom:14px}
.illustration .arrow{align-self:center;color:var(--neutral);font-size:30px;font-weight:800}
.illustration .label{font-size:19px;font-weight:800;margin-bottom:5px}
.illustration .desc{font-size:15px;color:var(--sub);line-height:1.55}
/* ── 对照（以为 vs 其实 / 内 vs 外）── */
.illustration .vs{display:flex;gap:20px}
.illustration .vs>div{flex:1;border-radius:16px;padding:24px 26px;border:1px solid var(--hair)}
.illustration .vs .think{background:var(--accent-soft)}
.illustration .vs .fact{background:#E7F3EC}
.illustration .tag{display:inline-block;font-size:13px;font-weight:700;padding:4px 12px;border-radius:999px;margin-bottom:12px}
.illustration .tag.think{background:var(--accent);color:#fff}
.illustration .tag.fact{background:var(--good);color:#fff}
/* ── 收口 punchline（图的一句话主张）── */
.illustration .punch{margin-top:34px;padding-top:22px;border-top:1px solid var(--hair);font-size:17px;font-weight:600;line-height:1.55}
.illustration .punch b{color:var(--accent)}
.illustration .note{margin-top:28px;font-size:14px;color:var(--sub);border-top:1px solid var(--hair);padding-top:16px;line-height:1.55}
"""


_VENDOR_ECHARTS = _HERE / "vendor" / "echarts.min.js"


@lru_cache(maxsize=1)
def _echarts_inline() -> str:
    """把 vendored echarts.min.js 读成内联 <script>，渲染时离线注入（不依赖 CDN）。"""
    if _VENDOR_ECHARTS.exists():
        return f"<script>{_VENDOR_ECHARTS.read_text(encoding='utf-8')}</script>"
    return ""


def wrap_fragment(fragment: str) -> str:
    """把 `.illustration` 片段包成带统一样式的完整 HTML 文档。

    - 若 fragment 已含完整 <html>，原样使用。
    - 含 <style> 时不再注入默认样式（让模型可覆盖）。
    - 用到 echarts 时，自动在 head 内联 vendored echarts.min.js（多序列数据图）。
    """
    low = fragment.lower()
    if "<html" in low:
        return fragment
    has_style = "<style" in low
    style_block = "" if has_style else f"<style>{ILLUSTRATION_CSS}</style>"
    echarts_block = _echarts_inline() if "echarts" in low else ""
    # 没有 .illustration 外层就补一个，保证截图选择器命中
    if 'class="illustration"' not in fragment and "class='illustration'" not in fragment:
        fragment = f'<div class="illustration">{fragment}</div>'
    return (
        "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
        f"{style_block}{echarts_block}</head><body>{fragment}</body></html>"
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
