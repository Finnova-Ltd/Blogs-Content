#!/usr/bin/env python3
"""
Comprehensive Melbourne Suburb & LGA SEO Engine + Longtail Pillar Generator
Generates high-converting localized suburb landing pages and buyer persona / policy pillar pages
for EZ Mortgage Broker matching the strict layout, MFAA accreditation, and Schema.org standards.
"""

import os
import sys
import re
import json
import html
from datetime import datetime

ROOT_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
LOCATIONS_DIR = os.path.join(ROOT_DIR, "pages", "locations")
PUB_LOCATIONS_DIR = os.path.join(ROOT_DIR, "public", "pages", "locations")
BLOG_DIR = os.path.join(ROOT_DIR, "pages", "blog")
PUB_BLOG_DIR = os.path.join(ROOT_DIR, "public", "pages", "blog")
POSTS_JSON = os.path.join(ROOT_DIR, "posts.json")
PUB_POSTS_JSON = os.path.join(ROOT_DIR, "public", "posts.json")

for p in [LOCATIONS_DIR, PUB_LOCATIONS_DIR, BLOG_DIR, PUB_BLOG_DIR]:
    os.makedirs(p, exist_ok=True)

# Melbourne LGA & Suburb Registry provided by user
MELBOURNE_SUBURBS = [
    # City of Melbourne
    {"suburb": "Melbourne CBD", "postcode": "3000", "lga": "City of Melbourne", "region": "Inner Melbourne", "highlights": "high-density apartments, commercial loan options, and CBD professional investor lending"},
    {"suburb": "Carlton", "postcode": "3053", "lga": "City of Melbourne", "region": "Inner North", "highlights": "heritage Victorian terrace refinancing, university precinct investments, and alt-doc doctor loans"},
    {"suburb": "Carlton North", "postcode": "3054", "lga": "City of Melbourne", "region": "Inner North", "highlights": "period home renovations, Rathdowne Village family purchases, and equity cashouts"},
    {"suburb": "Docklands", "postcode": "3008", "lga": "City of Melbourne", "region": "Inner Waterfront", "highlights": "waterfront high-rise apartment lending, high-LVR off-the-plan finance, and investor yields"},
    {"suburb": "East Melbourne", "postcode": "3002", "lga": "City of Melbourne", "region": "Inner East", "highlights": "prestige luxury properties, medical specialist loans, and private banking panel comparisons"},
    {"suburb": "Flemington", "postcode": "3031", "lga": "City of Melbourne", "region": "Inner West", "highlights": "period homes, first home buyer apartments, and racecourse precinct properties"},
    {"suburb": "Kensington", "postcode": "3031", "lga": "City of Melbourne", "region": "Inner West", "highlights": "warehouse conversions, young professional buyer grants, and low-doc self-employed lending"},
    {"suburb": "North Melbourne", "postcode": "3051", "lga": "City of Melbourne", "region": "Inner North", "highlights": "hospital precinct residential loans, terrace home renovations, and townhouse refinancing"},
    {"suburb": "Parkville", "postcode": "3052", "lga": "City of Melbourne", "region": "Inner North", "highlights": "biomedical and academic specialist home loans, premium family homes, and heritage estates"},
    {"suburb": "Port Melbourne", "postcode": "3207", "lga": "City of Melbourne", "region": "Bayside", "highlights": "Beacon Cove luxury beachside residences, Fisherman's Bend developments, and equity releases"},
    {"suburb": "Southbank", "postcode": "3006", "lga": "City of Melbourne", "region": "Inner City", "highlights": "high-yield corporate apartments, investor portfolios, and fast refinancing approvals"},
    {"suburb": "South Yarra", "postcode": "3141", "lga": "City of Melbourne", "region": "Inner South-East", "highlights": "Toorak Road luxury apartments, heritage cottages, and high-net-worth borrowing power"},
    {"suburb": "West Melbourne", "postcode": "3003", "lga": "City of Melbourne", "region": "Inner West", "highlights": "emerging urban village townhouses, mixed-use commercial lending, and first home buyer concessions"},

    # City of Port Phillip
    {"suburb": "Albert Park", "postcode": "3206", "lga": "City of Port Phillip", "region": "Bayside", "highlights": "Victorian & Edwardian heritage restorations, lake-view luxury homes, and portfolio restructuring"},
    {"suburb": "Balaclava", "postcode": "3183", "lga": "City of Port Phillip", "region": "Inner South", "highlights": "Carlisle Street lifestyle apartments, art deco flats, and young professional refinancing"},
    {"suburb": "Elwood", "postcode": "3184", "lga": "City of Port Phillip", "region": "Bayside", "highlights": "Elwood canal character apartments, seaside family homes, and low-rate fixed-to-variable switches"},
    {"suburb": "Middle Park", "postcode": "3206", "lga": "City of Port Phillip", "region": "Bayside", "highlights": "prime coastal real estate, boutique development funding, and prestige interest-only structuring"},
    {"suburb": "Ripponlea", "postcode": "3185", "lga": "City of Port Phillip", "region": "Inner South", "highlights": "heritage estate surroundings, family home refinancing, and high-equity mortgage reviews"},
    {"suburb": "St Kilda", "postcode": "3182", "lga": "City of Port Phillip", "region": "Bayside", "highlights": "beachside apartments, boutique hospitality business loans, and investor portfolio refinance"},
    {"suburb": "St Kilda East", "postcode": "3183", "lga": "City of Port Phillip", "region": "Inner South", "highlights": "quiet residential enclaves, larger family apartments, and self-employed alt-doc approvals"},
    {"suburb": "South Melbourne", "postcode": "3205", "lga": "City of Port Phillip", "region": "Inner South", "highlights": "Emerald Hill Victorian terraces, market precinct properties, and commercial office mortgages"},

    # City of Yarra
    {"suburb": "Abbotsford", "postcode": "3067", "lga": "City of Yarra", "region": "Inner East", "highlights": "Yarra riverfront apartments, converted brewery lofts, and first home buyer guarantee loans"},
    {"suburb": "Alphington", "postcode": "3078", "lga": "City of Yarra", "region": "Inner North-East", "highlights": "Yarra Bend eco-estates, spacious family residences, and sustainable building finance"},
    {"suburb": "Burnley", "postcode": "3121", "lga": "City of Yarra", "region": "Inner East", "highlights": "tech precinct townhomes, riverbank cottages, and competitive bank comparison rates"},
    {"suburb": "Clifton Hill", "postcode": "3068", "lga": "City of Yarra", "region": "Inner North-East", "highlights": "heritage conservation homes, Quarries parkside properties, and multi-lender assessment solutions"},
    {"suburb": "Collingwood", "postcode": "3066", "lga": "City of Yarra", "region": "Inner East", "highlights": "industrial warehouse conversions, boutique retail loans, and creative freelancer alt-doc mortgages"},
    {"suburb": "Cremorne", "postcode": "3121", "lga": "City of Yarra", "region": "Inner East", "highlights": "Silicon Yarra commercial finance, luxury worker cottage expansions, and equity redraw facilities"},
    {"suburb": "Fairfield", "postcode": "3078", "lga": "City of Yarra", "region": "Inner North-East", "highlights": "Station Street family enclaves, leafy residential streets, and debt consolidation strategies"},
    {"suburb": "Fitzroy", "postcode": "3065", "lga": "City of Yarra", "region": "Inner North", "highlights": "Brunswick Street bohemian lofts, historic terrace valuations, and low-deposit loan programs"},
    {"suburb": "Fitzroy North", "postcode": "3068", "lga": "City of Yarra", "region": "Inner North", "highlights": "Edinburgh Gardens parkside family living, high-value renovations, and construction mortgages"},
    {"suburb": "Richmond", "postcode": "3121", "lga": "City of Yarra", "region": "Inner East", "highlights": "Bridge Road townhomes, sports precinct rentals, and rapid refinancing approval turnarounds"},

    # City of Banyule & Darebin
    {"suburb": "Heidelberg", "postcode": "3084", "lga": "City of Banyule", "region": "North East", "highlights": "Austin Health medical practitioner loans, hospital precinct rentals, and family home auctions"},
    {"suburb": "Ivanhoe", "postcode": "3079", "lga": "City of Banyule", "region": "North East", "highlights": "prestigious leafy avenues, high-value property equity release, and private school catchment purchases"},
    {"suburb": "Greensborough", "postcode": "3088", "lga": "City of Banyule", "region": "North East", "highlights": "family upgrade purchases, generous block renovations, and competitive comparison rate options"},
    {"suburb": "Bundoora", "postcode": "3083", "lga": "City of Banyule & Darebin", "region": "North", "highlights": "university investor units, Polaris estate townhouses, and first home buyer guarantees"},
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

def generate_suburb_html(sub):
    s_name = sub["suburb"]
    p_code = sub["postcode"]
    lga = sub["lga"]
    region = sub["region"]
    highlights = sub["highlights"]
    slug = f"mortgage-broker-{re.sub(r'[^a-z0-9]+', '-', s_name.lower()).strip('-')}"

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Top-rated mortgage broker in {html.escape(s_name)} VIC {p_code} ({lga}). Compare 30+ accredited banks and lenders for home loans, refinancing, first home buyer grants, and alt-doc solutions.">
  <title>Mortgage Broker {html.escape(s_name)} VIC {p_code} | Home Loans &amp; Refinancing | EZ Mortgage Broker</title>
  <link rel="canonical" href="https://ezmortgagebroker.com.au/pages/locations/{slug}.html">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">

  <!-- Open Graph -->
  <meta property="og:title" content="Expert Mortgage Broker {html.escape(s_name)} VIC {p_code} | EZ Mortgage Broker">
  <meta property="og:description" content="Looking for the best home loan in {html.escape(s_name)}? Compare 30+ lenders, access competitive rates, and secure expert MFAA accredited guidance with 100% free service.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://ezmortgagebroker.com.au/pages/locations/{slug}.html">
  <meta property="og:site_name" content="EZ Mortgage Broker">
  <meta property="og:image" content="https://ezmortgagebroker.com.au/images/assets-ez-mortgage-broker/melbourne-suburb-property-valuation.jpg">

  <!-- FinancialService Schema (LocalBusiness JSON-LD) -->
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
      width: 100%;
      max-width: 1420px;
      margin: 0 auto;
      padding: 0 clamp(16px, 2.5vw, 32px);
    }}
    .site-header {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #ffffff;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
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
      grid-template-columns: minmax(0, 1fr) 340px;
      gap: 40px;
      margin-top: 40px;
      margin-bottom: 60px;
    }}
    @media (max-width: 992px) {{
      .article-body-grid {{
        grid-template-columns: 1fr;
      }}
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
      letter-spacing: 0.05em;
      padding: 14px 18px;
      border-bottom: 2px solid #0A2540;
    }}
    .article-data-table td {{
      padding: 14px 18px;
      border-bottom: 1px solid #f1f5f9;
      color: #334155;
    }}
    .article-data-table tbody tr:nth-child(even) td {{
      background: #f8fafc;
    }}
    .feature-card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      margin: 28px 0;
    }}
    .feature-card {{
      background: #ffffff;
      border: 1.5px solid #e2e8f0;
      border-radius: 12px;
      padding: 22px;
      box-shadow: 0 4px 12px rgba(10, 37, 64, 0.04);
    }}
    .feature-card h4 {{
      font-size: 1.1rem;
      font-weight: 800;
      color: #0A2540;
      margin: 0 0 8px;
    }}
    .feature-card p {{
      font-size: 0.92rem;
      color: #475569;
      line-height: 1.55;
      margin: 0;
    }}
    .broker-profile-box {{
      position: sticky;
      top: 96px;
      background: #ffffff;
      border: 1px solid #E2E8F0;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 10px 25px rgba(10, 37, 64, 0.08);
      margin-bottom: 30px;
    }}
    .broker-cover-header {{
      height: 90px;
      width: 100%;
      background: url('/images/ez-broker-cover-header.jpg') center/cover no-repeat;
    }}
    .broker-box-body {{
      padding: 0 20px 24px;
      position: relative;
      text-align: center;
    }}
    .broker-box-avatar {{
      width: 88px;
      height: 88px;
      border-radius: 50%;
      border: 3px solid #ffffff;
      box-shadow: 0 4px 14px rgba(0,0,0,0.15);
      margin: -44px auto 12px;
      display: block;
      object-fit: cover;
      background: #ffffff;
    }}
  </style>
