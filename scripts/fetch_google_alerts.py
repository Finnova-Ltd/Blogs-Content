#!/usr/bin/env python3
"""
EZ Mortgage Broker - Multi-Feed Google Alerts Extractor & Unique Content Publisher
Supports multiple feeds (Mortgages, Home Loans, Banking & Rates),
filters off-topic noise, de-duplicates cross-feed entries, and generates
unique, high-quality SEO-compliant articles.
"""

import urllib.request
import xml.etree.ElementTree as ET
import re
import json
import html
import os
import sys
import hashlib
from datetime import datetime

# Multi-Category Google Alerts RSS Feeds
ALERT_FEEDS = [
    {
        "category": "Mortgages",
        "badge": "MORTGAGE INSIGHTS",
        "url": "https://www.google.com/alerts/feeds/14625353401416373956/6439186835690371841"
    },
    {
        "category": "Home Loans",
        "badge": "HOME LOANS",
        "url": "https://www.google.com/alerts/feeds/14625353401416373956/10202701407179381699"
    },
    {
        "category": "Banking & Rates",
        "badge": "BANKING & RATES",
        "url": "https://www.google.com/alerts/feeds/14625353401416373956/1252910617246611092"
    }
]

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON_PATH = os.path.join(PROJECT_DIR, "posts.json")
BLOG_PAGES_DIR = os.path.join(PROJECT_DIR, "pages", "blog")

# Keywords to filter out off-topic / clickbait / sports / overseas politics
IRRELEVANT_KEYWORDS = [
    "basketball", "bruins", "nbl", "trump", "iran", "defamation",
    "fired 900 workers", "zoom", "solar battery", "aviation",
    "properties open for inspection", "mitcham", "resells for $17 million"
]

def clean_html(text):
    if not text:
        return ""
    clean = re.sub(r'<.*?>', '', text)
    return html.unescape(clean).strip()

def normalize_title(title):
    # Remove news outlet suffixes like " - AFR", " - ABC News", " | The Australian"
    norm = re.sub(r'\s*[-|–]\s*(AFR|The Australian|ABC News|The Age|The Adviser|Broker Daily|Broker News|Courier Mail|Sydney Morning Herald|SMH|Kalkine|Yahoo Finance|Motley Fool|Mirage News|Built Offsite|The Nightly).*$', '', title, flags=re.IGNORECASE)
    # Remove prefix tags like "VIDEO: "
    norm = re.sub(r'^(VIDEO|AUDIO|PODCAST|EXCLUSIVE):\s*', '', norm, flags=re.IGNORECASE)
    return norm.strip()

def is_relevant_mortgage_topic(title, snippet):
    combined = (title + " " + snippet).lower()
    for bad_word in IRRELEVANT_KEYWORDS:
        if bad_word in combined:
            return False
    # Must contain relevant Australian mortgage/banking/finance keywords
    relevant_terms = [
        "mortgage", "home loan", "lending", "lender", "bank", "interest rate",
        "rba", "refinanc", "first home", "fhb", "fhog", "deposit", "equity",
        "borrower", "borrowing", "broker", "apra", "cba", "nab", "westpac", "anz"
    ]
    return any(term in combined for term in relevant_terms)

def extract_actual_url(google_url):
    match = re.search(r'url=(https?://[^&]+)', google_url)
    if match:
        return match.group(1)
    return google_url

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')[:75]

