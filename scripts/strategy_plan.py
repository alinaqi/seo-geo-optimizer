"""Turn an ICP sheet into content briefs, a capped calendar and strategy.md.
Usage: python scripts/strategy_plan.py --icp icp.json --outdir strategy/ [--weekly-cap 3 --weeks 13]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # allow `python scripts/x.py`
import argparse
import csv
import json

THEMES = [("definition", "What is {category}? Who is it for?", "ST09"), ("best_for", "Best {category} for {segment}", "ST14"),
          ("comparison", "{brand} vs {competitor} for {segment}", "ST14"), ("pricing", "What does {category} cost for {segment}?", "ST22"),
          ("how_to", "How does {segment} get started with {category}?", "ST09"), ("proof", "Case study: {segment} results with {brand}", "ST04")]
GAIN = {"definition": "own definition plus a sourced market figure", "best_for": "explicit fit and not-for statements from win/loss data",
        "comparison": "sourced comparison cells with retrieval dates", "pricing": "real price drivers and billing basis",
        "how_to": "screenshots or steps from a real implementation", "proof": "named customer, metric, timeframe, approval on file"}
GATE = {"comparison": "product marketing + legal (REVIEW_REQUIRED)", "proof": "customer approval + data owner (HARD_BLOCK)",
        "pricing": "finance confirms figures", "definition": "content lead", "best_for": "product marketing", "how_to": "product owner"}


def _brief(seg, theme, lang, icp, n):
    key, title, sid = theme
    comp = (icp.get("competitors") or ["the alternative"])[0]
    t = title.format(category=icp["category"], segment=seg["segment"], brand=icp["brand"], competitor=comp)
    return {"id": f"B{n:03d}", "segment": seg["segment"], "theme": key, "language": lang, "strategy": sid, "intent": t,
            "engines": ", ".join(seg.get("engines", [])), "information_gain": GAIN[key], "gate": GATE[key],
            "author": "named human author (UNKNOWN until assigned)",
            "prompts": [t, f"{t} in {', '.join(seg.get('markets', []))}"]}


def build_briefs(icp):
    briefs, n = [], 1
    for seg in icp["segments"]:
        for lang in seg.get("languages", ["en"]):
            for theme in THEMES:
                briefs.append(_brief(seg, theme, lang, icp, n))
                n += 1
    return briefs


def schedule(briefs, weekly_cap=3, weeks=13):
    order = sorted(briefs, key=lambda b: ["definition", "best_for", "comparison", "pricing", "how_to", "proof"].index(b["theme"]))
    cal = []
    for i, b in enumerate(order[: weekly_cap * weeks]):
        cal.append({"week": i // weekly_cap + 1, **{k: (", ".join(v) if isinstance(v, list) else v) for k, v in b.items()}})
    return cal


def _segments_md(icp):
    return "\n".join(f"- **{s['segment']}**: roles {', '.join(s.get('roles', []))}; markets {', '.join(s.get('markets', []))}; "
                     f"languages {', '.join(s.get('languages', []))}; engines to sample {', '.join(s.get('engines', []))}" for s in icp["segments"])


def render(icp, cal, cap):
    rows = "\n".join(f"| {r['week']} | {r['id']} | {r['segment']} | {r['theme']} | {r['language']} | {r['strategy']} | {r['gate']} |" for r in cal)
    return "\n\n".join([f"# Content strategy: {icp['brand']} ({icp['category']})", "## ICP segments", _segments_md(icp),
                        f"## Velocity cap\n{cap} pages per week, never above the named reviewer's fact-check capacity; pause during confirmed Google update rollouts.",
                        "## Calendar", "| Week | Brief | Segment | Theme | Lang | Strategy | Gate |\n|---|---|---|---|---|---|---|\n" + rows,
                        "## Rules\n- Every brief states its information gain before writing starts; no 'summarise the top 10' briefs.\n- Each brief has a named human author, visible date and references.\n- The prompts column feeds the weekly measurement set (ST20).\n- Unknown facts stay UNKNOWN until a reviewer fills the claim ledger."])


def write(icp, outdir, weekly_cap=3, weeks=13):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    cal = schedule(build_briefs(icp), weekly_cap, weeks)
    with open(out / "calendar.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cal[0].keys()))
        w.writeheader()
        w.writerows(cal)
    (out / "strategy.md").write_text(render(icp, cal, weekly_cap))
    return out / "strategy.md"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--icp", required=True)
    ap.add_argument("--outdir", default="strategy")
    ap.add_argument("--weekly-cap", type=int, default=3)
    ap.add_argument("--weeks", type=int, default=13)
    a = ap.parse_args(argv)
    print("wrote", write(json.load(open(a.icp)), a.outdir, a.weekly_cap, a.weeks))


if __name__ == "__main__":
    main(sys.argv[1:])
