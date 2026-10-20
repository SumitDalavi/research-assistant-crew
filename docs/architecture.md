# Architecture: Research Assistant Crew
> Maturity: Functional Prototype

This project utilizes a multi-agent orchestration architecture powered by **CrewAI**.

## Flow Diagram

```mermaid
graph TD
    User([User Request: Topic]) --> Manager[Crew Process Engine]
    Manager --> SearchAgent[1. Search Agent]
    
    subgraph Agents
    SearchAgent --> |Retrieves Sources| AnalysisAgent[2. Analysis Agent]
    AnalysisAgent --> |Extracts Claims| WriterAgent[3. Writer Agent]
    end
    
    WriterAgent --> |Final Report| Manager
    Manager --> UserOut([Final Markdown Report])
```

## Design Decisions

### 1. Sequential Hand-Off
We chose CrewAI's `sequential` process model. This forces a strict hub-and-spoke pipeline where the output of one agent becomes the context for the next. This prevents infinite loops or agents talking over each other.

### 2. Separation of Concerns (Role Design)
- **Search Agent (Data Gathering)**: Exclusively has access to the `DuckDuckGoSearchRun` tool. We disabled delegation (`allow_delegation=False`) to prevent the Search Agent from handing off incomplete searches to other agents.
- **Analysis Agent (Data Extraction)**: Has no external tools. Its sole responsibility is reasoning over the Search Agent's output. By isolating this, we force the LLM to focus purely on validation and extraction, improving claim accuracy.
- **Writer Agent (Synthesis)**: Only receives the extracted claims, not the raw search data. This prevents the Writer from "hallucinating" facts that the Analyst didn't explicitly verify.

### 3. Agent Backstories
Giving each agent a distinct persona and explicit constraints (e.g., "you never merge two sources' claims into one without saying so") is what prevents CrewAI agents from blending into one generic voice. The constraints are defined in `src/agents.py`.

## Progressive Credential Loading & Production Architecture (v0.2.0)

This service implements the **Progressive Credential Loading (PCL)** pattern, decoupling development speed from external infrastructure provisioning:

```mermaid
graph LR
    Env[Environment Credentials] -->|Detect Keys & URLs| Detector[Credential Detector]
    Detector -->|No Credentials / Missing| Mock[Mock Mode Factory]
    Detector -->|Valid Credentials Present| Live[Live Provider Factory]
    Mock --> Runtime[Application Core & /health]
    Live --> Runtime
```

### Core Architecture Components
1. **Mode Detection Singleton:** Inspects environment configuration at boot time without hard crashes on missing secrets.
2. **Dual-Mode Factory Wrappers:**
   - **Storage / Cache:** In-process maps or SQLite `:memory:` transparently promote to managed Redis or PostgreSQL when connection strings are supplied.
   - **AI Providers:** Deterministic heuristic generators and local embeddings transparently promote to live OpenAI, Anthropic, or Gemini API clients.
3. **Hot-Reload & Dynamic TLS:** File watchers monitor mounted volume paths (Kubernetes ConfigMaps and Secrets) to update certificates and limit configs atomically without process restarts.
4. **Health & Observability:** The `/health` endpoint exposes real-time runtime mode metadata (`mock` vs `live`) across all backing adapters.
