"""Detect markets, languages and localisation patterns from a page. Usage: python scripts/market_detect.py page.html --url https://site"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # allow `python scripts/x.py`
import argparse
import json
import re
from collections import Counter
from urllib.parse import urlparse
from scripts.htmlutil import soup, visible_text
from scripts.markets_data import MARKETS, LANG_HINTS

CURRENCY = {"€": "EUR", "$": "USD", "£": "GBP", "¥": "JPY", "₹": "INR", "CHF": "CHF", "R$": "BRL", "₩": "KRW"}
SWAP_ATTRS = ("data-en", "data-de", "data-fr", "data-es", "data-lang", "data-i18n")


def detect_text_language(text):
    words = Counter(w.lower() for w in re.findall(r"\b\w+\b", text))
    scores = {lang: sum(words[w] for w in hints) for lang, hints in LANG_HINTS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "UNKNOWN"


def _hreflang(s):
    return sorted({(l.get("hreflang") or "").split("-")[0] for l in s.find_all("link", rel="alternate") if l.get("hreflang")})


def _js_swap(s):
    for attr in SWAP_ATTRS:
        n = len(s.find_all(attrs={attr: True}))
        if n:
            return {"pattern": attr, "count": n}
    return {"pattern": None, "count": 0}


def _currencies(text):
    return sorted({code for sym, code in CURRENCY.items() if sym in text})


def _geographies(text):
    found = []
    for m in MARKETS.values():
        found += [c for c in m["countries"] if re.search(rf"\b{re.escape(c)}\b", text)]
    return sorted(set(found))


def _findings(r):
    out = []
    lang = (r["html_lang"] or "").split("-")[0]
    if lang and r["detected_text_language"] not in ("UNKNOWN", lang):
        out.append(f"html lang='{r['html_lang']}' but visible text reads as '{r['detected_text_language']}'; engines classify the page by the wrong language")
    if r["js_language_swap"]["count"]:
        out.append(f"{r['js_language_swap']['count']} elements hold a second language in {r['js_language_swap']['pattern']} attributes; AI crawlers only read the rendered default language, so serve each language at its own URL")
    if not r["hreflang"] and r["js_language_swap"]["count"]:
        out.append("no hreflang alternates; add per-language URLs with hreflang pairs")
    return out


def detect(html, url=""):
    s, text = soup(html), visible_text(html)
    r = {"url": url, "tld": urlparse(url).hostname.rsplit(".", 1)[-1] if url else None,
         "html_lang": (s.html.get("lang") if s.html else None), "hreflang": _hreflang(s),
         "js_language_swap": _js_swap(s), "detected_text_language": detect_text_language(text),
         "currencies": _currencies(text), "geographies": _geographies(text)}
    r["findings"] = _findings(r)
    return r


def _matches(name, m, r):
    geo = bool(set(r["geographies"]) & m["countries"])
    tld = r["tld"] in m["tlds"]
    lang = bool(({r["detected_text_language"]} | set(r["hreflang"])) & m["languages"])
    return geo or tld or (lang and name not in ("US", "UK", "India"))


def market_profile(r):
    out = [{"market": n, "engines": m["engines"], "review_platforms": m["review_platforms"], "languages": sorted(m["languages"]), "notes": m["notes"]}
           for n, m in MARKETS.items() if _matches(n, m, r)]
    return out or [{"market": "UNKNOWN", "engines": MARKETS["US"]["engines"], "review_platforms": MARKETS["US"]["review_platforms"], "languages": ["en"], "notes": "No geography, TLD or language signal; confirm target markets with the owner."}]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--url", default="")
    a = ap.parse_args(argv)
    r = detect(open(a.page).read(), a.url)
    print(json.dumps({**r, "markets": market_profile(r)}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
