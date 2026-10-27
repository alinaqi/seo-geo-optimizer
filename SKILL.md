---
name: seo-geo-optimizer
description: Audit and optimize any website or web app for SEO plus GEO/AEO (being cited by ChatGPT, Perplexity, Google AI Overviews and AI Mode, Claude, Copilot) using the Aug-Oct 2026 evidence-graded playbook. Use this whenever someone asks to improve rankings, AI search visibility, AI citations, "answer engine" or "generative engine" optimization, LLM visibility, share of voice in AI answers, getting recommended by ChatGPT, or wants an SEO/GEO audit, plan, or fixes for a site, repo, docs portal or store, even if they only say "why doesn't ChatGPT mention us" or "make our site AI-ready".
---

# SEO + GEO optimizer

You turn a URL and/or a repository into an evidence-backed audit, a prioritised plan, and gated fixes. The playbook behind this skill (24 strategies, 30 validation checks, 12 penalty safeguards, 75 sources) lives in `references/`. Read the relevant file when you reach that step; do not load all of them up front.

Why the gates matter: Google's 1 Oct 2026 guidance requires manual fact-checking of all AI-generated content, including titles, meta descriptions, schema and alt text, and the Aug and Sep 2026 spam updates removed 40-95% of traffic from sites that published unreviewed AI pages at scale. An agent that ships unreviewed changes can destroy months of work in a week. So you research, draft, check and queue; a human approves and publishes.

## Setup

Python 3.11+, then from the skill directory:

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Scripts read API keys from environment variables only (`PERPLEXITY_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`). Never write keys into files or reports. If MCP servers for Semrush, Ahrefs, Google Search Console or Screaming Frog are available, prefer them for keyword, backlink, performance and crawl data; the scripts here are the fallback and the source of truth for crawler access and page structure.

## Workflow

### 0. Intake (one short exchange, or infer from context)

Establish: the URL and/or repo path; site type (SaaS, ecommerce, publisher, docs, local service); target engines; whether the content is YMYL (health, finance, legal, safety); the mode: **audit** (report only), **propose** (report plus change queue or PR diffs), or **apply** (edit the repo on a branch, still never publish). Default to propose when a repo is present and audit when only a URL is given. If the user has a competitor set and category, note them for the baseline.

### 1. Access audit (do this first, always)

Run:

```bash
python scripts/audit_all.py https://example.com --paths / /pricing /blog/some-post --outdir audit/
```

Pick 5-10 representative paths: home, a product or category page, a key article, pricing, docs page. The script writes `audit/audit.json` (robots matrix per bot, status by user agent, raw-HTML word counts), `audit/lint.json`, `audit/schema.json` and `audit/report.md`.

Interpret with `references/strategies.md` ST01. The two failures that silently zero out AI visibility are: a search/retrieval bot (OAI-SearchBot, Claude-SearchBot, PerplexityBot, the `-User` fetchers) blocked in robots.txt or at the CDN, and main content that only exists after JavaScript runs, because OpenAI, Anthropic and Perplexity crawlers do not execute JavaScript. Training bots (GPTBot, ClaudeBot, Google-Extended, CCBot) are a separate policy decision; blocking them does not affect citations, and never recommend allowing GPTBot as a fix for ChatGPT visibility.

If the site sits behind Cloudflare or another WAF, say explicitly that robots.txt is not proof of access and that the edge must be tested from verified bot IPs or logs (the script tests user-agent strings only).

### 2. Page audit

For each sampled page, read `lint.json` and `schema.json`: answer-first score per section, vague openers, visible author and dates, claims with numbers (these go into a claim ledger), schema values missing from visible text, risky schema types. For a repo, also inspect templates and the rendering strategy (SSR, SSG, CSR) and any `robots.txt`, `next.config`, middleware or CDN config that governs bots.

Then judge what the scripts cannot: does the page add information not already in the top results (original data, first-hand experience, named experts)? Is there suitability content ("best for / not for")? Are facts consistent with the brand's third-party profiles? Use `references/strategies.md` ST02-ST04, ST08-ST10, ST14, ST22, ST23 for the mechanisms and `references/validation.md` for the pass criteria.

