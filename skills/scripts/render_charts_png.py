#!/usr/bin/env python3
"""把 article.html 里已渲染的内联 HTML 图表反解 → matplotlib PNG。

背景：文章生成期把数据图表渲成了内联 <div style=...> HTML 图表（博客正常），
但微信公众号编辑器会清洗掉 CSS，导致草稿里图表退化成散落文字。
微信要的是真图片。本脚本把这些 HTML 图表反解成数据，用 matplotlib 渲成 PNG，
供后续上传微信草稿。

用法：
    python3 skills/scripts/render_charts_png.py <post_dir>
输出：
    <post_dir>/images/diagram_01.png ...（按文章内出现顺序）
"""
from __future__ import annotations

import re
import sys
from html import unescape
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ── 复用 wechat_theme 的图表块抽取（div 平衡计数，准确）──────────────────
_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO))
from aiwriter.wechat_theme import _extract_charts_in_order  # noqa: E402

# ── 中文字体 ────────────────────────────────────────────────────────────
_CJK = ("pingfang", "heiti", "stheiti", "songti", "hei", "noto sans cjk",
        "noto sans sc", "source han", "arial unicode")
_zh = [f.fname for f in fm.fontManager.ttflist
       if any(k in f.name.lower() for k in _CJK)]
if _zh:
    fm.fontManager.addfont(_zh[0])
    plt.rcParams["font.family"] = fm.FontProperties(fname=_zh[0]).get_name()
plt.rcParams["axes.unicode_minus"] = False

BLUE, RED, GRAY, GREEN, ORANGE = "#1A56DB", "#F05252", "#94A3B8", "#0E9F6E", "#FBBF24"
INK, SUB = "#1f2937", "#64748b"


