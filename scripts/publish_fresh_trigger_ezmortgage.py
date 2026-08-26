#!/usr/bin/env python3
import os
import json
import time

EZM_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
posts_path = os.path.join(EZM_DIR, "posts.json")
news_db_path = os.path.join(EZM_DIR, "data", "news_db.json")

ts = int(time.time())
slug = f"rba-cash-rate-market-update-{ts}"
title = f"RBA Cash Rate Forecast & Home Loan Refinancing ({ts})"

new_post = {
    "id": slug,
    "slug": slug,
    "title": title,
    "excerpt": "Australian mortgage borrowers are locking in competitive fixed rates as economic forecasts predict stable lending parameters.",
    "category": "Interest Rates & Refinancing",
    "publishDate": "Wed, 26 Aug 2026 08:00:00 +1000",
    "publishedDate": "26-Aug-2026",
    "formattedDate": "26-Aug-2026",
    "tags": ["#MortgageRates", "#RBA", "#Refinance", "#Australia"],
    "readTime": "4 min read",
    "videoUrl": "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/ezmortgage_2026_rba_cash_rate___refi_ultimate_avatar.mp4",
    "heroImage": "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "author": {"name": "R BAKSHI", "title": "Principal Mortgage Broker"}
}

# Update posts.json
if os.path.exists(posts_path):
    with open(posts_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        data.insert(0, new_post)
        with open(posts_path, "w", encoding="utf-8") as f:
            json.dump(data[:50], f, indent=2)

# Update news_db.json
if os.path.exists(news_db_path):
    with open(news_db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        data.insert(0, new_post)
        with open(news_db_path, "w", encoding="utf-8") as f:
            json.dump(data[:50], f, indent=2)

os.system(f'cd "{EZM_DIR}" && python3 scripts/generate_rss_feed.py && git commit -am "Publish fresh live trigger post {slug}" && git push origin main')
print(f"🚀 Fresh EZ Mortgage post published for instant trigger: {title}")
