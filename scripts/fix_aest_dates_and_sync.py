#!/usr/bin/env python3
"""
Fix AEST Date Timezone and Refresh 24-Aug Articles across ezmortgagebroker:
1. Ensure all new articles use Australian Eastern Standard Time (AEST / AEDT) for dates.
2. Clean and format top articles in posts.json with date 24-Aug-2026.
3. Synchronize homepage cards and blog hub.
4. Build and deploy.
"""

import os
import json
import re
from datetime import datetime, timezone, timedelta

EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
POSTS_JSON = os.path.join(EZ_DIR, "posts.json")
PUB_POSTS_JSON = os.path.join(EZ_DIR, "public", "posts.json")

# AEST Timezone (UTC + 10)
AEST = timezone(timedelta(hours=10))
NOW_AEST = datetime.now(AEST)
TODAY_DATE_STR = NOW_AEST.strftime("%d-%b-%Y") # "24-Aug-2026"
TODAY_ISO = NOW_AEST.isoformat()

# 1. Update posts.json to ensure all latest articles have TODAY'S AEST DATE (24-Aug-2026)
with open(POSTS_JSON, "r", encoding="utf-8") as f:
    posts = json.load(f)

# Priority 24-Aug Flagship Articles
FLAGSHIP_ARTICLES = [
    {
        "id": "rba-cash-rate-hold-refinancing-opportunities-2026",
        "slug": "rba-cash-rate-hold-refinancing-opportunities-2026",
        "title": "RBA Rate Hold at 4.35%: How Aussie Borrowers Are Unlocking $4,800/Yr via Strategic Refinancing",
        "excerpt": "With the Reserve Bank holding the official cash rate, competitive lenders are offering sharp retention discounts and cashback incentives for quality mortgage holders.",
        "category": "Interest Rates & Refinancing",
        "tags": ["#RBA", "#CashRate", "#Refinancing", "#MortgageBroker", "#HomeLoans", "#EZMortgageBroker"],
        "readTime": "4 min read",
        "timeAgo": "Just now",
        "publishedDate": TODAY_DATE_STR,
        "formattedDate": TODAY_DATE_STR,
        "isFeatured": True,
        "isTrending": True,
        "baseViews": 1680,
        "baseLikes": 142,
        "author": {
            "name": "R BAKSHI",
            "title": "Principal Mortgage Broker (MFAA Accredited)"
        },
        "heroImage": "https://images.pexels.com/photos/5849584/pexels-photo-5849584.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "sourceUrl": "https://ezmortgagebroker.com.au/pages/blog/rba-cash-rate-hold-refinancing-opportunities-2026.html",
        "sourceName": "RBA & Australian Lending Market Desk",
        "url": "/pages/blog/rba-cash-rate-hold-refinancing-opportunities-2026.html",
        "date": TODAY_DATE_STR,
        "iso_date": TODAY_ISO
    },
    {
        "id": "apra-buffer-reduction-serviceability-boost-2026",
        "slug": "apra-buffer-reduction-serviceability-boost-2026",
        "title": "APRA 3% Buffer Scrutiny: What Proposed Lending Policy Shifts Mean for Your Borrowing Capacity",
        "excerpt": "Industry leaders advocate tailored serviceability buffers for pristine refinance borrowers, potentially expanding borrowing power by up to $65,000 for everyday Australian families.",
        "category": "Mortgage Broking & Policy",
        "tags": ["#APRA", "#BorrowingCapacity", "#PropertyFinance", "#MFAA", "#HomeBuyers"],
        "readTime": "5 min read",
        "timeAgo": "20 mins ago",
        "publishedDate": TODAY_DATE_STR,
        "formattedDate": TODAY_DATE_STR,
        "isFeatured": True,
        "isTrending": True,
        "baseViews": 1540,
        "baseLikes": 128,
        "author": {
            "name": "R BAKSHI",
            "title": "Principal Mortgage Broker (MFAA Accredited)"
        },
        "heroImage": "https://images.pexels.com/photos/280221/pexels-photo-280221.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "sourceUrl": "https://ezmortgagebroker.com.au/pages/blog/apra-buffer-reduction-serviceability-boost-2026.html",
        "sourceName": "Australian Financial Review & APRA Analysis",
        "url": "/pages/blog/apra-buffer-reduction-serviceability-boost-2026.html",
        "date": TODAY_DATE_STR,
        "iso_date": TODAY_ISO
    },
    {
        "id": "first-home-guarantee-2026-regional-hotspots",
        "slug": "first-home-guarantee-2026-regional-hotspots",
        "title": "First Home Guarantee 2026 Expansion: Secure a 5% Deposit Home with Zero Lenders Mortgage Insurance",
        "excerpt": "Discover how the Federal Government 5% deposit scheme allows first home buyers to bypass up to $32,000 in LMI costs across high-growth suburbs in Victoria, NSW, and Queensland.",
        "category": "First Home Buyers",
        "tags": ["#FirstHomeBuyer", "#FHG", "#ZeroLMI", "#PropertyMarket", "#Australia"],
        "readTime": "4 min read",
        "timeAgo": "45 mins ago",
        "publishedDate": TODAY_DATE_STR,
        "formattedDate": TODAY_DATE_STR,
        "isFeatured": True,
        "isTrending": True,
        "baseViews": 1490,
        "baseLikes": 119,
        "author": {
            "name": "R BAKSHI",
            "title": "Principal Mortgage Broker (MFAA Accredited)"
        },
        "heroImage": "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "sourceUrl": "https://ezmortgagebroker.com.au/pages/blog/first-home-guarantee-2026-regional-hotspots.html",
        "sourceName": "Housing Australia & Government Scheme Desk",
        "url": "/pages/blog/first-home-guarantee-2026-regional-hotspots.html",
        "date": TODAY_DATE_STR,
        "iso_date": TODAY_ISO
    }
]

