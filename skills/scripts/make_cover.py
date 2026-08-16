#!/usr/bin/env python3
"""make_cover.py — 无图文章的排版封面生成器（PIL，零外部依赖）。

背景（2026-08-16）：认知类文章无配图时，封面兜底取正文首图，而 fill-images 的
图库搜图兜底曾让连续 3 篇文章用上同一张库存照。本脚本保证每篇自带 cover.png，
且按 slug 哈希轮换 6 套配色，避免封面模板同质化。

用法:
  python3 skills/scripts/make_cover.py <post_dir> --title "标题" [--title2 "第二行"] \
      [--kicker "眉题"] [--sub "副题"] [--palette N]

不传 --palette 时按 post_dir 目录名哈希自动轮换。输出 <post_dir>/cover.png（1080x460）。
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 460
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"

# (渐变起, 渐变止, 强调色)
PALETTES = [
    ((16, 34, 46), (36, 80, 95), (255, 196, 90)),     # 深青 + 暖金
    ((43, 29, 18), (94, 62, 33), (255, 209, 128)),    # 深棕 + 琥珀
    ((15, 36, 24), (31, 74, 53), (154, 230, 180)),    # 墨绿 + 浅绿
    ((26, 16, 48), (58, 42, 95), (196, 181, 253)),    # 靛紫 + 薰衣草
    ((46, 20, 24), (96, 44, 52), (255, 170, 160)),    # 绛红 + 珊瑚
    ((24, 28, 34), (52, 60, 72), (255, 255, 255)),    # 石墨 + 纯白
]


def make(post_dir: Path, title: str, title2: str, kicker: str, sub: str, palette: int | None) -> Path:
    if palette is None:
        palette = int(hashlib.md5(post_dir.name.encode()).hexdigest(), 16) % len(PALETTES)
    c1, c2, accent = PALETTES[palette % len(PALETTES)]

    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        for x in range(W):
            t = x / W * 0.6 + y / H * 0.4
            px[x, y] = tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))
    d = ImageDraw.Draw(img, "RGBA")

    # 右上光晕（强调色低透明）
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    cx, cy, R = W - 90, 40, 300
    for r in range(R, 0, -4):
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=int(42 * (1 - r / R)))
    img.paste(Image.new("RGB", (W, H), accent), (0, 0), glow)

    f_kicker = ImageFont.truetype(FONT, 26, index=1)
    f_title = ImageFont.truetype(FONT, 64 if title2 else 78, index=1)
    f_sub = ImageFont.truetype(FONT, 30, index=0)

    X = 72
    if kicker:
        kx = X
        for ch in kicker:
            d.text((kx, 62), ch, font=f_kicker, fill=accent)
            kx += f_kicker.getbbox(ch)[2] + 8

    if title2:
        d.text((X, 132), title, font=f_title, fill=(255, 255, 255))
        d.text((X, 218), title2, font=f_title, fill=(255, 255, 255))
        sub_y = 340
    else:
        d.text((X, 160), title, font=f_title, fill=(255, 255, 255))
        sub_y = 300
    if sub:
        d.text((X, sub_y), sub, font=f_sub, fill=(*accent, 235))

    out = post_dir / "cover.png"
    img.save(out, "PNG")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("post_dir", type=Path)
    ap.add_argument("--title", required=True)
    ap.add_argument("--title2", default="")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--sub", default="")
    ap.add_argument("--palette", type=int, default=None)
    a = ap.parse_args()
    print("saved:", make(a.post_dir, a.title, a.title2, a.kicker, a.sub, a.palette))
