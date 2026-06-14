#!/usr/bin/env python3
"""微信草稿同步——带【草稿箱实查去重】+【单篇失败不中断】+【限定近期文章】。

替代 wechat-sync-v2.yml 里脆弱的 bash 选文逻辑，根治三个问题：
  1) 旧 bash 用 `git log --diff-filter=A HEAD`（无范围=遍历全history）→ 重发所有无标记老文 → 重复。
     本脚本只按【目录日期】选最近 N 天的文章，永不碰老文。
  2) 旧 bash `set -e` 下单篇同步失败（如缺封面）→ 整批中断、新文也发不了。
     本脚本每篇 try/except，失败只记 warning 继续。
  3) 新增【草稿箱实查去重】：同步前拉草稿箱标题集，已存在的文章补标记并跳过，绝不重发。

用法：
  python skills/scripts/sync_drafts.py --post posts/2026-06-08/xxx     # 显式同步一篇
  python skills/scripts/sync_drafts.py --recent-days 3                 # 自动选最近3天未同步的
  python skills/scripts/sync_drafts.py --recent-days 3 --dry-run       # 只看计划不真同步
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO))
from aiwriter.config import load_config          # noqa: E402
from aiwriter.wechat import (                     # noqa: E402
    WeChatError, get_access_token, sync_post_to_draft,
)

WECHAT_BASE = "https://api.weixin.qq.com/cgi-bin"


def _article_title(post_dir: Path) -> str:
    """文章标题：优先 article.md 第一个 # 标题，回退 article.html <title>。"""
    md = post_dir / "article.md"
    if md.exists():
        m = re.search(r"^#\s+(.+)$", md.read_text(encoding="utf-8"), re.MULTILINE)
        if m:
            return m.group(1).strip()
    html = post_dir / "article.html"
    if html.exists():
        m = re.search(r"<title>(.*?)</title>", html.read_text(encoding="utf-8"), re.I | re.S)
        if m:
            return m.group(1).strip()
    return post_dir.name


def _fetch_draft_titles(token: str, *, client: httpx.Client) -> dict[str, str]:
    """拉草稿箱所有草稿，返回 {标题: media_id}。"""
    out: dict[str, str] = {}
    offset = 0
    while True:
        r = client.post(f"{WECHAT_BASE}/draft/batchget",
                        params={"access_token": token},
                        json={"offset": offset, "count": 20, "no_content": 1}).json()
        items = r.get("item", [])
        if not items:
            break
        for it in items:
            title = it.get("content", {}).get("news_item", [{}])[0].get("title", "").strip()
            if title:
                out[title] = it["media_id"]
        offset += len(items)
        if offset >= r.get("total_count", 0):
            break
    return out


def _write_marker(post_dir: Path, media_id: str, title: str, *, note: str) -> None:
    (post_dir / ".wechat-sync.json").write_text(
        json.dumps({
            "media_id": media_id, "title": title, "cover_url": "",
            "uploaded_image_count": 0,
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "note": note,
        }, ensure_ascii=False, indent=2), encoding="utf-8")


def _resolve_targets(args) -> list[Path]:
    if args.post:
        p = Path(args.post)
        if not p.is_absolute():
            p = (_REPO / p).resolve()
        return [p]
    cutoff = (datetime.now(timezone.utc) - timedelta(days=args.recent_days)).strftime("%Y-%m-%d")
    targets = []
    for html in sorted(_REPO.glob("posts/*/*/article.html"), reverse=True):
        d = html.parent
        date_part = d.relative_to(_REPO).parts[1]  # posts/<date>/<slug>
        if date_part >= cutoff and not (d / ".wechat-sync.json").exists():
            targets.append(d)
    return targets


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--post", help="显式指定 post 目录")
    ap.add_argument("--recent-days", type=int, default=3, help="自动选最近 N 天未同步文章")
    ap.add_argument("--dry-run", action="store_true", help="只列计划不真同步")
    ap.add_argument("--force", action="store_true", help="强制重发：跳过标题去重，先删除草稿箱已存在的同标题草稿再新增")
    args = ap.parse_args()

    config = load_config()
    if not config.has_wechat:
        print("::error::未配置 WECHAT_APPID/WECHAT_APPSECRET", file=sys.stderr)
        return 1

    targets = _resolve_targets(args)
    if not targets:
        print("::notice::没有最近未同步的文章")
        return 0
    print(f"候选 {len(targets)} 篇：" + ", ".join(str(t.relative_to(_REPO)) for t in targets))

    with httpx.Client(timeout=60) as client:
        token = get_access_token(config.wechat_appid, config.wechat_appsecret, client=client)
        box = _fetch_draft_titles(token, client=client)
        print(f"草稿箱现有 {len(box)} 篇")

        synced = skipped = deduped = failed = 0
        for d in targets:
            rel = d.relative_to(_REPO)
            if not (d / "article.html").exists():
                print(f"::warning::{rel}/article.html 不存在，跳过"); skipped += 1; continue
            if (d / ".wechat-sync.json").exists():
                print(f"  ⏭  {rel} 已有标记，跳过"); skipped += 1; continue

            title = _article_title(d)
            # 【核心去重】标题已在草稿箱 → 补标记跳过，绝不重发
            if title in box:
                if args.force:
                    old_media_id = box[title]
                    print(f"  ⚠  {rel} 强制模式：删除旧草稿《{title[:24]}》media_id={old_media_id[:22]}...")
                    try:
                        httpx.post(
                            f"{WECHAT_BASE}/draft/delete",
                            params={"access_token": token},
                            json={"media_id": old_media_id},
                            timeout=20,
                        ).raise_for_status()
                        print(f"    ✓ 已删除旧草稿")
                    except Exception as e:  # noqa: BLE001
                        print(f"::warning::删除旧草稿失败 {rel}: {e}（仍尝试新增）")
                else:
                    print(f"  ♻  {rel} 草稿箱已存在《{title[:24]}》→ 补标记跳过（去重）")
                    if not args.dry_run:
                        _write_marker(d, box[title], title, note="dedup: 草稿箱已存在，补标记防重发")
                    deduped += 1
                    continue

            if args.dry_run:
                print(f"  ✚ [dry-run] 将同步 {rel}《{title[:24]}》"); continue

            try:
                print(f"  → 同步 {rel}《{title[:24]}》")
                res = sync_post_to_draft(d, config, log=lambda m: None)
                print(f"    ✓ media_id={res.media_id[:22]}... 图片{res.uploaded_image_count}")
                synced += 1
            except WeChatError as e:
                print(f"::warning::同步失败 {rel}: {e}")   # 不中断，继续下一篇
                failed += 1
            except Exception as e:  # noqa: BLE001
                print(f"::warning::同步异常 {rel}: {e}")
                failed += 1

        print(f"\n汇总：同步 {synced} | 去重补标记 {deduped} | 跳过 {skipped} | 失败 {failed}")
    return 0   # 单篇失败不让整个 job 红（已记 warning）


if __name__ == "__main__":
    sys.exit(main())
