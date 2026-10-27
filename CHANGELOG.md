# Changelog

All notable changes to this project are documented here. The format follows Keep a Changelog; versions follow Semantic Versioning.

## [Unreleased]

## [0.3.0] - 2026-10-27

### Added
- ICP and market discovery: `scripts/icp_signals.py`, `scripts/market_detect.py`, `scripts/markets_data.py`.
- Content strategy generator: `scripts/strategy_plan.py` (briefs, capped calendar, prompt rows).
- `references/icp-and-markets.md` with the Oct 2026 market table, ICP sheet and brief templates.
- Playbook strategies ST25-ST27 and sources S76-S87; ADR 0007.
- SKILL.md steps 1b (ICP and market discovery) and 4b (content strategy); eval case `icp-two-market-strategy`.

## [0.2.0] - 2026-10-27

### Added
- `AGENTS.md` guideline for any coding agent (Claude Code, Codex), including GitHub-repo targets.
- `/monitor` command (`commands/monitor.md`) and `scripts/monitor.py` with snapshot diffing.
- `seo-geo.config.example.json`.
- Plain-language README: what works from August 2026, what does not, the guideline, sample results, getting started for Claude Code and Codex.
- Architecture decision records in `docs/adr/`, this changelog, `CONTRIBUTING.md`, `.env.example`, CI workflow.

### Changed
- Date wording: "from August 2026" instead of a fixed range.

## [0.1.0] - 2026-10-27

### Added
- Initial skill: `SKILL.md`, audit scripts (`crawl_audit`, `page_lint`, `schema_check`, `prompt_sampler`, `report`, `audit_all`), references generated from the playbook data, workbook builder, three eval cases, tests with 97% coverage.
