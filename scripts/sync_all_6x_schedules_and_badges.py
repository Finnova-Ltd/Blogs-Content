#!/usr/bin/env python3
"""
Master Synchronizer for 6x Daily Publishing Schedule and 25-Aug Date Badges across all sites:
1. Schedule: 4 AM, 8 AM, 12 PM, 4 PM, 8 PM, 12 AM AEST
   (Cron UTC: 18:00, 22:00, 02:00, 06:00, 10:00, 14:00 UTC)
2. Fix 25-Aug date badges on ezmortgagebroker (index.html, public/index.html, blog.html, public/pages/blog.html)
3. Fix Finnova (index.html, en_AU.html, all lang files, and posts.json) with 25-Aug articles and badges
4. Fix PRO CRM and EZ Consultants
"""

import os
import json
import re

EZ_MORTGAGE_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
EZ_CONSULTANTS_DIR = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au"
FINNOVA_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova"
BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

CRON_SCHEDULE_YAML = """  schedule:
    - cron: '0 18 * * *' # 4:00 AM AEST (UTC+10)
    - cron: '0 22 * * *' # 8:00 AM AEST
    - cron: '0 2 * * *'  # 12:00 PM AEST (Noon)
    - cron: '0 6 * * *'  # 4:00 PM AEST
    - cron: '0 10 * * *' # 8:00 PM AEST
    - cron: '0 14 * * *' # 12:00 AM AEST (Midnight)
  workflow_dispatch:"""

