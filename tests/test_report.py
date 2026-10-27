from scripts import report as rp

AUDIT = {"url": "https://acme.example", "robots": {"OAI-SearchBot": {"/": False}, "Googlebot": {"/": True}},
         "robots_findings": ["OAI-SearchBot blocked on /"], "pages": {"/": {"status": 200, "words": 30, "likely_spa_shell": True}}}
LINT = {"/": {"answer_first_score": 0.3, "findings": ["answer-first score 0.30 below 0.8"], "eeat": {"author": None}}}
SCHEMA = {"/": {"mismatches": [{"key": "headline", "value": "x"}], "warnings": []}}


def test_plan_maps_findings_to_strategy_ids_and_sorts_by_priority():
    plan = rp.build_plan(AUDIT, LINT, SCHEMA)
    ids = [p["strategy"] for p in plan]
    assert ids[0] == "ST01"
    assert "ST03" in ids and "ST11" in ids
    assert all(p["priority"] >= q["priority"] for p, q in zip(plan, plan[1:]))


def test_markdown_report_has_required_sections():
    md = rp.render(AUDIT, LINT, SCHEMA, None)
    for h in ["# SEO + GEO audit", "## Access matrix", "## Prioritised plan", "## Human gates"]:
        assert h in md
    assert "OAI-SearchBot" in md
