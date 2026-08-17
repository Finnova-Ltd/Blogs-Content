#!/usr/bin/env python3
"""
EZ Mortgage Broker - Google Alerts RSS Feed Extractor & Article Generator
Fetches Google Alerts RSS feeds (Atom format), extracts latest Australian mortgage news,
and generates structured blog articles and updates posts.json.
"""

import urllib.request
import xml.etree.ElementTree as ET
import re
import json
import html
import os
import sys
from datetime import datetime

FEED_URL = "https://www.google.com/alerts/feeds/14625353401416373956/6439186835690371841"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON_PATH = os.path.join(PROJECT_DIR, "posts.json")
BLOG_PAGES_DIR = os.path.join(PROJECT_DIR, "pages", "blog")

def clean_html(text):
    if not text:
        return ""
    clean = re.sub(r'<.*?>', '', text)
    return html.unescape(clean).strip()

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

def fetch_feed_entries():
    req = urllib.request.Request(
        FEED_URL,
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    )
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    entries = []
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
        actual_url = extract_actual_url(raw_link)

        pub_date = datetime.now()
        if raw_pub:
            try:
                pub_date = datetime.fromisoformat(raw_pub.replace('Z', '+00:00'))
            except:
                pass

        entries.append({
            "title": clean_title,
            "url": actual_url,
            "date": pub_date.strftime("%d-%b-%Y"),
            "iso_date": raw_pub or pub_date.isoformat(),
            "snippet": clean_content,
            "slug": slugify(clean_title)
        })

    return entries

def generate_article_html(item):
    slug = item['slug']
    title = item['title']
    date = item['date']
    snippet = item['snippet']
    source_url = item['url']

    html_content = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{title} - Australian Mortgage Market Insights from EZ Mortgage Broker.">
  <title>{title} | EZ Mortgage Broker</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Lato:wght@300;400;600;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="/css/style.css">
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
          <a href="/">Home</a> &gt; <a href="/pages/blog.html">Blog &amp; Insights</a> &gt; <span>Market Update</span>
        </div>

        <div class="article-header">
          <span class="section-label" style="display:inline-block; padding:4px 14px; background:#EFF6FF; color:#1D4ED8; border-radius:20px; font-weight:800; font-size:0.8rem; letter-spacing:0.08em; border:1px solid #DBEAFE; margin-bottom:14px;">LENDING ADVISORY</span>
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
              <p>As market dynamics and lender credit policies evolve, Australian homebuyers and investors are actively reviewing their loan portfolios to optimize interest rates and loan features.</p>
              
              <div class="table-responsive-wrapper">
                <table class="content-data-table">
                  <thead>
                    <tr>
                      <th style="width:30%;">Key Aspect</th>
                      <th style="width:45%;">Current Market Reality</th>
                      <th style="width:25%;">Borrower Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Interest Rate Volatility</strong></td>
                      <td>Lenders are competing heavily with unadvertised broker-only discretionary discounts.</td>
                      <td><span style="color:#16A34A; font-weight:700;">✓ Request rate review</span></td>
                    </tr>
                    <tr>
                      <td><strong>Borrowing Power Rules</strong></td>
                      <td>APRA serviceability buffers continue to shape maximum pre-approval limits.</td>
                      <td><span style="color:#16A34A; font-weight:700;">✓ Compare 50+ lenders</span></td>
                    </tr>
                    <tr>
                      <td><strong>Refinancing Opportunities</strong></td>
                      <td>Switching loans can reduce monthly repayment burdens and consolidate high-interest debts.</td>
                      <td><span style="color:#16A34A; font-weight:700;">✓ Calculate net savings</span></td>
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
              <p>Our senior credit advisors access wholesale rate cards and specialized credit policies across 50+ Australian lenders. We analyze your situation at zero cost to find the loan that fits your financial goals.</p>
              <div style="margin-top:20px;">
                <a href="/#contact" class="btn btn-primary" style="padding:12px 24px; font-weight:700; background:#0A2540; color:#ffffff; border-radius:8px; text-decoration:none; display:inline-block;">Book Free Broker Assessment &rarr;</a>
              </div>
            </div>
          </div>

          <div style="background:#F1F5F9; border-left:4px solid #3B82F6; padding:16px 20px; border-radius:0 8px 8px 0; margin-top:32px;">
            <p style="margin:0; font-size:0.88rem; color:#475569;">
              <strong>Source Reference:</strong> Originally reported by independent financial media. View reporting: <a href="{source_url}" target="_blank" rel="noopener noreferrer" style="color:#1D4ED8; word-break:break-all;">{source_url}</a>
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
                  <p class="highlight-item-summary">Rate fluctuations &amp; unadvertised discounts</p>
                </div>
              </a>
              <a href="#section-2" class="highlight-timeline-item" data-target="2">
                <span class="highlight-timeline-dot"></span>
                <div class="highlight-item-content">
                  <span class="highlight-item-tag">Broker Strategy</span>
                  <p class="highlight-item-summary">50+ lender comparison at zero fee</p>
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
    print(f"📡 Fetching Google Alerts feed from: {FEED_URL}")
    entries = fetch_feed_entries()
    print(f"✅ Found {len(entries)} alerts in feed.")

    if "--publish" in sys.argv or "--generate" in sys.argv:
        published_count = 0
        os.makedirs(BLOG_PAGES_DIR, exist_ok=True)
        
        for item in entries:
            out_file = os.path.join(BLOG_PAGES_DIR, f"{item['slug']}.html")
            if not os.path.exists(out_file):
                page_html = generate_article_html(item)
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(page_html)
                published_count += 1
                print(f"  📝 Generated new article: {out_file}")
        
        print(f"🎉 Generated {published_count} new articles from Google Alerts feed!")
    else:
        print("\nSample Extracted Alerts:")
        for idx, item in enumerate(entries[:5], 1):
            print(f"  {idx}. {item['title']}")
            print(f"     Source: {item['url']}")
            print(f"     Snippet: {item['snippet'][:90]}...")

if __name__ == "__main__":
    main()
