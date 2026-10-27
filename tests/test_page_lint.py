from pathlib import Path
from scripts import page_lint as pl

GOOD = Path("tests/fixtures/good_page.html").read_text()
WEAK = Path("tests/fixtures/weak_page.html").read_text()


def test_sections_are_extracted_with_headings():
    secs = pl.extract_sections(GOOD)
    assert [s["heading"] for s in secs][:2] == ["What is answer engine optimization?", "How does Acme Analytics track citations?"]
    assert secs[0]["words"] > 20


def test_answer_first_score_is_high_for_good_page_and_low_for_weak():
    assert pl.answer_first_score(pl.extract_sections(GOOD)) >= 0.8
    assert pl.answer_first_score(pl.extract_sections(WEAK)) < 0.5


def test_vague_openers_are_counted():
    assert pl.vague_openers(pl.extract_sections(WEAK)) >= 1
    assert pl.vague_openers(pl.extract_sections(GOOD)) == 0


def test_author_and_dates_checked_against_visible_text():
    good = pl.eeat_check(GOOD)
    assert good["author"] == "Jane Doe" and good["author_visible"] is True
    assert good["dates_visible"] is True
    weak = pl.eeat_check(WEAK)
    assert weak["dates_visible"] is False


def test_claims_with_numbers_are_extracted_for_ledger():
    claims = pl.extract_claims(GOOD)
    assert any("38%" in c for c in claims)


def test_lint_returns_findings_list():
    result = pl.lint(WEAK)
    assert result["answer_first_score"] < 0.5
    assert any("answer-first" in f for f in result["findings"])
