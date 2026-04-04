#!/usr/bin/env python3
"""
扫描 article.html 中的 img-placeholder 占位符，下载真实图片替换。

- concept 类：从占位符里提取 Prompt 关键词，搜索 Pexels / Unsplash 下载
- diagram 类：跳过（信息图需人工制作）
- 也支持直接传入外部图片 URL 列表作为候选（研究资料中抓取的图）

用法:
    # 处理单篇文章
    python3 fill_images.py posts/2026-04-04/slug/article.html

    # 处理整个 posts 目录
    python3 fill_images.py posts/

    # 传入候选图片 URL（来自研究资料），优先使用
    python3 fill_images.py article.html --candidate-urls url1 url2 ...

环境变量（至少配置一个）:
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

# 生成 Prompt 里的风格词，搜图时剔除掉
_STYLE_WORDS = {
    "flat", "design", "minimalist", "illustration", "tech", "style",
    "no", "text", "labels", "clean", "white", "background", "blue",
    "color", "palette", "and", "the", "a", "an", "of", "in", "with",
    "on", "at", "to", "for", "is", "are", "was", "were",
}

# 匹配占位符块：外层 div 总是以 </details>\s*</div> 结尾
_PLACEHOLDER_RE = re.compile(
    r'<div class="img-placeholder (concept|diagram)">(.*?</details>\s*)</div>',
    re.DOTALL,
)
# 提取 <pre> 里的文本（Prompt 或规格卡内容）
_PRE_RE = re.compile(r"<pre>(.*?)</pre>", re.DOTALL)


# ─── 图片搜索 ────────────────────────────────────────────────────────────────

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
        req = urllib.request.Request(url, headers={"Authorization": api_key, "User-Agent": "AIWriter/1.0"})
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
        req = urllib.request.Request(url, headers={"Accept-Version": "v1", "User-Agent": "AIWriter/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        img_url = data.get("urls", {}).get("regular", "")
        return bool(img_url) and _download_url(img_url, dest)
    except Exception:
        return False


def _try_candidate_url(url: str, dest: Path) -> bool:
    """直接下载来自研究资料的候选图片 URL。"""
    return _download_url(url, dest)


def fetch_image(query: str, dest: Path, candidate_urls: list[str] = []) -> Optional[str]:
    """
    依次尝试：候选 URL → Pexels → Unsplash。
    成功返回来源标识，失败返回 None。
    """
    for url in candidate_urls:
        if _try_candidate_url(url, dest):
            return f"candidate ({url[:60]})"

    if _try_pexels(query, dest):
        return "pexels"

    if _try_unsplash(query, dest):
        return "unsplash"

    return None


# ─── HTML 替换 ───────────────────────────────────────────────────────────────

def _img_html(rel_path: str, prompt_snippet: str) -> str:
    return (
        f'<figure style="margin:32px 0;text-align:center">'
        f'<img src="{rel_path}" alt="{prompt_snippet}" '
        f'style="max-width:100%;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,.08)">'
        f'</figure>'
    )


def fill_article(html_path: Path, candidate_urls: list[str] = []) -> dict:
    html = html_path.read_text(encoding="utf-8")
    img_dir = html_path.parent / "images"
    img_dir.mkdir(exist_ok=True)

    filled = skipped = 0
    counter = [0]  # mutable for closure

    def replace_placeholder(m: re.Match) -> str:
        kind = m.group(1)       # "concept" or "diagram"
        inner = m.group(2)

        if kind == "diagram":
            return m.group(0)   # 信息图跳过，无法自动生成

        # 提取 Prompt
        pre_m = _PRE_RE.search(inner)
        if not pre_m:
            return m.group(0)
        prompt = pre_m.group(1).strip()
        keywords = _extract_keywords(prompt)

        counter[0] += 1
        img_file = img_dir / f"concept_{counter[0]:02d}.jpg"

        source = fetch_image(keywords, img_file, candidate_urls)
        if source:
            rel = f"images/{img_file.name}"
            snippet = keywords[:50].replace('"', "'")
            nonlocal filled
            filled += 1
            print(f"  ✓ concept_{counter[0]:02d}.jpg  [{source}]  query: {keywords[:40]!r}")
            return _img_html(rel, snippet)
        else:
            nonlocal skipped
            skipped += 1
            print(f"  ✗ concept_{counter[0]:02d}  跳过（无 API key）  query: {keywords[:40]!r}")
            return m.group(0)

    new_html = _PLACEHOLDER_RE.sub(replace_placeholder, html)

    if filled:
        html_path.write_text(new_html, encoding="utf-8")

    return {"filled": filled, "skipped": skipped}


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="填充 article.html 中的图片占位符")
    parser.add_argument("targets", nargs="+", help="article.html 文件或 posts/ 目录")
    parser.add_argument(
        "--candidate-urls", nargs="*", default=[],
        metavar="URL",
        help="来自研究资料的候选图片 URL，优先使用",
    )
    args = parser.parse_args()

    # 收集所有要处理的文章
    articles: list[Path] = []
    for t in args.targets:
        p = Path(t)
        if p.is_dir():
            articles.extend(sorted(p.glob("*/*/article.html")))
        elif p.is_file() and p.suffix == ".html":
            articles.append(p)
        else:
            print(f"⚠ 跳过：{t}（不是 .html 文件或目录）", file=sys.stderr)

    if not articles:
        print("没有找到可处理的文章。", file=sys.stderr)
        sys.exit(1)

    if not os.environ.get("PEXELS_API_KEY") and not os.environ.get("UNSPLASH_ACCESS_KEY"):
        print(
            "⚠  未配置任何图片 API key。\n"
            "   请设置 PEXELS_API_KEY（推荐，免费注册：https://www.pexels.com/api/）\n"
            "   或 UNSPLASH_ACCESS_KEY（https://unsplash.com/developers）",
            file=sys.stderr,
        )

    total_filled = total_skipped = 0
    for html_path in articles:
        print(f"\n📄 {html_path}")
        result = fill_article(html_path, candidate_urls=args.candidate_urls)
        total_filled  += result["filled"]
        total_skipped += result["skipped"]

    print(
        f"\n{'─'*40}\n"
        f"完成：{total_filled} 张图片已填充，"
        f"{total_skipped} 张跳过（无 key 或 diagram 类）"
    )


if __name__ == "__main__":
    main()
