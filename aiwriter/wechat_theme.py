"""Markdown → 微信公众号 inline-style HTML 转换器。

微信公众号编辑器只识 inline style，不识 class、CSS 变量、伪元素、SVG 背景等。
本模块从干净的 Markdown 出发，输出全 inline-style 的 HTML，可直接喂进
draft/add 接口，效果对标 mdnice 默认主题。
"""

from __future__ import annotations

import re
from html.parser import HTMLParser

try:
    import markdown as _md
except ImportError as e:
    raise ImportError(
        "wechat_theme 需要 markdown 库。运行: pip install -e '.[wechat]'"
    ) from e


# ── 主题：所有微信支持的 inline style ───────────────────────────────────────

_BRAND = "#1A56DB"
_BRAND_DARK = "#1240a8"
_TEXT = "#3f3f3f"
_HEADING = "#1a1a2e"
_MUTE = "#666666"
_BG_LIGHT = "#f8f9ff"
_BORDER = "#e2e8f0"

THEME: dict[str, str] = {
    # —— 标题 ——
    "h1": (
        f"font-size: 22px; font-weight: 700; color: {_HEADING}; "
        "text-align: center; margin: 24px 0 20px; line-height: 1.4; "
        "letter-spacing: 0.02em;"
    ),
    "h2": (
        f"font-size: 18px; font-weight: 700; color: {_HEADING}; "
        f"margin: 32px 0 16px; padding: 8px 0 8px 12px; "
        f"border-left: 4px solid {_BRAND}; line-height: 1.5; "
        f"background: linear-gradient(90deg, {_BG_LIGHT}, transparent);"
    ),
    "h3": (
        f"font-size: 16px; font-weight: 700; color: {_BRAND}; "
        "margin: 24px 0 12px; line-height: 1.5;"
    ),
    "h4": (
        f"font-size: 15px; font-weight: 700; color: {_HEADING}; "
        "margin: 18px 0 10px;"
    ),
    "h5": f"font-size: 14px; font-weight: 700; color: {_HEADING}; margin: 16px 0 8px;",
    "h6": f"font-size: 13px; font-weight: 700; color: {_MUTE}; margin: 16px 0 8px;",

    # —— 段落 ——
    "p": (
        f"margin: 14px 0; line-height: 1.85; font-size: 15px; "
        f"color: {_TEXT}; letter-spacing: 0.05em; text-align: justify; "
        "word-spacing: 0.05em;"
    ),

    # —— 强调 ——
    "strong": f"font-weight: 700; color: {_HEADING};",
    "em": "font-style: italic; color: #555;",
    "del": "color: #999; text-decoration: line-through;",

    # —— 链接 ——
    "a": (
        f"color: {_BRAND}; text-decoration: none; "
        f"border-bottom: 1px solid {_BRAND}; word-break: break-all;"
    ),

    # —— 引用 ——
    "blockquote": (
        f"border-left: 4px solid {_BRAND}; padding: 12px 16px; "
        f"margin: 18px 0; background: {_BG_LIGHT}; "
        f"color: {_MUTE}; font-size: 14px; line-height: 1.75; "
        "border-radius: 0 6px 6px 0;"
    ),
    "blockquote_p": "margin: 0; color: inherit; font-size: inherit; line-height: inherit;",

    # —— 列表 ——
    "ul": "margin: 12px 0; padding-left: 1.5em;",
    "ol": "margin: 12px 0; padding-left: 1.5em;",
    "li": (
        f"margin: 6px 0; line-height: 1.75; color: {_TEXT}; "
        "font-size: 15px; letter-spacing: 0.05em;"
    ),

    # —— 代码 ——
    "code": (
        "background: #f3f4f6; color: #d6336c; padding: 2px 6px; "
        "border-radius: 4px; font-family: 'SFMono-Regular', Consolas, "
        "'Liberation Mono', Menlo, monospace; font-size: 13px; "
        "word-break: break-all;"
    ),
    "pre": (
        "background: #1e1e2e; color: #f8f8f2; padding: 16px; "
        "border-radius: 8px; overflow-x: auto; font-size: 13px; "
        "line-height: 1.6; margin: 18px 0;"
    ),
    "pre_code": (
        "background: transparent; color: inherit; padding: 0; "
        "font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', "
        "Menlo, monospace; font-size: 13px;"
    ),

    # —— 图片 ——
    "img": (
        "max-width: 100%; height: auto; display: block; "
        "margin: 18px auto; border-radius: 6px;"
    ),

    # —— 分隔线 ——
    "hr": (
        "border: none; border-top: 1px dashed #ccc; margin: 32px 0; "
        "height: 0;"
    ),

    # —— 表格 ——
    "table": (
        "border-collapse: collapse; width: 100%; margin: 18px 0; "
        "font-size: 14px;"
    ),
    "thead": "",
    "th": (
        f"border: 1px solid {_BORDER}; padding: 8px 12px; "
        f"background: {_BG_LIGHT}; font-weight: 700; text-align: left; "
        f"color: {_HEADING};"
    ),
    "td": (
        f"border: 1px solid {_BORDER}; padding: 8px 12px; "
        f"color: {_TEXT}; line-height: 1.7;"
    ),

    # —— 容器（最外层 section）——
    "wrapper": (
        f"font-size: 15px; color: {_TEXT}; line-height: 1.85; "
        "letter-spacing: 0.05em; padding: 0 4px;"
    ),
}


