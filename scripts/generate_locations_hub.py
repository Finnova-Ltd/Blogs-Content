#!/usr/bin/env python3
"""
Generate /locations.html - The All Melbourne Suburbs Directory Hub
Allows frontend users to search, filter by LGA / Region, and click through to all 91 suburb landing pages.
"""

import os
import json
import html
from datetime import datetime

TARGET_REPO = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
LOCATIONS_HUB_PATH = os.path.join(TARGET_REPO, "locations.html")
PUB_LOCATIONS_HUB_PATH = os.path.join(TARGET_REPO, "public", "locations.html")

from generate_suburbs_and_pillars import MELBOURNE_SUBURBS, slugify

def generate_locations_hub_html():
    # Group suburbs by LGA
    lga_groups = {}
    for sub in MELBOURNE_SUBURBS:
        lga = sub["lga"]
        if lga not in lga_groups:
            lga_groups[lga] = []
        lga_groups[lga].append(sub)

    suburb_cards_html = ""
    for sub in sorted(MELBOURNE_SUBURBS, key=lambda x: x["suburb"]):
        s_name = sub["suburb"]
        p_code = sub["postcode"]
        lga = sub["lga"]
        region = sub["region"]
        slug = f"/pages/locations/mortgage-broker-{slugify(s_name)}.html"

        suburb_cards_html += f"""
        <div class="suburb-item-card" data-suburb="{s_name.lower()}" data-lga="{lga.lower()}" data-postcode="{p_code}" data-region="{region.lower()}">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
            <h3 style="margin:0; font-size:1.15rem; font-weight:800; color:#0A2540;">{html.escape(s_name)}</h3>
            <span style="background:#E2E8F0; color:#0A2540; font-size:0.75rem; font-weight:800; padding:2px 8px; border-radius:12px;">{p_code}</span>
          </div>
          <p style="margin:0 0 12px; font-size:0.85rem; color:#64748B;">📍 {html.escape(lga)} · {html.escape(region)}</p>
          <a href="{slug}" class="suburb-card-btn">
            View {html.escape(s_name)} Rates &amp; Brokers &rarr;
          </a>
        </div>\n"""

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <link rel="icon" type="image/webp" href="/images/ez-mortgage-broker.webp">
  <link rel="apple-touch-icon" href="/images/ez-mortgage-broker.webp">
  <meta name="theme-color" content="#0A2540">

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Explore mortgage broking services across all 91 Melbourne suburbs. Compare 30+ lenders for home loans, refinancing, and first home buyer grants in your local area.">
  <title>Melbourne Mortgage Broker Locations Directory (91 Suburbs) | EZ Mortgage Broker</title>
  <link rel="canonical" href="https://ezmortgagebroker.com.au/locations.html">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/calculators.css">

  <style>
    .container {{
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
    @media (max-width: 992px) {{
      .site-header .logo {{
        margin-left: 0 !important;
      }}
    }}
    .locations-hero {{
      background: linear-gradient(135deg, #0A2540 0%, #1E3A8A 100%);
      color: #ffffff;
      padding: 56px 0 44px;
      text-align: center;
      border-radius: 0 0 16px 16px;
    }}
    .search-filter-bar {{
      max-width: 720px;
      margin: 28px auto 0;
      position: relative;
    }}
    .search-suburb-input {{
      width: 100%;
      padding: 16px 24px;
      border-radius: 30px;
      border: 2px solid rgba(255,255,255,0.4);
      background: rgba(255,255,255,0.98);
      font-size: 1.05rem;
      color: #0A2540;
      box-shadow: 0 8px 30px rgba(0,0,0,0.2);
      box-sizing: border-box;
      outline: none;
    }}
    .suburbs-directory-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
      margin: 40px 0 60px;
    }}
    .suburb-item-card {{
      background: #ffffff;
      border: 1.5px solid #E2E8F0;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(10,37,64,0.03);
      transition: all 0.25s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .suburb-item-card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 10px 24px rgba(10,37,64,0.08);
      border-color: #00876C;
    }}
    .suburb-card-btn {{
      display: block;
      text-align: center;
      background: #F8FAFC;
      border: 1px solid #CBD5E1;
      color: #00876C;
      font-weight: 700;
      font-size: 0.85rem;
      padding: 10px;
      border-radius: 8px;
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    .suburb-item-card:hover .suburb-card-btn {{
      background: #00876C;
      color: #ffffff;
      border-color: #00876C;
    }}
  </style>
</head>
<body style="font-family:'Inter',sans-serif; background:#F8FAFC; color:#0A2540; margin:0;">

  <!-- Site Header -->
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

  <!-- Hero -->
  <section class="locations-hero">
    <div class="container">
      <span style="background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.4); padding:6px 16px; border-radius:20px; font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em;">
        📍 Melbourne Local Coverage Directory
      </span>
      <h1 style="font-size:clamp(2rem, 3.5vw, 2.8rem); font-weight:900; margin:16px 0 10px;">Melbourne Mortgage Broker Locations</h1>
      <p style="font-size:1.1rem; color:rgba(255,255,255,0.9); max-width:760px; margin:0 auto 24px; line-height:1.6;">
        Compare 30+ accredited Australian lenders for home loans, refinancing, and first home buyer grants across all 91 Melbourne suburbs.
      </p>

      <!-- Live Search Bar -->
      <div class="search-filter-bar">
        <input type="text" id="suburbSearchInput" class="search-suburb-input" placeholder="🔍 Search by suburb, postcode (e.g. 3029), or LGA...">
      </div>
    </div>
  </section>

  <!-- Main Directory Container -->
  <main class="container">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:36px; padding-bottom:12px; border-bottom:2px solid #E2E8F0;">
      <div>
        <h2 style="font-size:1.4rem; font-weight:800; color:#0A2540; margin:0 0 4px;">All Melbourne Suburb Service Areas</h2>
        <p style="margin:0; font-size:0.9rem; color:#64748B;">Showing <span id="suburbCount">91</span> local mortgage broker landing pages</p>
      </div>
      <div>
        <span style="font-size:0.85rem; font-weight:700; color:#00876C;">⚡ Free Brokerage · 30+ Lenders</span>
      </div>
    </div>

    <!-- Grid of All 91 Suburb Cards -->
    <div class="suburbs-directory-grid" id="suburbsGrid">
{suburb_cards_html}    </div>
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

  <script>
    // Live Search Filter
    const searchInput = document.getElementById('suburbSearchInput');
    const cards = document.querySelectorAll('.suburb-item-card');
    const countSpan = document.getElementById('suburbCount');

    searchInput.addEventListener('input', (e) => {{
      const query = e.target.value.toLowerCase().trim();
      let visible = 0;

      cards.forEach(card => {{
        const s = card.getAttribute('data-suburb');
        const l = card.getAttribute('data-lga');
        const p = card.getAttribute('data-postcode');
        const r = card.getAttribute('data-region');

        if (!query || s.includes(query) || l.includes(query) || p.includes(query) || r.includes(query)) {{
          card.style.display = 'flex';
          visible++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      if (countSpan) {{
        countSpan.textContent = visible;
      }}
    }});
  </script>

</body>
</html>"""

def main():
    print("🚀 Generating /locations.html Directory Hub...")
    html_content = generate_locations_hub_html()
    for p in [LOCATIONS_HUB_PATH, PUB_LOCATIONS_HUB_PATH]:
        with open(p, "w", encoding="utf-8") as f:
            f.write(html_content)
    print("✅ Successfully generated /locations.html in both root and public/!")

if __name__ == "__main__":
    main()
