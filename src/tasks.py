from crewai import Task
from .agents import search_agent, analysis_agent, writer_agent

# 1. Search Task
search_task = Task(
    description="Research the topic: '{topic}'. Use the web search tool to find 5-8 credible, recent sources. Focus on official documentation, academic papers, or reputable industry blogs.",
    expected_output="A list of 5-8 sources containing the Title, URL, and a 1-sentence relevance note for each.",
    agent=search_agent
)

# 2. Analysis Task
analyze_task = Task(
    description="Review the sources provided by the Search Agent. Extract the 3-5 strongest claims from these sources.",
    expected_output="A list of 3-5 strong claims, each accompanied by the supporting evidence and the URL of the source it came from.",
    agent=analysis_agent,
    context=[search_task]
)

# 3. Write Task
write_task = Task(
    description="Synthesize the claims extracted by the Analysis Agent into a final structured report. Ensure you open directly with the answer (no filler intros) and back it with the provided evidence.",
    expected_output="A Markdown-formatted report containing:\n1. A 2-sentence summary\n2. 3-5 headed sections detailing the claims\n3. A Sources List at the bottom.",
    agent=writer_agent,
    context=[analyze_task]
)
