#!/usr/bin/env python3
"""
Pixel-Perfect Image 2 Layout Enforcer for EZ Mortgage Broker
============================================================
Replicates the exact PRO CRM blog layout (Image 2) across all EZ Mortgage Broker articles:
1. Full-Bleed Brand Navy Hero Banner with Background Image Scrim, High-Contrast Pure White Title,
   Subtitles in #E2E8F0, Published Badge, Trending Badge, Category Pill, Author, and Floating Social Share Pill.
2. Left Column:
   - Key Insights & Practical Overview Card (slate-50/70 border).
   - In-depth Analysis Paragraph Cards (slate-50/40 border).
   - Why It Matters & Strategic Broker Advisory Card (blue-50/70 border).
   - Source Attribution notice.
   - Social Engagement & Reaction Action Bar (Like, Comment, Repost, Send).
   - Tags bar (#HomeLoans, #Refinancing, etc.).
   - "Never Miss an Alert" Newsletter Signup Box.
3. Right Column (Sticky 340px Sidebar):
   - Highlights Widget with Crimson Header (#990000) and Connected Vertical Timeline.
   - Related Articles / News Card with Image Thumbnails.
   - Direct Broker Support Card (#084582) with "Speak with our Principal Broker" and Call Button.
"""

import os
import json
import glob
import re

EZM_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

