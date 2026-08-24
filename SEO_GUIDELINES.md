# 🔍 Master Technical SEO, Crawling & Indexing Specification (`SEO_GUIDELINES.md`)

This comprehensive engineering specification codifies official guidelines from **Google Search Central** (Search Essentials, Crawler Infrastructure, URL Structure, Link Architecture, Multi-Sitemaps, HTTP Status Handling, E-E-A-T Framework, and Generative AI Search Optimization) across all Finnova digital properties:
* `procrm.com.au` (Enterprise CRM & Cybersecurity Intelligence)
* `ezconsultants.com.au` (Cloud & Salesforce Engineering Advisory)
* `finnova.org.au` (Fintech & Digital Transformation)
* `ezmortgagebroker.com.au` (Property Finance & Mortgage Advisory)

---

## 🏛️ 1. The Three Stages of Google Search

```
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│       1. CRAWLING         │ ───► │        2. INDEXING        │ ───► │     3. SERVING RESULTS    │
│  Googlebot downloads text,│      │ Analyzes rendered DOM,    │      │ Matches search intent,    │
│  images, videos & renders │      │ JSON-LD, E-E-A-T signals  │      │ RAG grounding & fan-out.  │
│  JavaScript via Chrome.   │      │ & canonical clustering.   │      │ Serves rich snippets & AI.│
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘
```

1. **Crawling (Discovery & Rendering)**: Googlebot fetches URLs via crawlable `<a href="...">` links and XML sitemaps. Executes JavaScript, CSS, and dynamic DOM states via headless Chrome.
2. **Indexing (Semantics & Canonical Election)**: Evaluates textual semantics, metadata, JSON-LD structured data, image `alt` context, and elects a single canonical URL per cluster.
3. **Serving Results & Generative AI Features**: Dynamically generates Title Links, Snippets, Rich Badges, and grounds **Google AI Overviews** using Retrieval-Augmented Generation (RAG).

---

## 🔗 2. URL Structure Standards (IETF STD 66 / RFC 3986)

