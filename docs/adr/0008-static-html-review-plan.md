# 0008 - Static HTML review plan instead of hosted artifacts

**Status:** accepted
**Date:** 2026-10-28
**Spec:** SKILL.md step 6b, AGENTS.md step 4b, scripts/html_plan.py
**Deciders:** Ali Naqi Shaheen

## Context

The plan an agent produces has to be reviewed by a site owner who decides, item by item, what the agent may apply (ADR 0002). Until now the review surface was `report.md` in a terminal or a Claude-hosted artifact. Owners who run the guideline through Codex, CI or another agent have no artifact viewer, and a markdown file in a terminal is a poor place to make and record two dozen decisions.

## Decision

The skill writes `plan.html`, one self-contained static file, next to `report.md`:
- Built by `scripts/html_plan.py` from the same JSON the report uses, so the plan table is identical to the report's prioritised plan; `audit_all.py` writes it automatically and the agent regenerates it after extending the report or producing a strategy.
- No external scripts, fonts or stylesheets; it opens from disk in any browser and nothing is sent anywhere. Decisions and notes persist only in that browser's local storage.
- Each plan row has a decision (pending, approve, defer, reject) and a note. "Copy decisions" produces a markdown block the owner pastes back to the agent; that block is the authorisation to apply items.
- `monitor.py` writes `monitor-report.html` with the same renderer so monitor runs can be shared the same way.
- Claude-hosted artifacts remain optional for conversations in Claude, never a substitute for the file.

## Consequences

- One more dependency (`markdown`) and two small modules under the quality gates.
- The HTML is regenerated, never hand-edited; changes to the plan logic belong in `report.py`.
- Decisions are not synced back automatically; the paste step is deliberate so the agent never infers approval.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| Claude artifact only | Zero code | Unavailable to Codex, CI, other agents | Excludes half the intended users |
| Local web server with write-back | Decisions sync automatically | Needs a running process, port, and trust in automatic approval | Violates the explicit-gate rule |
| Markdown checklist in report.md | No new format | Awkward to edit, no notes per row, easy to misread in a terminal | Poor review experience |

## Links

- Supersedes: N/A
- Related: ADR 0002 (autonomy levels and human gates), ADR 0006 (quality gates)