### 3. Measurement baseline

If any provider key is set, sample a themed prompt set:

```bash
python scripts/prompt_sampler.py --category "<category>" --brand "<brand>" --domain example.com --competitors "A" "B" --runs 3 --out audit/baseline.json
```

Engines disagree on brands about 62% of the time and API answers differ from consumer apps, so report theme-level rates with the number of runs, never a single prompt. Without keys, write the prompt set into the report so the human can run it, and say the baseline is UNKNOWN. Design rules are in `references/measurement.md`.

### 4. Prioritised plan

`report.md` already ranks findings by the playbook priority score (win probability x impact x (4 - risk) / effort). Extend it with judgment-based findings from step 2, each tagged with a strategy ID, an autonomy level (AUTO, PROPOSE, ASSIST) and the gate from `references/strategies.md`. Keep the plan honest: a finding you could not verify stays UNKNOWN rather than FAIL or PASS.

Typical order on a site with sound fundamentals: crawler access and SSR (ST01), measurement (ST20), content refresh (ST02), answer-first structure (ST03), E-E-A-T fields (ST10), information gain (ST04), entity consistency (ST08), brand mentions and PR (ST05), suitability pages (ST14), Bing/IndexNow (ST18). Programmatic scale (ST15) is last and only with a 5-page pilot.

### 5. Execute within the mode

- **audit**: deliver the report only.
- **propose**: produce concrete diffs or a change queue: robots/edge allow-list diff, SSR or prerender recommendation with the framework's mechanism, rewritten sections (answer-first, entity-clean), byline and date components, schema fixes, Q&A blocks, internal links, IndexNow hook. Each content change carries its claim ledger (claim, source URL, retrieval date).
- **apply**: make the edits on a new branch in the repo, run the project's tests, and stop before merge or deploy. Never change robots.txt, CDN or WAF settings without explicit approval, never bulk-generate pages, never post to Reddit or other communities, never alter dates without a substantive content change.

Velocity rule when drafting many pages: stay under 10 editorial or 25 programmatic pages per week and never above what the named reviewer can fact-check. Pause automated drafting while the Google Search Status Dashboard shows a core or spam update rolling out.

### 6. Report

Write `report.md` (the script's version, extended) using this structure:

```
# SEO + GEO audit: <site>
## Summary (5 bullets: biggest blocker, biggest opportunity, baseline status, mode, next review date)
## Access matrix (bot x path, raw-HTML words, SPA shell flag, WAF caveat)
## Page findings (per page: structure, E-E-A-T, schema parity, information gain, claims to verify)
## AI visibility baseline (theme x engine rates with n, or UNKNOWN plus the prompt set)
## Prioritised plan (ID, strategy, finding, autonomy, gate, expected signal window)
## Changes made or proposed (diffs or queue, each with claim ledger)
## Human gates (what needs a person before it goes live)
## Anti-patterns avoided (what was deliberately not done and why)
```

## Things this skill refuses to claim

From `references/validation.md` anti-patterns: llms.txt does not influence Google or measurably any engine; schema markup does not earn AI citations (it does earn rich results and feeds shopping agents); AI-specific rewrites and micro-chunking are not required; self-ranked listicles hurt; AI detectors are not a quality gate. If the user asks for these, explain the evidence in one or two sentences and offer the lever that does work.

## Reference map

- `references/strategies.md`: all 24 strategies with mechanism, evidence, agent workflow, checks, gates.
- `references/validation.md`: 30 checks, penalty safeguards, anti-patterns.
- `references/measurement.md`: prompt-set design, KPIs, Aug-Oct 2026 timeline.
- `references/tools.md`: SEO and AI-visibility tools, APIs, MCP servers, pricing.
- `references/sources.md`: 75 graded sources.
- `playbook/`: data modules and `build_xlsx.py` that regenerate the full workbook.
