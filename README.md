# 🚀 Finnova Universal Native JS Blog & Studio Engine

[![Native JS](https://img.shields.io/badge/Architecture-Pure_Vanilla_JS_%26_HTML5-0176d3?style=for-the-badge&logo=javascript)](https://finnova.org.au)
[![No WordPress](https://img.shields.io/badge/Dependencies-Zero_PHP_%2F_Zero_WordPress-059669?style=for-the-badge)](https://github.com/Finnova-Ltd/Blogs-Content)
[![Standalone CMS](https://img.shields.io/badge/CMS-Standalone_%26_Portable-388bfd?style=for-the-badge)](https://github.com/Finnova-Ltd/Blogs-Content)

A **100% Native Client-Side JavaScript & HTML5 Engine** that re-engineers and improves upon the best features of **Yoast SEO**, **Gutenberg Block Editors**, and **GitBook Workspaces** — built entirely without PHP, WordPress, or external framework bloat.

---

## 💡 How We Engineered This Native Code Engine

While classic Yoast SEO requires PHP/WordPress and GitBook requires cloud SaaS subscriptions, **we engineered a native, lightweight JavaScript/HTML5 system** directly inside [`index.html`](./index.html) and [`posts.json`](./posts.json):

```
                       ┌───────────────────────────────────────────────────────────┐
                       │          FINNOVA NATIVE ENGINE (index.html)               │
                       └─────────────────────────────┬─────────────────────────────┘
                                                     │
         ┌───────────────────────────────────────────┼───────────────────────────────────────────┐
         │                                           │                                           │
 ┌───────▼────────────────────────┐         ┌────────▼────────────────────────┐         ┌───────▼────────────────────────┐
 │   Gutenberg Block Studio       │         │   Yoast-Style SEO Engine        │         │   GitBook Workspace Layout     │
 ├────────────────────────────────┤         ├────────────────────────────────┤         ├────────────────────────────────┤
 │ • Left Inserter Drawer         │         │ • 4-Tab Real-time Assessment   │         │ • 3-Column Studio Workspace    │
 │ • TEXT, MEDIA, DESIGN, WIDGETS │         │ • Flesch Readability Score     │         │ • Inline /Slash Popover        │
 │ • Click-to-insert snippet HTML │         │ • Snippet & Replacement Pills  │         │ • Auto Table of Contents       │
 │ • Pre-configured layout blocks │         │ • Connected JSON-LD @graph     │         │ • Sticky Social Share Bar      │
 └────────────────────────────────┘         └────────────────────────────────┘         └────────────────────────────────┘
```

---

## ⚡ Key Technical Innovations We Built

### 1. Native Yoast-Grade SEO & Readability Engine (Pure JS)
- Re-architected Yoast's PHP analysis rules into a zero-latency JavaScript evaluator (`updateYoastAnalysis()`).
- Calculates keyphrase density, H1 keyphrase placement, first paragraph presence, meta description length (120–156 chars), title length (50–60 chars), and Flesch Reading Ease scores instantly as authors type.
- Generates dynamic Schema.org JSON-LD structured data trees (`updateYoastSchemaGraph()`) connecting `Organization`, `WebPage`, `Article`, `BreadcrumbList`, and `LocalBusiness` nodes into `<script type="application/ld+json">`.

### 2. Native Inline `/Slash` Command Inserter
- Built a keyboard-friendly slash listener (`handleEditorSlashCommand(event)`) in native JS.
- Typing `/` anywhere in the editor body opens an inline block menu filtering blocks by keyword for mouse-free authoring.

### 3. GitBook 3-Column Workspace Architecture
- **Column 1**: Left Gutenberg Block & Pattern library inserter drawer.
- **Column 2**: Focused typography canvas with inline callouts (`💡 Key Takeaway`), details accordions, and custom block templates.
- **Column 3**: Right Yoast SEO assessment tabs (`🔴 SEO`, `🟢 Readability`, `▦ Schema`, `⇘ Social`).

### 4. Local SEO & Location Archive CPT (`/locations`)
- Built an interactive store locator and locations archive page (`#page-locations`) displaying community hubs (Melbourne CBD HQ, Geelong, Ballarat) with latitude/longitude coordinates, opening hours, directions, and GeoJSON sitemap outputs.

---

## 🛠️ Repository Code Files

| File | Type | Description |
|------|------|-------------|
| 🛠️ [`index.html`](./index.html) | **Native Application Engine** | Full single-page application containing our custom Gutenberg Inserter, Yoast SEO Analysis Engine, GitBook Studio, and Local SEO Store Locator. |
| 📄 [`posts.json`](./posts.json) | **Headless Content Store** | Master JSON database storing all published articles, guides, and knowledge base entries. |
| 📘 [`README.md`](./README.md) | **Documentation** | Technical overview and integration instructions. |

---

## 🧰 How to Use This Engine in Other Projects

Because this engine is **100% native JavaScript and HTML5**, you can drop it into any project:

```javascript
// Fetch articles directly from this single-source-of-truth JSON database
fetch('https://cdn.jsdelivr.net/gh/Finnova-Ltd/Blogs-Content@main/posts.json')
  .then(res => res.json())
  .then(posts => {
    // Render posts in your web project
  });
```

---

## 🔒 Maintenance
Maintained by the **Finnova Ltd Digital & Engineering Team**.  
Contact: `info@finnova.org.au` · Production Site: [finnova.org.au](https://finnova.org.au)

*Last updated: August 2026*
