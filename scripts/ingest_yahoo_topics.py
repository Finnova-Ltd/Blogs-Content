#!/usr/bin/env python3
"""
Yahoo Finance Australia & Multi-Topic Ingestion Engine
Updates card image overlays with:
- Top-Left: Date badge (23 AUG)
- Top-Right: Category pill
- Bottom-Left: Relative time added + read time
- Bottom-Right: Views and likes
"""

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

ROOT_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
POSTS_JSON = os.path.join(ROOT_DIR, "posts.json")
PUB_POSTS_JSON = os.path.join(ROOT_DIR, "public", "posts.json")
PAGES_BLOG_DIR = os.path.join(ROOT_DIR, "pages", "blog")
PUB_PAGES_BLOG_DIR = os.path.join(ROOT_DIR, "public", "pages", "blog")
INDEX_HTML = os.path.join(ROOT_DIR, "index.html")
PUB_INDEX_HTML = os.path.join(ROOT_DIR, "public", "index.html")

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
        
        matches = re.findall(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL)
        seen = set()
        for href, text in matches:
            clean_text = re.sub(r'<.*?>', '', text).strip()
            clean_text = html.unescape(clean_text)
            if len(clean_text) < 25 or len(clean_text) > 160:
                continue
            if any(skip in clean_text.lower() for skip in ["privacy", "terms", "sign in", "yahoo", "cookie", "skip to", "feedback"]):
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

def generate_sleek_card_html(p, idx):
    t = p.get("title", "")
    slug = p.get("slug", "")
    cat = p.get("category", "Money & Banking")
    img = p.get("heroImage") or p.get("image") or "https://images.pexels.com/photos/1181354/pexels-photo-1181354.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
    d_str = "23-Aug-2026"
    read_time = p.get("readTime", "4 min read")
    views = p.get("baseViews", 1400 + (idx * 40))
    likes = p.get("baseLikes", 110 + (idx * 8))
    exc = p.get("excerpt", "")
    url = f"/pages/blog/{slug}.html"

    time_offsets = ["Added 40 mins ago", "Added 2 hours ago", "Added 4 hours ago", "Added 6 hours ago", "Added 8 hours ago"]
    rel_time = time_offsets[idx % len(time_offsets)]

    cat_bg = "#1D4ED8" if "Banking" in cat or "Money" in cat else ("#00876C" if "Property" in cat or "Housing" in cat else "#7C3AED")

    return f"""        <!-- Sleek Image Overlay Card: {html.escape(t[:32])} -->
        <article class="insight-card fade-up" style="background:#ffffff; border:1.5px solid #E2E8F0; border-radius:16px; overflow:hidden; display:flex; flex-direction:column; box-shadow:0 6px 20px rgba(10,37,64,0.05); transition:transform 0.25s ease, box-shadow 0.25s ease;">
          <div class="insight-img-wrap" style="position:relative; height:225px; overflow:hidden; background:#0A2540;">
            <a href="{url}" aria-label="Read {html.escape(t)}" style="display:block; width:100%; height:100%;">
              <img src="{img}" alt="{html.escape(t)}" width="400" height="225" loading="lazy" style="width:100%; height:100%; object-fit:cover; display:block; transition:transform 0.5s ease;">
            </a>
            
            <!-- Top-Left: Date Badge (23 AUG) -->
            <div style="position:absolute; top:12px; left:12px; background:#ffffff; border-radius:8px; padding:5px 12px; text-align:center; box-shadow:0 4px 14px rgba(0,0,0,0.22); line-height:1.1; pointer-events:none; z-index:3;">
              <span style="display:block; font-size:1.15rem; font-weight:900; color:#0A2540;">23</span>
              <span style="display:block; font-size:0.68rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.05em;">AUG</span>
            </div>

            <!-- Top-Right: Category Pill -->
            <div style="position:absolute; top:12px; right:12px; background:{cat_bg}; color:#ffffff; font-size:0.72rem; font-weight:800; padding:5px 12px; border-radius:20px; text-transform:uppercase; letter-spacing:0.06em; box-shadow:0 2px 8px rgba(0,0,0,0.25); z-index:3;">
              {html.escape(cat)}
            </div>

            <!-- Bottom-Left: Relative Time Added & Read Time -->
            <div style="position:absolute; bottom:12px; left:12px; background:rgba(10,37,64,0.88); backdrop-filter:blur(6px); color:#ffffff; font-size:0.72rem; font-weight:700; padding:5px 10px; border-radius:6px; box-shadow:0 2px 8px rgba(0,0,0,0.25); display:inline-flex; align-items:center; gap:6px; z-index:3; pointer-events:none;">
              <span>🕒 {rel_time}</span> · <span>⏱️ {read_time}</span>
            </div>

            <!-- Bottom-Right: Views and Likes -->
            <div style="position:absolute; bottom:12px; right:12px; background:rgba(10,37,64,0.88); backdrop-filter:blur(6px); color:#ffffff; font-size:0.72rem; font-weight:700; padding:5px 10px; border-radius:6px; box-shadow:0 2px 8px rgba(0,0,0,0.25); display:inline-flex; align-items:center; gap:8px; z-index:3; pointer-events:none;">
              <span>👁️ {views:,}</span>
              <span>❤️ {likes}</span>
            </div>
          </div>

          <div class="insight-body" style="padding:22px 20px; display:flex; flex-direction:column; flex-grow:1;">
            <h3 style="font-size:1.15rem; font-weight:800; line-height:1.42; margin:0 0 12px;">
              <a href="{url}" style="color:#0A2540; text-decoration:none; transition:color 0.2s ease;">{html.escape(t)}</a>
            </h3>
            <p style="color:#475569; font-size:0.9rem; line-height:1.6; margin:0 0 20px; flex-grow:1;">{html.escape(exc[:145])}...</p>

            <!-- Bottom Progress Line & Read Article Button -->
            <div style="margin-top:auto; padding-top:14px; border-top:1px solid #F1F5F9; display:flex; align-items:center; justify-content:space-between;">
              <div style="height:3.5px; width:45%; background:linear-gradient(90deg, #1D4ED8, #38BDF8); border-radius:2px;"></div>
              <a href="{url}" style="font-size:0.88rem; font-weight:800; color:#1D4ED8; text-decoration:none; display:inline-flex; align-items:center; gap:4px;">
                Read Article &rarr;
              </a>
            </div>
          </div>
        </article>\n"""

