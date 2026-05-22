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


# ── 主题：温润纸感（warm paper），对长文阅读舒适 ────────────────────────────
#
# 设计思路：
# - 降饱和度：放弃 #1A56DB 这种鲜蓝，改用墨青 #2c4a6b（接近《纽约客》网页正文链接）
# - 暖色锚点：引用、警示用米色 #f6f1e7（纸感）+ 暖棕勾边 #b89968
# - 字体提层级：标题/正文颜色拉开梯度（黑 → 深炭 → 中灰）而非靠 hue
# - 行距放大：line-height 2.0（中文长文阅读最佳）

_INK = "#1c1c1c"           # 标题（接近黑，但更柔和）
_TEXT = "#2c2c2c"          # 正文（炭灰）
_MUTE = "#7a7a7a"           # 辅助文字
_BRAND = "#3b5275"         # 墨青：低饱和稳重，眼睛不累
_BRAND_SOFT = "#5d7494"    # 链接 hover/弱化
_ACCENT_BG = "#f6f1e7"     # 纸色：引用 / 强调块背景
_ACCENT_BORDER = "#b89968" # 暖棕：引用左缘
_DIVIDER = "#d8d4cc"        # 暖灰：分隔线
_CODE_BG = "#f4f1ec"       # 行内代码背景：浅米
_CODE_INK = "#a04848"       # 行内代码：暖红
_PRE_BG = "#252830"        # 块代码：深炭蓝
_PRE_INK = "#e8e2d3"       # 块代码文字：暖象牙