# ── 图片占位符清理 ────────────────────────────────────────────────────────

# article.md 里 fill-images 还没填的占位符。
# 结构：外层 <div class="img-placeholder ..."> 包 2 个 inner div + 1 个 details，再独占一行 </div>
_PLACEHOLDER_DIV = re.compile(
    r'<div class="img-placeholder[^"]*">.*?\n</div>',
    re.DOTALL,
)
_PROMPT_DETAILS = re.compile(r"<details>.*?</details>", re.DOTALL)


def _strip_image_placeholders(md_text: str) -> str:
    """移除 markdown 里残留的图片占位符块（如果有），保留正常的 markdown 图片。"""
    md_text = _PLACEHOLDER_DIV.sub("", md_text)
    md_text = _PROMPT_DETAILS.sub("", md_text)
    return md_text


# ── 关键：把 article.html 的图片 URL 回填到 markdown ────────────────────────

_HTML_IMG_RE = re.compile(
    r'<img[^>]*\bsrc="([^"]+)"[^>]*\balt="([^"]*)"',
    re.IGNORECASE,
)
_HTML_IMG_RE_REV = re.compile(
    r'<img[^>]*\balt="([^"]*)"[^>]*\bsrc="([^"]+)"',
    re.IGNORECASE,
)


def _extract_images_from_html(html: str) -> list[str]:
    """按出现顺序抽出 article.html 里所有图片 src。"""
    srcs: list[str] = []
    # 简单顺序匹配 <img ... src="...">
    for m in re.finditer(r'<img[^>]+\bsrc="([^"]+)"', html, re.IGNORECASE):
        srcs.append(m.group(1))
    return srcs


def _inject_images_into_md(md_text: str, html_srcs: list[str]) -> str:
    """把 article.html 里的图片按顺序回填进 markdown 的占位符位置。"""
    if not html_srcs:
        return _strip_image_placeholders(md_text)

    idx = [0]

    def replace_placeholder(match: re.Match) -> str:
        if idx[0] >= len(html_srcs):
            return ""
        src = html_srcs[idx[0]]
        idx[0] += 1
        # 用标准 markdown 图片语法替换占位符
        return f"\n![]({src})\n"

    md_text = _PLACEHOLDER_DIV.sub(replace_placeholder, md_text)
    return md_text


# ── inline-style 注入器 ───────────────────────────────────────────────────


_TAGS_TO_STYLE = {
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "blockquote", "ul", "ol", "li",
    "pre", "code", "a", "img", "hr",
    "table", "thead", "th", "td",
    "strong", "em", "del",
}


def _inject_styles(html: str) -> str:
    """给所有目标标签的开标签加上 inline style。"""
    # 用 HTMLParser 解析，重新拼装（保留属性、保留嵌套）
    out: list[str] = []
    parser = _StyleInjector(out)
    parser.feed(html)
    parser.close()
    return "".join(out)


