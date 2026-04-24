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
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

# 本次运行内已下载图片的 MD5，防止同一篇文章出现重复图
_used_hashes: set[str] = set()


def _img_hash(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()

# 自动从项目根的 .env 加载环境变量（symlink 调用也生效，因 resolve() 会跟随软链）
try:
    from dotenv import load_dotenv as _load_dotenv
    _script_path = Path(__file__).resolve()
    for _parent in [_script_path.parent, *_script_path.parents]:
        _env_file = _parent / ".env"
        if _env_file.exists():
            _load_dotenv(_env_file, override=False)
            break
except ImportError:
    pass

_STYLE_WORDS = {
    "flat", "design", "minimalist", "illustration", "tech", "style",
    "no", "text", "labels", "clean", "white", "background", "blue",
    "color", "palette", "and", "the", "a", "an", "of", "in", "with",
    "on", "at", "to", "for", "is", "are", "was", "were",
}

# 占位符匹配：</div> 可选（兼容 LLM 漏写关闭标签的情况）
_PLACEHOLDER_RE = re.compile(
    r'<div class="img-placeholder (concept|diagram)">(.*?</details>)\s*(?:</div>)?',
    re.DOTALL,
)
_PRE_RE = re.compile(r"<pre>(.*?)</pre>", re.DOTALL)


# ─── concept：搜图下载 ───────────────────────────────────────────────────────

def _extract_keywords(prompt: str, n: int = 5) -> str:
    words = [w.strip(",.():;\"'") for w in prompt.split()]
    filtered = [w for w in words if w.lower() not in _STYLE_WORDS and len(w) > 1]
    return " ".join(filtered[:n])


def _download_url(img_url: str, dest: Path) -> bool:
    """下载图片并写入文件，自动跳过重复图（基于 MD5）。"""
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
        h = _img_hash(data)
        if h in _used_hashes:
            return False   # 重复图，拒绝
        _used_hashes.add(h)
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def _try_pexels(query: str, dest: Path, page: int = 1) -> bool:
    """Pexels 搜图，page 参数用于翻页避免重复。"""
    api_key = os.environ.get("PEXELS_API_KEY", "")
    if not api_key:
        return False
    try:
        url = (
            f"https://api.pexels.com/v1/search"
            f"?query={urllib.parse.quote(query)}&per_page=1&page={page}&orientation=landscape"
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
        if not img_url:
            return False
        if _download_url(img_url, dest):
            return True
        # 图片重复，尝试下一页（最多 5 页）
        if page < 5:
            return _try_pexels(query, dest, page + 1)
        return False
    except Exception:
        return False


def _try_unsplash(query: str, dest: Path, attempts: int = 0) -> bool:
    """Unsplash 随机图，重复时最多重试 3 次。"""
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
        if not img_url:
            return False
        if _download_url(img_url, dest):
            return True
        # 随机图重复，再试一次（最多 3 次）
        if attempts < 3:
            return _try_unsplash(query, dest, attempts + 1)
        return False
    except Exception:
        return False


def _try_gemini(prompt: str, dest: Path) -> bool:
    """用 Gemini 2.5 Flash Image (nano banana) 生成概念图，成功返回 True。"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return False
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return False
    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )
        candidates = getattr(response, "candidates", None) or []
        if not candidates:
            return False
        for part in candidates[0].content.parts:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                h = _img_hash(inline.data)
                if h in _used_hashes:
                    return False  # 极少见，防御性检查
                _used_hashes.add(h)
                dest.write_bytes(inline.data)
                return True
        return False
    except Exception as e:
        err = str(e).lower()
        # 地区限制（Claude Code sandbox IP 被 Google 封）→ 静默 fallback
        if "location is not supported" in err or "failed_precondition" in err:
            return False
        return False


def fetch_concept_image(prompt: str, dest: Path, candidate_urls: list[str]) -> Optional[str]:
    """候选 URL → Gemini → Pexels → Unsplash，成功返回来源字符串，失败返回 None。"""
    for url in candidate_urls:
        if _download_url(url, dest):
            return "candidate"
    if _try_gemini(prompt, dest):
        return "gemini"
    keywords = _extract_keywords(prompt)
    if _try_pexels(keywords, dest):
        return f"pexels [{keywords}]"
    if _try_unsplash(keywords, dest):
        return f"unsplash [{keywords}]"
    return None


# ─── diagram：用 matplotlib 生成图表 ────────────────────────────────────────

_GROUP_ALIASES = {
    "流入": "in", "in": "in", "进": "in", "+": "in",
    "流出": "out", "out": "out", "出": "out", "-": "out",
    "参照": "ref", "ref": "ref", "基线": "ref", "baseline": "ref",
    "正": "pos", "pos": "pos",
    "负": "neg", "neg": "neg",
}


def _parse_spec(spec_text: str) -> dict:
    """从规格卡文本中提取结构化数据。

    支持字段：
      【图类型】      图表类型（条形 / 对账 / 流程 / 饼）
      【副标题】      （可选）图表副标题，显示在标题栏下方
      【单位】        （可选）所有数值的共同单位（"亿美元"、"%"等）
      【核心判断】    （可选）底部 punchline 行，图表的"一句话主张"
      【渲染】        （可选）html / matplotlib；默认 html
      【核心内容】/【数据】
        数据条目，支持行内分组标签：
          - AWS 投资 [流入]：330
          - 算力合约 [流出]：1000
          - 年化收入 [参照]：300
        分组值映射到颜色：流入=蓝 流出=红 参照=灰 正=绿 负=橙
    """
    result = {
        "chart_type": "",
        "subtitle": "",
        "unit": "",
        "punchline": "",
        "render": "html",
        "items": [],
        "raw": spec_text,
    }

    def _field(name: str) -> str:
        m = re.search(r"【" + name + r"】[：:]\s*(.+)", spec_text)
        return m.group(1).strip() if m else ""

    result["chart_type"] = _field("图类型")
    result["subtitle"]   = _field("副标题")
    result["unit"]       = _field("单位")
    result["punchline"]  = _field("核心判断") or _field("一句话")
    render_raw = _field("渲染").lower()
    if render_raw:
        result["render"] = "matplotlib" if ("matplotlib" in render_raw or "png" in render_raw) else "html"

    # 数据条目：支持 "- 标签 [分组]：数值" 或 "- 标签：数值"
    item_re = re.compile(
        r"-\s+(.+?)(?:\s*\[([^\]]+)\])?\s*[：:]\s*([+-]?\d+\.?\d*%?)"
    )
    for match in item_re.finditer(spec_text):
        label = match.group(1).strip()
        group_raw = (match.group(2) or "").strip().lower()
        raw_val = match.group(3).strip()
        try:
            val = float(raw_val.replace("%", ""))
        except ValueError:
            continue
        group = _GROUP_ALIASES.get(group_raw, "")
        # 自动推断：无显式分组时，负值归为 neg
        if not group and val < 0:
            group = "neg"
        result["items"].append({
            "label": label,
            "value": val,
            "raw": raw_val,
            "group": group,
        })

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


# 分组配色表：流入蓝 / 流出红 / 参照灰 / 正值绿 / 负值橙 / 默认蓝
_GROUP_STYLE = {
    "in":  {"bar": "#1A56DB", "track": "#EEF2FF", "tag": "流入"},
    "out": {"bar": "#F05252", "track": "#FFE4E4", "tag": "流出"},
    "ref": {"bar": "#94A3B8", "track": "#F1F5F9", "tag": "参照"},
    "pos": {"bar": "#0E9F6E", "track": "#DEF7EC", "tag": "正"},
    "neg": {"bar": "#F59E0B", "track": "#FEF3C7", "tag": "负"},
    "":    {"bar": "#1A56DB", "track": "#EEF2FF", "tag": ""},
}


def _chart_shell(title: str, subtitle: str, body_html: str, punchline: str = "") -> str:
    """统一的图表外框：标题栏（主标题 + 可选副标题） + 主体 + 可选 punchline 条。"""
    title_html = f'<div style="font-size:14px;font-weight:700;letter-spacing:.3px">{title}</div>'
    if subtitle:
        title_html += (
            f'<div style="font-size:12px;font-weight:500;color:#BFDBFE;'
            f'margin-top:3px;letter-spacing:.2px">{subtitle}</div>'
        )
    punchline_html = ""
    if punchline:
        punchline_html = (
            f'<div style="background:#1e3a8a;color:#fef9c3;padding:14px 20px;'
            f'font-size:13px;font-weight:600;line-height:1.55;border-top:1px solid #1e3a8a">'
            f'<span style="color:#fbbf24;margin-right:6px">▸</span>{punchline}</div>'
        )
    return (
        f'<div style="margin:32px 0;background:#fff;border:1px solid #e2e8f0;'
        f'border-radius:12px;overflow:hidden;box-shadow:0 2px 10px rgba(30,58,138,.07)">'
        f'<div style="background:linear-gradient(135deg,#1A56DB,#1e3a8a);color:#fff;'
        f'padding:14px 20px">{title_html}</div>'
        f'<div style="padding:22px 24px 18px">{body_html}</div>'
        f'{punchline_html}</div>'
    )


def _scale_pct(val: float, max_val: float) -> float:
    """把量级压缩到 [8%, 100%] 区间，避免小条在量级悬殊时彻底看不见。"""
    if max_val <= 0:
        return 0.0
    raw_pct = abs(val) / max_val * 100
    if raw_pct <= 0:
        return 0.0
    # 量级相差 > 10x 时，用 sqrt 压缩保证可见性
    if max_val / max(abs(val), 1) > 10:
        raw_pct = (raw_pct ** 0.6)
    return max(8.0, min(100.0, raw_pct))


def _bar_chart_html(title: str, items: list, subtitle: str = "",
                     unit: str = "", punchline: str = "") -> str:
    """水平条形图：支持分组染色、单位、副标题、punchline。"""
    max_val = max(abs(it["value"]) for it in items) or 1
    # 判断是否需要展示分组图例
    groups_used = {it["group"] for it in items if it["group"]}
    legend_html = ""
    if groups_used:
        legend_items = "".join(
            f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:14px">'
            f'<span style="width:10px;height:10px;border-radius:3px;'
            f'background:{_GROUP_STYLE[g]["bar"]};display:inline-block"></span>'
            f'<span style="font-size:11px;color:#64748b">{_GROUP_STYLE[g]["tag"]}</span></span>'
            for g in ["in", "out", "ref", "pos", "neg"] if g in groups_used
        )
        unit_badge = (
            f'<span style="font-size:11px;color:#94a3b8;font-weight:500">单位：{unit}</span>'
            if unit else ""
        )
        legend_html = (
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'margin-bottom:16px;padding-bottom:12px;border-bottom:1px dashed #e2e8f0">'
            f'<div>{legend_items}</div>{unit_badge}</div>'
        )
    elif unit:
        legend_html = (
            f'<div style="text-align:right;margin-bottom:12px">'
            f'<span style="font-size:11px;color:#94a3b8">单位：{unit}</span></div>'
        )

    bars = ""
    for it in items:
        style = _GROUP_STYLE[it["group"]]
        pct = _scale_pct(it["value"], max_val)
        # 数值显示：附加单位（如有）
        value_display = it["raw"]
        if unit and not it["raw"].endswith("%") and unit not in value_display:
            value_display = f'{it["raw"]} {unit}'
        bars += (
            f'<div style="margin-bottom:14px">'
            f'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px">'
            f'<span style="font-size:13px;color:#374151;flex:1;padding-right:12px">{it["label"]}</span>'
            f'<span style="font-size:15px;font-weight:700;color:{style["bar"]};white-space:nowrap">{value_display}</span>'
            f'</div>'
            f'<div style="background:{style["track"]};border-radius:5px;height:10px;overflow:hidden">'
            f'<div style="background:{style["bar"]};width:{pct:.1f}%;height:100%;border-radius:5px;'
            f'transition:width .4s ease"></div>'
            f'</div>'
            f'</div>'
        )
    return _chart_shell(title, subtitle, legend_html + bars, punchline)


def _compare_chart_html(title: str, items: list, subtitle: str = "",
                         unit: str = "", punchline: str = "") -> str:
    """对账式成对对比图：把数据按相邻两项自动配对为 流入 vs 流出。

    若用户显式在分组标签里写了 [流入]/[流出]，则按组分边；
    否则按顺序：第 1、3、5... 项为"流入"侧，第 2、4、6... 项为"流出"侧。
    """
    # 按顺序配对
    pairs = []
    left_side = []
    right_side = []
    for i, it in enumerate(items):
        if it["group"] == "in":
            left_side.append(it)
        elif it["group"] == "out":
            right_side.append(it)
        elif i % 2 == 0:
            left_side.append(it)
        else:
            right_side.append(it)

    # 对齐长度
    n = max(len(left_side), len(right_side))
    while len(left_side) < n:
        left_side.append(None)
    while len(right_side) < n:
        right_side.append(None)
    pairs = list(zip(left_side, right_side))

    max_val = max(abs(it["value"]) for it in items if it) or 1

    unit_suffix = f' {unit}' if unit else ''

    def _side_html(it, side: str) -> str:
        if it is None:
            return '<div style="flex:1"></div>'
        color = "#1A56DB" if side == "left" else "#F05252"
        track = "#EEF2FF" if side == "left" else "#FFE4E4"
        pct = _scale_pct(it["value"], max_val)
        bar_align = "flex-end" if side == "left" else "flex-start"
        return (
            f'<div style="flex:1;display:flex;flex-direction:column;align-items:{"flex-end" if side == "left" else "flex-start"}">'
            f'<div style="font-size:12px;color:#374151;margin-bottom:4px;max-width:100%">{it["label"]}</div>'
            f'<div style="width:100%;display:flex;justify-content:{bar_align}">'
            f'<div style="background:{track};border-radius:5px;height:14px;width:100%;position:relative;overflow:hidden">'
            f'<div style="background:{color};height:100%;width:{pct:.1f}%;'
            f'{"margin-left:auto;border-radius:5px 0 0 5px" if side == "left" else "border-radius:0 5px 5px 0"}"></div>'
            f'</div></div>'
            f'<div style="font-size:14px;font-weight:700;color:{color};margin-top:4px">{it["raw"]}{unit_suffix}</div>'
            f'</div>'
        )

    headers = (
        f'<div style="display:flex;align-items:center;gap:24px;margin-bottom:16px;'
        f'padding-bottom:10px;border-bottom:1px dashed #e2e8f0">'
        f'<div style="flex:1;text-align:right;font-size:12px;font-weight:700;color:#1A56DB;letter-spacing:1px">← 流入 / INFLOW</div>'
        f'<div style="width:20px"></div>'
        f'<div style="flex:1;text-align:left;font-size:12px;font-weight:700;color:#F05252;letter-spacing:1px">OUTFLOW / 流出 →</div>'
        f'</div>'
    )

    rows = ""
    for left, right in pairs:
        rows += (
            f'<div style="display:flex;align-items:center;gap:24px;margin-bottom:20px">'
            f'{_side_html(left, "left")}'
            f'<div style="width:20px;height:40px;border-left:2px solid #e2e8f0"></div>'
            f'{_side_html(right, "right")}'
            f'</div>'
        )

    return _chart_shell(title, subtitle, headers + rows, punchline)


def _flow_chart_html(title: str, items: list) -> str:
    """步骤流程图：编号方框 + 箭头连接。"""
    steps = ""
    for i, it in enumerate(items):
        num = int(it["value"]) if it["value"] == int(it["value"]) else i + 1
        if i > 0:
            steps += (
                f'<div style="font-size:22px;color:#93C5FD;margin:0 4px;'
                f'align-self:center">→</div>'
            )
        steps += (
            f'<div style="background:#EEF2FF;border:1.5px solid #C7D2FE;border-radius:10px;'
            f'padding:12px 16px;text-align:center;min-width:90px;max-width:160px;flex:1">'
            f'<div style="font-size:22px;font-weight:700;color:#1A56DB;line-height:1">{num}</div>'
            f'<div style="font-size:12px;color:#374151;margin-top:6px;line-height:1.4">{it["label"]}</div>'
            f'</div>'
        )
    return (
        f'<div style="margin:32px 0;background:#fff;border:1px solid #e2e8f0;'
        f'border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.06)">'
        f'<div style="background:#1A56DB;color:#fff;padding:10px 16px;font-size:13px;'
        f'font-weight:700">{title}</div>'
        f'<div style="padding:20px 24px;display:flex;flex-wrap:wrap;align-items:stretch;gap:8px">'
        f'{steps}</div>'
        f'</div>'
    )


def _donut_chart_html(title: str, items: list) -> str:
    """SVG 圆环图 + 图例列表。"""
    _PALETTE = ["#1A56DB", "#F05252", "#0E9F6E", "#FBBF24", "#8B5CF6", "#EC4899"]
    total = sum(abs(it["value"]) for it in items) or 1
    cx, cy, r_out, r_in = 80, 80, 70, 42
    import math

    def arc_path(start_deg: float, sweep_deg: float) -> str:
        start = math.radians(start_deg - 90)
        end = math.radians(start_deg + sweep_deg - 90)
        x1, y1 = cx + r_out * math.cos(start), cy + r_out * math.sin(start)
        x2, y2 = cx + r_out * math.cos(end),   cy + r_out * math.sin(end)
        ix1, iy1 = cx + r_in * math.cos(end),   cy + r_in * math.sin(end)
        ix2, iy2 = cx + r_in * math.cos(start), cy + r_in * math.sin(start)
        large = 1 if sweep_deg > 180 else 0
        return (
            f"M {x1:.2f} {y1:.2f} "
            f"A {r_out} {r_out} 0 {large} 1 {x2:.2f} {y2:.2f} "
            f"L {ix1:.2f} {iy1:.2f} "
            f"A {r_in} {r_in} 0 {large} 0 {ix2:.2f} {iy2:.2f} Z"
        )

    slices = ""
    angle = 0
    for i, it in enumerate(items):
        color = _PALETTE[i % len(_PALETTE)]
        sweep = abs(it["value"]) / total * 360
        slices += f'<path d="{arc_path(angle, sweep)}" fill="{color}" stroke="#fff" stroke-width="2"/>'
        angle += sweep

    legend = ""
    for i, it in enumerate(items):
        color = _PALETTE[i % len(_PALETTE)]
        pct = abs(it["value"]) / total * 100
        legend += (
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">'
            f'<div style="width:12px;height:12px;border-radius:3px;background:{color};flex-shrink:0"></div>'
            f'<span style="font-size:12px;color:#374151;flex:1">{it["label"]}</span>'
            f'<span style="font-size:12px;font-weight:700;color:{color}">{pct:.0f}%</span>'
            f'</div>'
        )

    svg = (
        f'<svg width="160" height="160" viewBox="0 0 160 160" style="flex-shrink:0">'
        f'{slices}'
        f'</svg>'
    )
    return (
        f'<div style="margin:32px 0;background:#fff;border:1px solid #e2e8f0;'
        f'border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.06)">'
        f'<div style="background:#1A56DB;color:#fff;padding:10px 16px;font-size:13px;'
        f'font-weight:700">{title}</div>'
        f'<div style="padding:20px 24px;display:flex;align-items:center;gap:24px;flex-wrap:wrap">'
        f'{svg}'
        f'<div style="flex:1;min-width:160px">{legend}</div>'
        f'</div>'
        f'</div>'
    )


def _spec_card_html(spec_text: str) -> str:
    """将规格卡渲染为可视化 HTML 图表（条形图 / 对账图 / 流程图 / 圆环图）。"""
    spec = _parse_spec(spec_text)
    title     = spec["chart_type"] or "数据图"
    subtitle  = spec["subtitle"]
    unit      = spec["unit"]
    punchline = spec["punchline"]
    items     = spec["items"]

    if not items:
        # 无法解析数据时直接显示原始规格卡文字
        plain = spec_text.replace("<!--", "").replace("-->", "").strip()
        return (
            f'<div style="background:#f8f9ff;border:1px solid #e2e8f0;border-radius:12px;'
            f'padding:20px 24px;margin:32px 0;font-size:13px;color:#4a4a6a;white-space:pre-wrap">'
            f'{plain}</div>'
        )

    ct = title
    if "流程" in ct:
        return _flow_chart_html(title, items)
    if "饼" in ct or "占比" in ct or "比例" in ct:
        return _donut_chart_html(title, items)
    # 对账 / 成对 / 对比式双列渲染
    if "对账" in ct or "成对" in ct or "双列" in ct or "pair" in ct.lower():
        return _compare_chart_html(title, items, subtitle, unit, punchline)
    # 默认：条形图 / 数据图 / 对比图
    return _bar_chart_html(title, items, subtitle, unit, punchline)


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
            # 默认走 HTML/SVG 渲染（矢量、零依赖、中文永远不乱码）。
            # 仅当规格卡显式写 【渲染】：matplotlib / PNG 或设置环境变量
            # AIWRITER_USE_MATPLOTLIB=1 时，才尝试 matplotlib。
            spec_preview = _parse_spec(spec_text)
            use_mpl = (
                spec_preview["render"] == "matplotlib"
                or os.environ.get("AIWRITER_USE_MATPLOTLIB") == "1"
            )
            if use_mpl:
                dest = img_dir / f"diagram_{diagram_count[0]:02d}.png"
                if _generate_chart(spec_text, dest):
                    filled += 1
                    print(f"  ✓ diagram_{diagram_count[0]:02d}.png  [matplotlib PNG]")
                    return _img_html(f"images/{dest.name}", "数据图")
                print(f"  ⚠  diagram_{diagram_count[0]:02d}  matplotlib 启用但不可用，回退 HTML 路径")
            filled += 1
            print(f"  ✓ diagram_{diagram_count[0]:02d}  [HTML图表]")
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

    if (not os.environ.get("GEMINI_API_KEY")
            and not os.environ.get("PEXELS_API_KEY")
            and not os.environ.get("UNSPLASH_ACCESS_KEY")):
        print(
            "⚠  未配置任何图片 API key，concept 图将跳过。\n"
            "   推荐设置 GEMINI_API_KEY（nano banana）或 PEXELS_API_KEY（https://www.pexels.com/api/）",
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
