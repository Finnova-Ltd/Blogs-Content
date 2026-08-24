# 🔍 Google Search Central Master SEO Standards & Implementation Guide (`SEO_GUIDELINES.md`)

This document synthesizes official guidelines from **Google Search Central (Search Essentials & SEO Starter Guide)** to ensure maximum organic discovery, rich search result eligibility, and top-tier search performance across all Finnova digital properties (`procrm.com.au`, `ezconsultants.com.au`, `finnova.org.au`, `ezmortgagebroker.com.au`).

---

## 🏛️ 1. Technical Crawling & Indexation Standards

### A. Descriptive, Human-Readable URLs
* Use clean, lowercase, hyphen-separated keywords reflecting the topic hierarchy:
  * ✅ `https://ezmortgagebroker.com.au/pages/blog/first-home-buyers-grant-2026-guide.html`
  * ❌ `https://example.com/blog/2026?id=892374&post=true`
* Group topically similar content within logical directories (`/pages/blog/`, `/services/`, `/loans/`).

### B. Canonicalization & Duplicate Content Elimination
* Every single HTML page must declare a self-referencing canonical tag in the `<head>` to prevent URL split-indexing:
  ```html
  <link rel="canonical" href="https://procrm.com.au/blog/asd-acsc-alert-cicd-pipeline-exploitation-cve-2026-63077" />
  ```

### C. XML Sitemaps & Robots.txt
* Keep `sitemap.xml` continuously updated with `<lastmod>`, `<changefreq>`, and `<priority>`.
* Ensure `robots.txt` explicitly allows search crawlers to access CSS, JavaScript, and asset files needed to render pages as users see them.

---

## 🎨 2. Search Appearance & Snippet Optimization

### A. Title Links (`<title>`)
* **Format**: `[Primary SEO Keyword / Actionable Topic] | [Brand Name] Australia`
* **Length**: 50–60 characters (to avoid snippet truncation).
* **Rule**: Must be unique to every single page and accurately reflect the primary `<h1>` topic.

### B. Meta Descriptions (`<meta name="description">`)
* **Length**: 140–155 characters.
* **Content**: Succinct, engaging summary incorporating the primary keyword and an active call to action (e.g., *"Learn how to...", "Read our expert analysis on..."*).
* **Rule**: Never use duplicate meta descriptions across different blog posts.

### C. Open Graph (OG) & Twitter Cards
* Pre-populate complete social metadata tags on every page for rich previews across LinkedIn, Twitter/X, and Facebook:
  ```html
  <meta property="og:title" content="..." />
  <meta property="og:description" content="..." />
  <meta property="og:image" content="https://.../cover.jpg" />
  <meta property="og:url" content="https://..." />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  ```

---

## 🌟 3. Schema.org Structured Data (JSON-LD)

To qualify for Google Rich Results, carousels, and visual breadcrumbs, every article must embed structured data in the `<head>` or body:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "ASD ACSC Alert: Active CI/CD Platform Exploitation in Australia",
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

## 🖼️ 4. Image Optimization & Visual Search

* **Descriptive Alt Text**: Every `<img>` tag must include contextual `alt` text explaining what the image portrays in relation to the article (e.g., `alt="Salesforce Data Cloud Zero-Copy bi-directional federation architecture diagram"`).
* **Next-Gen Formats & Dimensions**: Use WebP or modern compressed formats with explicit `width` and `height` (or aspect-ratio CSS) to prevent Cumulative Layout Shift (CLS).
* **Contextual Placement**: Place images directly adjacent to relevant paragraphs to help Google understand context.

---

## 🔗 5. Hyperlink Integrity & Descriptive Anchor Text

* **Meaningful Anchor Text**: Never write *"click here"* or *"read more"*. Use descriptive keyword phrases:
  * ✅ *"Review our [First Home Guarantee Eligibility Guide](file:///...)"*
  * ❌ *"For more info [click here](file:///...)"*
* **Secure Outbound Annotations**: Add `rel="noopener noreferrer"` for external links, and `rel="nofollow"` for unverified external user sources.

---

## 🚫 6. What Google Penalizes (Things We NEVER Do)

1. **No Keyword Stuffing**: Never unnaturally repeat keywords. Write naturally for the reader.
2. **No Obsolete Meta Keywords**: Google Search completely ignores `<meta name="keywords">`.
3. **No Scraped / Low-Effort Content**: Always rewrite and synthesize news in our own words with practical engineering and financial insights.
4. **No Hidden Text or Deceptive Cloaking**: What the Googlebot crawler sees must match 100% of what human users see.
