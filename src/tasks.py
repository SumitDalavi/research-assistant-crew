"""CrewAI task definitions for the research pipeline."""
from crewai import Task


def make_tasks(researcher, analyst, writer, topic: str):
	search_task = Task(
		description=(
			f"Search the web thoroughly for '{topic}'. "
			"Find 5-8 credible, recent sources. For each source return: title, URL, and a 1-2 sentence "
			"summary of why it is relevant. Prefer official docs, research papers, and reputable blogs "
			"over aggregator sites."
		),
		expected_output=(
			"A structured list of 5-8 sources with title, URL, and relevance note for each."
		),
		agent=researcher,
	)

	analysis_task = Task(
		description=(
			"Review the search results provided. Extract the 4-6 strongest, most evidence-backed "
			claims about the topic. For each claim, cite which source supports it. "
			"Flag any contradictions or gaps in the evidence. Do NOT invent facts."
		),
		expected_output=(
			"A list of 4-6 key claims with source citations, plus a brief note on any evidence gaps."
		),
		agent=analyst,
		context=[search_task],
	)

	writing_task = Task(
		description=(
			f"Write a comprehensive research report on '{topic}' based on the analysis. "
			"Include: an executive summary (3-4 sentences), key findings as bullet points, "
			"a 2-3 paragraph analysis, and a numbered reference list. "
			"Tone: professional, objective. Format: Markdown."
		),
		expected_output=(
			"A complete Markdown research report with summary, findings, analysis, and references."
		),
		agent=writer,
		context=[search_task, analysis_task],
	)

	return [search_task, analysis_task, writing_task]
