import pytest
import sys
from unittest.mock import MagicMock, patch
import os

mock_crewai = MagicMock()
mock_crewai.Agent = MagicMock
mock_crewai.Task = MagicMock
mock_crewai.Crew = MagicMock
mock_crewai.Process.sequential = "sequential"
sys.modules["crewai"] = mock_crewai

mock_langchain_openai = MagicMock()
sys.modules["langchain_openai"] = mock_langchain_openai

mock_langchain_community = MagicMock()
mock_langchain_community.tools = MagicMock()
sys.modules["langchain_community"] = mock_langchain_community
sys.modules["langchain_community.tools"] = mock_langchain_community.tools

def mock_decorator(*args, **kwargs):
    def wrapper(func):
        return func
    return wrapper

mock_fastapi = MagicMock()
mock_app = MagicMock()
mock_app.get = mock_decorator
mock_app.post = mock_decorator
mock_fastapi.FastAPI = MagicMock(return_value=mock_app)
sys.modules["fastapi"] = mock_fastapi

mock_pydantic = MagicMock()
mock_pydantic.BaseModel = type("BaseModel", (object,), {})
sys.modules["pydantic"] = mock_pydantic

mock_uvicorn = MagicMock()
sys.modules["uvicorn"] = mock_uvicorn

mock_ddg = MagicMock()
sys.modules["duckduckgo_search"] = mock_ddg

from src.agents import search_agent, analysis_agent, writer_agent
from src.crew import ResearchCrew
from src.tasks import make_tasks
from src.main import app, ResearchRequest, research, health

def test_agents():
    assert search_agent is not None
    assert analysis_agent is not None
    assert writer_agent is not None

def test_tasks():
    tasks = make_tasks("researcher", "analyst", "writer", "AI topic")
    assert len(tasks) == 3

def test_crew():
    crew = ResearchCrew("test topic")
    r, a, w = crew._make_agents()
    assert r is not None
    assert a is not None
    assert w is not None
    
    with patch("src.crew.Crew") as mock_crew_cls:
        mock_instance = MagicMock()
        mock_instance.kickoff.return_value = "Mock Report"
        mock_crew_cls.return_value = mock_instance
        report = crew.run()
        assert report == "Mock Report"

@pytest.mark.asyncio
async def test_main_endpoints():
    # health
    res = health()
    assert res["status"] == "ok"
    
    # research
    req = ResearchRequest()
    req.topic = "test topic"
    req.save_to_file = True
    
    with patch("src.main.ResearchCrew") as mock_crew:
        mock_instance = MagicMock()
        mock_instance.run.return_value = "Mock API Report"
        mock_crew.return_value = mock_instance
        
        with patch("src.main.save_report", return_value="/tmp/mock.md"):
            api_res = await research(req)
            assert api_res["topic"] == "test topic"
            assert api_res["report"] == "Mock API Report"
            assert api_res["saved_to"] == "/tmp/mock.md"

def test_main_cli():
    import runpy
    with patch("sys.argv", ["main.py", "run", "AI", "Agent"]):
        with patch("src.main.ResearchCrew") as mock_crew:
            mock_instance = MagicMock()
            mock_instance.run.return_value = "CLI Report"
            mock_crew.return_value = mock_instance
            with patch("src.main.save_report", return_value="/mock/cli.md"):
                runpy.run_module("src.main", run_name="__main__")

def test_main_uvicorn():
    import runpy
    with patch("sys.argv", ["main.py"]):
        runpy.run_module("src.main", run_name="__main__")
        mock_uvicorn.run.assert_called_once()

def test_formatter_and_citation():
    from src.output.formatter import format_report, save_report
    from src.tools.citation import format_citations, inline_cite
    import tempfile
    
    # citation
    sources = [{"title": "Example Source", "href": "http://example.com"}]
    citations = format_citations(sources)
    assert "[1]" in citations
    assert "Example Source" in citations
    
    empty_citations = format_citations([])
    assert empty_citations == ""
    
    text = inline_cite("The example is great.", sources)
    assert "example [1]" in text
    
    # formatter
    report = format_report("Topic", "Summary", ["Claim 1"], sources)
    assert "# Research Report: Topic" in report
    assert "Summary" in report
    assert "- Claim 1" in report
    assert "Example Source" in report
    
    with tempfile.TemporaryDirectory() as td:
        path = save_report("Topic", report, output_dir=td)
        assert os.path.exists(path)
        with open(path) as f:
            assert "Topic" in f.read()

def test_search():
    from src.tools.search import web_search, scrape_url
    
    import src.tools.search
    src.tools.search._DDGS_OK = False
    
    # Mock DDGS failure / fallback
    res = web_search("test", max_results=1)
    assert len(res) == 1
    assert "Result 1: test" in res[0]["title"]
    
    # Mock scrape URL
    with patch("httpx.get") as mock_get:
        mock_get.return_value.text = "<html><body>Hello world</body></html>"
        text = scrape_url("http://example.com")
        assert "Hello world" in text
        
        mock_get.side_effect = Exception("Failed")
        text = scrape_url("http://example.com")
        assert "[scrape error:" in text
