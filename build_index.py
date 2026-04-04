#!/usr/bin/env python3
"""
扫描 posts/ 目录下所有 article.html，提取标题，生成 posts.json。
新文章发布后运行一次即可更新首页索引。

用法：
  python3 build_index.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
OUTPUT = ROOT / "posts.json"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
DESC_RE = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
    re.IGNORECASE | re.DOTALL,
)


def extract_meta(html_path: Path) -> dict:
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    title_m = TITLE_RE.search(text)
    desc_m = DESC_RE.search(text)
    title = title_m.group(1).strip() if title_m else html_path.parent.name
    desc = desc_m.group(1).strip() if desc_m else ""
    return {"title": title, "description": desc}


def main():
    articles = sorted(POSTS_DIR.glob("*/*/article.html"), reverse=True)

    if not articles:
        print("⚠️  posts/ 下没有找到 article.html，posts.json 将为空列表。")

    posts = []
    for html_path in articles:
        # posts/<date>/<slug>/article.html
        parts = html_path.relative_to(ROOT).parts  # ('posts', date, slug, 'article.html')
        date = parts[1] if len(parts) >= 3 else ""
        url = "/".join(parts)  # 相对于站点根目录的路径
        meta = extract_meta(html_path)
        posts.append(
            {
                "title": meta["title"],
                "description": meta["description"],
                "date": date,
                "url": url,
            }
        )
        print(f"  ✓ {date}  {meta['title'][:40]}")

    OUTPUT.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 已生成 posts.json，共 {len(posts)} 篇文章。")


if __name__ == "__main__":
    main()
