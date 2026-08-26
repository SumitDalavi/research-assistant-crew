"""Markdown report formatter for the research crew output."""
from __future__ import annotations
from datetime import datetime
from typing import List, Dict

from src.tools.citation import format_citations


def format_report(topic: str, summary: str, key_claims: List[str], sources: List[Dict]) -> str:
    """Build a structured Markdown research report."""
    date = datetime.utcnow().strftime("%Y-%m-%d")
    claims_md = "\n".join(f"- {c}" for c in key_claims)
    citations = format_citations(sources)

    return f"""# Research Report: {topic}

*Generated: {date} | Sources: {len(sources)}*

---

## Executive Summary

{summary}

## Key Findings

{claims_md}

## Analysis

This report synthesised {len(sources)} sources on **{topic}**. The evidence suggests
several important trends and considerations that stakeholders should be aware of.
Readers are encouraged to consult the original sources for full context.

{citations}
"""


def save_report(topic: str, content: str, output_dir: str = "output") -> str:
    """Save the report as a Markdown file and return the path."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    slug = topic.lower().replace(" ", "-")[:40]
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(output_dir, f"{ts}_{slug}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
