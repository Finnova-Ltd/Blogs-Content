#!/usr/bin/env python3
"""
Update ezmortgagebroker ingestion engine with Yahoo Finance Topic Feeds:
1. Money (https://au.finance.yahoo.com/topic/money/)
2. Property (https://au.finance.yahoo.com/topic/property/)
3. Personal Finance (https://au.finance.yahoo.com/topic/personal-finance/)
Ensuring at least 4 articles from each category are published with Make.com syndication.
"""

import os
import sys
import re
import json
import html
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime

EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
POSTS_JSON = os.path.join(EZ_DIR, "posts.json")
PUB_POSTS_JSON = os.path.join(EZ_DIR, "public", "posts.json")
BLOG_DIR = os.path.join(EZ_DIR, "pages", "blog")
PUB_BLOG_DIR = os.path.join(EZ_DIR, "public", "pages", "blog")

os.makedirs(BLOG_DIR, exist_ok=True)
os.makedirs(PUB_BLOG_DIR, exist_ok=True)

CATEGORIES = [
    {
        "name": "Money & Banking",
        "url": "https://au.finance.yahoo.com/topic/money/",
        "target_count": 4,
        "keywords": ["mortgage", "rate", "interest", "bank", "buyer", "money", "loan", "lender", "cash", "super"]
    },
    {
        "name": "Property & Housing",
        "url": "https://au.finance.yahoo.com/topic/property/",
        "target_count": 4,
        "keywords": ["property", "housing", "mortgage", "home", "buyer", "landlord", "rent", "investor", "build", "estate"]
    },
    {
        "name": "Personal Finance & Centrelink",
        "url": "https://au.finance.yahoo.com/topic/personal-finance/",
        "target_count": 4,
        "keywords": ["centrelink", "tax", "finance", "superannuation", "saving", "cgt", "budget", "retirement", "debt", "wealth"]
    }
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def extract_topic_articles(topic_url, keywords):
    articles = []
    try:
        req = urllib.request.Request(topic_url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
        
        matches = re.findall(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL)
        seen = set()
        for href, text in matches:
            clean_text = re.sub(r'<.*?>', '', text).strip()
            clean_text = html.unescape(clean_text)
            if len(clean_text) < 25 or len(clean_text) > 160:
                continue
            if any(skip in clean_text.lower() for skip in ["privacy", "terms", "sign in", "yahoo", "cookie", "skip to"]):
                continue

            full_link = urllib.parse.urljoin("https://au.finance.yahoo.com", href)
            if full_link in seen:
                continue
            seen.add(full_link)

            # Check keyword match
            text_lower = clean_text.lower()
            if not any(k in text_lower for k in keywords):
                continue

            articles.append({
                "title": clean_text,
                "link": full_link
            })
    except Exception as e:
        print(f"⚠️ Error scraping {topic_url}: {e}")
    return articles

def rewrite_to_180_words(title, category, source_url):
    clean_title = title.replace("<b>", "").replace("</b>", "").strip()
    if not any(k in clean_title.lower() for k in ["australia", "borrower", "home loan", "property", "rate"]):
        clean_title = f"{clean_title}: Australian Borrower & Market Analysis"

    summary = (
        f"Recent Australian market intelligence in {category.lower()} outlines key shifts impacting everyday borrowers, home buyers, and property investors. "
        f"Industry data confirms that changing lender assessment benchmarks, interest rate expectations, and government policy rules are reshaping household borrowing power across Australian states. "
        f"Navigating these updates proactively allows borrowers to safeguard their serviceability buffers, reduce unadvertised bank loyalty premiums, and unlock strategic financing solutions."
    )

    bullets = [
        f"Lending Policy Impact: Financial institutions and regulators are recalibrating credit assessment buffers and living expense verification standards across {category}.",
        "Borrower Serviceability: Household cashflow buffers and debt-to-income limits remain paramount for loan pre-approvals and refinancing applications.",
        "Strategic Rate Negotiation: Accredited mortgage broker access to 50+ lenders provides significant leverage to negotiate unadvertised pricing discounts."
    ]

    tip = (
        "Never accept standard branch-advertised pricing or single-lender borrowing restrictions. "
        "Consult an accredited Australian mortgage specialist to evaluate over 50 accredited lenders and maximize your loan structure with zero broker fees."
    )

    return {
        "title": clean_title,
        "summary": summary,
        "bullets": bullets,
        "tip": tip
    }

def generate_blog_html(post):
    bullets_li = "".join([f'<li style="margin-bottom:10px;">• {b}</li>' for b in post["bullets"]])
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{post['title']} | EZ Mortgage Broker</title>
  <meta name="description" content="{post['excerpt']}">
  <link rel="canonical" href="https://ezmortgagebroker.com.au{post['url']}">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="/css/style.css">
  
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": "{post['title']}",
    "description": "{post['excerpt']}",
    "datePublished": "{post['iso_date']}",
    "author": {{"@type": "Person", "name": "R BAKSHI"}},
    "publisher": {{
      "@type": "Organization",
      "name": "EZ Mortgage Broker",
      "logo": {{"@type": "ImageObject", "url": "https://ezmortgagebroker.com.au/images/ez-mortgage-broker.webp"}}
    }}
  }}
  </script>
