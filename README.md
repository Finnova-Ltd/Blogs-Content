# 🚀 Universal Gutenberg, Yoast SEO & GitBook Knowledge Base CMS Engine

[![Yoast SEO Core](https://img.shields.io/badge/Yoast_SEO_Engine-robinbakshi007%2Fwordpress--seo-a0305a?style=for-the-badge&logo=wordpress)](https://github.com/robinbakshi007/wordpress-seo)
[![GitBook Workspace](https://img.shields.io/badge/GitBook_Layout-3--Column_Workspace-388bfd?style=for-the-badge&logo=gitbook)](https://gitbook.com)
[![Gutenberg Inserter](https://img.shields.io/badge/Gutenberg-Block_Inserter-000000?style=for-the-badge&logo=wordpress)](https://github.com/WordPress/gutenberg)
[![Standalone CMS](https://img.shields.io/badge/CMS_Type-Portable_%26_Reusable-059669?style=for-the-badge)](https://github.com/Finnova-Ltd/Blogs-Content)

An **independent, portable, multi-project Blog & Knowledge Base CMS engine** combining the full power of **WordPress Gutenberg Block Inserters**, **Yoast SEO Content & Schema.org Analysis**, and **GitBook 3-Column Workspace Architecture**.

Designed to be dropped seamlessly into **ANY** web application or project without complex backend dependencies.

---

## 🔗 Architecture & Source References Map

| Component Engine | Reference & Source Code Link | Architectural Function |
|------------------|------------------------------|------------------------|
| ⚙️ **Yoast SEO Engine** | [`robinbakshi007/wordpress-seo`](https://github.com/robinbakshi007/wordpress-seo) | Focus keyphrase analysis, Flesch reading score, SEO title/meta replacement variable pills (`%%title%%`, `%%excerpt%%`, etc.), Google snippet preview, and connected JSON-LD Schema.org `@graph` generation. |
| 📚 **GitBook Workspace** | [`GitBook Documentation Spec`](https://gitbook.com) | 3-column workspace design (Left block inserter, Center typography canvas, Right metadata sidebar), automated TOC, inline callout boxes, and keyboard `/slash` command inserters. |
| 🧩 **Gutenberg Inserter** | [`WordPress/gutenberg`](https://github.com/WordPress/gutenberg) | Visual Left Inserter Drawer with `TEXT`, `MEDIA`, `DESIGN`, `WIDGETS`, and `THEME` categories. |
| 💻 **Main Finnova Site** | [`PRO-CRM-AU/finnova`](https://github.com/PRO-CRM-AU/finnova) | Live production application utilizing this repository as its headless content & studio engine. |
| 🌐 **Live Website** | [finnova.org.au](https://finnova.org.au) | Live deployed website reading from `posts.json`. |

---

## 🧰 How to Use This Engine in ANY Other Project

This repository is **completely independent and reusable across multiple projects**. To embed this blog and knowledge base into a new website, use any of the options below:

### Method 1 — Load Content via CDN (1 Line of Code)
In your application's JavaScript, fetch articles directly from this repository:

```javascript
// Fetch raw blog content from this single-source-of-truth repo
fetch('https://cdn.jsdelivr.net/gh/Finnova-Ltd/Blogs-Content@main/posts.json')
  .then(res => res.json())
  .then(posts => {
    console.log('Loaded blog posts:', posts);
    // Render posts in your project UI!
  });
```

### Method 2 — Embed Full Standalone Studio & Editor (`index.html`)
Simply drop `index.html` into your project directory or host it directly. It contains:
- Complete Gutenberg Block Inserter Drawer
- Full Yoast SEO 4-Tab Sidebar (`SEO`, `Readability`, `Schema`, `Social`)
- GitBook 3-Column Reading & Authoring Canvas
- Inline `/Slash` command inserter popover

---

## ✍️ How to Edit or Add Articles

### Option 1 — Edit in GitHub UI (Easiest)
1. Open [`posts.json`](./posts.json) in this repository.
2. Click the ✏️ **Edit** pencil icon in the top-right.
3. Add your new post or update existing content.
4. Click **Commit changes** → All connected projects receive the update instantly.

### Option 2 — Use the Standalone Studio (`index.html`)
1. Open [`index.html`](./index.html) in your browser.
2. Click **Create / Edit Article** in the top navigation bar.
3. Author your content using the `/slash` command inserter and Yoast SEO assessment drawer.
4. Click **Publish** to update `posts.json`.

---

## 📄 Standardized Article Data Format

```json
{
  "id": "unique-article-slug",
  "title": "YOUR ARTICLE TITLE",
  "date": "10 August 2026",
  "author": "Author Name",
  "category": "Documentation",
  "tags": ["Tag1", "Tag2"],
  "excerpt": "A short 1-2 sentence summary shown in cards.",
  "image": "images/blog-image.png",
  "isHtml": true,
  "body": [
    "<p>Article content paragraph with HTML support...</p>",
    "<h3>Section Heading</h3>",
    "<p>More content...</p>"
  ]
}
```

---

## 📜 Credits & External References
- **Yoast SEO Core**: Derived from [`Yoast/wordpress-seo`](https://github.com/Yoast/wordpress-seo) & [`robinbakshi007/wordpress-seo`](https://github.com/robinbakshi007/wordpress-seo).
- **GitBook Specification**: Inspired by [GitBook Knowledge Base Workspace Design](https://gitbook.com).
- **Gutenberg Block Library**: Modeled on [WordPress Gutenberg Block System](https://github.com/WordPress/gutenberg).

*Maintained by Digital Engineering Team · Open for multi-project reuse*
