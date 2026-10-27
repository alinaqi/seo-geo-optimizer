"""Generate references/*.md from the playbook data modules so SKILL.md references stay in sync.
Usage: python -m playbook.export_references"""
from pathlib import Path
from playbook.data_strategies import STRATEGIES
from playbook.data_agent import AGENT_EXEC
from playbook.data_validation import CHECKS, PENALTIES, ANTIPATTERNS
from playbook.data_tools import SEO_TOOLS, AEO_TOOLS
from playbook.data_misc import PROMPT_SET, TIMELINE
from playbook.data_sources import SOURCES

OUT = Path(__file__).resolve().parent.parent / "references"


def _table(cols, rows):
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols)
    body = "\n".join("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in rows)
    return head + "\n" + body


def strategies_md():
    agents = {a["id"]: a for a in AGENT_EXEC}
    parts = ["# Strategies and agent execution (from SEO_AEO_Agentic_Playbook_2026.xlsx)\n",
             "Win probability = estimated chance of a measurable KPI gain in 90-180 days; priority = win x impact x (4 - risk) / effort.\n"]
    for s in sorted(STRATEGIES, key=lambda s: -(s["win_prob"] * s["impact"] * (4 - s["risk"]) / s["effort"])):
        a = agents[s["id"]]
        parts.append(f"## {s['id']} {s['name']} (win {s['win_prob']:.0%}, grade {s['grade']}, risk {s['risk']}/3)\n")
        parts.append(f"**What:** {s['what']}\n\n**Why:** {s['mechanism']}\n\n**Evidence:** {s['evidence']} Sources: {s['sources']}\n")
        parts.append(f"**Agent:** {a['agent']} | autonomy {a['autonomy']} | trigger {a['trigger']}\n\n**Steps:** {a['steps']}\n")
        parts.append(f"**Checks:** {a['checks']}\n\n**Gate:** {a['gate']} **Guardrails:** {a['guardrails']}\n")
    return "\n".join(parts)


def validation_md():
    return "\n\n".join(["# Validation checklist, penalty safeguards, anti-patterns\n",
                        "## Checks (verdicts PASS/FAIL/UNKNOWN; enforcement HARD_BLOCK/REVIEW_REQUIRED/ADVISORY)",
                        _table(["ID", "Stage", "Check", "Method", "Tool", "Pass", "Auto", "Freq", "Enforcement", "Strategies", "Controls"], CHECKS),
                        "## Penalty safeguards", _table(["Policy", "Trigger", "2026 evidence", "Guardrail", "Detection", "Sources"], PENALTIES),
                        "## Anti-patterns", _table(["Anti-pattern", "Evidence", "Do instead", "Sources"], ANTIPATTERNS)])


def tools_md():
    cols = ["Tool", "Category", "Role", "What it does", "API / MCP", "Pricing (Oct 2026)", "Notes", "Sources"]
    return "\n\n".join(["# Tools (verify pricing before purchase)", "## SEO tools", _table(cols, SEO_TOOLS), "## AEO / AI visibility tools", _table(cols, AEO_TOOLS)])


def measurement_md():
    return "\n\n".join(["# Measurement and prompt-set design", _table(["Element", "Guidance"], PROMPT_SET),
                        "## Timeline from Aug 2026", _table(["Date", "Event", "Implication", "Sources"], TIMELINE)])


def sources_md():
    return "# Sources (grade A official/primary, B industry dataset, C vendor/practitioner, D unverified)\n\n" + _table(["ID", "Title", "Publisher", "Date", "URL", "Grade"], SOURCES)


def main():
    OUT.mkdir(exist_ok=True)
    files = {"strategies.md": strategies_md(), "validation.md": validation_md(), "tools.md": tools_md(),
             "measurement.md": measurement_md(), "sources.md": sources_md()}
    for name, text in files.items():
        (OUT / name).write_text(text + "\n")
        print("wrote", name, len(text.splitlines()), "lines")


if __name__ == "__main__":
    main()
