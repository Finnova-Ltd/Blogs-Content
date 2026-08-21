#!/usr/bin/env python3
"""
EZ Mortgage Broker — Australian Industry Authority News Ingestion Engine
Fetches and publishes 1 daily high-authority article from:
1. AUSTRAC Media Releases (https://www.austrac.gov.au/news-and-media/news-and-media-releases)
2. Business News Australia (https://www.businessnewsaustralia.com)
3. MFAA News (https://www.mfaa.com.au/news)
4. FBAA NewsHub (https://www.fbaa.com.au/news-media/newshub/)
5. Australian Broker (https://www.brokernews.com.au/news/breaking-news/)
6. The Adviser (https://www.theadviser.com.au/news)
7. MPA Mag Australia (https://www.mpamag.com/au)
8. ABC News Mortgages (https://www.abc.net.au/news/topic/mortgages)
9. Mortgage Choice News (https://www.mortgagechoice.com.au/news/)
"""

import os
import sys
import re
import json
import html
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    from pexels_client import fetch_pexels_image
except ImportError:
    def fetch_pexels_image(q):
        return "https://images.pexels.com/photos/1181354/pexels-photo-1181354.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"

try:
    from unsplash_client import fetch_unsplash_image
except ImportError:
    def fetch_unsplash_image(q):
        return "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80"

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON = os.path.join(ROOT_DIR, "posts.json")
PUB_POSTS_JSON = os.path.join(ROOT_DIR, "public", "posts.json")
PAGES_BLOG_DIR = os.path.join(ROOT_DIR, "pages", "blog")
PUB_PAGES_BLOG_DIR = os.path.join(ROOT_DIR, "public", "pages", "blog")
RSS_FILE = os.path.join(ROOT_DIR, "rss.xml")
FEED_FILE = os.path.join(ROOT_DIR, "feed.xml")
PUB_RSS_FILE = os.path.join(ROOT_DIR, "public", "rss.xml")
PUB_FEED_FILE = os.path.join(ROOT_DIR, "public", "feed.xml")

for p in [PAGES_BLOG_DIR, PUB_PAGES_BLOG_DIR]:
    os.makedirs(p, exist_ok=True)

AUTHORITY_SOURCES = [
    {
        "name": "AUSTRAC Regulatory Intelligence",
        "category": "Compliance & Fraud Prevention",
        "site_query": "site:austrac.gov.au/news-and-media",
        "tag": "#AUSTRAC",
        "domain": "austrac.gov.au"
    },
    {
        "name": "MFAA Industry Leadership",
        "category": "Mortgage Broking & Policy",
        "site_query": "site:mfaa.com.au/news",
        "tag": "#MFAA",
        "domain": "mfaa.com.au"
    },
    {
        "name": "FBAA Broker Advocacy",
        "category": "Finance Broking & Rates",
        "site_query": "site:fbaa.com.au",
        "tag": "#FBAA",
        "domain": "fbaa.com.au"
    },
    {
        "name": "The Adviser Intelligence",
        "category": "Lending Strategy & Aggregators",
        "site_query": "site:theadviser.com.au",
        "tag": "#TheAdviser",
        "domain": "theadviser.com.au"
    },
    {
        "name": "Australian Broker Breaking",
        "category": "Bank Policies & Turnarounds",
        "site_query": "site:brokernews.com.au",
        "tag": "#AustralianBroker",
        "domain": "brokernews.com.au"
    },
    {
        "name": "MPA Mag Australia",
        "category": "Non-Bank & Commercial Lending",
        "site_query": "site:mpamag.com/au",
        "tag": "#MPAMag",
        "domain": "mpamag.com"
    },
    {
        "name": "ABC News Mortgages",
        "category": "RBA & Housing Economy",
        "site_query": "site:abc.net.au/news+mortgages",
        "tag": "#ABCNews",
        "domain": "abc.net.au"
    },
    {
        "name": "Business News Australia",
        "category": "Property Finance & M&A",
        "site_query": "site:businessnewsaustralia.com",
        "tag": "#BusinessNewsAU",
        "domain": "businessnewsaustralia.com"
    },
    {
        "name": "Mortgage Choice Market Insights",
        "category": "Home Loans & Refinancing",
        "site_query": "site:mortgagechoice.com.au",
        "tag": "#MortgageChoice",
        "domain": "mortgagechoice.com.au"
    }
]

def slugify(title):
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title).strip().lower()
    slug = re.sub(r'[\s_-]+', '-', clean)
    return slug[:75].rstrip('-')

