# seo-geo-optimizer

A skill for coding agents (Claude Code, Codex) that audits and optimizes any website or web app for SEO and GEO/AEO: ranking in Google and being cited or recommended by ChatGPT, Perplexity, Google AI Overviews and AI Mode, Claude and Copilot. It encodes what has actually worked from August 2026 onward, graded by evidence, and it refuses the tricks that stopped working.

Point it at a URL, a local repo or a GitHub repo. It produces an access matrix, page findings, a prioritised plan with strategy IDs and human gates, proposed diffs, and a recurring monitor.

## What works (from August 2026)

1. **Let the right bots in and give them real HTML.** ChatGPT, Perplexity and Claude cite only what their own search crawlers can fetch, and those crawlers do not run JavaScript. Allow OAI-SearchBot, Claude-SearchBot, PerplexityBot and the user-triggered fetchers, serve server-rendered pages, and test at the CDN, not just in robots.txt. Blocking training bots (GPTBot, ClaudeBot, Google-Extended) is a separate choice and does not cost you citations.
2. **Refresh what you already have.** AI engines favour recently updated pages. Substantive updates to decaying pages (new data, corrected facts, new sections, a visible changelog) beat publishing more pages. Never bump a date without changing content.
3. **Answer first, in self-contained sections.** Engines retrieve passages, not pages. Open every section with a direct answer, keep sections short enough to quote on their own, use question-shaped headings, name the entity instead of writing "it" or "this", and put the most citable facts near the top.
4. **Bring something new.** Original data, first-hand experience, named experts and cited primary sources are the strongest content levers in the only peer-reviewed study of generative engine optimization. A page that summarises the top ten results will not be cited.
5. **Get mentioned, not just linked.** Third-party brand mentions, YouTube presence, reviews on G2 or Trustpilot and inclusion in independent roundups correlate with AI visibility far more than backlinks do. Earn them with data stories, expert commentary and real community participation by named humans.
6. **Be the same company everywhere.** Keep one canonical description, pricing and product naming across your site, LinkedIn, Crunchbase, app stores and press. Models recommend brands whose facts agree across sources.
7. **Cover the sub-questions.** AI Mode and ChatGPT split a prompt into many sub-queries. Build topic clusters that answer definitions, how-to, cost, comparison, alternatives and "best for whom". Suitability pages that say who the product is and is not for are picked disproportionately by AI agents.
8. **Show real people and dates, and fact-check everything AI touched.** Since 1 October 2026 Google's guidance requires manual review of all AI-generated content including titles, meta descriptions, schema and alt text, and treats fabricated author profiles as deceptive.
9. **Feed shopping agents clean product data.** Merchant Center feeds, Product and Offer schema that match the page, live price and stock, and the agentic commerce protocols (OpenAI ACP, Google UCP) decide whether a product makes the AI shortlist.
10. **Measure with themed prompt sets, repeatedly, per engine.** Engines disagree with each other most of the time and a single prompt is noise. Sample themed prompts weekly with several runs, use Search Console's generative-AI report, Bing's AI Performance report and GA4's AI Assistant channel, and expect AI referrals to be undercounted.

11. **Know who you are writing for, and where.** AI discovery is persona-shaped and market-specific: half of B2B software buyers start in a chatbot, engines run most non-English sub-searches in English and ignore hreflang, and the engine mix differs by country (Naver in Korea, Baidu and DeepSeek in China, Le Chat in France). The skill derives ideal customer profiles and target markets from the site with evidence, then turns them into briefs, a capped calendar and per-segment prompt sets.

## What does not work

- `llms.txt`: Google says it does not use it and crawler logs show almost nobody fetches it.
- Schema markup as a citation lever: a large controlled study found no measurable citation gain. Keep schema for rich results and shopping feeds.
- Rewriting content "for LLMs" or chopping it into micro-chunks: not required by any engine.
- Self-ranked "best X" listicles on your own domain: linked to visibility losses.
- Bulk AI pages without review: the August and September 2026 spam updates removed most traffic from sites that did this.
- Fake authors, fake reviews, bumped dates, blocking the wrong bots, posting to Reddit with bots.

