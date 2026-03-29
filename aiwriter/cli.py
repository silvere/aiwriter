from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(help="AIWriter - AI驱动的文章写作工具")
console = Console()


@app.command()
def write(
    topic: str = typer.Option(..., "--topic", "-t", help="文章主题或关键词"),
    urls: List[str] = typer.Option([], "--url", "-u", help="参考链接（可多次使用）"),
    style: Optional[str] = typer.Option(None, "--style", "-s", help="文章风格: wechat 或 xiaohongshu"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="覆盖输出目录（默认使用vault路径）"),
) -> None:
    """生成一篇深度分析文章并保存到 Obsidian vault。"""
    from aiwriter.config import load_config
    from aiwriter.pipeline import run_pipeline

    config = load_config()
    if style:
        config.style.default = style

    run_pipeline(topic=topic, urls=urls, config=config)


@app.command()
def check() -> None:
    """检查配置和API Key状态。"""
    from aiwriter.config import load_config

    config = load_config()

    console.print(Panel("[bold]AIWriter 配置状态[/bold]", expand=False))

    # Vault info
    vault_table = Table(show_header=False, box=None, padding=(0, 2))
    vault_table.add_column("Key", style="bold cyan")
    vault_table.add_column("Value")
    vault_table.add_row("Vault 路径", str(config.vault.path))
    vault_table.add_row("文章目录", config.vault.articles_folder)
    vault_table.add_row("图片目录", config.vault.images_folder)
    vault_table.add_row("默认风格", config.style.default)
    vault_table.add_row("默认语言", config.style.default_language)
    vault_table.add_row("写作模型", config.llm.writing_model)
    vault_table.add_row("辅助模型", config.llm.auxiliary_model)
    console.print(vault_table)

    console.print()

    # API key status
    api_table = Table(title="API Key 状态", show_header=True)
    api_table.add_column("服务", style="bold")
    api_table.add_column("状态")
    api_table.add_column("功能")

    def _status(flag: bool) -> str:
        return "[green]已配置[/green]" if flag else "[red]未配置[/red]"

    api_table.add_row("Anthropic (Claude)", _status(config.has_anthropic), "文章写作")
    api_table.add_row("OpenAI (GPT / DALL-E)", _status(config.has_openai), "文章写作 / AI配图")
    api_table.add_row("Tavily", _status(config.has_tavily), "联网搜索")
    api_table.add_row("Unsplash", _status(config.has_unsplash), "高质量图片")
    api_table.add_row("Pexels", _status(config.has_pexels), "高质量图片")

    console.print(api_table)

    if not config.has_anthropic and not config.has_openai:
        console.print(
            "\n[bold yellow]警告:[/bold yellow] 未配置任何写作 API Key（Anthropic 或 OpenAI），"
            "无法生成文章。\n请在 .env 中设置 ANTHROPIC_API_KEY 或 OPENAI_API_KEY。"
        )


if __name__ == "__main__":
    app()
