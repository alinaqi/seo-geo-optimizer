import json
from scripts import monitor as mo

PREV = {"robots": {"OAI-SearchBot": {"/": True}, "GPTBot": {"/": False}}, "pages": {"/": {"status": 200, "words": 500, "likely_spa_shell": False}}}
CURR = {"robots": {"OAI-SearchBot": {"/": False}, "GPTBot": {"/": False}}, "pages": {"/": {"status": 500, "words": 20, "likely_spa_shell": True}}}


def test_load_config_requires_url_and_paths(tmp_path):
    cfg = tmp_path / "seo-geo.config.json"
    cfg.write_text(json.dumps({"url": "https://acme.example", "paths": ["/"], "brand": "Acme", "category": "x", "domain": "acme.example"}))
    c = mo.load_config(cfg)
    assert c["url"] == "https://acme.example" and c["paths"] == ["/"]


def test_diff_flags_new_bot_blocks_status_and_ssr_regressions():
    changes = mo.diff_audit(PREV, CURR)
    kinds = {c["kind"] for c in changes}
    assert {"bot_blocked", "status_changed", "spa_shell"} <= kinds
    assert any("OAI-SearchBot" in c["detail"] for c in changes)
    assert not any("GPTBot" in c["detail"] for c in changes)


def test_diff_is_empty_when_nothing_changed():
    assert mo.diff_audit(PREV, PREV) == []


def test_diff_baseline_reports_rate_drops():
    prev = {"scores": {"best_for|perplexity": {"n": 3, "mention_rate": 0.67, "citation_rate": 0.33}}}
    curr = {"scores": {"best_for|perplexity": {"n": 3, "mention_rate": 0.0, "citation_rate": 0.0}}}
    changes = mo.diff_baseline(prev, curr)
    assert changes and changes[0]["kind"] == "visibility_drop"
    assert mo.diff_baseline(prev, prev) == []


def test_run_writes_snapshot_and_report(monkeypatch, tmp_path):
    cfg = tmp_path / "seo-geo.config.json"
    cfg.write_text(json.dumps({"url": "https://acme.example", "paths": ["/"], "brand": "Acme", "category": "x", "domain": "acme.example"}))
    monkeypatch.setattr(mo.ca, "audit", lambda base, paths: PREV)
    monkeypatch.setattr(mo.ps, "available_providers", lambda: [])
    first = mo.run(cfg, tmp_path / ".seo-geo")
    monkeypatch.setattr(mo.ca, "audit", lambda base, paths: CURR)
    second = mo.run(cfg, tmp_path / ".seo-geo")
    report = second.read_text()
    assert "## Changes since" in report and "OAI-SearchBot" in report and first != second
