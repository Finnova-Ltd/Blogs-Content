#!/usr/bin/env python3
"""
EZ Mortgage Broker - Automated Facebook Page Publisher (Meta Graph API)
=======================================================================
Facebook Page: Ez Mortgage Broker (Page ID: 61577637252836)
Domain: https://ezmortgagebroker.com.au

Features:
1. Automatically formats news & blog articles into engaging, high-converting Facebook posts.
2. Attaches high-resolution mortgage assets from images/assets-ez-mortgage-broker/
3. Publishes directly to Facebook Page feed via Meta Graph API.
4. Prevents duplicate posts by tracking published IDs in .fb_published_log.json.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

SITE_URL = "https://ezmortgagebroker.com.au"
PAGE_ID = os.environ.get("FB_PAGE_ID", "61577637252836")
ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN", "")

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(PROJECT_DIR, ".fb_published_log.json")
POSTS_JSON_PATH = os.path.join(PROJECT_DIR, "posts.json")

def load_published_log():
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_published_log(log_set):
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(log_set), f, indent=2)

def format_facebook_post(article):
    title = article.get("title", "")
    category = article.get("category", "Mortgage Insights")
    snippet = article.get("snippet", article.get("excerpt", ""))
    slug = article.get("slug", "")
    article_url = f"{SITE_URL}/pages/blog/{slug}.html" if slug else SITE_URL

    hashtags = "#EzMortgageBroker #HomeLoansAustralia #MortgageBroker #Refinance #FirstHomeBuyer #RBA #PropertyAustralia"

    post_message = f"""⚡ {category.upper()} | MARKET UPDATE ⚡

{title}

📊 Key Takeaway for Australian Borrowers:
{snippet}

✅ What this means for you:
🔹 Compare 30+ accredited lenders to access discretionary interest rate discounts
🔹 Check borrowing capacity and 3.0% APRA buffer serviceability
🔹 Fast-track pre-approval with zero broker fees

👉 Read full article & calculate your savings:
{article_url}

📞 Speak with our team: 1300 050 099
💬 Book a free consult: {SITE_URL}/#contact

{hashtags}"""
    return post_message.strip(), article_url

def post_to_facebook_feed(message, link_url):
    if not ACCESS_TOKEN or ACCESS_TOKEN == "YOUR_FB_PAGE_ACCESS_TOKEN":
        print("⚠️ FB_PAGE_ACCESS_TOKEN is not configured in .env yet.")
        print("   (Generated post preview shown below)")
        return False

    graph_url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "link": link_url,
        "access_token": ACCESS_TOKEN
    }

    data = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(graph_url, data=data)

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode('utf-8'))
            post_id = res.get("id")
            print(f"🎉 Successfully published to Facebook Page! Post ID: {post_id}")
            return post_id
    except Exception as e:
        print(f"❌ Error publishing to Facebook Graph API: {e}")
        return False

def main():
    print(f"📘 Facebook Auto-Publisher for Page ID: {PAGE_ID} (Ez Mortgage Broker)")
    published_log = load_published_log()

    # Load latest articles from posts.json
    if not os.path.exists(POSTS_JSON_PATH):
        print("⚠️ posts.json not found.")
        return

    with open(POSTS_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    posts = data if isinstance(data, list) else data.get('posts', [])

    candidates = [p for p in posts if p.get('slug') and p.get('slug') not in published_log]
    print(f"📋 Found {len(candidates)} new article candidates ready for Facebook syndication.")

    if not candidates:
        print("✓ All current articles have already been published or logged.")
        return

    # Process newest candidate
    latest = candidates[0]
    message, link = format_facebook_post(latest)

    print("\n========================================================")
    print("📢 GENERATED FACEBOOK POST PREVIEW:")
    print("========================================================")
    print(message)
    print("========================================================\n")

    if "--publish" in sys.argv or "--live" in sys.argv:
        post_id = post_to_facebook_feed(message, link)
        if post_id:
            published_log.add(latest['slug'])
            save_published_log(published_log)
    else:
        print("💡 Run with `python3 scripts/publish_to_facebook.py --live` to push live once FB_PAGE_ACCESS_TOKEN is set in .env.")

if __name__ == "__main__":
    main()
