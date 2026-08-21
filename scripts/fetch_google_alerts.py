#!/usr/bin/env python3
"""
EZ Mortgage Broker (ezmortgagebroker.com.au) - Production Automated Publisher
=============================================================================
Primary Domain Focus:
- RBA cash rate announcements & rate cycle tracking
- APRA serviceability buffers (3.0% stress test)
- First Home Buyer Grants (FHOG) & Stamp Duty Concessions in VIC/AU
- Fixed vs. Variable Refinancing Strategies

Target RSS Feeds:
1. https://news.google.com/rss/search?q=RBA+cash+rate+decision+OR+interest+rates+Australia&hl=en-AU&gl=AU&ceid=AU:en
2. https://news.google.com/rss/search?q=first+home+buyer+grant+Victoria+OR+stamp+duty+changes&hl=en-AU&gl=AU&ceid=AU:en
3. https://news.google.com/rss/search?q=APRA+mortgage+serviceability+buffer+banks&hl=en-AU&gl=AU&ceid=AU:en
4. https://www.google.com/alerts/feeds/14625353401416373956/6439186835690371841 (Mortgage)
5. https://www.google.com/alerts/feeds/14625353401416373956/10202701407179381699 (Home Loans)
6. https://www.google.com/alerts/feeds/14625353401416373956/1252910617246611092 (Banks)

150-200 Word Value-Dense Template:
1. H1 Headline: High-intent borrower question (8-12 words)
2. Direct Rate/Policy Summary: Direct figure, percentage change, and effective date (35-45 words)
3. Borrower Impact: 3 bullet points on borrowing power, monthly repayment differences, and lender response (60-75 words)
4. Action / Broker Tip: 1-2 sentences advising readers to calculate repayment buffer or review loan terms (35-45 words)
5. Schema: FinancialProduct + FAQPage + NewsArticle JSON-LD
6. Internal Linking: /calculators.html#borrowing-power, /calculators.html#refinance-savings, /pages/first-home-buyers.html
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import json
import html
import os
import sys
from datetime import datetime

SITE_URL = "https://ezmortgagebroker.com.au"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON_PATH = os.path.join(PROJECT_DIR, "posts.json")
BLOG_PAGES_DIR = os.path.join(PROJECT_DIR, "pages", "blog")

TARGET_FEEDS = [
    {
        "category": "Home Loans",
        "badge": "MORTGAGE MARKET ALERT",
        "url": "https://www.google.com/alerts/feeds/14625353401416373956/18413967573759855438",
        "feed_type": "google_alerts"
    },
    {
        "category": "Super & SMSF",
        "badge": "SUPER & SMSF INSIGHT",
        "url": "https://www.google.com/alerts/feeds/14625353401416373956/1200677753741493727",
        "feed_type": "google_alerts"
    },
    {
        "category": "RBA & Rates",
        "badge": "RBA & RATE CYCLE",
        "url": "https://news.google.com/rss/search?q=RBA+cash+rate+decision+OR+interest+rates+Australia&hl=en-AU&gl=AU&ceid=AU:en",
        "feed_type": "google_news"
    },
    {
        "category": "First Home Buyers",
        "badge": "FHOG & STAMP DUTY",
        "url": "https://news.google.com/rss/search?q=first+home+buyer+grant+Victoria+OR+stamp+duty+changes&hl=en-AU&gl=AU&ceid=AU:en",
        "feed_type": "google_news"
    },
    {
        "category": "APRA & Lending",
        "badge": "APRA & SERVICEABILITY",
        "url": "https://news.google.com/rss/search?q=APRA+mortgage+serviceability+buffer+banks&hl=en-AU&gl=AU&ceid=AU:en",
        "feed_type": "google_news"
    },
    {
        "category": "Refinancing",
        "badge": "REFINANCE STRATEGY",
        "url": "https://www.google.com/alerts/feeds/14625353401416373956/6439186835690371841",
        "feed_type": "google_alerts"
    },
    {
        "category": "Home Loans",
        "badge": "HOME LOAN BRIEF",
        "url": "https://www.google.com/alerts/feeds/14625353401416373956/10202701407179381699",
        "feed_type": "google_alerts"
    }
]

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
    norm = re.sub(r'\s*[-|–]\s*(AFR|The Australian|ABC News|The Age|The Adviser|Broker Daily|Broker News|Courier Mail|Sydney Morning Herald|SMH|Kalkine|Yahoo Finance|Motley Fool|Mirage News|Built Offsite|The Nightly).*$', '', title, flags=re.IGNORECASE)
    norm = re.sub(r'^(VIDEO|AUDIO|PODCAST|EXCLUSIVE):\s*', '', norm, flags=re.IGNORECASE)
    return norm.strip()

def is_relevant_mortgage_topic(title, snippet):
    combined = (title + " " + snippet).lower()
    for bad_word in IRRELEVANT_KEYWORDS:
        if bad_word in combined:
            return False
    relevant_terms = [
        "mortgage", "home loan", "superannuation", "super", "smsf", "lending", "lender", "bank", "interest rate",
        "rba", "refinanc", "first home", "fhb", "fhog", "stamp duty", "deposit", "equity",
        "borrower", "borrowing", "broker", "apra", "serviceability", "buffer", "cba", "nab", "westpac", "anz"
    ]
    return any(term in combined for term in relevant_terms)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')[:75]

def format_longtail_headline(raw_title, category):
    t = normalize_title(raw_title)
    if "rba" in t.lower() or "rate" in t.lower():
        return f"What Does the Latest RBA Rate Decision Mean for Variable Home Loans?"
    elif "first home" in t.lower() or "grant" in t.lower() or "stamp duty" in t.lower():
        return f"How Much Deposit Is Required for the First Home Guarantee in Victoria?"
    elif "apra" in t.lower() or "buffer" in t.lower() or "serviceability" in t.lower():
        return f"How Does the APRA 3.0% Serviceability Buffer Impact Borrowing Power?"
    elif "super" in t.lower() or "smsf" in t.lower():
        return f"How Can Australians Leverage Superannuation & SMSF Property Lending in 2026?"
    elif "refinanc" in t.lower() or "fixed" in t.lower():
        return f"What Are the Best Refinancing Strategies When Fixed Rates Expire?" 
    else:
        if not t.endswith('?'):
            return f"What Does {t} Mean for Australian Borrowers?"
        return t

def generate_value_dense_content(headline, snippet, category):
    """
    150-200 Word Value-Dense Template:
    1. Direct Rate/Policy Summary: Direct figure, percentage change, and effective date (35-45 words)
    2. Borrower Impact: 3 bullet points on borrowing power, monthly repayments, lender response (60-75 words)
    3. Action / Broker Tip: 1-2 sentences advising buffer review or loan health check (35-45 words)
    """
    if "rba" in headline.lower() or "rate" in category.lower():
        summary = "The Reserve Bank of Australia and major retail banks have updated residential mortgage assessment benchmarks. Variable mortgage rates across standard owner-occupier loans are adjusting in line with interbank cash rate trajectories and lender margin reviews."
        b1 = "<strong>Borrowing Capacity:</strong> Every 0.25% change shifts average household borrowing limits by approximately 2.5% to 3.0%."
        b2 = "<strong>Monthly Repayments:</strong> On a standard $600,000 mortgage, a 25 bps movement translates to roughly $95–$105 in monthly cash-flow adjustments."
        b3 = "<strong>Lender Pricing Discretion:</strong> Non-bank and second-tier lenders are introducing unadvertised rate discounts to attract quality refinancers."
        tip = "<strong>Broker Advisory:</strong> We recommend stress-testing your monthly budget with a 3.00% buffer and reviewing discretionary rate discounts across 30+ accredited lenders before your next statement cycle."
    elif "first home" in headline.lower() or "first home" in category.lower():
        summary = "First home buyers in Victoria and Australia-wide can access the Home Guarantee Scheme (5% deposit with zero Lenders Mortgage Insurance) alongside state-based First Home Owner Grants ($10,000) and stamp duty exemptions under $600,000 thresholds."
        b1 = "<strong>Deposit Multipliers:</strong> Eligible buyers need as little as 5% genuine savings, avoiding tens of thousands in upfront LMI costs."
        b2 = "<strong>Government Price Caps:</strong> Property price caps apply per capital city and regional zone across all participating lenders."
        b3 = "<strong>Pre-Approval Crucial:</strong> Scheme allocation places fill rapidly; securing conditional pre-approval ensures your spot is reserved before auction day."
        tip = "<strong>Broker Advisory:</strong> Speak with our team to verify whether your income and target purchase price meet federal and state scheme criteria at zero broker cost."
    elif "super" in category.lower() or "smsf" in category.lower():
        summary = "Australia's $4+ trillion superannuation system continues to evolve amid legislative debates on early access for housing, First Home Super Saver Scheme (FHSSS) rules, and Limited Recourse Borrowing Arrangements (LRBA) for property investment."
        b1 = "<strong>FHSSS Home Deposit Accelerators:</strong> Eligible buyers can withdraw up to $50,000 in voluntary contributions taxed at only 15% to build a home deposit faster."
        b2 = "<strong>SMSF Property Lending (LRBA):</strong> Self-Managed Super Funds can purchase residential and commercial investment property using specialized SMSF lending structures."
        b3 = "<strong>Contribution Caps & Tax Efficiency:</strong> Concessional super contributions offer substantial tax deductions while growing retirement equity."
        tip = "<strong>Broker Advisory:</strong> Speak with our SMSF finance specialists to structure compliant property loans inside your Self-Managed Super Fund with accredited lenders."
    elif "apra" in headline.lower() or "apra" in category.lower():
        summary = "APRA's 3.00% mortgage serviceability buffer requires Australian banks to evaluate loan affordability at least 300 basis points above the actual product interest rate, maintaining prudent lending standards across household credit."
        b1 = "<strong>Maximum Loan Caps:</strong> The 300 bps assessment hurdle limits the total debt-to-income multiple lenders can extend to applicants."
        b2 = "<strong>Alternative Assessment Pathways:</strong> Select non-bank lenders offer 1.0% to 2.0% buffer policies for like-for-like refinancers with pristine repayment history."
        b3 = "<strong>Living Expense Verification:</strong> Household Expenditure Measure (HEM) rules scrutinize actual living expenses during credit underwriting."
        tip = "<strong>Broker Advisory:</strong> If standard bank calculators restrict your borrowing limit, alternative policy lenders can frequently deliver the borrowing capacity you require."
    else:
        summary = "Australian mortgage market dynamics are presenting renewed opportunities for homeowners with over 20% equity to negotiate sharp pricing discounts and consolidate higher-interest credit cards or personal loans into lower-rate facilities."
        b1 = "<strong>Equity Cashout & Buffers:</strong> Unlocking usable home equity provides low-cost liquidity for property upgrades or investment diversification."
        b2 = "<strong>Loyalty Tax Elimination:</strong> Existing bank customers paying higher back-book rates can save $3,000+ annually by switching to active market rates."
        b3 = "<strong>Streamlined Refinance Valuations:</strong> Desktop automated valuations allow fast approvals without requiring full physical property inspections."
        tip = "<strong>Broker Advisory:</strong> Calculate your exact break-even refinance timeframe and request a comprehensive bank valuation report with our accredited mortgage team."

    return {
        "summary": summary,
        "bullets": [b1, b2, b3],
        "tip": tip
    }

def generate_article_html(item):
    slug = item['slug']
    raw_title = item['title']
    category = item['category']
    headline = format_longtail_headline(raw_title, category)
    date = item['date']
    iso_date = item['iso_date']
    source_url = item['url']
    badge = item['badge']
    canonical_url = f"{SITE_URL}/pages/blog/{slug}.html"

    content = generate_value_dense_content(headline, item['snippet'], category)

    # Injects FinancialProduct + FAQPage + NewsArticle JSON-LD Schema
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "NewsArticle",
                "headline": headline,
                "description": content["summary"][:155],
                "datePublished": iso_date,
                "dateModified": iso_date,
                "mainEntityOfPage": canonical_url,
                "author": {
                    "@type": "Organization",
                    "name": "EZ Mortgage Broker Research Desk",
                    "url": SITE_URL
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "EZ Mortgage Broker",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{SITE_URL}/images/ez-mortgage-broker.webp"
                    }
                }
            },
            {
                "@type": "FinancialProduct",
                "name": "Australian Residential Home Loan Assessment",
                "description": "Comprehensive home loan, refinancing, and first home buyer credit comparison across 30+ accredited Australian lenders.",
                "provider": {
                    "@type": "FinancialService",
                    "name": "EZ Mortgage Broker",
                    "telephone": "1300 050 099",
                    "url": SITE_URL
                }
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": headline,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": content["summary"]
                        }
                    }
                ]
            }
        ]
    }

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{content['summary'][:155]}">
  <title>{headline} | EZ Mortgage Broker</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Lato:wght@300;400;600;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="canonical" href="{canonical_url}">
  <script type="application/ld+json">
{json.dumps(json_ld, indent=2)}
  </script>
</head>
<body>

  <!-- ========== SITE HEADER ========== -->
  <header class="site-header">
    <div class="header-top">
      <div class="container header-top-inner">
        <div class="breaking-news-ticker" id="breakingNewsTicker">
          <strong class="breaking-news-badge">⚡ MARKET BRIEF</strong>
          <a href="/pages/blog.html" class="breaking-news-title">{headline}</a>
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
          <h1 style="font-size:clamp(1.75rem, 3.2vw, 2.4rem); color:#0A2540; font-weight:800; line-height:1.25; margin-bottom:16px;">{headline}</h1>
          <div class="article-meta-row" style="display:flex; gap:16px; color:#64748B; font-size:0.88rem; margin-bottom:24px;">
            <span>📅 {date}</span>
            <span>⏱️ 2 min read</span>
            <span>✍️ EZ Mortgage Research Desk</span>
          </div>
        </div>

        <!-- 150-200 Word Value-Dense Executive Briefing -->
        <div class="article-body-content" style="background:#ffffff; border:1.5px solid #E2E8F0; border-radius:16px; padding:28px; box-shadow:0 4px 16px rgba(10,37,64,0.03);">
          
          <!-- 1. Direct Rate & Policy Summary (35-45 words) -->
          <div style="background:#EFF6FF; border-left:4px solid #1D4ED8; padding:18px 20px; border-radius:0 10px 10px 0; margin-bottom:24px;">
            <strong style="display:block; color:#1E3A8A; font-size:0.88rem; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">⚡ Direct Policy &amp; Rate Summary</strong>
            <p style="margin:0; font-size:1.05rem; color:#1E293B; line-height:1.6; font-weight:500;">
              {content["summary"]}
            </p>
          </div>

          <!-- 2. Borrower Impact (60-75 words) -->
          <h3 style="font-size:1.15rem; color:#0A2540; font-weight:800; margin:24px 0 14px;">Borrower Impact &amp; Assessment Analysis:</h3>
          <ul style="list-style:none; padding:0; margin:0 0 24px; display:flex; flex-direction:column; gap:12px;">
            <li style="position:relative; padding-left:26px; color:#334155; font-size:0.95rem; line-height:1.55;">
              <span style="position:absolute; left:0; color:#16A34A; font-weight:800;">✓</span> {content["bullets"][0]}
            </li>
            <li style="position:relative; padding-left:26px; color:#334155; font-size:0.95rem; line-height:1.55;">
              <span style="position:absolute; left:0; color:#16A34A; font-weight:800;">✓</span> {content["bullets"][1]}
            </li>
            <li style="position:relative; padding-left:26px; color:#334155; font-size:0.95rem; line-height:1.55;">
              <span style="position:absolute; left:0; color:#16A34A; font-weight:800;">✓</span> {content["bullets"][2]}
            </li>
          </ul>

          <!-- 3. Action / Broker Tip (35-45 words) -->
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:18px 20px; border-radius:10px; margin-bottom:24px;">
            <p style="margin:0; font-size:0.95rem; color:#334155; line-height:1.6;">
              {content["tip"]}
            </p>
          </div>

          <!-- 4. Internal Linking Targets -->
          <div style="border-top:1px solid #E2E8F0; padding-top:18px; margin-top:20px; display:flex; flex-wrap:wrap; gap:14px; align-items:center;">
            <span style="font-size:0.82rem; font-weight:800; color:#64748B; text-transform:uppercase;">Calculate &amp; Compare:</span>
            <a href="/calculators.html#borrowing-power" style="color:#1D4ED8; font-weight:700; font-size:0.88rem; text-decoration:none;">Calculate Borrowing Power &rarr;</a>
            <a href="/calculators.html#refinance-savings" style="color:#1D4ED8; font-weight:700; font-size:0.88rem; text-decoration:none;">Refinance Savings &rarr;</a>
            <a href="/pages/first-home-buyers.html" style="color:#1D4ED8; font-weight:700; font-size:0.88rem; text-decoration:none;">First Home Buyer Hub &rarr;</a>
          </div>

          <!-- 5. Canonical / Source Attribution -->
          <div style="margin-top:20px; font-size:0.8rem; color:#94A3B8;">
            Industry Source Attribution: Sourced from verified Australian banking &amp; regulatory reports. <a href="{source_url}" target="_blank" rel="nofollow noopener noreferrer" style="color:#64748B;">View Source Notice &rarr;</a>
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
              <div class="highlight-timeline-item">
                <span class="highlight-timeline-dot"></span>
                <div class="highlight-item-content">
                  <span class="highlight-item-tag">Rate Summary</span>
                  <p class="highlight-item-summary">Key figures, buffer margins &amp; timing</p>
                </div>
              </div>
              <div class="highlight-timeline-item">
                <span class="highlight-timeline-dot"></span>
                <div class="highlight-item-content">
                  <span class="highlight-item-tag">Broker Strategy</span>
                  <p class="highlight-item-summary">Compare 30+ accredited lenders at zero cost to you</p>
                </div>
              </div>
            </div>
            <div class="highlights-footer-btn-wrap">
              <button type="button" class="btn-more-highlights" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">Top of Article ↑</button>
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

def fetch_feed_entries():
    all_entries = []
    seen_fingerprints = set()

    for feed_info in TARGET_FEEDS:
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
            
            # Support both RSS 2.0 (<item>) and Atom (<entry>)
            items = root.findall('.//item')
            if not items:
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                items = root.findall('atom:entry', ns)

            for entry in items:
                # RSS vs Atom title
                title_el = entry.find('title') if entry.find('title') is not None else entry.find('{http://www.w3.org/2005/Atom}title')
                link_el = entry.find('link') if entry.find('link') is not None else entry.find('{http://www.w3.org/2005/Atom}link')
                pub_el = entry.find('pubDate') if entry.find('pubDate') is not None else entry.find('{http://www.w3.org/2005/Atom}published')
                desc_el = entry.find('description') if entry.find('description') is not None else entry.find('{http://www.w3.org/2005/Atom}content')

                raw_title = title_el.text if title_el is not None else ""
                raw_link = link_el.text if (link_el is not None and link_el.text) else (link_el.get('href') if link_el is not None else "")
                raw_pub = pub_el.text if pub_el is not None else ""
                raw_desc = desc_el.text if desc_el is not None else ""

                clean_t = clean_html(raw_title)
                clean_d = clean_html(raw_desc)
                norm_t = normalize_title(clean_t)

                if not is_relevant_mortgage_topic(norm_t, clean_d):
                    continue

                fingerprint = re.sub(r'[^a-z0-9]', '', norm_t.lower())[:45]
                if fingerprint in seen_fingerprints:
                    continue
                seen_fingerprints.add(fingerprint)

                slug = slugify(norm_t)
                all_entries.append({
                    "title": norm_t,
                    "category": category,
                    "badge": badge,
                    "url": raw_link,
                    "date": datetime.now().strftime("%d-%b-%Y"),
                    "iso_date": datetime.now().isoformat(),
                    "snippet": clean_d,
                    "slug": slug,
                    "fingerprint": fingerprint
                })
        except Exception as err:
            print(f"⚠️ Feed read error {feed_url}: {err}")

    return all_entries

def main():
    print(f"📡 Polling {len(TARGET_FEEDS)} targeted EZ Mortgage Broker domain feeds...")
    entries = fetch_feed_entries()
    print(f"✅ Filtered {len(entries)} verified domain candidates.")

    existing_slugs, existing_titles = get_existing_slugs_and_titles()

    if "--publish" in sys.argv or "--generate" in sys.argv:
        published_count = 0
        new_posts_to_add = []
        os.makedirs(BLOG_PAGES_DIR, exist_ok=True)

        for item in entries:
            slug = item['slug']
            norm_title = item['title'].lower()

            if slug in existing_slugs or norm_title in existing_titles:
                continue

            out_file = os.path.join(BLOG_PAGES_DIR, f"{slug}.html")
            page_html = generate_article_html(item)
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(page_html)

            # Sync with public/pages/blog
            pub_out_file = os.path.join(PROJECT_DIR, "public", "pages", "blog", f"{slug}.html")
            os.makedirs(os.path.dirname(pub_out_file), exist_ok=True)
            with open(pub_out_file, 'w', encoding='utf-8') as f:
                f.write(page_html)

            existing_slugs.add(slug)
            existing_titles.add(norm_title)
            published_count += 1

            # Update posts.json list
            new_post_obj = {
                "id": slug,
                "slug": slug,
                "title": format_longtail_headline(item['title'], item['category']),
                "category": item['category'],
                "badge": item['badge'],
                "date": datetime.now().strftime("%d-%b-%Y"),
                "iso_date": datetime.now().isoformat(),
                "readTime": "2 min read",
                "author": "R BAKSHI",
                "authorRole": "Principal Mortgage Broker",
                "authorImg": "/images/ez-mortgage-broker.webp",
                "excerpt": item['snippet'][:160] + "...",
                "snippet": item['snippet'],
                "image": "/images/assets-ez-mortgage-broker/australian-home-mortgage-approval.jpg",
                "url": f"/pages/blog/{slug}.html"
            }
            new_posts_to_add.append(new_post_obj)
            print(f"  ✨ Published Value-Dense Domain Briefing: [{item['category']}] {item['title']}")

        # Save to posts.json
        if new_posts_to_add:
            try:
                current_posts = []
                if os.path.exists(POSTS_JSON_PATH):
                    with open(POSTS_JSON_PATH, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        current_posts = data if isinstance(data, list) else data.get('posts', [])
                
                # Prepend newest posts
                merged_posts = new_posts_to_add + [p for p in current_posts if p.get('slug') not in existing_slugs]
                with open(POSTS_JSON_PATH, 'w', encoding='utf-8') as f:
                    json.dump(merged_posts, f, indent=2)
                
                pub_posts_json = os.path.join(PROJECT_DIR, "public", "posts.json")
                with open(pub_posts_json, 'w', encoding='utf-8') as f:
                    json.dump(merged_posts, f, indent=2)
                print(f"✅ Synced {len(new_posts_to_add)} new briefings into posts.json!")
            except Exception as e:
                print(f"⚠️ Error updating posts.json: {e}")

        
        # Auto-syndicate newly published posts to Make.com flow
        if new_posts_to_add:
            try:
                from syndicate_to_make import syndicate_article
                print(f"\n🚀 Auto-Syndicating {len(new_posts_to_add)} new articles to Make.com flow...")
                for np in new_posts_to_add:
                    syndicate_article(np)
            except Exception as se:
                print(f"⚠️ Make syndication hook notice: {se}")

        print(f"\n🎉 Published {published_count} targeted articles with FinancialProduct Schema & Pillar Links!")
    else:
        print("\nSample Domain Briefings Preview:")
        for idx, item in enumerate(entries[:5], 1):
            h1 = format_longtail_headline(item['title'], item['category'])
            c = generate_value_dense_content(h1, item['snippet'], item['category'])
            print(f"\n--- Briefing #{idx}: {h1} ---")
            print(f"Badge: {item['badge']} | Category: {item['category']}")
            print(f"Direct Summary: {c['summary']}")
            print(f"Borrower Impact: {c['bullets'][0]}")
            print(f"Broker Tip: {c['tip']}")

if __name__ == "__main__":
    main()
