#!/usr/bin/env python3
"""
生成/下载配图，保存到指定路径。

优先级：
  1. OpenAI gpt-image-1（AI生成，质量最好）
  2. Unsplash API 兜底（免费图库，需要 UNSPLASH_ACCESS_KEY）
  3. 全部失败 → exit 2，stdout 输出 Prompt 供手动操作

用法:
    python3 generate_image.py "<prompt_or_query>" "<output_path>"

退出码:
    0 — 成功，图片已保存（来源: openai 或 unsplash）
    1 — 硬失败
    2 — 软失败，stdout 输出 Prompt/Query 供手动操作

环境变量:
    OPENAI_API_KEY       — OpenAI API Key（优先）
    UNSPLASH_ACCESS_KEY  — Unsplash API Key（兜底，https://unsplash.com/developers 免费注册）
"""
import sys
import os
import base64
import urllib.request
import urllib.parse
import json
from pathlib import Path


def try_openai(prompt, output_path):
    """尝试用 OpenAI gpt-image-1 生成图片。返回错误原因或 None（成功）。"""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return "no_key"

    try:
        from openai import OpenAI
    except ImportError:
        return "no_package"

    try:
        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="medium",
        )

        image_data = response.data[0].b64_json
        if image_data:
            output_path.write_bytes(base64.b64decode(image_data))
        else:
            url = response.data[0].url
            if not url:
                return "empty_response"
            with urllib.request.urlopen(url, timeout=30) as resp:
                output_path.write_bytes(resp.read())

        return None  # 成功

    except Exception as e:
        err = str(e).lower()
        if any(k in err for k in ("authentication", "invalid_api_key", "api key")):
            return "invalid_key"
        if any(k in err for k in ("billing", "quota", "insufficient", "hard_limit")):
            return "billing"
        return f"error:{e}"


def try_unsplash(query, output_path):
    """尝试用 Unsplash API 下载图片。返回错误原因或 None（成功）。"""
    access_key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not access_key:
        return "no_key"

    try:
        # 搜索随机图片
        encoded_query = urllib.parse.quote(query)
        api_url = (
            f"https://api.unsplash.com/photos/random"
            f"?query={encoded_query}&orientation=landscape&client_id={access_key}"
        )
        req = urllib.request.Request(
            api_url,
            headers={"Accept-Version": "v1", "User-Agent": "AIWriter/1.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())

        # 取 regular 尺寸（~1080px）
        img_url = data.get("urls", {}).get("regular")
        if not img_url:
            return "no_url"

        # 下载图片
        img_req = urllib.request.Request(
            img_url,
            headers={"User-Agent": "AIWriter/1.0"},
        )
        with urllib.request.urlopen(img_req, timeout=30) as resp:
            raw = resp.read()

        if len(raw) < 1024:
            return "too_small"

        output_path.write_bytes(raw)
        return None  # 成功

    except urllib.error.HTTPError as e:
        if e.code == 403:
            return "invalid_key"
        if e.code == 429:
            return "rate_limit"
        return f"http_{e.code}"
    except Exception as e:
        return f"error:{e}"


def main():
    if len(sys.argv) != 3:
        print("用法: python3 generate_image.py \"<prompt>\" \"<output_path>\"", file=sys.stderr)
        sys.exit(1)

    prompt = sys.argv[1]
    output_path = Path(sys.argv[2])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ── 1. 尝试 OpenAI ──────────────────────────────────────────
    reason = try_openai(prompt, output_path)
    if reason is None:
        size_kb = output_path.stat().st_size // 1024
        print(f"OK [openai]: {output_path} ({size_kb}KB)")
        sys.exit(0)

    print(f"OpenAI 跳过: {reason}", file=sys.stderr)

    # ── 2. 尝试 Unsplash 兜底 ────────────────────────────────────
    # 从 prompt 提取搜索关键词（取前3个单词作为 query）
    query_words = [w for w in prompt.split() if w.lower() not in
                   ("flat", "design", "minimalist", "illustration", "tech", "style",
                    "no", "text", "labels", "clean", "white", "background", "blue",
                    "color", "palette", "and", "the", "a", "an", "of", "in")]
    unsplash_query = " ".join(query_words[:4]) if query_words else prompt[:50]

    reason2 = try_unsplash(unsplash_query, output_path)
    if reason2 is None:
        size_kb = output_path.stat().st_size // 1024
        print(f"OK [unsplash]: {output_path} ({size_kb}KB, query: {unsplash_query!r})")
        sys.exit(0)

    print(f"Unsplash 跳过: {reason2}", file=sys.stderr)

    # ── 3. 全部失败 → 软失败，输出 Prompt ───────────────────────
    print(prompt)  # stdout 给 skill 捕获
    hint = ""
    if "no_key" in reason2:
        hint = "（提示：在 https://unsplash.com/developers 免费注册，将 Access Key 设为 UNSPLASH_ACCESS_KEY 环境变量即可启用兜底）"
    print(f"SOFT_FAIL: OpenAI({reason}) + Unsplash({reason2}) 均不可用 {hint}", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