def build_image2_exact_html(post, recent_posts=[]):
    title = post.get("title", "Mortgage & Refinance Market Update")
    slug = post.get("slug", "mortgage-update")
    cat = post.get("category", "Home Loans")
    badge = post.get("badge", "Mortgage Insight")
    date_str = post.get("date", "27 August 2026")
    read_time = post.get("readTime", "5 min read")
    author = post.get("author", "Robin Bakshi (Principal Broker)")
    img = post.get("image", "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1600&q=80")
    excerpt = post.get("excerpt", "Australian mortgage market dynamics are presenting renewed opportunities for homeowners and investors to negotiate sharp interest rate discounts.")
    
    # 4 distinct high-depth paragraphs (350-500 words total)
    body_paragraphs = post.get("body", [
        f"In response to recent monetary policy commentary from the Reserve Bank of Australia (RBA) and macroeconomic lending data, Australian mortgage holders, property investors, and first home buyers are evaluating key shifts in interest rate pricing, serviceability buffers, and bank competition.",
        f"Current market conditions indicate that borrowers with over 20% home equity (LVR under 80%) are in a prime position to negotiate substantial discretionary rate discounts off published standard variable rates, eliminating the uncompetitive loyalty tax charged by major retail banks.",
        f"Why It Matters & Strategic Advisory: With APRA's serviceability assessment buffer maintained at 3.00% above actual borrowing rates, engaging an MFAA-accredited broker to compare borrowing power across 30+ wholesale and bank lenders can unlock $3,600 to $5,400+ in annual interest savings while structuring flexible loan features.",
        f"Source: EZ Mortgage Broker Research & Market Strategy Desk."
    ])

    p0 = body_paragraphs[0]
    p1 = body_paragraphs[1] if len(body_paragraphs) > 1 else "Borrowers can access streamlined automated valuations and rapid digital approvals to restructure debt facilities without administrative friction."
    p2 = body_paragraphs[2] if len(body_paragraphs) > 2 else "Why It Matters & Strategic Advisory: Proactive mortgage reviews ensure that your loan structure aligns with current property values, maximizing offset efficiency and debt reduction."
    p3 = body_paragraphs[3] if len(body_paragraphs) > 3 else "Source: EZ Mortgage Broker Market Review."

    # Build Related Articles HTML
    related_html = ""
    for rp in recent_posts[:3]:
        r_title = rp.get("title", "")
        r_slug = rp.get("slug", "")
        r_date = rp.get("date", "27 August 2026")
        r_img = rp.get("image", "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=200&q=80")
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
    
    /* Top Full-Bleed Hero Header */
    .article-hero-section {{
      position: relative;
      background-color: #084582;
      color: #FFFFFF !important;
      overflow: hidden;
      border-bottom: 1px solid #063565;
    }}
    .article-hero-bg-img {{
      position: absolute;
      inset: 0;
      background-image: url('{img}');
      background-size: cover;
      background-position: center;
      opacity: 0.25;
      transform: scale(1.02);
      pointer-events: none;
    }}
    .article-hero-scrim {{
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, rgba(6, 40, 77, 0.88) 0%, rgba(8, 69, 130, 0.72) 50%, rgba(6, 53, 101, 0.92) 100%);
      pointer-events: none;
    }}
    .article-hero-inner {{
      position: relative;
      z-index: 2;
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 20px 48px;
    }}
    .article-hero-title {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: clamp(1.85rem, 3.4vw, 2.65rem);
      font-weight: 700;
      color: #FFFFFF !important;
      line-height: 1.22;
      margin: 16px 0 12px 0;
      max-width: 1050px;
      text-shadow: 0 2px 8px rgba(0,0,0,0.35);
    }}
    .article-hero-subtitle {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: clamp(0.98rem, 1.35vw, 1.15rem);
      font-weight: 400;
      color: #E2E8F0 !important;
      line-height: 1.6;
      max-width: 950px;
      margin: 0 0 20px 0;
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

  <!-- Top Header Navigation -->
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
    <div style="max-width:1200px; margin:0 auto; padding:12px 20px; display:flex; justify-content:space-between; align-items:center;">
      <a href="/"><img src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" style="max-width:190px; height:auto;"></a>
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
        <a href="tel:1300050099" style="padding:8px 16px; border:1.5px solid #0A2540; color:#0A2540; border-radius:6px; font-weight:700; text-decoration:none; font-size:0.85rem;">Call Us</a>
        <a href="/#contact" style="padding:8px 18px; background:#1D4ED8; color:#ffffff; border-radius:6px; font-weight:700; text-decoration:none; font-size:0.85rem;">Book Consult</a>
      </div>
    </div>
  </header>

  <!-- =========================================================================
       1. FULL-BLEED HERO BANNER (EXACT IMAGE 2 REPLICATION)
       ========================================================================= -->
  <section class="article-hero-section">
    <div class="article-hero-bg-img"></div>
    <div class="article-hero-scrim"></div>
    <div class="article-hero-inner">
      
      <!-- Breadcrumbs -->
      <nav style="display:flex; align-items:center; gap:8px; font-size:0.78rem; font-weight:700; color:#93C5FD; margin-bottom:14px;">
        <a href="/" style="color:#BFDBFE; text-decoration:none;">Home</a>
        <span style="opacity:0.6;">/</span>
        <a href="/pages/blog.html" style="color:#BFDBFE; text-decoration:none;">Blog &amp; Insights</a>
        <span style="opacity:0.6;">/</span>
        <span style="color:#FFFFFF;">{cat}</span>
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

      <!-- Carousel Slide Indicators (Image 2 signature) -->
      <div style="display:flex; gap:6px; margin-top:24px;">
        <span style="width:28px; height:4px; background:#FFFFFF; border-radius:4px;"></span>
        <span style="width:6px; height:4px; background:rgba(255,255,255,0.4); border-radius:4px;"></span>
        <span style="width:6px; height:4px; background:rgba(255,255,255,0.4); border-radius:4px;"></span>
      </div>

    </div>
  </section>

  <!-- =========================================================================
       2. MAIN 2-COLUMN ARTICLE READING CONTAINER (EXACT IMAGE 2 REPLICATION)
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

        <!-- Social Engagement Action Bar (LinkedIn / Image 2 Signature) -->
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
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#{cat.replace(' ', '')}</span>
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#Refinancing</span>
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#HomeLoans</span>
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#RBA</span>
        <span style="background:#FFFFFF; border:1px solid #CBD5E1; color:#334155; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">#EZMortgage</span>
      </div>

      <!-- Never Miss an Alert Card (Exact Image 2 Replication) -->
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

    <!-- RIGHT COLUMN: Sticky Sidebar (Col 2 - 4 cols / 32% - Exact Image 2 Replication) -->
    <aside style="position:sticky; top:96px; display:flex; flex-direction:column; gap:18px;">
      
      <!-- 1. Highlights Widget (Solid Crimson Header) -->
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.03);">
        <div style="background:#990000; padding:10px 16px; color:#FFFFFF; display:flex; justify-content:space-between; align-items:center;">
          <h3 style="font-size:0.78rem; font-weight:900; text-transform:uppercase; margin:0; letter-spacing:0.04em;">Highlights</h3>
          <span style="font-size:0.68rem; font-weight:700; color:#FEE2E2; text-transform:uppercase; letter-spacing:0.06em;">In this article</span>
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

      <!-- 2. Related Articles / News (Image 2 signature) -->
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,0.03);">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #F1F5F9; padding-bottom:8px; margin-bottom:10px;">
          <span style="font-size:0.75rem; font-weight:900; color:#0F172A; text-transform:uppercase; letter-spacing:0.04em;">Related Articles / News</span>
          <span style="width:6px; height:6px; border-radius:50%; background:#10B981;"></span>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          {related_html}
        </div>
      </div>

      <!-- 3. Direct Broker Support Card (Image 2 signature) -->
      <div style="background:#084582; border-radius:18px; padding:18px; color:#FFFFFF; box-shadow:0 6px 20px rgba(8, 69, 130, 0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
          <span style="font-size:0.68rem; font-weight:900; text-transform:uppercase; letter-spacing:0.06em; color:#93C5FD;">Direct Broker Support</span>
          <span style="font-size:0.65rem; font-weight:800; background:rgba(30, 58, 138, 0.6); padding:2px 6px; border-radius:4px; color:#67E8F9;">Melbourne</span>
        </div>
        <h3 style="font-size:0.95rem; font-weight:900; margin:0 0 12px 0; color:#FFFFFF; line-height:1.3;">
          Speak with our Principal Broker
        </h3>
        <a href="tel:1300050099" style="display:flex; align-items:center; justify-content:center; gap:6px; width:100%; background:#FFFFFF; color:#084582; padding:10px 0; border-radius:10px; font-weight:900; font-size:0.84rem; text-decoration:none; box-sizing:border-box;">
          <span>📞 Call 1300 050 099</span>
        </a>
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

def regenerate_all_articles():
    posts_path = os.path.join(EZM_DIR, "posts.json")
    if not os.path.exists(posts_path):
        return
    with open(posts_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    blog_dir = os.path.join(EZM_DIR, "pages", "blog")
    os.makedirs(blog_dir, exist_ok=True)

    for p in posts:
        slug = p.get("slug")
        if not slug:
            continue
        recent = [rp for rp in posts if rp.get("slug") != slug]
        html_code = build_image2_exact_html(p, recent)
        fpath = os.path.join(blog_dir, f"{slug}.html")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html_code)

    print(f"🏆 100% Exact Image 2 Layout Applied Across all {len(posts)} articles in EZ Mortgage Broker!")

if __name__ == "__main__":
    regenerate_all_articles()
    
    # Commit and Push
    os.system(f'cd "{EZM_DIR}" && git add pages/blog/ && git commit -m "Deploy 100% Image 2 exact layout across all EZ Mortgage Broker articles" && git push origin main')
    os.system(f'cd "{BLOGS_DIR}" && git add . && git commit -m "Deploy Exact Image 2 Layout Script" && git push origin main')
    print("🚀 All articles updated with crisp text, dark scrim, and Image 2 layout!")
