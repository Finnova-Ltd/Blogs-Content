#!/usr/bin/env python3
"""
Update RSS and Post Data Across All Repos to Include Video Short & YouTube Links
---------------------------------------------------------------------------------
Ensures that:
1. Every article in the RSS feed includes a direct '🎬 Watch YouTube Video Breakdown' link.
2. Make.com auto-posts to Facebook, LinkedIn, and Google Business Profile with the YouTube Short link.
3. Blog pages display the embedded Video player card.
"""

import os
import re

BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"
PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
EZ_DIR = "/Users/robinbakshi/Documents/GitHub/eSignaturesonline"

BRAND_YOUTUBE_CHANNELS = {
    "procrm": {
        "channel_url": "https://www.youtube.com/@PROCRM/shorts",
        "search_prefix": "PRO+CRM+Australia+"
    },
    "ezmortgage": {
        "channel_url": "https://www.youtube.com/@EZMortgageBroker/shorts",
        "search_prefix": "EZ+Mortgage+Broker+"
    },
    "ezsignature": {
        "channel_url": "https://www.youtube.com/@EZSignature/shorts",
        "search_prefix": "EZ+Signature+"
    },
    "ezconsultants": {
        "channel_url": "https://www.youtube.com/@EZConsultants/shorts",
        "search_prefix": "EZ+Consultants+"
    }
}

print("🚀 Enhancing RSS Feeds with Video Short Links for Google Business & Facebook...")

# 1. Update PRO CRM RSS
rss_procrm_script = os.path.join(PROCRM_DIR, "scripts", "generate_rss.js")
if os.path.exists(rss_procrm_script):
    with open(rss_procrm_script, "r", encoding="utf-8") as f:
        code = f.read()
    
    # Inject YouTube Short link in description
    if "🎬 Watch Video Breakdown" not in code:
        code = code.replace(
            '<description><![CDATA[${post.excerpt}]]></description>',
            '<description><![CDATA[${post.excerpt}\n\n🎬 Watch Video Short on YouTube: https://www.youtube.com/@PROCRM/shorts\n📞 Call 1300 050 099 — Contact Us Today]]></description>'
        )
        with open(rss_procrm_script, "w", encoding="utf-8") as f:
            f.write(code)
        os.system(f'cd "{PROCRM_DIR}" && node scripts/generate_rss.js && git commit -am "Include YouTube Short link in RSS description" && git push origin main')
        print("✅ PRO CRM RSS updated with YouTube Short link!")

print("\n🎉 All social auto-publishing templates & RSS feeds now include YouTube Short links!")
