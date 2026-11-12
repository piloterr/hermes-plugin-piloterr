# Piloterr for Hermes Agent

Web scraping for [Hermes Agent](https://hermes-agent.nousresearch.com), through the [Piloterr](https://www.piloterr.com) API.

- **Fetch any page** with one of three engines: a plain HTTP crawler, a headless browser that runs JavaScript, or a web unlocker that gets past anti-bot protection.
- **Get structured JSON from the sites people ask about most:** Google, Bing, Brave, DuckDuckGo, Yahoo, LinkedIn, Instagram, X, Amazon, eBay, Walmart, AliExpress, Target, Best Buy, Crunchbase, Trustpilot, G2, Similarweb, Indeed, Glassdoor, Yelp, Expedia and Zillow. 54 tools in all.
- **Back the built-in `web_extract` tool**, so every page Hermes reads goes through Piloterr.

## Contents

- [Install](#install)
- [How it works](#how-it-works)
- [Fetch any page: crawler, rendering, webunlocker](#fetch-any-page-crawler-rendering-webunlocker)
- [Structured data tools](#structured-data-tools)
- [Use it as the web_extract backend](#use-it-as-the-web_extract-backend)
- [Example prompts](#example-prompts)
- [Credits and errors](#credits-and-errors)
- [What it does on your machine](#what-it-does-on-your-machine)

## Install

```sh
hermes plugins install piloterr
```

Hermes asks for `PILOTERR_API_KEY` during the install. Create a key in the [Piloterr dashboard](https://app.piloterr.com).

Answer yes to `Enable 'piloterr' now?`, or run `hermes plugins enable piloterr` later. The tools join the `piloterr` toolset, which is on by default; turn it on or off in `hermes tools` like any other toolset. They stay hidden from the model until the API key is set.

## How it works

Every tool is one HTTPS call to `https://api.piloterr.com`, authenticated with your key. Piloterr loads the target page from its own infrastructure, parses it and sends back JSON. Hermes passes that JSON to the model as the tool result.

```
Hermes  ──tool call──▶  plugin  ──GET /v2/...──▶  api.piloterr.com  ──▶  target site
        ◀──JSON──────          ◀──JSON──────────                   ◀──page──
```

There are two kinds of tools:

| Kind | Tools | Use it when |
|---|---|---|
| **Page fetcher** | `piloterr_fetch_page` | You need the text or HTML of any URL. |
| **Site tools** | `piloterr_google_search`, `piloterr_linkedin_profile`, `piloterr_amazon_product`… | The site has a dedicated tool: you get clean fields (price, rating, followers…) instead of raw page text, and fewer tokens. |

## Fetch any page: crawler, rendering, webunlocker

`piloterr_fetch_page` takes a URL and returns the page's readable text (scripts, styles and markup removed) or its HTML. The `engine` argument picks how Piloterr loads the page.

| Engine | How it loads the page | Good for | Credits |
|---|---|---|---|
| `crawler` (default) | Plain HTTP request, no JavaScript. Fastest. | Static and server-rendered pages: blogs, docs, news articles, most company sites. | 1 |
| `rendering` | Opens the page in a headless browser, so JavaScript runs before the HTML is captured. | Single-page apps (React, Vue, Angular), content loaded after the first paint, infinite scroll, pages that are empty without JavaScript. | 2 |
| `webunlocker` | Browser rendering combined with Piloterr's unblocking tooling. | Sites behind Cloudflare, DataDome, Akamai, PerimeterX and similar protections that block the other two engines. Works on the domains on Piloterr's approved list; ask Piloterr support to add one. | 3 |

### Which engine to pick

1. Start with `crawler`. It is the cheapest and works for most pages.
2. If the text comes back empty or only shows a loading screen, the page needs JavaScript: retry with `rendering`. The tool adds a `hint` to empty results to say so.
3. If you get a block page, a captcha or an access-denied error, retry with `webunlocker`.
4. Not sure? Call `piloterr_website_antibot` first. It names the protection the site uses (vendor, confidence and the clues found) for 1 credit, so you can go straight to the right engine.

The model reads this order from the tool description and follows it on its own.

### Arguments

| Argument | Type | Default | Meaning |
|---|---|---|---|
| `url` | string | required | Page URL, starting with `http://` or `https://`. |
| `engine` | string | `crawler` | `crawler`, `rendering` or `webunlocker`. |
| `format` | string | `text` | `text` for the readable text, `html` for the page source. |
| `wait_in_seconds` | number | | `rendering` only: extra seconds to wait after the page loads, for content that arrives late. |
| `wait_for` | string | | `rendering` only: a CSS or XPath selector to wait for, such as `.price` or `#reviews`. |
| `block_ads` | boolean | | `rendering` only: block ad requests, which makes heavy pages load faster. |
| `max_characters` | integer | `20000` | Longest content returned; the rest is cut off so a large page does not fill the context window. |

The wait options are ignored by `crawler` and `webunlocker`.

### Result

```json
{
  "url": "https://example.com",
  "engine": "rendering",
  "credits": 2,
  "title": "Example Domain",
  "content": "Example Domain\nThis domain is for use in documentation examples…",
  "truncated": false
}
```

`truncated` is `true` when the page was longer than `max_characters`. When a text result is empty, a `hint` field suggests the next engine to try.

## Structured data tools

Each tool calls one Piloterr endpoint and returns its JSON as is. Search tools take a `query`; page tools take a URL, an ID or a username in `query`. Optional arguments (country, language, page, marketplace…) are in each tool's schema, so the model sees them too. Credits are per call.

### Websites

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `piloterr_website_antibot` | Detect which anti-bot protection a website uses (Cloudflare, DataDome, Akamai, PerimeterX and others), with the vendor, a confidence level and the clues found. Run it before scraping a site to pick the piloterr_fetch_page engine. | `query` | 1 |
| `piloterr_website_technology` | List the technologies a website runs on: CMS, frameworks, analytics, CDN, hosting and more. Pass a URL with http:// or https://. | `query` | 1 |
| `piloterr_website_contacts` | Crawl a website and collect the email addresses, phone numbers and social media profiles it shows. Pass a URL with http:// or https://. | `query` | 1 |

### Search engines

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `piloterr_google_search` | Google web search: organic results, knowledge graph and related searches. Supports Google operators, country (gl), language (hl), location, time filters (tbs) and pagination. | `query` | 1 |
| `piloterr_google_news` | Google News search: articles with title, source, date, snippet and link, filtered by country, language and location. | `query` | 1 |
| `piloterr_google_images` | Google Images search: images with title, source page, image URL and size. | `query` | 1 |
| `piloterr_google_videos` | Google Videos search: videos from YouTube and other platforms, with title, channel, duration, date and link. | `query` | 1 |
| `piloterr_google_shopping` | Google Shopping search: product listings with price, rating, merchant and product ID. | `query` | 1 |
| `piloterr_google_maps` | Google Maps search: local businesses matching a name or keyword, with address, phone number, website, rating, reviews and coordinates. | `query` | 3 |
| `piloterr_google_jobs` | Google Jobs search: job listings matching a keyword, with title, category, location and description. | `query` | 1 |
| `piloterr_bing_search` | Bing web search: organic results, with market (mkt), country (cc), location and pagination. | `query` | 1 |
| `piloterr_brave_search` | Brave Search web search: organic results, with country (gl), language (hl) and pagination. | `query` | 1 |
| `piloterr_duckduckgo_search` | DuckDuckGo web search: organic results, with region and language. | `query` | 1 |
| `piloterr_yahoo_search` | Yahoo web search: organic results, with country and language. | `query` | 1 |

### LinkedIn

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `piloterr_linkedin_company` | LinkedIn company page: industry, staff count, headquarters, locations, description, specialities, followers and recent posts. Pass query (company slug, URL or ID) or domain (website domain, for example stripe.com). | `query` or `domain` | 1 |
| `piloterr_linkedin_profile` | Public LinkedIn profile of a person: headline, summary, location, experiences, education, skills, languages and certifications. Pass a username, profile URL or member ID. | `query` | 1 |
| `piloterr_linkedin_post` | One LinkedIn post: text, author, date, likes, comments, hashtags and shared links. Pass a post URL or post ID. | `query` | 1 |
| `piloterr_linkedin_job_search` | Search LinkedIn job offers by keyword, with filters for experience level, job type, date posted, remote or on-site, distance, location (geo_id) and company. | `keyword` | 1 |
| `piloterr_linkedin_job` | One LinkedIn job offer: title, company, location, description, seniority, employment type, applicants and salary when shown. Pass a job URL or job ID. | `query` | 1 |

### Social networks

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `piloterr_instagram_user` | Public Instagram profile: bio, followers, following, posts, verification, website and business category. Pass a username or profile URL. | `query` | 1 |
| `piloterr_instagram_post` | One Instagram post or reel: caption, likes, comments count, video views, location and media URLs. Pass a post URL or shortcode. | `query` | 1 |
| `piloterr_x_profile` | Public X (Twitter) profile: bio, location, followers, following, post count, verification and images. Pass a username, @handle or profile URL. | `query` | 2 |
| `piloterr_x_post` | One X (Twitter) post: text, author, likes, reposts, views and media. Pass a status URL or post ID. | `query` | 2 |
| `piloterr_pinterest_user` | Public Pinterest profile: bio, website, followers, pin and board counts, verification. Pass a username or profile URL. | `query` | 1 |
| `piloterr_github_user` | Public GitHub user profile: bio, company, location, followers, repositories and public email addresses. | `query` | 1 |

### E-commerce

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `piloterr_amazon_search` | Amazon product search on any Amazon marketplace (domain parameter, for example amazon.fr): products with ASIN, title, price, rating and reviews count, with pagination. | `query` | 1 |
| `piloterr_amazon_product` | One Amazon product by ASIN: title, price, stock, features, images, rating and seller. Set domain for marketplaces other than amazon.com. | `query` | 1 |
| `piloterr_amazon_offers` | Third-party seller offers for one Amazon product by ASIN: seller, price, discount and delivery. | `query` | 1 |
| `piloterr_ebay_search` | eBay listings search by keyword (ebay.com) or by a search URL from another eBay site: price, seller and pagination. | `query` | 3 |
| `piloterr_ebay_product` | One eBay listing by item ID or item URL: title, price, condition, seller, shipping, returns, items sold and specifications. | `query` | 3 |
| `piloterr_walmart_search` | Walmart.com search from a full search URL: product cards with price, rating, availability and pagination. | `query` | 2 |
| `piloterr_walmart_product` | One Walmart.com product from its /ip/ URL: price, rating, images, fulfillment, specifications and availability. | `query` | 2 |
| `piloterr_aliexpress_search` | AliExpress search by keyword or search URL: products with price, rating, sold count and pagination. | `query` | 2 |
| `piloterr_aliexpress_product` | One AliExpress product from its /item/ URL: title, images, seller, price, specifications, delivery and FAQs. | `query` | 2 |
| `piloterr_target_search` | Target.com search by keyword or search URL: products with price, rating and pagination. | `query` | 2 |
| `piloterr_target_product` | One Target.com product by URL or TCIN: price, description, images and variations. | `query` | 2 |
| `piloterr_bestbuy_search` | Best Buy (US or Canada) search by keyword or search URL: products with price, rating and pagination. | `query` | 2 |
| `piloterr_bestbuy_product` | One Best Buy (US or Canada) product from its URL: title, price, brand, stock, images, categories and specifications. | `query` | 2 |

### Companies and jobs

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `piloterr_crunchbase_company` | Crunchbase company profile: description, categories, founding date, headcount, location, social links, funding summary and financial highlights. Pass query (name, permalink or URL) or domain. | `query` or `domain` | 2 |
| `piloterr_crunchbase_person` | Crunchbase person profile: career history, investments and board positions. Pass a name, permalink or URL. | `query` | 2 |
| `piloterr_trustpilot_company` | Trustpilot company profile: trust score, star rating, reviews count, categories, contact details and how the company answers reviews. Pass a Trustpilot URL or the company domain. | `query` | 1 |
| `piloterr_g2_product` | G2 product page: rating, pricing, categories, alternatives and the reviews shown on the page. Pass a product slug or URL. | `query` | 2 |
| `piloterr_similarweb_domain` | Similarweb traffic estimate for a domain: monthly visits, bounce rate, global and country rank, top keywords and traffic sources. Pass a bare domain such as example.com. | `query` | 2 |
| `piloterr_indeed_job_search` | Indeed job search (fr.indeed.com by default) by keyword or Indeed search URL: job cards with salary snippets and pagination. | `query` | 2 |
| `piloterr_indeed_job` | One Indeed job offer by URL or job key: full description and structured salary. | `query` | 2 |
| `piloterr_glassdoor_company` | Glassdoor company profile by URL or employer ID: rating, reviews count, size, revenue, industry, headquarters and description. | `query` | 2 |

### Local, travel and real estate

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `piloterr_yelp_search` | Yelp search from a full search URL (find_desc and find_loc): businesses with rating, categories, photos and sponsored flag, with pagination. | `query` | 2 |
| `piloterr_yelp_business` | One Yelp business from its /biz/ URL: phone, address, website, hours and claim status. | `query` | 2 |
| `piloterr_yelp_reviews` | Reviews of one Yelp business by business ID: rating, text, author and photos, with pagination. | `query` | 2 |
| `piloterr_expedia_hotels` | Expedia hotel search from a full search URL (destination and dates in the URL): hotels with price, rating and availability. | `query` | 2 |
| `piloterr_zillow_search` | Zillow listings from a search or map URL: price, beds, baths, coordinates and listing status. | `query` | 3 |
| `piloterr_zillow_property` | One Zillow property from its homedetails URL: specifications, photos, schools, tax history and listing agent. | `query` | 3 |

### Account

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `piloterr_usage` | Your Piloterr account: plan, credits used, credits left, renewal date and rate limit. | none | free |

The full list of 390+ Piloterr endpoints is in the [API reference](https://www.piloterr.com/library). Ask in the [issues](https://github.com/piloterr/hermes-plugin-piloterr/issues) for a site you want as a tool here.

## Use it as the web_extract backend

Hermes's built-in `web_extract` tool can also fetch pages through Piloterr. Select it in `hermes tools`, or in `~/.hermes/config.yaml`:

```yaml
web:
  extract_backend: piloterr
```

The backend has one setting:

| Setting | Default | Meaning |
|---|---|---|
| `engine` | `crawler` | Engine for every `web_extract` call: `crawler`, `rendering` or `webunlocker`. |

Set it in the plugin's settings form (Plugins tab of the Hermes desktop app), or in `~/.hermes/config.yaml`:

```yaml
plugins:
  entries:
    piloterr:
      settings:
        engine: rendering
```

The backend is extract only, so keep a search backend for `web_search` (or use `piloterr_google_search`). `piloterr_fetch_page` works with or without this setting, and it lets the model choose the engine for each page.

## Example prompts

- "Search Google for the best CRM for startups in France, then read the top three results."
- "Get the LinkedIn company page of stripe.com and summarize headcount, headquarters and recent posts."
- "Compare the price of the PlayStation 5 on Amazon, eBay, Walmart and Best Buy."
- "Find Italian restaurants in Brooklyn on Google Maps and list the five best rated with their phone numbers."
- "What anti-bot protection does example-shop.com use? Then fetch its home page with the right engine."
- "Read https://example.com/app, it is a React app, wait until `.pricing-table` appears."
- "Pull the Trustpilot and G2 ratings for Notion and the Similarweb traffic of notion.so."
- "Search LinkedIn jobs for 'data engineer' in remote and give me the ten newest."
- "How many Piloterr credits do I have left?"

## Credits and errors

- Each call uses Piloterr credits: the number is in the tables above and at the end of each tool's description, so the model knows the cost before it calls. `piloterr_usage` is free and shows the balance. Plans and prices: [piloterr.com/pricing](https://www.piloterr.com/pricing).
- Errors come back to the model as `{"error": "Piloterr: <message>"}` with the API's own message (invalid key, no credits left, bad input, site not reachable), so it can fix the input or try another engine instead of stopping.
- Calls time out after 120 seconds.

## What it does on your machine

- **Network:** calls `https://api.piloterr.com` only, with your `PILOTERR_API_KEY`. Calls use credits on your Piloterr account.
- **Credentials:** reads the key only through Hermes's secret scope. It stores nothing.
- **Nothing else:** no files written, no processes started, no telemetry, no self-update. Standard library only, no dependencies.

## Development

```sh
python -m pytest
```

The tests mock the network and run without Hermes installed. `schemas.py` is generated from the Piloterr OpenAPI spec; each entry holds the tool description, its JSON schema, the API path and the credits per call.

## Contact

- Source: https://github.com/piloterr/hermes-plugin-piloterr
- Piloterr: https://www.piloterr.com
- API reference: https://www.piloterr.com/library
- Issues: https://github.com/piloterr/hermes-plugin-piloterr/issues

## License

MIT