class _StyleInjector(HTMLParser):
    """重写所有目标标签，注入 inline style。

    特殊处理：
    - blockquote 内部的 <p> 用 blockquote_p 样式
    - <pre><code> 里的 <code> 用 pre_code 样式
    """

    def __init__(self, out: list[str]) -> None:
        # convert_charrefs=False：保留原始 &amp; 等，不解码
        super().__init__(convert_charrefs=False)
        self._out = out
        self._in_blockquote = 0
        self._in_pre = 0

    def _write(self, s: str) -> None:
        self._out.append(s)

    def handle_starttag(self, tag, attrs):
        self._write(self._render_tag(tag, attrs, self_closing=False))
        if tag == "blockquote":
            self._in_blockquote += 1
        elif tag == "pre":
            self._in_pre += 1

    def handle_startendtag(self, tag, attrs):
        # <img />, <hr />, <br />
        self._write(self._render_tag(tag, attrs, self_closing=True))

    def handle_endtag(self, tag):
        if tag == "blockquote" and self._in_blockquote > 0:
            self._in_blockquote -= 1
        elif tag == "pre" and self._in_pre > 0:
            self._in_pre -= 1
        self._write(f"</{tag}>")

    def handle_data(self, data):
        self._write(data)

    def handle_entityref(self, name):
        self._write(f"&{name};")

    def handle_charref(self, name):
        self._write(f"&#{name};")

    def handle_comment(self, data):
        # 注释丢掉，微信不支持
        pass

    def _render_tag(self, tag, attrs, self_closing: bool) -> str:
        # 选样式
        style_key = tag
        if tag == "p" and self._in_blockquote > 0:
            style_key = "blockquote_p"
        elif tag == "code" and self._in_pre > 0:
            style_key = "pre_code"

        style = THEME.get(style_key, "")

        # 合并已有 style
        attr_pairs: list[tuple[str, str | None]] = []
        existing_style = ""
        for k, v in attrs:
            if k == "style":
                existing_style = v or ""
            elif k == "class":
                # 微信不认 class，丢掉
                continue
            elif k == "id":
                # id 也丢掉
                continue
            else:
                attr_pairs.append((k, v))

        merged_style = "; ".join(s for s in (style, existing_style) if s)
        if merged_style and tag in _TAGS_TO_STYLE:
            attr_pairs.append(("style", merged_style))

        # 拼出标签
        attrs_str = "".join(
            f' {k}="{_attr_escape(v)}"' if v is not None else f" {k}"
            for k, v in attr_pairs
        )
        if self_closing:
            return f"<{tag}{attrs_str} />"
        return f"<{tag}{attrs_str}>"


def _attr_escape(v: str) -> str:
    return (
        v.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ── 对外主入口 ────────────────────────────────────────────────────────────


def render_markdown_to_wechat(md_text: str, html_for_images: str = "") -> str:
    """把 markdown 文本渲染成微信 inline-style HTML。

    参数:
        md_text: 原始 markdown 内容
        html_for_images: 可选的 article.html，用于按顺序把图片回填到占位符
    """
    # 1) 把图片从 HTML 回填进 markdown
    if html_for_images:
        srcs = _extract_images_from_html(html_for_images)
        md_text = _inject_images_into_md(md_text, srcs)
    else:
        md_text = _strip_image_placeholders(md_text)

    # 2) 跳过首个 h1（微信会自动用标题），避免重复
    md_text = re.sub(r"^# .+\n", "", md_text, count=1, flags=re.MULTILINE)

    # 3) 剥掉 AI 味重的"核心观点"块（## 核心观点 → 直到下一个 --- 或下一个 ## 之前）
    md_text = re.sub(
        r"^##\s+核心观点\s*\n.*?(?=^---\s*$|^##\s+)",
        "",
        md_text,
        count=1,
        flags=re.MULTILINE | re.DOTALL,
    )
    # 顺便清掉残留的孤立 --- 分隔行（紧跟核心观点删除后留下的）
    md_text = re.sub(r"^---\s*\n\s*\n(?=##\s+)", "", md_text, count=1, flags=re.MULTILINE)

    # 3) Markdown → HTML
    md = _md.Markdown(
        extensions=[
            "extra",        # 表格、删除线、围栏代码
            "sane_lists",
            "nl2br",        # 中文文章习惯单换行就分段（按需）
        ],
        output_format="html5",
    )
    raw_html = md.convert(md_text)

    # 4) 注入 inline style
    styled = _inject_styles(raw_html)

    # 5) 用一个最外层 <section> 套住，写死字号和行高，作为兜底
    wrapper_style = THEME["wrapper"]
    return f'<section style="{wrapper_style}">{styled}</section>'
