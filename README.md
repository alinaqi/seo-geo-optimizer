# seo-geo-optimizer

A Claude Code skill that audits and optimizes any website or web app for SEO and GEO/AEO (being cited by ChatGPT, Perplexity, Google AI Overviews and AI Mode, Claude and Copilot). It is built on an evidence-graded playbook of practice from August to October 2026: 24 strategies with win-probability estimates, 30 validation checks, 12 penalty safeguards and 75 graded sources.

## Install

```bash
git clone https://github.com/alinaqi/seo-geo-optimizer ~/.claude/skills/seo-geo-optimizer
cd ~/.claude/skills/seo-geo-optimizer
python -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Then in Claude Code: "audit https://yoursite.com for SEO and AI search visibility".

Optional API keys for the measurement baseline, as environment variables only: `PERPLEXITY_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`.

## What it does

1. Access audit: robots rules per bot (search bots vs training bots), status codes by user agent, server-rendered text check.
2. Page audit: answer-first structure, entity-clean language, visible authors and dates, claim ledger, schema-to-text parity.
3. Measurement baseline: themed prompt set sampled across engines with repeated runs.
4. Prioritised plan scored by win probability x impact x (4 - risk) / effort.
5. Gated execution: audit, propose (diffs and change queue) or apply (branch edits, never publish).

## Layout

- `SKILL.md`: the workflow Claude follows.
- `scripts/`: `audit_all.py`, `crawl_audit.py`, `page_lint.py`, `schema_check.py`, `prompt_sampler.py`, `report.py`.
- `references/`: strategies, validation, measurement, tools, sources (generated from `playbook/`).
- `playbook/`: data modules plus `build_xlsx.py` to regenerate the full workbook.
- `evals/`: test cases in the `claude plugin eval` layout.

## Run tests

```bash
.venv/bin/python -m pytest
```

## Regenerate references and the workbook

```bash
.venv/bin/python -m playbook.export_references
.venv/bin/python playbook/build_xlsx.py SEO_AEO_Agentic_Playbook_2026.xlsx
```

MIT licensed.
