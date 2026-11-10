"""Adapt the Piloterr website API (HTML) to the Hermes web_extract contract."""

from __future__ import annotations

import html.parser
import re

from agent.web_search_provider import WebSearchProvider

from . import _client

ENGINES = ["crawler", "rendering", "webunlocker"]
DEFAULT_ENGINE = "crawler"


def _failed(url, message):
    return {"url": url, "title": "", "content": "", "raw_content": "", "error": f"Piloterr: {message}"}


class _Text(html.parser.HTMLParser):
    """Readable text from an HTML page: drops scripts and styles, keeps line breaks between blocks."""

    SKIP = {"script", "style", "noscript", "svg", "template", "head"}
    BLOCKS = {"p", "div", "br", "li", "tr", "section", "article", "header", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.title, self._skip, self._in_title = [], "", 0, False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        elif tag in self.SKIP:
            self._skip += 1
        elif tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in self.SKIP and self._skip:
            self._skip -= 1
        elif tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            self.parts.append(data)

    def text(self):
        lines = (re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in "".join(self.parts).split("\n"))
        return "\n".join(line for line in lines if line)


def _html(body):
    # The API answers with the page as a JSON string.
    if isinstance(body, str):
        return body
    raise ValueError("response must be the page HTML as a JSON string")


def _document(url, engine, page):
    parser = _Text()
    parser.feed(page)
    parser.close()
    return {
        "url": url,
        "title": parser.title.strip(),
        "content": parser.text(),
        "raw_content": page,
        "metadata": {"source": "piloterr", "engine": engine},
    }


class PiloterrWebExtractProvider(WebSearchProvider):
    """Extract only: fetches each URL and returns its text. Pair it with a search backend for web_search."""

    def __init__(self, ctx):
        self._get_config = ctx.get_config

    @property
    def name(self):
        return "piloterr"

    @property
    def display_name(self):
        return "Piloterr (web scraping)"

    def _engine(self):
        value = self._get_config("engine", DEFAULT_ENGINE)
        engine = value.strip().lower() if isinstance(value, str) else ""
        if engine not in ENGINES:
            raise ValueError("engine must be one of " + ", ".join(ENGINES))
        return engine

    def is_available(self):
        return bool(_client.api_key())

    def supports_search(self):
        return False

    def supports_extract(self):
        return True

    def get_setup_schema(self):
        return {
            "name": self.display_name,
            "badge": "paid",
            "tag": "Fetch pages, with JavaScript rendering or unblocking. Extract only.",
            "env_vars": [{"key": _client.KEY_ENV, "prompt": "Piloterr API key", "url": "https://app.piloterr.com"}],
        }

    def extract(self, urls, **kwargs):
        try:
            engine = self._engine()
        except ValueError as exc:
            return [_failed(str(url), str(exc)) for url in urls or []]
        documents = []
        for url in urls or []:
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                documents.append(_failed(str(url), "the URL must start with http:// or https://"))
                continue
            try:
                page = _html(_client.get("/v2/website/{engine}".format(engine=engine), {"query": url}))
                documents.append(_document(url, engine, page))
            except (ValueError, _client.ApiError) as exc:
                documents.append(_failed(url, str(exc)))
        return documents