To ensure Googlebot crawls our sites efficiently without runaway crawl loops or parameter explosions:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               URL BEST PRACTICES MATRIX                                 │
├───────────────────────────────────┬─────────────────────────────────────────────────────┤
│ Recommended Pattern               │ Avoided / Anti-Pattern                              │
├───────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • Hyphen-separated lowercase      │ ❌ Underscores (`format_date`) or merged words       │
│   `/cyber-security/patch-guide`   │    `/cybersecuritypatchguide`                       │
│ • History API for SPA state       │ ❌ URI Fragments / Hashes (`/#/patch-guide`)         │
│   `history.pushState()`           │    (Googlebot ignores hash fragments for content)   │
│ • Standard Key-Value Encoding     │ ❌ Custom colons or bracket notation                │
│   `?category=salesforce&sort=asc` │    `?[category:salesforce][sort:asc]`               │
│ • Multi-value comma separation    │ ❌ Double commas or non-standard delimiters         │
│   `?state=nsw,vic,qld`            │    `?state,,nsw,,vic`                               │
│ • Root-Relative internal links    │ ❌ Parent-relative chains (`../../category/guide`)  │
│   `<a href="/blog/guide">`        │    (Risk creating infinite phantom directory spaces)│
│ • Percent-encoding for non-ASCII  │ ❌ Unencoded non-ASCII or emoji characters in URIs  │
│   `%D9%86%D8%B9%D9%86%D8%A7%D8%B9`│                                                     │
└───────────────────────────────────┴─────────────────────────────────────────────────────┘
```

---

## ⚓ 3. Crawlable Link Architecture & Anchor Text Standards

Google uses hyperlinks as the primary signal for topical relevancy and new page discovery:

### A. Crawlable Anchor Elements
* **Always use valid HTML `<a>` tags with `href` attributes**:
  * ✅ `<a href="/blog/rba-rate-decision">Read RBA Analysis</a>`
  * ❌ `<span href="...">`, `<a routerLink="...">`, or `<a onclick="goTo('...')">`
* **Dynamic JavaScript Links**: When inserting links via JS, always inject true `<a href="...">` elements into the live DOM.

### B. Anchor Text Best Practices
* **Descriptive & Contextual**: State clearly what the destination page contains (e.g. *"explore our [First Home Guarantee Eligibility Guide](file:///...)"*).
* **Zero Generic Anchor Text**: Never use vague phrases like *"click here"*, *"read more"*, *"article"*, or *"website"*.
* **Image Links as Fallbacks**: When linking via an image, Google uses the image's `alt` attribute as anchor text. Always populate `alt="Detailed descriptive text"`.
* **Outbound Link Qualification (`rel`)**:
  * `rel="nofollow"`: For unverified external sources or paid mentions.
  * `rel="sponsored"`: For commercial affiliate or partner links.
  * `rel="ugc"`: For user-generated comments or community contributions.
  * `rel="noopener noreferrer"`: For all target `_blank` external tabs.

---

## 📁 4. Supported & Indexable File Formats

Google indexes both plain-text markup and parsed binary formats:
* **Flat Text Files**: HTML (`.html`), XML (`.xml`), CSV (`.csv`), TXT (`.txt`), SVG (`.svg`), and source code (`.py`, `.js`, `.ts`, `.cs`, `.java`).
* **Encoded Documents**: Adobe PDF (`.pdf` up to 64MB), Microsoft Office (`.docx`, `.xlsx`, `.pptx`), Rich Text (`.rtf`), EPUB (`.epub`).
* **Visual & Media Formats**: WebP, AVIF, PNG, JPEG, GIF, SVG, BMP, and MP4/WebM videos.
* **Search Operator**: Use `filetype:pdf` or `filetype:docx` in Google to audit indexed document assets.

---

## 🗺️ 5. Multi-Sitemap Architecture & Combining Extensions

### A. Specifications & Boundaries
* **Limits**: Maximum **50,000 URLs** and **50 MB** (uncompressed) per individual sitemap.
* **Sitemap Index (`sitemapindex`)**: Used to orchestrate up to 500 sub-sitemaps in Search Console.
* **`<lastmod>` Rule of Truth**: Must use W3C Datetime format (`YYYY-MM-DDThh:mm:ss+TZD`). Only update on substantive editorial or schema changes (never for simple copyright footer updates).

### B. Combined Extensions Syntax Example
Google allows combining News, Image, Video, and `hreflang` namespaces inside a single `<url>` container:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://procrm.com.au/blog/asd-acsc-alert-rmm-exploitation</loc>
    <lastmod>2026-08-25T08:00:00+10:00</lastmod>

    <!-- Google News Extension (<48h breaking news) -->
    <news:news>
      <news:publication>
        <news:name>PRO CRM Intelligence</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>2026-08-25T08:00:00+10:00</news:publication_date>
      <news:title>ASD ACSC Alert: Active Exploitation of RMM Platforms</news:title>
    </news:news>

    <!-- Google Image Extension -->
    <image:image>
      <image:loc>https://procrm.com.au/assets/news/rmm-patching-hero.webp</image:loc>
    </image:image>

    <!-- Google Video Extension -->
    <video:video>
      <video:thumbnail_loc>https://procrm.com.au/assets/thumbs/rmm-walkthrough.jpg</video:thumbnail_loc>
      <video:title>Zero-Trust RMM Patching Walkthrough</video:title>
      <video:description>Engineering guide on isolating management consoles and rotating API tokens.</video:description>
      <video:player_loc>https://procrm.com.au/videos/rmm-security.html</video:player_loc>
      <video:duration>360</video:duration>
      <video:publication_date>2026-08-25T08:00:00+10:00</video:publication_date>
      <video:family_friendly>yes</video:family_friendly>
    </video:video>

    <!-- Localized Alternate Version (hreflang) -->
    <xhtml:link rel="alternate" hreflang="en-au" href="https://procrm.com.au/blog/asd-acsc-alert-rmm-exploitation"/>
  </url>
</urlset>
```

---

## 🚦 6. HTTP Status Code Handling & Crawl Behaviors