## The guideline the agent follows

1. **Intake**: target (URL, local repo or GitHub repo URL), site type, target engines, YMYL or not, and the mode: audit (report only), propose (report plus diffs and a change queue), apply (edits on a branch, never published).
2. **Access audit**: robots rules per bot, status codes per user agent, raw-HTML word counts. This runs first because a blocked search bot or a client-rendered shell zeroes out everything else.
3. **ICP and market discovery**: roles, industries, size band, pricing model, review platforms and proof quotes with evidence; languages, hreflang, JavaScript language swaps, currencies and geographies mapped to a market table. One ICP row per segment, UNKNOWN where the site gives nothing.
4. **Page audit**: answer-first structure, vague openers, visible author and dates, claims that need sources, schema values missing from the visible text, information gain, suitability content.
5. **Measurement baseline**: a themed prompt set sampled across engines with repeated runs, or an explicit UNKNOWN plus the prompt set for a human to run.
6. **Prioritised plan**: each finding tagged with a strategy ID, a priority score, an autonomy level and the human gate it needs.
7. **Content strategy**: briefs with required information gain and gates, a calendar under the velocity cap, and the prompts that measure each brief (`strategy.md`, `calendar.csv`).
8. **Execution within the mode**: diffs that apply with `patch -p1`, a change queue with claim ledgers, nothing merged, nothing published.
9. **Report** in a fixed structure, plus a **review page** (`plan.html`) the owner opens in a browser to approve, defer or reject each item and paste the decisions back. Then **monitor** on a schedule.

The full reasoning is in [SKILL.md](SKILL.md); the agent-facing rules are in [AGENTS.md](AGENTS.md).

## What the results look like

An audit produces `audit/report.md` plus the JSON behind it. Trimmed example from a real run:

```markdown
# SEO + GEO audit: https://www.example.com

## Summary
- Biggest blocker: OAI-SearchBot and PerplexityBot disallowed in robots.txt (ST01)
- Biggest opportunity: pricing page has no quotable facts; rewrite answer-first (ST03, ST14)
- Baseline: UNKNOWN (no provider keys); 30-prompt set attached for the team to run
- Mode: propose. Next review: 2026-11-24

## Access matrix
| Bot | / | /pricing |
|---|---|---|
| Googlebot | allow | allow |
| OAI-SearchBot | BLOCKED | BLOCKED |
| PerplexityBot | BLOCKED | BLOCKED |
| GPTBot | BLOCKED | BLOCKED |   <- training bot, separate policy

## Prioritised plan
1. **ST01 AI-crawler access and server-rendered HTML** (priority 8.1): OAI-SearchBot blocked on /, /pricing
2. **ST01 ...** (priority 8.1): /: 2 words in raw HTML; AI crawlers do not run JavaScript
3. **ST10 Real authors, reviewers, visible dates** (priority 3.6): /pricing: no visible author or date
4. **ST03 Answer-first passage architecture** (priority 3.15): /pricing: answer-first score 0.00

## Human gates
- robots.txt change needs infra approval; test from verified bot IPs afterwards
- every proposed fact is a [VERIFY] placeholder until a named reviewer fills the claim ledger
```

Next to it sits `audit/plan.html`, a single file that opens in any browser with no server, account or hosted artifact, so it works the same for Codex, Claude Code and CI users. It shows the same plan as a table with a decision dropdown and a note on every row, the content strategy and calendar when they exist, and the full report underneath. The owner marks each row, clicks "Copy decisions" and pastes the generated markdown back to the agent, which then applies only the approved items:

