# Finnova Ltd — Blog & Knowledge Base Content

This repository is the **single source of truth** for all articles, blog posts, and knowledge base entries published on [finnova.org.au](https://finnova.org.au).

The website fetches articles directly from `posts.json` in this repo on every page load — no build step or deployment required.

---

## ✍️ How to Add or Edit an Article

### Option 1 — Edit in GitHub (easiest)
1. Open [`posts.json`](./posts.json) in this repo
2. Click the ✏️ **Edit** pencil icon in the top-right
3. Add your article following the format below
4. Click **Commit changes** → the website updates within minutes

### Option 2 — Clone and edit locally
```bash
git clone https://github.com/Finnova-Ltd/Blogs-Content.git
# Edit posts.json
git commit -am "Add article: <your article title>"
git push
```

---

## 📄 Article JSON Format

Each article in `posts.json` is an object in the array:

```json
{
  "id": "unique-slug-for-url",
  "title": "Your Article Title",
  "date": "1 January 2026",
  "author": "Finnova Team",
  "excerpt": "A 1-2 sentence summary shown in the article card on the home page.",
  "image": "images/blog-volunteer.png",
  "tags": ["Inclusion", "Cyber", "Census"],
  "category": "inclusion",
  "readTime": "4 min read",
  "isHtml": true,
  "body": [
    "<p>Your article content here. Supports full HTML.</p>",
    "<h3>Section Heading</h3>",
    "<p>More content...</p>"
  ]
}
```

### Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `id` | YES | Unique slug (lowercase, hyphens). Used in URLs. |
| `title` | YES | Article headline |
| `date` | YES | Human-readable date: "10 August 2026" |
| `author` | YES | Author name |
| `excerpt` | YES | Short summary (shown in article cards) |
| `image` | YES | Use: images/blog-volunteer.png, images/blog-cyber-safety.png, or images/blog-digital-divide.png |
| `tags` | YES | Array of tag strings. Common: "Inclusion", "Cyber", "Census", "Finance" |
| `category` | YES | Options: "inclusion", "cyber", "census", "finance" |
| `readTime` | YES | e.g. "3 min read" |
| `isHtml` | YES | Set to true (body supports HTML tags) |
| `body` | YES | Array of HTML strings (each string = a paragraph/section) |
| `youtubeId` | NO | Optional YouTube video ID to embed a player |

---

## 🔒 Who can edit?

Members of the Finnova-Ltd GitHub organisation with Write access to this repo.
Contact: info@finnova.com.au

*Last updated: August 2026 · Finnova Ltd Digital Team*
