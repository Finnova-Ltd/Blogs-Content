#!/usr/bin/env python3
import os
import re
import json
import subprocess
from datetime import datetime

EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
POSTS_JSON_PATH = os.path.join(EZ_DIR, "posts.json")
PUB_POSTS_JSON = os.path.join(EZ_DIR, "public", "posts.json")
PAGES_BLOG_DIR = os.path.join(EZ_DIR, "pages", "blog")
PUB_PAGES_BLOG_DIR = os.path.join(EZ_DIR, "public", "pages", "blog")

os.makedirs(PAGES_BLOG_DIR, exist_ok=True)
os.makedirs(PUB_PAGES_BLOG_DIR, exist_ok=True)

# Load existing posts
existing_posts = []
if os.path.exists(POSTS_JSON_PATH):
    with open(POSTS_JSON_PATH, "r", encoding="utf-8") as f:
        existing_posts = json.load(f)

existing_slugs = {p.get("slug") for p in existing_posts}

new_articles = [
    {
        "slug": "afg-mortgage-demand-cooling-budget-upgraders-property-guide-2026",
        "title": "AFG Reports Mortgage Demand Cooled Post-Budget: How Australian Upgraders & First-Home Buyers Navigate 2026 Rates",
        "category": "Home Loans",
        "badge": "MORTGAGE MARKET ALERT",
        "date": "20-Aug-2026",
        "iso_date": "2026-08-20T02:38:33Z",
        "readTime": "4 min read",
        "author": "R BAKSHI",
        "authorRole": "Principal Mortgage Broker",
        "authorImg": "/images/ez-mortgage-broker.webp",
        "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80",
        "excerpt": "Australian Finance Group (AFG) index data reveals mortgage demand has moderated following the Federal Budget, creating prime negotiation opportunities for property upgraders while first-home buyers leverage state concessions.",
        "summary": "Major aggregator Australian Finance Group (AFG) reports shifting market dynamics, with national home loan volumes easing post-Budget. While first-time purchasers face tight serviceability hurdles, property upgraders and equity-rich refinancers are unlocking competitive lender discounts as major banks battle for loan book share.",
        "bullets": [
            "Upgrader Opportunity: Banks are offering discretionary rate cuts and cash incentives to secure low-LVR property upgraders.",
            "Serviceability Buffers: The APRA 3.0% stress-test buffer remains the primary borrowing cap, making broker rate negotiation critical.",
            "First Home Buyer Strategy: Eligible buyers can bridge deposit gaps using the expanded First Home Guarantee (FHG) 5% deposit scheme without paying Lenders Mortgage Insurance (LMI)."
        ],
        "tip": "If you are planning to upgrade or enter the market, consult an MFAA-accredited broker at EZ Mortgage Broker to compare 30+ accredited Australian lenders and maximize your borrowing capacity.",
        "sourceUrl": "https://thewest.com.au/business/banking/afg-says-mortgage-demand-has-cooled-since-budget-as-upgraders-stir-but-first-home-buyers-stay-out-c-22748762"
    },
    {
        "slug": "mortgage-brokers-settle-80-percent-australian-home-loans-mfaa",
        "title": "Mortgage Brokers Now Arrange 80% of All Australian Home Loans: Why Borrowers Are Bypassing Direct Bank Branches",
        "category": "Home Loans",
        "badge": "INDUSTRY MILESTONE",
        "date": "20-Aug-2026",
        "iso_date": "2026-08-20T01:43:19Z",
        "readTime": "4 min read",
        "author": "R BAKSHI",
        "authorRole": "Principal Mortgage Broker",
        "authorImg": "/images/ez-mortgage-broker.webp",
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80",
        "excerpt": "Official MFAA industry data shows mortgage brokers now facilitate over 80% of all new residential home loans across Australia, driven by statutory Best Interests Duty (BID) and superior lender comparison.",
        "summary": "The Australian mortgage landscape has reached a historic tipping point, with mortgage brokers now arranging 8 out of every 10 residential home loans. Borrowers increasingly choose brokers over branch staff due to legally mandated Best Interests Duty (BID) protections and access to wholesale tier pricing.",
        "bullets": [
            "Best Interests Duty (BID): Brokers are legally obligated under the National Consumer Credit Protection Act to prioritize borrower welfare, whereas bank employees can only sell proprietary products.",
            "Panel Depth: Access to over 50 residential, commercial, and non-bank lenders provides tailored approval pathways for complex incomes and self-employed applicants.",
            "Turnaround Efficiency: Digital submission platforms and direct BDM escalation reduce conditional approval times from weeks to under 48 hours."
        ],
        "tip": "Take advantage of accredited broker guidance with zero out-of-pocket advisory fees. Speak with EZ Mortgage Broker to calculate your exact borrowing limits across all major Australian lenders.",
        "sourceUrl": "https://www.smh.com.au/national/australia-news-live-lambie-demands-government-abandon-cap-on-allied-health-spending-for-veterans-senior-swan-isaac-heeney-revealed-as-focus-of-police-investigation-20260820-p60pwn.html"
    },
    {
        "slug": "cba-cfo-perspective-australian-housing-market-borrowing-power-2026",
        "title": "CommBank CFO Alan Docherty on Housing Market Perspective: Interest Rate Outlook & Loan Repayment Strategies",
        "category": "RBA & Rates",
        "badge": "BANKING INSIGHT",
        "date": "20-Aug-2026",
        "iso_date": "2026-08-19T23:25:20Z",
        "readTime": "4 min read",
        "author": "R BAKSHI",
        "authorRole": "Principal Mortgage Broker",
        "authorImg": "/images/ez-mortgage-broker.webp",
        "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
        "excerpt": "Commonwealth Bank Chief Financial Officer Alan Docherty provides market perspective on moderating mortgage volumes, property price forecasts, and strategic rate buffer management for Australian households.",
        "summary": "Commonwealth Bank (CBA) leadership highlights that despite shifting property market headlines, underlying borrower balance sheets remain resilient. With inflation moderating and competitive lending margins tightening, savvy homeowners are actively restructuring their mortgage splits to hedge interest rate exposure.",
        "bullets": [
            "Rate Normalization Timeline: Major bank economics teams forecast potential RBA cash rate cuts as core inflation settles into the 2-3% target band.",
            "Split Loan Resilience: Combining fixed-rate stability with variable-rate offset accounts allows borrowers to protect against volatility while maximizing liquid savings.",
            "Equity Retention: Capital gains across Melbourne, Sydney, and regional centers provide existing owners with substantial equity to refinance and eliminate risk fees."
        ],
        "tip": "Review your home loan interest rate annually. A 0.40% rate reduction on a $750,000 mortgage saves over $3,000 in annual repayments. Use our free Refinance Calculator to see your potential savings.",
        "sourceUrl": "https://www.commbank.com.au/articles/newsroom/2026/08/keeping-perspective-australian-housing-market.html"
    },
    {
        "slug": "aussie-homeowners-bargaining-power-mortgage-rates-competition-2026",
        "title": "Aussie Homeowners Gain Mortgage Rate Bargaining Power: How to Negotiate Lower Rates Amid Lender Competition",
        "category": "Refinancing",
        "badge": "RATE STRATEGY",
        "date": "20-Aug-2026",
        "iso_date": "2026-08-19T22:19:51Z",
        "readTime": "4 min read",
        "author": "R BAKSHI",
        "authorRole": "Principal Mortgage Broker",
        "authorImg": "/images/ez-mortgage-broker.webp",
        "image": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
        "excerpt": "As residential loan application volumes moderate, major Australian banks and non-bank lenders are aggressively discounting variable rates to win high-quality borrowers. Here is how to claim your discount.",
        "summary": "With credit growth stabilizing, lenders are offering unpublished pricing discounts to retain reliable borrowers. Australian homeowners who have not reviewed their mortgage in the last 18 months are often paying a 'loyalty tax' of 0.50% to 0.85% above current market rates.",
        "bullets": [
            "The Loyalty Tax Penalty: Existing bank customers typically pay significantly higher interest rates than new-to-bank borrowers on identical mortgage products.",
            "Tiered LVR Pricing: Homeowners with Loan-to-Value Ratios below 70% qualify for the most aggressive tier discounts across tier-1 and tier-2 banks.",
            "Discharge Request Leverage: Requesting an official lender discharge form frequently triggers instant retention rate cuts from bank retention desks."
        ],
        "tip": "Do not accept your bank's default rate. Let EZ Mortgage Broker run a comprehensive repricing review on your behalf to negotiate or refinance to Australia's lowest available rates.",
        "sourceUrl": "https://7news.com.au/video/news/aussie-homeowners-gain-bargaining-power-on-mortgage-rates-bc-6403730800112"
    }
]

