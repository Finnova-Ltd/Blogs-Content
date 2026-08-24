# 🔍 Master Technical SEO, Crawling & Indexing Specification (`SEO_GUIDELINES.md`)

This comprehensive engineering specification codifies official guidelines from **Google Search Central** (Search Essentials, Robots Exclusion Protocol RFC 9309, Crawl Budget Optimization, Multi-Sitemaps, URL Structure, Generative AI Search Optimization, User-Agent Taxonomy, and Web Bot Authentication) across all Finnova digital properties:
* `procrm.com.au` (Enterprise CRM & Cybersecurity Intelligence)
* `ezconsultants.com.au` (Cloud & Salesforce Engineering Advisory)
* `finnova.org.au` (Fintech & Digital Transformation)
* `ezmortgagebroker.com.au` (Property Finance & Mortgage Advisory)
* `ezsignature.com` (Digital Signatures, NIST Cryptography & Contract Intelligence)

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

## 📜 2. Robots Exclusion Protocol (REP / RFC 9309) & Rule Engine

Google's automated crawlers strictly obey the **Robots Exclusion Protocol (RFC 9309)**:

### A. Technical Constraints & File Properties
* **File Location**: Must reside at the website root (`https://domain.com/robots.txt`).
* **Encoding & Size**: UTF-8 plain text with a strict **500 KiB maximum file size limit**.
* **Caching Duration**: Google caches `robots.txt` for up to **24 hours**. In emergency cache updates, use Search Console's *Robots.txt Report*.

### B. HTTP Response Behavior for `robots.txt`
* **`2xx Success`**: Processed and enforced.
* **`3xx Redirection`**: Follows up to 5 hops; if redirects continue, treated as a `404` (all crawling allowed).
* **`4xx Client Errors`** (except 429): Treated as non-existent file; all crawling is permitted.
* **`5xx Server Errors`**: Crawling is halted immediately for 12 hours. If errors persist up to 30 days, Google falls back to the last cached version.

### C. Rule Precedence & Wildcards (`*` and `$`)
* **Most Specific Rule Wins**: The directive with the longest matching character length takes precedence (e.g., `allow: /folder/sub` overrides `disallow: /folder`).
* **Equal Length Conflicts**: In a tie between `allow` and `disallow` of identical length, **`allow` (least restrictive) wins**.
* **Wildcards**:
  * `*` matches 0 or more characters (e.g. `disallow: /*?*filter=`).
  * `$` designates the end of the URL string (e.g. `disallow: /*.xls$`).
* **Unsupported Directives**: Google completely ignores non-standard rules like `crawl-delay`.

---

## 📊 3. Crawl Budget Theory: Capacity Limit vs. Crawl Demand

Crawl budget is determined by two distinct factors:

```
                  ┌────────────────────────────────────────────────────────┐
                  │              GOOGLE CRAWL BUDGET EQUATION              │
                  ├────────────────────────────┬───────────────────────────┤
                  │    CRAWL CAPACITY LIMIT    │       CRAWL DEMAND        │
                  │   (Server Hostload Limit)  │     (Popularity & Value)  │
                  ├────────────────────────────┼───────────────────────────┤
                  │ • Server response time     │ • Overall page quality    │
                  │ • TTFB & network latency   │ • Update frequency        │
                  │ • Error rates (5xx, 429)   │ • Real-time user demand   │
                  │ • Resource rendering load  │ • Canonical consolidation │
                  └────────────────────────────┴───────────────────────────┘
```

### Crawl Budget Myths vs. Facts
* ❌ **Myth**: Compressing sitemaps (`.gz`) gives more crawl budget. (Fact: Googlebot still has to fetch and unpack the file).
* ❌ **Myth**: Trivial date updates make content "fresh" for higher crawl rates. (Fact: Quality and true editorial changes determine priority).
* ❌ **Myth**: `noindex` saves crawl budget. (Fact: Google must crawl the page first to find the `noindex` tag; use `robots.txt` to prevent crawling entirely).
* ❌ **Myth**: `4xx` status codes waste crawl budget. (Fact: `404` and `410` status codes are immediately dropped and not recrawled).

---

## 🔍 4. Complete Google User-Agent & Fetcher Taxonomy

Google operates distinct categories of user agents across automated spiders, ad bots, and user-triggered AI fetchers:

