import os
import sys
import re
import json
import html
import urllib.request
import urllib.parse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from pexels_client import fetch_pexels_image
from ingest_authority_sources import generate_complete_article_html, slugify

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON = os.path.join(ROOT_DIR, "posts.json")
PUB_POSTS_JSON = os.path.join(ROOT_DIR, "public", "posts.json")
PAGES_BLOG_DIR = os.path.join(ROOT_DIR, "pages", "blog")
PUB_PAGES_BLOG_DIR = os.path.join(ROOT_DIR, "public", "pages", "blog")

for p in [PAGES_BLOG_DIR, PUB_PAGES_BLOG_DIR]:
    os.makedirs(p, exist_ok=True)

TOPICS = [
    {
        "name": "Money & Banking",
        "url": "https://au.finance.yahoo.com/topic/money/",
        "keywords": ["mortgage", "bank", "interest", "rate", "loan", "rba", "savings", "debt", "lending", "cba", "westpac", "nab", "anz", "macquarie", "cashback", "inflation", "coles", "woolworths"],
        "category": "Money & Banking",
        "cat_color": "#1D4ED8",
        "target_count": 4
    },
    {
        "name": "Property & Housing",
        "url": "https://au.finance.yahoo.com/topic/property/",
        "keywords": ["house", "property", "home", "buyer", "housing", "rent", "investor", "landlord", "sydney", "melbourne", "brisbane", "auction", "prices", "apartment", "unit", "stamp duty"],
        "category": "Property & Housing",
        "cat_color": "#00876C",
        "target_count": 4
    },
    {
        "name": "Personal Finance & Centrelink",
        "url": "https://au.finance.yahoo.com/topic/personal-finance/",
        "keywords": ["tax", "super", "superannuation", "centrelink", "ato", "income", "cost of living", "pension", "salary", "cgt", "smsf", "retire"],
        "category": "Personal Finance & Centrelink",
        "cat_color": "#7C3AED",
        "target_count": 4
    }
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_topic_articles(topic_url, keywords):
    articles = []
    try:
        req = urllib.request.Request(topic_url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
        
        matches = re.findall(r"<a\\s+[^>]*href=[\x27\"]([^\x27\"]+)[\x27\"][^>]*>(.*?)</a>", content, re.IGNORECASE | re.DOTALL)
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

def run_ingestion():
    print("🚀 Running Yahoo Finance Topic Ingestion with Full Accordion & 5-Widget Standard...")
    existing_posts = []
    if os.path.exists(POSTS_JSON):
        try:
            with open(POSTS_JSON, "r", encoding="utf-8") as f:
                existing_posts = json.load(f)
        except Exception:
            existing_posts = []

    existing_slugs = {p.get("slug") for p in existing_posts}
    new_posts = []

    for topic in TOPICS:
        name = topic["name"]
        cat = topic["category"]
        color = topic["cat_color"]
        url = topic["url"]
        keywords = topic["keywords"]
        target = topic["target_count"]

        print(f"📂 Processing Category: '{name}' from {url}...")
        articles = extract_topic_articles(url, keywords)
        
        count = 0
        for art in articles:
            if count >= target:
                break
            
            t = art["title"]
            slug = slugify(t)
            if slug in existing_slugs or not slug:
                continue

            summary = f"Recent Australian market intelligence in {cat.lower()} outlines key shifts impacting everyday borrowers, home buyers, and property investors. Navigating these updates proactively allows borrowers to safeguard their serviceability buffers and unlock strategic financing solutions."
            image = fetch_pexels_image(f"australia finance mortgage property {t}")
            d_str = datetime.now().strftime("%d-%b-%Y")
            read_time = "5 min read"

            page_html = generate_complete_article_html(t, summary, f"Yahoo Finance {name}", cat, color, "#YahooFinance", image, d_str, read_time, slug)
            
            for d in [PAGES_BLOG_DIR, PUB_PAGES_BLOG_DIR]:
                with open(os.path.join(d, f"{slug}.html"), "w", encoding="utf-8") as pf:
                    pf.write(page_html)

            post_obj = {
                "id": slug,
                "slug": slug,
                "title": t,
                "excerpt": summary[:160] + "...",
                "category": cat,
                "tags": ["#MortgageAustralia", "#HomeLoans", "#YahooFinance", "#EZMortgageBroker"],
                "readTime": read_time,
                "timeAgo": "Just now",
                "publishedDate": d_str,
                "formattedDate": d_str,
                "isFeatured": True,
                "isTrending": True,
                "baseViews": 1200 + len(new_posts) * 40,
                "baseLikes": 90 + len(new_posts) * 5,
                "author": {"name": "R BAKSHI", "title": "Principal Mortgage Broker"},
                "heroImage": image,
                "sourceUrl": art["link"],
                "sourceName": f"Yahoo Finance {name}",
                "url": f"/pages/blog/{slug}.html",
                "date": d_str
            }

            new_posts.append(post_obj)
            existing_slugs.add(slug)
            count += 1
            print(f"  ✨ [{count}/{target}] Published: {t[:60]}...")

    all_posts = new_posts + existing_posts
    with open(POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)
    with open(PUB_POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)

    print(f"✅ Total {len(new_posts)} new articles published adhering to standards!")

if __name__ == "__main__":
    run_ingestion()