def clean_html(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    return html.unescape(' '.join(text.split()))

def fetch_feed_items(site_query):
    encoded = urllib.parse.quote(site_query)
    feed_url = f"https://news.google.com/rss/search?q={encoded}&hl=en-AU&gl=AU&ceid=AU:en"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    items = []
    try:
        req = urllib.request.Request(feed_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
            for it in root.findall(".//item"):
                t = it.find("title").text if it.find("title") is not None else ""
                link = it.find("link").text if it.find("link") is not None else ""
                desc = it.find("description").text if it.find("description") is not None else ""
                pub = it.find("pubDate").text if it.find("pubDate") is not None else ""
                
                clean_t = re.sub(r'\s*-\s*[^-]+$', '', t).strip()
                if len(clean_t) > 20 and not any(k in clean_t.lower() for k in ["login", "terms of use", "privacy policy", "contact us"]):
                    items.append({
                        "title": clean_t,
                        "link": link,
                        "description": clean_html(desc),
                        "pubDate": pub
                    })
    except Exception as e:
        print(f"⚠️ Feed error ({site_query}): {e}")
    return items

def generate_article_content(title, summary, source_name, category, tag):
    slug = slugify(title)
    
    content_html = f"""
    <!-- Executive Summary & Direct Answer Card -->
    <div id="section-1" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 14px; padding: 24px; margin-bottom: 32px; scroll-margin-top: 100px;">
      <div style="color: #15803d; font-weight: 800; font-size: 0.85rem; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 0.9rem; color: #16a34a;">●</span> EXECUTIVE SUMMARY & DIRECT ANSWER
      </div>
      <p style="margin: 0; font-size: 1.05rem; line-height: 1.65; color: #1e293b; font-family: Georgia, serif;">
        {summary if len(summary) > 60 else title + " represents a key development across the Australian mortgage and lending landscape."} In recent industry advisories published by <strong>{source_name}</strong>, Australian mortgage brokers, borrowers, and commercial lenders are navigating critical shifts in credit policy, serviceability benchmarks, and regulatory oversight. For Australian property buyers, home loan refinancers, and commercial investors, understanding these macro changes is essential to locking in optimal borrowing capacity, avoiding lending rejections, and ensuring strict compliance with evolving APRA, ASIC, and AUSTRAC compliance standards.
      </p>
    </div>

    <!-- Section 1 -->
    <h2 style="font-size: 1.45rem; font-weight: 800; color: #0f172a; margin: 36px 0 16px 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">
      1. Australian Market Context & Lending Insights
    </h2>
    <p style="font-size: 1.05rem; line-height: 1.7; color: #334155; margin-bottom: 20px; font-family: Georgia, serif;">
      Across the Australian property market, changes in bank assessment interest rates (serviceability buffers) and lender turnaround times directly dictate how much everyday Aussies can borrow. In response to recent reports from {source_name}, mortgage brokers are leveraging real-time loan comparison engines to structure multi-tier lending applications across Big 4 banks (CBA, Westpac, NAB, ANZ) and leading non-bank specialist lenders.
    </p>

    <!-- Key Market Pillars -->
    <h3 style="font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 28px 0 14px 0; text-transform: uppercase; letter-spacing: 0.02em;">
      CORE LENDING & SERVICEABILITY HIGHLIGHTS:
    </h3>
    <ul style="list-style: none; padding: 0; margin: 0 0 32px 0; display: flex; flex-direction: column; gap: 14px;">
      <li style="display: flex; align-items: flex-start; gap: 10px; font-size: 1.02rem; line-height: 1.6; color: #334155; font-family: Georgia, serif;">
        <span style="color: #0284c7; font-weight: 900; font-size: 1.1rem; line-height: 1.3;">●</span>
        <span><strong style="color: #0f172a;">Serviceability & Buffer Analysis:</strong> Lenders assess applications with a mandatory +3.00% buffer above standard variable rates to test repayment durability.</span>
      </li>
      <li style="display: flex; align-items: flex-start; gap: 10px; font-size: 1.02rem; line-height: 1.6; color: #334155; font-family: Georgia, serif;">
        <span style="color: #0284c7; font-weight: 900; font-size: 1.1rem; line-height: 1.3;">●</span>
        <span><strong style="color: #0f172a;">Refinancing & Equity Release Velocity:</strong> Homeowners rolling off fixed rates are finding significant savings by comparing cashback promotions and negotiated discretionary discounts.</span>
      </li>
      <li style="display: flex; align-items: flex-start; gap: 10px; font-size: 1.02rem; line-height: 1.6; color: #334155; font-family: Georgia, serif;">
        <span style="color: #0284c7; font-weight: 900; font-size: 1.1rem; line-height: 1.3;">●</span>
        <span><strong style="color: #0f172a;">Regulatory Best Interests Duty (BID):</strong> Accredited Australian brokers are legally mandated under BID legislation to prioritize borrower outcomes over bank profitability.</span>
      </li>
    </ul>

    <!-- Section 2 -->
    <h2 id="section-2" style="font-size: 1.45rem; font-weight: 800; color: #0f172a; margin: 36px 0 16px 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; scroll-margin-top: 100px;">
      2. Technical & Policy Deep-Dive ({source_name})
    </h2>
    <p style="font-size: 1.05rem; line-height: 1.7; color: #334155; margin-bottom: 20px; font-family: Georgia, serif;">
      From an underwriting and credit assessment perspective, {source_name} emphasizes rigorous documentation validation, verified payslips, and comprehensive Comprehensive Credit Reporting (CCR) data. Modern digital identity verification (VOI) and Open Banking data sharing now allow pre-approvals to progress within 24–48 hours, significantly minimizing settlement risk for auction bidders and private treaty purchasers.
    </p>

    <!-- Section 3 -->
    <h2 id="section-3" style="font-size: 1.45rem; font-weight: 800; color: #0f172a; margin: 36px 0 16px 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; scroll-margin-top: 100px;">
      3. Regulatory Compliance & Consumer Protection
    </h2>
    <p style="font-size: 1.05rem; line-height: 1.7; color: #334155; margin-bottom: 20px; font-family: Georgia, serif;">
      With increased regulatory scrutiny from ASIC, APRA, and AUSTRAC regarding loan integrity and AML/CTF reporting standards, Australian finance brokers implement multi-point identity verification and anti-fraud safeguards. Borrowers benefit from transparent disclosure of commission models, total lifetime interest calculations, and tailored loan structuring (e.g. offset accounts vs. redraw facilities).
    </p>

    <!-- Section 4 -->
    <h2 id="section-4" style="font-size: 1.45rem; font-weight: 800; color: #0f172a; margin: 36px 0 16px 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; scroll-margin-top: 100px;">
      4. Implementation Roadmap & Borrower Action Checklist
    </h2>
    <p style="font-size: 1.05rem; line-height: 1.7; color: #334155; margin-bottom: 20px; font-family: Georgia, serif;">
      To maximize loan approval probability and secure top-tier interest rates, mortgage specialists recommend the following structured checklist:
    </p>
    <ul style="list-style: none; padding: 0; margin: 0 0 32px 0; display: flex; flex-direction: column; gap: 14px;">
      <li style="display: flex; align-items: flex-start; gap: 10px; font-size: 1.02rem; line-height: 1.6; color: #334155; font-family: Georgia, serif;">
        <span style="color: #10b981; font-weight: 900; font-size: 1.1rem; line-height: 1.3;">✓</span>
        <span><strong style="color: #0f172a;">Credit File & CCR Health Check:</strong> Audit your credit report for default errors or outdated credit cards prior to submitting formal applications.</span>
      </li>
      <li style="display: flex; align-items: flex-start; gap: 10px; font-size: 1.02rem; line-height: 1.6; color: #334155; font-family: Georgia, serif;">
        <span style="color: #10b981; font-weight: 900; font-size: 1.1rem; line-height: 1.3;">✓</span>
        <span><strong style="color: #0f172a;">Living Expense Harmonization:</strong> Minimize discretionary subscription overheads for 90 days before applying to boost borrowing capacity.</span>
      </li>
      <li style="display: flex; align-items: flex-start; gap: 10px; font-size: 1.02rem; line-height: 1.6; color: #334155; font-family: Georgia, serif;">
        <span style="color: #10b981; font-weight: 900; font-size: 1.1rem; line-height: 1.3;">✓</span>
        <span><strong style="color: #0f172a;">Multi-Lender Comparison:</strong> Compare over 40+ Australian wholesale & retail lenders through an accredited broker to negotiate fee waivers.</span>
      </li>
    </ul>

    <!-- Why It Matters Card -->
    <div style="background: #f0f7ff; border: 1px solid #bae0ff; border-radius: 14px; padding: 24px; margin-bottom: 28px;">
      <div style="color: #0050b3; font-weight: 800; font-size: 0.85rem; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 0.9rem; color: #0176D3;">●</span> WHY IT MATTERS & STRATEGIC ADVISORY
      </div>
      <p style="margin: 0; font-size: 1rem; line-height: 1.65; color: #1e293b; font-family: Georgia, serif;">
        <strong>How EZ Mortgage Broker Helps:</strong> Our team of licensed Australian mortgage brokers (MFAA / FBAA accredited) provides free loan health checks, borrowing power calculations, and direct rate negotiation across Australia's leading banks and non-bank lenders.
      </p>
    </div>

    <!-- Source Attribution -->
    <div style="font-size: 0.86rem; color: #64748b; font-style: italic; margin-bottom: 24px; display: flex; align-items: center; gap: 6px;">
      <span style="color: #ef4444;">🖋️</span> Source: {source_name} Official Advisory ({tag}).
    </div>
    """
    return content_html

def run_ingestion():
    print("🚀 Starting Australian Industry Authority News Ingestion Engine...")
    
    existing_posts = []
    if os.path.exists(POSTS_JSON):
        try:
            with open(POSTS_JSON, "r", encoding="utf-8") as f:
                existing_posts = json.load(f)
        except Exception:
            existing_posts = []
            
    existing_slugs = {p.get("slug") for p in existing_posts}
    new_posts = []
    
    for src in AUTHORITY_SOURCES:
        name = src["name"]
        cat = src["category"]
        query = src["site_query"]
        tag = src["tag"]
        
        print(f"📡 Polling {name} ({query})...")
        items = fetch_feed_items(query)
        print(f"   Found {len(items)} candidates.")
        
        published_for_source = False
        for it in items:
            t = it["title"]
            slug = slugify(t)
            
            if slug in existing_slugs or not slug:
                continue
                
            summary = it["description"] or f"Latest Australian lending analysis and regulatory updates from {name}."
            image = fetch_pexels_image(f"australia mortgage finance real estate {t}")
            
            content_html = generate_article_content(t, summary, name, cat, tag)
            d_str = datetime.now().strftime("%d %B %Y")
            
            post_obj = {
                "id": slug,
                "slug": slug,
                "title": t,
                "excerpt": summary[:160] + "...",
                "category": cat,
                "tags": ["#MortgageAustralia", "#HomeLoans", "#PropertyFinance", tag, "#EZMortgageBroker"],
                "readTime": "5 min read",
                "timeAgo": "Just now",
                "publishedDate": d_str,
                "formattedDate": d_str,
                "isFeatured": True,
                "isTrending": True,
                "baseViews": 1150 + len(new_posts) * 35,
                "baseLikes": 88 + len(new_posts) * 6,
                "author": {
                    "name": "EZ MORTGAGE RESEARCH",
                    "title": "Principal Lending & Credit Strategist"
                },
                "heroImage": image,
                "sourceUrl": it["link"],
                "sourceName": name,
                "highlights": [
                    {"id": "section-1", "time": "9:00 AM", "title": "Market Context & Lending Insights", "text": f"Strategic assessment of {t[:45]}..."},
                    {"id": "section-2", "time": "8:15 AM", "title": "Technical & Policy Deep-Dive", "text": f"Serviceability buffers, assessment rates, and lender turnaround times from {name}."},
                    {"id": "section-3", "time": "7:30 AM", "title": "Regulatory Compliance & Best Interests Duty", "text": "Alignment with APRA, ASIC, and AUSTRAC consumer credit standards."},
                    {"id": "section-4", "time": "6:45 AM", "title": "Borrower Roadmap & Action Checklist", "text": "4-phase checklist for credit file checks, expense audits, and rate negotiation."}
                ],
                "toc": [
                    {"id": "section-1", "title": "1. Australian Market Context"},
                    {"id": "section-2", "title": f"2. Technical & Policy Deep-Dive ({name})"},
                    {"id": "section-3", "title": "3. Regulatory Compliance & BID"},
                    {"id": "section-4", "title": "4. Borrower Action Checklist"}
                ],
                "content": content_html,
                "date": d_str,
                "url": f"/pages/blog/{slug}.html"
            }
            
            page_html = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(t)} | EZ Mortgage Broker Advisory</title>
    <meta name="description" content="{html.escape(summary[:160])}">
    <link rel="canonical" href="https://ezmortgagebroker.com.au/pages/blog/{slug}.html">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans antialiased min-h-screen">
    <main class="max-w-4xl mx-auto px-6 py-12">
        <h1 class="text-3xl font-bold text-emerald-400 mb-6">{html.escape(t)}</h1>
        <div class="bg-white text-slate-800 p-8 rounded-xl shadow-lg leading-relaxed">
            {content_html}
        </div>
    </main>
</body>
</html>"""
            for d in [PAGES_BLOG_DIR, PUB_PAGES_BLOG_DIR]:
                with open(os.path.join(d, f"{slug}.html"), "w", encoding="utf-8") as pf:
                    pf.write(page_html)
                    
            new_posts.append(post_obj)
            existing_slugs.add(slug)
            published_for_source = True
            print(f"   ✨ Published 1 article from {name}: {t[:60]}...")
            break
            
        if not published_for_source:
            print(f"   ℹ️ No new un-published stories for {name}.")

    all_posts = new_posts + existing_posts
    with open(POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)
    with open(PUB_POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)
        
    print(f"✅ Ingestion complete. Added {len(new_posts)} new articles. Total catalog: {len(all_posts)} articles.")

if __name__ == "__main__":
    run_ingestion()
