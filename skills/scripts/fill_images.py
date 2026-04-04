#!/usr/bin/env python3
"""
扫描 article.html 中的 img-placeholder 占位符，自动填充图片。

concept 类 → 关键词搜索 Pexels / Unsplash 下载图片
diagram 类 → 解析规格卡数据，用 matplotlib 生成图表；无法解析时渲染为数据卡片

用法:
    python3 fill_images.py posts/2026-04-04/slug/article.html
    python3 fill_images.py posts/          # 处理整个目录
    python3 fill_images.py article.html --candidate-urls url1 url2 ...

环境变量（至少配置一个用于 concept 图）:
    PEXELS_API_KEY        https://www.pexels.com/api/  免费，20000次/月
    UNSPLASH_ACCESS_KEY   https://unsplash.com/developers  免费，50次/小时
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

_STYLE_WORDS = {
    "flat", "design", "minimalist", "illustration", "tech", "style",
    "no", "text", "labels", "clean", "white", "background", "blue",
    "color", "palette", "and", "the", "a", "an", "of", "in", "with",
    "on", "at", "to", "for", "is", "are", "was", "were",
}

# 占位符匹配：外层 div 以 </details>\s*</div> 结尾
_PLACEHOLDER_RE = re.compile(
    r'<div class="img-placeholder (concept|diagram)">(.*?</details>\s*)</div>',
    re.DOTALL,
)
_PRE_RE = re.compile(r"<pre>(.*?)</pre>", re.DOTALL)


# ─── concept：搜图下载 ───────────────────────────────────────────────────────

def _extract_keywords(prompt: str, n: int = 5) -> str:
    words = [w.strip(",.():;\"'") for w in prompt.split()]
    filtered = [w for w in words if w.lower() not in _STYLE_WORDS and len(w) > 1]
    return " ".join(filtered[:n])


def _download_url(img_url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(
            img_url,
            headers={"User-Agent": "AIWriter/1.0",
                     "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        if len(data) < 2048:
            return False
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def _try_pexels(query: str, dest: Path) -> bool:
    api_key = os.environ.get("PEXELS_API_KEY", "")
    if not api_key:
        return False
    try:
        url = (
            f"https://api.pexels.com/v1/search"
            f"?query={urllib.parse.quote(query)}&per_page=1&orientation=landscape"
        )
        req = urllib.request.Request(
            url, headers={"Authorization": api_key, "User-Agent": "AIWriter/1.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        photos = data.get("photos", [])
        if not photos:
            return False
        img_url = photos[0]["src"].get("large2x") or photos[0]["src"].get("large", "")
        return bool(img_url) and _download_url(img_url, dest)
    except Exception:
        return False


def _try_unsplash(query: str, dest: Path) -> bool:
    key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not key:
        return False
    try:
        url = (
            f"https://api.unsplash.com/photos/random"
            f"?query={urllib.parse.quote(query)}&orientation=landscape&client_id={key}"
        )
        req = urllib.request.Request(
            url, headers={"Accept-Version": "v1", "User-Agent": "AIWriter/1.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        img_url = data.get("urls", {}).get("regular", "")
        return bool(img_url) and _download_url(img_url, dest)
    except Exception:
        return False


def fetch_concept_image(prompt: str, dest: Path, candidate_urls: list[str]) -> Optional[str]:
    """候选 URL → Pexels → Unsplash，成功返回来源字符串，失败返回 None。"""
    for url in candidate_urls:
        if _download_url(url, dest):
            return f"candidate"
    keywords = _extract_keywords(prompt)
    if _try_pexels(keywords, dest):
        return f"pexels [{keywords}]"
    if _try_unsplash(keywords, dest):
        return f"unsplash [{keywords}]"
    return None


# ─── diagram：用 matplotlib 生成图表 ────────────────────────────────────────

def _parse_spec(spec_text: str) -> dict:
    """从规格卡文本中提取结构化数据。"""
    result = {"chart_type": "", "title": "", "items": [], "raw": spec_text}

    # 图类型
    m = re.search(r"【图类型】[：:](.+)", spec_text)
    if m:
        result["chart_type"] = m.group(1).strip()

    # 数据条目：匹配 "- 标签：数值" 或 "- 标签: 数值"
    item_re = re.compile(r"-\s+(.+?)[：:]\s*([+-]?\d+\.?\d*%?)")
    for match in item_re.finditer(spec_text):
        label = match.group(1).strip()
        raw_val = match.group(2).strip()
        try:
            val = float(raw_val.replace("%", ""))
            result["items"].append({"label": label, "value": val, "raw": raw_val})
        except ValueError:
            pass

    return result


def _generate_chart(spec_text: str, dest: Path) -> bool:
    """解析规格卡并生成 matplotlib 图表，返回是否成功。"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
    except ImportError:
        return False

    spec = _parse_spec(spec_text)
    items = spec["items"]
    if not items:
        return False

    # 中文字体
    zh_fonts = [
        f.fname for f in fm.fontManager.ttflist
        if any(k in f.name.lower() for k in ("cjk", "noto", "wqy", "wenquanyi", "zen hei", "pingfang", "heiti", "simsun", "simhei"))
    ]
    if zh_fonts:
        fm.fontManager.addfont(zh_fonts[0])
        prop = fm.FontProperties(fname=zh_fonts[0])
        plt.rcParams["font.family"] = prop.get_name()
    plt.rcParams["axes.unicode_minus"] = False

    labels = [it["label"] for it in items]
    values = [it["value"] for it in items]
    chart_type = spec["chart_type"].lower()

    fig, ax = plt.subplots(figsize=(9, max(3.5, len(items) * 0.65)))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FAFAFA")

    all_negative = all(v <= 0 for v in values)
    colors = ["#F05252" if v < 0 else "#1A56DB" for v in values]

    # 横向条形图（含负值，或含"跌幅"等关键词）
    if all_negative or "条形" in chart_type or "bar" in chart_type:
        bars = ax.barh(labels, values, color=colors, height=0.55, zorder=3)
        for bar, it in zip(bars, items):
            x = bar.get_width()
            offset = -0.1 if x < 0 else 0.1
            ha = "right" if x < 0 else "left"
            ax.text(x + offset, bar.get_y() + bar.get_height() / 2,
                    it["raw"], va="center", ha=ha, fontsize=9.5,
                    fontweight="bold", color="#333")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.grid(axis="x", linestyle="--", alpha=0.35, zorder=0)
        ax.axvline(0, color="#ccc", linewidth=0.8)
    else:
        # 纵向条形图（默认）
        bars = ax.bar(labels, values, color=colors, width=0.55, zorder=3)
        for bar, it in zip(bars, items):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    it["raw"], ha="center", va="bottom", fontsize=9.5, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)

    ax.tick_params(axis="both", labelsize=9.5, colors="#333")
    plt.tight_layout(pad=1.2)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return True


