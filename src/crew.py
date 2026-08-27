"""Research Assistant Crew — three-agent research pipeline."""

import os
from crewai import Agent, Crew, Process
from langchain_openai import ChatOpenAI
from src.tasks import make_tasks
from src.tools.search import web_search

try:
    from duckduckgo_search import DDGS
    from langchain_community.tools import DuckDuckGoSearchRun

    _search_tool = DuckDuckGoSearchRun()
    _TOOLS = [_search_tool]
except Exception:
    _TOOLS = []

_llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY", "dummy"),
)


class ResearchCrew:
    def __init__(self, topic: str):
        self.topic = topic

    def _make_agents(self):
        researcher = Agent(
            role="Senior Research Librarian",
            goal=f"Find 5-8 credible, recent sources on '{self.topic}' and summarise each.",
            backstory="15-year veteran finding primary sources for investigative journalists. "
            "Distrusts SEO farms. Prefers official docs, papers, and first-party blogs.",
            tools=_TOOLS,
            allow_delegation=False,
            llm=_llm,
            verbose=True,
        )
        analyst = Agent(
            role="Critical Research Analyst",
            goal="Extract the 4-6 strongest evidence-backed claims from the search results.",
            backstory="Reviewed thousands of papers for a research lab. Flags unsupported claims. "
            "Never merges two sources' claims without attribution.",
            tools=[],
            allow_delegation=False,
            llm=_llm,
            verbose=True,
        )
        writer = Agent(
            role="Technical Report Writer",
            goal=f"Write a professional Markdown research report on '{self.topic}'.",
            backstory="Former science journalist. Writes for senior engineers — clear, dense, no fluff. "
            "Always includes numbered references.",
            tools=[],
            allow_delegation=False,
            llm=_llm,
            verbose=True,
        )
        return researcher, analyst, writer

    def run(self) -> str:
        researcher, analyst, writer = self._make_agents()
        tasks = make_tasks(researcher, analyst, writer, self.topic)
        crew = Crew(
            agents=[researcher, analyst, writer],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        return str(result)