| HTTP Status Code | Classification | Googlebot & Search Indexing Behavior | Engineering Requirement |
| :--- | :--- | :--- | :--- |
| **`200 OK`** | Success | Passed to indexing pipeline. **Does not guarantee indexing.** If empty or broken, flagged as `soft 404`. | Ensure complete DOM rendering and non-empty content. |
| **`301` / **`308`** | Permanent Redirect | Google follows up to 10 hops. Strong canonical signal transferring signals to destination. | Use for all permanently moved URLs or slug renames. |
| **`302` / **`307`** | Temporary Redirect | Followed by crawler, but weak signal. Original URL remains indexed. | Use only for short-term maintenance redirects. |
| **`304 Not Modified`** | HTTP Cache Revalidation | Signals content is unchanged. Saves bandwidth and preserves crawl budget without re-downloading body. | Implement `ETag` and `If-None-Match` on static and article assets. |
| **`404` / **`410`** | Not Found / Gone | URL is immediately excluded or dropped from index. Crawl frequency decreases. | Return true `404`/`410` for deleted pages. Never return `200 OK` on custom 404 pages. |
| **`429`** | Too Many Requests | Treated as server overload (equivalent to 5xx). Prompts crawlers to slow down immediately. | Use temporarily during traffic spikes; never leave >2 days. |
| **`500` / **`502`** / **`503`** | Server Error | Crawl rate decreases proportionately. URLs temporarily preserved, but dropped if errors persist >48h. | Monitor host capacity; resolve backend and API timeouts immediately. |

---

## 🔌 7. Network, DNS & Firewall Resilience

Network timeouts, connection resets (`RST`), and DNS failures are treated identically to `5xx` server errors, causing immediate crawling slowdowns and index de-listing within days.

