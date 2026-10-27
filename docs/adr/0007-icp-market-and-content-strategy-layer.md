# 0007 - ICP, market and content-strategy layer

**Status:** accepted
**Date:** 2026-10-27
**Spec:** SKILL.md steps 1b and 4b, references/icp-and-markets.md
**Deciders:** Ali Naqi Shaheen

## Context

The first version audited pages and crawler access but did not say who the buyers are, which markets and languages matter, or what to publish for whom. 2026 buyer research shows AI discovery is persona-shaped and market-specific (engine mix, citation pools, language behaviour), so a plan without an ICP and market layer under-serves multi-market sites.

## Decision

Add a discovery step before the page audit and a strategy step after the plan:
- `scripts/icp_signals.py` extracts roles, industries, size band, pricing model, review platforms and proof quotes with evidence; `scripts/market_detect.py` detects languages, hreflang, JavaScript language swaps, currencies and geographies and maps them to a market table (`scripts/markets_data.py`).
- The agent writes an ICP sheet (one row per segment, UNKNOWN where the site gives no evidence) and the owner confirms it.
- `scripts/strategy_plan.py` turns the ICP sheet into briefs with required information gain and gates, a calendar under the velocity cap, and prompt rows for measurement.
- Three playbook strategies (ST25 ICP-led content strategy, ST26 market and language localisation, ST27 persona prompt coverage) with graded sources.

## Consequences

- Reports grow by an ICP and market section and a strategy deliverable; audit-only runs still produce the ICP sheet.
- The market table is a maintained data module; it must be re-verified each quarter.
- Heuristic extraction is evidence for the agent, not a substitute for owner confirmation.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| LLM-only inference without scripts | Flexible | No evidence trail, invents personas | Violates the no-invented-facts rule |
| External persona tools | Rich data | Cost, no AI-search mapping | Keep as optional inputs |

## Links

- Related: ADR 0002, ADR 0003
