import csv, json
from scripts import strategy_plan as sp

ICP = {"brand": "Acme", "category": "corporate learning platform", "segments": [
    {"segment": "HR leaders, mid-market DACH", "roles": ["HR"], "markets": ["DACH"], "languages": ["de", "en"], "engines": ["Google AI Mode", "ChatGPT"]},
    {"segment": "Sales enablement, US", "roles": ["Head of Sales"], "markets": ["US"], "languages": ["en"], "engines": ["ChatGPT", "Perplexity"]}],
    "competitors": ["360Learning", "Docebo"]}


def test_briefs_cover_each_segment_theme_and_language():
    briefs = sp.build_briefs(ICP)
    assert any(b["segment"].startswith("HR") and b["theme"] == "comparison" and b["language"] == "de" for b in briefs)
    assert all({"id", "segment", "theme", "language", "intent", "information_gain", "gate", "prompts"} <= set(b) for b in briefs)


def test_calendar_respects_velocity_cap():
    briefs = sp.build_briefs(ICP)
    cal = sp.schedule(briefs, weekly_cap=3, weeks=13)
    per_week = {}
    for row in cal:
        per_week[row["week"]] = per_week.get(row["week"], 0) + 1
    assert max(per_week.values()) <= 3
    assert len(cal) <= 39


def test_render_writes_strategy_md_and_csv(tmp_path):
    out = sp.write(ICP, tmp_path, weekly_cap=2, weeks=4)
    assert (tmp_path / "strategy.md").exists() and (tmp_path / "calendar.csv").exists()
    rows = list(csv.DictReader(open(tmp_path / "calendar.csv")))
    assert rows and "gate" in rows[0]
    text = (tmp_path / "strategy.md").read_text()
    assert "## ICP segments" in text and "velocity cap" in text.lower()