def _spec_card_html(spec_text: str) -> str:
    """当图表生成失败时，将规格卡渲染为可读的 HTML 数据卡片。"""
    spec = _parse_spec(spec_text)
    rows = ""
    for it in spec["items"]:
        color = "#F05252" if it["value"] < 0 else "#1A56DB"
        rows += (
            f'<tr><td style="padding:6px 12px;color:#333">{it["label"]}</td>'
            f'<td style="padding:6px 12px;font-weight:700;color:{color};text-align:right">'
            f'{it["raw"]}</td></tr>'
        )
    if not rows:
        # 无法解析数据时直接显示原始规格卡文字
        plain = spec_text.replace("<!--", "").replace("-->", "").strip()
        return (
            f'<div style="background:#f8f9ff;border:1px solid #e2e8f0;border-radius:12px;'
            f'padding:20px 24px;margin:32px 0;font-size:13px;color:#4a4a6a;white-space:pre-wrap">'
            f'{plain}</div>'
        )
    title = spec["chart_type"] or "数据图"
    return (
        f'<div style="margin:32px 0;background:#fff;border:1px solid #e2e8f0;'
        f'border-radius:12px;overflow:hidden">'
        f'<div style="background:#1A56DB;color:#fff;padding:10px 16px;font-size:13px;'
        f'font-weight:700">{title}</div>'
        f'<table style="width:100%;border-collapse:collapse">{rows}</table>'
        f'</div>'
    )


