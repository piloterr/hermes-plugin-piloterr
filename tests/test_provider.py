"""Unit tests for the Piloterr plugin. The network is mocked."""

import io
import json
import urllib.error

import hermes_plugin_piloterr as plugin
import pytest
from hermes_plugin_piloterr import _client


class FakeContext:
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.providers, self.tools = [], {}

    def get_config(self, key, default=None):
        return self.settings.get(key, default)

    def register_web_search_provider(self, provider):
        self.providers.append(provider)

    def register_tool(self, name, toolset, schema, handler, check_fn=None, **kwargs):
        self.tools[name] = {"toolset": toolset, "schema": schema, "handler": handler, "check_fn": check_fn}


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class Calls(list):
    """Records each request and answers it with the payload given to respond()."""

    def __init__(self, monkeypatch):
        super().__init__()
        self.monkeypatch = monkeypatch

    def respond(self, payload):
        def urlopen(request, timeout):
            self.append({"request": request, "timeout": timeout})
            return FakeResponse(json.dumps(payload).encode())

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)

    def fail(self, status, body):
        def urlopen(request, timeout):
            self.append({"request": request, "timeout": timeout})
            raise urllib.error.HTTPError(request.full_url, status, "error", {}, io.BytesIO(json.dumps(body).encode()))

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)

    def unreachable(self):
        def urlopen(request, timeout):
            raise urllib.error.URLError("down")

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)


@pytest.fixture
def calls(monkeypatch):
    return Calls(monkeypatch)


@pytest.fixture
def api_key(monkeypatch):
    monkeypatch.setattr(_client, "get_secret", lambda name, default=None: "test-key" if name == _client.KEY_ENV else default)


@pytest.fixture
def no_key(monkeypatch):
    monkeypatch.setattr(_client, "get_secret", lambda name, default=None: default)


def query(request):
    return dict(_client.urllib.parse.parse_qsl(_client.urllib.parse.urlsplit(request.full_url).query))


def assert_auth(request):
    assert request.get_header("User-agent").startswith("hermes-plugin-piloterr/")
    assert request.get_header("X-api-key") == "test-key"


def provider(settings=None):
    ctx = FakeContext(settings)
    plugin.register(ctx)
    return ctx.providers[0]


PAGE = (
    "<!doctype html><html><head><title>Example Domain</title><style>body{color:red}</style></head>"
    "<body><h1>Example Domain</h1><p>This domain is for   examples.</p><script>track()</script>"
    "<ul><li>One</li><li>Two &amp; three</li></ul></body></html>"
)


def test_register_adds_an_extract_only_provider():
    p = provider()
    assert p.name == "piloterr"
    assert p.supports_search() is False
    assert p.supports_extract() is True


def test_not_available_without_key(no_key, calls):
    assert provider().is_available() is False
    [doc] = provider().extract(["https://example.com"])
    assert "PILOTERR_API_KEY" in doc["error"]
    assert calls == []


def test_default_engine(api_key, calls):
    calls.respond(PAGE)
    provider().extract(["https://example.com"])
    request = calls[0]["request"]
    assert request.full_url == "https://api.piloterr.com/v2/website/crawler?query=https%3A%2F%2Fexample.com"
    assert_auth(request)


def test_engine_setting(api_key, calls):
    calls.respond(PAGE)
    provider({"engine": "Rendering"}).extract(["https://example.com"])
    assert "/website/rendering?" in calls[0]["request"].full_url


def test_invalid_engine_fails_without_a_request(api_key, calls):
    [doc] = provider({"engine": "fast"}).extract(["https://example.com"])
    assert "engine" in doc["error"]
    assert calls == []


def test_extract_returns_readable_text(api_key, calls):
    calls.respond(PAGE)
    [doc] = provider().extract(["https://example.com"])
    assert doc["title"] == "Example Domain"
    assert doc["content"] == "Example Domain\nThis domain is for examples.\nOne\nTwo & three"
    assert doc["raw_content"] == PAGE
    assert doc["metadata"] == {"source": "piloterr", "engine": "crawler"}


def test_one_document_per_url_and_per_url_errors(api_key, calls):
    calls.respond(PAGE)
    docs = provider().extract(["https://example.com", "example.com"])
    assert "error" not in docs[0] and "http" in docs[1]["error"]
    assert len(calls) == 1


def test_api_error_message_is_returned(api_key, calls):
    calls.fail(402, {"error": "Not enough credits"})
    [doc] = provider().extract(["https://example.com"])
    assert doc["error"] == "Piloterr: Not enough credits"


def test_network_error(api_key, calls):
    calls.unreachable()
    [doc] = provider().extract(["https://example.com"])
    assert doc["error"] == "Piloterr: could not reach the API"


def test_unexpected_response(api_key, calls):
    calls.respond({"html": "<p>hi</p>"})
    [doc] = provider().extract(["https://example.com"])
    assert "HTML" in doc["error"]


# Tools


def tools(settings=None):
    ctx = FakeContext(settings)
    plugin.register(ctx)
    return ctx.tools


def run(name, args):
    return json.loads(tools()[name]["handler"](args))


