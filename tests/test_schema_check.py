from pathlib import Path
from scripts import schema_check as sc

GOOD = Path("tests/fixtures/good_page.html").read_text()
WEAK = Path("tests/fixtures/weak_page.html").read_text()


def test_jsonld_blocks_are_loaded():
    blocks = sc.load_jsonld(GOOD)
    assert blocks[0]["@type"] == "Article"


def test_parity_passes_when_schema_values_appear_in_text():
    report = sc.check(GOOD)
    assert report["mismatches"] == []


def test_parity_flags_values_missing_from_visible_text():
    report = sc.check(WEAK)
    keys = {m["key"] for m in report["mismatches"]}
    assert "headline" in keys and "author.name" in keys


def test_unsupported_or_risky_types_are_flagged():
    html = '<html><body><script type="application/ld+json">{"@type":"FAQPage","mainEntity":[]}</script><p>hi</p></body></html>'
    report = sc.check(html)
    assert any("FAQPage" in w for w in report["warnings"])