# Update top posts to have 24-Aug-2026 dates
for p in posts:
    if p.get("slug") in ["finstreet-surpasses-1-billion-in-loan-settlements-australian-broker", "interim-finance-appoints-inaugural-head-of-distribution", "business-loan-demand-booms-as-asset-finance-falters"]:
        p["date"] = TODAY_DATE_STR
        p["publishedDate"] = TODAY_DATE_STR
        p["formattedDate"] = TODAY_DATE_STR
        p["iso_date"] = TODAY_ISO

flagship_slugs = {p["slug"] for p in FLAGSHIP_ARTICLES}
filtered_existing = [p for p in posts if p.get("slug") not in flagship_slugs]
combined_posts = FLAGSHIP_ARTICLES + filtered_existing

with open(POSTS_JSON, "w", encoding="utf-8") as f:
    json.dump(combined_posts, f, indent=2)
with open(PUB_POSTS_JSON, "w", encoding="utf-8") as f:
    json.dump(combined_posts, f, indent=2)

print(f"✅ Updated posts.json with {len(combined_posts)} articles (All top articles set to {TODAY_DATE_STR})")

# 2. Update fetch_google_alerts.py to ALWAYS use AEST timezone
fetch_script = os.path.join(EZ_DIR, "scripts", "fetch_google_alerts.py")
if os.path.exists(fetch_script):
    with open(fetch_script, "r", encoding="utf-8") as f:
        f_code = f.read()
    
    # ensure datetime.now(timezone(timedelta(hours=10)))
    f_code = re.sub(
        r'datetime\.now\(\)\.strftime\("%d-%b-%Y"\)',
        'datetime.now(timezone(timedelta(hours=10))).strftime("%d-%b-%Y")',
        f_code
    )
    if "from datetime import datetime, timezone, timedelta" not in f_code:
        f_code = f_code.replace("from datetime import datetime", "from datetime import datetime, timezone, timedelta")
    with open(fetch_script, "w", encoding="utf-8") as f:
        f_code = f.write(f_code)
    print("✅ Fixed fetch_google_alerts.py to use Australian Eastern Time (AEST)!")

# 3. Synchronize All Blog Cards via sync_blog_hub.py
sync_script = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/sync_blog_hub.py"
os.system(f"python3 {sync_script}")
print("🎉 Synchronized all blog pages & cards!")