</head>
<body style="font-family:'Inter',sans-serif; background:#F8FAFC; color:#0A2540; margin:0;">

  <!-- Site Navigation -->
  <header class="site-header" style="padding: 12px 0; border-bottom: 1px solid #E2E8F0;">
    <div class="container" style="display:flex; align-items:center; justify-content:space-between;">
      <a href="/" style="display:flex; align-items:center; text-decoration:none;">
        <img src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" width="180" height="48" style="height:44px; width:auto;">
      </a>
      <div style="display:flex; align-items:center; gap:16px;">
        <a href="tel:1300050099" class="btn btn-outline" style="padding:8px 18px; border-radius:8px; border:1.5px solid #00876C; color:#00876C; font-weight:700; text-decoration:none; font-size:0.92rem;">📞 1300 050 099</a>
        <a href="/calculators.html" class="btn btn-primary" style="padding:9px 20px; border-radius:8px; background:#00876C; color:#ffffff; font-weight:700; text-decoration:none; font-size:0.92rem; box-shadow:0 4px 12px rgba(0,135,108,0.25);">Book Free Consultation</a>
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

        <div class="feature-card-grid">
          <div class="feature-card">
            <h4>🏆 30+ Accredited Lenders</h4>
            <p>Direct panel access to Big 4 banks, regional banks, and tier-1 non-bank lenders offering exclusive broker specials.</p>
          </div>
          <div class="feature-card">
            <h4>⚡ $0 Cost to You</h4>
            <p>Our residential broking services are 100% free to borrowers, remunerated directly by the chosen lender upon settlement.</p>
          </div>
          <div class="feature-card">
            <h4>📑 Alt-Doc &amp; Self-Employed</h4>
            <p>Tailored solutions for contractors, business owners, and trust structures with 1-year tax returns or BAS verification.</p>
          </div>
          <div class="feature-card">
            <h4>🔄 Refinance Cashbacks</h4>
            <p>Access up to $2,000–$4,000 refinance rebates and explore 1.00% modified buffer refinancing rules.</p>
          </div>
        </div>

        <h2>Lending Criteria &amp; Serviceability Comparison</h2>
        <p>
          Comparing bank policies is essential when purchasing in {html.escape(s_name)}. Below is how standard bank criteria compares against broker-accessed alternative lenders:
        </p>

        <div class="article-data-table-wrapper">
          <table class="article-data-table">
            <thead>
              <tr>
                <th>Lending Category</th>
                <th>Standard Major Bank Rule</th>
                <th>EZ Mortgage Broker Solution</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Serviceability Buffer</strong></td>
                <td>+3.00% above actual rate</td>
                <td>Access to 1.00% Modified Buffer for eligible refinancers</td>
              </tr>
              <tr>
                <td><strong>Self-Employed Income</strong></td>
                <td>Strict 2 full years of tax returns</td>
                <td>Alt-Doc options with 1-year returns or 6-month BAS</td>
              </tr>
              <tr>
                <td><strong>Deposit Requirements</strong></td>
                <td>20% deposit or mandatory LMI</td>
                <td>5% First Home Guarantee (0% LMI) &amp; Guarantor loans</td>
              </tr>
              <tr>
                <td><strong>SMSF Property Lending</strong></td>
                <td>Unavailable at most retail branches</td>
                <td>Specialist residential &amp; commercial SMSF LRBA lenders</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2>Frequently Asked Questions ({html.escape(s_name)} Borrowers)</h2>
        
        <h3>Does using a mortgage broker in {html.escape(s_name)} cost me money?</h3>
        <p>
          No. Our mortgage broking service for residential home loans and refinancing in {html.escape(s_name)} is completely free for borrowers. Under Australian National Consumer Credit Protection (NCCP) regulations, we are remunerated by the lender upon loan settlement.
        </p>

        <h3>How do I calculate how much I can borrow for a home in {html.escape(s_name)}?</h3>
        <p>
          Your borrowing capacity depends on your household gross income, number of financial dependents, ongoing credit card limits, and existing liabilities. Use our <a href="/calculators.html" style="color:#00876C; font-weight:700;">online borrowing power calculator</a> or contact our team for an exact pre-assessment across 30+ lender calculators.
        </p>

        <h3>Can I get pre-approval before making an offer at an auction in {html.escape(s_name)}?</h3>
        <p>
          Yes. We strongly recommend obtaining a formal pre-approval before bidding at an auction. A formal pre-approval provides confidence in your maximum bidding limit and ensures rapid formal approval once your contract of sale is signed.
        </p>

        <!-- CTA Banner -->
        <div style="background:linear-gradient(135deg, #0A2540 0%, #1D4ED8 100%); border-radius:14px; padding:32px; color:#ffffff; margin-top:40px; text-align:center; box-shadow:0 10px 28px rgba(10,37,64,0.18);">
          <h3 style="color:#ffffff; margin:0 0 12px; font-size:1.5rem;">Ready to Secure Your {html.escape(s_name)} Home Loan?</h3>
          <p style="color:rgba(255,255,255,0.9); margin:0 0 20px; font-size:1rem; max-width:640px; margin-left:auto; margin-right:auto;">
            Book a free, 15-minute consultation with R Bakshi — MFAA Accredited Finance Broker. Compare rates, unlock borrowing capacity, and get pre-approved.
          </p>
          <div style="display:flex; justify-content:center; gap:14px; flex-wrap:wrap;">
            <a href="/calculators.html" style="background:#00876C; color:#ffffff; font-weight:800; padding:12px 28px; border-radius:8px; text-decoration:none; font-size:0.95rem;">Book Free Strategy Session</a>
            <a href="tel:1300050099" style="background:#ffffff; color:#0A2540; font-weight:800; padding:12px 24px; border-radius:8px; text-decoration:none; font-size:0.95rem;">Call 1300 050 099</a>
          </div>
        </div>

      </div>

      <!-- Sticky Sidebar: Broker Profile & Quick Links -->
      <aside>
        <div class="broker-profile-box">
          <div class="broker-cover-header"></div>
          <div class="broker-box-body">
            <img src="/images/r-bakshi.jpeg" alt="R Bakshi - Mortgage Broker Melbourne" class="broker-box-avatar" width="88" height="88">
            <h4 style="font-size:1.15rem; font-weight:800; color:#0A2540; margin:0 0 4px;">R BAKSHI</h4>
            <div style="font-size:0.8rem; font-weight:700; color:#00876C; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.04em;">
              Principal Finance Broker (MFAA Accredited)
            </div>
            <p style="font-size:0.84rem; color:#64748b; line-height:1.55; margin:0 0 16px;">
              Specializing in Melbourne residential property finance, self-employed lending, and wealth restructuring across 30+ accredited lenders.
            </p>
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px; font-size:0.78rem; color:#475569; text-align:left; margin-bottom:16px;">
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

        <!-- Loan Pillar Shortcuts -->
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:22px; box-shadow:0 4px 12px rgba(10,37,64,0.04);">
          <h4 style="font-size:1rem; font-weight:800; color:#0A2540; margin:0 0 14px; border-bottom:1.5px solid #F1F5F9; padding-bottom:8px;">
            Popular Loan Pillars
          </h4>
          <ul style="list-style:none; padding:0; margin:0; font-size:0.88rem; line-height:2;">
            <li><a href="/pages/loans/self-employed-alt-doc-loans.html" style="color:#1D4ED8; text-decoration:none; font-weight:600;">💼 Self-Employed Alt-Doc Loans &rarr;</a></li>
            <li><a href="/pages/loans/ndis-sda-property-finance.html" style="color:#1D4ED8; text-decoration:none; font-weight:600;">🏡 NDIS SDA Property Finance &rarr;</a></li>
            <li><a href="/pages/blog/first-home-buyers-grant-2026-guide.html" style="color:#1D4ED8; text-decoration:none; font-weight:600;">🔑 First Home Guarantee 5% Deposit &rarr;</a></li>
            <li><a href="/pages/blog/how-to-refinance-mortgage-australia-playbook.html" style="color:#1D4ED8; text-decoration:none; font-weight:600;">🔄 Mortgage Refinancing Playbook &rarr;</a></li>
            <li><a href="/calculators.html" style="color:#1D4ED8; text-decoration:none; font-weight:600;">🧮 Borrowing Power Calculator &rarr;</a></li>
          </ul>
        </div>
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

def run_suburb_generation():
    print(f"🚀 Generating {len(MELBOURNE_SUBURBS)} Melbourne Suburb Landing Pages...")
    for sub in MELBOURNE_SUBURBS:
        s_name = sub["suburb"]
        slug = f"mortgage-broker-{re.sub(r'[^a-z0-9]+', '-', s_name.lower()).strip('-')}"
        html_code = generate_suburb_html(sub)
        
        for d in [LOCATIONS_DIR, PUB_LOCATIONS_DIR]:
            fpath = os.path.join(d, f"{slug}.html")
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(html_code)
        
        print(f"  ✅ Created: {slug}.html ({sub['lga']})")

    print(f"🎉 Generated {len(MELBOURNE_SUBURBS)} targeted suburb landing pages successfully!")

if __name__ == "__main__":
    run_suburb_generation()
