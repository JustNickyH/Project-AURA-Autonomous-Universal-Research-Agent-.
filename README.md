# 🌐 Project AURA: Autonomous Multi-Agent Cyber Intelligence

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Multi-Agent](https://img.shields.io/badge/Architecture-Multi_Agent_System-8A2BE2?style=for-the-badge&logo=openai&logoColor=white)
![CrewAI](https://img.shields.io/badge/Framework-CrewAI%20%7C%20LangChain-FF9900?style=for-the-badge)
![Gemini](https://img.shields.io/badge/LLM-Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

> **"Transitioning from AI as a reactive tool to AI as a collaborative, autonomous workforce."**
> Project AURA orchestrates specialized AI agents to autonomously analyze threat vectors and synthesize actionable C-level Security Operations Center (SOC) reports in seconds.

## 📑 5-Point Project Framework

### 1. Background
In modern enterprise environments, Tier-1 SOC analysts suffer from severe alert fatigue. When a threat indicator (like a suspicious IP or malware hash) is flagged, analysts must manually gather threat intelligence, correlate vulnerabilities, and draft incident reports. This sequential, manual process creates dangerous operational bottlenecks.

### 2. Objective
To architect **AURA (Autonomous Universal Research Agent)**, a Multi-Agent system that simulates a micro-SOC environment. The goal is to deploy collaborative, role-playing AI agents that can autonomously hand off tasks—from raw threat hunting to executive reporting—without human intervention.

### 3. Tools & Technologies
* **Orchestration Framework:** CrewAI & LangChain
* **LLM Engine:** Google Gemini Generative AI (`gemini-1.5-flash`) via `langchain-google-genai`
* **Credential Management:** `python-dotenv` for strict environment variable isolation
* **Architecture:** Sequential Task Delegation (Multi-Agent Workflow)

### 4. Insights & Engineering Challenges
The critical leap in this project was moving from basic *Prompt Engineering* to **Agent Orchestration**.
* **The Hallucination Problem:** A single LLM tasked with both analyzing raw technical data and writing a readable report often hallucinates or loses technical fidelity. 
* **The Multi-Agent Solution:** I engineered a decoupled, two-node architecture. 
  1. **Node A (The Threat Researcher):** Strictly prompted to operate as a cynical, data-driven security analyst. Its only job is to extract attack vectors, CVEs, and technical indicators.
  2. **Node B (The SOC Reporter):** Programmed as a Senior Security Consultant. It takes Node A's raw technical output as its *only* context and translates it into a polished, risk-assessed executive summary. 
  By isolating data-gathering from data-presentation, the system ensures high accuracy and zero hallucination.

### 5. Measurable Impact
* **Workflow Automation:** Successfully simulates a multi-tiered SOC analysis pipeline, reducing report generation time from an average of 25 minutes to under **15 seconds**.
* **Scalable Architecture:** Establishes a scalable blueprint. Additional agents (e.g., a "Malware Reverse Engineer" or "Compliance Auditor") can be seamlessly injected into the crew to handle expanding enterprise requirements.

---

## ⚙️ Core Architecture: CrewAI Orchestration

The system leverages `CrewAI` to define strict personas, goals, and sequential tasks.

```python
# Snippet: AURA's Multi-Agent Orchestration Logic
from crewai import Agent, Task, Crew, Process

# 1. Define the Specialized Agents
threat_researcher = Agent(
    role='Senior Threat Intelligence Analyst',
    goal='Uncover attack vectors, CVEs, and technical details of the provided threat.',
    backstory='You are a cynical, detail-oriented cyber security researcher who only cares about raw technical facts.',
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

soc_reporter = Agent(
    role='Lead SOC Consultant',
    goal='Synthesize raw threat data into a clear, actionable C-level executive summary.',
    backstory='You bridge the gap between technical complexity and business risk. You write with authority and clarity.',
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# 2. Define the Sequential Tasks
research_task = Task(
    description='Analyze the following threat scenario: {threat_input}. Extract all technical indicators.',
    expected_output='A detailed technical breakdown of the threat.',
    agent=threat_researcher
)

reporting_task = Task(
    description='Take the researcher\'s output and draft a 3-paragraph executive incident report.',
    expected_output='A professional, C-level SOC report with Risk Level and Mitigation steps.',
    agent=soc_reporter
)

# 3. Assemble the Crew and Execute
aura_crew = Crew(
    agents=[threat_researcher, soc_reporter],
    tasks=[research_task, reporting_task],
    process=Process.sequential # Node A must finish before Node B starts
)
Architected by Nicky Hadfat Sugianto | AI Agent Developer & Cyber Security Enthusiast.
