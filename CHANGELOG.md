# Changelog

All notable changes to this project are documented here. The format follows Keep a Changelog; versions follow Semantic Versioning.

## [Unreleased]

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