### A. Common Search Crawlers (Obey `robots.txt` by Default)
* **`Googlebot`**: Primary mobile (`Googlebot Smartphone`) and desktop indexing crawler.
* **`Googlebot-News`**: Dedicated crawler for Google News aggregation.
* **`Googlebot-Image`**: Image indexing and visual search.
* **`Googlebot-Video`**: Video indexing and structured duration parsing.
* **`Storebot-Google`**: Google Shopping and merchant product surface analysis.
* **`Google-InspectionTool`**: Search Console URL Inspection and Rich Results live rendering.
* **`GoogleOther` / `GoogleOther-Image` / `GoogleOther-Video`**: Internal research and R&D crawls.

### B. Special-Case Crawlers & Control Tokens
* **`Google-Extended`**: Product token in `robots.txt` enabling site owners to control whether content is used to train Gemini AI models or ground Vertex AI search without affecting Google Search ranking.
* **`Mediapartners-Google`**: Google AdSense contextual targeting crawler.
* **`AdsBot-Google` / `AdsBot-Google-Mobile`**: Ad landing page quality verifier.
* **`Google-Safety`**: Automated abuse and malware scanning (ignores `robots.txt`).

### C. User-Triggered Fetchers (Human-Initiated / Ignore `robots.txt`)
* **`Google-Agent`**: Autonomous AI agent operating on Google infrastructure upon direct user instruction (supports **Web Bot Auth RFC 9421**).
* **`Google-GeminiNotebook`**: Fetches source URLs referenced by users in Gemini Notebook.
* **`FeedFetcher-Google`**: Fetches RSS/Atom feeds for Google News and WebSub.
* **`Google-Read-Aloud`**: Text-to-speech page reader (Opt out via `<meta name="google" content="nopagereadaloud">`).
* **`GoogleMessages`**: Generates rich link previews in chat messages.
* **`Google Site Verifier`**: Fetches Search Console verification meta tokens.

---

## 🔗 5. URL Structure Standards (IETF STD 66 / RFC 3986)

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

## 🗂️ 6. Managing Faceted Navigation & Infinite URL Spaces

Faceted search and multi-parameter filtering create exponential URL permutations that exhaust crawl bandwidth:

1. **Disallow Combinations in `robots.txt`**:
   ```
   User-agent: Googlebot
   Disallow: /*?*filter=
   Disallow: /*?*sort=
   Disallow: /*?*size=
   Allow: /*?category=
   ```
2. **Use URL Fragments for UI Filtering**: Filtering via hash fragments (`/#/color=blue`) does not trigger server requests or crawl consumption.
3. **Serve True 404s on Empty Filters**: If a filter combination has zero items, return HTTP `404 Not Found` rather than an empty `200 OK` page.

---

## 🗺️ 7. Combined Multi-Sitemap Architecture (50k URLs / 50MB Limit)

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

## 🚦 8. HTTP Status Codes & Soft 404 Remediation

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

## 🧠 9. Generative AI Search & AI Overviews Optimization (RAG & Fan-Out)

Google Search grounds generative AI features (AI Overviews, AI Mode) using **Retrieval-Augmented Generation (RAG)** and **Query Fan-Out**.

* **Retrieval-Augmented Generation (RAG)**: Grounding articles in hard data (ASD ACSC CVE IDs, RBA monetary statistics, APRA reports).
* **Query Fan-Out Matching**: Structuring content to answer primary search intent + multi-dimensional secondary questions using punchy 3-bullet value lists.
* **Non-Commodity Content**: Writing original, actionable engineering and broker solutions rather than generic 101 advice.
* **Mythbusting AI Hacks**: Zero reliance on gimmicks like `llms.txt` (which Google Search ignores) or artificial micro-chunking.

---

## 🏆 10. E-E-A-T & "Who, How, Why" Editorial Framework

Especially critical for **YMYL (Your Money or Your Life)** domains like Cybersecurity and Mortgage Finance:

* **Who (Authorship & Authority)**: Every article features clear author bylines (e.g. *Robin Bakshi, Principal Cyber Architect / Accredited MFAA Broker*), job titles, and verified publisher organizations.
* **How (Methodology & Process)**: Transparent disclosures on testing, data aggregation from official authorities (ASD ACSC, RBA, APRA, Salesforce), and verified engineering remediation workflows.
* **Why (People-First Purpose)**: Content created exclusively to empower Australian businesses and homeowners with actionable solutions, never just to harvest keyword impressions.

---

## 🌐 11. IETF Internet Standards Early Adoption Policy (RFC 9421)

We actively monitor and adopt emerging standards developed by the **IETF (Internet Engineering Task Force)**—specifically from working groups like `webbotauth`, `httpbis`, and `aipref`—to maintain a strategic, technical advantage over competitors.

