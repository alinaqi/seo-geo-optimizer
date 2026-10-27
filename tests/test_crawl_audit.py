from pathlib import Path
from scripts import crawl_audit as ca

ROBOTS = """User-agent: *
Disallow: /private/
User-agent: OAI-SearchBot
Disallow: /
User-agent: GPTBot
Disallow: /
"""


def test_parse_robots_groups_rules_by_agent():
    rules = ca.parse_robots(ROBOTS)
    assert rules["*"] == [("disallow", "/private/")]
    assert rules["oai-searchbot"] == [("disallow", "/")]


def test_is_allowed_uses_specific_group_before_wildcard():
    rules = ca.parse_robots(ROBOTS)
    assert ca.is_allowed(rules, "OAI-SearchBot", "/pricing") is False
    assert ca.is_allowed(rules, "PerplexityBot", "/pricing") is True
    assert ca.is_allowed(rules, "PerplexityBot", "/private/x") is False


def test_robots_matrix_flags_blocked_search_bots():
    rules = ca.parse_robots(ROBOTS)
    matrix = ca.robots_matrix(rules, ["/", "/pricing"])
    assert matrix["OAI-SearchBot"]["/"] is False
    assert matrix["Googlebot"]["/"] is True
    findings = ca.robots_findings(matrix)
    assert any("OAI-SearchBot" in f for f in findings)
    assert not any("GPTBot" in f for f in findings)


def test_ssr_score_distinguishes_shell_from_content():
    good = Path("tests/fixtures/good_page.html").read_text()
    weak = Path("tests/fixtures/weak_page.html").read_text()
    assert ca.ssr_score(good)["words"] > 60
    assert ca.ssr_score(good)["likely_spa_shell"] is False
    assert ca.ssr_score(weak)["likely_spa_shell"] is True


def test_search_bots_are_separated_from_training_bots():
    assert "OAI-SearchBot" in ca.SEARCH_BOTS
    assert "GPTBot" in ca.TRAINING_BOTS
    assert not set(ca.SEARCH_BOTS) & set(ca.TRAINING_BOTS)
