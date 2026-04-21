#!/usr/bin/env python3
"""
生成/下载配图，保存到指定路径。

优先级：
  1. OpenAI 兼容生图（首选，需 OPENAI_API_KEY；配 OPENAI_BASE_URL 可走 hub.jerryai.cn 等国内代理）
  2. Google Gemini 2.5 Flash Image (nano banana)（需 GEMINI_API_KEY，国内 IP 被封）
  3. Unsplash API 搜索兜底（需 UNSPLASH_ACCESS_KEY）
  4. Pexels API 搜索兜底（需 PEXELS_API_KEY）
  5. 全部失败 → exit 2，stdout 输出 Prompt 供手动操作

用法:
    python3 generate_image.py "<prompt_or_query>" "<output_path>"

退出码:
    0 — 成功，图片已保存（来源: openai / gemini / unsplash / pexels）
    1 — 硬失败
    2 — 软失败，stdout 输出 Prompt/Query 供手动操作

环境变量:
    OPENAI_API_KEY       — OpenAI 兼容 API Key（首选）
    OPENAI_BASE_URL      — 可选，指向代理（如 https://hub.jerryai.cn/v1）
    OPENAI_IMAGE_MODEL   — 可选，默认 gpt-image-1
    GEMINI_API_KEY       — Google Gemini API Key；兼容回落 GOOGLE_API_KEY
    GEMINI_IMAGE_MODEL   — 可选，默认 gemini-2.5-flash-image
    UNSPLASH_ACCESS_KEY  — Unsplash API Key（搜索兜底，https://unsplash.com/developers）
    PEXELS_API_KEY       — Pexels API Key（搜索兜底，https://www.pexels.com/api/）
"""
import sys
import os
import base64
import urllib.request
import urllib.parse
import json
from pathlib import Path


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


