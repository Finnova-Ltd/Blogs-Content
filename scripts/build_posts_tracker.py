#!/usr/bin/env python3
"""
Scan All 5 Websites and Compile Post.md Tracker
-----------------------------------------------
Tracks:
- Platform / Brand
- Article Title
- Post Type (Regulatory Analysis, Market Intelligence, Tech Playbook, Anti-Scam Alert)
- Published Date
- Canonical Live URL
- Media Assets (YouTube Short, Audio Podcast)
"""

import os
import shutil
import glob
import re
from datetime import datetime

POSTS_MD_PATH = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/Post.md"

# 1. Gather EZ Mortgage Broker Posts
ezm_posts = []
ezm_dir = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker/pages/blog"
if os.path.exists(ezm_dir):
    for f in sorted(os.listdir(ezm_dir)):
        if f.endswith(".html"):
            p = os.path.join(ezm_dir, f)
            with open(p, "r", encoding="utf-8") as file:
                c = file.read()
            title_m = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
            title = title_m.group(1).replace(" | EZ Mortgage Broker", "").strip() if title_m else f
            ezm_posts.append({
                "brand": "EZ Mortgage Broker",
                "domain": "ezmortgagebroker.com.au",
                "title": title,
                "type": "Market Intelligence & Lending Rates",
                "date": "25-Aug-2026",
                "url": f"https://ezmortgagebroker.com.au/pages/blog/{f}"
            })

# 2. Gather PRO CRM Posts
procrm_posts = []
procrm_blog_js = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/pages/Blog.jsx"
if os.path.exists(procrm_blog_js):
    with open(procrm_blog_js, "r", encoding="utf-8") as f:
        c = f.read()
    titles = re.findall(r'title:\s*["\'](.*?)["\']', c)
    slugs = re.findall(r'id:\s*["\'](.*?)["\']', c)
    for t, s in zip(titles, slugs):
        procrm_posts.append({
            "brand": "PRO CRM",
            "domain": "procrm.com.au",
            "title": t,
            "type": "Cyber Security & Enterprise Compliance",
            "date": "25-Aug-2026",
            "url": f"https://procrm.com.au/blog/{s}"
        })

# 3. Gather EZ Consultants Posts
ezcon_posts = []
ezcon_blog_js = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/src/pages/Blog.jsx"
if os.path.exists(ezcon_blog_js):
    with open(ezcon_blog_js, "r", encoding="utf-8") as f:
        c = f.read()
    titles = re.findall(r'title:\s*["\'](.*?)["\']', c)
    slugs = re.findall(r'id:\s*["\'](.*?)["\']', c)
    for t, s in zip(titles, slugs):
        ezcon_posts.append({
            "brand": "EZ Consultants",
            "domain": "ezconsultants.com.au",
            "title": t,
            "type": "Salesforce & AI Cloud Transformation",
            "date": "25-Aug-2026",
            "url": f"https://ezconsultants.com.au/blog/{s}"
        })

# 4. Gather EZ Signature Posts & Landing Pages
ezsig_posts = [
    {
        "brand": "EZ Signature",
        "domain": "ezsignature.com",
        "title": "Electronic Transactions Act 1999 & ISO 27001 eSignature Legality Guide",
        "type": "Digital Signatures & Legaltech Compliance",
        "date": "25-Aug-2026",
        "url": "https://ezsignature.com/electronic-signature-legality"
    },
    {
        "brand": "EZ Signature",
        "domain": "ezsignature.com",
        "title": "DocuSign Alternatives & Australian Volume-Based Pricing",
        "type": "Product Comparison & Commercial Playbook",
        "date": "25-Aug-2026",
        "url": "https://ezsignature.com/compare-us"
    }
]

# 5. Gather Finnova Posts
fin_posts = [
    {
        "brand": "Finnova Hub",
        "domain": "finnova.org.au",
        "title": "Australian Senior Digital Inclusion & Anti-Scam Verification Guide",
        "type": "Community Welfare & Financial Inclusion",
        "date": "25-Aug-2026",
        "url": "https://finnova.org.au/index.html"
    }
]

all_posts = ezm_posts + procrm_posts + ezcon_posts + ezsig_posts + fin_posts

# Generate Post.md content
md_lines = [
    "# 📋 Master Content & Publishing Tracker (`Post.md`)",
    "",
    "> Central repository index tracking all published articles, educational guides, case studies, videos, and podcasts across the Finnova network.",
    "",
    f"**Total Published Posts Tracked**: `{len(all_posts)}`  ",
    f"**Last Sync Date**: `{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}`",
    "",
    "---",
    "",
    "## 📊 Content Inventory by Brand",
    "",
    "| # | Brand / Platform | Article Title | Post Type / Category | Publish Date | Live Canonical URL | Media Assets |",
    "| :- | :--- | :--- | :--- | :--- | :--- | :--- |"
]

for idx, p in enumerate(all_posts, 1):
    short_title = p['title'][:65] + ("..." if len(p['title']) > 65 else "")
    md_lines.append(f"| {idx} | **{p['brand']}** | {short_title} | `{p['type']}` | {p['date']} | [View Article]({p['url']}) | 🎥 Short / 🎙️ Podcast |")

md_lines.extend([
    "",
    "---",
    "",
    "## 📁 Central Asset Library Mapping",
    "",
    "All reusable digital assets are synchronized in `Blogs-Content/assets/`:",
    "",
    "```",
    "Blogs-Content/assets/",
    "├── logos/                 # Official brand logo PNGs & SVGs",
    "│   ├── ezmortgagebroker-logo.png",
    "│   ├── ezsignature-logo.png",
    "│   ├── procrm-logo.png",
    "│   ├── ezconsultants-logo.png",
    "│   └── finnova-logo.png",
    "├── images/                # High-res bright hero & stock photography",
    "├── audio/                 # Generated neural voiceovers & podcast clips (.mp3)",
    "└── videos/                # Rendered 9:16 YouTube Shorts & 16:9 Landscape videos (.mp4)",
    "```",
    "",
    "### Google Drive Sync Architecture",
    "* **Local Mirror**: `/Users/robinbakshi/Documents/GitHub/Blogs-Content/assets/`",
    "* **Google Drive Cloud Target**: `Google Drive > Finnova Network Assets > {logos, images, audio, videos}`",
    "* **Automation**: Publishing scripts automatically reference `assets/logos/` and `assets/images/` to prevent duplicate downloads and maintain branding consistency."
])

with open(POSTS_MD_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

# Also make a copy as POSTS.md for standard naming
shutil.copy2(POSTS_MD_PATH, "/Users/robinbakshi/Documents/GitHub/Blogs-Content/POSTS.md")
print(f"✅ Generated Post.md and POSTS.md tracking {len(all_posts)} articles across all 5 platforms!")
