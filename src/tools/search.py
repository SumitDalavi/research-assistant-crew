"""Real web search tool using DuckDuckGo (free, no API key required)."""

from __future__ import annotations
import re
from typing import List, Dict

try:
    from duckduckgo_search import DDGS

    _DDGS_OK = True
except ImportError:
    _DDGS_OK = False


def web_search(query: str, max_results: int = 5) -> List[Dict]:
    """Search the web. Returns list of {title, href, body}."""
    if _DDGS_OK:
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=max_results))
        except Exception as e:
            print(f"[search] DuckDuckGo error ({e}), using mock results")
    # Mock fallback
    return [
        {
            "title": f"Result {i+1}: {query}",
            "href": f"https://example.com/{i}",
            "body": f"Content about {query} — point {i+1}.",
        }
        for i in range(max_results)
    ]


def scrape_url(url: str, max_chars: int = 3000) -> str:
    """Fetch plain text from a URL."""
    try:
        import httpx, re as _re

        resp = httpx.get(
            url,
            timeout=8,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (research-bot)"},
        )
        text = _re.sub(r"<[^>]+>", " ", resp.text)
        text = _re.sub(r"\s+", " ", text).strip()
        return text[:max_chars]
    except Exception as e:
        return f"[scrape error: {e}]"
