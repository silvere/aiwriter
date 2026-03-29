#!/usr/bin/env python3
"""
初始化 Obsidian vault 文章目录结构。
用法: python3 setup_vault.py <vault_path> <article_slug>
输出: 创建的路径信息（JSON格式）
"""
import sys
import json
from pathlib import Path
from datetime import date


def find_vault_root(path: Path) -> Path | None:
    """往上查找包含 .obsidian 目录的 vault 根目录。"""
    current = path.resolve()
    for _ in range(5):  # 最多往上找5层
        if (current / ".obsidian").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def setup(vault_path: str, article_slug: str) -> dict:
    given = Path(vault_path).expanduser().resolve()

    if not given.exists():
        return {"ok": False, "error": f"路径不存在: {given}"}

    # 自动向上查找 vault 根目录
    vault = find_vault_root(given)
    if vault is None:
        return {"ok": False, "error": f"找不到 Obsidian vault（在 {given} 及其父目录中均无 .obsidian）"}

    month = date.today().strftime("%Y-%m")

    # 创建目录
    articles_dir = vault / "AI-Articles" / month
    attachments_dir = vault / "attachments" / article_slug

    articles_dir.mkdir(parents=True, exist_ok=True)
    attachments_dir.mkdir(parents=True, exist_ok=True)

    article_path = articles_dir / f"{article_slug}.md"

    return {
        "ok": True,
        "vault": str(vault),
        "article_path": str(article_path),
        "attachments_dir": str(attachments_dir),
        "attachments_relative": f"attachments/{article_slug}",
        "month": month,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"ok": False, "error": "用法: python3 setup_vault.py <vault_path> <article_slug>"}))
        sys.exit(1)

    result = setup(sys.argv[1], sys.argv[2])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["ok"] else 1)
