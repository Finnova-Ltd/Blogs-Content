#!/usr/bin/env python3
"""
Make.com Content & Social Syndicator
====================================
Syndicates newly generated articles and news items to Make.com scenarios
for automated multi-channel posting across Facebook, LinkedIn, Google Business, and 𝕏.

Supports:
1. Direct Custom Webhook Post (`MAKE_WEBHOOK_URL`)
2. Make API Scenario Trigger (`MAKE_API_TOKEN` + `MAKE_SCENARIO_ID`)
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, Optional
from make_api_client import MakeApiClient

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON_PATH = os.path.join(PROJECT_DIR, "posts.json")
CONFIG_PATH = os.path.join(PROJECT_DIR, "content_engine_config.example.json")

def load_posts():
    if not os.path.exists(POSTS_JSON_PATH):
        print(f"❌ posts.json not found at {POSTS_JSON_PATH}")
        return []
    with open(POSTS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else data.get("posts", [])

def format_social_payload(post: Dict[str, Any], brand_url: str = "https://ezmortgagebroker.com.au") -> Dict[str, Any]:
    """Formats an article into an enriched payload ready for Make.com social modules."""
    title = post.get("title", "")
    slug = post.get("slug", "")
    url = f"{brand_url}/pages/blog/{slug}.html" if slug else f"{brand_url}/pages/blog.html"
    excerpt = post.get("excerpt", post.get("summary", post.get("metaDescription", "")))
    image = post.get("image", "")
    category = post.get("category", "Mortgage Insights")
    tags = post.get("tags", [category])
    author = post.get("author", "R BAKSHI")
    pub_date = post.get("publishDate", post.get("date", post.get("iso_date", "")))

    hashtags = " ".join([f"#{t.replace(' ', '').replace('&', '').replace('-', '')}" for t in tags])
    
    # Custom prepared captions for social platforms
    fb_caption = f"📊 {title}\n\n{excerpt}\n\n🔗 Read Full Advisory: {url}\n\n{hashtags}"
    li_caption = f"🏦 AUSTRALIAN MORTGAGE MARKET UPDATE | {category.upper()}\n\n{title}\n\nKey Takeaway: {excerpt}\n\n👉 Full Breakdown & Interactive Calculators: {url}\n\n{hashtags} #MortgageBroker #FinanceAustralia"
    gmb_summary = f"{title}\n\n{excerpt}\n\nBook your consultation or read more at {url}"

    return {
        "event": "new_article_published",
        "title": title,
        "slug": slug,
        "url": url,
        "excerpt": excerpt,
        "image": image,
        "category": category,
        "tags": tags,
        "author": author,
        "publishDate": pub_date,
        "hashtags": hashtags,
        "facebook_caption": fb_caption,
        "linkedin_caption": li_caption,
        "gmb_summary": gmb_summary,
        "raw_post": post
    }

def syndicate_article(
    post: Dict[str, Any],
    webhook_url: Optional[str] = None,
    scenario_id: Optional[int] = None,
    api_token: Optional[str] = None,
    zone: str = "eu1"
) -> bool:
    payload = format_social_payload(post)
    print(f"📦 Prepared syndication payload for: \"{payload['title']}\"")
    print(f"🔗 Article URL: {payload['url']}")

    success = False

    # 1. Custom Webhook dispatch
    target_webhook = webhook_url or os.getenv("MAKE_WEBHOOK_URL")
    if target_webhook:
        print(f"📡 Dispatching to Make.com Webhook: {target_webhook[:35]}...")
        wh_success = MakeApiClient.send_webhook_payload(target_webhook, payload)
        if wh_success:
            print("✅ Successfully delivered payload to Make.com Webhook!")
            success = True
        else:
            print("❌ Webhook dispatch failed.")

    # 2. Make API Scenario Trigger
    target_scenario = scenario_id or os.getenv("MAKE_SCENARIO_ID")
    target_token = api_token or os.getenv("MAKE_API_TOKEN")

    if target_scenario and target_token:
        try:
            s_id = int(target_scenario)
            client = MakeApiClient(api_token=target_token, zone=zone)
            print(f"🚀 Triggering Make.com Scenario ID: {s_id} via Make API v2...")
            res = client.run_scenario(s_id, data=payload)
            print("✅ Make Scenario triggered successfully!")
            print(f"Response: {json.dumps(res, indent=2)}")
            success = True
        except Exception as e:
            print(f"❌ Failed to trigger scenario via Make API: {e}")

    if not target_webhook and not (target_scenario and target_token):
        print("⚠️ No Make.com Webhook URL or Make API credentials found in environment.")
        print("💡 Set MAKE_WEBHOOK_URL or MAKE_API_TOKEN + MAKE_SCENARIO_ID to enable automated syndication.")
        print("Sample payload generated:")
        print(json.dumps(payload, indent=2))

    return success

def main():
    parser = argparse.ArgumentParser(description="Syndicate published articles to Make.com")
    parser.add_argument("--slug", type=str, help="Specific article slug to syndicate (defaults to latest)")
    parser.add_argument("--webhook-url", type=str, help="Make.com custom webhook URL")
    parser.add_argument("--scenario-id", type=int, help="Make.com scenario ID to trigger via API")
    parser.add_argument("--api-token", type=str, help="Make.com API Token")
    parser.add_argument("--zone", type=str, default="eu1", help="Make.com Zone (eu1, eu2, us1, us2)")

    args = parser.parse_args()

    posts = load_posts()
    if not posts:
        print("No articles found in posts.json.")
        sys.exit(1)

    target_post = None
    if args.slug:
        target_post = next((p for p in posts if p.get("slug") == args.slug), None)
        if not target_post:
            print(f"❌ Article with slug '{args.slug}' not found.")
            sys.exit(1)
    else:
        target_post = posts[0]

    syndicate_article(
        post=target_post,
        webhook_url=args.webhook_url,
        scenario_id=args.scenario_id,
        api_token=args.api_token,
        zone=args.zone
    )

if __name__ == "__main__":
    main()