```markdown
## Review decisions (2026-10-28)
- 1 ST01 AI-crawler access and server-rendered HTML: **approve** - infra ticket opened (/deloitte/: 13 words in raw HTML)
- 2 ST10 Real authors, reviewers, visible dates: **defer** - waiting on bios (/: no visible real author)
- 3 ST03 Answer-first passage architecture: **reject** - page is being retired (/studio/: answer-first score 0.29)
```

In propose mode you also get `change-queue.md` and `diffs/*.diff`. The monitor produces `.seo-geo/runs/<timestamp>/monitor-report.md` (and the same as `monitor-report.html`):

```markdown
# Monitor report: https://www.example.com
## Changes since 20261027T213000Z
- [bot_blocked] OAI-SearchBot newly blocked on /pricing
- [visibility_drop] best_for|perplexity: mention 67%->0%, citation 33%->0%
## Next step
Check status.search.google.com for an active update before changing anything.
```

## Getting started with Claude Code

```bash
git clone https://github.com/alinaqi/seo-geo-optimizer ~/.claude/skills/seo-geo-optimizer
cd ~/.claude/skills/seo-geo-optimizer
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp commands/monitor.md ~/.claude/commands/monitor.md        # enables /monitor
```

Then, in any project or an empty folder:

- `audit https://www.example.com for SEO and AI search visibility`
- `review this repo for GEO problems and propose fixes as diffs`
- `audit https://github.com/org/site and write a plan` (the skill clones it first)
- `/monitor` after creating `seo-geo.config.json` from `seo-geo.config.example.json`; `/loop 1w /monitor` makes it recurring.

Optional keys for the AI baseline, exported in your shell: `PERPLEXITY_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`.

## Getting started with Codex

```bash
git clone https://github.com/alinaqi/seo-geo-optimizer ~/seo-geo-optimizer
cd ~/seo-geo-optimizer && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cd /path/to/your/site-repo        # or an empty folder for a URL-only audit
codex "Follow ~/seo-geo-optimizer/AGENTS.md. Target: https://www.example.com. Mode: propose. Write report.md and diffs."
```

Codex reads `AGENTS.md` from the working directory automatically, so you can also copy it into the target repo. For a GitHub target, give the repo URL in the prompt; the guideline tells the agent to clone it first.

## Recurring monitoring

`scripts/monitor.py` snapshots each run under `.seo-geo/runs/<timestamp>/` and diffs it against the previous one: newly blocked search bots, status changes, pages that turned into client-rendered shells, and theme-level visibility drops of 20 points or more. Commit `.seo-geo/` so history persists. Run it from `/monitor`, from `/loop 1w /monitor`, or from CI:

```bash
~/seo-geo-optimizer/.venv/bin/python ~/seo-geo-optimizer/scripts/monitor.py --config seo-geo.config.json --state .seo-geo
```

## Repository layout

- `SKILL.md`: the workflow Claude follows, with the reasoning.
- `AGENTS.md`: the same guideline written for any coding agent.
- `commands/monitor.md`: the `/monitor` slash command for Claude Code.
- `scripts/`: `audit_all.py`, `crawl_audit.py`, `page_lint.py`, `schema_check.py`, `icp_signals.py`, `market_detect.py`, `strategy_plan.py`, `prompt_sampler.py`, `report.py`, `html_plan.py` (review page), `monitor.py`.
- `references/`: strategies, validation checks, measurement, tools, sources (generated from `playbook/`).
- `playbook/`: data modules and `build_xlsx.py` that regenerate the full evidence workbook.
- `evals/`: test cases in the `claude plugin eval` layout.

## Development

```bash
.venv/bin/python -m pytest                       # tests with coverage
.venv/bin/python -m playbook.export_references   # regenerate references/
.venv/bin/python playbook/build_xlsx.py playbook.xlsx
```

MIT licensed. Evidence sources are listed with grades in `references/sources.md`; many 2026 figures come from vendors and change monthly, so re-verify before quoting them.