def generate_html(post):
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{post['title']} | EZ Mortgage Broker</title>
  <meta name="description" content="{post['excerpt']}">
  <link rel="canonical" href="https://ezmortgagebroker.com.au/pages/blog/{post['slug']}.html">
  <meta property="og:title" content="{post['title']}">
  <meta property="og:description" content="{post['excerpt']}">
  <meta property="og:image" content="{post['image']}">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/calculators.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": "{post['title']}",
    "description": "{post['excerpt']}",
    "datePublished": "{post['iso_date']}",
    "dateModified": "{post['iso_date']}",
    "image": "{post['image']}",
    "author": {{
      "@type": "Person",
      "name": "{post['author']}",
      "jobTitle": "{post['authorRole']}"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "EZ Mortgage Broker",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://ezmortgagebroker.com.au/images/logo.png"
      }}
    }}
  }}
  </script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased font-sans">
  <!-- Top Bar -->
  <header class="bg-[#084582] text-white py-4 px-4 sm:px-8 border-b border-blue-900">
    <div class="max-w-6xl mx-auto flex items-center justify-between">
      <a href="/" class="text-xl font-black tracking-tight text-white flex items-center gap-2">
        <span>EZ MORTGAGE BROKER</span>
      </a>
      <div class="flex items-center gap-4 text-xs font-bold">
        <a href="/pages/blog" class="text-blue-200 hover:text-white transition">Blog & Insights</a>
        <a href="/calculators.html" class="text-blue-200 hover:text-white transition">Calculators</a>
        <a href="/#contact" class="bg-amber-500 text-slate-900 px-4 py-2 rounded-xl font-extrabold hover:bg-amber-400 transition">Book Consult</a>
      </div>
    </div>
  </header>

  <!-- Hero Header -->
  <section class="bg-gradient-to-r from-[#063565] via-[#084582] to-[#0a559e] text-white py-12 px-4 sm:px-8 shadow-sm">
    <div class="max-w-4xl mx-auto space-y-4">
      <div class="flex items-center gap-2 text-xs font-semibold text-blue-200">
        <a href="/" class="hover:text-white">Home</a>
        <span>/</span>
        <a href="/pages/blog" class="hover:text-white">Blog</a>
        <span>/</span>
        <span class="text-white">{post['category']}</span>
      </div>
      <span class="inline-block bg-amber-500 text-slate-900 text-xs font-black uppercase px-3 py-1 rounded-md">
        {post['badge']}
      </span>
      <h1 class="text-2xl sm:text-3xl md:text-4xl font-black leading-tight tracking-tight text-white">
        {post['title']}
      </h1>
      <div class="flex items-center gap-3 text-xs text-blue-100 font-medium">
        <span>By {post['author']}</span>
        <span>•</span>
        <span>{post['date']}</span>
        <span>•</span>
        <span>{post['readTime']}</span>
      </div>
    </div>
  </section>

  <!-- Main Content -->
  <main class="max-w-4xl mx-auto px-4 sm:px-8 py-10 space-y-8">
    <article class="bg-white p-6 sm:p-10 rounded-3xl border border-slate-200/80 shadow-xs space-y-6">
      
      <!-- Executive Summary Box -->
      <div class="rounded-2xl p-6 bg-slate-50 border border-slate-200 space-y-2">
        <span class="text-xs font-black uppercase text-[#084582] tracking-wider block">Market Briefing & Direct Summary</span>
        <p class="text-base text-slate-800 leading-relaxed font-medium">
          {post['summary']}
        </p>
      </div>

      <!-- Core Takeaways -->
      <div class="space-y-4 pt-2">
        <h2 class="text-lg font-black text-slate-900 uppercase tracking-wide">Key Borrower Takeaways & Market Impact</h2>
        <ul class="space-y-3">
          {"".join([f'<li class="flex items-start gap-3 text-sm text-slate-700 leading-relaxed"><span class="mt-1.5 h-2 w-2 rounded-full bg-[#084582] shrink-0"></span><span>{b}</span></li>' for b in post['bullets']])}
        </ul>
      </div>

      <!-- Broker Tip Box -->
      <div class="rounded-2xl p-6 bg-blue-50/70 border border-blue-200/80 space-y-2">
        <span class="text-xs font-black uppercase text-[#084582] tracking-wider block">Expert Broker Tip</span>
        <p class="text-sm text-slate-800 leading-relaxed font-medium">
          {post['tip']}
        </p>
      </div>

      <!-- Source Link -->
      <div class="pt-4 border-t border-slate-100 text-xs text-slate-400 italic">
        Source: <a href="{post['sourceUrl']}" target="_blank" rel="nofollow noopener" class="underline hover:text-slate-600">Australian Financial Media & Official Industry Data</a>
      </div>
    </article>

    <!-- Consultation CTA -->
    <div class="rounded-3xl bg-[#084582] text-white p-8 text-center space-y-4 shadow-md">
      <h3 class="text-xl sm:text-2xl font-black">Want to calculate your exact borrowing power or interest rate savings?</h3>
      <p class="text-sm text-blue-100 max-w-xl mx-auto">
        Speak with an MFAA-accredited mortgage broker in Melbourne. We compare 30+ accredited lenders to find you the lowest available rate with zero broker fees.
      </p>
      <div class="flex items-center justify-center gap-4 pt-2">
        <a href="/calculators.html#borrowing-power" class="bg-amber-500 hover:bg-amber-400 text-slate-900 text-xs font-black px-6 py-3 rounded-xl transition">
          Calculate Borrowing Power ↗
        </a>
        <a href="/#contact" class="border border-white/40 hover:bg-white/10 text-white text-xs font-black px-6 py-3 rounded-xl transition">
          Book Free Consultation
        </a>
      </div>
    </div>
  </main>
