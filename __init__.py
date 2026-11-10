"""Piloterr web extract backend for Hermes Agent."""


def register(ctx):
    from .provider import PiloterrWebExtractProvider

    ctx.register_web_search_provider(PiloterrWebExtractProvider(ctx))
