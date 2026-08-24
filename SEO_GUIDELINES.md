# 🔍 Google Search Essentials & Master Technical SEO Specification (`SEO_GUIDELINES.md`)

This comprehensive engineering specification codifies official guidelines from **Google Search Central** (Search Essentials, Webmaster Guidelines, Crawler Infrastructure, and Sitemap Protocols) across all Finnova digital properties:
* `procrm.com.au`
* `ezconsultants.com.au`
* `finnova.org.au`
* `ezmortgagebroker.com.au`

---

## 🏛️ 1. The Three Stages of Google Search

```
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│       1. CRAWLING         │ ───► │        2. INDEXING        │ ───► │     3. SERVING RESULTS    │
│  Googlebot downloads text,│      │ Analyzes text, rendered   │      │ Matches search intent,    │
│  images, videos & renders │      │ DOM, JSON-LD, canonical   │      │ location & device. Serves │
│  JavaScript via Chrome.   │      │ clustering & signals.     │      │ rich snippets & links.    │
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘
```

1. **Crawling (URL Discovery & Fetching)**:
   * Google discovers URLs via standard crawlable `<a href="...">` links, XML sitemaps, and RSS/Atom feeds.
   * Renders the page using an evergreen, modern headless Chrome browser. All client-side JavaScript, CSS, and dynamic DOM states are executed during crawling.
2. **Indexing (Analysis & Canonical Selection)**:
   * Analyzes textual content, `<title>`, meta descriptions, structured data (JSON-LD), headings, and visual media.
   * Clusters near-duplicate URLs and elects a single **Canonical URL**.
3. **Serving Search Results (Relevancy & UI Features)**:
   * Dynamically renders Title Links, Snippets, Visual Breadcrumbs, Rich Snippet Badges, and Carousels based on query context, location, and device type.

---

## 🤖 2. Googlebot Technical Specifications & Crawl Requirements

* **Primary Crawler**: **Googlebot Smartphone** (Mobile-First Indexing). Desktop crawler is secondary.
* **File Size Limits**:
  * **HTML / Web Pages**: Googlebot fetches and parses up to **2 MB** of uncompressed text/HTML per resource.
  * **PDF Files**: Up to **64 MB**.
* **Rendering & Resources**:
  * All critical assets (CSS, JS bundles, fonts, API endpoints) **must never be disallowed** in `robots.txt`.
  * If CSS/JS is blocked, Googlebot cannot render the layout and may flag the page with indexing errors or `soft 404`.
* **Transfer Protocols & Compression**:
  * Googlebot supports **HTTP/1.1** and **HTTP/2**.
  * Supported encodings: `Brotli (br)`, `gzip`, and `deflate`.
* **Verification**:
  * Verified via reverse DNS lookup matching `*.googlebot.com` or official Google IP CIDR ranges.

---

## ⚡ 3. Crawl Efficiency, Server Load & HTTP Caching Protocol

### A. HTTP Caching Headers (`ETag` & `Last-Modified`)
Googlebot supports heuristic HTTP caching to minimize unnecessary server bandwidth:
* **`ETag` and `If-None-Match`**: Googlebot sends `If-None-Match` with previously fetched ETags. If unchanged, our servers return **`304 Not Modified`** (zero response body).
* **`Last-Modified` and `If-Modified-Since`**: Dates must strictly follow RFC 9110 format (`Weekday, DD Mon YYYY HH:MM:SS GMT`).
* **`Cache-Control: max-age=...`**: Specify expected cache freshness.

### B. Accurate Status Codes & Soft 404 Prevention
* **Never return `200 OK` on broken, empty, or missing content pages** (which triggers a `soft 404` penalty).
* **Removed Content (No replacement)**: Return HTTP **`404 Not Found`** or **`410 Gone`** with a user-friendly custom 404 template.
* **Moved Content**: Return HTTP **`301 Permanent Redirect`** directly to the target URL (avoid redirect chains).
* **Emergency Host Load / Server Maintenance**:
  * Return **`503 Service Unavailable`** or **`429 Too Many Requests`** temporarily. Googlebot automatically slows down and retries for 1–2 days.
  * *Warning*: Never leave `503` or `429` for >2 days or URLs will be dropped from the index.

---

## 🗺️ 4. Multi-Sitemap Architecture & Protocols

