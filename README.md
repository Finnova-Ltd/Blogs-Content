# 📚 Finnova Ltd — Standalone Blog & Knowledge Base Content CMS

[![Website](https://img.shields.io/badge/Live_Website-finnova.org.au-0176d3?style=for-the-badge&logo=googlechrome)](https://finnova.org.au)
[![Main Code Repo](https://img.shields.io/badge/App_Code_Repo-PRO--CRM--AU%2Ffinnova-24292e?style=for-the-badge&logo=github)](https://github.com/PRO-CRM-AU/finnova)
[![Content Repo](https://img.shields.io/badge/Content_Repo-Finnova--Ltd%2FBlogs--Content-059669?style=for-the-badge&logo=gitbook)](https://github.com/Finnova-Ltd/Blogs-Content)

This repository contains **both** the standalone Gutenberg, Yoast SEO & GitBook documentation engine (`index.html`) **and** the headless JSON content store (`posts.json`) for Finnova Ltd.

---

## 🔗 Related Repository Map & Quick Links

| Resource | Description | Direct Link |
|----------|-------------|-------------|
| 🌐 **Live Website** | Production Web Application | [finnova.org.au](https://finnova.org.au) |
| 💻 **Main App Source Code** | Core Website Repository & Infrastructure | [github.com/PRO-CRM-AU/finnova](https://github.com/PRO-CRM-AU/finnova) |
| 📝 **Content & Studio Repo** | Independent CMS Engine & JSON Posts Store | [github.com/Finnova-Ltd/Blogs-Content](https://github.com/Finnova-Ltd/Blogs-Content) |
| 📄 **Raw Content Data** | Master JSON Post & Article Records | [`posts.json`](./posts.json) |
| 🛠️ **Standalone Studio App** | Independent Gutenberg + Yoast SEO Studio Engine | [`index.html`](./index.html) |

---

## 🚀 Independent Code & Engine Architecture

This repository operates as an **independent, self-contained Blog & Knowledge Base CMS**. It imports and includes:

1. **Gutenberg Block Inserter Studio (`index.html`)**:
   - Full Left Drawer Inserter (`Blocks`, `Patterns`, `Media` tabs).
   - Block categories: `TEXT`, `MEDIA`, `DESIGN`, `WIDGETS`, `THEME`.
   - Keyboard-friendly `/slash` command inserter.

2. **Yoast SEO & Schema Analysis Engine**:
   - Real-time 4-tab sidebar (`SEO`, `Readability`, `Schema`, `Social`).
   - Focus keyphrase validation, Flesch Reading Ease score, and Google Search Snippet preview.
   - Dynamic JSON-LD Schema.org `@graph` builder (`Organization`, `WebPage`, `Article`, `BreadcrumbList`).

3. **GitBook 3-Column Workspace**:
   - 3-column workspace design (Left block inserter, Center reading canvas, Right metadata sidebar).
   - Automated table of contents and inline callout blocks.

---

## ✍️ How to Add or Edit an Article

### Option 1 — Edit in GitHub UI (Easiest)
1. Open [`posts.json`](./posts.json) in this repo.
2. Click the ✏️ **Edit** pencil icon in the top-right.
3. Add your article following the JSON format below.
4. Click **Commit changes** → the live website updates automatically within minutes via CDN.

### Option 2 — Use the Standalone Studio (`index.html`)
1. Clone this repository locally or open `index.html` in your browser.
2. Click **Create / Edit Article** in the top navigation.
3. Use the Gutenberg block inserter, `/slash` commands, and Yoast SEO assessment drawer.
4. Click **Publish** to sync changes to `posts.json`.

---

## 📄 Article JSON Format Reference

```json
{
  "id": "unique-article-slug",
  "title": "YOUR ARTICLE HEADLINE",
  "date": "10 August 2026",
  "author": "Finnova Team",
  "category": "Inclusion",
  "tags": ["Digital Inclusion", "Census", "Cyber Safety"],
  "excerpt": "A 1-2 sentence summary shown in the article card on the website.",
  "image": "images/blog-digital-divide.png",
  "isHtml": true,
  "body": [
    "<p>Your paragraph text with HTML support...</p>",
    "<h3>Section Heading</h3>",
    "<p>More detailed content...</p>"
  ]
}
```

---

## 🔒 Access & Maintenance
Maintained by the **Finnova Ltd Digital & Engineering Team**.  
Contact: `info@finnova.org.au` · GitHub: [@Finnova-Ltd](https://github.com/Finnova-Ltd)

*Last updated: August 2026*
