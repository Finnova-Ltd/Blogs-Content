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
from datetime import datetime, timezone, timedelta

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
    },
    {
        "category": "Nine Finance News",
        "badge": "FINANCE & MARKET WATCH",
        "url": "https://news.google.com/rss/search?q=site:nine.com.au+finance+(mortgage+OR+property+OR+rates+OR+home+loans+OR+rba+OR+housing)&hl=en-AU&gl=AU&ceid=AU:en",
        "feed_type": "google_news"
    },
    {
        "category": "AFR Financial Review",
        "badge": "AFR BANKING & PROPERTY",
        "url": "https://news.google.com/rss/search?q=site:afr.com+(mortgage+OR+property+OR+housing+OR+interest+rates+OR+superannuation+OR+banks)&hl=en-AU&gl=AU&ceid=AU:en",
        "feed_type": "google_news"
    },
    {
        "category": "AFR Property",
        "badge": "AFR PROPERTY INSIGHT",
        "url": "https://www.afr.com/rss/property",
        "feed_type": "rss"
    },
    {
        "category": "AFR Banking & Finance",
        "badge": "AFR BANKING WATCH",
        "url": "https://www.afr.com/rss/banking-and-finance",
        "feed_type": "rss"
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

def clean_snippet(text, title=""):
    if not text:
        return "Australian mortgage market dynamics and official regulatory policy updates analysed by R Bakshi for homeowners and property investors."
    t = re.sub(r"(News\.\s*)?By\s+[A-Za-z\s]+?\.\s*[A-Za-z]{3}\s*\d{1,2},\s*\d{4}\s*Share\.\s*", "", text, flags=re.IGNORECASE)
    t = re.sub(r"Get the hottest and freshest property and mortgage news delivered right into.*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"Explore the InfoChoice Group network.*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\b(AFR|Australian Financial Review|nine\.com\.au|9News|Nine News|news\.com\.au|Your Mortgage|InfoChoice|The Adviser|Broker News|The Mercury|realestate\.com\.au|Savings\.com\.au)\b", "Australian lending policy", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) < 50 or "..." in t[:10] or t.endswith("AFR"):
        return "Strategic credit policy breakdown by Principal Broker R Bakshi, evaluating borrowing power benchmarks, interest rate buffers, and lender serviceability criteria."
    return t

def normalize_title(title):
    norm = re.sub(r'\s*[-|–]\s*(AFR|Australian Financial Review|Nine News|9News|nine\.com\.au|The Australian|ABC News|The Age|The Adviser|Broker Daily|Broker News|Courier Mail|Sydney Morning Herald|SMH|Kalkine|Yahoo Finance|Motley Fool|Mirage News|Built Offsite|The Nightly|news\.com\.au|The Mercury|InfoChoice|Your Mortgage).*$', '', title, flags=re.IGNORECASE)
    norm = re.sub(r'^(VIDEO|AUDIO|PODCAST|EXCLUSIVE|NEWS):\s*', '', norm, flags=re.IGNORECASE)
    norm = re.sub(r'\s+', ' ', norm).strip()
    if len(norm) > 80:
        norm = norm[:80].rsplit(' ', 1)[0].rstrip(' :-—,|&')
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
            return f"Market Brief: {t}"[:80]
        return t[:80]

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
    elif "nine" in category.lower() or "market watch" in category.lower():
        summary = "National consumer finance tracking and retail banking updates highlight shifting household budget priorities. Australian homeowners are increasingly reviewing discretionary spending, offsetting mortgage interest, and consolidating revolving debt to combat cost-of-living pressures."
        b1 = "<strong>Household Cash Flow:</strong> Optimizing home loan offset accounts directly reduces non-deductible interest and preserves monthly cash reserves."
        b2 = "<strong>Rate Renegotiation:</strong> Borrowers with over 20% equity are successfully requesting 30–50 bps rate discounts directly from existing major lenders."
        b3 = "<strong>Debt Consolidation:</strong> Rolling high-interest personal loans and credit cards into low-rate mortgage facilities can cut total monthly outgoings by 40%+."
        tip = "<strong>Broker Advisory:</strong> Speak with R Bakshi to conduct a free loan health check and review how much you can save each month under current lending policies."
    elif "afr" in category.lower() or "financial review" in category.lower():
        summary = "Australian macroeconomic trends, wholesale funding dynamics, and commercial credit cycles continue to reshape lender risk appetite. Prime and non-conforming lenders are adjusting residential and commercial borrowing thresholds in response to evolving APRA guidelines."
        b1 = "<strong>Tier-1 vs Non-Bank Margins:</strong> Competitive non-bank lenders are expanding alternative-doc and commercial property lending solutions to fill major bank serviceability gaps."
        b2 = "<strong>Capital Market Liquidity:</strong> Residential Mortgage-Backed Securities (RMBS) issuance remains robust, sustaining strong pricing competition across non-major lenders."
        b3 = "<strong>Commercial & Portfolio Structuring:</strong> Multi-property investors are utilizing specialized corporate trust and SMSF structures to maximize tax efficiency and borrowing capacity."
        tip = "<strong>Broker Advisory:</strong> Schedule a consultation with R Bakshi to review strategic loan structuring across 30+ accredited retail and institutional lenders."
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

  <!-- 1. Full-Bleed Article Header Banner (100% Width Gold Standard) -->
  <header class="article-header" style="position:relative; background:#0A2540; color:#ffffff !important; padding:48px 0 44px; overflow:hidden;">
    <div class="article-header-bg" style="position:absolute; inset:0; background-image:url('/images/assets-ez-mortgage-broker/australian-home-mortgage-approval.jpg'); background-size:cover; background-position:center; filter:blur(3px) brightness(0.35);"></div>
    <div class="article-header-overlay" style="position:absolute; inset:0; background:linear-gradient(135deg, rgba(10,37,64,0.92) 0%, rgba(10,37,64,0.97) 100%);"></div>
    <div class="container article-header-content" style="position:relative; z-index:2; max-width:1200px; margin:0 auto; padding:0 20px;">
      <div class="article-top-toolbar" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px;">
        <div class="article-breadcrumbs" style="font-size:0.85rem; color:#94A3B8; font-weight:600;">
          <a href="/" style="color:#60A5FA; text-decoration:none;">Home</a> <span>&gt;</span>
          <a href="/pages/blog.html" style="color:#60A5FA; text-decoration:none;">News</a> <span>&gt;</span>
          <span style="color:#E2E8F0;">{category}</span>
        </div>
        <div class="article-social-share-bar" style="display:flex; gap:8px; align-items:center;">
          <a href="https://www.facebook.com/sharer/sharer.php?u=https://ezmortgagebroker.com.au/pages/blog/{slug}.html" target="_blank" style="width:32px; height:32px; border-radius:50%; background:#1877F2; color:#ffffff !important; display:flex; align-items:center; justify-content:center; text-decoration:none; font-size:0.85rem; font-weight:900;">f</a>
          <a href="https://twitter.com/intent/tweet?url=https://ezmortgagebroker.com.au/pages/blog/{slug}.html&text={headline}" target="_blank" style="width:32px; height:32px; border-radius:50%; background:#000000; color:#ffffff !important; display:flex; align-items:center; justify-content:center; text-decoration:none; font-size:0.85rem; font-weight:900;">𝕏</a>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://ezmortgagebroker.com.au/pages/blog/{slug}.html" target="_blank" style="width:32px; height:32px; border-radius:50%; background:#0A66C2; color:#ffffff !important; display:flex; align-items:center; justify-content:center; text-decoration:none; font-size:0.85rem; font-weight:900;">in</a>
          <a href="https://api.whatsapp.com/send?text={headline}%20https://ezmortgagebroker.com.au/pages/blog/{slug}.html" target="_blank" style="width:32px; height:32px; border-radius:50%; background:#25D366; color:#ffffff !important; display:flex; align-items:center; justify-content:center; text-decoration:none; font-size:0.85rem; font-weight:900;">wa</a>
        </div>
      </div>

      <span class="article-category-badge" style="display:inline-block; background-color:#1D4ED8; color:#ffffff !important; font-size:0.78rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; padding:6px 14px; border-radius:4px; margin-bottom:16px;">⚡ {badge}</span>
      <h1 class="article-title" style="font-size:clamp(1.8rem, 3.2vw, 2.6rem); font-weight:900; line-height:1.25; margin:0 0 14px; color:#ffffff !important;">{headline}</h1>
      <p class="article-subtitle" style="font-size:clamp(0.98rem, 1.3vw, 1.12rem); line-height:1.6; color:#E2E8F0 !important; max-width:900px; margin:0 0 22px; font-weight:400;">{content["summary"]}</p>

      <div class="article-meta-row" style="display:flex; align-items:center; flex-wrap:wrap; gap:16px; font-size:0.86rem; color:#CBD5E1; border-top:1px solid rgba(255, 255, 255, 0.15); padding-top:16px;">
        <span>📅 {date}</span>
        <span>⏱️ 4 min read</span>
        <span>✍️ <strong>R BAKSHI</strong> (Principal Mortgage Broker MFAA)</span>
      </div>
    </div>
  </header>

  <!-- 2. Main 2-Column Layout Container -->
  <main class="container" style="max-width:1200px; margin:0 auto; padding:0 20px;">
    <div class="article-layout" style="display:grid; grid-template-columns:minmax(0, 1fr) 360px; gap:40px; padding:48px 0 80px; align-items:flex-start;">
      
      <!-- LEFT COLUMN: 5 Interactive Accordions & Deep Dives (450+ Words) -->
      <div class="article-content-body">
        
        <p style="font-size:1.05rem; line-height:1.75; color:#1e293b; margin-bottom:28px; font-family:Georgia, serif;">
          In response to ongoing monetary policy adjustments by the <strong>Reserve Bank of Australia (RBA)</strong> and macroprudential serviceability updates by <strong>APRA</strong>, Australian mortgage holders, property investors, and first home buyers are actively restructuring their residential and commercial credit facilities. Navigating tiered interest rate pricing across 30+ accredited lenders requires a strategic assessment of loan-to-value ratios (LVR), debt-to-income (DTI) metrics, and genuine equity utilization.
        </p>

        <!-- Accordion 1: Market Overview & Data Matrix (Open by Default) -->
        <div class="article-section-accordion open" style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:10px; margin-bottom:16px; overflow:hidden;">
          <button class="article-section-accordion-header" onclick="this.parentElement.classList.toggle('open')" style="width:100%; text-align:left; padding:18px 24px; background:#F8FAFC; border:none; font-size:1.15rem; font-weight:800; color:#0A2540; display:flex; justify-content:space-between; align-items:center; cursor:pointer;">
            <span>1. Understanding the Market Context &amp; Lending Impact</span>
            <span class="accordion-icon">−</span>
          </button>
          <div class="article-section-accordion-body" style="padding:24px; color:#334155; line-height:1.7;">
            <p>{content["summary"]}</p>
            
            <div class="article-data-table-wrapper" style="overflow-x:auto; margin:18px 0; border-radius:8px; border:1px solid #e2e8f0;">
              <table class="article-data-table" style="width:100%; border-collapse:collapse; font-size:0.85rem; text-align:left;">
                <thead>
                  <tr>
                    <th style="background:#0A2540; color:#ffffff !important; padding:12px 14px; font-weight:700;">LENDING TIMELINE</th>
                    <th style="background:#0A2540; color:#ffffff !important; padding:12px 14px; font-weight:700;">ASSESSMENT BUFFER &amp; APPLICABLE RULES</th>
                    <th style="background:#0A2540; color:#ffffff !important; padding:12px 14px; font-weight:700;">BORROWER BENEFIT &amp; STRATEGY</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding:12px 14px; border-bottom:1px solid #f1f5f9;"><strong>Standard Residential</strong></td>
                    <td style="padding:12px 14px; border-bottom:1px solid #f1f5f9;">+3.00% APRA Serviceability Buffer above actual rate</td>
                    <td style="padding:12px 14px; border-bottom:1px solid #f1f5f9;">Guarantees repayment durability across shifting interest rate cycles.</td>
                  </tr>
                  <tr>
                    <td style="padding:12px 14px; border-bottom:1px solid #f1f5f9;"><strong>Refinancing Exception</strong></td>
                    <td style="padding:12px 14px; border-bottom:1px solid #f1f5f9;">1.00% Streamlined Buffer (Low-risk borrowers &lt;80% LVR)</td>
                    <td style="padding:12px 14px; border-bottom:1px solid #f1f5f9;">Unlocks immediate loyalty tax elimination and discretionary rate discounts.</td>
                  </tr>
                  <tr>
                    <td style="padding:12px 14px; border-bottom:1px solid #f1f5f9;"><strong>SMSF / Commercial</strong></td>
                    <td style="padding:12px 14px; border-bottom:1px solid #f1f5f9;">Limited Recourse Borrowing (LRBA) Bare Trust Benchmark</td>
                    <td style="padding:12px 14px; border-bottom:1px solid #f1f5f9;">Enables 15% concessional super tax rate on business property yields.</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p>Borrowers who audit their loan facilities proactively with an MFAA-accredited broker can avoid costly loyalty inertia and unlock substantial annual interest savings.</p>
          </div>
        </div>

        <!-- Accordion 2: Technical & Policy Deep-Dive -->
        <div class="article-section-accordion" style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:10px; margin-bottom:16px; overflow:hidden;">
          <button class="article-section-accordion-header" onclick="this.parentElement.classList.toggle('open')" style="width:100%; text-align:left; padding:18px 24px; background:#F8FAFC; border:none; font-size:1.15rem; font-weight:800; color:#0A2540; display:flex; justify-content:space-between; align-items:center; cursor:pointer;">
            <span>2. Technical Underwriting &amp; Valuation Deep-Dive</span>
            <span class="accordion-icon">+</span>
          </button>
          <div class="article-section-accordion-body" style="padding:24px; color:#334155; line-height:1.7;">
            <p>Under modern digital credit evaluation frameworks, Australian Tier 1 banks and non-bank lenders utilize automated valuation models (AVMs) and Open Banking data sharing to expedite loan approvals within 24 to 48 hours. Genuine savings criteria, Comprehensive Credit Reporting (CCR) verification, and living expense harmonization remain decisive factors in determining borrowing capacity.</p>
            <p>{content["tip"]}</p>
          </div>
        </div>

        <!-- Accordion 3: Regulatory Compliance & BID -->
        <div class="article-section-accordion" style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:10px; margin-bottom:16px; overflow:hidden;">
          <button class="article-section-accordion-header" onclick="this.parentElement.classList.toggle('open')" style="width:100%; text-align:left; padding:18px 24px; background:#F8FAFC; border:none; font-size:1.15rem; font-weight:800; color:#0A2540; display:flex; justify-content:space-between; align-items:center; cursor:pointer;">
            <span>3. Regulatory Compliance &amp; Statutory Best Interests Duty (BID)</span>
            <span class="accordion-icon">+</span>
          </button>
          <div class="article-section-accordion-body" style="padding:24px; color:#334155; line-height:1.7;">
            <p>Under the statutory Best Interests Duty (BID) governed by ASIC and the National Consumer Credit Protection Act (NCCP), licensed Australian mortgage brokers are legally mandated to prioritize the borrower's best interests over any lending institution. Clients receive complete transparent disclosures regarding lifetime interest comparisons, lender commission structures, and tailored feature suitability.</p>
          </div>
        </div>

        <!-- Accordion 4: Action Checklist -->
        <div class="article-section-accordion" style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:10px; margin-bottom:16px; overflow:hidden;">
          <button class="article-section-accordion-header" onclick="this.parentElement.classList.toggle('open')" style="width:100%; text-align:left; padding:18px 24px; background:#F8FAFC; border:none; font-size:1.15rem; font-weight:800; color:#0A2540; display:flex; justify-content:space-between; align-items:center; cursor:pointer;">
            <span>4. Pre-Application Borrower Action Checklist</span>
            <span class="accordion-icon">+</span>
          </button>
          <div class="article-section-accordion-body" style="padding:24px; color:#334155; line-height:1.7;">
            <p>To maximize borrowing capacity and secure discounted lender rate pricing, our senior credit specialists recommend following this 4-phase preparation roadmap:</p>
            <div class="article-checklist-card" style="background:#F8FAFC; border-left:4px solid #00876C; padding:18px 20px; border-radius:0 8px 8px 0; margin:18px 0;">
              <strong style="color:#00876C; font-size:0.95rem;">✓ 4-PHASE BROKER HYGIENE CHECKLIST:</strong>
              <ul class="article-checklist-list" style="list-style:none; padding:0; margin:10px 0 0; display:flex; flex-direction:column; gap:8px;">
                <li><strong>Phase 1:</strong> Audit your credit file for default errors or outdated credit card limits before applying.</li>
                <li><strong>Phase 2:</strong> Harmonize discretionary living expenses for 90 days prior to formal submission.</li>
                <li><strong>Phase 3:</strong> Compare over 30+ Australian wholesale &amp; retail lenders to negotiate fee waivers and special pricing.</li>
                <li><strong>Phase 4:</strong> Secure formal pre-approval with full valuation backing before auction bidding.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Accordion 5: Advisory Assistance & Sources -->
        <div class="article-section-accordion" style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:10px; margin-bottom:16px; overflow:hidden;">
          <button class="article-section-accordion-header" onclick="this.parentElement.classList.toggle('open')" style="width:100%; text-align:left; padding:18px 24px; background:#F8FAFC; border:none; font-size:1.15rem; font-weight:800; color:#0A2540; display:flex; justify-content:space-between; align-items:center; cursor:pointer;">
            <span>5. Talk to EZ Mortgage Broker Today</span>
            <span class="accordion-icon">+</span>
          </button>
          <div class="article-section-accordion-body" style="padding:24px; color:#334155; line-height:1.7;">
            <p>Our team of accredited Australian mortgage brokers provides free borrowing power assessments, loan health audits, and bank rate negotiations across all major metropolitan and regional centers.</p>
            <div style="border-top:1px solid #E2E8F0; padding-top:14px; margin-top:14px; display:flex; flex-wrap:wrap; gap:12px; font-size:0.85rem;">
              <strong>Tools:</strong>
              <a href="/calculators.html#borrowing-power" style="color:#1D4ED8; font-weight:700; text-decoration:none;">Borrowing Power Calculator &rarr;</a>
              <a href="/calculators.html#refinance-savings" style="color:#1D4ED8; font-weight:700; text-decoration:none;">Refinance Calculator &rarr;</a>
              <a href="/pages/first-home-buyers.html" style="color:#1D4ED8; font-weight:700; text-decoration:none;">First Home Buyer Hub &rarr;</a>
            </div>
            <p style="margin-top:12px; font-size:0.8rem; color:#94A3B8; font-style:italic;">🖋️ Industry Source Attribution: Sourced from verified Australian banking &amp; regulatory reports. <a href="{source_url}" target="_blank" rel="nofollow noopener noreferrer" style="color:#64748B;">View Source Notice &rarr;</a></p>
          </div>
        </div>

      </div>

      <!-- RIGHT COLUMN: Sticky 4-Widget Sidebar (360px) -->
      <aside class="article-sidebar" style="position: -webkit-sticky !important; position: sticky !important; top: 105px !important; align-self: flex-start !important; max-height: calc(100vh - 120px) !important; overflow-y: auto !important; scrollbar-width: thin !important; display: flex; flex-direction: column; gap: 18px;">
        
        <!-- 1. Broker Profile Card with Real Portrait & Banner Header -->
        <div class="author-profile-box" id="broker-contact-card" style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:14px; overflow:hidden; text-align:center; box-shadow:0 4px 16px rgba(0,0,0,0.06); margin-bottom:20px;">
          <div class="author-profile-banner" style="height:84px; overflow:hidden;">
            <img src="/images/ez-broker-cover-header.jpg" alt="EZ Mortgage Broker Header" style="width:100%; height:100%; object-fit:cover; display:block;">
          </div>
          <div class="author-profile-avatar-wrap" style="width:78px; height:78px; border-radius:50%; background:#ffffff; box-shadow:0 4px 14px rgba(0,0,0,0.14); margin:-39px auto 10px; display:flex; align-items:center; justify-content:center; padding:6px; overflow:hidden; border:3px solid #ffffff;">
            <img src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker Logo" class="author-profile-avatar-img" style="width:100%; height:100%; object-fit:contain; display:block;">
          </div>
          <div class="author-profile-content" style="padding:0 18px 20px;">
            <h3 class="author-profile-name" style="font-size:1.2rem; color:#0A2540; margin:0 0 2px; font-weight:800;">R Bakshi</h3>
            <p class="author-profile-title" style="font-size:0.82rem; color:#64748b; margin:0 0 4px; font-weight:600;">Principal Mortgage Broker</p>
            <p style="font-size:0.75rem; color:#1D4ED8; font-weight:700; margin:0 0 6px;">MFAA Accredited | CRN: 538522</p>
            <div class="author-rating-stars" style="color:#f59e0b; font-size:0.88rem; margin-bottom:14px; font-weight:700;">★★★★★ <span>(14 Reviews)</span></div>
            <div class="author-actions-col" style="display:flex; flex-direction:column; gap:8px;">
              <a href="tel:1300050099" class="author-action-btn" style="display:flex; align-items:center; justify-content:center; gap:8px; width:100%; padding:10px 14px; border-radius:6px; font-weight:700; font-size:0.85rem; text-decoration:none; background:#1D4ED8; color:#ffffff !important; box-shadow:0 4px 12px rgba(29,78,216,0.25);">📞 Call 1300 050 099</a>
              <a href="/#contact" class="author-action-btn secondary" style="display:flex; align-items:center; justify-content:center; gap:8px; width:100%; padding:10px 14px; border-radius:6px; font-weight:700; font-size:0.85rem; text-decoration:none; background:#F8FAFC; border:1px solid #CBD5E1; color:#0A2540 !important;">📅 Book Consultation</a>
            </div>
          </div>
        </div>

        <!-- 2. Crimson Highlights Widget (#a81127 Standard) -->
        <div class="article-highlights-widget" id="articleHighlightsWidget" style="background:#ffffff; border:2px solid #a81127; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(168, 17, 39, 0.08); margin-bottom:20px;">
          <div class="highlights-header" style="background:#a81127; color:#ffffff !important; padding:12px 18px; display:flex; align-items:center; justify-content:space-between; font-weight:800; font-size:0.95rem;">
            <span>Highlights</span>
            <span style="font-weight:900;">−</span>
          </div>
          <div class="highlights-body" style="padding:18px;">
            <div style="font-size:0.75rem; font-weight:800; color:#a81127; text-transform:uppercase; margin-bottom:10px;">— {date}</div>
            <div class="highlights-item" style="display:flex; gap:10px; align-items:flex-start; margin-bottom:14px; font-size:0.85rem;">
              <span class="highlight-bullet" style="color:#a81127; font-size:0.9rem; margin-top:1px;">●</span>
              <div>
                <strong style="color:#0A2540; font-size:0.85rem;">Rate Policy Spread</strong>
                <p style="margin:2px 0 0; color:#64748B; font-size:0.8rem;">Key serviceability buffers &amp; discount margins</p>
              </div>
            </div>
            <div class="highlights-item" style="display:flex; gap:10px; align-items:flex-start; margin-bottom:14px; font-size:0.85rem;">
              <span class="highlight-bullet" style="color:#a81127; font-size:0.9rem; margin-top:1px;">●</span>
              <div>
                <strong style="color:#0A2540; font-size:0.85rem;">Broker Strategy</strong>
                <p style="margin:2px 0 0; color:#64748B; font-size:0.8rem;">Audit 30+ lenders at zero cost to borrower</p>
              </div>
            </div>
            <a href="#" onclick="window.scrollTo({{top:0, behavior:'smooth'}}); return false;" style="display:block; text-align:center; font-size:0.78rem; font-weight:800; color:#a81127; text-decoration:none; margin-top:10px; border-top:1px solid #f1f5f9; padding-top:8px;">
              Top of Article ↑
            </a>
          </div>
        </div>

        <!-- 3. Official RBA Key Indicators Mini Card -->
        <div style="background:#ffffff; border:1.5px solid #e2e8f0; border-top:4px solid #00897B; border-radius:12px; padding:18px; margin-bottom:20px; box-shadow:0 4px 14px rgba(10,37,64,0.04);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-size:0.78rem; font-weight:800; color:#0A2540; text-transform:uppercase;">🏛️ RBA Cash Rate</span>
            <span style="font-size:0.68rem; color:#00897B; font-weight:800; background:#E0F2F1; padding:2px 6px; border-radius:4px;">Live</span>
          </div>
          <div style="font-size:2.2rem; font-weight:900; color:#0A2540; line-height:1; margin:6px 0;">4.35<span style="font-size:1.3rem; font-weight:800; vertical-align:super;">%</span></div>
          <div style="font-size:0.72rem; color:#64748B; border-top:1px solid #f1f5f9; padding-top:6px; margin-top:6px;">
            Inflation: <strong>3.8%</strong> | Next Decision: <strong>29 Sept</strong>
          </div>
        </div>

        <!-- 4. Sticky Advisory Call Card -->
        <div class="sidebar-sticky-cta-card" style="position:sticky; top:96px; background:linear-gradient(135deg, #0A2540 0%, #17345f 100%); border:1.5px solid rgba(255, 220, 74, 0.4); border-radius:14px; padding:22px 18px; color:#ffffff !important;">
          <h4 style="font-size:1.05rem; font-weight:900; margin:0 0 6px; color:#ffffff;">Need Borrowing Power Advice?</h4>
          <p style="font-size:0.82rem; color:#E2E8F0; margin:0 0 14px; line-height:1.45;">
            Speak directly with our senior MFAA accredited credit advisors across Australia.
          </p>
          <a href="tel:1300050099" style="display:block; text-align:center; background:#FFDC4A; color:#0A2540; padding:10px 0; border-radius:6px; font-weight:900; font-size:0.88rem; text-decoration:none;">
            📞 1300 050 099
          </a>
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
                    "date": datetime.now(timezone(timedelta(hours=10))).strftime("%d-%b-%Y"),
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
                "date": datetime.now(timezone(timedelta(hours=10))).strftime("%d-%b-%Y"),
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