def _strip_tags(s: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", s)).strip()


def _num(raw: str) -> float:
    m = re.search(r"-?\d+\.?\d*", raw.replace(",", ""))
    return float(m.group()) if m else 0.0


def _parse(block: str) -> dict:
    """从一个内联图表 HTML 块反解出结构化数据。"""
    # 标题（图类型）：头部第一个 font-weight:700 的 div
    mt = re.search(r'font-weight:700[^>]*>([^<]+)</div>', block)
    title = _strip_tags(mt.group(1)) if mt else ""
    # 副标题：紧跟其后 font-size:12px...color:#BFDBFE
    ms = re.search(r'color:#BFDBFE[^>]*>([^<]+)</div>', block)
    subtitle = _strip_tags(ms.group(1)) if ms else ""
    # punchline：底部 background:#1e3a8a 那条
    mp = re.search(r'background:#1e3a8a[^>]*>(.*?)</div>', block, re.DOTALL)
    punch = _strip_tags(mp.group(1)).lstrip("▸").strip() if mp else ""
    # 单位
    mu = re.search(r'单位：([^<\s]+)', block)
    unit = mu.group(1).strip() if mu else ""

    is_compare = "INFLOW" in block or "流入" in block and "流出" in block and "OUTFLOW" in block

    items = []  # {label, raw, value, side('left'/'right'/None), color}
    if is_compare:
        # 对账图：每个 _side_html 段含 label(12px,#374151) + 数值(14px,700,color)
        side_re = re.compile(
            r'font-size:12px;color:#374151;margin-bottom:4px[^>]*>(.*?)</div>.*?'
            r'background:(#[0-9A-Fa-f]{6});height:100%.*?'
            r'font-size:14px;font-weight:700;color:(#[0-9A-Fa-f]{6})[^>]*>(.*?)</div>',
            re.DOTALL)
        for m in side_re.finditer(block):
            label = _strip_tags(m.group(1))
            color = m.group(3)
            raw = _strip_tags(m.group(4))
            side = "left" if color.upper() == BLUE else "right"
            items.append({"label": label, "raw": raw, "value": _num(raw),
                          "side": side, "color": color})
    else:
        # 条形图：每条 label(13px,#374151,flex:1) + 数值(15px,700,color)
        bar_re = re.compile(
            r'font-size:13px;color:#374151;flex:1[^>]*>(.*?)</span>\s*'
            r'<span style="font-size:15px;font-weight:700;color:(#[0-9A-Fa-f]{6})[^>]*>(.*?)</span>',
            re.DOTALL)
        for m in bar_re.finditer(block):
            label = _strip_tags(m.group(1))
            color = m.group(2)
            raw = _strip_tags(m.group(3))
            items.append({"label": label, "raw": raw, "value": _num(raw),
                          "side": None, "color": color})

    return {"title": title, "subtitle": subtitle, "punchline": punch,
            "unit": unit, "is_compare": is_compare, "items": items}


def _wrap(text: str, n: int) -> str:
    out, line = [], ""
    for ch in text:
        line += ch
        if len(line) >= n:
            out.append(line); line = ""
    if line:
        out.append(line)
    return "\n".join(out)


def _render(spec: dict, dest: Path) -> bool:
    items = spec["items"]
    if not items:
        return False
    unit = spec["unit"]

    if spec["is_compare"]:
        left = [it for it in items if it["side"] == "left"]
        right = [it for it in items if it["side"] == "right"]
        rows = max(len(left), len(right))
        left += [None] * (rows - len(left))
        right += [None] * (rows - len(right))
        maxv = max((abs(it["value"]) for it in items), default=1) or 1
        fig, ax = plt.subplots(figsize=(9.2, max(3.2, rows * 1.15)))
        y = list(range(rows))[::-1]
        for yi, l, r in zip(y, left, right):
            if l:
                w = l["value"] / maxv
                ax.barh(yi, -w, color=BLUE, height=0.5, zorder=3)
                ax.text(-w - 0.02, yi, f'{l["raw"]}', va="center", ha="right",
                        fontsize=10.5, fontweight="bold", color=BLUE)
                ax.text(-0.02, yi + 0.34, _wrap(l["label"], 16), va="bottom", ha="right",
                        fontsize=9, color=INK)
            if r:
                w = r["value"] / maxv
                ax.barh(yi, w, color=RED, height=0.5, zorder=3)
                ax.text(w + 0.02, yi, f'{r["raw"]}', va="center", ha="left",
                        fontsize=10.5, fontweight="bold", color=RED)
                ax.text(0.02, yi + 0.34, _wrap(r["label"], 16), va="bottom", ha="left",
                        fontsize=9, color=INK)
        ax.axvline(0, color="#cbd5e1", lw=1.2, zorder=2)
        ax.set_xlim(-1.45, 1.45)
        ax.set_ylim(-0.6, rows - 0.2)
        ax.set_yticks([])
        ax.set_xticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.text(-1.0, rows - 0.35, "← 流入 / INFLOW", ha="center", fontsize=10,
                fontweight="bold", color=BLUE)
        ax.text(1.0, rows - 0.35, "OUTFLOW / 流出 →", ha="center", fontsize=10,
                fontweight="bold", color=RED)
    else:
        maxv = max((abs(it["value"]) for it in items), default=1) or 1
        fig, ax = plt.subplots(figsize=(9.2, max(3.0, len(items) * 0.78)))
        y = list(range(len(items)))[::-1]
        colors = [it["color"] for it in items]
        ax.barh(y, [it["value"] / maxv for it in items], color=colors,
                height=0.55, zorder=3)
        for yi, it in zip(y, items):
            ax.text(it["value"] / maxv + 0.015, yi,
                    f'{it["raw"]}{(" " + unit) if unit and not it["raw"].endswith("%") and unit not in it["raw"] else ""}',
                    va="center", ha="left", fontsize=10.5, fontweight="bold",
                    color=it["color"])
            ax.text(-0.015, yi, _wrap(it["label"], 22), va="center", ha="right",
                    fontsize=9.5, color=INK)
        ax.set_xlim(-0.9, 1.32)
        ax.set_yticks([])
        ax.set_xticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    # 标题 + 副标题
    ttl = spec["title"] or "数据图"
    fig.suptitle(ttl, x=0.02, ha="left", fontsize=15, fontweight="bold", color=INK)
    if spec["subtitle"]:
        ax.set_title(spec["subtitle"], loc="left", fontsize=10.5, color=SUB, pad=14)
    # punchline 底部（不用 ▸，避免字体缺字；改用底色高亮条）
    if spec["punchline"]:
        fig.text(0.5, 0.02, spec["punchline"], ha="center", fontsize=10.5,
                 color="#fef9c3", fontweight="bold", wrap=True,
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="#1e3a8a",
                           edgecolor="none"))
        plt.subplots_adjust(bottom=0.18)

    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=170, bbox_inches="tight", facecolor="white", pad_inches=0.35)
    plt.close(fig)
    return True


def main():
    if len(sys.argv) < 2:
        print("用法: render_charts_png.py <post_dir>", file=sys.stderr)
        sys.exit(1)
    post = Path(sys.argv[1])
    html = (post / "article.html").read_text(encoding="utf-8")
    charts = _extract_charts_in_order(html)
    print(f"抽取到 {len(charts)} 个图表块")
    img_dir = post / "images"
    n = 0
    for i, block in enumerate(charts, 1):
        spec = _parse(block)
        dest = img_dir / f"diagram_{i:02d}.png"
        ok = _render(spec, dest)
        flag = "✓" if ok else "✗"
        print(f"  {flag} diagram_{i:02d}.png  [{spec['title']}] {spec['subtitle'][:24]} "
              f"items={len(spec['items'])}")
        if ok:
            n += 1
    print(f"完成：{n}/{len(charts)} 渲染成功")


if __name__ == "__main__":
    main()
