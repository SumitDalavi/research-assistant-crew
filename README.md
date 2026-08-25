# Research Assistant Crew

An autonomous multi-agent web research and summary pipeline built with CrewAI.

## Overview
This system delegates a research question to three specialized agents, orchestrating a seamless handoff between searching, analyzing, and writing. It cuts manual literature-review time by automating the synthesis of web sources.

## How it works

1. **Manager Agent (Implicit)**: Orchestrates the sequential pipeline.
2. **Search Agent**: Uses DuckDuckGo to pull credible sources.
3. **Analysis Agent**: Extracts key claims and evidence from the search results.
4. **Writer Agent**: Synthesizes the extracted claims into a final structured report.

## Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Copy `.env.example` to `.env` and provide your OpenAI API key:
```bash
OPENAI_API_KEY=sk-...
```

### 3. Run the Crew
```bash
# Run with the default topic
python src/main.py

# Or provide a custom topic
python src/main.py "Impact of WebAssembly on Backend Architecture in 2024"
```
