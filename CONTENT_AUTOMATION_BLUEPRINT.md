# 🚀 Reusable Content Publishing & Social Syndication Engine

A production-grade, fully automated content publishing engine that creates **Top-Tier High-Fidelity Articles (Image 2 Format)**, curates **Image 1 Grid Hubs**, fetches **high-resolution images from Pexels / Pixabay / Unsplash**, and syndicates automatically via **Make.com & RSS to Facebook, LinkedIn, and Google Business Profile**.

---

## 🌟 Key Architectural Features

1. **🎨 High-Fidelity Article Format (Image 2)**:
   * **Hero Header Banner**: Dark navy overlay, crisp `#ffffff` titles with deep text-shadows, social share pills (FB, 𝕏, LinkedIn, WhatsApp), and metadata.
   * **Expandable Accordion Sections**: 5 responsive interactive accordions containing structured comparison tables, feature checklists, and broker tips.
   * **Sticky Sidebar Ecosystem**:
     * **Author Profile Card**: Avatar, 5-star Google rating (`★★★★★ 14`), booking buttons (`Book Appointment`, `Send Message`, `Contact Card`).
     * **Crimson Highlights Box**: Target bullet points (`◉`), date badge, and instant smooth-scroll `Top of Article ↑`.
     * **15-Second Vertical Google Reviews Carousel**: Smooth top-to-bottom vertical slide animation cycling real reviews every 15 seconds with a visual progress bar and hover-pause.
     * **Mortgage Calculators Widget** & **Sticky CTA Card**.
   * **Mobile Optimized**: Flexible re-ordering so the Crimson Highlights box places directly below the hero header before the article content on mobile devices ($\le 1024\text{px}$).

2. **📰 Curated Blog Hub (Image 1 Grid)**:
   * 3-column responsive card feed with category filters and real-time counter pills.
   * Daily Top 4 Article Slotting directly at the top of the feed grid.

3. **📸 Image Automation (Pexels, Pixabay, Unsplash & Canva)**:
   * Supported through [`scripts/fetch_pexels_pixabay_images.py`](file:///scripts/fetch_pexels_pixabay_images.py).
   * Automatically resolves high-resolution landscape images via Pexels API, Pixabay API, or curated Australian finance fallbacks.

4. **⚡ Automated Syndication Pipeline (Make.com + RSS + Cron)**:
   * 4x daily triggers via GitHub Actions (`0 20,2,8,14 * * *` AEST).
   * Generates standard `rss.xml` and `feed.xml`.
   * Webhook connection triggers **Make.com** scenarios for automatic posting to **Facebook Pages, LinkedIn Company Pages, and Google Business Profiles**.

---

## 🛠️ Step-by-Step Implementation on Any New Project

### Step 1: Clone or Copy the Blueprint Engine
Copy the following directories into your new repository:
* `scripts/` (Image fetcher, article generator, RSS synthesizer)
* `css/style.css` (Contains the Image 2 article layout & 15s reviews carousel styles)
* `js/main.js` (Contains `initSidebarReviewsCarousels` and accordion handlers)
* `templates/` (Raw HTML templates for articles and blog hubs)
* `.github/workflows/daily_rss_publisher.yml` (Scheduled automation pipeline)

### Step 2: Configure Your Brand Settings
Update `content_engine_config.example.json` with your project's brand name, domain, phone, address, and author credentials:
```json
{
  "brand": {
    "name": "Your Brand Name",
    "domain": "https://yourbrand.com.au",
    "phone": "1300 000 000",
    "email": "hello@yourbrand.com.au"
  }
}
```

### Step 3: Add API Keys to GitHub Secrets (Optional)
In your repository settings under **Settings > Secrets and variables > Actions**:
* `PEXELS_API_KEY`: Your Pexels API key.
* `PIXABAY_API_KEY`: Your Pixabay API key.
* `MAKE_WEBHOOK_URL`: Your Make.com custom webhook URL for instant multi-channel social posting.

### Step 4: Run the Image Fetcher & Article Generator
```bash
# 1. Fetch images for a topic
python3 scripts/fetch_pexels_pixabay_images.py "Sydney property investment" "hero-banner.jpg"

# 2. Generate daily articles & update hub
python3 scripts/generate_top_daily_articles.py

# 3. Build RSS and deploy
python3 scripts/generate_rss_feed.py
npm run build
```

---

## 🔗 Make.com Social Syndication Setup Guide

1. **Trigger**: RSS Watch New Items (pointing to `https://yourdomain.com.au/rss.xml`) OR Custom Webhook.
2. **Action 1 (Facebook)**: Create Page Post with `title`, `summary`, `url`, and `image`.
3. **Action 2 (LinkedIn)**: Create Share with rich article preview card.
4. **Action 3 (Google Business Profile)**: Create What's New post with `Call Now` button linked to your phone number.

---
*Maintained by Finnova Ltd / EZ Mortgage Broker Engineering Team.*
