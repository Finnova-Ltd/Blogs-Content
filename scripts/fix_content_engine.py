#!/usr/bin/env python3
import os

REPO_DIR = "/Users/robinbakshi/Documents/GitHub/rss"
content_engine_path = os.path.join(REPO_DIR, "content_engine.py")

content = """#!/usr/bin/env python3
\"\"\"
Multi-Source Content Engine & Blog Publisher
============================================
1. Ingests from multiple sources per project (RSS/XML feeds, web pages, Yahoo Finance tickers, Google Alerts).
2. Filters strictly by custom keywords (e.g. "home buyers", "centrelink", "mortgage", "rates").
3. Automatically rewrites raw news items into 180-200 word value-dense expert blog articles in your own words.
4. Publishes to posts.json and HTML/Markdown pages for any target website.
5. Auto-syndicates to Make.com / Zapier webhooks for instant Facebook and LinkedIn multi-channel posting.
\"\"\"

import os
import sys
import re
import json
import html
import urllib.request
import urllib.parse
from datetime import datetime
from universal_rss import UniversalRSS

class MultiSourceContentEngine:
    def __init__(self, config_or_path):
        if isinstance(config_or_path, str):
            with open(config_or_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = config_or_path

    def fetch_project_items(self, project_cfg):
        \"\"\"Polls all configured sources for a project and filters by keywords.\"\"\"
        all_candidates = []
        keywords = project_cfg.get("keywords", [])
        sources = project_cfg.get("sources", [])

        print(f"📡 Polling {len(sources)} sources for project: '{project_cfg.get('name', 'Default')}'...")
        print(f"🎯 Filtering by keywords: {keywords}")

        for src in sources:
            src_type = src.get("type", "url")
            src_val = src.get("value")
            category = src.get("category", "Market News")

            feed = UniversalRSS(title="Temp", link="https://example.com")

            if src_type == "rss" or src_type == "xml":
                if "google.com/alerts" in src_val or "<feed" in src_val:
                    feed.from_google_alerts(src_val)
                else:
                    try:
                        req = urllib.request.Request(src_val, headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req, timeout=10) as resp:
                            xml_str = resp.read().decode("utf-8", errors="ignore")
                        items = re.findall(r'<item>(.*?)</item>', xml_str, re.DOTALL)
                        for item in items:
                            t_m = re.search(r'<title[^>]*>(.*?)</title>', item, re.DOTALL)
                            l_m = re.search(r'<link[^>]*>(.*?)</link>', item, re.DOTALL)
                            d_m = re.search(r'<description[^>]*>(.*?)</description>', item, re.DOTALL)
                            title = html.unescape(re.sub(r'<.*?>', '', t_m.group(1))).strip() if t_m else ""
                            link = l_m.group(1).strip() if l_m else ""
                            desc = html.unescape(re.sub(r'<.*?>', '', d_m.group(1))).strip() if d_m else ""
                            if title and link:
                                feed.add_item(title=title, link=link, description=desc, category=category)
                    except Exception as e:
                        print(f"⚠️ RSS read error for {src_val}: {e}")

            elif src_type == "yahoo_finance":
                feed.from_yahoo_finance(src_val, keywords=keywords)

            elif src_type == "url":
                feed.from_url(src_val)

            elif src_type == "wordpress":
                feed.from_wordpress_api(src_val)

            elif src_type == "substack":
                feed.from_substack_api(src_val)

            # Filter items by keywords
            for entry in feed.entries:
                text_to_check = (entry["title"] + " " + entry["description"]).lower()
                if keywords:
                    if not any(k.lower() in text_to_check for k in keywords):
                        continue
                entry["project_category"] = category
                all_candidates.append(entry)

        print(f"✅ Extracted {len(all_candidates)} matching candidates.")
        return all_candidates

    def rewrite_article(self, item, brand_voice="Expert Mortgage Broker"):
        \"\"\"
        Rewrites raw news item into a 180-200 word value-dense advisory brief.
        Uses OpenAI/Gemini if API keys are set in environment, or intelligent structured engine fallback.
        \"\"\"
        title = item["title"]
        summary = item["description"]
        category = item.get("project_category", "Market Update")
        source_url = item["link"]

        # Check for Gemini / OpenAI API Keys
        gemini_key = os.getenv("GEMINI_API_KEY")

        if gemini_key:
            try:
                prompt = (
                    f"You are writing for an Australian financial blog as a {brand_voice}. "
                    f"Rewrite the following news story into a 180-200 word value-dense article in our own words. "
                    f"Headline: {title}. Summary: {summary}. "
                    f"Return a JSON object with keys: title, summary (approx 60 words), bullets (array of 3 key borrower takeaways), tip (expert broker tip)."
                )
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"response_mime_type": "application/json"}
                }
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=12) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                    text_resp = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    ai_obj = json.loads(text_resp)
                    return {
                        "title": ai_obj.get("title", title),
                        "summary": ai_obj.get("summary", summary),
                        "bullets": ai_obj.get("bullets", []),
                        "tip": ai_obj.get("tip", "Contact our accredited specialists to discuss your tailored options."),
                        "sourceUrl": source_url,
                        "category": category
                    }
            except Exception as ge:
                print(f"ℹ️ Gemini rewrite notice (using structured engine): {ge}")

        # Intelligent Structured Fallback Engine (180-200 words)
        clean_title = title
        if not any(k in clean_title.lower() for k in ["australia", "borrower", "home loan", "property"]):
            clean_title = f"{title}: Australian Market Analysis & Borrower Advisory"

        lead_summary = (
            f"Recent Australian financial and market developments regarding {category.lower()} highlight shifting conditions across lenders and regulators. "
            f"{summary if len(summary) > 60 else 'Industry reports confirm that borrowers and home buyers are navigating changing assessment policies and rate benchmarks.'} "
            f"For property owners, first-home buyers, and investors, understanding these policy shifts is critical to structuring loans effectively and avoiding unnecessary interest costs."
        )

        bullets = [
            f"Market Impact: Key changes in {category} are prompting lenders to review borrowing capacity algorithms and assessment buffers.",
            "Borrower Serviceability: Household living expense declarations and debt-to-income benchmarks remain under active scrutiny by credit assessors.",
            "Strategic Negotiation: Existing mortgage holders with equity have substantial leverage to request unadvertised rate discounts or restructure loan splits."
        ]

        tip = (
            "Never accept standard advertised rates or single-lender limits. "
            "Consult an accredited specialist to compare over 50 Australian lenders and calculate your exact borrowing capacity with zero broker fees."
        )

        return {
            "title": clean_title,
            "summary": lead_summary,
            "bullets": bullets,
            "tip": tip,
            "sourceUrl": source_url,
            "category": category
        }

    def publish_project(self, project_cfg):
        \"\"\"Runs end-to-end ingestion, rewriting, file generation, and Make.com syndication for a project.\"\"\"
        candidates = self.fetch_project_items(project_cfg)
        output_posts_json = project_cfg.get("posts_json_path")
        output_html_dir = project_cfg.get("html_dir")
        make_webhook = project_cfg.get("make_webhook_url") or os.getenv("MAKE_WEBHOOK_URL")
        brand_name = project_cfg.get("brand_name", "EZ Mortgage Broker")
        brand_url = project_cfg.get("brand_url", "https://ezmortgagebroker.com.au")
        author = project_cfg.get("author", "R BAKSHI")

        existing_slugs = set()
        existing_posts = []

        if output_posts_json and os.path.exists(output_posts_json):
            try:
                with open(output_posts_json, "r", encoding="utf-8") as f:
                    existing_posts = json.load(f)
                    existing_slugs = {p.get("slug") for p in existing_posts}
            except Exception:
                existing_posts = []

        new_published = []

        for item in candidates[:project_cfg.get("max_publish_per_run", 4)]:
            slug = re.sub(r'[^a-z0-9\\s-]', '', item["title"].lower())
            slug = re.sub(r'[\\s-]+', '-', slug).strip('-')[:75]

            if slug in existing_slugs:
                continue

            article = self.rewrite_article(item, brand_voice=project_cfg.get("brand_voice", "Mortgage Specialist"))

            post_obj = {
                "id": slug,
                "slug": slug,
                "title": article["title"],
                "category": article["category"],
                "date": datetime.now().strftime("%d-%b-%Y"),
                "iso_date": datetime.now().isoformat(),
                "readTime": "4 min read",
                "author": author,
                "excerpt": article["summary"][:160] + "...",
                "summary": article["summary"],
                "bullets": article["bullets"],
                "tip": article["tip"],
                "sourceUrl": article["sourceUrl"],
                "url": f"/pages/blog/{slug}.html"
            }

            if output_html_dir:
                os.makedirs(output_html_dir, exist_ok=True)
                html_path = os.path.join(output_html_dir, f"{slug}.html")
                html_content = self.generate_blog_html(post_obj, brand_name, brand_url)
                with open(html_path, "w", encoding="utf-8") as hf:
                    hf.write(html_content)

            new_published.append(post_obj)
            existing_slugs.add(slug)
            print(f"✨ Successfully Rewrote & Published: [{article['category']}] {article['title']}")

            if make_webhook:
                self.dispatch_to_make(make_webhook, post_obj, brand_url)

        if new_published and output_posts_json:
            merged = new_published + existing_posts
            os.makedirs(os.path.dirname(os.path.abspath(output_posts_json)), exist_ok=True)
            with open(output_posts_json, "w", encoding="utf-8") as f:
                json.dump(merged, f, indent=2)
            print(f"✅ Synced {len(new_published)} new articles into {output_posts_json} (Total: {len(merged)})")

        return len(new_published)

    def dispatch_to_make(self, webhook_url, post, brand_url):
        \"\"\"Sends rich social payload to Make.com scenario for Facebook, LinkedIn & GMB auto-posting.\"\"\"
        try:
            url = f"{brand_url}{post['url']}"
            fb_caption = f"📊 {post['title']}\\n\\n{post['excerpt']}\\n\\n🔗 Read Full Briefing: {url}"
            li_caption = f"🏦 AUSTRALIAN MARKET INSIGHT | {post['category'].upper()}\\n\\n{post['title']}\\n\\nKey Takeaway: {post['summary']}\\n\\n👉 Full Breakdown & Calculators: {url}"

            payload = {
                "event": "new_article_published",
                "title": post["title"],
                "slug": post["slug"],
                "url": url,
                "excerpt": post["excerpt"],
                "summary": post["summary"],
                "category": post["category"],
                "author": post["author"],
                "facebook_caption": fb_caption,
                "linkedin_caption": li_caption,
                "raw_post": post
            }

            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "Finnova-Content-Engine/1.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                print(f"🚀 Dispatched '{post['title'][:35]}...' to Make.com Webhook (Status {r.status})")
        except Exception as me:
            print(f"⚠️ Make.com webhook notice: {me}")

    def generate_blog_html(self, post, brand_name, brand_url):
        \"\"\"Generates standard responsive HTML page with Schema JSON-LD.\"\"\"
        bullets_li = "".join([f'<li style="margin-bottom:8px;">• {b}</li>' for b in post.get("bullets", [])])
        return f\"\"\"<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <title>{post['title']} | {brand_name}</title>
  <meta name="description" content="{post['excerpt']}">
  <link rel="canonical" href="{brand_url}{post['url']}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": "{post['title']}",
    "description": "{post['excerpt']}",
    "datePublished": "{post['iso_date']}",
    "author": {{"@type": "Person", "name": "{post['author']}"}}
  }}
  </script>
</head>
<body style="font-family: sans-serif; background: #f8fafc; padding: 40px 20px; color: #1e293b;">
  <article style="max-width: 800px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
    <span style="background: #0284c7; color: #fff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700;">{post['category']}</span>
    <h1 style="font-size: 28px; line-height: 1.3; color: #084582; margin-top: 16px;">{post['title']}</h1>
    <div style="font-size: 13px; color: #64748b; margin-bottom: 24px;">By {post['author']} • {post['date']} • {post['readTime']}</div>
    
    <div style="background: #f1f5f9; padding: 20px; border-radius: 12px; margin-bottom: 24px;">
      <h3 style="margin-top:0; font-size: 16px; color: #084582;">Executive Summary</h3>
      <p style="line-height: 1.6; font-size: 15px; margin: 0;">{post['summary']}</p>
    </div>

    <h3 style="color: #0f172a;">Key Market Takeaways</h3>
    <ul style="line-height: 1.6; padding-left: 20px;">
      {bullets_li}
    </ul>

    <div style="background: #e0f2fe; padding: 20px; border-radius: 12px; margin: 24px 0; border: 1px solid #bae6fd;">
      <h4 style="margin-top:0; color: #0369a1;">Expert Advisory Tip</h4>
      <p style="margin: 0; line-height: 1.5; font-size: 14px;">{post['tip']}</p>
    </div>

    <div style="font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 16px;">
      Source: <a href="{post['sourceUrl']}" target="_blank" rel="nofollow" style="color: #0284c7;">Original Market Intelligence Source</a>
    </div>
  </article>
</body>
</html>\"\"\"

def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else "projects_config.example.json"
    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        return

    engine = MultiSourceContentEngine(config_file)
    projects = engine.config.get("projects", [])
    print(f"🚀 Running Multi-Source Content Engine across {len(projects)} configured project(s)...")

    for proj in projects:
        print(f"\\n--- Processing Project: {proj['name']} ---")
        engine.publish_project(proj)

if __name__ == "__main__":
    main()
"""

with open(content_engine_path, "w", encoding="utf-8") as f:
    f.write(content)
print("✅ Fixed content_engine.py in Finnova-Ltd/rss")