### Diagnostic Checklist:
1. **Firewall Rules**: Ensure edge firewalls (Cloudflare, AWS WAF, NGINX) never block [Google published IP ranges](https://developers.google.com/static/crawling/ipranges/common-crawlers.json). Allow both `UDP` and `TCP` for DNS and HTTP traffic.
2. **DNS Health**: Validate `A`, `CNAME`, and `NS` records using `dig +nocmd example.com a +noall +answer`.
3. **DNS Cache Flush**: After DNS record migrations, purge [Google Public DNS Cache](https://developers.google.com/speed/public-dns/faq#update_cache) to accelerate global propagation.

---

## 🤖 8. Google Crawlers & Cryptographic Web Bot Auth (RFC 9421)

| Crawler Type | Description | Reverse DNS Mask | Published IP List |
| :--- | :--- | :--- | :--- |
| **Common Crawlers** | Search indexing spiders (`Googlebot Smartphone`, `Googlebot Desktop`). Obeys `robots.txt`. | `crawl-***.googlebot.com`<br>`geo-crawl-***.geo.googlebot.com` | [`common-crawlers.json`](https://developers.google.com/static/crawling/ipranges/common-crawlers.json) |
| **Special-Case Crawlers** | Product-specific crawlers (`AdsBot`, abuse verification). | `rate-limited-proxy-***.google.com` | [`special-crawlers.json`](https://developers.google.com/static/crawling/ipranges/special-crawlers.json) |
| **User-Triggered Fetchers** | On-demand tools (`Google Site Verifier`, `Google-Agent`, `Google-GeminiNotebook`). | `***.gae.googleusercontent.com`<br>`google-proxy-***.google.com` | [`user-triggered-fetchers.json`](https://developers.google.com/static/crawling/ipranges/user-triggered-fetchers.json)<br>[`user-triggered-agents.json`](https://developers.google.com/static/crawling/ipranges/user-triggered-agents.json) |

* **Cryptographic Verification**: AI agent requests include `Signature-Agent: g="https://agent.bot.goog"`. Public keys are retrieved from `https://agent.bot.goog/.well-known/http-message-signatures-directory` and validated per [RFC 9421](https://datatracker.ietf.org/doc/html/rfc9421).
* **Weekly Changelog Audits**: Maintain weekly monitoring of the [Google Crawling Changelog](https://developers.google.com/crawling/docs/changelog) to adapt to new user agents and IP blocks.

---

## 🧠 9. Generative AI Search & AI Overviews Optimization

Google Search grounds generative AI features (AI Overviews, AI Mode) using **Retrieval-Augmented Generation (RAG)** and **Query Fan-Out**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               GENERATIVE AI SEARCH OPTIMIZATION (RAG & QUERY FAN-OUT)                  │
├──────────────────────────────────────┬─────────────────────────────────────────────────┤
│ Core Google Strategy                 │ Technical Implementation in Our Blogs           │
├──────────────────────────────────────┼─────────────────────────────────────────────────┤
│ • Retrieval-Augmented Gen (RAG)      │ Ground answers in hard data, official ASD alerts,│
│                                      │ RBA monetary statistics, and CVE patch guides   │
│ • Query Fan-Out Matching             │ Structure articles to answer primary + multi-   │
│                                      │ dimension secondary questions (3 punchy points) │
│ • Non-Commodity Content              │ Provide proprietary engineering fixes & broker  │
│                                      │ strategies rather than generic recycled advice   │
│ • Semantic Accessibility Tree        │ Clean semantic HTML (`<article>`, `<header>`,   │
│                                      │ `<section>`) readable by autonomous AI agents   │
└──────────────────────────────────────┴─────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Mythbusting AI Optimization (Things We Ignore)**:
> * ❌ **No `llms.txt` files**: Google Search ignores `llms.txt` files for search indexing.
> * ❌ **No Artificial Chunking**: Do not chop content into awkward micro-snippets; write natural, structured sections.
> * ❌ **No "AEO/GEO" Hacks**: Generative visibility is rooted entirely in foundational, high-quality technical SEO.

---

## 🏆 10. E-E-A-T & "Who, How, Why" Editorial Framework

Especially critical for **YMYL (Your Money or Your Life)** domains like Cybersecurity and Mortgage Finance:

* **Who (Authorship & Authority)**: Every article features clear author bylines (e.g. *Robin Bakshi, Principal Cyber Architect / Accredited MFAA Broker*), job titles, and verified publisher organizations.
* **How (Methodology & Process)**: Transparent disclosures on testing, data aggregation from official authorities (ASD ACSC, RBA, APRA, Salesforce), and verified engineering remediation workflows.
* **Why (People-First Purpose)**: Content created exclusively to empower Australian businesses and homeowners with actionable solutions, never just to harvest keyword impressions.

---

## 🌐 11. IETF Internet Standards Early Adoption Policy (Competitive Edge)

We actively monitor and adopt emerging standards developed by the **IETF (Internet Engineering Task Force)**—specifically from working groups like `webbotauth`, `httpbis`, and `aipref`—to maintain a strategic, technical advantage over competitors.

> [!TIP]
> **Core Principle**: By adopting standards produced at the IETF (such as **HTTP Message Signatures [RFC 9421]**, **HTTP/2 caching protocols**, and **structured schema**) as early adopters, our platforms gain **faster indexing, stronger security, and better search rankings** than competitors.

---

## 💡 12. Direct Benefits to Finnova, PRO CRM, EZ Consultants & EZ Mortgage Broker

```
┌───────────────────────────────────────────────┬────────────────────────────────────────────────────────┐
│ Technical Pillar                              │ Direct Business & Platform Benefit                     │
├───────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 1. Zero Soft-404s & Proper 301/304 Statuses   │ Conserves 100% of crawl budget for new breaking news;  │
│                                               │ eliminates indexing drop-offs and wasted server load.  │
├───────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 2. Cryptographic Web Bot Auth & IP Whitelists │ Prevents malicious scrapers from draining server power │
│                                               │ while guaranteeing Googlebot & AI agents 0% blockage. │
├───────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 3. RAG Grounding & Non-Commodity Content      │ High probability of being cited as the primary source  │
│                                               │ in Google AI Overviews and enterprise search queries. │
├───────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 4. Combined Multi-Sitemaps (News, Image, Vid) │ Immediate indexing for breaking news (<48h) and media  │
│                                               │ rich snippets across Google News & Video carousels.    │
├───────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 5. IETF Standards Early Adoption (RFC 9421)   │ Delivers a 6–18 month architectural head start over    │
│                                               │ industry competitors in indexation speed and trust.    │
└───────────────────────────────────────────────┴────────────────────────────────────────────────────────┘
```
