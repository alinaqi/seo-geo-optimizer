"""Combine audit outputs into a prioritised plan and markdown report.
Usage: python scripts/report.py --audit audit.json --lint lint.json --schema schema.json [--baseline baseline.json] --out report.md"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # allow `python scripts/x.py`
import argparse
import json

# win probability, impact, effort, risk from the playbook (references/strategies.md)
STRATEGY = {"ST01": ("AI-crawler access and server-rendered HTML", 0.90, 3, 1, 1),
            "ST03": ("Answer-first passage architecture", 0.70, 3, 2, 1),
            "ST10": ("Real authors, reviewers, visible dates", 0.60, 2, 1, 1),
            "ST11": ("Structured data hygiene", 0.55, 1, 1, 1),
            "ST20": ("AI visibility measurement program", 0.85, 2, 2, 1),
            "ST02": ("Content refresh and decay program", 0.75, 3, 2, 1)}
GATES = ["Human fact-check of every AI-assisted change, including titles, meta descriptions, schema and alt text (Google, 1 Oct 2026).",
         "robots.txt, CDN or WAF changes need infra approval; test from verified bot IPs after the change.",
         "No automated publishing above the velocity cap; pause during confirmed Google update rollouts.",
         "No community posting by agents; humans post with disclosure.",
         "Do not report llms.txt or schema as AI-citation levers."]


def _priority(sid):
    _, win, impact, effort, risk = STRATEGY[sid]
    return round(win * impact * (4 - risk) / effort, 2)


def _item(sid, finding):
    return {"strategy": sid, "name": STRATEGY[sid][0], "finding": finding, "priority": _priority(sid)}


def _access_items(audit):
    items = [_item("ST01", f) for f in audit.get("robots_findings", [])]
    for path, page in audit.get("pages", {}).items():
        if page.get("likely_spa_shell"):
            items.append(_item("ST01", f"{path}: {page.get('words', 0)} words in raw HTML; AI crawlers do not run JavaScript"))
    return items


def _content_items(lint, schema):
    items = []
    for path, res in lint.items():
        items += [_item("ST10" if ("author" in f or "date" in f) else "ST03", f"{path}: {f}") for f in res.get("findings", [])]
    for path, res in schema.items():
        items += [_item("ST11", f"{path}: schema {m['key']}='{m['value']}' not in visible text") for m in res.get("mismatches", [])]
    return items


def build_plan(audit, lint, schema):
    items = _access_items(audit) + _content_items(lint, schema) + [_item("ST20", "establish weekly prompt-set baseline across engines")]
    return sorted(items, key=lambda i: -i["priority"])


def _matrix_md(audit):
    bots = list(audit.get("robots", {}))
    paths = list(next(iter(audit["robots"].values()), {})) if bots else []
    lines = ["| Bot | " + " | ".join(paths) + " |", "|---|" + "---|" * len(paths)]
    for bot in bots:
        lines.append(f"| {bot} | " + " | ".join("allow" if audit["robots"][bot][p] else "BLOCKED" for p in paths) + " |")
    return "\n".join(lines)


def _baseline_md(baseline):
    if not baseline:
        return "No baseline sampled yet (set provider API keys and run prompt_sampler.py)."
    rows = ["| Theme | Provider | n | Mention rate | Citation rate |", "|---|---|---|---|---|"]
    for key, v in baseline.get("scores", {}).items():
        theme, prov = key.split("|")
        rows.append(f"| {theme} | {prov} | {v['n']} | {v['mention_rate']:.0%} | {v['citation_rate']:.0%} |")
    return "\n".join(rows)


def render(audit, lint, schema, baseline):
    plan = build_plan(audit, lint, schema)
    plan_md = "\n".join(f"{i}. **{p['strategy']} {p['name']}** (priority {p['priority']}): {p['finding']}" for i, p in enumerate(plan, 1))
    return "\n\n".join([f"# SEO + GEO audit: {audit.get('url', '')}", "## Access matrix", _matrix_md(audit),
                        "## Prioritised plan", plan_md, "## AI visibility baseline", _baseline_md(baseline),
                        "## Human gates", "\n".join(f"- {g}" for g in GATES)])


def main(argv=None):
    ap = argparse.ArgumentParser()
    for name in ("--audit", "--lint", "--schema"):
        ap.add_argument(name, required=True)
    ap.add_argument("--baseline")
    ap.add_argument("--out", default="report.md")
    a = ap.parse_args(argv)
    load = lambda p: json.load(open(p)) if p else None
    open(a.out, "w").write(render(load(a.audit), load(a.lint), load(a.schema), load(a.baseline)))
    print("wrote", a.out)


if __name__ == "__main__":
    main(sys.argv[1:])
