"""Shared HTML helpers (visible text, JSON-LD, headings)."""
import json
import re
from bs4 import BeautifulSoup

SKIP_TAGS = ("script", "style", "noscript", "template", "svg")


def soup(html):
    return BeautifulSoup(html, "html.parser")


def visible_text(html):
    s = soup(html)
    for t in s(SKIP_TAGS):
        t.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ")).strip()


def jsonld_blocks(html):
    blocks = []
    for tag in soup(html).find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
        except ValueError:
            continue
        blocks.extend(data if isinstance(data, list) else [data])
    return blocks


def word_count(text):
    return len(re.findall(r"\b\w+\b", text))
