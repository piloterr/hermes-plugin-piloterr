# Piloterr for Hermes Agent

Fetch web pages for the built-in web_extract tool through the Piloterr web scraping API, with optional JavaScript rendering or anti-bot unblocking.

## Install

```sh
hermes plugins install piloterr
```

Hermes asks for `PILOTERR_API_KEY` during the install. Create a key in the [Piloterr dashboard](https://app.piloterr.com).

Then select it in `hermes tools`, or in `~/.hermes/config.yaml`:

```yaml
web:
  extract_backend: piloterr
```

It is extract only, so keep a search backend for `web_search`.

## Settings

| Setting | Default | Meaning |
|---|---|---|
| `engine` | `crawler` | `crawler` (plain HTTP, cheapest), `rendering` (headless browser for JavaScript pages) or `webunlocker` (gets past anti-bot protection, most expensive). |

## What it does on your machine

- **Network:** calls `https://api.piloterr.com` only, with your `PILOTERR_API_KEY`. Calls can use credits on your Piloterr account ([pricing](https://www.piloterr.com/pricing)).
- **Credentials:** reads the key only through Hermes's secret scope. It stores nothing.
- **Nothing else:** no files written, no processes started, no telemetry, no self-update. Standard library only, no dependencies.

## Development

```sh
python -m pytest
```

The tests mock the network and run without Hermes installed.

## Contact

- Source: https://github.com/piloterr/hermes-plugin-piloterr
- Piloterr: https://www.piloterr.com
- Issues: https://github.com/piloterr/hermes-plugin-piloterr/issues

## License

MIT
