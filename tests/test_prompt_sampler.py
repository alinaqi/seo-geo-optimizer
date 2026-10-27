from scripts import prompt_sampler as ps


def test_build_prompts_covers_required_themes():
    prompts = ps.build_prompts("AI visibility analytics", "Acme Analytics", ["Profound", "Peec AI"])
    themes = {p["theme"] for p in prompts}
    assert {"definition", "best_for", "comparison", "pricing", "brand_facts"} <= themes
    assert len(prompts) >= 12


def test_score_computes_mention_and_citation_rates():
    records = [
        dict(theme="best_for", provider="perplexity", answer="Acme Analytics and Profound are options.", sources=["https://acme.example/pricing"]),
        dict(theme="best_for", provider="perplexity", answer="Profound leads.", sources=["https://profound.example"]),
    ]
    s = ps.score(records, brand="Acme Analytics", domain="acme.example")
    row = s[("best_for", "perplexity")]
    assert row["mention_rate"] == 0.5 and row["citation_rate"] == 0.5 and row["n"] == 2


def test_available_providers_depends_on_env(monkeypatch):
    for k in ps.ENV_KEYS.values():
        monkeypatch.delenv(k, raising=False)
    assert ps.available_providers() == []
    monkeypatch.setenv("PERPLEXITY_API_KEY", "x")
    assert ps.available_providers() == ["perplexity"]
