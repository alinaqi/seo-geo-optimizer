"""Build a themed prompt set and sample AI engines to measure mentions and citations.
Usage: python scripts/prompt_sampler.py --category "X" --brand "Y" --domain y.com --competitors A B --runs 3 --out baseline.json"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # allow `python scripts/x.py`
import argparse
import json
import os
from collections import defaultdict
from scripts import providers

ENV_KEYS = {"perplexity": "PERPLEXITY_API_KEY", "openai": "OPENAI_API_KEY", "gemini": "GEMINI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
THEMES = {
    "definition": ["What is {category} and why does it matter in 2026?", "Explain {category} to a marketing lead in plain language."],
    "best_for": ["What are the best {category} tools for a mid-size B2B company?", "Recommend {category} software for a small team on a budget."],
    "comparison": ["Compare {brand} vs {competitor} for {category}.", "{brand} or {competitor}: which should I pick and why?"],
    "pricing": ["How much does {brand} cost and is it worth it?", "What is typical pricing for {category} tools?"],
    "how_to": ["How do I get started with {category} step by step?"],
    "brand_facts": ["What is {brand}? Who makes it and what does it do?", "Is {brand} a reliable {category} provider?"],
    "alternatives": ["What are good alternatives to {brand}?"],
}


def build_prompts(category, brand, competitors):
    comp = competitors[0] if competitors else "the market leader"
    out = []
    for theme, templates in THEMES.items():
        for t in templates:
            out.append({"theme": theme, "prompt": t.format(category=category, brand=brand, competitor=comp)})
    return out


def available_providers():
    return [p for p, key in ENV_KEYS.items() if os.environ.get(key)]


def sample(prompts, provs, runs=1):
    records = []
    for p in prompts:
        for prov in provs:
            for i in range(runs):
                answer, sources = providers.CLIENTS[prov](p["prompt"])
                records.append({**p, "provider": prov, "run": i + 1, "answer": answer, "sources": [s for s in sources if s]})
    return records


def score(records, brand, domain):
    groups = defaultdict(list)
    for r in records:
        groups[(r["theme"], r["provider"])].append(r)
    out = {}
    for key, rows in groups.items():
        n = len(rows)
        mentions = sum(brand.lower() in r["answer"].lower() for r in rows)
        cites = sum(any(domain in (s or "") for s in r["sources"]) for r in rows)
        out[key] = {"n": n, "mention_rate": mentions / n, "citation_rate": cites / n}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    for name in ("--category", "--brand", "--domain"):
        ap.add_argument(name, required=True)
    ap.add_argument("--competitors", nargs="*", default=[])
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--out", default="baseline.json")
    a = ap.parse_args(argv)
    provs = available_providers()
    records = sample(build_prompts(a.category, a.brand, a.competitors), provs, a.runs)
    scores = {f"{t}|{p}": v for (t, p), v in score(records, a.brand, a.domain).items()}
    json.dump({"providers": provs, "records": records, "scores": scores}, open(a.out, "w"), indent=2)
    print(json.dumps(scores, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
