"""JSON-LD vs visible text parity and risky-type warnings. Usage: python scripts/schema_check.py page.html"""
import json
import sys
from scripts.htmlutil import jsonld_blocks, visible_text

PARITY_KEYS = ("name", "headline", "price", "datePublished", "dateModified", "author.name", "offers.price")
RISKY = {"FAQPage": "FAQ rich results are limited to authoritative sites and FAQ markup does not earn AI citations; keep only if questions are visible on the page",
         "HowTo": "HowTo rich results were deprecated; markup adds maintenance without AI citation benefit",
         "AggregateRating": "ratings must be real, visible and user-generated"}


def load_jsonld(html):
    return jsonld_blocks(html)


def _get(obj, dotted):
    for part in dotted.split("."):
        obj = obj.get(part) if isinstance(obj, dict) else None
    return obj


def _mismatches(block, text):
    out = []
    for key in PARITY_KEYS:
        value = _get(block, key)
        if value is not None and str(value) not in text:
            out.append({"key": key, "value": str(value), "type": block.get("@type")})
    return out


def _warnings(block):
    types = block.get("@type")
    types = types if isinstance(types, list) else [types]
    return [f"{t}: {RISKY[t]}" for t in types if t in RISKY]


def check(html):
    text = visible_text(html)
    blocks = load_jsonld(html)
    mismatches = [m for b in blocks for m in _mismatches(b, text)]
    warnings = [w for b in blocks for w in _warnings(b)]
    return {"blocks": len(blocks), "types": [b.get("@type") for b in blocks], "mismatches": mismatches, "warnings": warnings}


def main(argv):
    print(json.dumps(check(open(argv[0]).read()), indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
