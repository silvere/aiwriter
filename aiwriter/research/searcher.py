from typing import List, Optional

import httpx

from aiwriter.config import Config
from aiwriter.models import SearchResult

TAVILY_API_URL = "https://api.tavily.com/search"


def search_topic(
    topic: str,
    config: Config,
    extra_keywords: Optional[List[str]] = None,
) -> List[SearchResult]:
    """Search Tavily for topic. Returns list of SearchResult.

    Returns an empty list (without raising) if Tavily is not configured or
    if the request fails.
    """
    if not config.has_tavily or not config.tavily_api_key:
        return []

    query = topic
    if extra_keywords:
        query = f"{topic} {' '.join(extra_keywords)}"

    payload = {
        "api_key": config.tavily_api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": config.search.max_results,
        "include_raw_content": True,
    }

    try:
        with httpx.Client(timeout=60) as client:
            response = client.post(TAVILY_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as exc:
        # Surface the error message but do not raise; caller handles empty list
        from rich.console import Console
        Console().print(
            f"[yellow]Warning:[/yellow] Tavily search failed with HTTP "
            f"{exc.response.status_code}: {exc.response.text[:200]}"
        )
        return []
    except Exception as exc:
        from rich.console import Console
        Console().print(f"[yellow]Warning:[/yellow] Tavily search error: {exc}")
        return []

    results: List[SearchResult] = []
    for item in data.get("results", []):
        results.append(
            SearchResult(
                url=item.get("url", ""),
                title=item.get("title", ""),
                snippet=item.get("content", ""),
                content=item.get("raw_content", "") or item.get("content", ""),
                score=float(item.get("score", 0.0)),
            )
        )

    return results
