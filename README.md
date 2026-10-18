> **NOTE:** This repository is an archival lab or partial prototype. It is not actively maintained and should not be used as a reference for production-grade deployments or performance benchmarks.


# Research Assistant Crew

[![Release](https://img.shields.io/github/v/release/SumitDalavi/research-assistant-crew?color=blue&logo=github)](https://github.com/SumitDalavi/research-assistant-crew/releases)
[![Release Workflow](https://github.com/SumitDalavi/research-assistant-crew/actions/workflows/release.yml/badge.svg)](https://github.com/SumitDalavi/research-assistant-crew/actions/workflows/release.yml)
[![SBOM](https://img.shields.io/badge/SBOM-SPDX%20JSON-blueviolet?logo=spdx)](https://github.com/SumitDalavi/research-assistant-crew/releases)

[![Release](https://img.shields.io/github/v/release/SumitDalavi/research-assistant-crew?color=blue&logo=github)](https://github.com/SumitDalavi/research-assistant-crew/releases)
[![SBOM](https://img.shields.io/badge/SBOM-SPDX%20JSON-blueviolet?logo=spdx)](https://github.com/SumitDalavi/research-assistant-crew/releases)

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


## CI & Reliability Updates (August 2026)

- **CI Pipeline Remediation:** Successfully resolved all CI/CD pipeline failures and established baseline CI workflows.
- **Specific Fix:** Added and configured robust GitHub Actions workflows for automated testing, linting, and formatting.
- **Status:** 🟩 Passing

## Release & Security Verification

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
gh release view v0.1.0 --repo SumitDalavi/research-assistant-crew

# Download and inspect SBOM
gh release download v0.1.0 --repo SumitDalavi/research-assistant-crew --pattern "sbom.spdx.json"
cat sbom.spdx.json | jq .
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Runbook](docs/runbook.md)
- [Decisions](docs/decisions.md)
- [Changelog](docs/changelog.md)