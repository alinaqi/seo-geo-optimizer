# 0001 - Skill structure and references generated from playbook data

**Status:** accepted
**Date:** 2026-10-27
**Spec:** README.md, SKILL.md
**Deciders:** Ali Naqi Shaheen

## Context

The skill must work for Claude Code (SKILL.md, progressive disclosure) and for other coding agents (Codex reads AGENTS.md). The evidence base is a 14-sheet workbook that changes as research is updated; hand-maintained markdown copies would drift.

## Decision

- `SKILL.md` holds the workflow and reasoning; `AGENTS.md` holds the same rules for any agent; `commands/monitor.md` is the Claude Code slash command.
- `playbook/data_*.py` is the single source of truth. `playbook/export_references.py` generates `references/*.md`; `playbook/build_xlsx.py` generates the workbook. Generated files are committed so the skill works without a build step.
- `scripts/` contains small, testable CLIs; each inserts the repo root on `sys.path` so it runs from any directory.

## Consequences

- Editing a strategy means editing a data module and regenerating; CI fails if references are stale.
- Data modules may exceed the 200-line file limit because they are data, not logic (see ADR 0006).

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| Hand-written references | Simple | Drift from workbook | Two sources of truth |
| Load the xlsx at runtime | One artefact | Needs openpyxl at runtime, opaque diffs | Markdown is reviewable |

## Links

- Related: ADR 0003
