"""Citation formatter — turns raw search results into numbered references."""

from __future__ import annotations
from typing import List, Dict


def format_citations(sources: List[Dict]) -> str:
    """Format a list of search results as Markdown footnotes."""
    if not sources:
        return ""
    lines = ["\n---\n**References**\n"]
    for i, src in enumerate(sources, 1):
        title = src.get("title", "Untitled")
        url = src.get("href", src.get("url", "#"))
        lines.append(f"[{i}] [{title}]({url})")
    return "\n".join(lines)


def inline_cite(text: str, sources: List[Dict]) -> str:
    """Append inline citation numbers to sentences mentioning source keywords."""
    for i, src in enumerate(sources, 1):
        title_words = [w for w in src.get("title", "").lower().split() if len(w) > 4]
        for word in title_words[:2]:
            text = text.replace(word, f"{word} [{i}]", 1)
    return text
