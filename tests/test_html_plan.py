import json
from scripts import html_plan as hp, audit_all as aa, crawl_audit as ca, monitor as mo

AUDIT = {"url": "https://acme.example", "robots": {"Googlebot": {"/": True}, "OAI-SearchBot": {"/": False}},
         "robots_findings": ["OAI-SearchBot blocked on /"], "pages": {"/": {"words": 12, "likely_spa_shell": True}}}


def _outdir(tmp_path):
    (tmp_path / "audit.json").write_text(json.dumps(AUDIT))
    (tmp_path / "lint.json").write_text(json.dumps({"/": {"findings": ["no visible author or date"]}}))
    (tmp_path / "schema.json").write_text(json.dumps({"/": {"mismatches": []}}))
    (tmp_path / "report.md").write_text("# SEO + GEO audit: https://acme.example\n\n## Summary\n- Biggest blocker: bots\n")
    return tmp_path


def test_plan_table_has_items_and_decision_controls(tmp_path):
    html = hp.build(_outdir(tmp_path))
    assert "ST01" in html and "ST10" in html
    assert 'class="decision"' in html and "Copy decisions" in html
    assert "<h2" in html and "Summary" in html


def test_plan_is_self_contained(tmp_path):
    html = hp.build(_outdir(tmp_path))
    assert "<script src=" not in html and "https://cdn" not in html
    assert "prefers-color-scheme" in html


def test_strategy_calendar_included_when_present(tmp_path):
    out = _outdir(tmp_path)
    (out / "strategy.md").write_text("# Content strategy: Acme\n\n## Calendar\n| Week | Brief |\n|---|---|\n| 1 | B001 |\n")
    (out / "calendar.csv").write_text("week,id,segment,theme,language,strategy,gate\n1,B001,SMB,definition,en,ST09,content lead\n")
    html = hp.build(out)
    assert "B001" in html and "Content strategy" in html and "definition" in html


def test_write_and_cli(tmp_path):
    out = _outdir(tmp_path)
    hp.main(["--outdir", str(out)])
    assert (out / "plan.html").read_text().startswith("<!doctype html>")


def test_audit_all_writes_plan_html(monkeypatch, tmp_path):
    html = open("tests/fixtures/good_page.html").read()
    monkeypatch.setattr(ca, "fetch", lambda url, ua="Browser", timeout=15: (200, "User-agent: *\nDisallow:\n" if url.endswith("robots.txt") else html))
    aa.run("https://acme.example", ["/"], tmp_path / "a")
    assert (tmp_path / "a" / "plan.html").exists()


def test_monitor_writes_html(monkeypatch, tmp_path):
    cfg = {"url": "https://acme.example", "paths": ["/"], "brand": "Acme", "category": "crm", "domain": "acme.example", "competitors": [], "runs": 1}
    (tmp_path / "cfg.json").write_text(json.dumps(cfg))
    monkeypatch.setattr(ca, "audit", lambda base, paths: AUDIT)
    monkeypatch.setattr(mo, "_baseline", lambda cfg: None)
    report = mo.run(tmp_path / "cfg.json", tmp_path / "state")
    assert (report.parent / "monitor-report.html").exists()


def test_markdown_tables_get_scroll_container():
    assert '<div class="tbl"><table>' in hp.md("| a | b |\n|---|---|\n| 1 | 2 |\n")