</body>
</html>"""

new_posts_added = []
for p in new_articles:
    if p["slug"] in existing_slugs:
        continue
    
    # Write page html
    html_content = generate_html(p)
    with open(os.path.join(PAGES_BLOG_DIR, f"{p['slug']}.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(os.path.join(PUB_PAGES_BLOG_DIR, f"{p['slug']}.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    
    post_obj = {
        "id": p["slug"],
        "slug": p["slug"],
        "title": p["title"],
        "category": p["category"],
        "badge": p["badge"],
        "date": p["date"],
        "iso_date": p["iso_date"],
        "readTime": p["readTime"],
        "author": p["author"],
        "authorRole": p["authorRole"],
        "authorImg": p["authorImg"],
        "excerpt": p["excerpt"],
        "summary": p["summary"],
        "image": p["image"],
        "url": f"/pages/blog/{p['slug']}.html"
    }
    new_posts_added.append(post_obj)
    existing_slugs.add(p["slug"])
    print(f"✅ Generated article & HTML page: {p['title']}")

if new_posts_added:
    merged = new_posts_added + existing_posts
    with open(POSTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)
    with open(PUB_POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)
    print(f"✅ Synced {len(new_posts_added)} new posts into posts.json (Total: {len(merged)})")

# Run RSS Generator
print("Running generate_rss_feed.py...")
subprocess.run(["python3", "generate_rss_feed.py"], cwd=os.path.join(EZ_DIR, "scripts"), capture_output=True)

# Run Make.com Flow Syndicator
print("🚀 Triggering Make.com flow syndicator (Scenario 6988857)...")
res_make = subprocess.run(["python3", "syndicate_to_make.py"], cwd=os.path.join(EZ_DIR, "scripts"), capture_output=True, text=True)
print("Make syndicator output:\n", res_make.stdout)
if res_make.stderr:
    print("Make stderr:\n", res_make.stderr)

# Build ezmortgagebroker
print("Building ezmortgagebroker with Vite...")
res_build = subprocess.run(["npm", "run", "build"], cwd=EZ_DIR, capture_output=True, text=True)
print("Vite build output:\n", res_build.stdout)
if res_build.returncode != 0:
    print("Build error:\n", res_build.stderr)
else:
    print("✅ ezmortgagebroker build succeeded!")
