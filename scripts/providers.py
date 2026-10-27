"""Thin API clients for AI answer sampling. Keys come from environment variables only."""
import os
import requests

TIMEOUT = 120


def perplexity(prompt):
    r = requests.post("https://api.perplexity.ai/chat/completions", timeout=TIMEOUT,
                      headers={"Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}"},
                      json={"model": "sonar", "messages": [{"role": "user", "content": prompt}]})
    d = r.json()
    sources = [s.get("url") for s in d.get("search_results", [])] or d.get("citations", [])
    return d["choices"][0]["message"]["content"], sources


def openai(prompt):
    r = requests.post("https://api.openai.com/v1/responses", timeout=TIMEOUT,
                      headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
                      json={"model": os.environ.get("OPENAI_MODEL", "gpt-5"), "tools": [{"type": "web_search"}], "input": prompt})
    d = r.json()
    text, sources = "", []
    for item in d.get("output", []):
        for part in item.get("content", []) or []:
            text += part.get("text", "")
            sources += [a.get("url") for a in part.get("annotations", []) if a.get("url")]
    return text, sources


def gemini(prompt):
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={os.environ['GEMINI_API_KEY']}"
    r = requests.post(url, timeout=TIMEOUT, json={"contents": [{"parts": [{"text": prompt}]}], "tools": [{"google_search": {}}]})
    cand = r.json()["candidates"][0]
    text = "".join(p.get("text", "") for p in cand["content"]["parts"])
    chunks = cand.get("groundingMetadata", {}).get("groundingChunks", [])
    return text, [c.get("web", {}).get("uri") for c in chunks]


def anthropic(prompt):
    r = requests.post("https://api.anthropic.com/v1/messages", timeout=TIMEOUT,
                      headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
                      json={"model": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5"), "max_tokens": 1500,
                            "tools": [{"type": "web_search_20250305", "name": "web_search"}],
                            "messages": [{"role": "user", "content": prompt}]})
    text, sources = "", []
    for block in r.json().get("content", []):
        text += block.get("text", "")
        sources += [c.get("url") for c in block.get("citations", []) or [] if c.get("url")]
    return text, sources


CLIENTS = {"perplexity": perplexity, "openai": openai, "gemini": gemini, "anthropic": anthropic}
