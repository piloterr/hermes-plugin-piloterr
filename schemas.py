"""Tool schemas (what the model reads) and how each tool maps to the Piloterr API.

Generated from the Piloterr OpenAPI spec. Each entry: (description, JSON schema of the arguments,
API path, {argument: API parameter}, fixed parameters, credits per call, README group).
"""

TOOLS = {
    'piloterr_website_antibot': (
        'Detect which anti-bot protection a website uses (Cloudflare, DataDome, Akamai, PerimeterX and others), with the vendor, a confidence level and the clues found. Run it before scraping a site to pick the piloterr_fetch_page engine. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full URL or domain name to analyze for anti-bot protection. Must be a valid hostname."
                },
                "timeout": {
                    "type": "number",
                    "description": "Maximum request timeout in seconds. Defaults to `15`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/website/antibot',
        {'query': 'query', 'timeout': 'timeout'},
        {},
        '1',
        'Websites',
    ),
    'piloterr_website_technology': (
        'List the technologies a website runs on: CMS, frameworks, analytics, CDN, hosting and more. Pass a URL with http:// or https://. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A website URL to analyze for technology stack detection. Must include the `http://` or `https://` protocol."
                },
                "mode": {
                    "type": "string",
                    "description": "Controls the level of detail returned in the technology detection response. Default: expert."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/website/technology',
        {'query': 'query', 'mode': 'mode'},
        {},
        '1',
        'Websites',
    ),
    'piloterr_website_contacts': (
        'Crawl a website and collect the email addresses, phone numbers and social media profiles it shows. Pass a URL with http:// or https://. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A website URL to crawl for contact information. Must include the `http://` or `https://` protocol. The crawler will follow internal links (\"a\" anchors) to find contact details across the site."
                },
                "country_code": {
                    "type": "string",
                    "description": "An ISO 3166-1 alpha-2 country code used to improve the accuracy of phone number validation and parsing."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/website/email_phone_extractor',
        {'query': 'query', 'country_code': 'country_code'},
        {},
        '1',
        'Websites',
    ),
    'piloterr_google_search': (
        'Google web search: organic results, knowledge graph and related searches. Supports Google operators, country (gl), language (hl), location, time filters (tbs) and pagination. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to execute on Google. Supports all standard Google search operators."
                },
                "tbs": {
                    "type": "string",
                    "description": "Advanced time-range and filter string for Google Search. Used to restrict results by recency. - `qdr:h`: Last hour - `qdr:d`: Last day - `qdr:w`: Last week - `qdr:m`: Last month - `qdr:y`: Last year Example: qdr:w"
                },
                "location": {
                    "type": "string",
                    "description": "City or region from which the search should originate. Simulates a real user's search from the specified location. Examples: ``` New York, NY ``` ``` Paris, France ``` ``` Tokyo, Japan ```"
                },
                "uule": {
                    "type": "string",
                    "description": "Google-encoded location string for precise geographic targeting."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to `google.com`. Examples: - `google.com` - `google.co.uk` - `google.fr` Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. `us` for the United States, `uk` for United Kingdom, or `fr` for France). Example: us Default: us."
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. `en`, `es`, `fr`), optionally followed by a region code (e.g. `en-gb`, `es-419`). Example: en Default: en."
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use `country{XX}` with `|` as delimiter (e.g. `countryFR|countryDE`). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use `lang_{xx}` with `|` as delimiter (e.g. `lang_fr|lang_de`). Example: lang_en"
                },
                "page": {
                    "type": "number",
                    "description": "Page number of search results to retrieve. - `1`: First page (default) - `2`: Second page, etc. Default: 1."
                },
                "num": {
                    "type": "number",
                    "description": "Maximum number of results to return per page (e.g. `10`, `40`, `100`). Note: This parameter is deprecated and may not reliably affect the number of results returned. Default: 10."
                },
                "safe": {
                    "type": "string",
                    "description": "Adult content filter. `active` enables Google SafeSearch; `off` disables it. Omit to use Google default."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/google/search',
        {'query': 'query', 'tbs': 'tbs', 'location': 'location', 'uule': 'uule', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'page': 'page', 'num': 'num', 'safe': 'safe'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_google_news': (
        'Google News search: articles with title, source, date, snippet and link, filtered by country, language and location. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The news search query to execute on Google News. Supports standard Google search operators."
                },
                "location": {
                    "type": "string",
                    "description": "City or region from which the news search should originate. Simulates a search performed from the specified location. Examples: ``` New York, NY ``` ``` Paris, France ``` ``` Tokyo, Japan ```"
                },
                "uule": {
                    "type": "string",
                    "description": "Google-encoded location string for precise geographic targeting. Use this instead of `location` when you need exact control."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to `google.com`. Examples: - `google.com` - `google.co.uk` - `google.fr` Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. `us` for the United States, `uk` for United Kingdom, or `fr` for France). Example: us Default: us."
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. `en`, `es`, `fr`), optionally followed by a region code (e.g. `en-gb`, `es-419`). Example: en Default: en."
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use `country{XX}` with `|` as delimiter (e.g. `countryFR|countryDE`). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use `lang_{xx}` with `|` as delimiter (e.g. `lang_fr|lang_de`). Example: lang_en"
                },
                "page": {
                    "type": "number",
                    "description": "Page number of news results to retrieve. - `1`: First page (default) - `2`: Second page, etc. Default: 1."
                },
                "num": {
                    "type": "number",
                    "description": "Maximum number of results to return per page. - `10`: Default - `40`: 40 results - `100`: 100 results Default: 10."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/google/news',
        {'query': 'query', 'location': 'location', 'uule': 'uule', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'page': 'page', 'num': 'num'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_google_images': (
        'Google Images search: images with title, source page, image URL and size. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The image search query to execute on Google Images. Example: mountain landscape"
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to `google.com`. Examples: - `google.com` - `google.co.uk` - `google.fr` Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. `us` for the United States, `uk` for United Kingdom, or `fr` for France). Example: us Default: us."
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. `en`, `es`, `fr`), optionally followed by a region code (e.g. `en-gb`, `es-419`). Example: en Default: en."
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use `country{XX}` with `|` as delimiter (e.g. `countryFR|countryDE`). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use `lang_{xx}` with `|` as delimiter (e.g. `lang_fr|lang_de`). Example: lang_en"
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination. Images are returned in batches of 100 per page. - `1`: First 100 images (default) - `2`: Next 100 images - `3`: Next 100 images, etc. Default: 1."
                },
                "safe": {
                    "type": "string",
                    "description": "Adult content filter. `active` enables Google SafeSearch; `off` disables it. Omit to use Google default."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/google/images',
        {'query': 'query', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'page': 'page', 'safe': 'safe'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_google_videos': (
        'Google Videos search: videos from YouTube and other platforms, with title, channel, duration, date and link. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The video search query to execute on Google Videos. Supports standard Google search operators."
                },
                "location": {
                    "type": "string",
                    "description": "City or region from which the video search should originate. Examples: ``` New York, NY ``` ``` Paris, France ```"
                },
                "uule": {
                    "type": "string",
                    "description": "Google-encoded location string for precise geographic targeting."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to `google.com`. Examples: - `google.com` - `google.co.uk` - `google.fr` Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. `us` for the United States, `uk` for United Kingdom, or `fr` for France). Example: us Default: us."
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. `en`, `es`, `fr`), optionally followed by a region code (e.g. `en-gb`, `es-419`). Example: en Default: en."
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use `country{XX}` with `|` as delimiter (e.g. `countryFR|countryDE`). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use `lang_{xx}` with `|` as delimiter (e.g. `lang_fr|lang_de`). Example: lang_en"
                },
                "page": {
                    "type": "number",
                    "description": "Page number of video results to retrieve. - `1`: First page (default) - `2`: Second page, etc. Default: 1."
                },
                "num": {
                    "type": "number",
                    "description": "Maximum number of video results to return per page. - `10`: Default - `40`: 40 results - `100`: 100 results Default: 10."
                },
                "safe": {
                    "type": "string",
                    "description": "Adult content filter. `active` enables Google SafeSearch; `off` disables it. Omit to use Google default."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/google/videos',
        {'query': 'query', 'location': 'location', 'uule': 'uule', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'page': 'page', 'num': 'num', 'safe': 'safe'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_google_shopping': (
        'Google Shopping search: product listings with price, rating, merchant and product ID. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Product search query on Google Shopping. Use a product name, brand, or category."
                },
                "page": {
                    "type": "number",
                    "description": "Page number of Shopping results. Each page returns about 20 products. There is no `num` parameter. - `1`: First page (default) - `2`: Second page, etc. Default: 1."
                },
                "location": {
                    "type": "string",
                    "description": "City or region used to localize Shopping results. Simulates a search from that location and generates the UULE parameter automatically."
                },
                "uule": {
                    "type": "string",
                    "description": "Google-encoded location string (UULE) for precise geo-targeting. Use `location` instead if you do not already have an encoded value."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to `google.com`. Examples: - `google.com` - `google.co.uk` - `google.fr` Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. `us` for the United States, `uk` for United Kingdom, or `fr` for France). Example: us Default: us."
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. `en`, `es`, `fr`), optionally followed by a region code (e.g. `en-gb`, `es-419`). Example: en Default: en."
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use `country{XX}` with `|` as delimiter (e.g. `countryFR|countryDE`). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use `lang_{xx}` with `|` as delimiter (e.g. `lang_fr|lang_de`). Example: lang_en"
                },
                "safe": {
                    "type": "string",
                    "description": "Adult content filter. `active` enables Google SafeSearch; `off` disables it. Omit to use Google default."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/google/shopping',
        {'query': 'query', 'page': 'page', 'location': 'location', 'uule': 'uule', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'safe': 'safe'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_google_maps': (
        'Google Maps search: local businesses matching a name or keyword, with address, phone number, website, rating, reviews and coordinates. Costs 3 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Business name or keyword to search for relevant data."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/google/maps',
        {'query': 'query'},
        {},
        '3',
        'Search engines',
    ),
    'piloterr_google_jobs': (
        'Google Jobs search: job listings matching a keyword, with title, category, location and description. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Job search term or keyword for querying Google job listings."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/google/jobs',
        {'query': 'query'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_bing_search': (
        'Bing web search: organic results, with market (mkt), country (cc), location and pagination. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to execute on Bing. Supports all Bing advanced search operators."
                },
                "page": {
                    "type": "number",
                    "description": "Page number of results to retrieve. Used for pagination. - `1`: First page (default) - `2`: Second page - `3`: Third page, etc."
                },
                "num": {
                    "type": "number",
                    "description": "Number of results per page. Minimum: `10`, Maximum: `50`. Note: This parameter is only a suggestion and might not reflect the actual number of results returned."
                },
                "location": {
                    "type": "string",
                    "description": "City or region from which the search should originate. If multiple locations match, the most popular one is selected. Note: Cannot be used together with `lat`/`lon`."
                },
                "lat": {
                    "type": "number",
                    "description": "GPS latitude coordinate for the search origin. Example: 48.8566"
                },
                "lon": {
                    "type": "number",
                    "description": "GPS longitude coordinate for the search origin. Example: 2.3522"
                },
                "mkt": {
                    "type": "string",
                    "description": "Market code combining language and country, in the form `<language>-<country>`. Defines where the results come from."
                },
                "cc": {
                    "type": "string",
                    "description": "Two-letter ISO 3166-1 country code defining the country to search from. - `us`: United States - `de`: Germany - `gb`: United Kingdom - `fr`: France Note: Cannot be used together with `mkt`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/bing/search',
        {'query': 'query', 'page': 'page', 'num': 'num', 'location': 'location', 'lat': 'lat', 'lon': 'lon', 'mkt': 'mkt', 'cc': 'cc'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_brave_search': (
        'Brave Search web search: organic results, with country (gl), language (hl) and pagination. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to execute on Brave Search. Supports all standard Brave search operators."
                },
                "page": {
                    "type": "number",
                    "description": "Page number of results to retrieve. Used for pagination. - `1`: First page (default) - `2`: Second page - `3`: Third page, etc. Default: 1."
                },
                "gl": {
                    "type": "string",
                    "description": "Country code, for example us, fr, gb, de. Default: us."
                },
                "hl": {
                    "type": "string",
                    "description": "Language code, for example en, fr, de. Default: en."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/brave/search',
        {'query': 'query', 'page': 'page', 'gl': 'gl', 'hl': 'hl'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_duckduckgo_search': (
        'DuckDuckGo web search: organic results, with region and language. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query sent to DuckDuckGo Search."
                },
                "page": {
                    "type": "number",
                    "description": "Page number. Page 1 is the first page of results. Default: 1."
                },
                "gl": {
                    "type": "string",
                    "description": "Country code, for example us, fr, gb, de, jp."
                },
                "hl": {
                    "type": "string",
                    "description": "Language code, for example en, fr, de, ja, zh."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/duckduckgo/search',
        {'query': 'query', 'page': 'page', 'gl': 'gl', 'hl': 'hl'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_yahoo_search': (
        'Yahoo web search: organic results, with country and language. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query sent to Yahoo Search."
                },
                "page": {
                    "type": "number",
                    "description": "Page number. Page 1 is the first page of results. Default: 1."
                },
                "gl": {
                    "type": "string",
                    "description": "Country code, for example us, fr, gb, de, jp."
                },
                "hl": {
                    "type": "string",
                    "description": "Language code, for example en, fr, de, ja, zh."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/yahoo/search',
        {'query': 'query', 'page': 'page', 'gl': 'gl', 'hl': 'hl'},
        {},
        '1',
        'Search engines',
    ),
    'piloterr_linkedin_company': (
        'LinkedIn company page: industry, staff count, headquarters, locations, description, specialities, followers and recent posts. Pass query (company slug, URL or ID) or domain (website domain, for example stripe.com). Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "LinkedIn company identifier when you already know the page."
                },
                "domain": {
                    "type": "string",
                    "description": "Company website domain for reverse lookup when you do not have the LinkedIn URL."
                }
            },
            "required": []
        },
        '/v2/linkedin/company/info',
        {'query': 'query', 'domain': 'domain'},
        {},
        '1',
        'LinkedIn',
    ),
    'piloterr_linkedin_profile': (
        'Public LinkedIn profile of a person: headline, summary, location, experiences, education, skills, languages and certifications. Pass a username, profile URL or member ID. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The LinkedIn profile to retrieve. Accepts a username, full profile URL, or numeric member ID."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/linkedin/profile/info',
        {'query': 'query'},
        {},
        '1',
        'LinkedIn',
    ),
    'piloterr_linkedin_post': (
        'One LinkedIn post: text, author, date, likes, comments, hashtags and shared links. Pass a post URL or post ID. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The LinkedIn post to retrieve. Accepts a numeric post ID or a full post URL."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/linkedin/post/info',
        {'query': 'query'},
        {},
        '1',
        'LinkedIn',
    ),
    'piloterr_linkedin_job_search': (
        'Search LinkedIn job offers by keyword, with filters for experience level, job type, date posted, remote or on-site, distance, location (geo_id) and company. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "Job title or keyword to search for. Example: Software Engineer Leave empty to return all jobs matching the other filters."
                },
                "experience_level": {
                    "type": "string",
                    "description": "Filter by seniority level."
                },
                "job_type": {
                    "type": "string",
                    "description": "Filter by employment type."
                },
                "when": {
                    "type": "string",
                    "description": "Filter by posting date recency. Accepted values: - `day`: Posted in the last 24 hours - `week`: Posted in the last 7 days - `month`: Posted in the last 30 days"
                },
                "flexibility": {
                    "type": "string",
                    "description": "Filter by work arrangement. Accepted values: - `remote`: Fully remote positions - `flexible`: Hybrid or flexible arrangements - `on_site`: On-site only positions"
                },
                "distance": {
                    "type": "number",
                    "description": "Maximum radius in miles from the target location (requires `geo_id`). Accepted values: `5`, `10`, `25`, `50`, `100`"
                },
                "geo_id": {
                    "type": "string",
                    "description": "LinkedIn geo ID for the target location. Default is `92000000` (worldwide). Default: 92000000."
                },
                "company_id": {
                    "type": "string",
                    "description": "LinkedIn numeric company ID to filter results to jobs posted by a specific company. Example: - `33246798`: TikTok Use the LinkedIn Company Info endpoint to retrieve a company's ID."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for paginating through results. Default is `1`. Each page returns up to 25 job listings. Default: 1."
                }
            },
            "required": []
        },
        '/v2/linkedin/job/search',
        {'keyword': 'keyword', 'experience_level': 'experience_level', 'job_type': 'job_type', 'when': 'when', 'flexibility': 'flexibility', 'distance': 'distance', 'geo_id': 'geo_id', 'company_id': 'company_id', 'page': 'page'},
        {},
        '1',
        'LinkedIn',
    ),
    'piloterr_linkedin_job': (
        'One LinkedIn job offer: title, company, location, description, seniority, employment type, applicants and salary when shown. Pass a job URL or job ID. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The LinkedIn job posting to retrieve. Accepts a numeric job ID or a full job posting URL."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/linkedin/job/info',
        {'query': 'query'},
        {},
        '1',
        'LinkedIn',
    ),
    'piloterr_instagram_user': (
        'Public Instagram profile: bio, followers, following, posts, verification, website and business category. Pass a username or profile URL. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The Instagram user to look up. Accepts a full profile URL or a username."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/instagram/user/info',
        {'query': 'query'},
        {},
        '1',
        'Social networks',
    ),
    'piloterr_instagram_post': (
        'One Instagram post or reel: caption, likes, comments count, video views, location and media URLs. Pass a post URL or shortcode. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The Instagram post or reel to retrieve. Accepts a full URL or a shortcode."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/instagram/post/info',
        {'query': 'query'},
        {},
        '1',
        'Social networks',
    ),
    'piloterr_x_profile': (
        'Public X (Twitter) profile: bio, location, followers, following, post count, verification and images. Pass a username, @handle or profile URL. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "X profile to look up. Accepts a username, @handle, or profile URL. Examples: ``` elonmusk ``` ``` @example-user ``` ``` https://x.com/example-user ``` Notes: - Legacy `twitter.com` URLs are supported."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return the raw HTML page source as `{\"result\": \"...\"}` instead of structured JSON. Defaults to `false`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/x/profile/info',
        {'query': 'query', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'Social networks',
    ),
    'piloterr_x_post': (
        'One X (Twitter) post: text, author, likes, reposts, views and media. Pass a status URL or post ID. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "X tweet to retrieve. Accepts a full status URL or numeric tweet ID."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return the raw HTML page source as `{\"result\": \"...\"}` instead of structured JSON. Defaults to `false`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/x/post/info',
        {'query': 'query', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'Social networks',
    ),
    'piloterr_pinterest_user': (
        'Public Pinterest profile: bio, website, followers, pin and board counts, verification. Pass a username or profile URL. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The Pinterest profile to retrieve. Accepts a full profile URL or a username."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/pinterest/user/info',
        {'query': 'query'},
        {},
        '1',
        'Social networks',
    ),
    'piloterr_github_user': (
        'Public GitHub user profile: bio, company, location, followers, repositories and public email addresses. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A GitHub user identifier."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/github/user/info',
        {'query': 'query'},
        {},
        '1',
        'Social networks',
    ),
    'piloterr_amazon_search': (
        'Amazon product search on any Amazon marketplace (domain parameter, for example amazon.fr): products with ASIN, title, price, rating and reviews count, with pagination. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword or phrase to search for products on Amazon. Example: playstation 5 Notes: - Searches are performed against the marketplace set by the `domain` parameter. - Results include both organic and sponsored (ad) listings"
                },
                "domain": {
                    "type": "string",
                    "description": "Amazon domain extension to query. Controls which Amazon marketplace is searched. Default: com."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for paginated search results. Each page returns up to 60 results. Default: 1."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/amazon/search',
        {'query': 'query', 'domain': 'domain', 'page': 'page'},
        {},
        '1',
        'E-commerce',
    ),
    'piloterr_amazon_product': (
        'One Amazon product by ASIN: title, price, stock, features, images, rating and seller. Set domain for marketplaces other than amazon.com. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Amazon product ASIN (Amazon Standard Identification Number) to retrieve full product details for. Example: B09DFCB66S Notes: - The ASIN is a 10-character alphanumeric code found in the Amazon product URL (e.g."
                },
                "domain": {
                    "type": "string",
                    "description": "Amazon domain extension to query. Controls which Amazon marketplace is targeted. Default: com."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/amazon/product',
        {'query': 'query', 'domain': 'domain'},
        {},
        '1',
        'E-commerce',
    ),
    'piloterr_amazon_offers': (
        'Third-party seller offers for one Amazon product by ASIN: seller, price, discount and delivery. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Amazon product ASIN (Amazon Standard Identification Number) to retrieve third-party seller offers for. Example: B093C9B1HK Notes: - The ASIN is a 10-character alphanumeric code visible in the product URL on Amazon (e.g."
                },
                "domain": {
                    "type": "string",
                    "description": "Amazon domain extension to query. Controls which Amazon marketplace is targeted. Default: com."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for paginated offer results. Note: Use this parameter to paginate through multiple pages of offers when a product has many third-party sellers. Default: 1."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/amazon/product/offer',
        {'query': 'query', 'domain': 'domain', 'page': 'page'},
        {},
        '1',
        'E-commerce',
    ),
    'piloterr_ebay_search': (
        'eBay listings search by keyword (ebay.com) or by a search URL from another eBay site: price, seller and pagination. Costs 3 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword on www.ebay.com, or a search URL on a supported eBay site. Example (keyword): laptop Example (search URL): https://www.ebay.fr/sch/i.html?_nkw=ordinateur Notes: - A keyword always searches `www.ebay.com`."
                },
                "page": {
                    "type": "number",
                    "description": "Page number, sent as _pgn. Default 1 for a keyword. On a URL, the page already in the URL is kept when this is empty. Below 1 returns 400."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When true, return raw HTML."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/ebay/search',
        {'query': 'query', 'page': 'page', 'return_page_source': 'return_page_source'},
        {},
        '3',
        'E-commerce',
    ),
    'piloterr_ebay_product': (
        'One eBay listing by item ID or item URL: title, price, condition, seller, shipping, returns, items sold and specifications. Costs 3 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Item id, or an item URL on a supported eBay site. Example (item id): 257758922911 Example (item URL): https://www.ebay.de/itm/257758922911 Notes: - A bare id is loaded on `www.ebay.com`."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When true, return raw HTML."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/ebay/product',
        {'query': 'query', 'return_page_source': 'return_page_source'},
        {},
        '3',
        'E-commerce',
    ),
    'piloterr_walmart_search': (
        'Walmart.com search from a full search URL: product cards with price, rating, availability and pagination. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full Walmart search results URL."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/walmart/search',
        {'query': 'query'},
        {},
        '2',
        'E-commerce',
    ),
    'piloterr_walmart_product': (
        'One Walmart.com product from its /ip/ URL: price, rating, images, fulfillment, specifications and availability. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full Walmart product page URL. Example: https://www.walmart.com/ip/Fresh-Rockit-Crisp-Sweet-Miniature-Apples-3lb-Tub/309762096 Notes: - The URL must point to a Walmart product detail page containing `/ip/` in the path."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/walmart/product',
        {'query': 'query'},
        {},
        '2',
        'E-commerce',
    ),
    'piloterr_aliexpress_search': (
        'AliExpress search by keyword or search URL: products with price, rating, sold count and pagination. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keyword or full AliExpress search results URL. Example (keyword): meta Resolves to a wholesale search page such as `https://www.aliexpress.com/w/wholesale-meta.html`."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return the raw HTML page source as `{\"result\": \"...\"}` instead of structured JSON. Defaults to `false`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/aliexpress/search',
        {'query': 'query', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'E-commerce',
    ),
    'piloterr_aliexpress_product': (
        'One AliExpress product from its /item/ URL: title, images, seller, price, specifications, delivery and FAQs. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full AliExpress product page URL (`/item/{id}.html`)."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return the raw HTML page source as `{\"result\": \"...\"}` instead of parsed JSON. Defaults to `false`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/aliexpress/product',
        {'query': 'query', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'E-commerce',
    ),
    'piloterr_target_search': (
        'Target.com search by keyword or search URL: products with price, rating and pagination. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword or Target search URL. Examples: ``` shampoo ``` ``` root touch up hair dye ``` ``` https://www.target.com/s?searchTerm=shampoo ```"
                },
                "page": {
                    "type": "string",
                    "description": "Page number (1-based)."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return rendered HTML instead of JSON."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/target/search',
        {'query': 'query', 'page': 'page', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'E-commerce',
    ),
    'piloterr_target_product': (
        'One Target.com product by URL or TCIN: price, description, images and variations. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Target product URL or bare TCIN. Examples: ``` 17457624 ``` ``` https://www.target.com/p/-/A-17457624 ``` ``` https://www.target.com/p/l-oreal-paris-magic-root-cover-up-medium-brown-2-0oz/-/A-17457624 ```"
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return rendered HTML instead of JSON."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/target/product',
        {'query': 'query', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'E-commerce',
    ),
    'piloterr_bestbuy_search': (
        'Best Buy (US or Canada) search by keyword or search URL: products with price, rating and pagination. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword or full Best Buy search URL."
                },
                "region": {
                    "type": "string",
                    "description": "Best Buy country when `query` is not a full URL (default: `com`). Supported: - `com` → www.bestbuy.com, USD - `ca` → www.bestbuy.ca, CAD"
                },
                "page": {
                    "type": "number",
                    "description": "Page number (default: `1`)."
                },
                "sort": {
                    "type": "string",
                    "description": "Sort order (default: `best_selling`). Supported: `best_selling`, `best_discount` Default: best_selling."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return rendered HTML as `{\"result\": \"...\"}` instead of JSON. Defaults to `false`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/bestbuy/search',
        {'query': 'query', 'region': 'region', 'page': 'page', 'sort': 'sort', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'E-commerce',
    ),
    'piloterr_bestbuy_product': (
        'One Best Buy (US or Canada) product from its URL: title, price, brand, stock, images, categories and specifications. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full Best Buy product URL."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return rendered HTML as `{\"result\": \"...\"}` instead of JSON. Defaults to `false`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/bestbuy/product',
        {'query': 'query', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'E-commerce',
    ),
    'piloterr_crunchbase_company': (
        'Crunchbase company profile: description, categories, founding date, headcount, location, social links, funding summary and financial highlights. Pass query (name, permalink or URL) or domain. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search for a company by its name, permalink, or full Crunchbase URL."
                },
                "domain": {
                    "type": "string",
                    "description": "Perform a reverse lookup by domain name to find the associated Crunchbase company profile."
                }
            },
            "required": []
        },
        '/v2/crunchbase/company/info',
        {'query': 'query', 'domain': 'domain'},
        {},
        '2',
        'Companies and jobs',
    ),
    'piloterr_crunchbase_person': (
        'Crunchbase person profile: career history, investments and board positions. Pass a name, permalink or URL. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search for a person by their name, Crunchbase permalink, or full Crunchbase profile URL."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/crunchbase/people/info',
        {'query': 'query'},
        {},
        '2',
        'Companies and jobs',
    ),
    'piloterr_trustpilot_company': (
        'Trustpilot company profile: trust score, star rating, reviews count, categories, contact details and how the company answers reviews. Pass a Trustpilot URL or the company domain. Costs 1 Piloterr credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A Trustpilot company URL or domain name. Examples: https://www.trustpilot.com/review/nordvpn.com Both the full Trustpilot review URL and the company domain are accepted."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/trustpilot/company/info',
        {'query': 'query'},
        {},
        '1',
        'Companies and jobs',
    ),
    'piloterr_g2_product': (
        'G2 product page: rating, pricing, categories, alternatives and the reviews shown on the page. Pass a product slug or URL. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Product slug or a www.g2.com product URL. Examples: postman https://www.g2.com/products/postman Both the slug and the full product URL are accepted."
                },
                "nps_score": {
                    "type": "number",
                    "description": "Keep reviews of one star rating, from 1 to 5. Omit it to read the unfiltered reviews page."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "Return the rendered HTML instead of the parsed product."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/g2/product/info',
        {'query': 'query', 'nps_score': 'nps_score', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'Companies and jobs',
    ),
    'piloterr_similarweb_domain': (
        'Similarweb traffic estimate for a domain: monthly visits, bounce rate, global and country rank, top keywords and traffic sources. Pass a bare domain such as example.com. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A domain name to retrieve traffic and engagement metrics for. Examples: google.com Provide the bare domain without `https://` or `www.` prefixes."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/similarweb/domain',
        {'query': 'query'},
        {},
        '2',
        'Companies and jobs',
    ),
    'piloterr_indeed_job_search': (
        'Indeed job search (fr.indeed.com by default) by keyword or Indeed search URL: job cards with salary snippets and pagination. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword, Indeed `/jobs` URL or SEO search URL on fr.indeed.com (default domain)."
                },
                "page": {
                    "type": "number",
                    "description": "1-based page number (10 results per page). Default: `1`."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return the raw HTML as `{\\\"result\\\": \\\"...\\\"}` instead of structured JSON. Defaults to `false`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/indeed/job/search',
        {'query': 'query', 'page': 'page', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'Companies and jobs',
    ),
    'piloterr_indeed_job': (
        'One Indeed job offer by URL or job key: full description and structured salary. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Indeed job URL, sponsored SERP click URL or 16-char `jk` job key. Examples: ``` 585181841cb618e0 ``` ``` https://fr.indeed.com/viewjob?jk=585181841cb618e0 ``` Bare `jk` values resolve on fr.indeed.com."
                },
                "return_page_source": {
                    "type": "boolean",
                    "description": "When `true`, return the raw HTML as `{\\\"result\\\": \\\"...\\\"}` instead of structured JSON. Defaults to `false`."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/indeed/job/info',
        {'query': 'query', 'return_page_source': 'return_page_source'},
        {},
        '2',
        'Companies and jobs',
    ),
    'piloterr_glassdoor_company': (
        'Glassdoor company profile by URL or employer ID: rating, reviews count, size, revenue, industry, headquarters and description. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Company URL or employer id.\\n\\nExample:\\n\\n 1692882"
                },
                "domain": {
                    "type": "string",
                    "description": "Glassdoor TLD when query is not a full URL. Default: fr."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/glassdoor/company/info',
        {'query': 'query', 'domain': 'domain'},
        {},
        '2',
        'Companies and jobs',
    ),
    'piloterr_yelp_search': (
        'Yelp search from a full search URL (find_desc and find_loc): businesses with rating, categories, photos and sponsored flag, with pagination. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full Yelp search URL with `find_desc` and `find_loc` query parameters."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/yelp/search',
        {'query': 'query'},
        {},
        '2',
        'Local, travel and real estate',
    ),
    'piloterr_yelp_business': (
        'One Yelp business from its /biz/ URL: phone, address, website, hours and claim status. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full Yelp business URL. Example: https://www.yelp.com/biz/novela-san-francisco-2 Use an organic `/biz/` link from Yelp Search results."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/yelp/business',
        {'query': 'query'},
        {},
        '2',
        'Local, travel and real estate',
    ),
    'piloterr_yelp_reviews': (
        'Reviews of one Yelp business by business ID: rating, text, author and photos, with pagination. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Yelp business ID / encid. Example: cX5dOMkwZ5rqWbeIJpw_Ig Use `biz_id` from Yelp Search or `business_id` from Yelp Business."
                },
                "page": {
                    "type": "number",
                    "description": "Page number. Each page returns up to 10 reviews. Default: `1`. Default: 1."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/yelp/reviews',
        {'query': 'query', 'page': 'page'},
        {},
        '2',
        'Local, travel and real estate',
    ),
    'piloterr_expedia_hotels': (
        'Expedia hotel search from a full search URL (destination and dates in the URL): hotels with price, rating and availability. Costs 2 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A valid Expedia hotel search URL. Copy the URL directly from your Expedia search results page."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/expedia/search',
        {'query': 'query'},
        {},
        '2',
        'Local, travel and real estate',
    ),
    'piloterr_zillow_search': (
        'Zillow listings from a search or map URL: price, beds, baths, coordinates and listing status. Costs 3 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full Zillow search or map results URL."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/zillow/search',
        {'query': 'query'},
        {},
        '3',
        'Local, travel and real estate',
    ),
    'piloterr_zillow_property': (
        'One Zillow property from its homedetails URL: specifications, photos, schools, tax history and listing agent. Costs 3 Piloterr credits per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full Zillow homedetails URL. Example: https://www.zillow.com/homedetails/20-Kyle-Ct-Staten-Island-NY-10312/32361983_zpid/ Notes: - Only Zillow homedetails URLs are accepted (`/homedetails/.../{zpid}_zpid/`)."
                }
            },
            "required": [
                "query"
            ]
        },
        '/v2/zillow/property',
        {'query': 'query'},
        {},
        '3',
        'Local, travel and real estate',
    ),
    'piloterr_usage': (
        'Your Piloterr account: plan, credits used, credits left, renewal date and rate limit. Free.',
        {
            "type": "object",
            "properties": {},
            "required": []
        },
        '/v2/usage',
        {},
        {},
        None,
        'Account',
    ),
}