def update_homepage_featured_articles(all_posts):
    if not all_posts:
        return
    top3 = all_posts[:3]
    cards_html = ""
    for idx, p in enumerate(top3):
        cards_html += generate_sleek_card_html(p, idx)

    grid_replacement = f'<div id="home-insights-grid" class="insights-grid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:28px;">\n{cards_html}      </div>'
    
    for idx_file in [INDEX_HTML, PUB_INDEX_HTML]:
        if os.path.exists(idx_file):
            try:
                with open(idx_file, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content = re.sub(r'<div id="home-insights-grid"[^>]*>.*?</div>\s*</div>\s*</section>', f'{grid_replacement}\n    </div>\n  </section>', content, flags=re.DOTALL)
                if new_content != content:
                    with open(idx_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ Updated featured news cards on {os.path.basename(idx_file)}!")
            except Exception as e:
                print(f"⚠️ Error updating {idx_file}: {e}")

def run_ingestion():
    print("🚀 Running Yahoo Finance Topic Ingestion Engine...")
    existing_posts = []
    if os.path.exists(POSTS_JSON):
        try:
            with open(POSTS_JSON, "r", encoding="utf-8") as f:
                existing_posts = json.load(f)
        except Exception:
            existing_posts = []

    existing_slugs = {p.get("slug") for p in existing_posts}
    new_posts = []
    d_str = "23-Aug-2026"
    
    for topic in TOPICS:
        name = topic["name"]
        url = topic["url"]
        keywords = topic["keywords"]
        cat = topic["category"]
        cat_color = topic["cat_color"]
        target_count = topic["target_count"]

        print(f"📡 Polling Yahoo Finance Australia: {name}...")
        articles = extract_topic_articles(url, keywords)
        print(f"   Found {len(articles)} relevant articles for {name}.")

        count_added = 0
        for art in articles:
            if count_added >= target_count:
                break
            
            t = art["title"]
            slug = slugify(t)
            if slug in existing_slugs or not slug:
                continue

            summary = f"Recent Australian market intelligence in {name.lower()} outlines key shifts impacting everyday borrowers, home buyers, and property investors. Industry data confirms changing bank policies across the market."
            image = fetch_pexels_image(f"australia mortgage finance real estate {t}")
            read_time = "4 min read"

            page_html = generate_complete_article_html(t, summary, "Yahoo Finance Australia", cat, cat_color, "#YahooFinance", image, d_str, read_time, slug)

            for d in [PAGES_BLOG_DIR, PUB_PAGES_BLOG_DIR]:
                with open(os.path.join(d, f"{slug}.html"), "w", encoding="utf-8") as pf:
                    pf.write(page_html)

            post_obj = {
                "id": slug,
                "slug": slug,
                "title": t,
                "excerpt": summary[:160] + "...",
                "category": cat,
                "tags": ["#MortgageAustralia", "#YahooFinance", "#PropertyInvestment", "#EZMortgageBroker"],
                "readTime": read_time,
                "timeAgo": "Just now",
                "publishedDate": d_str,
                "formattedDate": d_str,
                "isFeatured": True,
                "isTrending": True,
                "baseViews": 1400 + len(new_posts) * 40,
                "baseLikes": 110 + len(new_posts) * 8,
                "author": {
                    "name": "R BAKSHI",
                    "title": "Principal Mortgage Broker (MFAA Accredited)"
                },
                "heroImage": image,
                "sourceUrl": art["link"],
                "sourceName": "Yahoo Finance Australia",
                "url": f"/pages/blog/{slug}.html",
                "date": d_str
            }

            new_posts.append(post_obj)
            existing_slugs.add(slug)
            count_added += 1
            print(f"   ✨ Added: {t[:55]}...")

    # Update published dates of existing recent posts to 23-Aug-2026
    for p in existing_posts[:20]:
        p["publishedDate"] = d_str
        p["date"] = d_str
        p["formattedDate"] = d_str

    all_posts = new_posts + existing_posts
    with open(POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)
    with open(PUB_POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)

    update_homepage_featured_articles(all_posts)
    print(f"✅ Ingestion complete. Updated posts to 23-Aug-2026!")

if __name__ == "__main__":
    run_ingestion()