def try_gemini(prompt, output_path):
    """尝试用 Google Gemini 2.5 Flash Image (nano banana) 生成图片。返回错误原因或 None（成功）。"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return "no_key"

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return "no_package"

    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        candidates = getattr(response, "candidates", None) or []
        if not candidates:
            return "empty_response"

        for part in candidates[0].content.parts:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                output_path.write_bytes(inline.data)
                return None

        return "empty_response"

    except Exception as e:
        err = str(e).lower()
        # 地区限制：Gemini API 在中国大陆等地区、数据中心 IP 不可用
        if "location is not supported" in err or "failed_precondition" in err:
            return "location_blocked"
        # 模型 id 过期或 v1beta 未开放
        if "not found" in err or "not_found" in err:
            return "model_not_found"
        if "unauthenticated" in err or "permission_denied" in err or "api_key" in err or "api key" in err:
            return "invalid_key"
        # 用完整词匹配避免 generateContent 含 "rate" 的子串误判
        if "quota" in err or "resource_exhausted" in err or "rate_limit" in err or "rate limit" in err:
            return "rate_limit"
        if "safety" in err or "blocked" in err:
            return "safety_blocked"
        return f"error:{e}"


def try_openai(prompt, output_path):
    """尝试用 OpenAI 兼容接口生成图片（含 hub.jerryai.cn 等代理）。返回错误原因或 None（成功）。"""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return "no_key"

    try:
        from openai import OpenAI
    except ImportError:
        return "no_package"

    base_url = os.environ.get("OPENAI_BASE_URL") or None
    model = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")

    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        kwargs = dict(model=model, prompt=prompt, n=1, size="1024x1024")
        # 只有官方 gpt-image-1 接口支持 quality 参数，代理里不一定支持，直接省略最稳
        response = client.images.generate(**kwargs)

        data0 = response.data[0]
        b64 = getattr(data0, "b64_json", None)
        if b64:
            output_path.write_bytes(base64.b64decode(b64))
        else:
            url = getattr(data0, "url", None)
            if not url:
                return "empty_response"
            with urllib.request.urlopen(url, timeout=30) as resp:
                output_path.write_bytes(resp.read())

        return None  # 成功

    except Exception as e:
        err = str(e).lower()
        if any(k in err for k in ("authentication", "invalid_api_key", "api key", "unauthorized", "401")):
            return "invalid_key"
        if any(k in err for k in ("billing", "quota", "insufficient", "hard_limit", "balance", "余额")):
            return "billing"
        if "not found" in err or "model_not_found" in err or "404" in err:
            return "model_not_found"
        if "rate limit" in err or "429" in err:
            return "rate_limit"
        return f"error:{e}"


def try_pexels(query, output_path):
    """尝试用 Pexels API 下载图片（免费，20000次/月）。返回错误原因或 None（成功）。"""
    api_key = os.environ.get("PEXELS_API_KEY", "")
    if not api_key:
        return "no_key"

    try:
        encoded_query = urllib.parse.quote(query)
        api_url = (
            f"https://api.pexels.com/v1/search"
            f"?query={encoded_query}&per_page=1&orientation=landscape"
        )
        req = urllib.request.Request(
            api_url,
            headers={"Authorization": api_key, "User-Agent": "AIWriter/1.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())

        photos = data.get("photos", [])
        if not photos:
            return "no_results"

        img_url = photos[0]["src"].get("large2x") or photos[0]["src"].get("large")
        if not img_url:
            return "no_url"

        img_req = urllib.request.Request(img_url, headers={"User-Agent": "AIWriter/1.0"})
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

    # ── 1. 尝试 OpenAI 兼容接口 (含 hub.jerryai.cn 代理，国内可用) ──
    reason_openai = try_openai(prompt, output_path)
    if reason_openai is None:
        size_kb = output_path.stat().st_size // 1024
        print(f"OK [openai]: {output_path} ({size_kb}KB)")
        sys.exit(0)

    print(f"OpenAI 跳过: {reason_openai}", file=sys.stderr)

    # ── 2. 尝试 Gemini (nano banana) ─────────────────────────────
    reason_gemini = try_gemini(prompt, output_path)
    if reason_gemini is None:
        size_kb = output_path.stat().st_size // 1024
        print(f"OK [gemini]: {output_path} ({size_kb}KB)")
        sys.exit(0)

    print(f"Gemini 跳过: {reason_gemini}", file=sys.stderr)

    # ── 3. 尝试 Unsplash 兜底 ────────────────────────────────────
    # 从 prompt 提取搜索关键词（取前3个单词作为 query）
    query_words = [w for w in prompt.split() if w.lower() not in
                   ("flat", "design", "minimalist", "illustration", "tech", "style",
                    "no", "text", "labels", "clean", "white", "background", "blue",
                    "color", "palette", "and", "the", "a", "an", "of", "in")]
    unsplash_query = " ".join(query_words[:4]) if query_words else prompt[:50]

    reason_unsplash = try_unsplash(unsplash_query, output_path)
    if reason_unsplash is None:
        size_kb = output_path.stat().st_size // 1024
        print(f"OK [unsplash]: {output_path} ({size_kb}KB, query: {unsplash_query!r})")
        sys.exit(0)

    print(f"Unsplash 跳过: {reason_unsplash}", file=sys.stderr)

    # ── 4. 尝试 Pexels 兜底 ─────────────────────────────────────
    reason_pexels = try_pexels(unsplash_query, output_path)
    if reason_pexels is None:
        size_kb = output_path.stat().st_size // 1024
        print(f"OK [pexels]: {output_path} ({size_kb}KB, query: {unsplash_query!r})")
        sys.exit(0)

    print(f"Pexels 跳过: {reason_pexels}", file=sys.stderr)

    # ── 5. 全部失败 → 软失败，输出 Prompt ───────────────────────
    print(prompt)  # stdout 给 skill 捕获
    hints = []
    if "no_key" in reason_openai:
        hints.append("设置 OPENAI_API_KEY（+ 可选 OPENAI_BASE_URL 走 hub.jerryai.cn 等代理）")
    if "no_key" in reason_gemini:
        hints.append("设置 GEMINI_API_KEY 启用 nano banana 生图（https://aistudio.google.com/apikey）")
    if "no_key" in reason_unsplash:
        hints.append("设置 UNSPLASH_ACCESS_KEY 启用 Unsplash 兜底")
    if "no_key" in reason_pexels:
        hints.append("设置 PEXELS_API_KEY 启用 Pexels 兜底")
    hint = " ｜ ".join(hints)
    print(
        f"SOFT_FAIL: OpenAI({reason_openai}) + Gemini({reason_gemini}) + "
        f"Unsplash({reason_unsplash}) + Pexels({reason_pexels}) 均不可用 {hint}",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
