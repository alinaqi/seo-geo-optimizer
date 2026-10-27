# 0005 - Measurement via official APIs, env-var keys, snapshot monitor

**Status:** accepted
**Date:** 2026-10-27
**Spec:** scripts/prompt_sampler.py, scripts/providers.py, scripts/monitor.py
**Deciders:** Ali Naqi Shaheen

## Context

Consumer AI apps expose no query data and scraping them breaks their terms. Engines disagree with each other most of the time and answers vary run to run. Users need a repeatable, cheap signal and a way to see regressions over time.

## Decision

Sampling uses only official APIs (OpenAI Responses web_search, Perplexity Sonar, Gemini grounding, Anthropic web search), keyed from environment variables that are never written to files. Prompts are themed and run several times; results are reported as theme-level rates with n. The monitor snapshots each run under `.seo-geo/runs/<timestamp>/` in the target project and diffs against the previous run; it is read-only.

## Consequences

- API answers differ from consumer apps; reports label them as proxies and require monthly spot checks.
- Snapshots live in the target repo so history travels with the project.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| Scrape consumer UIs | Closer to users | Violates terms, brittle | Not acceptable |
| Vendor tool only | Rich UI | Cost, lock-in | Keep as optional, listed in references/tools.md |

## Links

- Related: ADR 0002
