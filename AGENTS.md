# Guideline for coding agents (Claude Code, Codex, others)

You are optimizing a website or web app for SEO and GEO/AEO: being found in Google and being cited by ChatGPT, Perplexity, Google AI Overviews and AI Mode, Claude and Copilot. Follow this file in order. The reasoning behind each step is in `SKILL.md`; the evidence is in `references/`.

## 1. Set up

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q      # should pass before you rely on the scripts
```

API keys are optional and come from the environment only: `PERPLEXITY_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`. Never write a key into a file, a report or a commit.

## 2. Identify the target

The target is one of:
- a live URL (`https://www.example.com`): audit mode by default;
- a local repository path: propose mode by default (diffs and a change queue, nothing merged);
- a GitHub repository URL: clone it first, then treat it as a local repository:

```bash
git clone --depth 1 https://github.com/org/repo target/ && cd target
```

Never run the audit scripts from inside the cloned target with the target on `sys.path`; call them by absolute path from this skill directory.

## 3. Run the audit

```bash
<skill-dir>/.venv/bin/python <skill-dir>/scripts/audit_all.py https://www.example.com --paths / /pricing /blog/post --outdir audit/
```

For a repository that is not deployed, reconstruct the HTML each route would emit (read the templates and the rendering mode) and run `page_lint.py` and `schema_check.py` on that HTML; run `crawl_audit.parse_robots` on `public/robots.txt`. Label those results as reconstructed, not crawled.

## 3b. Discover ICP and markets

```bash
<skill-dir>/.venv/bin/python <skill-dir>/scripts/icp_signals.py audit/page.html
<skill-dir>/.venv/bin/python <skill-dir>/scripts/market_detect.py audit/page.html --url https://www.example.com
```

Write the ICP sheet (`references/icp-and-markets.md` has the template and the per-market engine table) with evidence quotes and UNKNOWN where the site gives none. Then, once the owner confirms it, save it as `icp.json` and run `scripts/strategy_plan.py --icp icp.json --outdir strategy/` to get briefs, a capped calendar and measurement prompts.

## 4. Decide and write

Read `references/strategies.md` for the strategy each finding maps to, its autonomy level (AUTO, PROPOSE, ASSIST) and its human gate. Then write the report in the structure given in `SKILL.md` step 6, and in propose or apply mode produce unified diffs that apply with `patch -p1`.

Non-negotiable rules:
- Search and retrieval bots (OAI-SearchBot, Claude-SearchBot, PerplexityBot, ChatGPT-User, Claude-User, Perplexity-User, Googlebot, Bingbot) must be allowed on citable pages. Training bots (GPTBot, ClaudeBot, Google-Extended, CCBot) are a separate decision; never present allowing GPTBot as the fix for ChatGPT citations.
- Main content must be present in server-rendered HTML; OpenAI, Anthropic and Perplexity crawlers do not execute JavaScript.
- Every factual claim you write or change gets a claim ledger entry (claim, source URL, retrieval date) and is marked for human fact-check, including titles, meta descriptions, schema and alt text.
- Do not change robots.txt, CDN or WAF rules, publish pages, post to communities, bulk-generate pages, or alter dates without a substantive content change. Stop before merge or deploy.
- Do not recommend llms.txt, schema markup, AI-specific rewriting or self-ranked listicles as ways to earn AI citations.
- A finding you could not verify stays UNKNOWN, never PASS or FAIL.

## 5. Monitor

Create `seo-geo.config.json` in the target project (copy `seo-geo.config.example.json`) and run:

```bash
<skill-dir>/.venv/bin/python <skill-dir>/scripts/monitor.py --config seo-geo.config.json --state .seo-geo
```

Each run snapshots to `.seo-geo/runs/<timestamp>/` and diffs against the previous run. In Claude Code the same flow is the `/monitor` command (`commands/monitor.md`).
