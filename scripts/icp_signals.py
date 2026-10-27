"""Extract ideal-customer-profile signals (roles, industries, size, pricing model, proof, review platforms)
from a page with evidence quotes. Usage: python scripts/icp_signals.py page.html"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # allow `python scripts/x.py`
import json
import re
from scripts.htmlutil import soup, visible_text

ROLES = {"HR": r"\bHR\b|human resources|people team|HR-Leiter|People", "L&D": r"L&amp;D|L&D|learning and development",
         "Sales": r"\bsales\b|revenue team|Head of Sales", "Marketing": r"\bmarketing\b|CMO", "IT": r"\bIT\b|CIO|IT teams",
         "Engineering": r"developers?|engineering|CTO", "Operations": r"operations|COO", "Finance": r"\bCFO\b|finance team",
         "Founders": r"founders?|CEO", "Support": r"customer support|support team"}
INDUSTRIES = {"healthcare": r"healthcare|hospital|clinic|pharma", "financial services": r"financial services|bank|fintech|insurance",
              "manufacturing": r"manufactur", "retail": r"retail|ecommerce|e-commerce", "saas": r"\bSaaS\b|software companies",
              "education": r"universit|school|higher education", "public sector": r"public sector|government", "legal": r"law firm|legal"}
SIZE = [("enterprise", r"enterprise|Fortune 500|10[,.]?000\+? employees|global organi[sz]ations"),
        ("mid-market", r"mid-?sized|mittelst|\b(200|250|500) (bis|to|-) ?(1[,.]?000|2[,.]?000)\b|mid-market"),
        ("smb", r"small business|SMB|startups?|teams of \d{1,2}\b|freelancers")]
REVIEW_SITES = {"G2": "g2.com", "Capterra": "capterra", "OMR Reviews": "omr.com/reviews", "Trustpilot": "trustpilot", "TrustRadius": "trustradius",
                "GetApp": "getapp", "Yelp": "yelp.com", "Product Hunt": "producthunt", "ITreview": "itreview", "Reclame Aqui": "reclameaqui"}
PRICE = re.compile(r"(from|ab|starting at|starts at)\s*(€|\$|£|CHF\s?)\s?(\d[\d.,]*)", re.I)
PER_SEAT = re.compile(r"per (seat|user|employee)|pro (Nutzer|Mitarbeiter)|/seat|/user", re.I)


def _hits(table, text):
    out, evidence = [], {}
    for name, pattern in table.items():
        m = re.search(pattern, text, re.I)
        if m:
            out.append(name)
            evidence[name] = text[max(0, m.start() - 60): m.end() + 60].strip()
    return out, evidence


def _size(text):
    best = {"band": "UNKNOWN", "evidence": [], "hits": 0}
    for band, pattern in SIZE:
        matches = list(re.finditer(pattern, text, re.I))
        if len(matches) > best["hits"]:
            ev = [text[max(0, m.start() - 60): m.end() + 60].strip() for m in matches[:2]]
            best = {"band": band, "evidence": ev, "hits": len(matches)}
    return {"band": best["band"], "evidence": best["evidence"]}


def _pricing(text):
    m = PRICE.search(text)
    if m:
        return {"model": "from-price", "from": f"{m.group(2).strip()}{m.group(3)}", "per_seat": bool(PER_SEAT.search(text)), "evidence": m.group(0)}
    if PER_SEAT.search(text):
        return {"model": "per-seat", "from": None, "per_seat": True, "evidence": PER_SEAT.search(text).group(0)}
    return {"model": "UNKNOWN", "from": None, "per_seat": False, "evidence": ""}


def _review_platforms(html):
    hrefs = " ".join(a.get("href", "") for a in soup(html).find_all("a"))
    return [name for name, needle in REVIEW_SITES.items() if needle in hrefs]


def _proof(text):
    quotes = re.findall(r"[\"“]([^\"”]{20,240})[\"”]", text)
    stats = [s.strip() for s in re.findall(r"[^.]*\b\d{2,}[^.]*(?:customers|organi[sz]ations|reps|users|companies|teams)[^.]*\.", text, re.I)]
    return quotes + stats


def extract(html):
    text = visible_text(html) + " " + " ".join(a.get_text(" ") for a in soup(html).find_all("a"))
    roles, role_ev = _hits(ROLES, text)
    industries, ind_ev = _hits(INDUSTRIES, text)
    return {"roles": roles, "industries": industries, "company_size": _size(text), "pricing": _pricing(text),
            "review_platforms": _review_platforms(html), "proof_quotes": _proof(text),
            "evidence": {**role_ev, **ind_ev}}


def icp_sheet(signals):
    roles = signals["roles"] or ["UNKNOWN"]
    inds = signals["industries"] or ["cross-industry"]
    size = signals["company_size"]["band"]
    conf = "medium" if signals["roles"] and size != "UNKNOWN" else "low"
    return [{"segment": f"{r} in {i}", "roles": [r], "industries": [i], "size": size,
             "evidence": [signals["evidence"].get(r, ""), signals["evidence"].get(i, "")] + signals["company_size"]["evidence"],
             "confidence": conf} for r in roles for i in inds][:12]


def main(argv):
    s = extract(open(argv[0]).read())
    print(json.dumps({**s, "icp_sheet": icp_sheet(s)}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
