import sys
from dotenv import load_dotenv
from crewai import Crew, Process

# Load environment variables (e.g. OPENAI_API_KEY)
load_dotenv()

from src.agents import search_agent, analysis_agent, writer_agent
from src.tasks import search_task, analyze_task, write_task

def run_crew(topic: str):
    print(f"\n🚀 Initiating Research Assistant Crew for topic: '{topic}'\n")

    # Initialize the Crew
    research_crew = Crew(
        agents=[search_agent, analysis_agent, writer_agent],
        tasks=[search_task, analyze_task, write_task],
        process=Process.sequential,  # Agents run in sequence
        verbose=True
    )

    # Kick off the research process
    result = research_crew.kickoff(inputs={"topic": topic})

    print("\n================================================\n")
    print("📋 FINAL RESEARCH REPORT:")
    print("\n================================================\n")
    print(result)

if __name__ == "__main__":
    # Allow passing a topic via command line arguments
    topic = "State of agentic AI, 2026"
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    
    run_crew(topic)
