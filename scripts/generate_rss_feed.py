#!/usr/bin/env python3
"""
Generates standard RSS 2.0 feed (rss.xml / feed.xml) from posts.json
for EZ Mortgage Broker.
"""

import json, os, html
from datetime import datetime, timezone, timedelta

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_PATH = os.path.join(PROJECT_DIR, "posts.json")
SITE_URL = "https://ezmortgagebroker.com.au"

def build_rss():
    if not os.path.exists(POSTS_PATH):
        print("posts.json not found")
        return

    with open(POSTS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    posts = data if isinstance(data, list) else data.get('posts', [])

    rss_items = []
    for p in posts:
        title = html.escape(p.get('title', 'Mortgage Insight'))
        slug = p.get('slug', '')
        link = f"{SITE_URL}/pages/blog/{slug}.html" if slug else f"{SITE_URL}/pages/blog.html"
        desc = html.escape(p.get('excerpt', p.get('metaDescription', '')))
        pub_date = p.get('publishDate', datetime.now(timezone(timedelta(hours=10))).strftime("%a, %d %b %Y 00:00:00 +1000"))
        category = html.escape(p.get('category', 'Home Loans'))

        item_xml = f"""    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <description>{desc}</description>
      <category>{category}</category>
      <pubDate>{pub_date}</pubDate>
    </item>"""
        rss_items.append(item_xml)

    now_rfc = datetime.now(timezone(timedelta(hours=10))).strftime("%a, %d %b %Y %H:%M:%S +1000")

    full_rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>EZ Mortgage Broker — Australian Mortgage Insights &amp; Market News</title>
    <link>{SITE_URL}</link>
    <description>Daily Australian home loan updates, interest rate forecasts, first home buyer schemes, and refinancing guides.</description>
    <language>en-au</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml" />
{chr(10).join(rss_items)}
  </channel>
</rss>"""

    for out_p in [
        os.path.join(PROJECT_DIR, "rss.xml"),
        os.path.join(PROJECT_DIR, "feed.xml"),
        os.path.join(PROJECT_DIR, "public", "rss.xml"),
        os.path.join(PROJECT_DIR, "public", "feed.xml")
    ]:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        with open(out_p, 'w', encoding='utf-8') as f:
            f.write(full_rss)
        print(f"Generated {out_p}")

if __name__ == "__main__":
    build_rss()
