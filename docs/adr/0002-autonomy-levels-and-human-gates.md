# 0002 - Autonomy levels and human gates; agents never publish

**Status:** accepted
**Date:** 2026-10-27
**Spec:** SKILL.md step 5, references/validation.md
**Deciders:** Ali Naqi Shaheen

## Context

Google's 1 Oct 2026 guidance requires manual fact-checking of all AI-generated content including metadata, and the August and September 2026 spam updates removed most traffic from sites publishing unreviewed AI pages at scale. An agent that publishes directly can cause months of damage in days.

## Decision

Every strategy carries an autonomy level: AUTO (read-only or reversible actions), PROPOSE (agent drafts, human approves in a queue), ASSIST (agent researches, human executes). Modes are audit, propose and apply; apply edits a branch and stops before merge or deploy. Agents never change robots.txt, CDN or WAF rules, publish pages, post to communities, bulk-generate pages or alter dates without a content change. A claim ledger accompanies every factual change. A velocity governor (10 editorial or 25 programmatic pages per week, never above review capacity) and a pause during confirmed Google updates are part of the workflow.

## Consequences

- Slower than fully autonomous publishing; that is the point.
- Reports keep UNKNOWN for anything not observed.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| Full autonomy with post-hoc review | Fast | Penalty exposure, hallucinated facts live | Contradicts Google guidance |
| Audit only | Safe | Low value for repo owners | Users asked for fixes |

## Links

- Related: ADR 0004
