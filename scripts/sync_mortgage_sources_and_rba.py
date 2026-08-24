#!/usr/bin/env python3
"""
Sync Mortgage Sources, Update Markdown Registry Docs, and Inject RBA Live Economic Indicator Widget
"""

import os
import json
import re

EZ_MORTGAGE_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
EZ_CONSULTANTS_DIR = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au"
FINNOVA_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova"
BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

MORTGAGE_AUTHORITY_SOURCES = """### C. Australian Property Finance & Mortgage Ingestion Sources (`ezmortgagebroker.com.au`)
1. `https://www.rba.gov.au/` (Reserve Bank of Australia — Cash Rate Decisions & Economic Indicators)
2. `https://www.afr.com/companies/financial-services` (Australian Financial Review — Financial Services & Banking)
3. `https://www.savings.com.au/news/` (Savings.com.au — Home Loans & Rate Movements)
4. `https://www.canstar.com.au/media/` (Canstar Media — Mortgage Market Releases & Product Comparisons)
5. `https://www.cotality.com/au/insights` (Cotality — Real Estate & Property Market Insights)
6. `https://www.apra.gov.au/news-and-publications` (APRA — Macroprudential Lending Buffers & Bank Scrutiny)
7. `https://www.abc.net.au/news/lifestyle#anchor-102961872` (ABC News — Consumer Finance, Housing & Lifestyle)"""

# -----------------------------------------------------------------------------
# 1. Update INSTRUCTIONS.md
# -----------------------------------------------------------------------------
instructions_path = os.path.join(BLOGS_DIR, "INSTRUCTIONS.md")
with open(instructions_path, "r", encoding="utf-8") as f:
    instr_c = f.read()

if "https://www.afr.com/companies/financial-services" not in instr_c:
    instr_c += f"\n\n{MORTGAGE_AUTHORITY_SOURCES}\n"
    with open(instructions_path, "w", encoding="utf-8") as f:
        f.write(instr_c)

# -----------------------------------------------------------------------------
# 2. Update ALERTS.md
# -----------------------------------------------------------------------------
alerts_path = os.path.join(BLOGS_DIR, "ALERTS.md")
with open(alerts_path, "r", encoding="utf-8") as f:
    alerts_c = f.read()

if "https://www.savings.com.au/news/" not in alerts_c:
    # Update entry 06 in ALERTS.md
    old_row_6 = "| **06** | **RBA & Australian Property Finance** | `https://www.rba.gov.au/rss/rss-cb-media-releases.xml` | **6x Daily** (Every 4 Hours AEST) | • `ezmortgagebroker.com.au` | Cash rate decisions, First Home Guarantee (5% deposit), bank interest margins, refinancing. | [`.github/workflows/daily_rss_publisher.yml`](file:///Users/robinbakshi/Documents/GitHub/ezmortgagebroker/.github/workflows/daily_rss_publisher.yml) |"
    new_row_6 = """| **06** | **RBA & Property Finance Network** | • `https://www.rba.gov.au/`<br>• `https://www.afr.com/companies/financial-services`<br>• `https://www.savings.com.au/news/`<br>• `https://www.canstar.com.au/media/`<br>• `https://www.cotality.com/au/insights`<br>• `https://www.apra.gov.au/news-and-publications`<br>• `https://www.abc.net.au/news/lifestyle` | **6x Daily** (Every 4 Hours AEST) | • `ezmortgagebroker.com.au` | Cash rate target (4.35%), inflation (3.8%), APRA 3% serviceability buffer, 5% deposit First Home Guarantee, broker clawback reforms. | [`.github/workflows/daily_rss_publisher.yml`](file:///Users/robinbakshi/Documents/GitHub/ezmortgagebroker/.github/workflows/daily_rss_publisher.yml) |"""
    alerts_c = alerts_c.replace(old_row_6, new_row_6)
    with open(alerts_path, "w", encoding="utf-8") as f:
        f.write(alerts_c)

