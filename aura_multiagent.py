#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          PROJECT AURA v1.0                                 ║
║            Autonomous Multi-Agent Cyber Intelligence System                ║
║                                                                            ║
║  Developed by: Nicky Hadfat Sugianto (JustNickyH)                         ║
║  Framework   : CrewAI + LangChain Google GenAI                            ║
║  Model       : Gemini 1.5 Flash                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

A production-ready multi-agent threat intelligence pipeline that extracts,
analyzes, and synthesizes cyber threat data into executive-ready reports.

Usage:
    python aura_multiagent.py
"""

from __future__ import annotations

import os
import sys
import textwrap
import time
from datetime import datetime, timezone

# ──────────────────────────────────────────────────────────────────────────────
# ASCII Banner
# ──────────────────────────────────────────────────────────────────────────────

BANNER = r"""
[38;5;51m
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║     █████╗ ██╗   ██╗██████╗  █████╗                                  ║
    ║    ██╔══██╗██║   ██║██╔══██╗██╔══██╗                                 ║
    ║    ███████║██║   ██║██████╔╝███████║                                  ║
    ║    ██╔══██║██║   ██║██╔══██╗██╔══██║                                  ║
    ║    ██║  ██║╚██████╔╝██║  ██║██║  ██║                                  ║
    ║    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝                               ║
    ║                                                                       ║
    ║    ┌─────────────────────────────────────────────────────────────┐    ║
    ║    │  AUTONOMOUS  MULTI-AGENT  CYBER  INTELLIGENCE  SYSTEM      │    ║
    ║    └─────────────────────────────────────────────────────────────┘    ║
    ║                                                                       ║
    ║    [38;5;245m◈  Version   :  1.0.0-production[38;5;51m                                   ║
    ║    [38;5;245m◈  Framework :  CrewAI + LangChain Google GenAI[38;5;51m                     ║
    ║    [38;5;245m◈  Model     :  Gemini 1.5 Flash[38;5;51m                                   ║
    ║    [38;5;245m◈  Architect :  Nicky Hadfat Sugianto (JustNickyH)[38;5;51m                 ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
[0m"""

# ANSI color helpers
CYAN = "\033[38;5;51m"
GRAY = "\033[38;5;245m"
GREEN = "\033[38;5;46m"
RED = "\033[38;5;196m"
YELLOW = "\033[38;5;226m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"


def print_status(icon: str, message: str, color: str = CYAN) -> None:
    """Print a formatted status message."""
    print(f"  {color}{icon}{RESET}  {message}")


def print_separator() -> None:
    """Print a visual separator line."""
    print(f"  {GRAY}{'─' * 68}{RESET}")


def print_phase(phase_name: str) -> None:
    """Print a phase header."""
    print()
    print(f"  {CYAN}◆ ─── {BOLD}{phase_name}{RESET}{CYAN} ─────────────────────────────────────────{RESET}")
    print()


# ──────────────────────────────────────────────────────────────────────────────
# Dependency & Environment Validation
# ──────────────────────────────────────────────────────────────────────────────

def validate_environment() -> str:
    """
    Validate that all required dependencies are installed and the
    GOOGLE_API_KEY environment variable is set.

    Returns:
        The validated GOOGLE_API_KEY string.

    Raises:
        SystemExit: If dependencies are missing or the API key is not set.
    """
    print_phase("ENVIRONMENT VALIDATION")

    # --- Check python-dotenv ---
    try:
        from dotenv import load_dotenv  # noqa: F811
        print_status("✓", "python-dotenv ............ loaded", GREEN)
    except ImportError:
        print_status("✗", "python-dotenv is not installed.", RED)
        print_status("→", "Run: pip install python-dotenv", YELLOW)
        sys.exit(1)

    # --- Check crewai ---
    try:
        import crewai  # noqa: F401
        print_status("✓", f"crewai ................... v{crewai.__version__}", GREEN)
    except ImportError:
        print_status("✗", "crewai is not installed.", RED)
        print_status("→", "Run: pip install crewai", YELLOW)
        sys.exit(1)

    # --- Check langchain-google-genai ---
    try:
        import langchain_google_genai  # noqa: F401
        print_status("✓", "langchain-google-genai ... loaded", GREEN)
    except ImportError:
        print_status("✗", "langchain-google-genai is not installed.", RED)
        print_status("→", "Run: pip install langchain-google-genai", YELLOW)
        sys.exit(1)

    # --- Load .env file ---
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    load_dotenv(dotenv_path=env_path)

    if os.path.isfile(env_path):
        print_status("✓", ".env file ................ found", GREEN)
    else:
        print_status("!", ".env file ................ not found (using system env)", YELLOW)

    # --- Validate API key ---
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        print()
        print_status("✗", "GOOGLE_API_KEY is not set!", RED)
        print()
        print(f"  {YELLOW}To fix this, create a .env file in the project root:{RESET}")
        print(f"  {DIM}  GOOGLE_API_KEY=your-api-key-here{RESET}")
        print()
        print(f"  {YELLOW}Or export it in your shell:{RESET}")
        print(f"  {DIM}  export GOOGLE_API_KEY=your-api-key-here{RESET}")
        print()
        sys.exit(1)

    # Mask the key for display
    masked = api_key[:4] + "•" * (len(api_key) - 8) + api_key[-4:]
    print_status("✓", f"GOOGLE_API_KEY ........... {masked}", GREEN)
    print()
    return api_key


# ──────────────────────────────────────────────────────────────────────────────
# Agent & Crew Construction
# ──────────────────────────────────────────────────────────────────────────────

def build_crew(threat_scenario: str, api_key: str):
    """
    Construct the CrewAI crew with two agents in a sequential pipeline.

    Agent 1 — Threat_Researcher:
        Extracts attack vectors, IOCs, TTPs, CVEs, and raw technical details
        from the provided threat scenario.

    Agent 2 — SOC_Reporter:
        Synthesizes the researcher's raw intelligence into a polished,
        3-paragraph executive summary suitable for C-level stakeholders.

    Args:
        threat_scenario: The user-provided threat scenario string.
        api_key: The validated Google API key.

    Returns:
        A configured CrewAI Crew instance ready for kickoff.
    """
    from crewai import Agent, Crew, Process, Task
    from langchain_google_genai import ChatGoogleGenerativeAI

    # ── LLM instances ────────────────────────────────────────────────────
    # Lower temperature for the researcher → precise, factual extraction.
    llm_researcher = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.4,
        convert_system_message_to_human=True,
    )

    # Slightly higher temperature for the reporter → natural executive prose.
    llm_reporter = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.7,
        convert_system_message_to_human=True,
    )

    # ── Agent 1: Threat Researcher ───────────────────────────────────────
    threat_researcher = Agent(
        role="Senior Threat Intelligence Analyst",
        goal=(
            "Perform deep technical analysis of the provided cyber threat scenario. "
            "Extract and enumerate all attack vectors, Indicators of Compromise (IOCs), "
            "Tactics Techniques and Procedures (TTPs) mapped to MITRE ATT&CK where "
            "applicable, relevant CVEs, affected systems, threat actor profiles, "
            "and any actionable raw intelligence data."
        ),
        backstory=(
            "You are a cynical, battle-hardened threat intelligence analyst with 15 years "
            "of experience tracking APT groups and zero-day exploits across classified and "
            "open-source feeds. You trust only hard evidence — packet captures, malware "
            "signatures, and forensic artifacts. You have zero patience for speculation "
            "and fluff. Every claim you make is backed by observable data points. You've "
            "seen it all: from script kiddies to state-sponsored campaigns, and nothing "
            "surprises you anymore. Your analysis is surgical, exhaustive, and merciless."
        ),
        llm=llm_researcher,
        allow_delegation=False,
        verbose=True,
        max_iter=5,
    )

    # ── Agent 2: SOC Reporter ────────────────────────────────────────────
    soc_reporter = Agent(
        role="Lead SOC Consultant",
        goal=(
            "Synthesize the raw threat intelligence data produced by the Senior Threat "
            "Intelligence Analyst into a polished, 3-paragraph executive summary. "
            "The summary must bridge technical complexity with business risk, using "
            "language appropriate for C-level executives (CISO, CTO, CEO). Quantify "
            "potential business impact where possible, recommend strategic response "
            "priorities, and frame the threat in terms of organizational risk posture."
        ),
        backstory=(
            "You are a seasoned SOC consultant who has briefed Fortune 500 boards and "
            "government CISOs. Your superpower is translating deeply technical threat "
            "data into narratives that drive executive action. You understand that a "
            "boardroom doesn't care about hex dumps — they care about revenue impact, "
            "regulatory exposure, and brand reputation. You write with authority, "
            "clarity, and a sense of measured urgency. Every sentence you craft is "
            "designed to inform, not alarm, while ensuring decision-makers have the "
            "context they need to allocate resources effectively."
        ),
        llm=llm_reporter,
        allow_delegation=False,
        verbose=True,
        max_iter=5,
    )

    # ── Task 1: Deep Threat Analysis ─────────────────────────────────────
    task_research = Task(
        description=(
            f"Analyze the following cyber threat scenario and produce a comprehensive "
            f"technical intelligence report:\n\n"
            f"--- BEGIN THREAT SCENARIO ---\n"
            f"{threat_scenario}\n"
            f"--- END THREAT SCENARIO ---\n\n"
            f"Your report MUST include the following sections:\n"
            f"1. **Threat Overview** — Brief classification of the threat type\n"
            f"2. **Attack Vectors** — All identified entry points and delivery mechanisms\n"
            f"3. **Indicators of Compromise (IOCs)** — Hashes, IPs, domains, file paths, "
            f"registry keys, or behavioral signatures\n"
            f"4. **TTPs (MITRE ATT&CK Mapping)** — Mapped tactics and techniques\n"
            f"5. **CVEs & Vulnerabilities** — Any known CVEs being exploited\n"
            f"6. **Affected Systems & Scope** — Target platforms, services, and scale\n"
            f"7. **Threat Actor Profile** — Attribution signals if available\n"
            f"8. **Raw Technical Evidence** — Supporting forensic details\n\n"
            f"Be exhaustive. Be precise. No speculation without evidence."
        ),
        expected_output=(
            "A structured technical threat intelligence report with clearly labeled "
            "sections covering: Threat Overview, Attack Vectors, IOCs, MITRE ATT&CK "
            "TTPs, CVEs, Affected Systems, Threat Actor Profile, and Raw Technical "
            "Evidence. All findings must be data-driven and sourced."
        ),
        agent=threat_researcher,
    )

    # ── Task 2: Executive Summary Synthesis ──────────────────────────────
    task_report = Task(
        description=(
            "Using the raw threat intelligence report produced by the Senior Threat "
            "Intelligence Analyst, synthesize the findings into a polished executive "
            "summary.\n\n"
            "The summary MUST be exactly 3 paragraphs:\n\n"
            "**Paragraph 1 — Threat Landscape:**\n"
            "Describe what happened, the nature of the threat, and why it matters to "
            "the organization. Frame it in business terms.\n\n"
            "**Paragraph 2 — Impact Assessment:**\n"
            "Quantify or qualify the potential business impact: operational disruption, "
            "data exposure, financial loss, regulatory/compliance risk, and reputational "
            "damage. Reference specific technical findings from the analyst's report.\n\n"
            "**Paragraph 3 — Strategic Recommendations:**\n"
            "Provide 3-5 prioritized, actionable recommendations for the executive team. "
            "Frame them as risk mitigation investments, not technical tasks. Include "
            "timeline urgency (immediate / short-term / long-term).\n\n"
            "Write for a CISO or CTO audience. No jargon without explanation. "
            "Authoritative tone with measured urgency."
        ),
        expected_output=(
            "A polished 3-paragraph executive summary suitable for C-level stakeholders, "
            "covering: (1) Threat Landscape, (2) Impact Assessment with quantified risks, "
            "and (3) Strategic Recommendations with prioritized action items and timelines."
        ),
        agent=soc_reporter,
    )

    # ── Crew Assembly (Sequential Pipeline) ──────────────────────────────
    crew = Crew(
        agents=[threat_researcher, soc_reporter],
        tasks=[task_research, task_report],
        process=Process.sequential,
        verbose=True,
    )

    return crew


# ──────────────────────────────────────────────────────────────────────────────
# CLI Interface
# ──────────────────────────────────────────────────────────────────────────────

def get_threat_input() -> str:
    """
    Prompt the user for a threat scenario via the CLI.

    Returns:
        The user-provided threat scenario string.

    Raises:
        SystemExit: If the user cancels input or provides empty input.
    """
    print_phase("THREAT SCENARIO INPUT")
    print(f"  {GRAY}Describe the cyber threat scenario you want analyzed.{RESET}")
    print(f"  {GRAY}Be as detailed as possible — include IOCs, CVEs, attack{RESET}")
    print(f"  {GRAY}descriptions, or paste raw threat intel reports.{RESET}")
    print()
    print(f"  {DIM}(Press Ctrl+C to abort){RESET}")
    print()

    try:
        scenario = input(f"  {CYAN}⟩ {BOLD}Threat Scenario:{RESET} ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        print()
        print_status("⊘", "Operation cancelled by user.", YELLOW)
        print()
        sys.exit(0)

    if not scenario:
        print()
        print_status("✗", "No threat scenario provided. Aborting.", RED)
        print()
        sys.exit(1)

    return scenario


def display_results(result) -> None:
    """
    Display the final crew output in a formatted block.

    Args:
        result: The CrewOutput returned by crew.kickoff().
    """
    print()
    print(f"  {CYAN}╔{'═' * 68}╗{RESET}")
    print(f"  {CYAN}║{RESET}{BOLD}  ◆  PROJECT AURA — INTELLIGENCE REPORT{RESET}{'':>30}{CYAN}║{RESET}")
    print(f"  {CYAN}╠{'═' * 68}╣{RESET}")
    print(f"  {CYAN}║{RESET}  Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
          f"{'':>30}{CYAN}║{RESET}")
    print(f"  {CYAN}╚{'═' * 68}╝{RESET}")
    print()

    # Format and print the result
    output_text = str(result)
    wrapped_lines = []
    for paragraph in output_text.split("\n"):
        if paragraph.strip():
            wrapped = textwrap.fill(paragraph, width=72, initial_indent="  ", subsequent_indent="  ")
            wrapped_lines.append(wrapped)
        else:
            wrapped_lines.append("")

    print("\n".join(wrapped_lines))
    print()
    print_separator()
    print_status("✓", f"Report generated successfully at "
                 f"{datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}", GREEN)
    print()


# ──────────────────────────────────────────────────────────────────────────────
# Main Entry Point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """Main entry point for Project AURA."""
    # Display the banner
    print(BANNER)
    print_separator()
    print()

    # Phase 1: Validate environment
    api_key = validate_environment()

    # Phase 2: Get threat scenario from user
    threat_scenario = get_threat_input()

    # Phase 3: Build and execute the crew
    print_phase("AGENT PIPELINE EXECUTION")
    print_status("◈", "Initializing Agent Pipeline ...", CYAN)
    print_status("│", f"Agent 1: {BOLD}Threat_Researcher{RESET}  →  Senior Threat Intelligence Analyst")
    print_status("│", f"Agent 2: {BOLD}SOC_Reporter{RESET}       →  Lead SOC Consultant")
    print_status("│", f"Process: {BOLD}Sequential{RESET}         →  Researcher → Reporter")
    print_status("◈", f"LLM:     {BOLD}gemini-1.5-flash{RESET}   →  Google Generative AI")
    print()
    print_separator()
    print()

    start_time = time.time()

    try:
        crew = build_crew(threat_scenario, api_key)

        print_status("▶", "Kickoff! Agents are now working ...", GREEN)
        print()

        result = crew.kickoff()

        elapsed = time.time() - start_time
        minutes, seconds = divmod(int(elapsed), 60)

        display_results(result)

        print_status("⏱", f"Total execution time: {minutes}m {seconds}s", GRAY)
        print()

    except KeyboardInterrupt:
        print()
        print()
        print_status("⊘", "Pipeline interrupted by user.", YELLOW)
        print()
        sys.exit(0)

    except Exception as exc:
        elapsed = time.time() - start_time
        print()
        print_separator()
        print()
        print_status("✗", f"Pipeline failed after {int(elapsed)}s", RED)
        print()

        error_msg = str(exc)

        # Provide contextual guidance based on common failure modes
        if "API key" in error_msg or "401" in error_msg or "403" in error_msg:
            print_status("→", "API key may be invalid or expired.", YELLOW)
            print_status("→", "Verify your GOOGLE_API_KEY in .env", YELLOW)
        elif "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
            print_status("→", "API quota exceeded or rate-limited.", YELLOW)
            print_status("→", "Wait a few minutes and try again.", YELLOW)
            print_status("→", "Consider using gemini-1.5-flash for lower quota usage.", YELLOW)
        elif "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            print_status("→", "Request timed out.", YELLOW)
            print_status("→", "Check your network connection and try again.", YELLOW)
        else:
            print_status("→", f"Error: {error_msg}", YELLOW)

        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
