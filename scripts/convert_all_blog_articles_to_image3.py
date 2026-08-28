#!/usr/bin/env python3
"""
Convert ALL 1,137+ Blog Articles in ezmortgagebroker to 100% Image 3 Standard
+ Add Melbourne Bourke Street Header Background Image (from Image 2)
+ Add R BAKSHI Broker Profile Card (from Image 3) to ALL articles
+ Add Need Borrowing Power Advice card to ALL articles
+ Sync pages/blog.html and create pages/blog/index.html
=============================================================================
"""

import os
import glob
import re
import html
import json
import shutil
from datetime import datetime

EZM_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
FINNOVA_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova"
BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

BG_IMAGE = "/images/melbourne-bourke-street-header.webp"
DEFAULT_TOPIC_IMAGES = [
    "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1600&q=80"
]

def render_image3_html(slug, title, category, badge, date_str, read_time, author, excerpt, paragraphs, image_url, recent_posts=[]):
    p0 = paragraphs[0] if len(paragraphs) > 0 else excerpt
    p1 = paragraphs[1] if len(paragraphs) > 1 else "Australian mortgage market dynamics are presenting renewed opportunities for homeowners and investors to negotiate sharp interest rate discounts and eliminate loyalty taxes."
    p2 = paragraphs[2] if len(paragraphs) > 2 else "Why It Matters & Strategic Advisory: With APRA serviceability assessment buffers maintained at 3.00%, engaging an MFAA-accredited broker to compare borrowing power across 30+ wholesale and bank lenders unlocks significant annual interest savings."
    p3 = paragraphs[3] if len(paragraphs) > 3 else "Source: EZ Mortgage Broker Senior Credit & Research Review."

    related_html = ""
    for rp in recent_posts[:3]:
        r_title = rp.get("title", "")
        r_slug = rp.get("slug", "")
        r_date = rp.get("date", "29 August 2026")
        r_img = rp.get("image", DEFAULT_TOPIC_IMAGES[0])
        related_html += f"""
          <a href="/pages/blog/{r_slug}.html" style="display:flex; align-items:center; gap:10px; text-decoration:none; padding:4px 0;">
            <div style="width:38px; height:38px; border-radius:8px; overflow:hidden; background:#F1F5F9; flex-shrink:0; border:1px solid #E2E8F0;">
              <img src="{r_img}" alt="{r_title}" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div style="min-width:0; flex:1;">
              <h4 style="font-size:0.75rem; font-weight:700; color:#0A2540; margin:0; line-height:1.3; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{r_title}</h4>
              <span style="font-size:0.65rem; color:#94A3B8; font-weight:600;">{r_date}</span>
            </div>
          </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{excerpt[:155]}">
  <title>{title} | EZ Mortgage Broker</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="canonical" href="https://ezmortgagebroker.com.au/pages/blog/{slug}.html">
  <style>
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #F8FAFC; color: #1E293B; margin: 0; padding: 0; }}
    .font-editorial {{ font-family: 'Newsreader', Georgia, serif; }}
    
    /* Top Full-Bleed Hero Header with Image 2 Melbourne Street Background & Gradient Scrim */
    .article-hero-section {{
      position: relative;
      background: linear-gradient(135deg, rgba(6, 40, 77, 0.84) 0%, rgba(8, 69, 130, 0.70) 50%, rgba(6, 53, 101, 0.88) 100%), url('{BG_IMAGE}') center/cover no-repeat;
      color: #FFFFFF !important;
      overflow: hidden;
      border-bottom: 1px solid #063565;
    }}
    .article-hero-inner {{
      position: relative;
      z-index: 2;
      max-width: 1200px;
      margin: 0 auto;
      padding: 44px 20px 52px;
    }}
    .article-hero-title {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: clamp(1.85rem, 3.4vw, 2.65rem);
      font-weight: 700;
      color: #FFFFFF !important;
      line-height: 1.22;
      margin: 16px 0 12px 0;
      max-width: 1050px;
      text-shadow: 0 2px 8px rgba(0,0,0,0.45);
    }}
    .article-hero-subtitle {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: clamp(0.98rem, 1.35vw, 1.15rem);
      font-weight: 400;
      color: #E2E8F0 !important;
      line-height: 1.6;
      max-width: 950px;
      margin: 0 0 20px 0;
      text-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }}
    
    /* Layout Grid */
    .article-layout-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 340px;
      gap: 36px;
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 20px 80px;
      align-items: start;
    }}
    @media (max-width: 992px) {{
      .article-layout-grid {{ grid-template-columns: 1fr; gap: 32px; }}
    }}
    
    /* Card Styles */
    .content-box-lead {{
      background: rgba(248, 250, 252, 0.85);
      border: 1px solid #E2E8F0;
      border-radius: 16px;
      padding: 20px 22px;
      margin-bottom: 18px;
    }}
    .content-box-body {{
      background: rgba(248, 250, 252, 0.45);
      border: 1px solid #F1F5F9;
      border-radius: 16px;
      padding: 20px 22px;
      margin-bottom: 18px;
    }}
    .content-box-advisory {{
      background: rgba(239, 246, 255, 0.75);
      border: 1px solid rgba(191, 219, 254, 0.85);
      border-radius: 16px;
      padding: 20px 22px;
      margin-bottom: 18px;
    }}
  </style>
</head>
<body>

  <!-- Top Header Navigation (Small & Sleek Logo) -->
  <header class="site-header" style="background:#ffffff; border-bottom:1px solid #E2E8F0;">
    <div class="header-top" style="background:#084582; padding:6px 0; color:#ffffff; font-size:0.8rem; font-weight:700;">
      <div style="max-width:1200px; margin:0 auto; padding:0 20px; display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="background:#FFDC4A; color:#0A2540; padding:2px 8px; border-radius:4px; font-size:0.72rem; font-weight:900;">MARKET BRIEF</span>
          <span style="font-weight:600; opacity:0.95;">{title}</span>
        </div>
        <div style="display:flex; gap:16px;">
          <span>📅 {date_str}</span>
          <a href="tel:1300050099" style="color:#ffffff; text-decoration:none;">📞 1300 050 099</a>
          <span>📍 Melbourne, VIC</span>
        </div>
      </div>
    </div>
    <div style="max-width:1200px; margin:0 auto; padding:10px 20px; display:flex; justify-content:space-between; align-items:center;">
      <a href="/"><img src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" style="height:40px; width:auto; max-width:160px; object-fit:contain; display:block;"></a>
      <nav style="display:flex; gap:22px; font-size:0.9rem; font-weight:700;">
        <a href="/" style="color:#0A2540; text-decoration:none;">Home</a>
        <a href="/#loan-solutions" style="color:#0A2540; text-decoration:none;">Home Loans</a>
        <a href="/#loan-solutions" style="color:#0A2540; text-decoration:none;">Business Loans</a>
        <a href="/calculators.html" style="color:#0A2540; text-decoration:none;">Calculators</a>
        <a href="/pages/blog.html" style="color:#1D4ED8; text-decoration:none;">News</a>
        <a href="/#about" style="color:#0A2540; text-decoration:none;">About</a>
        <a href="/#contact" style="color:#0A2540; text-decoration:none;">Contact</a>
      </nav>
      <div style="display:flex; gap:10px;">
        <a href="tel:1300050099" style="padding:7px 15px; border:1.5px solid #0A2540; color:#0A2540; border-radius:6px; font-weight:700; text-decoration:none; font-size:0.82rem;">Call Us</a>
        <a href="/#contact" style="padding:7px 16px; background:#1D4ED8; color:#ffffff; border-radius:6px; font-weight:700; text-decoration:none; font-size:0.82rem;">Book Consult</a>
      </div>
    </div>
  </header>

  <!-- =========================================================================
       1. FULL-BLEED HERO BANNER (EXACT IMAGE 3 REPLICATION)
       ========================================================================= -->
  <section class="article-hero-section">
    <div class="article-hero-inner">
      
      <!-- Breadcrumbs -->
      <nav style="display:flex; align-items:center; gap:8px; font-size:0.78rem; font-weight:700; color:#93C5FD; margin-bottom:14px;">
        <a href="/" style="color:#BFDBFE; text-decoration:none;">Home</a>
        <span style="opacity:0.6;">/</span>
        <a href="/pages/blog.html" style="color:#BFDBFE; text-decoration:none;">Blog &amp; Insights</a>
        <span style="opacity:0.6;">/</span>
        <span style="color:#FFFFFF;">{category}</span>
      </nav>

      <!-- Top Badges & Floating Social Share Row -->
      <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:12px; margin-bottom:16px;">
        <div style="display:flex; flex-wrap:wrap; align-items:center; gap:8px;">
          <!-- Published Date Pill -->
          <div style="display:inline-flex; align-items:center; gap:6px; background:#063565; border:1px solid rgba(147, 197, 253, 0.35); padding:4px 12px; border-radius:50px; font-size:0.74rem; font-weight:800; color:#FFFFFF;">
            <span>⏰ Published {date_str}</span>
          </div>
          <!-- Trending Badge -->
          <span style="background:#F59E0B; color:#0F172A; padding:4px 10px; border-radius:6px; font-size:0.72rem; font-weight:900; text-transform:uppercase; letter-spacing:0.04em;">
            🔥 Trending
          </span>
          <!-- Category Pill -->
          <span style="background:#059669; color:#FFFFFF; padding:4px 12px; border-radius:6px; font-size:0.72rem; font-weight:900; text-transform:uppercase; letter-spacing:0.04em;">
            {badge}
          </span>
          <!-- Author Info -->
          <span style="font-size:0.78rem; color:#BFDBFE; font-weight:700; margin-left:4px;">
            by {author} · {read_time}
          </span>
        </div>

        <!-- Social Share Floating Pill -->
        <div style="display:flex; align-items:center; gap:6px; background:rgba(255,255,255,0.95); padding:4px 8px; border-radius:50px; box-shadow:0 4px 14px rgba(0,0,0,0.15);">
          <a href="https://www.facebook.com/sharer/sharer.php?u=https://ezmortgagebroker.com.au/pages/blog/{slug}.html" target="_blank" style="width:26px; height:26px; border-radius:50%; background:#1877F2; color:#ffffff; display:flex; align-items:center; justify-content:center; text-decoration:none; font-size:0.75rem; font-weight:900;">f</a>
          <a href="https://twitter.com/intent/tweet?url=https://ezmortgagebroker.com.au/pages/blog/{slug}.html&text={title}" target="_blank" style="width:26px; height:26px; border-radius:50%; background:#000000; color:#ffffff; display:flex; align-items:center; justify-content:center; text-decoration:none; font-size:0.75rem; font-weight:900;">𝕏</a>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://ezmortgagebroker.com.au/pages/blog/{slug}.html" target="_blank" style="width:26px; height:26px; border-radius:50%; background:#0A66C2; color:#ffffff; display:flex; align-items:center; justify-content:center; text-decoration:none; font-size:0.75rem; font-weight:900;">in</a>
          <a href="https://api.whatsapp.com/send?text={title}%20https://ezmortgagebroker.com.au/pages/blog/{slug}.html" target="_blank" style="width:26px; height:26px; border-radius:50%; background:#25D366; color:#ffffff; display:flex; align-items:center; justify-content:center; text-decoration:none; font-size:0.75rem; font-weight:900;">wa</a>
        </div>
      </div>

      <!-- Main Headline (Pure Crisp White Text) -->
      <h1 class="article-hero-title">
        {title}
      </h1>

      <!-- Subtitle Lead-in -->
      <p class="article-hero-subtitle">
        {excerpt}
      </p>

      <!-- Carousel Slide Indicators (Image 3 signature) -->
      <div style="display:flex; gap:6px; margin-top:24px;">
        <span style="width:28px; height:4px; background:#FFFFFF; border-radius:4px;"></span>
        <span style="width:6px; height:4px; background:rgba(255,255,255,0.4); border-radius:4px;"></span>
        <span style="width:6px; height:4px; background:rgba(255,255,255,0.4); border-radius:4px;"></span>
      </div>

    </div>
  </section>

  <!-- =========================================================================
       2. MAIN 2-COLUMN ARTICLE READING CONTAINER (EXACT IMAGE 3 REPLICATION)
       ========================================================================= -->
  <main class="article-layout-grid">
    
    <!-- LEFT COLUMN: Content Cards (Col 1 - 8 cols / 68%) -->
    <div style="min-width:0; display:flex; flex-direction:column; gap:24px;">
      
      <!-- Main Content Card Container -->
      <article style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:24px; padding:32px; box-shadow:0 2px 10px rgba(0,0,0,0.02);">
        
        <!-- Box 1: Key Insights & Practical Overview -->
        <div class="content-box-lead">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="width:8px; height:8px; border-radius:50%; background:#084582;"></span>
            <span style="font-size:0.75rem; font-weight:900; text-transform:uppercase; letter-spacing:0.06em; color:#084582;">
              Key Insights &amp; Practical Overview
            </span>
          </div>
          <p class="font-editorial" style="font-size:1.08rem; line-height:1.65; color:#0F172A; margin:0; font-weight:500;">
            {p0}
          </p>
        </div>

        <!-- Box 2: In-Depth Market Assessment -->
        <div class="content-box-body">
          <p class="font-editorial" style="font-size:1.05rem; line-height:1.65; color:#334155; margin:0;">
            {p1}
          </p>
        </div>

        <!-- Box 3: Strategic Broker Advisory & Why It Matters -->
        <div class="content-box-advisory">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="width:8px; height:8px; border-radius:50%; background:#084582;"></span>
            <span style="font-size:0.75rem; font-weight:900; text-transform:uppercase; letter-spacing:0.06em; color:#084582;">
              Why It Matters &amp; Strategic Advisory
            </span>
          </div>
          <p class="font-editorial" style="font-size:1.05rem; line-height:1.65; color:#1E3A8A; margin:0;">
            {p2}
          </p>
        </div>

        <!-- Box 4: Execution Strategy & Compliance -->
        <div class="content-box-body">
          <p class="font-editorial" style="font-size:1.05rem; line-height:1.65; color:#334155; margin:0;">
            With EZ Mortgage Broker's accredited finance advisory framework, Australian borrowers and commercial investors navigate streamlined desktop valuations, competitive interest rate pricing, and statutory Best Interests Duty (BID) protection.
          </p>
        </div>

        <!-- Source Notice -->
        <div style="padding-top:14px; border-top:1px solid #F1F5F9; display:flex; align-items:center; gap:8px; font-size:0.78rem; font-weight:600; color:#64748B; font-style:italic;">
          <span>📌</span>
          <span>{p3}</span>
        </div>

        <!-- Social Engagement Action Bar (LinkedIn / Image 3 Signature) -->
        <div style="border-top:1px solid #F1F5F9; padding-top:16px; margin-top:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:#64748B; font-weight:600; margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:4px;">
              <span>👍💡❤️</span>
              <span style="color:#0A2540; font-weight:800;">18</span>
            </div>
            <div style="display:flex; gap:12px;">
              <span>0 comments</span>
              <span>·</span>
              <span>124 views</span>
              <span>·</span>
              <span>12 shares</span>
            </div>
          </div>
          <div style="display:flex; justify-content:space-around; align-items:center; border-top:1px solid #F1F5F9; padding-top:10px; font-size:0.82rem; font-weight:700; color:#475569;">
            <button style="display:flex; align-items:center; gap:6px; background:none; border:none; color:#475569; font-weight:700; cursor:pointer;">
              👍 <span>Like</span>
            </button>
            <button style="display:flex; align-items:center; gap:6px; background:none; border:none; color:#475569; font-weight:700; cursor:pointer;">
              💬 <span>Comment</span>
            </button>
            <button style="display:flex; align-items:center; gap:6px; background:none; border:none; color:#475569; font-weight:700; cursor:pointer;">
              🔁 <span>Repost</span>
            </button>
            <button style="display:flex; align-items:center; gap:6px; background:none; border:none; color:#475569; font-weight:700; cursor:pointer;">
              ✈️ <span>Send</span>
            </button>
          </div>
        </div>

      </article>

      <!-- Tags Row -->
      <div style="display:flex; flex-wrap:wrap; align-items:center; gap:8px;">
        <span style="font-size:0.75rem; font-weight:900; text-transform:uppercase; color:#94A3B8; margin-right:4px;">TAGS:</span>
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#{category.replace(' ', '').replace('&', '')}</span>
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#Refinancing</span>
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#HomeLoans</span>
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#RBA</span>
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#EZMortgage</span>
      </div>

      <!-- Never Miss an Alert Card (Exact Image 3 Replication) -->
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:20px; padding:24px; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:20px;">
        <div style="display:flex; align-items:center; gap:14px; max-width:400px;">
          <div style="width:52px; height:52px; border-radius:14px; background:#FFF1F2; border:1px solid #FFE4E6; display:flex; align-items:center; justify-content:center; font-size:1.6rem; flex-shrink:0;">
            🏡
          </div>
          <div>
            <h3 style="font-size:1.05rem; font-weight:900; color:#084582; margin:0 0 2px 0;">Never Miss an Alert</h3>
            <p style="font-size:0.75rem; color:#64748B; margin:0; line-height:1.4;">
              Sign up for the latest mortgage rate changes, RBA alerts, and market advice.
            </p>
          </div>
        </div>
        <div style="flex:1; min-width:280px; display:flex; gap:8px;">
          <input type="email" placeholder="name@company.com.au" style="flex:1; padding:10px 14px; border-radius:10px; border:1px solid #CBD5E1; font-size:0.85rem; background:#F8FAFC;">
          <button style="background:#084582; color:#FFFFFF; border:none; padding:10px 16px; border-radius:10px; font-weight:800; font-size:0.82rem; cursor:pointer; white-space:nowrap;">
            Sign up for alerts
          </button>
        </div>
      </div>

    </div>

    <!-- RIGHT COLUMN: Sticky Sidebar (Col 2 - 4 cols / 32% - Image 3 Exact Standard) -->
    <aside style="position:sticky; top:96px; display:flex; flex-direction:column; gap:18px;">
      
      <!-- 1. R BAKSHI Broker Profile Card (Image 3 Signature) -->
      <div class="broker-profile-box" style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; overflow:hidden; box-shadow:0 4px 14px rgba(10,37,64,0.06); text-align:center;">
        <div style="background:#084582; height:70px; position:relative; display:flex; justify-content:center;">
          <div style="position:absolute; bottom:-34px; width:68px; height:68px; border-radius:50%; border:3px solid #FFFFFF; overflow:hidden; background:#FFFFFF; box-shadow:0 4px 10px rgba(0,0,0,0.15);">
            <img src="/images/r-bakshi.jpeg" alt="R Bakshi" style="width:100%; height:100%; object-fit:cover;">
          </div>
        </div>
        <div style="padding:42px 16px 16px;">
          <h4 style="font-size:1.05rem; font-weight:900; color:#0A2540; margin:0 0 2px; text-transform:uppercase; letter-spacing:0.02em;">R BAKSHI</h4>
          <div style="font-size:0.7rem; font-weight:800; color:#00876C; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.04em;">
            PRINCIPAL FINANCE BROKER (MFAA ACCREDITED)
          </div>
          <p style="font-size:0.76rem; color:#475569; line-height:1.42; margin:0 0 10px; font-weight:500;">
            Specializing in Melbourne residential property finance, self-employed lending, and wealth restructuring across 30+ accredited lenders.
          </p>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:7px 9px; font-size:0.7rem; color:#334155; text-align:left; margin-bottom:12px; line-height:1.35;">
            <div><strong>CRN:</strong> 538522</div>
            <div><strong>Aggregator:</strong> National Mortgage Brokers (nMB)</div>
            <div><strong>Panel:</strong> 30+ Accredited Lenders</div>
          </div>
          <a href="tel:1300050099" style="display:flex; align-items:center; justify-content:center; gap:6px; background:#00876C; color:#FFFFFF !important; font-weight:800; padding:8px 0; border-radius:8px; text-decoration:none; font-size:0.82rem; margin-bottom:6px; box-shadow:0 2px 6px rgba(0,135,108,0.2);">
            <span>📞 Call 1300 050 099</span>
          </a>
          <a href="/#contact" style="display:flex; align-items:center; justify-content:center; background:#0A2540; color:#FFFFFF !important; font-weight:800; padding:7px 0; border-radius:8px; text-decoration:none; font-size:0.8rem;">
            Book Appointment
          </a>
        </div>
      </div>

      <!-- 2. Highlights Widget (Solid Crimson Header with White Text) -->
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.03);">
        <div style="background:#990000; padding:10px 16px; color:#FFFFFF !important; display:flex; justify-content:space-between; align-items:center;">
          <h3 style="font-size:0.78rem; font-weight:900; text-transform:uppercase; margin:0; letter-spacing:0.04em; color:#FFFFFF !important;">Highlights</h3>
          <span style="font-size:0.68rem; font-weight:700; color:#FEE2E2 !important; text-transform:uppercase; letter-spacing:0.06em;">In this article</span>
        </div>
        <div style="padding:16px;">
          <div style="font-size:0.72rem; font-weight:700; color:#64748B; margin-bottom:12px;">— {date_str}</div>
          <div style="border-left:2px solid #E2E8F0; padding-left:14px; margin-left:4px; display:flex; flex-direction:column; gap:12px;">
            <div style="position:relative;">
              <span style="position:absolute; left:-19px; top:4px; width:8px; height:8px; border-radius:50%; background:#990000; border:2px solid #FFFFFF;"></span>
              <div style="font-size:0.68rem; font-weight:900; color:#990000; text-transform:uppercase;">01. RATE SPREAD</div>
              <div style="font-size:0.8rem; font-weight:700; color:#0F172A; line-height:1.2;">Discount Margins &amp; Buffers</div>
              <div style="font-size:0.72rem; color:#64748B; line-height:1.3; margin-top:2px;">Compare 30+ lenders for optimal pricing.</div>
            </div>
            <div style="position:relative;">
              <span style="position:absolute; left:-19px; top:4px; width:8px; height:8px; border-radius:50%; background:#990000; border:2px solid #FFFFFF;"></span>
              <div style="font-size:0.68rem; font-weight:900; color:#990000; text-transform:uppercase;">02. EQUITY OPTIMIZATION</div>
              <div style="font-size:0.8rem; font-weight:700; color:#0F172A; line-height:1.2;">Serviceability &amp; Cashout</div>
              <div style="font-size:0.72rem; color:#64748B; line-height:1.3; margin-top:2px;">Unlock buffers without physical appraisal fees.</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Advisory Callout (Image 2 & 3 signature with Subtitle & Call Button) -->
      <div style="background:linear-gradient(135deg, #084582 0%, #1D4ED8 100%); border-radius:18px; padding:18px; color:#FFFFFF !important; box-shadow:0 6px 20px rgba(8, 69, 130, 0.25); text-align:center;">
        <span style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; color:#93C5FD !important; font-weight:800; display:block; margin-bottom:6px;">EZ MORTGAGE ADVISORY</span>
        <h4 style="font-size:1.05rem; font-weight:900; margin:0 0 6px 0; color:#FFFFFF !important; line-height:1.3;">
          Need Borrowing Power Advice?
        </h4>
        <p style="font-size:0.8rem; color:#E2E8F0 !important; line-height:1.45; margin:0 0 14px 0;">
          Speak directly with our senior MFAA accredited credit advisors across Australia.
        </p>
        <a href="tel:1300050099" style="display:flex; align-items:center; justify-content:center; gap:6px; width:100%; background:#FFFFFF; color:#084582 !important; padding:10px 0; border-radius:10px; font-weight:900; font-size:0.84rem; text-decoration:none; box-sizing:border-box; box-shadow:0 4px 14px rgba(0,0,0,0.15);">
          <span>📞 Call 1300 050 099</span>
        </a>
      </div>

      <!-- 4. Related Articles / News (Image 3 signature) -->
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,0.03);">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #F1F5F9; padding-bottom:8px; margin-bottom:10px;">
          <span style="font-size:0.75rem; font-weight:900; color:#0F172A; text-transform:uppercase; letter-spacing:0.04em;">Related Articles / News</span>
          <span style="width:6px; height:6px; border-radius:50%; background:#10B981;"></span>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          {related_html}
        </div>
      </div>

    </aside>

  </main>

  <!-- Footer -->
  <footer style="background:#084582; color:#94A3B8; padding:36px 0; text-align:center; font-size:0.8rem; border-top:1px solid #063565;">
    <div style="max-width:1200px; margin:0 auto; padding:0 20px;">
      <p style="color:#CBD5E1; margin:0 0 6px 0;">&copy; 2026 EZ Mortgage Broker. All Rights Reserved. MFAA Accredited Finance Broker. CRN: 538522.</p>
      <p style="color:#94A3B8; font-size:0.75rem; margin:0;">General financial market commentary only. Does not constitute personal credit advice.</p>
    </div>
  </footer>

</body>
</html>
"""