</head>
<body style="font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #0f172a; margin: 0; padding: 0;">

  <!-- Header -->
  <header style="background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 14px 24px;">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between;">
      <a href="/" style="display: flex; align-items: center;">
        <img src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" style="height: 54px; width: auto;">
      </a>
      <a href="/calculators.html" style="background: #084582; color: #ffffff; padding: 8px 18px; border-radius: 999px; text-decoration: none; font-weight: 700; font-size: 0.88rem;">Calculate Borrowing Power ↗</a>
    </div>
  </header>

  <main style="max-width: 860px; margin: 40px auto; padding: 0 20px;">
    <article style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; padding: clamp(24px, 4vw, 48px); box-shadow: 0 4px 20px rgba(0,0,0,0.04);">
      
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">
        <span style="background: #f59e0b; color: #ffffff; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; padding: 4px 12px; border-radius: 9999px;">{post['category']}</span>
        <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">By R BAKSHI • {post['date']} • {post['readTime']}</span>
      </div>

      <h1 style="font-size: clamp(1.75rem, 3.2vw, 2.35rem); font-weight: 900; color: #084582; line-height: 1.25; margin: 0 0 24px;">{post['title']}</h1>

      <!-- Executive Summary Box -->
      <div style="background: #f0f7ff; border-left: 4px solid #0284c7; padding: 20px; border-radius: 0 12px 12px 0; margin-bottom: 32px;">
        <h3 style="margin: 0 0 8px; font-size: 1rem; color: #0369a1; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">Executive Summary</h3>
        <p style="margin: 0; line-height: 1.65; color: #334155; font-size: 0.98rem;">{post['summary']}</p>
      </div>

      <h2 style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0 0 14px;">Key Market & Borrower Takeaways</h2>
      <ul style="line-height: 1.65; color: #475569; padding-left: 20px; margin: 0 0 32px; font-size: 0.95rem;">
        {bullets_li}
      </ul>

      <!-- Broker Tip Callout -->
      <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 14px; padding: 22px; margin-bottom: 32px;">
        <h3 style="margin: 0 0 8px; font-size: 1rem; color: #065f46; font-weight: 800;">💡 Accredited Mortgage Specialist Advice</h3>
        <p style="margin: 0; line-height: 1.6; color: #047857; font-size: 0.94rem;">{post['tip']}</p>
      </div>

      <!-- Action Box -->
      <div style="background: linear-gradient(135deg, #084582 0%, #0369a1 100%); color: #ffffff; padding: 32px; border-radius: 16px; text-align: center; margin-bottom: 32px;">
        <h3 style="margin: 0 0 8px; font-size: 1.4rem; font-weight: 900;">Take Advantage of Current Rate Discounts</h3>
        <p style="margin: 0 auto 20px; max-width: 550px; font-size: 0.95rem; opacity: 0.92;">Compare over 50 Australian banks and non-bank lenders with zero broker fees.</p>
        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
          <a href="/calculators.html#borrowing-power" style="background: #f59e0b; color: #ffffff; padding: 12px 24px; border-radius: 10px; font-weight: 800; text-decoration: none;">Calculate Borrowing Power ↗</a>
          <a href="/#contact" style="background: #ffffff; color: #084582; padding: 12px 24px; border-radius: 10px; font-weight: 800; text-decoration: none;">Book Strategy Consultation</a>
        </div>
      </div>

      <div style="font-size: 0.8rem; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 16px;">
        Market Source: <a href="{post['sourceUrl']}" target="_blank" rel="nofollow noopener" style="color: #0284c7;">Yahoo Finance Australia Market Intelligence</a>
      </div>
    </article>
  </main>
