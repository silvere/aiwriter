#!/usr/bin/env python3
"""
把文章标题转换为文件系统安全的 slug。
中文直接保留，英文/数字保留，特殊符号转连字符。
用法: python3 slugify.py "2025年大模型竞争格局深度分析"
输出: 2025年大模型竞争格局深度分析
"""
import sys
import re
from datetime import date


def slugify(title: str, max_length: int = 50) -> str:
    # 去除 Markdown 格式（加粗、链接等）
    title = re.sub(r'\*+|#+|`', '', title)
    title = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', title)

    # 保留：中文字符、英文字母、数字、连字符
    slug = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbf\w]', '-', title)

    # 合并连续连字符，去掉首尾
    slug = re.sub(r'-+', '-', slug).strip('-')

    # 截断（按字符，中文一个字算一个）
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')

    return slug


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 如果没有参数，生成带日期的默认 slug
        print(f"article-{date.today().strftime('%Y%m%d')}")
        sys.exit(0)

    title = " ".join(sys.argv[1:])
    print(slugify(title))
