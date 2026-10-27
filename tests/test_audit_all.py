from scripts import audit_all as aa, crawl_audit as ca


def test_audit_all_writes_report(monkeypatch, tmp_path):
    html = open("tests/fixtures/good_page.html").read()
    monkeypatch.setattr(ca, "fetch", lambda url, ua="Browser", timeout=15: (200, "User-agent: *\nDisallow:\n" if url.endswith("robots.txt") else html))
    aa.main(["https://acme.example", "--paths", "/", "--outdir", str(tmp_path / "a")])
    report = (tmp_path / "a" / "report.md").read_text()
    assert "## Access matrix" in report and (tmp_path / "a" / "lint.json").exists()
