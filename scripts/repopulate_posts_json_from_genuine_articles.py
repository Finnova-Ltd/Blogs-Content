#!/usr/bin/env python3
"""
Repopulate posts.json from the 294 Genuine Blog Articles
FINNOVA / EZMORTGAGE BROKERAGE • METADATA PURITY ENGINE
"""

import os
import re
import json
import glob
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime

AEST = ZoneInfo("Australia/Melbourne")
BASE_DIR = Path(__file__).resolve().parent.parent
EZ_DIR = Path("/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker")
BLOG_DIR = EZ_DIR / "pages" / "blog"

def rebuild():
    html_files = sorted(list(BLOG_DIR.glob("*.html")), key=lambda p: p.stat().st_mtime, reverse=True)
    posts = []

    for f in html_files:
        if f.name in ["index.html"]:
            continue
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                html = fp.read()

            slug = f.stem
            # Extract Title
            m_title = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
            title = m_title.group(1).split("|")[0].strip() if m_title else slug.replace("-", " ").title()

            # Extract Category
            m_cat = re.search(r'class="badge-category"[^>]*>(.*?)</span>', html)
            category = m_cat.group(1).strip() if m_cat else "Home Loans"

            # Extract Date
            m_date = re.search(r'class="article-date"[^>]*>(.*?)</span>', html)
            if not m_date:
                m_date = re.search(r'—\s*([0-9]{1,2}-[A-Za-z]{3}-[0-9]{4})', html)
            date_str = m_date.group(1).strip() if m_date else datetime.fromtimestamp(f.stat().st_mtime, tz=AEST).strftime("%d-%b-%Y")

            # Extract first paragraph / excerpt
            m_p = re.search(r'<p class="font-editorial"[^>]*>(.*?)</p>', html, re.DOTALL)
            excerpt = re.sub(r'<[^>]+>', '', m_p.group(1)).strip() if m_p else "Compare accredited Australian mortgage rates and borrowing capacity."
            if len(excerpt) > 160:
                excerpt = excerpt[:157] + "..."

            # Hero image
            m_img = re.search(r'<img[^>]+src="([^">]+)"[^>]+alt="Hero', html)
            image_url = m_img.group(1) if m_img else "/assets/luxury-home-refinance-hero-OeZc7gD4.webp"

            posts.append({
                "slug": slug,
                "title": title,
                "category": category,
                "date": date_str,
                "publishedDate": date_str,
                "excerpt": excerpt,
                "content": excerpt,
                "image": image_url,
                "url": f"/pages/blog/{slug}.html"
            })
        except Exception as e:
            print(f"Error parsing {f.name}: {e}")

    print(f"Rebuilt {len(posts)} genuine articles into posts.json")
    with open(BASE_DIR / "posts.json", "w") as fp:
        json.dump(posts, fp, indent=2)
    with open(EZ_DIR / "posts.json", "w") as fp:
        json.dump(posts, fp, indent=2)

if __name__ == "__main__":
    rebuild()
