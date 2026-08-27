"""CLI + FastAPI entrypoint for the Research Assistant Crew."""

import os, sys
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from src.crew import ResearchCrew
from src.output.formatter import save_report

app = FastAPI(title="Research Assistant Crew", version="1.0.0")


class ResearchRequest(BaseModel):
    topic: str
    save_to_file: bool = True


@app.post("/api/v1/research")
async def research(req: ResearchRequest):
    crew = ResearchCrew(req.topic)
    report = crew.run()
    result = {"topic": req.topic, "report": report}
    if req.save_to_file:
        path = save_report(req.topic, report)
        result["saved_to"] = path
    return result


@app.get("/health")
def health():
    return {"status": "ok", "llm_key_set": bool(os.getenv("OPENAI_API_KEY"))}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        topic = " ".join(sys.argv[2:]) or "AI agent orchestration patterns"
        print(f"\nResearching: {topic}\n")
        crew = ResearchCrew(topic)
        report = crew.run()
        path = save_report(topic, report)
        print(f"\nReport saved to: {path}")
    else:
        uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