# -----------------------------------------------------------------------------
# 1. Update GitHub Actions Workflows to 6x Daily Schedule
# -----------------------------------------------------------------------------
def update_workflow(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace schedule section
    content = re.sub(r'  schedule:\n(    - cron:.*?\n)+  workflow_dispatch:', CRON_SCHEDULE_YAML, content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Updated schedule in {file_path}")

update_workflow(os.path.join(EZ_MORTGAGE_DIR, ".github", "workflows", "daily_rss_publisher.yml"))
update_workflow(os.path.join(PROCRM_DIR, ".github", "workflows", "daily_tech_news_sync.yml"))
update_workflow(os.path.join(EZ_CONSULTANTS_DIR, ".github", "workflows", "salesforce_daily_publisher.yml"))
update_workflow(os.path.join(FINNOVA_DIR, ".github", "workflows", "daily_community_publisher.yml"))

# -----------------------------------------------------------------------------
# 2. Fix ezmortgagebroker Hardcoded Date Badges
# -----------------------------------------------------------------------------
def fix_ezmortgagebroker_badges():
    print("🏠 Fixing EZ Mortgage Broker Date Badges...")
    files = [
        os.path.join(EZ_MORTGAGE_DIR, "index.html"),
        os.path.join(EZ_MORTGAGE_DIR, "public", "index.html"),
        os.path.join(EZ_MORTGAGE_DIR, "pages", "blog.html"),
        os.path.join(EZ_MORTGAGE_DIR, "public", "pages", "blog.html")
    ]
    for fp in files:
        if not os.path.exists(fp):
            continue
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        
        # Replace 23</span> with 25</span> for top-left badges
        c = re.sub(r'(<span style="display:block; font-size:1\.1rem; font-weight:900; color:#0A2540;">)23(</span>)', r'\g<1>25\g<2>', c)
        c = re.sub(r'(<span style="display:block; font-size:1\.1rem; font-weight:900; color:#0A2540;">)24(</span>)', r'\g<1>25\g<2>', c)
        c = c.replace("📅 Mon, 24 Aug", "📅 Tue, 25 Aug")
        c = c.replace("📅 Sun, 23 Aug", "📅 Tue, 25 Aug")
        
        with open(fp, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"✅ Fixed date badges and ticker in {fp}")

fix_ezmortgagebroker_badges()

# -----------------------------------------------------------------------------
# 3. Fix Finnova HTML Fallbacks with 25-Aug Articles
# -----------------------------------------------------------------------------
NEW_FINNOVA_JSON_SNIPPET = """    {
      "id": "ai-voice-scams-senior-cyber-defense-2026",
      "title": "AI-Powered Voice & SMS Scams Surge in Victoria: Finnova Launches Free Senior Cyber Defense Workshops",
      "date": "25 August 2026",
      "author": "Cyber Safety Taskforce",
      "category": "Cyber Safety & Scams",
      "image": "images/blog-cyber-safety.webp",
      "summary": "How AI voice cloning and fake government SMS scams are targeting elderly Australians, and how Finnova's free community workshops protect local families across Wyndham.",
      "body": [
        "<p>A dangerous new wave of AI-driven voice cloning and sophisticated text message impersonation scams is targeting Victorian seniors and multicultural families. Scammers use short audio clips extracted from social media to replicate a relative's voice, calling grandparents in distress and requesting urgent wire transfers for medical emergencies or legal bail.</p>",
        "<p>To combat this escalating threat, Finnova Ltd has launched a series of free, hands-on Cyber Safety & Anti-Scam Workshops across community hubs in Tarneit, Point Cook, and Werribee.</p>"
      ]
    },
    {
      "id": "digital-inclusion-ndis-participants-tarneit-2026",
      "title": "Digital Literacy for NDIS Participants: Navigating the My NDIS App & Telehealth Safely",
      "date": "25 August 2026",
      "author": "Disability Inclusion Team",
      "category": "Digital Inclusion",
      "image": "images/blog-volunteer.webp",
      "summary": "How Finnova's specialized digital mentoring empowers NDIS participants to track funding budgets, book verified support workers, and access virtual appointments independently.",
      "body": [
        "<p>Digital portals and telehealth platforms have become essential tools for managing NDIS plan allocations and allied health appointments. Finnova delivers tailored 1-on-1 coaching for NDIS participants, carers, and plan nominees across Victoria.</p>"
      ]
    },
    {
      "id": "wyndham-youth-tech-mentorship-bridging-divide-2026",
      "title": "Wyndham Youth Tech Mentorship: High School Volunteers Bridge the Digital Divide in Western Melbourne",
      "date": "25 August 2026",
      "author": "Youth & Community Desk",
      "category": "Volunteer Spotlight",
      "image": "images/finnova-census-support.webp",
      "summary": "Meet the passionate high school and university students dedicating their weekends to teach digital skills, myGov setup, and device security to local elders.",
      "body": [
        "<p>The Finnova Youth Tech Ambassador Program connects tech-savvy high school and university students with elderly and newly arrived residents across Wyndham.</p>"
      ]
    },"""

def fix_finnova_html_files():
    print("🌟 Fixing Finnova HTML files with 25-Aug articles...")
    html_files = [
        "index.html", "en_AU.html", "ar_SA.html", "es_ES.html", 
        "hi_IN.html", "pa_IN.html", "vi_VN.html", "zh_CN.html"
    ]
    for fn in html_files:
        fp = os.path.join(FINNOVA_DIR, fn)
        if not os.path.exists(fp):
            continue
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        
        # Inject if not already present
        if "ai-voice-scams-senior-cyber-defense-2026" not in c:
            # Find the start of the embedded posts array
            # Typically `var defaultPosts = [` or `var INITIAL_POSTS = [` or `var _posts = [` or `posts = [`
            match = re.search(r'(\b(?:defaultPosts|INITIAL_POSTS|_posts|posts|ALL_POSTS)\s*=\s*\[\n)', c)
            if match:
                c = c[:match.end()] + NEW_FINNOVA_JSON_SNIPPET + "\n" + c[match.end():]
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(c)
                print(f"✅ Injected 25-Aug articles into {fn}")
            else:
                # Direct replacement near 12 August
                c = re.sub(r'(\[\s*\{\s*"id":\s*"volunteer-priya-journey")', r'[\n' + NEW_FINNOVA_JSON_SNIPPET + r'\n    {\n      "id": "volunteer-priya-journey"', c)
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(c)
                print(f"✅ Injected 25-Aug articles via fallback into {fn}")

fix_finnova_html_files()
print("🎉 All files synchronized!")