def get_existing_slugs_and_titles():
    existing_slugs = set()
    existing_titles = set()

    if os.path.exists(POSTS_JSON_PATH):
        try:
            with open(POSTS_JSON_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            posts = data if isinstance(data, list) else data.get('posts', [])
            for p in posts:
                if 'slug' in p:
                    existing_slugs.add(p['slug'])
                if 'title' in p:
                    existing_titles.add(normalize_title(p['title']).lower())
        except Exception as e:
            print(f"Warning reading posts.json: {e}")

    if os.path.exists(BLOG_PAGES_DIR):
        for f in os.listdir(BLOG_PAGES_DIR):
            if f.endswith('.html'):
                existing_slugs.add(f[:-5])

    return existing_slugs, existing_titles

def fetch_all_feeds():
    all_entries = []
    seen_fingerprints = set()

    for feed_info in ALERT_FEEDS:
        category = feed_info["category"]
        badge = feed_info["badge"]
        feed_url = feed_info["url"]

        try:
            req = urllib.request.Request(
                feed_url,
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()

            root = ET.fromstring(xml_data)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', ns):
                title_el = entry.find('atom:title', ns)
                link_el = entry.find('atom:link', ns)
                pub_el = entry.find('atom:published', ns)
                content_el = entry.find('atom:content', ns)

                raw_title = title_el.text if title_el is not None else ""
                raw_link = link_el.get('href') if link_el is not None else ""
                raw_pub = pub_el.text if pub_el is not None else ""
                raw_content = content_el.text if content_el is not None else ""

                clean_title = clean_html(raw_title)
                clean_content = clean_html(raw_content)
                norm_title = normalize_title(clean_title)
                actual_url = extract_actual_url(raw_link)

                # Filter out irrelevant / noise topics
                if not is_relevant_mortgage_topic(norm_title, clean_content):
                    continue

                # De-duplicate fingerprint based on normalized title words
                fingerprint = re.sub(r'[^a-z0-9]', '', norm_title.lower())[:45]
                if fingerprint in seen_fingerprints:
                    continue
                seen_fingerprints.add(fingerprint)

                # Parse publication date
                pub_date = datetime.now()
                if raw_pub:
                    try:
                        pub_date = datetime.fromisoformat(raw_pub.replace('Z', '+00:00'))
                    except:
                        pass

                slug = slugify(norm_title)
                all_entries.append({
                    "title": norm_title,
                    "original_title": clean_title,
                    "category": category,
                    "badge": badge,
                    "url": actual_url,
                    "date": pub_date.strftime("%d-%b-%Y"),
                    "iso_date": raw_pub or pub_date.isoformat(),
                    "snippet": clean_content,
                    "slug": slug,
                    "fingerprint": fingerprint
                })
        except Exception as err:
            print(f"⚠️ Error fetching feed {feed_url}: {err}")

    return all_entries

def generate_article_html(item):
    slug = item['slug']
    title = item['title']
    date = item['date']
    snippet = item['snippet']
    source_url = item['url']
    badge = item['badge']
    category = item['category']

    html_content = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{title} - Australian mortgage and lending market analysis by EZ Mortgage Broker.">
  <title>{title} | EZ Mortgage Broker</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Lato:wght@300;400;600;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="canonical" href="https://ezmortgagebroker.com.au/pages/blog/{slug}.html">
</head>
<body>

  <!-- ========== SITE HEADER ========== -->
  <header class="site-header">
    <div class="header-top">
      <div class="container header-top-inner">
        <div class="breaking-news-ticker" id="breakingNewsTicker">
          <strong class="breaking-news-badge">⚡ BREAKING NEWS</strong>
          <a href="https://www.mfaa.com.au/news" target="_blank" rel="noopener noreferrer" class="breaking-news-title" id="breakingNewsTitle">Mortgage brokers settle record 81.0% of all Australian residential home loans</a>
        </div>
        <div class="header-contact-group">
          <span id="headerCurrentDate" class="header-date">📅 {date}</span>
          <span id="headerWeatherWidget" class="header-weather">☀️ Melbourne 18°C</span>
          <a href="tel:1300050099">📞 1300 050 099</a>
          <a href="mailto:info@ezmortgagebroker.com.au">✉️ info@ezmortgagebroker.com.au</a>
          <span>📍 Melbourne, VIC</span>
        </div>
      </div>
    </div>
    <div class="header-main">
      <div class="container">
        <div class="header-inner">
          <a href="/" class="logo"><img class="brand-logo" src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" style="max-width:200px; height:auto; display:inline-block;"></a>
          <nav>
            <ul class="nav-primary">
              <li><a href="/">Home</a></li>
              <li><a href="/#loan-solutions" class="nav-tab-link" data-tab="home-loans">Home Loans</a></li>
              <li><a href="/#loan-solutions" class="nav-tab-link" data-tab="business-loans">Business Loans</a></li>
              <li><a href="/#loan-solutions" class="nav-tab-link" data-tab="personal-loans">Personal Loans</a></li>
              <li><a href="/calculators.html">Calculators</a></li>
              <li><a href="/pages/blog.html" class="active">Blog &amp; Insights</a></li>
              <li><a href="/#about">About</a></li>
              <li><a href="/#contact">Contact</a></li>
            </ul>
          </nav>
          <div class="header-cta-group">
            <a href="tel:1300050099" class="btn btn-outline">Call Us</a>
            <a href="/#contact" class="btn btn-primary">Book Consult</a>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Article Layout (2-Column Grid) -->
  <main class="article-detail-page section-pad" style="background:#F8FAFC; padding-top:40px;">
    <div class="container article-detail-grid">
      
      <!-- Article Content Column (Col 1) -->
      <article class="article-main-content">
        <div class="article-breadcrumb">
          <a href="/">Home</a> &gt; <a href="/pages/blog.html">Blog &amp; Insights</a> &gt; <span>{category}</span>
        </div>

        <div class="article-header">
          <span class="section-label" style="display:inline-block; padding:4px 14px; background:#EFF6FF; color:#1D4ED8; border-radius:20px; font-weight:800; font-size:0.8rem; letter-spacing:0.08em; border:1px solid #DBEAFE; margin-bottom:14px;">{badge}</span>
          <h1 style="font-size:clamp(1.8rem, 3.5vw, 2.5rem); color:#0A2540; font-weight:800; line-height:1.25; margin-bottom:16px;">{title}</h1>
          <div class="article-meta-row" style="display:flex; gap:16px; color:#64748B; font-size:0.88rem; margin-bottom:24px;">
            <span>📅 {date}</span>
            <span>⏱️ 4 min read</span>
            <span>✍️ EZ Mortgage Research Desk</span>
          </div>
        </div>

        <div class="article-body-content">
          <p class="lead-text" style="font-size:1.15rem; color:#1E293B; line-height:1.65; margin-bottom:24px;">
            {snippet}
          </p>

          <div class="article-section-accordion open" data-accordion-index="1">
            <button type="button" class="article-section-accordion-header" aria-expanded="true">
              <h2>1. Key Market Developments &amp; Impact on Borrowers</h2>
              <span class="section-accordion-icon">−</span>
            </button>
            <div class="article-section-accordion-body">
              <p>As lending conditions evolve across major Australian banks and specialist non-bank lenders, borrowers face shifting assessment rules, rate benchmarks, and borrowing capacity guidelines.</p>
              
              <div class="table-responsive-wrapper">
                <table class="content-data-table">
                  <thead>
                    <tr>
                      <th style="width:30%;">Market Factor</th>
                      <th style="width:45%;">Current Industry Situation</th>
                      <th style="width:25%;">Borrower Strategy</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Rate Movements &amp; Buffers</strong></td>
                      <td>APRA 3.0% serviceability stress test remains a primary determinant of pre-approval limits.</td>
                      <td><span style="color:#16A34A; font-weight:700;">✓ Check actual borrowing capacity</span></td>
                    </tr>
                    <tr>
                      <td><strong>Lender Competition</strong></td>
                      <td>Banks are offering unadvertised discretionary rate discounts through broker networks.</td>
                      <td><span style="color:#16A34A; font-weight:700;">✓ Compare 50+ lenders</span></td>
                    </tr>
                    <tr>
                      <td><strong>Refinancing &amp; Equity</strong></td>
                      <td>Borrowers with 20%+ equity can renegotiate lower margins or release capital.</td>
                      <td><span style="color:#16A34A; font-weight:700;">✓ Calculate repayment savings</span></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="article-section-accordion open" data-accordion-index="2">
            <button type="button" class="article-section-accordion-header" aria-expanded="true">
              <h2>2. How EZ Mortgage Broker Supports You</h2>
              <span class="section-accordion-icon">−</span>
            </button>
            <div class="article-section-accordion-body">
              <p>EZ Mortgage Broker compares hundreds of loan products across 50+ Australian lenders with zero broker fees for residential borrowers. We handle loan structuring, paperwork submission, and approval negotiations from start to finish.</p>
              <div style="margin-top:20px;">
                <a href="/#contact" class="btn btn-primary" style="padding:12px 24px; font-weight:700; background:#0A2540; color:#ffffff; border-radius:8px; text-decoration:none; display:inline-block;">Book Free Broker Assessment &rarr;</a>
              </div>
            </div>
          </div>

          <div style="background:#F1F5F9; border-left:4px solid #3B82F6; padding:16px 20px; border-radius:0 8px 8px 0; margin-top:32px;">
            <p style="margin:0; font-size:0.88rem; color:#475569;">
              <strong>Industry Source Reference:</strong> Originally reported across Australian financial news wires. Source: <a href="{source_url}" target="_blank" rel="noopener noreferrer" style="color:#1D4ED8; word-break:break-all;">{source_url}</a>
            </p>
          </div>
        </div>
      </article>

      <!-- Sidebar Column (Col 2 & Col 3) -->
      <aside class="article-sidebar">
        
        <!-- 1. Principal Broker Profile Card (Image 2) -->
        <div class="author-profile-box">
          <div class="author-profile-banner"></div>
          <div class="author-profile-avatar-wrap">
            <img src="../../images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker Logo" class="author-profile-avatar-img">
          </div>
          <div class="author-profile-content">
            <h3 class="author-profile-name">R Bakshi</h3>
            <p class="author-profile-title">EZ Mortgage Broker</p>
            <div class="author-rating-stars">★★★★★ <span>(14)</span></div>
            <div class="author-actions-col">
              <a href="/#contact" class="author-action-btn">💬 Book Appointment</a>
              <a href="tel:1300050099" class="author-action-btn">📱 Send Message</a>
              <a href="/#contact" class="author-action-btn">📇 Contact Card</a>
            </div>
          </div>
        </div>

        <!-- 2. Article Highlights Accordion Widget (Image 1 - Below Image 2) -->
        <div class="article-highlights-widget open" id="articleHighlightsWidget">
          <button type="button" class="highlights-widget-header" aria-expanded="true">
            <h3>Highlights</h3>
            <span class="highlights-accordion-icon">−</span>
          </button>
          <div class="highlights-widget-body">
            <div class="highlights-date-label">— {date}</div>
            <div class="highlights-timeline">
              <a href="#section-1" class="highlight-timeline-item" data-target="1">
                <span class="highlight-timeline-dot"></span>
                <div class="highlight-item-content">
                  <span class="highlight-item-tag">Market Reality</span>
                  <p class="highlight-item-summary">Interest rate buffers &amp; lender competition</p>
                </div>
              </a>
              <a href="#section-2" class="highlight-timeline-item" data-target="2">
                <span class="highlight-timeline-dot"></span>
                <div class="highlight-item-content">
                  <span class="highlight-item-tag">Broker Strategy</span>
                  <p class="highlight-item-summary">Compare 50+ lenders at zero cost to you</p>
                </div>
              </a>
            </div>
            <div class="highlights-footer-btn-wrap">
              <button type="button" class="btn-more-highlights" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">Top of Article ↑</button>
            </div>
          </div>
        </div>

        <!-- 3. Google Reviews Accordion Widget -->
        <div class="sidebar-accordion-widget google-reviews-sidebar open">
          <button type="button" class="sidebar-accordion-header" aria-expanded="true">
            <h4>Google Reviews</h4>
            <span class="sidebar-accordion-icon">−</span>
          </button>
          <div class="sidebar-accordion-body">
            <div class="review-mini-item">
              <div class="review-mini-author">Jaspreet Sidhu</div>
              <div class="review-mini-stars">★★★★★</div>
              <p class="review-mini-text">"EZ Mortgage Broker has helped me since 2018 for all my financial needs. Very professional, honest and reliable."</p>
            </div>
          </div>
        </div>

      </aside>

    </div>
  </main>

  <script src="../../js/main.js"></script>
  <script src="../../js/article-state-tabs.js"></script>
</body>
</html>"""
    return html_content

def main():
    print(f"📡 Fetching from {len(ALERT_FEEDS)} Google Alert categories...")
    entries = fetch_all_feeds()
    print(f"✅ Filtered and extracted {len(entries)} unique relevant mortgage & banking stories.")

    existing_slugs, existing_titles = get_existing_slugs_and_titles()

    if "--publish" in sys.argv or "--generate" in sys.argv:
        published_count = 0
        os.makedirs(BLOG_PAGES_DIR, exist_ok=True)

        for item in entries:
            slug = item['slug']
            norm_title = item['title'].lower()

            # Strict uniqueness check
            if slug in existing_slugs or norm_title in existing_titles:
                print(f"  ⏭️ Skipping duplicate: {item['title']}")
                continue

            out_file = os.path.join(BLOG_PAGES_DIR, f"{slug}.html")
            page_html = generate_article_html(item)
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(page_html)

            existing_slugs.add(slug)
            existing_titles.add(norm_title)
            published_count += 1
            print(f"  ✨ Published new unique article: [{item['category']}] {item['title']}")

        print(f"\n🎉 Published {published_count} new unique articles across all categories!")
    else:
        print("\nSample Unique Extracted Stories:")
        for idx, item in enumerate(entries[:8], 1):
            print(f"  {idx}. [{item['category']}] {item['title']} ({item['date']})")
            print(f"     Snippet: {item['snippet'][:90]}...")

if __name__ == "__main__":
    main()
