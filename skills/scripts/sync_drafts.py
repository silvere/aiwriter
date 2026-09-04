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


def _resolve_cutoff(posts: list[tuple[str, Path]], *, recent_days: int,
                    max_backfill_days: int, now: datetime | None = None) -> str:
    """选文下界日期 = 原 N 天窗口，若窗口外还压着未同步文章则回退到最老那篇。

    为什么不能只用「今天往前 N 天」这一个固定窗口（2026-09-04 的事故）：
    self-hosted runner 从 8-31 起离线 4 天，每次触发都排队 24 小时被 GitHub 超时取消。
    runner 回来那天，`--recent-days 3` 的窗口只剩 09-01 起，8-31 那篇已经滑出窗口——
    不报错、不重试，就这么永久漏发了。窗口锚在「今天」，积压却是按「上次成功同步」
    攒的，两者一旦错位，中间的文章静默消失，而且再也不会被任何一次定时运行看到。

    所以下界改成「能盖住积压」：窗口外只要还有没标记的文章，就把下界退到最老的那一篇，
    积压多少补多少，runner 停几天都自愈。护栏是 max_backfill_days：
    早期有 60+ 篇文章从来没有标记（那时还没这套机制），下界绝不早于这个上限，
    免得停机数月后一次性把老文全推进草稿箱。真撞上重复，sync_drafts 同步前还会
    拉草稿箱按标题去重、补标记跳过，这是第二道网。
    """
    now = now or datetime.now(timezone.utc)

    def _ago(days: int) -> str:
        return (now - timedelta(days=days)).strftime("%Y-%m-%d")

    window, floor = _ago(recent_days), _ago(max_backfill_days)
    backlog = [dp for dp, d in posts
               if floor <= dp < window and not (d / ".wechat-sync.json").exists()]
    return min(backlog) if backlog else window


def _resolve_targets(args) -> list[Path]:
    if args.post:
        p = Path(args.post)
        if not p.is_absolute():
            p = (_REPO / p).resolve()
        return [p]
    posts = [
        (html.parent.relative_to(_REPO).parts[1], html.parent)   # posts/<date>/<slug>
        for html in sorted(_REPO.glob("posts/*/*/article.html"), reverse=True)
    ]
    cutoff = _resolve_cutoff(posts, recent_days=args.recent_days,
                             max_backfill_days=args.max_backfill_days)
    normal = (datetime.now(timezone.utc) - timedelta(days=args.recent_days)).strftime("%Y-%m-%d")
    if cutoff < normal:
        print(f"::warning::检测到积压：下界从 {normal} 回退到 {cutoff} 补发"
              f"（runner 停机过久？上限 {args.max_backfill_days} 天）")
    else:
        print(f"::notice::选文下界 {cutoff}（窗口 {args.recent_days} 天）")
    targets = [d for date_part, d in posts                      # posts 已按日期倒序
               if date_part >= cutoff and not (d / ".wechat-sync.json").exists()]
    # 单次上限：定时任务每 2 小时一轮，积压会在几轮内排干。作用是兜住极端情况——
    # 比如全新 clone 上一个标记都没有时，别一次性往草稿箱灌几十篇。
    if len(targets) > args.max_backfill_posts:
        print(f"::warning::积压 {len(targets)} 篇，本轮先发最新 {args.max_backfill_posts} 篇，"
              f"其余下一轮继续")
        targets = targets[:args.max_backfill_posts]
    return targets


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--post", help="显式指定 post 目录")
    ap.add_argument("--recent-days", type=int, default=3, help="自动选最近 N 天未同步文章")
    ap.add_argument("--max-backfill-days", type=int, default=30,
                    help="runner 停机后回溯补发的最大天数上限（防止一次性重发早期无标记老文）")
    ap.add_argument("--max-backfill-posts", type=int, default=10,
                    help="单次运行最多补发几篇，其余留给下一轮（定时任务每 2 小时一轮）")
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
            # --force 的唯一用途就是重发"已经同步过"的文章，所以它必须能越过本地标记；
            # 否则这道检查会先于下面的强制分支把目标筛掉，让 --force 永远是空操作。
            if (d / ".wechat-sync.json").exists() and not args.force:
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
