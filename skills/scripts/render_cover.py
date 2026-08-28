#!/usr/bin/env python3
"""render_cover.py — 题图（公众号封面）兜底生成器：标题 → 编辑级封面 PNG。

为什么要它（2026-08-28 起）：题图靠 Step 7.5 的 generate_image.py 出摄影图，
本机没有生图 API key 时会软失败 → 文章 commit 里没有 cover.* → wechat-sync 按
_pick_cover 回退取正文第一张图，并写下 .wechat-sync.json 标记；标记一旦落地，
后补的 cover.* 再也同步不上（幂等跳过）。这条脚本用 HTML→PNG（Chromium，本机/CI
都装了）把标题渲染成一张深色排版封面，**不依赖任何外部 API**，保证每篇在首次
同步前一定有 cover.*，彻底堵住"封面回退+标记锁死"这个时序坑。

用法:
    python3 render_cover.py <post_dir> [--title "标题"] [--kicker "眉题"] \
        [--sub "副题"] [--foot "底部小字"] [--badge-n "150" --badge-t "跌幅"] \
        [--palette N] [--out cover.jpg]

不传 --title 时从 <post_dir>/article.html 的 <title> 读；不传 --kicker 时从
article.md 的「**分类**：X」读。标题含破折号（—/——）时，破折号前作主标、后作副标。
不传 --palette 按 post_dir 目录名哈希在 6 套深色配色间轮换（避免每天同一张脸）。

退出码: 0 成功 ｜ 2 Chromium 不可用（可降级，调用方跳过即可）｜ 1 其它失败
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent

# (背景渐变起, 背景渐变止, 强调色) —— 全部深色底，白字 + 单强调色
PALETTES = [
    ("#12151b", "#1b212b", "#E0792B"),   # 石墨 + 暖橙（默认主色）
    ("#101a1e", "#16303a", "#4FB0C6"),   # 深青 + 湖蓝
    ("#12170f", "#1d2c1a", "#7BB661"),   # 墨绿 + 苔绿
    ("#1a1220", "#2a1c3a", "#B57BE0"),   # 靛紫 + 薰衣草
    ("#1e1112", "#341a1d", "#E06A5A"),   # 绛红 + 珊瑚
    ("#161311", "#2a231d", "#D9A441"),   # 深棕 + 琥珀
]


def _read_title(post_dir: Path) -> str:
    ah = post_dir / "article.html"
    if ah.exists():
        m = re.search(r"<title>(.*?)</title>", ah.read_text(encoding="utf-8", errors="ignore"), re.I | re.S)
        if m:
            return html.unescape(m.group(1)).strip()
    am = post_dir / "article.md"
    if am.exists():
        for line in am.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return post_dir.name


def _read_kicker(post_dir: Path) -> str:
    am = post_dir / "article.md"
    if am.exists():
        m = re.search(r"\*\*分类\*\*[:：]\s*([^\n|]+)", am.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1).strip()
    return "AIWRITER"


def _split_title(title: str) -> tuple[str, str]:
    """破折号前作主标、后作副标；没有破折号则整句作主标。"""
    for sep in ("——", "—", "--"):
        if sep in title:
            head, tail = title.split(sep, 1)
            return head.strip("，。、 "), tail.strip("，。、 ")
    return title.strip(), ""


def _cover_html(c1: str, c2: str, accent: str, kicker: str, main: str,
                sub: str, foot: str, badge_n: str, badge_t: str) -> str:
    # 主标越长字号越小，保证一屏放得下
    n = len(main)
    main_size = 150 if n <= 8 else 118 if n <= 12 else 92 if n <= 18 else 72 if n <= 26 else 56
    e = html.escape
    badge = ""
    if badge_n:
        badge = (f'<div class="badge"><div class="n">{e(badge_n)}'
                 f'<span class="x">×↓</span></div><div class="t">{e(badge_t)}</div></div>')
    sub_html = f'<div class="sub">{e(sub)}</div>' if sub else ""
    foot_line = e(foot) if foot else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:{c1}}}
  .cover{{width:1536px;height:1024px;position:relative;overflow:hidden;
    background:radial-gradient(1200px 700px at 78% 12%,{accent}29,transparent 60%),
      linear-gradient(150deg,{c1} 0%,{c2} 60%,{c1} 100%);
    font-family:'PingFang SC','Noto Sans CJK SC','WenQuanYi Zen Hei',sans-serif;
    color:#F4F1EA;padding:96px 104px;display:flex;flex-direction:column;justify-content:space-between}}
  .kicker{{font-size:30px;letter-spacing:.32em;color:{accent};font-weight:700}}
  .h1{{font-size:{main_size}px;font-weight:800;line-height:1.08;letter-spacing:-.01em;margin-top:14px}}
  .sub{{margin-top:34px;font-size:42px;font-weight:600;color:#C7CBD3;line-height:1.4}}
  .row{{display:flex;align-items:flex-end;justify-content:space-between}}
  .foot{{font-size:27px;color:#8A929E;letter-spacing:.04em;max-width:70%}}
  .badge{{text-align:right}}
  .badge .n{{font-size:118px;font-weight:800;color:{accent};line-height:.9}}
  .badge .x{{font-size:54px}}
  .badge .t{{font-size:25px;color:#9AA4B2;margin-top:10px;letter-spacing:.06em}}
  .hair{{height:1px;background:linear-gradient(90deg,{accent}99,{accent}00);margin:0 0 26px}}
</style></head><body>
<div class="cover">
  <div>
    <div class="kicker">{e(kicker)}</div>
    <div class="h1">{e(main)}</div>
    {sub_html}
  </div>
  <div>
    <div class="hair"></div>
    <div class="row"><div class="foot">{foot_line}</div>{badge}</div>
  </div>
</div>
</body></html>"""


def make(post_dir: Path, title: str, kicker: str, sub: str, foot: str,
         badge_n: str, badge_t: str, palette, out_name: str) -> int:
    if palette is None:
        palette = int(hashlib.md5(post_dir.name.encode()).hexdigest(), 16) % len(PALETTES)
    c1, c2, accent = PALETTES[palette % len(PALETTES)]

    auto_main, auto_sub = _split_title(title)
    main = auto_main
    if not sub:
        sub = auto_sub

    doc = _cover_html(c1, c2, accent, kicker, main, sub, foot, badge_n, badge_t)
    out = post_dir / out_name
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(doc)
        tmp = f.name

    cmd = ["node", str(_HERE / "html_to_png.js"), tmp, str(out),
           "--selector", ".cover", "--width", "1536", "--scale", "2"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0:
        print(f"saved: {out}")
        return 0
    # html_to_png 用 2 表示 Chromium 不可用（可降级）
    sys.stderr.write((proc.stderr or "").strip() + "\n")
    return 2 if proc.returncode == 2 else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("post_dir", type=Path)
    ap.add_argument("--title", default="")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--sub", default="")
    ap.add_argument("--foot", default="")
    ap.add_argument("--badge-n", dest="badge_n", default="")
    ap.add_argument("--badge-t", dest="badge_t", default="")
    ap.add_argument("--palette", type=int, default=None)
    ap.add_argument("--out", default="cover.jpg")
    a = ap.parse_args()
    title = a.title or _read_title(a.post_dir)
    kicker = a.kicker or _read_kicker(a.post_dir)
    sys.exit(make(a.post_dir, title, kicker, a.sub, a.foot, a.badge_n, a.badge_t, a.palette, a.out))
