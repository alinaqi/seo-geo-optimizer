"""Page lint: answer-first structure, vague openers, E-E-A-T fields, claim extraction.
Usage: python scripts/page_lint.py page.html  (or a URL)"""
import json
import re
import sys
from scripts.htmlutil import soup, visible_text, word_count, jsonld_blocks

VAGUE = re.compile(r"^(it|this|they|these|those|in this (article|post|guide)|welcome|today)\b", re.I)
DATE = re.compile(r"\b(20\d{2}-\d{2}-\d{2}|\d{1,2} \w+ 20\d{2}|\w+ \d{1,2}, 20\d{2})\b")
CLAIM = re.compile(r"[^.!?]*\d[^.!?]*[.!?]")


def extract_sections(html):
    sections, current = [], None
    for el in soup(html).find_all(["h1", "h2", "h3", "p", "li", "td"]):
        text = re.sub(r"\s+", " ", el.get_text(" ")).strip()
        if el.name in ("h2", "h3"):
            current = {"heading": text, "text": "", "words": 0}
            sections.append(current)
        elif current is not None and text:
            current["text"] = (current["text"] + " " + text).strip()
            current["words"] = word_count(current["text"])
    return sections


def _answer_first(section):
    first = " ".join(section["text"].split()[:60])
    has_sentence = bool(re.search(r"[.!?]", first)) and section["words"] >= 25
    return has_sentence and not VAGUE.match(section["text"]) and section["words"] <= 350


def answer_first_score(sections):
    if not sections:
        return 0.0
    return round(sum(_answer_first(s) for s in sections) / len(sections), 2)


def vague_openers(sections):
    return sum(bool(VAGUE.match(s["text"])) for s in sections)


def _schema_author(html):
    for b in jsonld_blocks(html):
        author = b.get("author") or {}
        if isinstance(author, dict) and author.get("name"):
            return author["name"]
    return None


def eeat_check(html):
    text = visible_text(html)
    meta = soup(html).find("meta", attrs={"name": "author"})
    author = (meta.get("content") if meta else None) or _schema_author(html)
    return {"author": author, "author_visible": bool(author and author in text),
            "dates_visible": bool(DATE.search(text)), "has_schema_dates": any("datePublished" in b for b in jsonld_blocks(html))}


def extract_claims(html):
    return [c.strip() for c in CLAIM.findall(visible_text(html)) if "%" in c or re.search(r"\b\d{2,}\b", c)]


def _findings(score, vague, eeat):
    out = []
    if score < 0.8:
        out.append(f"answer-first score {score:.2f} below 0.8: open each section with a direct 40-60 word answer")
    if vague:
        out.append(f"{vague} section(s) open with a vague reference (it/this/in this article); name the entity")
    if not eeat["author_visible"]:
        out.append("no visible real author; add byline, bio and matching schema author")
    if not eeat["dates_visible"]:
        out.append("no visible published/updated date; show dates that match schema")
    return out


def lint(html):
    sections = extract_sections(html)
    score, vague, eeat = answer_first_score(sections), vague_openers(sections), eeat_check(html)
    return {"sections": len(sections), "answer_first_score": score, "vague_openers": vague, "eeat": eeat,
            "claims": extract_claims(html), "findings": _findings(score, vague, eeat)}


def main(argv):
    src = argv[0]
    html = open(src).read() if not src.startswith("http") else __import__("requests").get(src, timeout=15).text
    print(json.dumps(lint(html), indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
