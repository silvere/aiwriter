from typing import List

from aiwriter.config import Config
from aiwriter.models import ResearchBundle, Article


def run_pipeline(topic: str, urls: List[str], config: Config) -> None:
    """Main pipeline orchestrator. Runs all phases in sequence."""
    from rich.console import Console

    console = Console()

    # Phase 1: Research
    console.print("[bold blue]Phase 1: 研究中...[/bold blue]")
    research = _run_research(topic, urls, config)

    total_sources = len([p for p in research.scraped_pages if p.success]) + len(research.search_results)
    console.print(f"  [green]研究完成:[/green] 获取到 {total_sources} 个来源")

    if research.scraped_pages:
        success = [p for p in research.scraped_pages if p.success]
        failed = [p for p in research.scraped_pages if not p.success]
        console.print(f"  抓取链接: {len(success)} 成功, {len(failed)} 失败")
        for page in failed:
            console.print(f"    [red]✗[/red] {page.url}: {page.error}")

    if research.search_results:
        console.print(f"  搜索结果: {len(research.search_results)} 条")

    # Phase 2: Outline (stub - will be implemented in Phase 2)
    console.print("[bold blue]Phase 2: 生成大纲...[/bold blue]")
    # outline = _run_outline(research, config)

    console.print("[yellow]写作和配图功能正在开发中，敬请期待[/yellow]")


def _run_research(topic: str, urls: List[str], config: Config) -> ResearchBundle:
    from aiwriter.research.scraper import scrape_urls
    from aiwriter.research.searcher import search_topic
    from rich.console import Console

    console = Console()

    bundle = ResearchBundle(topic=topic)

    if urls:
        console.print(f"  抓取 {len(urls)} 个链接...")
        bundle.scraped_pages = scrape_urls(urls)

    if config.has_tavily:
        console.print("  Tavily 联网搜索...")
        bundle.search_results = search_topic(topic, config)

    return bundle
