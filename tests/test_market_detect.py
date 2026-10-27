from pathlib import Path
from scripts import market_detect as md

HTML = Path("tests/fixtures/de_site.html").read_text()


def test_detects_declared_lang_and_hreflang():
    r = md.detect(HTML, url="https://example.de/")
    assert r["html_lang"] == "en-US"
    assert set(r["hreflang"]) == {"de", "en"}


def test_detects_js_language_swap_and_language_mismatch():
    r = md.detect(HTML, url="https://example.de/")
    assert r["js_language_swap"]["pattern"] == "data-en"
    assert r["js_language_swap"]["count"] >= 2
    assert r["detected_text_language"] == "de"
    assert any("lang" in f for f in r["findings"])


def test_detects_currency_and_geography_cues():
    r = md.detect(HTML, url="https://example.de/")
    assert "EUR" in r["currencies"]
    assert {"Germany", "Austria", "Switzerland"} <= set(r["geographies"])
    assert r["tld"] == "de"


def test_market_profile_lists_engines_for_detected_markets():
    r = md.detect(HTML, url="https://example.de/")
    profile = md.market_profile(r)
    assert any(m["market"] == "DACH" for m in profile)
    dach = next(m for m in profile if m["market"] == "DACH")
    assert "OMR Reviews" in dach["review_platforms"]
    assert "Google AI Mode" in dach["engines"]
