---
name: seo-geo-optimizer
description: Audit and optimize any website or web app for SEO plus GEO/AEO (being cited by ChatGPT, Perplexity, Google AI Overviews and AI Mode, Claude, Copilot) using an evidence-graded playbook of what works from August 2026 onward. Use this whenever someone asks to improve rankings, AI search visibility, AI citations, "answer engine" or "generative engine" optimization, LLM visibility, share of voice in AI answers, getting recommended by ChatGPT, or wants an SEO/GEO audit, plan, or fixes for a site, repo, docs portal or store, even if they only say "why doesn't ChatGPT mention us" or "make our site AI-ready".
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

Establish: the target, which may be a URL, a local repo path, or a GitHub repo URL (clone it first with `git clone --depth 1 <url> target/` and treat it as a local repo); site type (SaaS, ecommerce, publisher, docs, local service); target engines; whether the content is YMYL (health, finance, legal, safety); the mode: **audit** (report only), **propose** (report plus change queue or PR diffs), or **apply** (edit the repo on a branch, still never publish). Default to propose when a repo is present and audit when only a URL is given. If the user has a competitor set and category, note them for the baseline.

### 1. Access audit (do this first, always)

Run:

```bash
python scripts/audit_all.py https://example.com --paths / /pricing /blog/some-post --outdir audit/
```

Pick 5-10 representative paths: home, a product or category page, a key article, pricing, docs page. The script writes `audit/audit.json` (robots matrix per bot, status by user agent, raw-HTML word counts), `audit/lint.json`, `audit/schema.json`, `audit/report.md` and `audit/plan.html` (a self-contained review page; see step 6b).

Interpret with `references/strategies.md` ST01. The two failures that silently zero out AI visibility are: a search/retrieval bot (OAI-SearchBot, Claude-SearchBot, PerplexityBot, the `-User` fetchers) blocked in robots.txt or at the CDN, and main content that only exists after JavaScript runs, because OpenAI, Anthropic and Perplexity crawlers do not execute JavaScript. Training bots (GPTBot, ClaudeBot, Google-Extended, CCBot) are a separate policy decision; blocking them does not affect citations, and never recommend allowing GPTBot as a fix for ChatGPT visibility.

If the site sits behind Cloudflare or another WAF, say explicitly that robots.txt is not proof of access and that the edge must be tested from verified bot IPs or logs (the script tests user-agent strings only).

### 1b. ICP and market discovery

Before judging pages, establish who the site is for and where. Run on the same sampled pages:

```bash
python scripts/icp_signals.py audit/page.html      # roles, industries, size band, pricing model, review platforms, proof quotes with evidence
python scripts/market_detect.py audit/page.html --url https://example.com   # languages, hreflang, JavaScript language swaps, currencies, geographies, market profile
```

Write an ICP sheet with one row per segment (role, size, industry, market, language, triggers, objections, engines to sample, prompts, competitors, confidence) using the template in `references/icp-and-markets.md`. Quote the evidence for every field and leave UNKNOWN where the site gives nothing; the owner confirms the sheet before it drives content. The market table in that file tells you which engines and third-party citation pools matter per market, because the mix differs (Naver in Korea, Baidu and DeepSeek in China, Le Chat in France, Trustpilot for UK consumers, OMR Reviews in DACH).

Language matters more than it used to: engines ignore hreflang when composing answers and run many non-English sub-searches in English, so a JavaScript language toggle or thin translated subfolder is invisible. `market_detect.py` flags both patterns.

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

### 4b. Content strategy

Save the confirmed ICP sheet as `icp.json` (brand, category, competitors, segments with roles, markets, languages, engines) and run:

```bash
python scripts/strategy_plan.py --icp icp.json --outdir strategy/ --weekly-cap 3 --weeks 13
```

It writes `strategy.md` (segments, velocity cap, calendar, rules) and `calendar.csv` (one brief per row: segment, theme, language, strategy ID, intent, information gain, gate, prompts). Every brief must state its information gain before writing starts; a brief that would only summarise existing results is dropped. For consumer sites add demographic fields from reviews and analytics, never guessed. The prompts column becomes rows in the measurement set so each page is checked for retrieval after it ships.

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
## ICP and markets (segments with evidence and confidence; market table rows that apply; language findings)
## Prioritised plan (ID, strategy, finding, autonomy, gate, expected signal window)
## Content strategy (link to strategy.md and calendar.csv, or the first 10 briefs inline)
## Changes made or proposed (diffs or queue, each with claim ledger)
## Human gates (what needs a person before it goes live)
## Anti-patterns avoided (what was deliberately not done and why)
```

### 6b. Hand the owner a reviewable plan (plan.html)

After the report and, if produced, the strategy, regenerate the review page:

```bash
python scripts/html_plan.py --outdir audit/ --strategy strategy/
```

`plan.html` is one static file with no external resources: the prioritised plan as a table with a decision dropdown (pending, approve, defer, reject) and a note per item, the content strategy and calendar, and the full report. The owner opens it in any browser (`open audit/plan.html`), marks each item, clicks "Copy decisions" and pastes the resulting markdown back to you. Treat that pasted block as the authorisation for step 5: apply approved items within the mode, leave deferred ones in the change queue, drop rejected ones and record why in the report. Decisions are stored only in the owner's browser; never assume an item is approved until the pasted block says so. Tell the owner the file path and that nothing in it is sent anywhere. Do not substitute a hosted artifact or a chat-only summary for this file; owners using Codex or CI have no artifact viewer.

### 7. Monitor on a schedule

When the user wants ongoing review, create `seo-geo.config.json` in their project from `seo-geo.config.example.json` and run `scripts/monitor.py --config seo-geo.config.json --state .seo-geo`. It snapshots each run and diffs it against the previous one (newly blocked search bots, status changes, client-rendered shells, theme-level visibility drops), writing `monitor-report.md` and a browser-ready `monitor-report.html`. In Claude Code the same flow is the `/monitor` command in `commands/monitor.md`; `/loop 1w /monitor` makes it recurring. The monitor is read-only; any fix goes back through steps 4 and 5.

## Things this skill refuses to claim

From `references/validation.md` anti-patterns: llms.txt does not influence Google or measurably any engine; schema markup does not earn AI citations (it does earn rich results and feeds shopping agents); AI-specific rewrites and micro-chunking are not required; self-ranked listicles hurt; AI detectors are not a quality gate. If the user asks for these, explain the evidence in one or two sentences and offer the lever that does work.

## Reference map

- `references/icp-and-markets.md`: ICP sheet template, market table (engines and citation pools per market), language rules, brief template.
- `references/strategies.md`: all 27 strategies with mechanism, evidence, agent workflow, checks, gates.
- `references/validation.md`: 30 checks, penalty safeguards, anti-patterns.
- `references/measurement.md`: prompt-set design, KPIs, timeline from August 2026.
- `references/tools.md`: SEO and AI-visibility tools, APIs, MCP servers, pricing.
- `references/sources.md`: 75 graded sources.
- `playbook/`: data modules and `build_xlsx.py` that regenerate the full workbook.
- `AGENTS.md`: the same guideline for any coding agent (Codex reads it automatically).
- `commands/monitor.md`: the `/monitor` slash command.
