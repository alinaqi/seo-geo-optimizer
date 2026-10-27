# 0004 - Crawler policy stance and refused levers

**Status:** accepted
**Date:** 2026-10-27
**Spec:** scripts/crawl_audit.py, SKILL.md "Things this skill refuses to claim"
**Deciders:** Ali Naqi Shaheen

## Context

The most common and most expensive 2026 AEO mistake is confusing training crawlers with search crawlers. Several popular tactics (llms.txt, schema for citations, AI-specific rewrites, self-ranked listicles) have no supporting evidence or negative evidence.

## Decision

`SEARCH_BOTS` (Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User) and `TRAINING_BOTS` (GPTBot, ClaudeBot, Google-Extended, CCBot) are disjoint constants. Findings are raised only for blocked search bots; training bots are reported as a separate policy decision. The skill explicitly refuses to recommend llms.txt, schema markup, AI rewrites or self-ranked listicles as citation levers, and explains why in one or two sentences.

## Consequences

- The bot lists must be updated when vendors add crawlers; a test guards their disjointness.
- Users who want those tactics get an explanation and the working alternative.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| Report all bots equally | Simpler | Misleads users into allowing GPTBot | Wrong fix |
| Stay neutral on llms.txt | Avoids argument | Wastes user effort | Evidence is clear |

## Links

- Related: ADR 0002
