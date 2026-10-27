# 0003 - Evidence grading and priority score

**Status:** accepted
**Date:** 2026-10-27
**Spec:** playbook/data_strategies.py, references/strategies.md
**Deciders:** Ali Naqi Shaheen

## Context

Most 2026 SEO and GEO figures come from vendors with commercial interest and conflict with each other. Users still need a ranking of what to do first.

## Decision

Sources are graded A (official or peer-reviewed), B (large industry dataset or trade-press reporting of official news), C (vendor or practitioner report), D (single unverified claim). Each strategy carries an estimated win probability (chance of a measurable KPI gain in 90-180 days), impact, effort and penalty risk on 1-3 scales. Priority = win probability x impact x (4 - risk) / effort. The estimates are expert judgments, labelled as such, and editable in the workbook.

## Consequences

- Rankings are explainable and re-scorable.
- Probabilities are not measured frequencies; the README says so.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| Unranked list | No false precision | Users cannot prioritise | Asked for probabilities |
| ICE/RICE only | Familiar | Ignores penalty risk | Risk is the 2026 differentiator |

## Links

- Related: ADR 0001
