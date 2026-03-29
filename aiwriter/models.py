from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List


@dataclass
class ScrapedContent:
    url: str
    title: str
    text: str
    word_count: int
    success: bool
    error: Optional[str] = None


@dataclass
class SearchResult:
    url: str
    title: str
    snippet: str
    content: str
    score: float = 0.0


@dataclass
class ResearchBundle:
    topic: str
    scraped_pages: List[ScrapedContent] = field(default_factory=list)
    search_results: List[SearchResult] = field(default_factory=list)

    def get_all_text(self) -> str:
        """Combine all research text for LLM consumption."""
        parts = []
        for page in self.scraped_pages:
            if page.success:
                parts.append(f"[来源: {page.url}]\n标题: {page.title}\n\n{page.text}")
        for result in self.search_results:
            parts.append(
                f"[搜索结果: {result.url}]\n{result.title}\n{result.content or result.snippet}"
            )
        return "\n\n---\n\n".join(parts)


@dataclass
class SectionOutline:
    id: str
    heading: str
    key_points: List[str]
    image_type: str  # "web_search", "data_chart", "ai_generate", "none"
    image_query: str = ""
    estimated_words: int = 300


@dataclass
class ArticleOutline:
    title: str
    hook: str
    sections: List[SectionOutline]
    conclusion: str
    tags: List[str] = field(default_factory=list)


@dataclass
class ImageResult:
    section_id: str
    local_path: Optional[Path]
    attribution: str = ""
    source_url: str = ""
    image_type: str = ""  # "web", "chart", "ai", "placeholder"
    success: bool = True
    alt_text: str = ""


@dataclass
class ArticleSection:
    outline: SectionOutline
    content: str = ""
    image: Optional[ImageResult] = None


@dataclass
class Article:
    outline: ArticleOutline
    sections: List[ArticleSection] = field(default_factory=list)
    platform: str = "wechat"
    slug: str = ""
