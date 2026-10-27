"""Network paths exercised with monkeypatched HTTP so no real requests are made."""
import json
from scripts import crawl_audit as ca, prompt_sampler as ps, providers as pv, report as rp, page_lint as pl, schema_check as sc


class FakeResp:
    def __init__(self, status=200, text="", payload=None):
        self.status_code, self.text, self._payload = status, text, payload or {}

    def json(self):
        return self._payload


def test_fetch_and_audit_with_mocked_http(monkeypatch):
    html = "<html><body>" + "word " * 200 + "</body></html>"
    monkeypatch.setattr(ca.requests, "get", lambda url, **kw: FakeResp(200, "User-agent: *\nDisallow: /x\n" if url.endswith("robots.txt") else html))
    result = ca.audit("https://acme.example", ["/", "/x"])
    assert result["robots"]["OAI-SearchBot"]["/x"] is False
    assert result["pages"]["/"]["status"] == 200 and result["pages"]["/"]["likely_spa_shell"] is False


def test_fetch_handles_connection_errors(monkeypatch):
    def boom(*a, **k):
        raise ca.requests.RequestException("down")
    monkeypatch.setattr(ca.requests, "get", boom)
    assert ca.fetch("https://acme.example")[0] == 0


def test_crawl_main_writes_json(monkeypatch, tmp_path):
    monkeypatch.setattr(ca, "audit", lambda base, paths: {"url": base, "paths": paths})
    out = tmp_path / "a.json"
    ca.main(["https://acme.example", "--paths", "/", "--out", str(out)])
    assert json.load(open(out))["url"] == "https://acme.example"


def test_sample_uses_clients_and_scores(monkeypatch):
    monkeypatch.setitem(pv.CLIENTS, "perplexity", lambda prompt: ("Acme Analytics is great", ["https://acme.example/a"]))
    recs = ps.sample([{"theme": "best_for", "prompt": "x"}], ["perplexity"], runs=2)
    assert len(recs) == 2 and recs[0]["sources"] == ["https://acme.example/a"]
    s = ps.score(recs, "Acme Analytics", "acme.example")
    assert s[("best_for", "perplexity")]["citation_rate"] == 1.0


def test_sampler_main_runs_end_to_end(monkeypatch, tmp_path):
    monkeypatch.setenv("PERPLEXITY_API_KEY", "x")
    monkeypatch.setitem(pv.CLIENTS, "perplexity", lambda prompt: ("answer", []))
    out = tmp_path / "b.json"
    ps.main(["--category", "c", "--brand", "Acme", "--domain", "acme.example", "--out", str(out)])
    assert "providers" in json.load(open(out))


def test_provider_parsers(monkeypatch):
    monkeypatch.setenv("PERPLEXITY_API_KEY", "k"); monkeypatch.setenv("OPENAI_API_KEY", "k")
    monkeypatch.setenv("GEMINI_API_KEY", "k"); monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    payloads = {
        "perplexity.ai": {"choices": [{"message": {"content": "p"}}], "search_results": [{"url": "u1"}]},
        "openai.com": {"output": [{"content": [{"text": "o", "annotations": [{"url": "u2"}]}]}]},
        "googleapis.com": {"candidates": [{"content": {"parts": [{"text": "g"}]}, "groundingMetadata": {"groundingChunks": [{"web": {"uri": "u3"}}]}}]},
        "anthropic.com": {"content": [{"text": "a", "citations": [{"url": "u4"}]}]},
    }
    monkeypatch.setattr(pv.requests, "post", lambda url, **kw: FakeResp(payload=next(v for k, v in payloads.items() if k in url)))
    assert pv.perplexity("q") == ("p", ["u1"]) and pv.openai("q") == ("o", ["u2"])
    assert pv.gemini("q") == ("g", ["u3"]) and pv.anthropic("q") == ("a", ["u4"])


def test_report_main_and_baseline(tmp_path):
    audit = {"url": "u", "robots": {"Googlebot": {"/": True}}, "robots_findings": [], "pages": {}}
    baseline = {"scores": {"best_for|perplexity": {"n": 2, "mention_rate": 0.5, "citation_rate": 0.0}}}
    paths = {}
    for name, data in {"audit": audit, "lint": {}, "schema": {}, "baseline": baseline}.items():
        paths[name] = tmp_path / f"{name}.json"; json.dump(data, open(paths[name], "w"))
    out = tmp_path / "r.md"
    rp.main(["--audit", str(paths["audit"]), "--lint", str(paths["lint"]), "--schema", str(paths["schema"]), "--baseline", str(paths["baseline"]), "--out", str(out)])
    assert "| best_for | perplexity | 2 | 50% | 0% |" in out.read_text()


def test_lint_and_schema_cli(capsys, tmp_path):
    f = tmp_path / "p.html"; f.write_text(open("tests/fixtures/good_page.html").read())
    pl.main([str(f)]); sc.main([str(f)])
    assert "answer_first_score" in capsys.readouterr().out