THEME: dict[str, str] = {
    # —— 标题 ——
    "h1": (
        f"font-size: 22px; font-weight: 700; color: {_INK}; "
        "text-align: center; margin: 24px 0 20px; line-height: 1.5; "
        "letter-spacing: 0.02em;"
    ),
    "h2": (
        f"font-size: 19px; font-weight: 700; color: {_INK}; "
        f"margin: 36px 0 18px; padding-left: 12px; "
        f"border-left: 3px solid {_ACCENT_BORDER}; line-height: 1.5; "
        "letter-spacing: 0.02em;"
    ),
    "h3": (
        f"font-size: 16px; font-weight: 700; color: {_BRAND}; "
        "margin: 26px 0 12px; line-height: 1.5; letter-spacing: 0.02em;"
    ),
    "h4": f"font-size: 15px; font-weight: 700; color: {_INK}; margin: 18px 0 10px;",
    "h5": f"font-size: 14px; font-weight: 700; color: {_TEXT}; margin: 16px 0 8px;",
    "h6": f"font-size: 13px; font-weight: 700; color: {_MUTE}; margin: 16px 0 8px;",

    # —— 段落 ——
    "p": (
        f"margin: 16px 0; line-height: 2.0; font-size: 15px; "
        f"color: {_TEXT}; letter-spacing: 0.04em; text-align: justify; "
        "word-spacing: 0.05em;"
    ),

    # —— 强调 ——
    "strong": f"font-weight: 700; color: {_INK};",
    "em": f"font-style: italic; color: {_MUTE};",
    "del": "color: #b0b0b0; text-decoration: line-through;",

    # —— 链接 ——
    "a": (
        f"color: {_BRAND}; text-decoration: none; "
        f"border-bottom: 1px solid {_BRAND_SOFT}; word-break: break-all;"
    ),

    # —— 引用 ——
    "blockquote": (
        f"border-left: 3px solid {_ACCENT_BORDER}; padding: 14px 18px; "
        f"margin: 20px 0; background: {_ACCENT_BG}; "
        f"color: #594a32; font-size: 14px; line-height: 1.9; "
        "border-radius: 0 4px 4px 0;"
    ),
    "blockquote_p": (
        "margin: 0; color: inherit; font-size: inherit; "
        "line-height: inherit; letter-spacing: 0.03em;"
    ),

    # —— 列表 ——
    "ul": "margin: 14px 0; padding-left: 1.5em;",
    "ol": "margin: 14px 0; padding-left: 1.5em;",
    "li": (
        f"margin: 8px 0; line-height: 1.9; color: {_TEXT}; "
        "font-size: 15px; letter-spacing: 0.04em;"
    ),

    # —— 代码 ——
    "code": (
        f"background: {_CODE_BG}; color: {_CODE_INK}; padding: 2px 6px; "
        "border-radius: 3px; font-family: 'SFMono-Regular', Consolas, "
        "'Liberation Mono', Menlo, monospace; font-size: 13px; "
        "word-break: break-all;"
    ),
    "pre": (
        f"background: {_PRE_BG}; color: {_PRE_INK}; padding: 16px 18px; "
        "border-radius: 6px; overflow-x: auto; font-size: 13px; "
        "line-height: 1.7; margin: 20px 0;"
    ),
    "pre_code": (
        "background: transparent; color: inherit; padding: 0; "
        "font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', "
        "Menlo, monospace; font-size: 13px;"
    ),

    # —— 图片 ——
    "img": (
        "max-width: 100%; height: auto; display: block; "
        "margin: 20px auto; border-radius: 4px;"
    ),

    # —— 分隔线 ——
    "hr": (
        f"border: none; border-top: 1px solid {_DIVIDER}; margin: 36px 0; "
        "height: 0;"
    ),

    # —— 表格 ——
    "table": (
        "border-collapse: collapse; width: 100%; margin: 20px 0; "
        "font-size: 14px;"
    ),
    "thead": "",
    "th": (
        f"border: 1px solid {_DIVIDER}; padding: 10px 12px; "
        f"background: {_ACCENT_BG}; font-weight: 700; text-align: left; "
        f"color: {_INK};"
    ),
    "td": (
        f"border: 1px solid {_DIVIDER}; padding: 10px 12px; "
        f"color: {_TEXT}; line-height: 1.8;"
    ),

    # —— 容器（最外层 section）——
    "wrapper": (
        f"font-size: 15px; color: {_TEXT}; line-height: 2.0; "
        "letter-spacing: 0.04em; padding: 0 4px;"
    ),

    # —— 自定义：URL 展示 ——
    # 段落上下文里用 <br/> + inline span（段落里 <br/> 不会衍生 bullet）
    "_link_url_line": (
        f"font-size: 12px; color: {_MUTE}; line-height: 1.5; "
        "word-break: break-all; "
        "font-family: 'SFMono-Regular', Consolas, Menlo, monospace;"
    ),

    # —— 自定义：参考文献卡片 ——
    # 数据来源段彻底不走 <ul>/<li>，每条引用一张独立 <section>，
    # 完全脱离微信的 list 解析逻辑，杜绝空 bullet
    "_ref_card": (
        f"margin: 12px 0; padding: 12px 16px; "
        f"background: {_ACCENT_BG}; border-radius: 6px; "
        f"border-left: 3px solid {_ACCENT_BORDER}; "
        "line-height: 1.6;"
    ),
    "_ref_card_title": (
        f"color: {_BRAND}; font-weight: 700; text-decoration: none; "
        f"font-size: 14px; border-bottom: 1px solid {_BRAND_SOFT};"
    ),
    "_ref_card_url": (
        f"display: block; margin-top: 6px; font-size: 11px; "
        f"color: {_MUTE}; line-height: 1.5; word-break: break-all; "
        "font-family: 'SFMono-Regular', Consolas, Menlo, monospace;"
    ),

    # —— 自定义：未填充图片占位 ——
    "_missing_image": (
        f"margin: 20px 0; padding: 24px 20px; background: {_ACCENT_BG}; "
        f"border: 1px dashed {_ACCENT_BORDER}; border-radius: 6px; "
        f"color: {_MUTE}; font-size: 13px; line-height: 1.7; "
        "text-align: center;"
    ),
    "_missing_image_label": (
        f"display: block; font-weight: 700; color: #8b6f47; "
        "margin-bottom: 8px; letter-spacing: 0.1em; font-size: 12px;"
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


# fill-images 产出的 chart 块特征：起头是 `<div style="margin:32px 0;background:#fff`
# chart 内部嵌套多层 div，普通正则匹配不准，必须做 div 平衡计数
_CHART_OPEN_MARKER = '<div style="margin:32px 0;background:#fff'

# figure 块（concept 图片）正则
_FIGURE_BLOCK_RE = re.compile(
    r'<figure\s+style="margin:32px 0[^"]*"[^>]*>.*?</figure>',
    re.DOTALL | re.IGNORECASE,
)


def _extract_balanced_div(html: str, start: int) -> int | None:
    """从 start 位置（指向 `<div`）开始，找到对应闭合 </div> 的位置（不含）。
    返回闭合 </div> 之后的位置；找不到平衡返回 None。
    """
    depth = 0
    i = start
    n = len(html)
    open_re = re.compile(r"<div\b", re.IGNORECASE)
    close_re = re.compile(r"</div>", re.IGNORECASE)
    while i < n:
        m_open = open_re.search(html, i)
        m_close = close_re.search(html, i)
        if m_close is None:
            return None
        if m_open is not None and m_open.start() < m_close.start():
            depth += 1
            i = m_open.end()
        else:
            depth -= 1
            i = m_close.end()
            if depth == 0:
                return i
    return None


def _extract_charts_in_order(html: str) -> list[str]:
    """按出现顺序抽出 article.html 里所有 diagram chart HTML 块（div 平衡）。"""
    charts: list[str] = []
    pos = 0
    while True:
        start = html.find(_CHART_OPEN_MARKER, pos)
        if start == -1:
            break
        end = _extract_balanced_div(html, start)
        if end is None:
            break
        charts.append(html[start:end])
        pos = end
    return charts


def _iter_visual_blocks_in_order(html: str) -> list[tuple[int, str]]:
    """按出现顺序返回所有视觉块的 (位置, HTML)；用于判断 chart 与 figure 顺序。"""
    blocks: list[tuple[int, str]] = []
    # figure 块用正则
    for m in _FIGURE_BLOCK_RE.finditer(html):
        blocks.append((m.start(), m.group(0)))
    # chart 块走平衡计数
    pos = 0
    while True:
        start = html.find(_CHART_OPEN_MARKER, pos)
        if start == -1:
            break
        end = _extract_balanced_div(html, start)
        if end is None:
            break
        blocks.append((start, html[start:end]))
        pos = end
    blocks.sort(key=lambda x: x[0])
    return blocks


# fill-images 处理 diagram 时没改写 md，留下的孤立占位符
_AIWRITER_RESIDUAL_PLACEHOLDER = "<<__AIWRITER_PLACEHOLDER__>>"


def _replace_aiwriter_placeholders(md_text: str, charts: list[str]) -> str:
    """把 article.md 里残留的 <<__AIWRITER_PLACEHOLDER__>> 按顺序换成 chart HTML。

    fill-images 处理 concept 类时改写了 md（→ `![]()`），但 diagram 类
    走 HTML inline chart 路径，没构造 md replacement，placeholder 留下。
    本函数按 article.html 里 chart 出现顺序，把每个残留 placeholder 替换
    为对应的 chart raw HTML 块（独立段落，前后空行，markdown 不解析内部）。
    """
    if _AIWRITER_RESIDUAL_PLACEHOLDER not in md_text:
        return md_text

    idx = [0]

    def repl(_m: re.Match) -> str:
        if idx[0] < len(charts):
            block = charts[idx[0]]
            idx[0] += 1
            # 前后留空行让 markdown 把它识别为 HTML 块（不被加入段落）
            return f"\n\n{block}\n\n"
        # chart 不够：清掉残留 placeholder，避免变成难看的文本
        return ""

    return re.sub(
        re.escape(_AIWRITER_RESIDUAL_PLACEHOLDER), repl, md_text
    )


_PLACEHOLDER_TYPE_RE = re.compile(r'img-placeholder\s+([a-z]+)"')
_PLACEHOLDER_LABEL_RE = re.compile(r'img-placeholder-label">([^<]+)</div>')


def _inject_images_into_md(md_text: str, html_srcs: list[str]) -> str:
    """把 article.html 里的图片按顺序回填进 markdown 的占位符位置。

    未填充的占位符 → 降级为一个可见的"配图待补"提示块（HTML inline-style），
    让发文的人在草稿里能一眼看到缺图位置，而不是静默吞掉。
    """
    idx = [0]

    def replace_placeholder(match: re.Match) -> str:
        block = match.group(0)

        # 还有图就按顺序填
        if idx[0] < len(html_srcs):
            src = html_srcs[idx[0]]
            idx[0] += 1
            return f"\n![]({src})\n"

        # 否则：渲染成"配图占位"提示块（直接给 inline-style HTML，跳过 markdown）
        kind_m = _PLACEHOLDER_TYPE_RE.search(block)
        label_m = _PLACEHOLDER_LABEL_RE.search(block)
        kind = kind_m.group(1) if kind_m else "concept"
        label = label_m.group(1) if label_m else "配图"
        icon = "📊" if kind == "diagram" else "🎨"
        box_style = THEME["_missing_image"]
        label_style = THEME["_missing_image_label"]
        return (
            f'\n<section style="{box_style}">'
            f'<span style="{label_style}">{icon} {label}（待补）</span>'
            f'<span>此处原计划放一张{label}，自动生成未成功，可在草稿箱手动插入。</span>'
            f"</section>\n"
        )

    return _PLACEHOLDER_DIV.sub(replace_placeholder, md_text)


# 识别参考文献段：## 数据来源 / ## 参考文献 / ## 参考资料 / ## 相关链接 / ## 延伸阅读 / ## 引用
_REFS_HEADING_PATTERN = (
    r"数据来源|参考文献|参考资料|相关链接|延伸阅读|引用|参考"
)
_REFS_SECTION_RE = re.compile(
    rf"(^##\s+(?:{_REFS_HEADING_PATTERN})\s*\n)(.+?)(?=\n##\s+|\Z)",
    re.MULTILINE | re.DOTALL,
)
_REF_ITEM_RE = re.compile(
    r"^\s*[-*+]\s+\[([^\]]+)\]\(([^)]+)\)\s*$",
    re.MULTILINE,
)

# 用纯字母占位，避免 markdown 把 `<<` / `__` 当成转义或加粗处理
_REFS_PLACEHOLDER = "AIWRPLACEHOLDERREFSBLOCKAIWR"


def _extract_references_section(md_text: str) -> tuple[str, str]:
    """把参考文献段从 markdown 里抠出来，留一个 placeholder。

    返回 (placeholder_aware_md, refs_html)。
    refs_html 是已渲染好的 HTML 卡片串，会在 inline-style 注入后直接替换 placeholder。
    """
    match = _REFS_SECTION_RE.search(md_text)
    if not match:
        return md_text, ""

    heading_line = match.group(1).strip()
    body = match.group(2)
    items = _REF_ITEM_RE.findall(body)
    if not items:
        return md_text, ""

    # 构建 HTML 卡片串
    card_style = THEME["_ref_card"]
    title_style = THEME["_ref_card_title"]
    url_style = THEME["_ref_card_url"]
    h2_style = THEME["h2"]

    cards: list[str] = [
        f'<h2 style="{h2_style}">{heading_line.lstrip("# ").strip()}</h2>'
    ]
    for title, url in items:
        # html-escape 必要字符
        title_esc = (
            title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        url_esc = url.replace("&", "&amp;").replace('"', "&quot;")
        cards.append(
            f'<section style="{card_style}">'
            f'<a href="{url_esc}" style="{title_style}">{title_esc}</a>'
            f'<span style="{url_style}">{url_esc}</span>'
            f"</section>"
        )
    refs_html = "\n".join(cards)

    # markdown 里把整段替换成 placeholder
    new_md = _REFS_SECTION_RE.sub(f"\n\n{_REFS_PLACEHOLDER}\n\n", md_text, count=1)
    return new_md, refs_html


_EXTERNAL_LINK_RE = re.compile(
    r'(<a\b[^>]*\bhref="(https?://[^"]+)"[^>]*>)([^<]+)(</a>)',
    re.IGNORECASE,
)


def _append_url_to_external_links(html: str) -> str:
    """微信外链不可点击，在每个外链文本下方追加一行可读的 URL。

    仅处理"链接文字 ≠ URL"的情况（避免重复显示）。
    """
    url_style = THEME["_link_url_line"]

    def repl(m: re.Match) -> str:
        full_open, url, text, close = m.group(1), m.group(2), m.group(3), m.group(4)
        # 文字本身就是这个 URL → 不重复
        text_stripped = text.strip()
        if text_stripped == url or text_stripped == url.rstrip("/"):
            return m.group(0)
        # 用 <br/> 强制换行 + inline span 显示 URL，避免 <li> 内出现空 bullet
        return f'{full_open}{text}{close}<br/><span style="{url_style}">{url}</span>'

    return _EXTERNAL_LINK_RE.sub(repl, html)


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
        # 1.5) 把 fill-images 残留的 <<__AIWRITER_PLACEHOLDER__>>（仅 diagram 类）
        #      按顺序换成 article.html 里的 chart HTML 块 → 位置精确
        charts = _extract_charts_in_order(html_for_images)
        md_text = _replace_aiwriter_placeholders(md_text, charts)
    else:
        md_text = _strip_image_placeholders(md_text)
        md_text = _replace_aiwriter_placeholders(md_text, [])

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

    # 3.5) 抽出"数据来源/参考文献"段，用 placeholder 占位
    md_text, refs_html = _extract_references_section(md_text)

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

    # 5) 外链下方追加可读 URL（微信外链不可点击）
    styled = _append_url_to_external_links(styled)

    # 6) （已移除：之前的"chart 跟在 img 后面"位置注入）
    #     现在改用 _replace_aiwriter_placeholders 在 markdown 阶段精准位置插入

    # 7) 把参考文献 placeholder 替换为预渲染的卡片串
    if refs_html:
        # placeholder 在 markdown 阶段会被包成 <p>placeholder</p>，整段替换
        styled = re.sub(
            rf"<p[^>]*>\s*{re.escape(_REFS_PLACEHOLDER)}\s*</p>",
            refs_html,
            styled,
        )
        # 兜底：未被包 <p> 时也替换
        styled = styled.replace(_REFS_PLACEHOLDER, refs_html)

    # 8) 用一个最外层 <section> 套住，写死字号和行高，作为兜底
    wrapper_style = THEME["wrapper"]
    return f'<section style="{wrapper_style}">{styled}</section>'