def _img_html(rel_path: str, alt: str) -> str:
    return (
        f'<figure style="margin:32px 0;text-align:center">'
        f'<img src="{rel_path}" alt="{alt}" '
        f'style="max-width:100%;border-radius:12px;'
        f'box-shadow:0 4px 20px rgba(0,0,0,.08)">'
        f'</figure>'
    )


# ─── 主处理逻辑 ──────────────────────────────────────────────────────────────

def fill_article(html_path: Path, candidate_urls: list[str] = []) -> dict:
    html = html_path.read_text(encoding="utf-8")
    img_dir = html_path.parent / "images"
    img_dir.mkdir(exist_ok=True)

    concept_count = [0]
    diagram_count = [0]
    filled = skipped = 0

    def replace_placeholder(m: re.Match) -> str:
        nonlocal filled, skipped
        kind = m.group(1)
        inner = m.group(2)
        pre_m = _PRE_RE.search(inner)
        spec_text = pre_m.group(1).strip() if pre_m else ""

        if kind == "concept":
            concept_count[0] += 1
            dest = img_dir / f"concept_{concept_count[0]:02d}.jpg"
            source = fetch_concept_image(spec_text, dest, candidate_urls)
            if source:
                filled += 1
                print(f"  ✓ concept_{concept_count[0]:02d}.jpg  [{source}]")
                return _img_html(f"images/{dest.name}", _extract_keywords(spec_text)[:50])
            else:
                skipped += 1
                print(f"  ✗ concept_{concept_count[0]:02d}  跳过（无 API key）")
                return m.group(0)

        else:  # diagram
            diagram_count[0] += 1
            dest = img_dir / f"diagram_{diagram_count[0]:02d}.png"
            if _generate_chart(spec_text, dest):
                filled += 1
                print(f"  ✓ diagram_{diagram_count[0]:02d}.png  [matplotlib]")
                return _img_html(f"images/{dest.name}", "数据图")
            else:
                # 降级：渲染为数据卡片 HTML
                filled += 1
                print(f"  ✓ diagram_{diagram_count[0]:02d}  [数据卡片]")
                return _spec_card_html(spec_text)

    new_html = _PLACEHOLDER_RE.sub(replace_placeholder, html)
    if filled:
        html_path.write_text(new_html, encoding="utf-8")
    return {"filled": filled, "skipped": skipped}


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="填充 article.html 中的图片占位符")
    parser.add_argument("targets", nargs="+", help="article.html 文件或 posts/ 目录")
    parser.add_argument(
        "--candidate-urls", nargs="*", default=[], metavar="URL",
        help="研究资料中的图片 URL，concept 图优先使用",
    )
    args = parser.parse_args()

    articles: list[Path] = []
    for t in args.targets:
        p = Path(t)
        if p.is_dir():
            articles.extend(sorted(p.glob("*/*/article.html")))
        elif p.is_file() and p.suffix == ".html":
            articles.append(p)
        else:
            print(f"⚠ 跳过：{t}", file=sys.stderr)

    if not articles:
        print("没有找到可处理的文章。", file=sys.stderr)
        sys.exit(1)

    if not os.environ.get("PEXELS_API_KEY") and not os.environ.get("UNSPLASH_ACCESS_KEY"):
        print(
            "⚠  未配置图片 API key，concept 图将跳过。\n"
            "   建议设置 PEXELS_API_KEY（免费：https://www.pexels.com/api/）",
            file=sys.stderr,
        )

    total_filled = total_skipped = 0
    for html_path in articles:
        print(f"\n📄 {html_path}")
        r = fill_article(html_path, candidate_urls=args.candidate_urls)
        total_filled += r["filled"]
        total_skipped += r["skipped"]

    print(f"\n{'─'*40}\n完成：{total_filled} 处已填充，{total_skipped} 处跳过")


if __name__ == "__main__":
    main()