# -----------------------------------------------------------------------------
# 3. Create RBA Live Indicator Component HTML & CSS
# -----------------------------------------------------------------------------
RBA_WIDGET_HTML = """
<!-- RBA Live Key Indicators Widget (Image 1 Exact Format) -->
<div class="rba-widget-container" style="margin: 24px 0 32px 0;">
  <div style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #0A2540; margin-bottom: 12px; display: flex; items-center; justify-content: space-between;">
    <span>🏛️ Official Reserve Bank of Australia (RBA) Key Indicators</span>
    <span style="font-size: 0.72rem; color: #00897B; font-weight: 700; background: #E0F2F1; padding: 2px 8px; border-radius: 6px;">Live Monetary Data</span>
  </div>
  
  <div class="rba-cards-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px;">
    
    <!-- Card 1: Cash Rate Target -->
    <div class="rba-card" style="background: #ffffff; border: 1px solid #E2E8F0; border-top: 4px solid #00897B; border-radius: 10px; padding: 18px; box-shadow: 0 4px 14px rgba(10,37,64,0.04); display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="font-size: 1.15rem; font-weight: 800; color: #0A2540; text-decoration: underline; text-decoration-color: #26C6DA; text-underline-offset: 6px;">
          Cash rate target
        </div>
        <div style="font-size: 2.8rem; font-weight: 900; color: #0A2540; letter-spacing: -0.03em; margin: 12px 0 6px 0; line-height: 1;">
          4.35<span style="font-size: 1.6rem; vertical-align: super; font-weight: 800;">%</span>
        </div>
      </div>
      <div style="font-size: 0.75rem; color: #475569; border-top: 1px solid #F1F5F9; padding-top: 10px; margin-top: 10px; line-height: 1.45;">
        <div>Effective date 12 August 2026</div>
        <div>Next update 2.30 pm, 29 September 2026</div>
      </div>
    </div>

    <!-- Card 2: Inflation -->
    <div class="rba-card" style="background: #ffffff; border: 1px solid #E2E8F0; border-top: 4px solid #00897B; border-radius: 10px; padding: 18px; box-shadow: 0 4px 14px rgba(10,37,64,0.04); display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="font-size: 1.15rem; font-weight: 800; color: #0A2540; text-decoration: underline; text-decoration-color: #26C6DA; text-underline-offset: 6px;">
          Inflation
        </div>
        <div style="display: flex; align-items: baseline; gap: 8px; margin: 12px 0 6px 0;">
          <div style="font-size: 2.8rem; font-weight: 900; color: #0A2540; letter-spacing: -0.03em; line-height: 1;">
            3.8<span style="font-size: 1.6rem; vertical-align: super; font-weight: 800;">%</span>
          </div>
          <div style="font-size: 0.72rem; font-weight: 800; color: #0A2540; line-height: 1.25; text-transform: uppercase;">
            Consumer Price Index<br><span style="font-weight: 500; text-transform: none; color: #64748B; font-size: 0.7rem;">Annual change June month 2026</span>
          </div>
        </div>
      </div>
      <div style="font-size: 0.75rem; color: #475569; border-top: 1px solid #F1F5F9; padding-top: 10px; margin-top: 10px; line-height: 1.45;">
        <div>Next update 26 August 2026</div>
      </div>
    </div>

    <!-- Card 3: Exchange Rates -->
    <div class="rba-card" style="background: #ffffff; border: 1px solid #E2E8F0; border-top: 4px solid #00897B; border-radius: 10px; padding: 18px; box-shadow: 0 4px 14px rgba(10,37,64,0.04); display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="font-size: 1.15rem; font-weight: 800; color: #0A2540; text-decoration: underline; text-decoration-color: #26C6DA; text-underline-offset: 6px;">
          Exchange rates
        </div>
        <div style="margin: 10px 0 6px 0;">
          <div style="display: flex; justify-content: space-between; align-items: baseline; font-size: 0.75rem; font-weight: 800; color: #0A2540; margin-bottom: 6px;">
            <span>TRADE-WEIGHTED INDEX</span>
            <span style="font-size: 1.25rem; font-weight: 900;">66.1</span>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px 12px; font-size: 0.75rem; color: #334155; font-weight: 600;">
            <div>USD <span style="font-weight: 700;">0.7169</span></div>
            <div>JPY <span style="font-weight: 700;">113.92</span></div>
            <div>CNY <span style="font-weight: 700;">4.8200</span></div>
            <div>EUR <span style="font-weight: 700;">0.6137</span></div>
          </div>
        </div>
      </div>
      <div style="font-size: 0.75rem; color: #475569; border-top: 1px solid #F1F5F9; padding-top: 10px; margin-top: 10px; line-height: 1.45;">
        <div>As at 4.00 pm, 24 August 2026</div>
      </div>
    </div>

  </div>
</div>
"""

# -----------------------------------------------------------------------------
# 4. Inject RBA Widget into ezmortgagebroker/pages/blog.html
# -----------------------------------------------------------------------------
blog_html_path = os.path.join(EZ_MORTGAGE_DIR, "pages", "blog.html")
pub_blog_html_path = os.path.join(EZ_MORTGAGE_DIR, "public", "pages", "blog.html")

for path in [blog_html_path, pub_blog_html_path]:
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        html_c = f.read()
    
    if "Official Reserve Bank of Australia (RBA) Key Indicators" not in html_c:
        # Inject right on top of <main class="blog-main-feed">
        html_c = html_c.replace('<main class="blog-main-feed">', f'<main class="blog-main-feed">\n{RBA_WIDGET_HTML}\n')
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_c)
        print(f"✅ Injected RBA Live Economic Widget into {path}!")

# -----------------------------------------------------------------------------
# 5. Distribute Markdown Files to All Repositories
# -----------------------------------------------------------------------------
for target_dir in [PROCRM_DIR, EZ_CONSULTANTS_DIR, EZ_MORTGAGE_DIR, FINNOVA_DIR]:
    for doc in ["INSTRUCTIONS.md", "ALERTS.md", "RULE.md", "SCHEDULE.md"]:
        src = os.path.join(BLOGS_DIR, doc)
        dest = os.path.join(target_dir, doc)
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as sf:
                c = sf.read()
            with open(dest, "w", encoding="utf-8") as df:
                df.write(c)

print("✅ Distributed all updated markdown registries across all 5 repositories!")
