# 🛡️ Project AURA — Autonomous Multi-Agent Cyber Intelligence

<div align="center">

```
     █████╗ ██╗   ██╗██████╗  █████╗
    ██╔══██╗██║   ██║██╔══██╗██╔══██╗
    ███████║██║   ██║██████╔╝███████║
    ██╔══██║██║   ██║██╔══██╗██╔══██║
    ██║  ██║╚██████╔╝██║  ██║██║  ██║
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
```

**Autonomous Multi-Agent Cyber Intelligence System**

*Powered by CrewAI + Google Gemini 1.5 Flash*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-blueviolet)](https://crewai.com)
[![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-orange?logo=google)](https://ai.google.dev)

</div>

---

## 📖 Overview

**Project AURA** is a production-ready multi-agent threat intelligence system that leverages Google's Gemini 1.5 Flash model through a CrewAI sequential pipeline. It transforms raw cyber threat scenarios into actionable, executive-ready intelligence reports.

### The Pipeline

```
┌─────────────────────┐        ┌─────────────────────┐
│   Threat_Researcher │  ───►  │    SOC_Reporter      │
│                     │        │                       │
│  • Attack Vectors   │        │  • Threat Landscape   │
│  • IOCs & TTPs      │ output │  • Impact Assessment  │
│  • CVE Analysis     │ ────►  │  • Strategic Recs     │
│  • MITRE ATT&CK     │        │  • Business Risk      │
│  • Forensic Data    │        │  • C-Level Summary    │
└─────────────────────┘        └─────────────────────┘
   Senior Threat Intel             Lead SOC Consultant
      Analyst                    (Executive Reporting)
```

## 🚀 Quick Start

### 1. Clone & Navigate

```bash
cd "Project AURA Autonomous Multi-Agent Cyber Intelligence"
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

```bash
cp .env.example .env
```

Edit `.env` and add your Google API key:

```
GOOGLE_API_KEY=your-actual-api-key-here
```

> 🔑 Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 5. Run AURA

```bash
python aura_multiagent.py
```

## 🏗️ Architecture

### Agents

| Agent | Role | Temperature | Purpose |
|-------|------|:-----------:|---------|
| **Threat_Researcher** | Senior Threat Intelligence Analyst | 0.4 | Precise technical extraction of IOCs, TTPs, CVEs |
| **SOC_Reporter** | Lead SOC Consultant | 0.7 | Natural-language executive summary generation |

### Key Design Decisions

- **Gemini 1.5 Flash**: Chosen for its low quota consumption and fast inference, ideal for multi-agent pipelines where two sequential LLM calls are required per run.
- **Sequential Process**: The Reporter *depends* on the Researcher's output — parallel execution would break the intelligence pipeline.
- **No Delegation**: Both agents are set to `allow_delegation=False` to prevent circular delegation loops and ensure deterministic execution order.
- **Dual Temperature**: Lower temperature for factual extraction (0.4), higher for creative executive prose (0.7).

## 📝 Example Usage

```
⟩ Threat Scenario: A sophisticated phishing campaign targeting our finance
  department using lookalike domains and deploying Cobalt Strike beacons
  after initial access via macro-enabled Excel attachments.
```

The system will produce:

1. **Technical Intelligence Report** — Full breakdown with MITRE ATT&CK mapping
2. **Executive Summary** — 3-paragraph C-level briefing with impact assessment and strategic recommendations

## 📁 Project Structure

```
Project AURA/
├── aura_multiagent.py    # Main multi-agent script
├── .env                  # Your API key (git-ignored)
├── .env.example          # API key template
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `GOOGLE_API_KEY is not set` | Create `.env` file with your API key |
| `crewai is not installed` | Run `pip install -r requirements.txt` |
| `429 / Quota exceeded` | Wait a few minutes; Gemini 1.5 Flash has generous free-tier limits |
| `API key invalid` | Verify your key at [Google AI Studio](https://aistudio.google.com) |

## 👤 Credits

**Architect & Developer:** Nicky Hadfat Sugianto ([@JustNickyH](https://github.com/JustNickyH))

---

<div align="center">

*Built with 🔒 by JustNickyH — Defending the digital frontier, one agent at a time.*

</div>