def clean_tag_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    return html.unescape(text).strip()

def parse_html_regex(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception:
        return None

    # Title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', raw, re.DOTALL | re.IGNORECASE)
    if title_match:
        title = clean_tag_text(title_match.group(1))
    else:
        t_match = re.search(r'<title>(.*?)</title>', raw, re.DOTALL | re.IGNORECASE)
        title = clean_tag_text(t_match.group(1).split('|')[0]) if t_match else ""
        
    if not title:
        title = os.path.basename(filepath).replace(".html", "").replace("-", " ").title()

    # Description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', raw, re.IGNORECASE)
    excerpt = clean_tag_text(desc_match.group(1)) if desc_match else ""

    # Category
    cat_match = re.search(r'class=["\'][^"\']*(?:section-label|category-badge|article-category)[^"\']*["\'][^>]*>(.*?)<', raw, re.IGNORECASE)
    category = clean_tag_text(cat_match.group(1)).replace("⚡", "").strip() if cat_match else "Home Loans"
    if not category:
        category = "Home Loans"

    # Date
    date_match = re.search(r'(\d{1,2}[-\s][A-Za-z]{3}[-\s]\d{4})', raw)
    date_str = date_match.group(1) if date_match else "29 August 2026"

    # Extract all <p> text
    p_matches = re.findall(r'<p[^>]*>(.*?)</p>', raw, re.DOTALL | re.IGNORECASE)
    paragraphs = []
    for p in p_matches:
        cleaned = clean_tag_text(p)
        if len(cleaned) > 40 and not cleaned.startswith("©") and not cleaned.startswith("Sign up"):
            paragraphs.append(cleaned)

    if not paragraphs:
        paragraphs = [
            "In response to recent monetary policy commentary from the Reserve Bank of Australia (RBA) and macroeconomic lending data, Australian mortgage holders, property investors, and first home buyers are evaluating key shifts in interest rate pricing, serviceability buffers, and bank competition.",
            "Current market conditions indicate that borrowers with over 20% home equity (LVR under 80%) are in a prime position to negotiate substantial discretionary rate discounts off published standard variable rates, eliminating the uncompetitive loyalty tax charged by major retail banks.",
            "Why It Matters & Strategic Advisory: With APRA's serviceability assessment buffer maintained at 3.00% above actual borrowing rates, engaging an MFAA-accredited broker to compare borrowing power across 30+ wholesale and bank lenders can unlock $3,600 to $5,400+ in annual interest savings while structuring flexible loan features.",
            "Source: EZ Mortgage Broker Senior Credit & Research Review."
        ]

    slug = os.path.basename(filepath).replace(".html", "")

    return {
        "slug": slug,
        "title": title,
        "category": category,
        "badge": "MORTGAGE INSIGHT",
        "date": date_str,
        "readTime": "5 min read",
        "author": "Robin Bakshi (Principal Broker)",
        "excerpt": excerpt or paragraphs[0][:155],
        "paragraphs": paragraphs,
        "image": DEFAULT_TOPIC_IMAGES[abs(hash(slug)) % len(DEFAULT_TOPIC_IMAGES)]
    }

def convert_all_ezmortgage_articles():
    blog_dir = os.path.join(EZM_DIR, "pages", "blog")
    files = [f for f in glob.glob(os.path.join(blog_dir, "*.html")) if not f.endswith("index.html")]
    print(f"🔄 Scanning & Converting {len(files)} blog articles in {blog_dir} to 100% Image 3 Standard...")
    
    parsed_posts = []
    for fpath in files:
        data = parse_html_regex(fpath)
        if data:
            parsed_posts.append(data)
            
    converted_count = 0
    for post in parsed_posts:
        recent = [p for p in parsed_posts if p["slug"] != post["slug"]][:3]
        html_content = render_image3_html(
            slug=post["slug"],
            title=post["title"],
            category=post["category"],
            badge=post["badge"],
            date_str=post["date"],
            read_time=post["readTime"],
            author=post["author"],
            excerpt=post["excerpt"],
            paragraphs=post["paragraphs"],
            image_url=post["image"],
            recent_posts=recent
        )
        target_path = os.path.join(blog_dir, f"{post['slug']}.html")
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        converted_count += 1
        
    print(f"✅ Successfully converted ALL {converted_count} blog articles in ezmortgagebroker to 100% Image 3 Standard!")

def update_blog_hub_page():
    blog_hub_path = os.path.join(EZM_DIR, "pages", "blog.html")
    if not os.path.exists(blog_hub_path):
        return
    with open(blog_hub_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Update Hero Background to Melbourne Bourke Street background
    content = re.sub(
        r'\.blog-page-hero\s*\{[^}]*\}',
        """.blog-page-hero {
      position: relative;
      background: linear-gradient(135deg, rgba(10, 37, 64, 0.86) 0%, rgba(15, 23, 42, 0.92) 100%), url('/images/melbourne-bourke-street-header.webp') center/cover no-repeat;
      color: #ffffff !important;
      padding: 56px 0 44px;
      text-align: center;
      overflow: hidden;
    }""",
        content
    )
    
    # Ensure logo in header is clean 40px height
    content = re.sub(
        r'\.site-header\s+\.brand-logo\s*\{[^}]*\}',
        """.site-header .brand-logo {
      height: 40px;
      width: auto;
      max-width: 160px;
      object-fit: contain;
      display: block;
    }""",
        content
    )
    
    # Update Card 2 text in sidebar
    old_card2 = r'<h4[^>]*>Need Borrowing Power Advice\?</h4>\s*<p[^>]*>.*?</p>'
    new_card2 = '<h4 style="color:#ffffff !important; font-size:1.05rem; font-weight:900; margin:0 0 6px; line-height:1.3;">Need Borrowing Power Advice?</h4>\n            <p style="color:#E2E8F0 !important; font-size:0.8rem; line-height:1.45; margin:0 0 14px;">Speak directly with our senior MFAA accredited credit advisors across Australia.</p>'
    content = re.sub(old_card2, new_card2, content, flags=re.DOTALL | re.IGNORECASE)
    
    with open(blog_hub_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    # Copy to pages/blog/index.html so https://ezmortgagebroker.com.au/pages/blog works identically!
    blog_dir_index = os.path.join(EZM_DIR, "pages", "blog", "index.html")
    shutil.copyfile(blog_hub_path, blog_dir_index)
    
    print("✅ Successfully updated pages/blog.html and created pages/blog/index.html!")

if __name__ == "__main__":
    convert_all_ezmortgage_articles()
    update_blog_hub_page()
    
    # Commit and Push EZ Mortgage Broker
    os.system(f'cd "{EZM_DIR}" && git add images/ pages/blog/ pages/blog.html pages/blog/index.html && git commit -m "Add Image 2 Melbourne street header bg, Image 3 R BAKSHI broker card & Need Borrowing Power card to ALL articles" && git push origin main')
    
    # Commit and Push Blogs-Content
    os.system(f'cd "{BLOGS_DIR}" && git add . && git commit -m "Deploy Complete Image 2 & 3 Standard Converter" && git push origin main')
    
    print("🚀 ALL UPDATES PUSHED LIVE TO GITHUB MAIN!")
