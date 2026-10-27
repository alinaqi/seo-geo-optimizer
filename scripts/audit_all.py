"""One-shot audit: access matrix, page lint, schema parity and report for a URL.
Usage: python scripts/audit_all.py https://site --paths / /pricing --outdir audit/"""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urljoin
from scripts import crawl_audit as ca, page_lint as pl, schema_check as sc, report as rp


def run(base, paths, outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    audit = ca.audit(base, paths)
    pages = {p: ca.fetch(urljoin(base, p))[1] for p in paths}
    lint = {p: pl.lint(h) for p, h in pages.items()}
    schema = {p: sc.check(h) for p, h in pages.items()}
    for name, data in {"audit": audit, "lint": lint, "schema": schema}.items():
        (out / f"{name}.json").write_text(json.dumps(data, indent=2))
    (out / "report.md").write_text(rp.render(audit, lint, schema, None))
    return out / "report.md"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--paths", nargs="+", default=["/"])
    ap.add_argument("--outdir", default="audit")
    a = ap.parse_args(argv)
    print("wrote", run(a.url, a.paths, a.outdir))


if __name__ == "__main__":
    main(sys.argv[1:])
