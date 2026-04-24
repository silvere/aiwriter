#!/usr/bin/env python3
"""
md_to_html.py  —  将 article.md + metadata.json 组装进 HTML 模板

用法：
  python3 skills/scripts/md_to_html.py <article_md> [选项]

选项：
  --title       文章标题（覆盖 MD 一级标题）
  --category    分类标签（默认：AI深度报道）
  --date        日期 YYYY-MM-DD（默认：今天）
  --lead        导语
  --conclusion1/2 结论段落
  --out         输出 HTML 路径（默认：同目录 article.html）
"""

import re
import sys
import json
import argparse
from pathlib import Path
from datetime import date

try:
    import markdown as md_lib
    def md_to_html(text):
        return md_lib.markdown(text, extensions=['tables', 'fenced_code'])
except ImportError:
    # 简易降级：处理常见 Markdown 语法
    def md_to_html(text):
        # 代码块
        text = re.sub(r'```[\w]*\n(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
        # 标题
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        # 引用
        text = re.sub(r'^> (.+)$', r'<blockquote><p>\1</p></blockquote>', text, flags=re.MULTILINE)
        # 粗体
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # 列表
        text = re.sub(r'^[-*] (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'(<li>.*?</li>\n)+', lambda m: '<ul>' + m.group(0) + '</ul>', text, flags=re.DOTALL)
        # 有序列表
        text = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        # 水平线
        text = re.sub(r'^---+$', '<hr>', text, flags=re.MULTILINE)
        # 段落（空行分隔，非标签行）
        paragraphs = text.split('\n\n')
        result = []
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            if p.startswith('<'):
                result.append(p)
            else:
                # 行内换行
                p = p.replace('\n', '<br>')
                result.append(f'<p>{p}</p>')
        return '\n\n    '.join(result)


def parse_metadata_from_md(md_text):
    """从 MD 文件头部注释或正文提取元数据"""
    meta = {}
    # 提取一级标题作为 title
    m = re.search(r'^# (.+)$', md_text, re.MULTILINE)
    if m:
        meta['title'] = m.group(1).strip()
    return meta


def extract_body(md_text):
    """去掉 YAML front matter、一级标题、导语注释行，保留正文"""
    # 去掉 YAML front matter
    md_text = re.sub(r'^---\n.*?\n---\n', '', md_text, flags=re.DOTALL)
    # 去掉一级标题
    md_text = re.sub(r'^# .+\n', '', md_text, flags=re.MULTILINE)
    # 去掉 > **发布日期** 这种 meta 行
    md_text = re.sub(r'^> \*\*发布日期\*\*.*\n', '', md_text, flags=re.MULTILINE)
    # 去掉 ## 核心观点 到第一个 --- 之间的内容（由模板单独渲染）
    md_text = re.sub(r'## 核心观点\n\n.*?\n\n---\n\n', '', md_text, flags=re.DOTALL)
    # 去掉 ## 导语 段落
    md_text = re.sub(r'## 导语\n\n.*?\n\n---\n\n', '', md_text, flags=re.DOTALL)
    # 去掉 ## 数据来源 及以后（放 footer）
    md_text = re.sub(r'\n## 数据来源\n.*$', '', md_text, flags=re.DOTALL)
    return md_text.strip()


def extract_sources(md_text):
    """从 ## 数据来源 节提取链接。每条来源独立一行，避免挤成一坨。"""
    m = re.search(r'## 数据来源\n(.*?)$', md_text, re.DOTALL)
    if not m:
        return ''
    links = re.findall(r'\[(.+?)\]\((.+?)\)', m.group(1))
    parts = []
    for name, url in links:
        parts.append(
            f'<div class="footer-source-item">'
            f'<a href="{url}" target="_blank" rel="noopener">{name}</a>'
            f'</div>'
        )
    return '\n      '.join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('md_path', help='article.md 路径')
    parser.add_argument('--title', default='')
    parser.add_argument('--category', default='AI深度报道')
    parser.add_argument('--date', default=str(date.today()))
    parser.add_argument('--lead', default='')
    parser.add_argument('--conclusion1', default='')
    parser.add_argument('--conclusion2', default='')
    parser.add_argument('--out', default='')
    args = parser.parse_args()

    md_path = Path(args.md_path)
    md_text = md_path.read_text(encoding='utf-8')

    # 元数据：CLI 参数 > metadata.json > MD 内提取
    meta_file = md_path.parent / 'metadata.json'
    file_meta = {}
    if meta_file.exists():
        file_meta = json.loads(meta_file.read_text(encoding='utf-8'))

    md_meta = parse_metadata_from_md(md_text)

    def get(key, cli_val, default=''):
        if cli_val:
            return cli_val
        return file_meta.get(key, md_meta.get(key, default))

    title       = get('title',       args.title,       '文章标题')
    category    = get('category',    args.category,    'AI深度报道')
    pub_date    = get('date',        args.date,        str(date.today()))
    lead        = get('lead',        args.lead,        '')
    conclusion1 = get('conclusion1', args.conclusion1, '')
    conclusion2 = get('conclusion2', args.conclusion2, '')

    # 读取 HTML 模板
    template_path = Path(__file__).parent.parent / 'templates' / 'article.html'
    html = template_path.read_text(encoding='utf-8')

    # 替换单行占位符
    html = html.replace('{{TITLE}}',          title)
    html = html.replace('{{CATEGORY}}',       category)
    html = html.replace('{{DATE}}',           pub_date)
    html = html.replace('{{LEAD}}',           lead)
    html = html.replace('{{CONCLUSION_P1}}',  conclusion1)
    html = html.replace('{{CONCLUSION_P2}}',  conclusion2)

    # 转换正文
    body_md   = extract_body(md_text)
    body_html = md_to_html(body_md)

    html = re.sub(
        r'<!-- BODY_START -->.*?<!-- BODY_END -->',
        '<!-- BODY_START -->\n    ' + body_html + '\n    <!-- BODY_END -->',
        html,
        flags=re.DOTALL
    )

    # 来源 footer
    sources_html = extract_sources(md_text)
    if sources_html:
        html = re.sub(
            r'<a href="\{\{SOURCE_URL_1\}\}".*?<!-- 按实际来源数量增减 -->',
            sources_html,
            html,
            flags=re.DOTALL
        )

    # 输出
    out_path = Path(args.out) if args.out else md_path.parent / 'article.html'
    out_path.write_text(html, encoding='utf-8')
    print(f'✅ Written {len(html):,} chars → {out_path}')


if __name__ == '__main__':
    main()
