"""微信公众号同步：把生成的 HTML 文章上传到草稿箱。

只对接 draft/add 接口（不自动群发），图片走 material/add_material 和
media/uploadimg，IP 白名单需要在公众平台后台预先配置。
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional

import httpx

from aiwriter.config import Config

WECHAT_BASE = "https://api.weixin.qq.com/cgi-bin"

# 公众号正文图片可显示的扩展名（来自 material/add_material 文档）
_RASTER_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}


class WeChatError(RuntimeError):
    """微信 API 返回的业务错误。"""


@dataclass
class _TokenCache:
    token: str
    expires_at: float


_token_cache: Optional[_TokenCache] = None


def get_access_token(appid: str, secret: str, *, client: httpx.Client) -> str:
    """获取并缓存 access_token（进程级，提前 60s 续期）。"""
    global _token_cache
    now = time.time()
    if _token_cache and _token_cache.expires_at - 60 > now:
        return _token_cache.token

    r = client.get(
        f"{WECHAT_BASE}/token",
        params={"grant_type": "client_credential", "appid": appid, "secret": secret},
        timeout=15,
    )
    data = r.json()
    if "access_token" not in data:
        raise WeChatError(f"获取 access_token 失败: {data}")
    _token_cache = _TokenCache(token=data["access_token"], expires_at=now + data.get("expires_in", 7200))
    return _token_cache.token


def _check(resp: httpx.Response, action: str) -> dict:
    data = resp.json()
    if isinstance(data, dict) and data.get("errcode", 0) not in (0, None):
        raise WeChatError(f"{action} 失败: errcode={data.get('errcode')}, errmsg={data.get('errmsg')}")
    return data


def upload_content_image(token: str, image_path: Path, *, client: httpx.Client) -> str:
    """正文图片上传，返回可在文章 HTML 里用的 URL（不占素材库配额，仅本接口有效）。"""
    with image_path.open("rb") as f:
        r = client.post(
            f"{WECHAT_BASE}/media/uploadimg",
            params={"access_token": token},
            files={"media": (image_path.name, f, "application/octet-stream")},
            timeout=30,
        )
    data = _check(r, f"上传正文图 {image_path.name}")
    return data["url"]


def upload_thumb_material(token: str, image_path: Path, *, client: httpx.Client) -> tuple[str, str]:
    """永久图片素材上传，返回 (media_id, url)。用于封面 thumb_media_id。"""
    with image_path.open("rb") as f:
        r = client.post(
            f"{WECHAT_BASE}/material/add_material",
            params={"access_token": token, "type": "image"},
            files={"media": (image_path.name, f, "application/octet-stream")},
            timeout=60,
        )
    data = _check(r, f"上传封面素材 {image_path.name}")
    return data["media_id"], data.get("url", "")


def add_draft(
    token: str,
    *,
    title: str,
    content_html: str,
    thumb_media_id: str,
    author: str = "",
    digest: str = "",
    content_source_url: str = "",
    client: httpx.Client,
) -> str:
    """新建图文草稿，返回草稿 media_id。"""
    body = {
        "articles": [
            {
                "title": title[:64],
                "author": author[:8] if author else "",
                "digest": digest[:120],
                "content": content_html,
                "content_source_url": content_source_url,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }
    r = client.post(
        f"{WECHAT_BASE}/draft/add",
        params={"access_token": token},
        # 微信对中文要求 UTF-8 不转义，必须用 data 而不是 json=
        content=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    data = _check(r, "新建草稿")
    return data["media_id"]


# --- HTML 解析与改写 ---


_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
_BODY_RE = re.compile(r"<body[^>]*>(.*?)</body>", re.IGNORECASE | re.DOTALL)
_STYLE_RE = re.compile(r"<style[^>]*>.*?</style>", re.IGNORECASE | re.DOTALL)
_SCRIPT_RE = re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL)
_IMG_SRC_RE = re.compile(r'(<img[^>]*\bsrc=")([^"]+)(")', re.IGNORECASE)


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip > 0:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip == 0:
            self.parts.append(data)


def _extract_title(html: str, fallback: str) -> str:
    m = _TITLE_RE.search(html)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()
        if title:
            return title
    return fallback


def _extract_body(html: str) -> str:
    m = _BODY_RE.search(html)
    inner = m.group(1) if m else html
    inner = _STYLE_RE.sub("", inner)
    inner = _SCRIPT_RE.sub("", inner)
    return inner.strip()


def _extract_digest(html: str, max_chars: int) -> str:
    body = _extract_body(html)
    parser = _TextExtractor()
    parser.feed(body)
    text = re.sub(r"\s+", " ", "".join(parser.parts)).strip()
    return text[:max_chars]


def _convert_svg_to_png(svg_path: Path) -> Optional[Path]:
    """SVG → PNG。需要 cairosvg；不可用时返回 None。"""
    try:
        import cairosvg  # type: ignore
    except ImportError:
        return None
    png_path = svg_path.with_suffix(".png")
    if not png_path.exists():
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=1200)
    return png_path


def _resolve_image(src: str, base_dir: Path) -> Optional[Path]:
    """把 HTML 里的 src 解析为本地文件路径；远程 URL 返回 None。"""
    if src.startswith(("http://", "https://", "data:")):
        return None
    p = (base_dir / src).resolve()
    return p if p.exists() else None


def _rewrite_images(
    html_body: str,
    base_dir: Path,
    token: str,
    *,
    client: httpx.Client,
    log,
) -> tuple[str, list[Path]]:
    """遍历正文图片，上传后替换 src。返回 (新HTML, 已上传的本地图片列表)。"""
    uploaded_locals: list[Path] = []
    cache: dict[str, str] = {}

    def replace(match: re.Match) -> str:
        prefix, src, suffix = match.group(1), match.group(2), match.group(3)
        if src in cache:
            return f"{prefix}{cache[src]}{suffix}"

        local = _resolve_image(src, base_dir)
        if local is None:
            # 远程 URL 或不存在 → 保持原样
            log(f"  [yellow]跳过 src（非本地或不存在）:[/yellow] {src}")
            return match.group(0)

        path_to_upload = local
        if local.suffix.lower() == ".svg":
            png = _convert_svg_to_png(local)
            if png is None:
                log(f"  [yellow]跳过 SVG（未安装 cairosvg）:[/yellow] {local.name}")
                return match.group(0)
            path_to_upload = png
        elif local.suffix.lower() not in _RASTER_EXTS:
            log(f"  [yellow]跳过不支持的图片格式:[/yellow] {local.name}")
            return match.group(0)

        try:
            new_url = upload_content_image(token, path_to_upload, client=client)
        except WeChatError as e:
            log(f"  [red]上传失败:[/red] {local.name} ({e})")
            return match.group(0)

        log(f"  [green]✓[/green] {local.name} → {new_url}")
        cache[src] = new_url
        uploaded_locals.append(local)
        return f"{prefix}{new_url}{suffix}"

    new_html = _IMG_SRC_RE.sub(replace, html_body)
    return new_html, uploaded_locals


def _pick_cover(post_dir: Path, fallback_images: list[Path]) -> Optional[Path]:
    """挑封面：优先 cover.{png,jpg,jpeg,gif}，否则取正文第一张光栅图。"""
    for ext in ("png", "jpg", "jpeg", "gif"):
        p = post_dir / f"cover.{ext}"
        if p.exists():
            return p
    for img in fallback_images:
        if img.suffix.lower() in _RASTER_EXTS:
            return img
        if img.suffix.lower() == ".svg":
            png = _convert_svg_to_png(img)
            if png is not None:
                return png
    return None


# --- 对外主入口 ---


@dataclass
class SyncResult:
    media_id: str
    title: str
    cover_url: str
    uploaded_image_count: int


def sync_post_to_draft(
    post_dir: Path,
    config: Config,
    *,
    log=lambda msg: None,
    source_url: str = "",
) -> SyncResult:
    """把单个 post 目录下的 article.html 同步到微信草稿箱。"""
    if not config.has_wechat:
        raise WeChatError("未配置 WECHAT_APPID / WECHAT_APPSECRET")

    html_path = post_dir / "article.html"
    if not html_path.exists():
        raise WeChatError(f"找不到 article.html: {html_path}")

    raw_html = html_path.read_text(encoding="utf-8")
    title = _extract_title(raw_html, fallback=post_dir.name)
    body = _extract_body(raw_html)
    digest = _extract_digest(raw_html, config.wechat.default_digest_chars)

    with httpx.Client() as client:
        token = get_access_token(config.wechat_appid, config.wechat_appsecret, client=client)
        log(f"[bold]→ 同步到微信草稿箱:[/bold] {title}")

        log("[bold]Step 1/3:[/bold] 上传正文图片")
        new_body, uploaded = _rewrite_images(body, post_dir, token, client=client, log=log)

        log("[bold]Step 2/3:[/bold] 上传封面")
        cover = _pick_cover(post_dir, uploaded)
        if cover is None:
            raise WeChatError(
                f"找不到封面图。请在 {post_dir} 放一张 cover.png/.jpg，"
                "或确保文章正文里至少有一张光栅图（PNG/JPG/GIF）"
            )
        thumb_media_id, cover_url = upload_thumb_material(token, cover, client=client)
        log(f"  [green]✓[/green] 封面: {cover.name} (media_id={thumb_media_id})")

        log("[bold]Step 3/3:[/bold] 创建草稿")
        media_id = add_draft(
            token,
            title=title,
            content_html=new_body,
            thumb_media_id=thumb_media_id,
            author=config.wechat.author,
            digest=digest,
            content_source_url=source_url,
            client=client,
        )
        log(f"  [green]✓[/green] 草稿已创建: media_id={media_id}")

    return SyncResult(
        media_id=media_id,
        title=title,
        cover_url=cover_url,
        uploaded_image_count=len(uploaded),
    )