def test_register_adds_the_fetch_tool_and_every_endpoint_tool():
    registered = tools()
    from hermes_plugin_piloterr.schemas import TOOLS

    assert set(registered) == {"piloterr_fetch_page", *TOOLS}
    assert {t["toolset"] for t in registered.values()} == {"piloterr"}
    for name, tool in registered.items():
        assert tool["schema"]["name"] == name
        assert tool["schema"]["parameters"]["type"] == "object"


def test_manifest_lists_every_tool():
    from pathlib import Path

    manifest = (Path(__file__).resolve().parents[1] / "plugin.yaml").read_text()
    listed = {line.strip()[2:] for line in manifest.splitlines() if line.strip().startswith("- piloterr_")}
    assert listed == set(tools())


def test_tools_hidden_without_key(no_key):
    assert all(tool["check_fn"]() is False for tool in tools().values())


def test_fetch_page_defaults_to_crawler_text(api_key, calls):
    calls.respond(PAGE)
    result = run("piloterr_fetch_page", {"url": "https://example.com"})
    request = calls[0]["request"]
    assert request.full_url.startswith("https://api.piloterr.com/v2/website/crawler?")
    assert query(request) == {"query": "https://example.com"}
    assert request.get_header("X-api-key") == "test-key"
    assert result["engine"] == "crawler" and result["credits"] == 1
    assert result["title"] == "Example Domain"
    assert "This domain is for examples." in result["content"]
    assert "track()" not in result["content"]
    assert result["truncated"] is False


def test_fetch_page_rendering_sends_wait_options(api_key, calls):
    calls.respond(PAGE)
    result = run(
        "piloterr_fetch_page",
        {"url": "https://example.com", "engine": "rendering", "wait_in_seconds": 3, "wait_for": "#app", "block_ads": True},
    )
    request = calls[0]["request"]
    assert "/v2/website/rendering?" in request.full_url
    assert query(request) == {"query": "https://example.com", "wait_in_seconds": "3", "wait_for": "#app", "block_ads": "True"}
    assert result["credits"] == 2


def test_fetch_page_webunlocker_ignores_rendering_options(api_key, calls):
    calls.respond(PAGE)
    result = run("piloterr_fetch_page", {"url": "https://example.com", "engine": "webunlocker", "wait_for": "#app"})
    assert "/v2/website/webunlocker?" in calls[0]["request"].full_url
    assert query(calls[0]["request"]) == {"query": "https://example.com"}
    assert result["credits"] == 3


def test_fetch_page_html_and_truncation(api_key, calls):
    calls.respond(PAGE)
    result = run("piloterr_fetch_page", {"url": "https://example.com", "format": "html", "max_characters": 20})
    assert result["content"] == PAGE[:20]
    assert result["truncated"] is True


def test_fetch_page_empty_text_suggests_another_engine(api_key, calls):
    calls.respond("<html><head><title>App</title></head><body><div id='root'></div><script>boot()</script></body></html>")
    result = run("piloterr_fetch_page", {"url": "https://example.com"})
    assert result["content"] == ""
    assert "rendering" in result["hint"]


@pytest.mark.parametrize(
    "args, message",
    [
        ({"url": "example.com"}, "http://"),
        ({"url": "https://example.com", "engine": "chrome"}, "engine must be one of"),
        ({"url": "https://example.com", "format": "pdf"}, "format must be"),
        ({"url": "https://example.com", "max_characters": 0}, "max_characters"),
    ],
)
def test_fetch_page_rejects_bad_arguments_without_a_request(api_key, calls, args, message):
    calls.respond(PAGE)
    result = run("piloterr_fetch_page", args)
    assert message in result["error"]
    assert calls == []


def test_fetch_page_api_error(api_key, calls):
    calls.fail(403, {"error": "Domain not allowed for webunlocker"})
    result = run("piloterr_fetch_page", {"url": "https://example.com", "engine": "webunlocker"})
    assert result["error"] == "Piloterr: Domain not allowed for webunlocker"


def test_endpoint_tool_sends_arguments(api_key, calls):
    calls.respond({"name": "Piloterr", "staff_count": 12})
    result = run("piloterr_linkedin_company", {"query": "piloterr", "domain": ""})
    request = calls[0]["request"]
    assert request.full_url.startswith("https://api.piloterr.com/v2/linkedin/company/info?")
    assert query(request) == {"query": "piloterr"}
    assert result == {"name": "Piloterr", "staff_count": 12}


def test_endpoint_tool_requires_its_inputs(api_key, calls):
    result = run("piloterr_amazon_product", {"domain": "fr"})
    assert result == {"error": "Piloterr: query is required"}
    assert calls == []


def test_endpoint_tool_api_error(api_key, calls):
    calls.fail(402, {"error": {"message": "Not enough credits"}})
    assert run("piloterr_google_search", {"query": "web scraping"}) == {"error": "Piloterr: Not enough credits"}


def test_endpoint_tool_without_key(no_key, calls):
    result = run("piloterr_google_search", {"query": "web scraping"})
    assert "PILOTERR_API_KEY" in result["error"]
    assert calls == []
