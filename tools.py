"""Tool handlers: each one calls the Piloterr API and returns a JSON string, errors included."""

from __future__ import annotations

import json

from . import _client
from .provider import DEFAULT_ENGINE, ENGINES, _document, _html
from .schemas import TOOLS

FETCH_PAGE = "piloterr_fetch_page"
DEFAULT_MAX_CHARACTERS = 20000
ENGINE_CREDITS = {"crawler": 1, "rendering": 2, "webunlocker": 3}

FETCH_PAGE_SCHEMA = {
    "name": FETCH_PAGE,
    "description": (
        "Fetch a web page through Piloterr and return its readable text (or its HTML). Pick the engine for the site: "
        "crawler is a plain HTTP request (1 credit, fastest; static and server-rendered pages); rendering loads the page "
        "in a headless browser so JavaScript runs (2 credits; single-page apps, lazy content; can wait for a selector); "
        "webunlocker gets past anti-bot protection such as Cloudflare, DataDome, Akamai or PerimeterX (3 credits; "
        "approved domains only). Start with crawler, move to rendering when the text is empty, and to webunlocker when the "
        "page is blocked. piloterr_website_antibot tells you which protection a site uses."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Page URL, starting with http:// or https://."},
            "engine": {
                "type": "string",
                "enum": ENGINES,
                "description": "crawler (default), rendering or webunlocker.",
            },
            "format": {
                "type": "string",
                "enum": ["text", "html"],
                "description": "text (default) returns the page's readable text; html returns the page source.",
            },
            "wait_in_seconds": {
                "type": "number",
                "description": "rendering only: seconds to wait after the page loads, for content that appears late.",
            },
            "wait_for": {
                "type": "string",
                "description": "rendering only: CSS or XPath selector to wait for before returning the page.",
            },
            "block_ads": {"type": "boolean", "description": "rendering only: block ad requests while loading."},
            "max_characters": {
                "type": "integer",
                "description": f"Longest content to return (default {DEFAULT_MAX_CHARACTERS}); the rest is cut off.",
            },
        },
        "required": ["url"],
    },
}


def _arguments(name, args):
    _, schema, path, mapping, fixed, _cost, _group = TOOLS[name]
    params = dict(fixed)
    for arg, value in (args or {}).items():
        if value is None or value == "" or arg not in mapping:
            continue
        params[mapping[arg]] = json.dumps(value, separators=(",", ":")) if isinstance(value, (dict, list)) else value
    for arg in schema.get("required", []):
        if mapping.get(arg) not in params:
            raise ValueError(f"{arg} is required")
    return path, params


def call(name, args):
    try:
        path, params = _arguments(name, args)
        return json.dumps(_client.get(path, params), ensure_ascii=False)
    except (ValueError, KeyError, _client.ApiError) as exc:
        return json.dumps({"error": f"Piloterr: {exc}"})


def fetch_page(args):
    args = args or {}
    url = str(args.get("url") or "").strip()
    engine = str(args.get("engine") or DEFAULT_ENGINE).strip().lower()
    output = str(args.get("format") or "text").strip().lower()
    try:
        if not url.startswith(("http://", "https://")):
            raise ValueError("the URL must start with http:// or https://")
        if engine not in ENGINES:
            raise ValueError("engine must be one of " + ", ".join(ENGINES))
        if output not in ("text", "html"):
            raise ValueError("format must be text or html")
        raw_limit = args.get("max_characters")
        limit = DEFAULT_MAX_CHARACTERS if raw_limit in (None, "") else int(raw_limit)
        if limit < 1:
            raise ValueError("max_characters must be at least 1")
        params = {"query": url}
        if engine == "rendering":
            for key in ("wait_in_seconds", "wait_for", "block_ads"):
                if args.get(key) not in (None, ""):
                    params[key] = args[key]
        page = _html(_client.get(f"/v2/website/{engine}", params))
    except (ValueError, TypeError, _client.ApiError) as exc:
        return json.dumps({"url": url, "engine": engine, "error": f"Piloterr: {exc}"})
    document = _document(url, engine, page)
    content = document["content"] if output == "text" else page
    result = {
        "url": url,
        "engine": engine,
        "credits": ENGINE_CREDITS[engine],
        "title": document["title"],
        "content": content[:limit],
        "truncated": len(content) > limit,
    }
    if output == "text" and not content:
        result["hint"] = (
            "No readable text: the page may need JavaScript (try engine=rendering) or be blocked (try engine=webunlocker)."
        )
    return json.dumps(result, ensure_ascii=False)


def handler(name):
    def run(args, **kwargs):
        return fetch_page(args) if name == FETCH_PAGE else call(name, args)

    run.__name__ = name
    return run