> [!TIP]
> **Core Principle**: By adopting standards produced at the IETF (such as **HTTP Message Signatures [RFC 9421]**, **HTTP/2 caching protocols**, and **structured schema**) as early adopters, our platforms gain **faster indexing, stronger security, and better search rankings** than competitors.

---

## 💡 12. Direct Benefits to Finnova, PRO CRM, EZ Consultants, EZ Mortgage Broker & EZ Signature

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
│ 5. Full User-Agent & REP RFC 9309 Management  │ Complete control over Vertex AI & Gemini AI model      │
│                                               │ training (`Google-Extended`) while maximizing search.  │
└───────────────────────────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 📢 13. Google Search Central Official Intelligence & 2026 Policy Enforcement

All engineering teams must continuously ingest updates from the **Google Search Central Official Blog Feed** (`https://feeds.feedburner.com/blogspot/amDG`):

### A. Search Console Platform Properties
* Enables consolidated tracking of external brand reach on **YouTube, TikTok, Instagram, and X** inside Search Console.
* Monitors how social and video assets perform across **Google Search, Discover, and Google News**.

### B. Search Generative AI Performance Reports
* Dedicated analytics dashboard in Search Console tracking brand impressions, click-through rates, and citations inside **Google AI Overviews**.

### C. Anti-"Back Button Hijacking" Spam Policy Compliance
* **Zero Browser History Manipulation**: Never trap users or block the browser's back button via malicious `history.pushState()` loops or forced redirect traps.
* **Penalty Prevention**: Google treats back button hijacking as a severe violation of its *Malicious Practices Spam Policy*, resulting in manual algorithmic demotion or de-indexing.

---

## ⚡ 14. Cloudflare Performance, Core Web Vitals (CWV) & Image Optimization Architecture

Search engines like Google factor page speed into rankings. Fast sites rank higher, maintain lower bounce rates, and convert better (Google data shows **53% of mobile visits are abandoned if a page takes longer than 3 seconds to load**).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CORE WEB VITALS (CWV) THRESHOLD BENCHMARKS                      │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ Largest Contentful Paint   │ Interaction to Next Paint   │ Cumulative Layout Shift     │
│ (LCP) — Loading Speed      │ (INP / FID) — Interactivity │ (CLS) — Visual Stability    │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ 🎯 Target: < 2.5 seconds   │ 🎯 Target: < 100 ms         │ 🎯 Target: < 0.1            │
│ • WebP / AVIF compression  │ • Minified JavaScript (Vite)│ • Explicit width & height   │
│ • Cloudflare CDN caching   │ • Minimal main-thread blocks│ • CSS aspect-ratio boxes    │
│ • High-priority hero load  │ • Pre-rendered static HTML  │ • Zero layout shift on load │
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

### A. Core Web Vitals (CWV) Implementation Checklist
1. **LCP Optimization (< 2.5s)**:
   * Serve all images in modern **WebP / AVIF** formats.
   * Add `fetchpriority="high"` on above-the-fold hero images; defer below-the-fold images via `loading="lazy"`.
   * Distribute static bundles through Cloudflare's global edge network across 335+ cities.
2. **INP & FID Optimization (< 100ms)**:
   * Use Vite / Rollup production tree-shaking and minification for JS & CSS.
   * Pre-render static HTML (`SSG`) for instant First Contentful Paint (`FCP`) and sub-second Time to Interactive (`TTI`).
3. **CLS Prevention (< 0.1)**:
   * Always declare explicit `width` and `height` attributes or CSS `aspect-ratio` on all `<img>`, `<svg>`, and video containers.
   * Reserve placeholder dimensions for dynamic widgets to eliminate visual jump during load.

### B. Cloudflare Images & Media Pipeline
* **Automatic Format Negotiation**: Cloudflare edge dynamically detects client browser capabilities and serves **AVIF** or **WebP** on-the-fly.
* **Flexible Variants**: URL-based transformations (`w=800,format=auto,quality=85`) to serve device-appropriate resolutions to mobile, tablet, and 4K desktop screens.
* **Lossy vs. Lossless Standards**: Photographic assets compressed with lossy algorithms for 70%+ file size reduction without visible perceptual degradation.

### C. Cloudflare Bot Management vs. Search Spiders
* **Verified Good Bots**: Cloudflare's automated allowlist guarantees zero false-positive blocks for verified search crawlers (`Googlebot`, `Bingbot`, `Baiduspider`, `DuckDuckBot`, `YandexBot`).
* **AI Crawler Policy**: Distinguishes between search indexing crawlers and bulk AI training scrapers (`GPTBot`, `ClaudeBot`, `Meta-ExternalAgent`), enabling granular control via `robots.txt` and Cloudflare WAF rules without impacting search indexing.


