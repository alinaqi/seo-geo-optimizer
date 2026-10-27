from pathlib import Path
from scripts import icp_signals as ic

HTML = Path("tests/fixtures/de_site.html").read_text()


def test_extracts_roles_industries_and_size_with_evidence():
    s = ic.extract(HTML)
    assert "HR" in s["roles"] and "L&D" in s["roles"]
    assert {"healthcare", "financial services"} <= set(s["industries"])
    assert s["company_size"]["band"] == "mid-market"
    assert any("200 bis 2000" in e for e in s["company_size"]["evidence"])


def test_extracts_pricing_model_and_review_platforms():
    s = ic.extract(HTML)
    assert s["pricing"]["model"] == "from-price"
    assert s["pricing"]["from"] == "€990"
    assert {"G2", "OMR Reviews"} <= set(s["review_platforms"])


def test_extracts_proof_and_marks_unknowns():
    s = ic.extract(HTML)
    assert any("200 reps" in q for q in s["proof_quotes"])
    weak = ic.extract("<html><body><p>Hello</p></body></html>")
    assert weak["roles"] == [] and weak["company_size"]["band"] == "UNKNOWN"


def test_icp_sheet_rows_have_required_fields():
    rows = ic.icp_sheet(ic.extract(HTML))
    assert rows and {"segment", "roles", "industries", "size", "evidence", "confidence"} <= set(rows[0])
