"""Recurring monitor: re-run the audit (and the AI baseline when keys exist), snapshot it under
.seo-geo/runs/<timestamp>/, diff against the previous run and write monitor-report.md.
Usage: python scripts/monitor.py --config seo-geo.config.json [--state .seo-geo]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # allow `python scripts/x.py`
import argparse
import json
from datetime import datetime, timezone
from scripts import crawl_audit as ca, prompt_sampler as ps

REQUIRED = ("url", "paths", "brand", "category", "domain")
DROP = 0.2  # theme-level rate drop that counts as a regression


def load_config(path):
    cfg = json.load(open(path))
    missing = [k for k in REQUIRED if k not in cfg]
    if missing:
        raise SystemExit(f"config missing keys: {missing}")
    cfg.setdefault("competitors", [])
    cfg.setdefault("runs", 3)
    return cfg


def _bot_changes(prev, curr):
    out = []
    for bot in ca.SEARCH_BOTS:
        for path, ok in curr.get("robots", {}).get(bot, {}).items():
            if prev.get("robots", {}).get(bot, {}).get(path, True) and not ok:
                out.append({"kind": "bot_blocked", "detail": f"{bot} newly blocked on {path}"})
    return out


def _page_changes(prev, curr):
    out = []
    for path, page in curr.get("pages", {}).items():
        old = prev.get("pages", {}).get(path, {})
        if old.get("status") != page.get("status"):
            out.append({"kind": "status_changed", "detail": f"{path}: status {old.get('status')} -> {page.get('status')}"})
        if page.get("likely_spa_shell") and not old.get("likely_spa_shell"):
            out.append({"kind": "spa_shell", "detail": f"{path}: raw HTML dropped to {page.get('words')} words (client-side rendering?)"})
    return out


def diff_audit(prev, curr):
    return _bot_changes(prev, curr) + _page_changes(prev, curr)


def diff_baseline(prev, curr):
    out = []
    for key, now in (curr or {}).get("scores", {}).items():
        old = (prev or {}).get("scores", {}).get(key)
        if old and (old["mention_rate"] - now["mention_rate"] >= DROP or old["citation_rate"] - now["citation_rate"] >= DROP):
            out.append({"kind": "visibility_drop", "detail": f"{key}: mention {old['mention_rate']:.0%}->{now['mention_rate']:.0%}, citation {old['citation_rate']:.0%}->{now['citation_rate']:.0%}"})
    return out


def _previous(state):
    runs = sorted((state / "runs").glob("*")) if (state / "runs").exists() else []
    return runs[-1] if runs else None


def _load(path):
    return json.load(open(path)) if path and path.exists() else None


def _baseline(cfg):
    provs = ps.available_providers()
    if not provs:
        return None
    prompts = ps.build_prompts(cfg["category"], cfg["brand"], cfg["competitors"])
    records = ps.sample(prompts, provs, cfg["runs"])
    scores = {f"{t}|{p}": v for (t, p), v in ps.score(records, cfg["brand"], cfg["domain"]).items()}
    return {"providers": provs, "records": records, "scores": scores}


def _render(prev_dir, changes, audit):
    since = prev_dir.name if prev_dir else "first run (no previous snapshot)"
    lines = [f"# Monitor report: {audit.get('url')}", f"## Changes since {since}"]
    lines += [f"- [{c['kind']}] {c['detail']}" for c in changes] or ["- no regressions detected"]
    lines += ["## Current access findings"] + [f"- {f}" for f in audit.get("robots_findings", [])] or []
    lines.append("## Next step\nIf a bot block, status change or visibility drop appears, open the full skill workflow (SKILL.md step 1 and 4) before changing anything; check the Google Search Status Dashboard for an active update first.")
    return "\n".join(lines) + "\n"


def run(config_path, state):
    cfg = load_config(config_path)
    state = Path(state)
    prev_dir = _previous(state)
    out = state / "runs" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out.mkdir(parents=True)
    audit, baseline = ca.audit(cfg["url"], cfg["paths"]), _baseline(cfg)
    (out / "audit.json").write_text(json.dumps(audit, indent=2))
    if baseline:
        (out / "baseline.json").write_text(json.dumps(baseline, indent=2))
    changes = diff_audit(_load(prev_dir / "audit.json" if prev_dir else None) or {}, audit)
    changes += diff_baseline(_load(prev_dir / "baseline.json" if prev_dir else None), baseline)
    report = out / "monitor-report.md"
    report.write_text(_render(prev_dir, changes, audit))
    return report


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="seo-geo.config.json")
    ap.add_argument("--state", default=".seo-geo")
    a = ap.parse_args(argv)
    report = run(a.config, a.state)
    print(report.read_text())


if __name__ == "__main__":
    main(sys.argv[1:])
