from typing import List

import httpx
import trafilatura

from aiwriter.models import ScrapedContent


def scrape_url(url: str, timeout: int = 30) -> ScrapedContent:
    """Scrape a URL. Falls back to Jina Reader if trafilatura fails."""
    # --- Attempt 1: trafilatura ---
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            result = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=True,
                no_fallback=False,
                favor_precision=False,
            )
            if result and len(result.strip()) >= 200:
                metadata = trafilatura.extract_metadata(downloaded)
                title = (metadata.title if metadata and metadata.title else "") or url
                text = result.strip()
                return ScrapedContent(
                    url=url,
                    title=title,
                    text=text,
                    word_count=len(text.split()),
                    success=True,
                )
    except Exception:
        pass  # Fall through to Jina Reader

    # --- Attempt 2: Jina Reader fallback ---
    try:
        jina_url = f"https://r.jina.ai/{url}"
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(
                jina_url,
                headers={"Accept": "text/plain", "X-Return-Format": "text"},
            )
            response.raise_for_status()
            text = response.text.strip()

        if not text or len(text) < 50:
            return ScrapedContent(
                url=url,
                title=url,
                text="",
                word_count=0,
                success=False,
                error="No content returned from Jina Reader",
            )

        # Attempt to extract a title from the first line if Jina provides it
        lines = text.splitlines()
        title = url
        if lines and lines[0].startswith("Title:"):
            title = lines[0].replace("Title:", "").strip()
            # Remove the title line and any blank line immediately following it
            text = "\n".join(lines[1:]).lstrip()

        return ScrapedContent(
            url=url,
            title=title,
            text=text,
            word_count=len(text.split()),
            success=True,
        )

    except httpx.HTTPStatusError as exc:
        return ScrapedContent(
            url=url,
            title=url,
            text="",
            word_count=0,
            success=False,
            error=f"HTTP {exc.response.status_code} from Jina Reader for {url}",
        )
    except Exception as exc:
        return ScrapedContent(
            url=url,
            title=url,
            text="",
            word_count=0,
            success=False,
            error=str(exc),
        )


def scrape_urls(urls: List[str]) -> List[ScrapedContent]:
    """Scrape multiple URLs, returning results for all (including failures)."""
    results: List[ScrapedContent] = []
    for url in urls:
        results.append(scrape_url(url))
    return results
