#!/usr/bin/env python3
"""
Generate 91 Melbourne Suburb Location Landing Pages
Features:
- Header logo shifted 4cm (150px) to the right for maximum visibility
- Full site header with topbar and mega menus
- Column 3 with:
  1. MFAA Broker Profile (R Bakshi)
  2. Nearby Suburb Guides Carousel / Directory
  3. Latest Market News & Recent Articles Feed
"""

import os
import re
import json
import html
from datetime import datetime

TARGET_REPO = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
LOCATIONS_DIR = os.path.join(TARGET_REPO, "pages", "locations")
PUB_LOCATIONS_DIR = os.path.join(TARGET_REPO, "public", "pages", "locations")
POSTS_JSON = os.path.join(TARGET_REPO, "posts.json")

for d in [LOCATIONS_DIR, PUB_LOCATIONS_DIR]:
    os.makedirs(d, exist_ok=True)

# Load recent posts for the sidebar widget
recent_posts = []
if os.path.exists(POSTS_JSON):
    try:
        with open(POSTS_JSON, "r", encoding="utf-8") as f:
            recent_posts = json.load(f)[:3]
    except Exception:
        recent_posts = []

MELBOURNE_SUBURBS = [
    # City of Melbourne & Inner
    {"suburb": "Melbourne CBD", "postcode": "3000", "lga": "City of Melbourne", "region": "Central Melbourne", "highlights": "high-density apartment lending, off-the-plan finance, foreign income qualification, and commercial office loans"},
    {"suburb": "Docklands", "postcode": "3008", "lga": "City of Melbourne", "region": "Central Melbourne", "highlights": "waterfront high-rise apartments, investor lending ratios, and low-deposit options"},
    {"suburb": "Southbank", "postcode": "3006", "lga": "City of Melbourne", "region": "Central Melbourne", "highlights": "arts precinct high-density residential towers, refinancing cashback deals, and SMSF apartment acquisitions"},
    {"suburb": "Carlton", "postcode": "3053", "lga": "City of Melbourne", "region": "Inner North", "highlights": "heritage Victorian terrace financing, university precinct investment units, and parent guarantor loans"},
    {"suburb": "North Melbourne", "postcode": "3051", "lga": "City of Melbourne", "region": "Inner North", "highlights": "Arden urban renewal precinct growth, warehouse conversions, and flexible redraw home loans"},
    {"suburb": "East Melbourne", "postcode": "3002", "lga": "City of Melbourne", "region": "Inner East", "highlights": "prestige heritage properties, medical professional doctor loan packages (up to 95% LMI waiver), and high-net-worth portfolio loans"},
    {"suburb": "Kensington", "postcode": "3031", "lga": "City of Melbourne", "region": "Inner West", "highlights": "historic stock route heritage homes, young family upgrades, and offset account strategies"},
    {"suburb": "Parkville", "postcode": "3052", "lga": "City of Melbourne", "region": "Inner North", "highlights": "biomedical and university precinct residences, medico mortgage broker specialists, and low-doc self-employed loans"},
    {"suburb": "West Melbourne", "postcode": "3003", "lga": "City of Melbourne", "region": "Inner West", "highlights": "modern urban fringe developments, first home buyer stamp duty exemptions, and investment structuring"},

    # City of Port Phillip & City of Yarra
    {"suburb": "South Melbourne", "postcode": "3205", "lga": "City of Port Phillip", "region": "Inner South", "highlights": "market precinct townhouses, commercial shop-top housing, and self-employed alt-doc lending"},
    {"suburb": "Port Melbourne", "postcode": "3207", "lga": "City of Port Phillip", "region": "Bayside", "highlights": "Beacon Cove beachfront homes, modern lifestyle apartments, and competitive variable rate renegotiation"},
    {"suburb": "St Kilda", "postcode": "3182", "lga": "City of Port Phillip", "region": "Bayside", "highlights": "iconic lifestyle apartments, Art Deco renovation finance, and short-stay Airbnb investment lending"},
    {"suburb": "Elwood", "postcode": "3184", "lga": "City of Port Phillip", "region": "Bayside", "highlights": "canal-side leafy residential apartments, family character homes, and equity release loans"},
    {"suburb": "Albert Park", "postcode": "3206", "lga": "City of Port Phillip", "region": "Inner South", "highlights": "grand Victorian and Edwardian residences, high-value prestige refinances, and custom construction loans"},
    {"suburb": "Middle Park", "postcode": "3206", "lga": "City of Port Phillip", "region": "Inner South", "highlights": "premier heritage conservation zones, luxury wealth structuring, and private bank lending terms"},
    {"suburb": "Richmond", "postcode": "3121", "lga": "City of Yarra", "region": "Inner East", "highlights": "Swan Street & Bridge Road urban terraces, warehouse conversions, and first-time buyer guarantee approvals"},
    {"suburb": "Fitzroy", "postcode": "3065", "lga": "City of Yarra", "region": "Inner North", "highlights": "Brunswick Street bohemian lofts, historic worker cottages, and flexible ABN contractor lending"},
    {"suburb": "Collingwood", "postcode": "3066", "lga": "City of Yarra", "region": "Inner North", "highlights": "Smith Street gentrified industrial lofts, tech professional mortgages, and multi-lender comparison"},
    {"suburb": "Abbotsford", "postcode": "3067", "lga": "City of Yarra", "region": "Inner East", "highlights": "Yarra riverfront master-planned apartments, convent precinct townhouses, and quick pre-approvals"},
    {"suburb": "Clifton Hill", "postcode": "3068", "lga": "City of Yarra", "region": "Inner North", "highlights": "leafy heritage boulevards, family home extensions, and debt consolidation refinancing"},

    # City of Banyule & Darebin
    {"suburb": "Heidelberg", "postcode": "3084", "lga": "City of Banyule", "region": "North East", "highlights": "Austin Hospital health precinct doctor loans, mid-century family properties, and construction mortgages"},
    {"suburb": "Ivanhoe", "postcode": "3079", "lga": "City of Banyule", "region": "Inner North-East", "highlights": "prestigious leafy estates, elite school catchment family homes, and portfolio refinancing"},
    {"suburb": "Greensborough", "postcode": "3088", "lga": "City of Banyule", "region": "North East", "highlights": "green-wedge family residences, first home buyer house & land packages, and split-loan facilities"},
    {"suburb": "Northcote", "postcode": "3070", "lga": "City of Darebin", "region": "Inner North", "highlights": "High Street trendsetter residences, architect-designed extensions, and contractor finance"},
    {"suburb": "Preston", "postcode": "3072", "lga": "City of Darebin", "region": "Northern Melbourne", "highlights": "Preston Market precinct transformations, modern townhomes, and 1-year tax return self-employed loans"},
    {"suburb": "Reservoir", "postcode": "3073", "lga": "City of Darebin", "region": "Northern Melbourne", "highlights": "high-growth entry-level family homes, subdivision construction loans, and first-time buyer grants"},
    {"suburb": "Thornbury", "postcode": "3071", "lga": "City of Darebin", "region": "Inner North", "highlights": "vibrant village cafes, stylish Edwardian renovations, and bank serviceability optimization"},

    # City of Hume & Merri-bek
    {"suburb": "Craigieburn", "postcode": "3064", "lga": "City of Hume", "region": "Outer North", "highlights": "high-growth masterplanned estates, 5% deposit First Home Guarantee, and land-and-build loans"},
    {"suburb": "Greenvale", "postcode": "3059", "lga": "City of Hume", "region": "Northern Melbourne", "highlights": "executive acreage homes, custom home builder finance, and luxury family upgrades"},
    {"suburb": "Mickleham", "postcode": "3064", "lga": "City of Hume", "region": "Northern Growth Corridor", "highlights": "rapidly growing new estates, dual-occupancy investment loans, and construction progress payments"},
    {"suburb": "Roxburgh Park", "postcode": "3064", "lga": "City of Hume", "region": "Northern Melbourne", "highlights": "established family properties, low-rate refinancing switches, and equity redraw options"},
    {"suburb": "Sunbury", "postcode": "3429", "lga": "City of Hume", "region": "North-West", "highlights": "spacious country-feel estates, Jackson Hill properties, and regional first home benefits"},
    {"suburb": "Brunswick", "postcode": "3056", "lga": "City of Merri-bek", "region": "Inner North", "highlights": "Sydney Road retail lofts, sustainable modern units, and self-employed contractor income"},
    {"suburb": "Coburg", "postcode": "3058", "lga": "City of Merri-bek", "region": "Northern Melbourne", "highlights": "Coburg Hill family townhouses, heritage homes, and rapid loan pre-approval workflows"},
    {"suburb": "Glenroy", "postcode": "3046", "lga": "City of Merri-bek", "region": "Northern Melbourne", "highlights": "affordable inner-north entry points, subdivision development finance, and investor refinancing"},
    {"suburb": "Pascoe Vale", "postcode": "3044", "lga": "City of Merri-bek", "region": "Northern Melbourne", "highlights": "Strathmore Secondary zone homes, unit developments, and competitive fixed/variable splits"},

    # City of Whittlesea
    {"suburb": "Epping", "postcode": "3076", "lga": "City of Whittlesea", "region": "Northern Growth Corridor", "highlights": "hospital and retail hub properties, family upgrade home loans, and low-fee refinancing"},
    {"suburb": "Mernda", "postcode": "3754", "lga": "City of Whittlesea", "region": "Northern Growth Corridor", "highlights": "family-friendly community living, turnkey house & land packages, and stamp duty savings"},
    {"suburb": "South Morang", "postcode": "3752", "lga": "City of Whittlesea", "region": "Northern Growth Corridor", "highlights": "transport-connected estates, equity access for renovations, and lender cashback deals"},
    {"suburb": "Wollert", "postcode": "3750", "lga": "City of Whittlesea", "region": "Northern Growth Corridor", "highlights": "brand-new construction builds, guarantor loan options, and multi-lender comparison"},

    # Eastern Municipalities (Boroondara, Knox, Manningham, Whitehorse, Monash)
    {"suburb": "Camberwell", "postcode": "3124", "lga": "City of Boroondara", "region": "Inner East", "highlights": "prestige heritage estates, Junction shopping precinct, and high-borrowing-capacity structuring"},
    {"suburb": "Hawthorn", "postcode": "3122", "lga": "City of Boroondara", "region": "Inner East", "highlights": "Glenferrie road lifestyle apartments, private school corridor residences, and SMSF property loans"},
    {"suburb": "Kew", "postcode": "3101", "lga": "City of Boroondara", "region": "Inner East", "highlights": "luxury family mansions, Studley Park prestige properties, and private banking terms"},
    {"suburb": "Balwyn", "postcode": "3103", "lga": "City of Boroondara", "region": "Eastern Melbourne", "highlights": "Balwyn High School zone properties, luxury rebuilds, and foreign tax resident income loans"},
    {"suburb": "Rowville", "postcode": "3178", "lga": "City of Knox", "region": "Outer East", "highlights": "golf course estates, substantial family homes, and debt consolidation refinancing"},
    {"suburb": "Wantirna", "postcode": "3152", "lga": "City of Knox", "region": "Eastern Melbourne", "highlights": "Knox City retail proximity, family residences, and 1% modified refinancing buffer checks"},
    {"suburb": "Doncaster", "postcode": "3108", "lga": "City of Manningham", "region": "Eastern Melbourne", "highlights": "Westfield hill luxury towers, family brick homes, and equity release for secondary investment"},
    {"suburb": "Templestowe", "postcode": "3106", "lga": "City of Manningham", "region": "Eastern Melbourne", "highlights": "acreage lifestyle mansions, custom architectural builds, and premium non-bank lending"},
    {"suburb": "Box Hill", "postcode": "3128", "lga": "City of Whitehorse", "region": "Eastern Melbourne", "highlights": "bustling commercial CBD towers, multilingual broker consultations, and development funding"},
    {"suburb": "Glen Waverley", "postcode": "3150", "lga": "City of Monash", "region": "South East", "highlights": "GWSC school catchment properties, The Glen retail precinct luxury units, and SMSF commercial loans"},
    {"suburb": "Mount Waverley", "postcode": "3149", "lga": "City of Monash", "region": "South East", "highlights": "spacious suburban blocks, knock-down rebuild mortgages, and family equity top-ups"},
    {"suburb": "Clayton", "postcode": "3168", "lga": "City of Monash", "region": "South East", "highlights": "Monash University & medical center investor townhouses, student accommodation, and high-yield returns"},

    # Bayside & South Eastern Municipalities (Bayside, Glen Eira, Kingston, Stonnington)
    {"suburb": "Brighton", "postcode": "3186", "lga": "City of Bayside", "region": "Bayside", "highlights": "Dendy Street bathing box luxury homes, Church Street retail residences, and bespoke wealth loans"},
    {"suburb": "Sandringham", "postcode": "3191", "lga": "City of Bayside", "region": "Bayside", "highlights": "coastal village lifestyle, seaside family residences, and variable rate discount negotiations"},
    {"suburb": "Caulfield", "postcode": "3162", "lga": "City of Glen Eira", "region": "South East", "highlights": "racecourse precinct townhouses, Monash campus apartments, and investor interest-only lending"},
    {"suburb": "Bentleigh", "postcode": "3204", "lga": "City of Glen Eira", "region": "South East", "highlights": "Centre Road shopping strip family homes, dual-occupancy construction, and fast pre-approvals"},
    {"suburb": "Cheltenham", "postcode": "3192", "lga": "City of Kingston", "region": "Bayside South", "highlights": "Southland shopping center precinct, entry-level Bayside units, and cash rebate refinancing"},
    {"suburb": "Moorabbin", "postcode": "3189", "lga": "City of Kingston", "region": "South East", "highlights": "commercial business warehouse loans, transport-oriented development units, and ABN mortgages"},
    {"suburb": "Toorak", "postcode": "3142", "lga": "City of Stonnington", "region": "Inner South-East", "highlights": "Australia's premier luxury real estate, complex trust & company borrowing, and ultra-high-net-worth solutions"},
    {"suburb": "Malvern", "postcode": "3144", "lga": "City of Stonnington", "region": "Inner South-East", "highlights": "historic Glenferrie road estates, Malvern Central properties, and family wealth transfer planning"},
    {"suburb": "Prahran", "postcode": "3181", "lga": "City of Stonnington", "region": "Inner South-East", "highlights": "Chapel Street urban lifestyle apartments, boutique shopfronts, and contractor low-doc finance"},

    # Western Municipalities (Brimbank, Hobsons Bay, Maribyrnong, Melton, Moonee Valley, Wyndham)
    {"suburb": "Sunshine", "postcode": "3020", "lga": "City of Brimbank", "region": "Western Melbourne", "highlights": "super-hub transport upgrades, high-capital-growth potential, and affordable entry refinancing"},
    {"suburb": "Taylors Lakes", "postcode": "3038", "lga": "City of Brimbank", "region": "North-West", "highlights": "Watergardens town center proximity, large family residences, and equity cashouts"},
    {"suburb": "Altona", "postcode": "3018", "lga": "City of Hobsons Bay", "region": "Western Bayside", "highlights": "coastal beachside cottages, modern townhomes, and competitive offset account setups"},
    {"suburb": "Williamstown", "postcode": "3016", "lga": "City of Hobsons Bay", "region": "Western Bayside", "highlights": "historic maritime village properties, waterfront prestige homes, and premium lender rate discounts"},
    {"suburb": "Footscray", "postcode": "3011", "lga": "City of Maribyrnong", "region": "Inner West", "highlights": "rapidly gentrifying cultural hub, new hospital precinct apartments, and first-home buyer schemes"},
    {"suburb": "Yarraville", "postcode": "3013", "lga": "City of Maribyrnong", "region": "Inner West", "highlights": "Sun Theatre village charm, character Edwardian homes, and young family upgrade loans"},
    {"suburb": "Caroline Springs", "postcode": "3023", "lga": "City of Melton", "region": "Western Melbourne", "highlights": "lakefront masterplanned living, family upgrade finance, and low-rate fixed-to-variable switches"},
    {"suburb": "Fraser Rise", "postcode": "3336", "lga": "City of Melton", "region": "Western Melbourne", "highlights": "vibrant new housing developments, first home builder grants, and 5% deposit guarantees"},
    {"suburb": "Aintree", "postcode": "3336", "lga": "City of Melton", "region": "Western Melbourne", "highlights": "Woodlea estate premium homes, family-oriented lending packages, and land-and-build approvals"},
    {"suburb": "Essendon", "postcode": "3040", "lga": "City of Moonee Valley", "region": "Inner North-West", "highlights": "prestige period family homes, Maribyrnong river frontage, and high-income tax structuring"},
    {"suburb": "Moonee Ponds", "postcode": "3039", "lga": "City of Moonee Valley", "region": "Inner North-West", "highlights": "Puckle Street shopping strip, racetrack precinct towers, and fast-track loan applications"},
    {"suburb": "Point Cook", "postcode": "3030", "lga": "City of Wyndham", "region": "Western Melbourne", "highlights": "Sanctuary Lakes luxury waterfronts, Alamanda school zone properties, and equity cashouts"},
    {"suburb": "Tarneit", "postcode": "3029", "lga": "City of Wyndham", "region": "Western Growth Corridor", "highlights": "Australia's top growth corridor, affordable first homes, 5% deposit grants, and investor rentals"},
    {"suburb": "Truganina", "postcode": "3029", "lga": "City of Wyndham", "region": "Western Growth Corridor", "highlights": "industrial and residential expansion, modern family homes, and low-doc ABN contractor loans"},
    {"suburb": "Werribee", "postcode": "3030", "lga": "City of Wyndham", "region": "Western Melbourne", "highlights": "heritage riverfront township, expansive block renovations, and $2,000+ cashback refinancing"},
    {"suburb": "Williams Landing", "postcode": "3027", "lga": "City of Wyndham", "region": "Western Melbourne", "highlights": "transit-oriented masterplanned living, executive townhouses, and business owner borrowing power"},
    {"suburb": "Hoppers Crossing", "postcode": "3029", "lga": "City of Wyndham", "region": "Western Melbourne", "highlights": "established family properties, Werribee Plaza precinct, and competitive rate comparisons"},
    {"suburb": "Manor Lakes", "postcode": "3024", "lga": "City of Wyndham", "region": "Western Growth Corridor", "highlights": "lakefront community estates, new railway connectivity, and first home buyer support"}
]

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text.strip('-')

