"""Piloterr for Hermes Agent: a web_extract backend plus tools for 50+ Piloterr endpoints."""


def register(ctx):
    from . import _client
    from .provider import PiloterrWebExtractProvider
    from .schemas import TOOLS
    from .tools import FETCH_PAGE, FETCH_PAGE_SCHEMA, handler

    ctx.register_web_search_provider(PiloterrWebExtractProvider(ctx))

    def available():
        return bool(_client.api_key())

    ctx.register_tool(
        name=FETCH_PAGE, toolset="piloterr", schema=FETCH_PAGE_SCHEMA, handler=handler(FETCH_PAGE), check_fn=available
    )
    for name, (description, parameters, *_rest) in TOOLS.items():
        ctx.register_tool(
            name=name,
            toolset="piloterr",
            schema={"name": name, "description": description, "parameters": parameters},
            handler=handler(name),
            check_fn=available,
        )
