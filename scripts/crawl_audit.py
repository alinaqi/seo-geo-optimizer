"""Access audit: robots.txt per bot, HTTP status by user agent, server-rendered text check.
Usage: python scripts/crawl_audit.py https://example.com --paths / /pricing --out audit.json"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # allow `python scripts/x.py`
import argparse
import json
from urllib.parse import urljoin
import requests
from scripts.htmlutil import visible_text, word_count, soup

SEARCH_BOTS = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User"]
TRAINING_BOTS = ["GPTBot", "ClaudeBot", "Google-Extended", "CCBot"]
UA_STRINGS = {"Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
              "OAI-SearchBot": "Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)",
              "PerplexityBot": "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
              "Claude-SearchBot": "Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +https://www.anthropic.com)",
              "Browser": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/130 Safari/537.36"}


def _robots_lines(text):
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if ":" in line:
            key, value = [p.strip() for p in line.split(":", 1)]
            yield key.lower(), value


def parse_robots(text):
    rules, agents, in_rules = {}, [], False
    for key, value in _robots_lines(text):
        if key == "user-agent":
            agents = [] if in_rules else agents
            agents.append(value.lower())
            rules.setdefault(value.lower(), [])
            in_rules = False
        elif key in ("allow", "disallow") and agents and value:
            in_rules = True
            for a in agents:
                rules[a].append((key, value))
    return rules


def _group_for(rules, ua):
    ua = ua.lower()
    return rules.get(ua) if ua in rules else rules.get("*", [])


def is_allowed(rules, ua, path):
    best = ("allow", "")
    for kind, pattern in _group_for(rules, ua) or []:
        if path.startswith(pattern.rstrip("*")) and len(pattern) >= len(best[1]):
            best = (kind, pattern)
    return best[0] == "allow"


def robots_matrix(rules, paths):
    return {bot: {p: is_allowed(rules, bot, p) for p in paths} for bot in SEARCH_BOTS + TRAINING_BOTS}


def robots_findings(matrix):
    out = []
    for bot in SEARCH_BOTS:
        blocked = [p for p, ok in matrix[bot].items() if not ok]
        if blocked:
            out.append(f"{bot} blocked on {', '.join(blocked)} (search/retrieval bot: citations impossible)")
    return out


def ssr_score(html):
    words = word_count(visible_text(html))
    scripts = len(soup(html).find_all("script", src=True))
    return {"words": words, "script_tags": scripts, "likely_spa_shell": words < 100 and scripts > 0}


def fetch(url, ua="Browser", timeout=15):
    try:
        r = requests.get(url, headers={"User-Agent": UA_STRINGS.get(ua, ua)}, timeout=timeout, allow_redirects=True)
        return r.status_code, r.text
    except requests.RequestException as exc:
        return 0, str(exc)


def audit_page(base, path):
    url = urljoin(base, path)
    statuses = {ua: fetch(url, ua)[0] for ua in UA_STRINGS}
    status, html = fetch(url)
    return {"url": url, "status": status, "status_by_ua": statuses, **ssr_score(html if status else "")}


def audit(base, paths):
    status, robots_txt = fetch(urljoin(base, "/robots.txt"))
    rules = parse_robots(robots_txt if status == 200 else "")
    matrix = robots_matrix(rules, paths)
    pages = {p: audit_page(base, p) for p in paths}
    return {"url": base, "robots_status": status, "robots": matrix, "robots_findings": robots_findings(matrix), "pages": pages}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--paths", nargs="+", default=["/"])
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    result = audit(a.url, a.paths)
    text = json.dumps(result, indent=2)
    (open(a.out, "w").write(text) if a.out else print(text))


if __name__ == "__main__":
    main(sys.argv[1:])