Google accepts standard XML sitemaps, sitemap index files, and domain-specific extensions up to **50,000 URLs / 50 MB** per uncompressed file.

### A. Master Sitemap Index (`sitemap_index.xml`)
Combines specialized sub-sitemaps into a single discovery endpoint:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://procrm.com.au/sitemap-main.xml</loc>
    <lastmod>2026-08-25T08:00:00+10:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://procrm.com.au/sitemap-news.xml</loc>
    <lastmod>2026-08-25T08:00:00+10:00</lastmod>
  </sitemap>
</sitemapindex>
```

### B. Google News Sitemap (`<news:news>`)
Used for articles published within the last 48 hours:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  <url>
    <loc>https://procrm.com.au/blog/asd-acsc-alert-cicd-pipeline-exploitation-cve-2026-63077</loc>
    <news:news>
      <news:publication>
        <news:name>PRO CRM Intelligence</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>2026-08-25T08:00:00+10:00</news:publication_date>
      <news:title>ASD ACSC Alert: Active CI/CD Platform Exploitation in Australia</news:title>
    </news:news>
  </url>
</urlset>
```

### C. Image & Video Sitemaps
* **Image Sitemaps** (`xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"`):
  * `<image:image><image:loc>https://.../cover.webp</image:loc></image:image>`
* **Video Sitemaps** (`xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"`):
  * Must specify `<video:thumbnail_loc>`, `<video:title>`, `<video:description>`, and either `<video:content_loc>` or `<video:player_loc>`.

### D. `<lastmod>` Rule of Truth
* Googlebot uses `<lastmod>` **only if it is verifiably accurate**.
* Do not update `<lastmod>` for minor copyright updates; update only when significant editorial content, structured data, or links have changed.

---

## 💎 5. On-Page Content, Link Architecture & Structure

1. **People-First Helpful Content**:
   * Solve genuine user problems with clear engineering and advisory solutions.
   * Structure with 1x `<h1>` (matching the title topic), clean `<h2>` sections, and concise bullet points.
2. **Keyword Placement (Expect Reader Queries)**:
   * Front-load primary search terms in the first sentence and within the `<h1>` title.
   * Zero keyword stuffing: write naturally with rich vocabulary.
3. **Crawlable Standard Hyperlinks**:
   * Always use `<a href="/target-path">` (never `<span onclick="...">` or javascript void pseudo-links).
   * **Descriptive Anchor Text**: State clearly what the destination page contains (e.g., *"view our [First Home Guarantee Eligibility Guide](file:///...)"*).
4. **Link Annotations**:
   * Use `rel="noopener noreferrer"` on external links.
   * Add `rel="nofollow"` to unverified user-generated links or sponsored mentions.

---

## 🏷️ 6. Rich Results & Schema.org JSON-LD

Every blog post, advisory, and market insight must inject complete JSON-LD:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "ASD ACSC Alert: Active Exploitation of CI/CD Platforms in Australia",
  "description": "ASD's ACSC warns of active exploitation of build servers (CVE-2026-63077). Step-by-step remediation guide.",
  "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1600&q=80",
  "datePublished": "2026-08-25T08:00:00+10:00",
  "dateModified": "2026-08-25T08:00:00+10:00",
  "author": {
    "@type": "Person",
    "name": "Robin Bakshi",
    "jobTitle": "Principal Cyber Architect",
    "worksFor": {
      "@type": "Organization",
      "name": "PRO CRM Australia"
    }
  },
  "publisher": {
    "@type": "Organization",
    "name": "PRO CRM",
    "logo": {
      "@type": "ImageObject",
      "url": "https://procrm.com.au/assets/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://procrm.com.au/blog/asd-acsc-alert-cicd-pipeline-exploitation-cve-2026-63077"
  }
}
</script>
```

---

## 🚫 7. Google Spam Policy Compliance (Zero Tolerance)

1. **No Scraped Content**: All articles must be written in our own words with original engineering analysis.
2. **No Deceptive Cloaking**: What Googlebot renders must match 100% of human user viewports.
3. **No Obsolete `<meta name="keywords">`**: Google Search completely ignores keywords meta tags.
4. **No Intrusive Interstitials**: Zero blocking popups or obstructive modals on mobile viewports.
