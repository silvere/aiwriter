#!/usr/bin/env python3
"""把 PNG 图表写进 article.md 占位符，并【原地更新】已存在的微信草稿（不新建）。

前置：先用 render_charts_png.py 生成 images/diagram_NN.png。
做的事：
  1) article.md 里的 <<__AIWRITER_PLACEHOLDER__>> 按序换成 ![](images/diagram_NN.png)
  2) 渲染微信正文 + 上传正文图片（PNG）+ 上传封面
  3) 用 draft/update 更新 .wechat-sync.json 记录的 media_id（原地覆盖，不产生重复草稿）
  4) 回查草稿 <img> 数量

用法: python3 skills/scripts/update_wechat_draft_images.py <post_dir>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import httpx

_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO))
from aiwriter.wechat import (  # noqa: E402
    get_access_token, _rewrite_images, upload_thumb_material,
    _pick_cover, _digest_from_md,
)
from aiwriter.wechat_theme import render_markdown_to_wechat  # noqa: E402

TOKEN = "<<__AIWRITER_PLACEHOLDER__>>"


def _load_env() -> dict:
    env = {}
    for line in (_REPO / ".env").read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def main():
    post = Path(sys.argv[1])
    env = _load_env()
    appid, secret = env["WECHAT_APPID"], env["WECHAT_APPSECRET"]

    md_path = post / "article.md"
    html_path = post / "article.html"
    md_text = md_path.read_text(encoding="utf-8")
    raw_html = html_path.read_text(encoding="utf-8")

    # 已存在的草稿 media_id
    marker = json.loads((post / ".wechat-sync.json").read_text(encoding="utf-8"))
    media_id = marker["media_id"]
    title = marker.get("title") or post.name

    # 1) 占位符 → 图片引用（按 diagram_NN.png 顺序）
    imgs = sorted((post / "images").glob("diagram_*.png"))
    n_tokens = md_text.count(TOKEN)
    print(f"占位符 {n_tokens} 个，PNG {len(imgs)} 张")
    idx = [0]

    def repl(_m):
        i = idx[0]
        idx[0] += 1
        if i < len(imgs):
            return f"![数据图](images/{imgs[i].name})"
        return ""  # 多余占位符清掉

    new_md = re.sub(re.escape(TOKEN), repl, md_text)
    md_path.write_text(new_md, encoding="utf-8")
    print(f"  已改写 article.md：{min(idx[0], len(imgs))} 处占位符 → 图片")

    # 2) 渲染微信正文（此时 md 已无 token，markdown 图片直接成 <img>）
    body = render_markdown_to_wechat(new_md, html_for_images=raw_html)
    digest = _digest_from_md(new_md, 54)

    with httpx.Client(timeout=60) as client:
        token = get_access_token(appid, secret, client=client)

        print("Step 1/3: 上传正文图片")
        new_body, uploaded = _rewrite_images(body, post, token, client=client,
                                             log=lambda m: print("  ", re.sub(r"\[/?[a-z ]+\]", "", m)))
        print(f"  → 上传 {len(uploaded)} 张")

        print("Step 2/3: 上传封面")
        cover = _pick_cover(post, uploaded)
        thumb_media_id, cover_url = upload_thumb_material(token, cover, client=client)
        print(f"  → 封面 {cover.name}")

        print("Step 3/3: 原地更新草稿 draft/update")
        r = client.post(
            "https://api.weixin.qq.com/cgi-bin/draft/update",
            params={"access_token": token},
            json={
                "media_id": media_id,
                "index": 0,
                "articles": {
                    "title": title,
                    "author": marker.get("author", ""),
                    "digest": digest,
                    "content": new_body,
                    "content_source_url": "",
                    "thumb_media_id": thumb_media_id,
                    "need_open_comment": 1,
                    "only_fans_can_comment": 0,
                },
            },
        )
        res = r.json()
        if res.get("errcode", 0) != 0:
            print("  ❌ 更新失败:", res)
            sys.exit(1)
        print(f"  ✓ 已更新草稿 media_id={media_id[:24]}...")

        # 4) 回查
        g = client.post("https://api.weixin.qq.com/cgi-bin/draft/get",
                        params={"access_token": token}, json={"media_id": media_id})
        g.encoding = "utf-8"
        content = g.json().get("news_item", [{}])[0].get("content", "")
        nimg = len(re.findall(r"<img[^>]*>", content))
        print(f"\n回查草稿：<img> 数 = {nimg}（之前是 0）")

    # 更新本地标记
    marker["uploaded_image_count"] = len(uploaded)
    marker["images_fixed"] = True
    (post / ".wechat-sync.json").write_text(
        json.dumps(marker, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
