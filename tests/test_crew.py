"""Tests for the research assistant crew."""
import pytest
from unittest.mock import patch, MagicMock
from src.tools.search import web_search
from src.tools.citation import format_citations, inline_cite
from src.output.formatter import format_report, save_report


def test_web_search_returns_list():
	with patch("src.tools.search._DDGS_OK", False):
		results = web_search("Kubernetes", max_results=3)
	assert isinstance(results, list)
	assert len(results) == 3
	assert "title" in results[0]


def test_format_citations_empty():
	assert format_citations([]) == ""


def test_format_citations_with_sources():
	sources = [{"title": "K8s Docs", "href": "https://k8s.io"}, {"title": "CNCF Blog", "href": "https://cncf.io"}]
	result = format_citations(sources)
	assert "[1]" in result
	assert "K8s Docs" in result
	assert "CNCF Blog" in result


def test_format_report_structure():
	report = format_report(
		topic="GitOps",
		summary="GitOps uses Git as the source of truth.",
		key_claims=["Claim 1", "Claim 2"],
		sources=[{"title": "Flux Docs", "href": "https://fluxcd.io"}],
	)
	assert "# Research Report: GitOps" in report
	assert "Executive Summary" in report
	assert "Key Findings" in report
	assert "References" in report
	assert "Flux Docs" in report


def test_save_report_creates_file(tmp_path):
	content = "# Test\n\nContent here."
	path = save_report("Test Topic", content, output_dir=str(tmp_path))
	import os
	assert os.path.exists(path)
	assert open(path).read() == content


def test_inline_cite_adds_numbers():
	sources = [{"title": "Redis documentation guide", "href": "https://redis.io"}]
	text = "Redis is used for caching in distributed systems."
	result = inline_cite(text, sources)
	assert "[1]" in result