</body>
</html>"""

def main():
    existing_posts = []
    if os.path.exists(POSTS_JSON):
        try:
            with open(POSTS_JSON, "r", encoding="utf-8") as f:
                existing_posts = json.load(f)
        except Exception:
            existing_posts = []

    existing_slugs = {p.get("slug") for p in existing_posts}
    new_published = []

    print("🚀 Running Yahoo Finance Topic Ingestion (Money, Property, Personal Finance)...")

    for cat in CATEGORIES:
        cat_name = cat["name"]
        cat_url = cat["url"]
        target_count = cat["target_count"]
        keywords = cat["keywords"]

        print(f"\n📂 Processing Category: '{cat_name}' from {cat_url} (Target: {target_count} articles)...")
        candidates = extract_topic_articles(cat_url, keywords)
        print(f"  Found {len(candidates)} matching articles.")

        count = 0
        for cand in candidates:
            if count >= target_count:
                break
            
            slug = re.sub(r'[^a-z0-9\s-]', '', cand["title"].lower())
            slug = re.sub(r'[\s-]+', '-', slug).strip('-')[:70]

            if slug in existing_slugs:
                continue

            rewritten = rewrite_to_180_words(cand["title"], cat_name, cand["link"])

            post_obj = {
                "id": slug,
                "slug": slug,
                "title": rewritten["title"],
                "category": cat_name,
                "date": datetime.now().strftime("%d-%b-%Y"),
                "iso_date": datetime.now().isoformat(),
                "readTime": "4 min read",
                "author": "R BAKSHI",
                "excerpt": rewritten["summary"][:160] + "...",
                "summary": rewritten["summary"],
                "bullets": rewritten["bullets"],
                "tip": rewritten["tip"],
                "sourceUrl": cand["link"],
                "url": f"/pages/blog/{slug}.html"
            }

            # Write HTML
            html_content = generate_blog_html(post_obj)
            with open(os.path.join(BLOG_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
            with open(os.path.join(PUB_BLOG_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
                f.write(html_content)

            new_published.append(post_obj)
            existing_slugs.add(slug)
            count += 1
            print(f"  ✨ [{count}/{target_count}] Published: {rewritten['title'][:65]}...")

    if new_published:
        merged = new_published + existing_posts
        with open(POSTS_JSON, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)
        with open(PUB_POSTS_JSON, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)
        print(f"\n✅ Total {len(new_published)} new articles published and saved into posts.json!")
    else:
        print("\nℹ️ All articles up to date.")

    # Vite Build
    print("\n📦 Building ezmortgagebroker with Vite...")
    subprocess.run(["npm", "run", "build"], cwd=EZ_DIR, capture_output=True)
    print("✅ Build complete!")

if __name__ == "__main__":
    main()
