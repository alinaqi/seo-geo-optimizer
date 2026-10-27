# Contributing

## Workflow

1. Open an issue or describe the change in the PR. Architectural changes need an ADR in `docs/adr/` (copy `template.md`, status `proposed`).
2. Tests first: write the failing test, run it, then implement (`.venv/bin/python -m pytest`). Coverage must stay at or above 80%.
3. Keep logic files within the limits in ADR 0006 (20-line functions, 3 parameters, 200-line files).
4. If you change `playbook/data_*.py`, run `.venv/bin/python -m playbook.export_references` and commit the regenerated `references/`.
5. Add a line under `[Unreleased]` in `CHANGELOG.md`.
6. Never commit API keys; scripts read them from the environment only. `.env` is ignored; `.env.example` lists the names.

## Evidence rules

New strategies or claims need a source row in `playbook/data_sources.py` with a grade (A official/primary, B industry dataset, C vendor/practitioner, D unverified). Do not add numbers without a source ID.

## Running the evals

The `evals/` folder follows the `claude plugin eval` layout. From the repo root with Claude Code installed:

```bash
claude plugin eval . --allow-tools Write,Edit,Bash,WebFetch --scaffold
```
