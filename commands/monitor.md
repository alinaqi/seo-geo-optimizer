---
description: Re-audit the configured site for SEO/GEO regressions, diff against the last snapshot, and recommend actions
argument-hint: [path to seo-geo.config.json]
allowed-tools: Bash, Read, Glob, Grep
---

Run the recurring SEO + GEO monitor for this project and report what changed.

1. Locate the config: use `$ARGUMENTS` if given, otherwise `seo-geo.config.json` in the current directory. If it does not exist, create it from `seo-geo.config.example.json` in the seo-geo-optimizer skill directory and ask the user for url, paths, brand, domain and category before continuing.
2. Run the monitor script from the seo-geo-optimizer skill directory (`~/.claude/skills/seo-geo-optimizer` unless the user installed it elsewhere):
   `"<skill-dir>/.venv/bin/python" "<skill-dir>/scripts/monitor.py" --config <config> --state .seo-geo`
   It writes `.seo-geo/runs/<timestamp>/` with audit.json, baseline.json (only when provider API keys are set in the environment) and monitor-report.md.
3. Read the new monitor-report.md and the previous run's audit.json. Summarise in this order: regressions (a search bot newly blocked, a status change, a page that became a client-rendered shell, a theme-level visibility drop of 20 points or more), then unchanged areas, then the AI baseline status (UNKNOWN if no keys).
4. Before attributing any visibility drop to the site, check whether a Google core or spam update is rolling out (status.search.google.com) or whether an engine changed behaviour; say so in the report.
5. Recommend at most three actions, each tagged with a strategy ID from the skill's references/strategies.md and its human gate. Do not change robots.txt, CDN settings, metadata or content from this command; it is read-only.
6. If the user wants this to recur, suggest `/loop 1w /monitor` in Claude Code, or a CI/cron job running the same script, and commit `.seo-geo/` so snapshots persist.
