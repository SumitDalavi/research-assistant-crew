# Research Assistant Crew

[![CI Pipeline](https://github.com/SumitDalavi/research-assistant-crew/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/SumitDalavi/research-assistant-crew/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/SumitDalavi/research-assistant-crew?color=0969da&label=release&logo=github)](https://github.com/SumitDalavi/research-assistant-crew/releases)
[![Release Workflow](https://github.com/SumitDalavi/research-assistant-crew/actions/workflows/release.yml/badge.svg)](https://github.com/SumitDalavi/research-assistant-crew/actions/workflows/release.yml)
[![GHCR Container](https://img.shields.io/badge/ghcr.io-v0.2.0-blue?logo=docker&logoColor=white)](https://github.com/SumitDalavi/research-assistant-crew/pkgs/container/research-assistant-crew)
[![PyPI Wheel](https://img.shields.io/badge/wheel-0.2.0-3776ab?logo=pypi&logoColor=white)](https://github.com/SumitDalavi/research-assistant-crew/releases/tag/v0.2.0)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![SBOM](https://img.shields.io/badge/SBOM-SPDX%202.3-blueviolet?logo=spdx)](https://github.com/SumitDalavi/research-assistant-crew/releases/tag/v0.2.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

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

## 🔒 Release & Security Verification

The project includes an automated DevSecOps release pipeline (`.github/workflows/release.yml`) triggered on semantic version tags (`v*.*.*`).

Each release automatically:
1. Executes test suite gates.
2. Builds the container image.
3. Performs vulnerability scanning via Trivy.
4. Generates an SPDX SBOM (`sbom.spdx.json`) using Anchore Syft.
5. Publishes a GitHub Release with attached SBOM.

### Verifying the Release
```bash
# Verify release via GitHub CLI
gh release view v0.2.0 --repo SumitDalavi/research-assistant-crew

# Download and inspect SBOM
gh release download v0.2.0 --repo SumitDalavi/research-assistant-crew --pattern "sbom.spdx.json"
cat sbom.spdx.json | jq .
```

## 🚀 Progressive Credential Loading & Execution Tiers

This project implements **Progressive Credential Loading (PCL)**, allowing it to run immediately out-of-the-box without external dependencies while seamlessly upgrading as credentials are provided.

### Tier 1: Zero-Config Mock Mode (Default)
Ideal for CI, testing, and rapid local evaluation.
- **Execution:** Run with default configuration (`cp .env.example .env`). Zero API keys, databases, or cloud credentials required.
- **Fallback Behavior:** In-memory caches, deterministic offline heuristics, mock vector embeddings, and local mock storage are automatically used.
- **Health Verification:** Endpoints report `{"mode": "mock"}` for unconfigured dependencies.

### Tier 2: Local Development with Live Services
Connect specific external services while keeping others mocked.
- **Execution:** Provide credentials in `.env` for the services you want active (e.g., `OPENAI_API_KEY, LLM_MODEL`).
- **Progressive Upgrade:** The runtime inspects environment variables on boot and dynamically promotes only configured modules to live mode.
- **Safe Fallback:** Any missing credentials automatically remain on mock fallbacks with no crashes or missing service errors.

### Tier 3: Production Hardened
Enterprise deployment with production-grade backends, security scans, and container distributions.
- **OCI Container Image:** Pre-built, multi-arch image on GitHub Container Registry:
  ```bash
  docker pull ghcr.io/sumitdalavi/research-assistant-crew:v0.2.0
  ```
- **Production Orchestration:** Mount secrets via Kubernetes Secrets or cloud secret managers with atomic config reload support.
- **Release Verification:** Checksums and SPDX SBOM available on [GitHub Releases](https://github.com/SumitDalavi/research-assistant-crew/releases).

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Runbook](docs/runbook.md)
- [Decisions](docs/decisions.md)
- [Changelog](docs/changelog.md)

### Python Package & CLI Installation
Install directly as a standard Python wheel/package:
```bash
pip install .
# Execute research crew CLI:
research-crew --help
```

## 👨‍💻 Author

**Sumit Dalavi** — Senior DevSecOps / Platform Engineer  
[GitHub](https://github.com/SumitDalavi) | [LinkedIn](https://in.linkedin.com/in/sumit-dalavi-762838129)

---
*Built with a focus on robust patterns, not toy demos.*

