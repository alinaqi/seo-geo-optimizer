# 0006 - Quality gates, TDD and CI

**Status:** accepted
**Date:** 2026-10-27
**Spec:** pytest.ini, .github/workflows/ci.yml, CONTRIBUTING.md
**Deciders:** Ali Naqi Shaheen

## Context

The scripts are run by agents without supervision; silent breakage would produce wrong audits.

## Decision

Every script change follows RED-GREEN-VALIDATE: failing test first, minimal implementation, then the full suite with coverage at or above 80% (currently 95%+). Limits for logic files: 20 lines per function, 3 parameters, nesting depth 2, 200 lines per file, 10 functions per file. Data modules under `playbook/` are exempt from the line limit because they contain no logic. Network calls are isolated in `providers.py` and tested with monkeypatched HTTP. CI runs the suite and checks that generated references are current.

## Consequences

- Small modules, more files.
- Contributors must regenerate references when changing playbook data.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| No coverage gate | Faster | Regressions reach agents | Unacceptable for unattended use |

## Links

- Related: ADR 0001
