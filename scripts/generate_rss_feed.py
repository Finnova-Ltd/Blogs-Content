#!/usr/bin/env python3
"""
Generates standard RSS 2.0 feed with Media Enclosures (rss.xml / feed.xml) from posts.json.
Enables Make.com and social distribution platforms to ingest and publish:
1. Daily YouTube Shorts (<enclosure url="...mp4" type="video/mp4" />)
2. Daily 10-Minute Masterclass Long Video (<media:content url="...10min.mp4" ... />)

Enforces Australian Timezone (Australia/Melbourne) as per AGENTS.md conventions.
"""

import json
import os
import html
from datetime import datetime
from zoneinfo import ZoneInfo

MELBOURNE_TZ = ZoneInfo("Australia/Melbourne")
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_PATH = os.path.join(PROJECT_DIR, "posts.json")
SITE_URL = "https://ezmortgagebroker.com.au"

DEFAULT_SHORT_VIDEO = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/ezmortgage_latest_studio_short.mp4"
DEFAULT_LONG_VIDEO = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/masterclass_ezmortgage_10min.mp4"

def build_rss():
    if not os.path.exists(POSTS_PATH):
        print("posts.json not found")
        return

    with open(POSTS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    posts = data if isinstance(data, list) else data.get('posts', [])
    updated = False

    rss_items = []
    for p in posts:
        title = html.escape(p.get('title', 'Mortgage Insight'))
        slug = p.get('slug', '')
        link = f"{SITE_URL}/pages/blog/{slug}.html" if slug else f"{SITE_URL}/pages/blog.html"
        desc_raw = p.get('excerpt', p.get('metaDescription', ''))
        
        # Ensure video URLs are populated
        video_url = p.get('videoUrl')
        if not video_url or video_url == "None":
            video_url = DEFAULT_SHORT_VIDEO
            p['videoUrl'] = video_url
            updated = True
            
        long_video_url = p.get('longVideoUrl')
        if not long_video_url or long_video_url == "None":
            long_video_url = DEFAULT_LONG_VIDEO
            p['longVideoUrl'] = long_video_url
            updated = True

        pub_date = p.get('publishDate')
        if not pub_date:
            pub_date = datetime.now(MELBOURNE_TZ).strftime("%a, %d %b %Y 00:00:00 +1000")

        category = html.escape(p.get('category', 'Home Loans'))

        full_desc = (
            f"{desc_raw}\n\n"
            f"🎬 Watch YouTube Short Breakdown: {video_url}\n"
            f"📺 Watch Complete 10-Minute Masterclass: {long_video_url}\n"
            f"📞 Call 1300 050 099 — Connect with an Accredited Mortgage Broker at EZ Mortgage Broker"
        )
        desc_escaped = html.escape(full_desc)

        item_xml = f"""    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <description>{desc_escaped}</description>
      <category>{category}</category>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{video_url}" length="2621440" type="video/mp4" />
      <media:content url="{video_url}" medium="video" type="video/mp4" expression="full" duration="45">
        <media:title>{title} #Shorts</media:title>
        <media:description>{html.escape(desc_raw)}</media:description>
      </media:content>
      <media:content url="{long_video_url}" medium="video" type="video/mp4" expression="full" duration="600">
        <media:title>{title} — 10-Minute Full Masterclass Analysis</media:title>
        <media:description>{html.escape(desc_raw)}</media:description>
      </media:content>
    </item>"""
        rss_items.append(item_xml)

    now_rfc = datetime.now(MELBOURNE_TZ).strftime("%a, %d %b %Y %H:%M:%S +1000")

    full_rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>EZ Mortgage Broker — Australian Mortgage Insights &amp; Market News</title>
    <link>{SITE_URL}</link>
    <description>Daily Australian home loan updates, interest rate forecasts, YouTube Shorts, and 10-minute masterclasses.</description>
    <language>en-au</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml" />
{chr(10).join(rss_items)}
  </channel>
</rss>"""

    # Save updated posts.json if we filled in missing video URLs
    if updated:
        with open(POSTS_PATH, 'w', encoding='utf-8') as f:
            if isinstance(data, list):
                json.dump(posts, f, indent=2, ensure_ascii=False)
            else:
                data['posts'] = posts
                json.dump(data, f, indent=2, ensure_ascii=False)
        print("✅ Updated posts.json with active videoUrl and longVideoUrl across all posts")

    # Write out feed files in Blogs-Content
    targets = [
        os.path.join(PROJECT_DIR, "rss.xml"),
        os.path.join(PROJECT_DIR, "feed.xml"),
        os.path.join(PROJECT_DIR, "public", "rss.xml"),
        os.path.join(PROJECT_DIR, "public", "feed.xml")
    ]
    
    # Also write to ezmortgagebroker if present
    ezm_dir = "/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker"
    if os.path.exists(ezm_dir):
        targets.extend([
            os.path.join(ezm_dir, "rss.xml"),
            os.path.join(ezm_dir, "feed.xml"),
            os.path.join(ezm_dir, "public", "rss.xml"),
            os.path.join(ezm_dir, "public", "feed.xml")
        ])

    for out_p in targets:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        with open(out_p, 'w', encoding='utf-8') as f:
            f.write(full_rss)
        print(f"Generated {out_p}")

if __name__ == "__main__":
    build_rss()