def generate_suburb_html(sub):
    s_name = sub["suburb"]
    p_code = sub["postcode"]
    lga = sub["lga"]
    region = sub["region"]
    highlights = sub["highlights"]
    slug = f"mortgage-broker-{slugify(s_name)}"

    # Generate Nearby Suburbs links (carousel/list)
    nearby_subs = [s for s in MELBOURNE_SUBURBS if s["suburb"] != s_name][:8]
    nearby_html = ""
    for ns in nearby_subs:
        n_name = ns["suburb"]
        n_code = ns["postcode"]
        n_slug = f"mortgage-broker-{slugify(n_name)}.html"
        nearby_html += f"""            <a href="/pages/locations/{n_slug}" style="display:flex; justify-content:space-between; align-items:center; padding:9px 12px; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; text-decoration:none; color:#0A2540; font-size:0.85rem; font-weight:700; transition:all 0.2s ease;">
              <span>📍 {html.escape(n_name)}</span>
              <span style="font-size:0.75rem; color:#64748B;">({n_code}) &rarr;</span>
            </a>\n"""

    # Generate Recent Articles widget
    recent_articles_html = ""
    for idx, rp in enumerate(recent_posts[:3]):
        rt = rp.get("title", "")
        rslug = rp.get("slug", "")
        rimg = rp.get("heroImage") or "https://images.pexels.com/photos/1181354/pexels-photo-1181354.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
        rurl = f"/pages/blog/{rslug}.html"
        recent_articles_html += f"""            <a href="{rurl}" style="display:flex; gap:10px; align-items:center; text-decoration:none; padding:8px 0; border-bottom:1px solid #F1F5F9;">
              <img src="{rimg}" alt="{html.escape(rt)}" style="width:54px; height:44px; object-fit:cover; border-radius:6px; flex-shrink:0;">
              <div style="min-width:0;">
                <h5 style="margin:0 0 2px; font-size:0.8rem; font-weight:700; color:#0A2540; line-height:1.3; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{html.escape(rt)}</h5>
                <span style="font-size:0.7rem; color:#00876C; font-weight:700;">23 Aug 2026</span>
              </div>
            </a>\n"""

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <link rel="icon" type="image/webp" href="/images/ez-mortgage-broker.webp">
  <link rel="apple-touch-icon" href="/images/ez-mortgage-broker.webp">
  <meta name="theme-color" content="#0A2540">

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Top-rated mortgage broker in {html.escape(s_name)} VIC {p_code} ({html.escape(lga)}). Compare 30+ accredited banks and lenders for home loans, refinancing, first home buyer grants, and alt-doc solutions.">
  <title>Mortgage Broker {html.escape(s_name)} VIC {p_code} | Home Loans &amp; Refinancing | EZ Mortgage Broker</title>
  <link rel="canonical" href="https://ezmortgagebroker.com.au/pages/locations/{slug}.html">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/calculators.css">

  <!-- Open Graph -->
  <meta property="og:title" content="Expert Mortgage Broker {html.escape(s_name)} VIC {p_code} | EZ Mortgage Broker">
  <meta property="og:description" content="Looking for the best home loan in {html.escape(s_name)}? Compare 30+ lenders, access competitive rates, and secure expert MFAA accredited guidance with 100% free service.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://ezmortgagebroker.com.au/pages/locations/{slug}.html">
  <meta property="og:site_name" content="EZ Mortgage Broker">
  <meta property="og:image" content="https://ezmortgagebroker.com.au/images/assets-ez-mortgage-broker/melbourne-suburb-property-valuation.jpg">

  <!-- FinancialService Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FinancialService",
    "name": "EZ Mortgage Broker - {html.escape(s_name)}",
    "image": "https://ezmortgagebroker.com.au/images/ez-mortgage-broker.webp",
    "@id": "https://ezmortgagebroker.com.au/#organization",
    "url": "https://ezmortgagebroker.com.au/pages/locations/{slug}.html",
    "telephone": "+611300050099",
    "priceRange": "$$",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "470 St Kilda Rd",
      "addressLocality": "Melbourne",
      "addressRegion": "VIC",
      "postalCode": "3004",
      "addressCountry": "AU"
    }},
    "geo": {{
      "@type": "GeoCoordinates",
      "latitude": -37.842718,
      "longitude": 144.976543
    }},
    "areaServed": [
      "{html.escape(s_name)}",
      "{html.escape(lga)}",
      "Melbourne",
      "Victoria"
    ],
    "openingHoursSpecification": [
      {{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "08:30",
        "closes": "18:00"
      }},
      {{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Saturday"],
        "opens": "09:00",
        "closes": "15:00"
      }}
    ]
  }}
  </script>

  <!-- FAQPage Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{
        "@type": "Question",
        "name": "Does using a mortgage broker in {html.escape(s_name)} cost me money?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "No. Our mortgage broking service for residential home loans and refinancing in {html.escape(s_name)} is 100% free for borrowers. We are remunerated directly by the lender upon successful settlement."
        }}
      }},
      {{
        "@type": "Question",
        "name": "How many lenders do you compare for {html.escape(s_name)} properties?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "Through our National Mortgage Brokers (nMB) accreditation, we feature more than 30 residential and commercial lenders on our panel, providing direct access to over 500 competitive home loan products."
        }}
      }},
      {{
        "@type": "Question",
        "name": "Can self-employed or ABN holders in {html.escape(s_name)} get approved without 2 years of tax returns?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "Yes. We specialize in low-doc and alt-doc mortgages using 1-year tax returns, 6 months of BAS statements, or an accountant declaration letter."
        }}
      }}
    ]
  }}
  </script>

  <style>
    .container, .article-container {{
      width: 98% !important;
      max-width: 1920px !important;
      margin: 0 auto;
      padding: 0 clamp(16px, 1.8vw, 32px);
      box-sizing: border-box;
    }}
    .site-header .logo {{
      margin-left: 4cm !important;
      display: flex;
      align-items: center;
    }}
    .site-header .brand-logo {{
      height: 48px;
      width: auto;
      display: block;
    }}
    .article-header {{
      position: relative;
      background-color: #0A2540;
      color: #ffffff !important;
      padding: 52px 0 44px;
      overflow: hidden;
      border-radius: 0 0 16px 16px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
    }}
    .article-header-bg {{
      position: absolute;
      top: -15px; left: -15px; right: -15px; bottom: -15px;
      background-image: url('/images/assets-ez-mortgage-broker/melbourne-suburb-property-valuation.jpg');
      background-size: cover;
      background-position: center 30%;
      filter: blur(3px) brightness(0.85) saturate(1.1);
      transform: scale(1.05);
      z-index: 1;
    }}
    .article-header-overlay {{
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(180deg, rgba(10, 37, 64, 0.6) 0%, rgba(10, 37, 64, 0.92) 100%);
      z-index: 2;
    }}
    .article-header-content {{
      position: relative;
      z-index: 3;
    }}
    .article-top-toolbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 20px;
    }}
    .article-last-updated-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(10, 37, 64, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.45);
      backdrop-filter: blur(12px);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      color: #ffffff !important;
    }}
    .article-header h1 {{
      font-size: clamp(1.8rem, 3.5vw, 2.6rem);
      font-weight: 800;
      color: #ffffff !important;
      margin-bottom: 16px;
      line-height: 1.25;
    }}
    .article-lead {{
      font-size: clamp(1rem, 1.25vw, 1.18rem);
      color: rgba(255, 255, 255, 0.92);
      line-height: 1.6;
      max-width: 900px;
      margin-bottom: 24px;
    }}
    .article-body-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 350px;
      gap: 36px;
      margin-top: 36px;
      margin-bottom: 60px;
      align-items: start;
    }}
    @media (max-width: 992px) {{
      .article-body-grid {{
        grid-template-columns: 1fr;
      }}
      .site-header .logo {{
        margin-left: 0 !important;
      }}
      .article-sidebar-col {{
        position: static !important;
      }}
    }}
    .article-sidebar-col {{
      position: sticky;
      top: 24px;
      align-self: start;
    }}
    .article-main-col {{
      min-width: 0;
      font-size: 1.05rem;
      line-height: 1.8;
      color: #1e293b;
    }}
    .article-main-col h2 {{
      font-size: 1.65rem;
      font-weight: 800;
      color: #0A2540;
      margin-top: 40px;
      margin-bottom: 16px;
      padding-bottom: 8px;
      border-bottom: 2px solid #e2e8f0;
    }}
    .article-main-col h3 {{
      font-size: 1.3rem;
      font-weight: 700;
      color: #0A2540;
      margin-top: 28px;
      margin-bottom: 12px;
    }}
    .article-data-table-wrapper {{
      overflow-x: auto;
      margin: 24px 0;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
    }}
    .article-data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.92rem;
      text-align: left;
    }}
    .article-data-table thead {{
      background: #0A2540 !important;
    }}
    .article-data-table th {{
      background: #0A2540 !important;
      color: #ffffff !important;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 14px 16px;
      border: none;
    }}
    .article-data-table td {{
      padding: 14px 16px;
      border-bottom: 1px solid #f1f5f9;
      color: #334155;
    }}
    .article-data-table tr:hover {{
      background: #f8fafc;
    }}
    .suburb-usp-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      margin: 28px 0;
    }}
    .suburb-usp-card {{
      background: #ffffff;
      border: 1.5px solid #e2e8f0;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(10,37,64,0.03);
    }}
    .suburb-usp-card h4 {{
      font-size: 1.05rem;
      font-weight: 800;
      color: #0A2540;
      margin: 0 0 8px;
    }}
    .suburb-usp-card p {{
      font-size: 0.88rem;
      line-height: 1.55;
      color: #475569;
      margin: 0;
    }}
    .faq-item {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
    }}
    .faq-item h4 {{
      margin: 0 0 8px;
      font-size: 1.1rem;
      font-weight: 700;
      color: #0A2540;
    }}
    .faq-item p {{
      margin: 0;
      color: #475569;
      font-size: 0.95rem;
      line-height: 1.6;
    }}
    .sidebar-widget-block {{
      background: #ffffff;
      border: 1.5px solid #E2E8F0;
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 6px 18px rgba(10,37,64,0.04);
    }}
    .sidebar-widget-title {{
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 800;
      color: #0A2540;
      margin: 0 0 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .broker-sticky-card {{
      background: #ffffff;
      border: 1.5px solid #E2E8F0;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 8px 24px rgba(10,37,64,0.06);
      margin-bottom: 20px;
    }}
    .broker-cover-header {{
      height: 105px;
      width: 100%;
      background-image: url('/images/headers/marquee-background-1600x500-1.webp');
      background-size: cover;
      background-position: center;
    }}
    .broker-box-body {{
      padding: 0 20px 24px;
      position: relative;
      text-align: center;
    }}
    .broker-avatar-wrapper {{
      width: 116px;
      height: 116px;
      border-radius: 50%;
      border: 4px solid #ffffff;
      box-shadow: 0 6px 20px rgba(0,135,108,0.25);
      margin: -58px auto 10px;
      overflow: hidden;
      background: #ffffff;
    }}
    .broker-box-avatar {{
      width: 100%;
      height: 100%;
      display: block;
      object-fit: cover;
      object-position: center 20%;
      transform: scale(1.22);
      filter: brightness(1.14) contrast(1.06);
    }}
  </style>
</head>
<body style="font-family:'Inter',sans-serif; background:#F8FAFC; color:#0A2540; margin:0;">

  <!-- ========== FULL SITE HEADER (Logo moved 4cm to the right) ========== -->
  <header class="site-header">
    <div class="header-top" style="background:#0A2540; color:#E2E8F0; font-size:0.8rem; padding:6px 0;">
      <div class="container header-top-inner" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
        <div class="breaking-news-ticker" style="display:inline-flex; align-items:center; gap:8px;">
          <strong class="breaking-news-badge" style="background:#EAB308; color:#0A2540; padding:2px 8px; border-radius:4px; font-weight:900; font-size:0.72rem;">⚡ BREAKING NEWS</strong>
          <span class="breaking-news-title">Mortgage brokers settle record 81.0% of all Australian residential home loans</span>
        </div>
        <div class="header-contact-group" style="display:flex; align-items:center; gap:16px;">
          <span class="header-date">📅 Sun, 23 Aug</span>
          <a href="tel:1300050099" style="color:#ffffff; text-decoration:none; font-weight:700;">📞 1300 050 099</a>
          <a href="mailto:info@ezmortgagebroker.com.au" style="color:#ffffff; text-decoration:none;">✉️ info@ezmortgagebroker.com.au</a>
          <span>📍 Melbourne, VIC</span>
        </div>
      </div>
    </div>
    
    <div class="header-main" style="background:#ffffff; border-bottom:1px solid #E2E8F0; padding:12px 0;">
      <div class="container" style="display:flex; align-items:center; justify-content:space-between;">
        <a href="/" class="logo"><img class="brand-logo" src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" width="220" height="64" style="height:46px; width:auto;"></a>
        
        <nav style="display:flex; align-items:center; gap:20px;">
          <a href="/" style="color:#0A2540; text-decoration:none; font-weight:600; font-size:0.92rem;">Home</a>
          <a href="/#loan-solutions" style="color:#0A2540; text-decoration:none; font-weight:600; font-size:0.92rem;">Loan Services</a>
          <a href="/locations.html" style="color:#1D4ED8; text-decoration:none; font-weight:800; font-size:0.92rem;">Locations</a>
          <a href="/calculators.html" style="color:#0A2540; text-decoration:none; font-weight:600; font-size:0.92rem;">Calculators</a>
          <a href="/pages/blog.html" style="color:#0A2540; text-decoration:none; font-weight:600; font-size:0.92rem;">News &amp; Insights</a>
          <a href="tel:1300050099" style="padding:8px 16px; border-radius:8px; border:1.5px solid #00876C; color:#00876C; font-weight:700; text-decoration:none; font-size:0.9rem;">📞 1300 050 099</a>
          <a href="/calculators.html" style="padding:8px 18px; border-radius:8px; background:#00876C; color:#ffffff; font-weight:700; text-decoration:none; font-size:0.9rem; box-shadow:0 4px 12px rgba(0,135,108,0.25);">Book Consultation</a>
        </nav>
      </div>
    </div>
  </header>

  <!-- Location Header Banner -->
  <header class="article-header">
    <div class="article-header-bg"></div>
    <div class="article-header-overlay"></div>
    <div class="container article-header-content">
      <div class="article-top-toolbar">
        <span class="article-last-updated-badge">
          📍 {html.escape(region)} · {html.escape(lga)} · Postcode {p_code}
        </span>
        <span style="font-size:0.84rem; color:rgba(255,255,255,0.85); font-weight:600;">
          MFAA Accredited Finance Broker · CRN: 538522
        </span>
      </div>

      <h1>Mortgage Broker {html.escape(s_name)} VIC {p_code}</h1>
      <p class="article-lead">
        Secure market-leading home loan rates, maximize your borrowing capacity, and access over 30+ accredited Australian lenders. Expert local mortgage broking tailored for {html.escape(s_name)} buyers, investors, and homeowners.
      </p>

      <div style="display:flex; flex-wrap:wrap; gap:12px; margin-top:20px;">
        <a href="/calculators.html" style="background:#00876C; color:#ffffff; font-weight:800; padding:12px 26px; border-radius:8px; text-decoration:none; font-size:0.95rem; box-shadow:0 4px 14px rgba(0,135,108,0.3);">Calculate Borrowing Power</a>
        <a href="tel:1300050099" style="background:rgba(255,255,255,0.15); border:1.5px solid rgba(255,255,255,0.6); color:#ffffff; font-weight:700; padding:12px 24px; border-radius:8px; text-decoration:none; font-size:0.95rem; backdrop-filter:blur(8px);">Speak with {html.escape(s_name)} Specialist</a>
      </div>
    </div>
  </header>

  <!-- Main Content Layout -->
  <main class="container">
    <div class="article-body-grid">
      
      <!-- Article / Location Content -->
      <div class="article-main-col">
        
        <h2>Local Mortgage &amp; Property Insights for {html.escape(s_name)}</h2>
        <p>
          Whether you are purchasing your first home, upgrading to a larger family residence, or refinancing an existing mortgage in <strong>{html.escape(s_name)} ({p_code})</strong>, having a dedicated mortgage broker who understands the {html.escape(lga)} property landscape provides an unmatched advantage.
        </p>
        <p>
          {html.escape(s_name)} is renowned for {html.escape(highlights)}. In today's dynamic interest rate cycle, navigating the +3.00% APRA serviceability buffer requires strategic lender selection to ensure your application gets approved smoothly without unnecessary stress.
        </p>

        <!-- USPs -->
        <div class="suburb-usp-grid">
          <div class="suburb-usp-card">
            <h4>🏆 30+ Accredited Lenders</h4>
            <p>Direct panel access to Big 4 banks, regional banks, and tier-1 non-bank lenders offering exclusive broker specials.</p>
          </div>
          <div class="suburb-usp-card">
            <h4>⚡ $0 Cost to You</h4>
            <p>Our residential broking services are 100% free to borrowers, remunerated directly by the chosen lender upon settlement.</p>
          </div>
          <div class="suburb-usp-card">
            <h4>📄 Alt-Doc &amp; Self-Employed</h4>
            <p>Tailored solutions for contractors, business owners, and trust structures with 1-year tax returns or BAS verification.</p>
          </div>
        </div>

        <!-- Lending Comparison Table -->
        <h2>{html.escape(s_name)} Lending Options &amp; Eligibility Overview</h2>
        <div class="article-data-table-wrapper">
          <table class="article-data-table">
            <thead>
              <tr>
                <th>Loan Product</th>
                <th>Typical Deposit</th>
                <th>Serviceability Assessment</th>
                <th>Best Suited For</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>First Home Buyer Guarantee</strong></td>
                <td>5% (No LMI)</td>
                <td>Standard APRA +3.00%</td>
                <td>Eligible Australian citizens &amp; PRs purchasing in {html.escape(s_name)}</td>
              </tr>
              <tr>
                <td><strong>Variable Rate Refinance</strong></td>
                <td>10% - 20% equity</td>
                <td>1% Modified Refinance Buffer</td>
                <td>Borrowers switching to competitive market rates</td>
              </tr>
              <tr>
                <td><strong>Self-Employed Alt-Doc</strong></td>
                <td>15% - 20%</td>
                <td>1-Year Financials / 6-Month BAS</td>
                <td>Sole traders, company directors, and contractors in {html.escape(lga)}</td>
              </tr>
              <tr>
                <td><strong>SMSF Property Lending</strong></td>
                <td>20% - 30%</td>
                <td>Super contributions &amp; rental income</td>
                <td>Trustees acquiring residential or commercial real estate</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- FAQs -->
        <h2>Frequently Asked Questions ({html.escape(s_name)} Borrowers)</h2>
        <div class="faq-item">
          <h4>Does using a mortgage broker in {html.escape(s_name)} cost me money?</h4>
          <p>No. Our mortgage broking service for residential home loans and refinancing in {html.escape(s_name)} is 100% free for borrowers. We are remunerated directly by the lender upon successful settlement.</p>
        </div>
        <div class="faq-item">
          <h4>How many lenders do you compare for {html.escape(s_name)} properties?</h4>
          <p>Through our National Mortgage Brokers (nMB) accreditation, we feature more than 30 residential and commercial lenders on our panel, providing direct access to over 500 competitive home loan products.</p>
        </div>
        <div class="faq-item">
          <h4>Can self-employed or ABN holders in {html.escape(s_name)} get approved without 2 years of tax returns?</h4>
          <p>Yes. We specialize in low-doc and alt-doc mortgages using 1-year tax returns, 6 months of BAS statements, or an accountant declaration letter.</p>
        </div>

      </div>

      <!-- Right Column (Col 2 Fixed/Sticky: Broker Details + Recent Articles + Collapsible Nearby Suburbs Accordion) -->
      <aside class="article-sidebar-col">
        
        <!-- 1. Broker Profile Details Card -->
        <div class="broker-sticky-card">
          <div class="broker-cover-header"></div>
          <div class="broker-box-body">
            <div class="broker-avatar-wrapper">
              <img src="/images/r-bakshi.jpeg" alt="R Bakshi - Principal Mortgage Broker" class="broker-box-avatar" width="116" height="116">
            </div>
            <h4 style="font-size:1.15rem; font-weight:800; color:#0A2540; margin:0 0 2px;">R BAKSHI</h4>
            <div style="font-size:0.75rem; font-weight:700; color:#00876C; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.04em;">
              Principal Finance Broker (MFAA ACCREDITED)
            </div>
            <div style="color:#EAB308; font-size:0.85rem; font-weight:800; margin-bottom:10px;">
              ★★★★★ <span style="color:#64748B; font-size:0.75rem; font-weight:600;">(14 Google Reviews)</span>
            </div>
            <p style="font-size:0.82rem; color:#64748b; line-height:1.55; margin:0 0 14px;">
              Specializing in Melbourne residential property finance, self-employed lending, and wealth restructuring across 30+ accredited lenders.
            </p>
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px; font-size:0.75rem; color:#475569; text-align:left; margin-bottom:14px;">
              <div><strong>CRN:</strong> 538522</div>
              <div><strong>Aggregator:</strong> National Mortgage Brokers (nMB)</div>
              <div><strong>Panel:</strong> 30+ Accredited Lenders</div>
            </div>
            <a href="tel:1300050099" style="display:block; background:#00876C; color:#ffffff; font-weight:800; padding:10px; border-radius:8px; text-decoration:none; font-size:0.9rem; margin-bottom:8px;">
              📞 Call 1300 050 099
            </a>
            <a href="/calculators.html" style="display:block; background:#0A2540; color:#ffffff; font-weight:700; padding:9px; border-radius:8px; text-decoration:none; font-size:0.85rem;">
              Book Appointment
            </a>
          </div>
        </div>

        <!-- 2. Latest Market News & Recent Articles (Moved ABOVE Suburb list) -->
        <div class="sidebar-widget-block">
          <h4 class="sidebar-widget-title">
            <span>Recent Market News</span>
            <span style="font-size:0.72rem; color:#00876C; font-weight:700;">Updated Daily</span>
          </h4>
          <div style="display:flex; flex-direction:column;">
{recent_articles_html}          </div>
          <a href="/pages/blog.html" style="display:block; text-align:center; margin-top:12px; font-size:0.82rem; font-weight:800; color:#1D4ED8; text-decoration:none;">
            View All Market News &rarr;
          </a>
        </div>

        <!-- 3. Nearby Suburb Guides (Collapsed Accordion below Recent News) -->
        <details style="background:#ffffff; border:1.5px solid #E2E8F0; border-radius:16px; padding:16px; margin-bottom:20px; box-shadow:0 6px 18px rgba(10,37,64,0.04);">
          <summary style="font-size:0.85rem; text-transform:uppercase; letter-spacing:0.08em; font-weight:800; color:#0A2540; cursor:pointer; list-style:none; display:flex; justify-content:space-between; align-items:center; user-select:none;">
            <span>📍 Nearby Suburb Guides</span>
            <span style="font-size:0.75rem; color:#1D4ED8; font-weight:700; background:#EFF6FF; padding:3px 8px; border-radius:12px;">+ View Suburbs</span>
          </summary>
          <div style="display:flex; flex-direction:column; gap:6px; margin-top:14px;">
{nearby_html}          </div>
          <a href="/locations.html" style="display:block; text-align:center; margin-top:10px; font-size:0.8rem; font-weight:700; color:#00876C; text-decoration:none;">
            Browse All 91 Suburbs &rarr;
          </a>
        </details>

      </aside>

    </div>
  </main>

  <!-- Site Footer -->
  <footer style="background:#0A2540; color:rgba(255,255,255,0.8); padding:40px 0 24px; margin-top:60px; font-size:0.85rem;">
    <div class="container" style="text-align:center;">
      <p style="margin:0 0 10px; color:#ffffff; font-weight:700;">EZ Mortgage Broker — Australia-Wide Mortgage Advisory</p>
      <p style="max-width:800px; margin:0 auto 16px; color:rgba(255,255,255,0.65); line-height:1.5;">
        R Bakshi is an MFAA Accredited Finance Broker (Credit Representative Number 538522) operating under National Mortgage Brokers (nMB). Access to 30+ lenders and 500+ home loan products across Australia.
      </p>
      <div style="border-top:1px solid rgba(255,255,255,0.15); padding-top:16px; font-size:0.78rem; color:rgba(255,255,255,0.5);">
        &copy; {datetime.now().year} EZ Mortgage Broker. All Rights Reserved. · <a href="/terms-of-use.html" style="color:rgba(255,255,255,0.7); text-decoration:none;">Terms of Use</a> · <a href="/cookie-policy.html" style="color:rgba(255,255,255,0.7); text-decoration:none;">Privacy Policy</a>
      </div>
    </div>
  </footer>

</body>
</html>"""

def main():
    print(f"🚀 Regenerating {len(MELBOURNE_SUBURBS)} Suburb Pages (Logo moved 4cm right + Col 3 Nearby Suburbs Carousel & Articles)...")
    for sub in MELBOURNE_SUBURBS:
        s_html = generate_suburb_html(sub)
        slug = f"mortgage-broker-{slugify(sub['suburb'])}.html"
        
        for d in [LOCATIONS_DIR, PUB_LOCATIONS_DIR]:
            with open(os.path.join(d, slug), "w", encoding="utf-8") as f:
                f.write(s_html)

    print(f"✅ Successfully regenerated {len(MELBOURNE_SUBURBS)} suburb pages!")

if __name__ == "__main__":
    main()
