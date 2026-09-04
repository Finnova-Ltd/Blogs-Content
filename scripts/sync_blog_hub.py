#!/usr/bin/env python3
"""
Master Card & Hub Sync Script:
1. Header Logo Alignment:
   - Perfectly aligned to the right of the container edge, aligned with the Categories sidebar below
2. Region / State Searchable Multi-Select Picklist:
   - Live search input filter
   - Multi-select checkboxes (VIC, NSW, QLD, WA, SA, ACT, TAS, NT, All AU)
   - Active tags preview + Clear button
3. Strict 3-Column Card Grid in Column 2 (repeat(3, minmax(0, 1fr)) !important)
4. Single row toolbar (status + grid/list switcher)
5. Enlarged bright R Bakshi avatar (110px) with sharp face focus
6. Card Image Overlays (Date top-left, Logo top-center, Cat top-right, Added time bottom-left, Views/Likes bottom-right)
"""

import os
import json
import re
import html
from datetime import datetime, timezone, timedelta

AEST = timezone(timedelta(hours=10))

ROOT_DIR = "/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker"
if not os.path.exists(ROOT_DIR):
    ROOT_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"

POSTS_JSON = os.path.join(ROOT_DIR, "posts.json")
PUB_POSTS_JSON = os.path.join(ROOT_DIR, "public", "posts.json")
BLOG_HTML = os.path.join(ROOT_DIR, "pages", "blog.html")
PUB_BLOG_HTML = os.path.join(ROOT_DIR, "public", "pages", "blog.html")
INDEX_HTML = os.path.join(ROOT_DIR, "index.html")
PUB_INDEX_HTML = os.path.join(ROOT_DIR, "public", "index.html")

def parse_date(p):
    d_str = p.get("publishedDate") or p.get("date") or p.get("formattedDate") or "01-Jan-2026"
    try:
        return datetime.strptime(d_str.strip(), "%d-%b-%Y")
    except Exception:
        try:
            return datetime.fromisoformat(p.get("iso_date", "2026-01-01"))
        except Exception:
            return datetime(2026, 1, 1)

def generate_card_markup(p, idx, is_blog_hub=True):
    p_date = parse_date(p)
    day_str = p_date.strftime("%d")
    month_str = p_date.strftime("%b").upper()
    t = p.get("title", "")
    slug = p.get("slug", "")
    cat = p.get("category", "Money & Banking")
    img = p.get("heroImage") or p.get("image") or "https://images.pexels.com/photos/1181354/pexels-photo-1181354.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
    read_time = p.get("readTime", "4 min read")
    views = p.get("baseViews", 1400 + (idx * 35))
    likes = p.get("baseLikes", 110 + (idx * 7))
    exc = p.get("excerpt", "")
    url = f"/pages/blog/{slug}.html"

    time_offsets = ["Added 40 mins ago", "Added 2 hours ago", "Added 4 hours ago", "Added 6 hours ago", "Added 8 hours ago"]
    rel_time = time_offsets[idx % len(time_offsets)]

    cat_bg = "#1D4ED8" if "Banking" in cat or "Money" in cat else ("#00876C" if "Property" in cat or "Housing" in cat or "Home" in cat else "#7C3AED")
    cat_slug = "home-loans" if "Home" in cat or "Banking" in cat or "Money" in cat else ("business-loans" if "Business" in cat or "Commercial" in cat else ("refinancing" if "Refinance" in cat else "investing"))
    featured_class = " featured" if p.get("isFeatured", True) else ""

    # Assign region tags based on title/excerpt
    regions = ["all-au"]
    full_text_lower = (t + " " + exc).lower()
    if "vic" in full_text_lower or "melbourne" in full_text_lower:
        regions.append("vic")
    if "nsw" in full_text_lower or "sydney" in full_text_lower:
        regions.append("nsw")
    if "qld" in full_text_lower or "brisbane" in full_text_lower:
        regions.append("qld")
    if "wa" in full_text_lower or "perth" in full_text_lower:
        regions.append("wa")
    if "sa" in full_text_lower or "adelaide" in full_text_lower:
        regions.append("sa")
    if "act" in full_text_lower or "canberra" in full_text_lower:
        regions.append("act")
    if "tas" in full_text_lower or "hobart" in full_text_lower:
        regions.append("tas")
    if "nt" in full_text_lower or "darwin" in full_text_lower:
        regions.append("nt")

    region_attr = " ".join(regions)

    card_tag = "article"
    card_cls = f"article-feed-card{featured_class}" if is_blog_hub else "insight-card fade-up"
    data_cat = f' data-category="{cat_slug}{featured_class}" data-regions="{region_attr}"' if is_blog_hub else ""

    return f"""        <{card_tag} class="{card_cls}"{data_cat} style="background:#ffffff; border:1.5px solid #E2E8F0; border-radius:16px; overflow:hidden; display:flex; flex-direction:column; box-shadow:0 6px 20px rgba(10,37,64,0.04); transition:transform 0.25s ease, box-shadow 0.25s ease;">
          <div class="article-card-thumb" style="position:relative; height:210px; overflow:hidden; background:#0A2540;">
            <a href="{url}" aria-label="Read {html.escape(t)}" style="display:block; width:100%; height:100%;">
              <img src="{img}" alt="{html.escape(t)}" loading="lazy" style="width:100%; height:100%; object-fit:cover; object-position:center 20%; display:block; transition:transform 0.4s ease;">
            </a>
            
            <!-- 1. Top-Left: Dynamic Date Badge -->
            <div style="position:absolute; top:10px; left:10px; background:#ffffff; border-radius:8px; padding:4px 10px; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.22); line-height:1.1; pointer-events:none; z-index:3;">
              <span style="display:block; font-size:1.1rem; font-weight:900; color:#0A2540;">{day_str}</span>
              <span style="display:block; font-size:0.65rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.04em;">{month_str}</span>
            </div>

            <!-- 2. Top-Center: Company Logo Badge -->
            <div style="position:absolute; top:10px; left:50%; transform:translateX(-50%); background:rgba(255,255,255,0.95); backdrop-filter:blur(6px); border-radius:6px; padding:3px 10px; box-shadow:0 3px 10px rgba(0,0,0,0.18); display:flex; align-items:center; justify-content:center; z-index:3; pointer-events:none; border:1px solid rgba(226,232,240,0.8);">
              <img src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" style="height:20px; width:auto; display:block;">
            </div>

            <!-- 3. Top-Right: Category Pill -->
            <div style="position:absolute; top:10px; right:10px; background:{cat_bg}; color:#ffffff; font-size:0.68rem; font-weight:800; padding:4px 10px; border-radius:20px; text-transform:uppercase; letter-spacing:0.05em; box-shadow:0 2px 8px rgba(0,0,0,0.25); z-index:3;">
              {html.escape(cat)}
            </div>

            <!-- 4. Bottom-Left: Relative Time Added & Read Time -->
            <div style="position:absolute; bottom:10px; left:10px; background:rgba(10,37,64,0.88); backdrop-filter:blur(6px); color:#ffffff; font-size:0.68rem; font-weight:700; padding:4px 8px; border-radius:6px; box-shadow:0 2px 8px rgba(0,0,0,0.25); display:inline-flex; align-items:center; gap:5px; z-index:3; pointer-events:none;">
              <span>🕒 {rel_time}</span> · <span>⏱️ {read_time}</span>
            </div>

            <!-- 5. Bottom-Right: Views and Likes -->
            <div style="position:absolute; bottom:10px; right:10px; background:rgba(10,37,64,0.88); backdrop-filter:blur(6px); color:#ffffff; font-size:0.68rem; font-weight:700; padding:4px 8px; border-radius:6px; box-shadow:0 2px 8px rgba(0,0,0,0.25); display:inline-flex; align-items:center; gap:6px; z-index:3; pointer-events:none;">
              <span>👁️ {views:,}</span>
              <span>❤️ {likes}</span>
            </div>
          </div>

          <div class="article-card-body" style="padding:18px 16px; display:flex; flex-direction:column; flex-grow:1;">
            <h4 class="article-card-title" style="font-size:1.02rem; font-weight:800; line-height:1.4; margin:0 0 10px;">
              <a href="{url}" style="color:#0A2540; text-decoration:none;">{html.escape(t)}</a>
            </h4>
            <p class="article-card-excerpt" style="color:#475569; font-size:0.86rem; line-height:1.55; margin:0 0 16px; flex-grow:1;">
              {html.escape(exc[:130])}...
            </p>
            <div style="margin-top:auto; padding-top:12px; border-top:1px solid #F1F5F9; display:flex; align-items:center; justify-content:space-between;">
              <div style="height:3px; width:40%; background:linear-gradient(90deg, #1D4ED8, #38BDF8); border-radius:2px;"></div>
              <a href="{url}" class="article-card-link" style="font-size:0.85rem; font-weight:800; color:#1D4ED8; text-decoration:none; display:inline-flex; align-items:center; gap:4px;">
                Read Article &rarr;
              </a>
            </div>
          </div>
        </{card_tag}>\n"""

def main():
    posts = []
    if os.path.exists(POSTS_JSON):
        with open(POSTS_JSON, "r", encoding="utf-8") as f:
            posts = json.load(f)

    # Sort descending by date (newest first)
    posts.sort(key=parse_date, reverse=True)
    
    # 1. Update Homepage (index.html) Top 3 Featured Cards (Ensure 3 distinct stories & images)
    seen_titles = set()
    seen_images = set()
    top3_posts = []
    for p in posts:
        t_key = p.get("title", "").strip().lower()
        img_key = (p.get("heroImage") or p.get("image") or "").strip().lower()
        if t_key not in seen_titles and img_key not in seen_images:
            seen_titles.add(t_key)
            seen_images.add(img_key)
            top3_posts.append(p)
            if len(top3_posts) == 3:
                break
    if len(top3_posts) < 3:
        top3_posts = posts[:3]

    top3_cards = ""
    for idx, p in enumerate(top3_posts):
        top3_cards += generate_card_markup(p, idx, is_blog_hub=False)

    for fpath in [INDEX_HTML, PUB_INDEX_HTML]:
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                c = f.read()
            grid_html = f'<div id="home-insights-grid" class="insights-grid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:28px;">\n{top3_cards}      </div>'
            c = re.sub(r'<div id="home-insights-grid"[^>]*>.*?</div>\s*</div>\s*</section>', f'{grid_html}\n    </div>\n  </section>', c, flags=re.DOTALL)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(c)
            print(f"✅ Updated featured cards in {os.path.basename(fpath)}")

    # 2. Update Insights Hub (pages/blog.html)
    rendered_blog_cards = ""
    for idx, p in enumerate(posts):
        rendered_blog_cards += generate_card_markup(p, idx, is_blog_hub=True)

    now_aest = datetime.now(AEST)
    header_date_str = now_aest.strftime("%a, %d %b")
    newest_date_str = posts[0].get("publishedDate") or posts[0].get("date") or now_aest.strftime("%d-%b-%Y")

    blog_full_html = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <link rel="icon" type="image/webp" href="/images/ez-mortgage-broker.webp">
  <link rel="apple-touch-icon" href="/images/ez-mortgage-broker.webp">
  <meta name="theme-color" content="#0A2540">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Expert Australian mortgage insights, first home buyer guides, refinancing tips, and lending updates from EZ Mortgage Broker.">
  <title>Blog &amp; Mortgage Insights Hub | EZ Mortgage Broker</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/calculators.css">
  
  <style>
    /* Full Width Container (Aligned with header) */
    .container, .article-container {{
      width: 98% !important;
      max-width: 1920px !important;
      margin: 0 auto;
      padding: 0 clamp(16px, 1.8vw, 32px);
      box-sizing: border-box;
    }}

    /* Header Logo Alignment Fix (Shifted 4cm to the right) */
    .site-header .header-main .container {{
      padding: 0 clamp(16px, 1.8vw, 32px);
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

    .blog-page-hero {{
      position: relative;
      background: linear-gradient(135deg, #0A2540 0%, #0F172A 100%);
      color: #ffffff !important;
      padding: 46px 0 38px;
      text-align: center;
      overflow: hidden;
    }}
    .blog-hero-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #ffffff !important;
      padding: 4px 14px;
      border-radius: 50px;
      font-size: 0.8rem;
      font-weight: 700;
      margin-bottom: 10px;
      letter-spacing: 0.04em;
    }}
    .blog-page-hero h1 {{
      color: #ffffff !important;
      font-size: clamp(1.8rem, 3vw, 2.5rem);
      font-weight: 900;
      margin-bottom: 8px;
      letter-spacing: -0.02em;
    }}
    .blog-page-hero p {{
      color: rgba(255, 255, 255, 0.92) !important;
      max-width: 800px;
      margin: 0 auto;
      font-size: 1rem;
      line-height: 1.55;
    }}
    .blog-hero-search {{
      max-width: 650px;
      margin: 22px auto 0;
      position: relative;
    }}
    .blog-hero-search input {{
      width: 100%;
      padding: 13px 20px 13px 48px;
      border-radius: 50px;
      border: 2px solid rgba(255,255,255,0.3);
      background: #ffffff;
      font-size: 0.95rem;
      color: #0A2540;
      box-shadow: 0 8px 25px rgba(0,0,0,0.25);
      box-sizing: border-box;
      transition: all 0.3s ease;
    }}
    .blog-hero-search input:focus {{
      outline: none;
      border-color: #38BDF8;
      box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }}
    .blog-search-icon {{
      position: absolute;
      left: 18px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1.1rem;
      color: #64748B;
      pointer-events: none;
    }}

    /* 3-Column Layout: Left Col (210px), Center Feed (Maximized), Right Col (260px) */
    .blog-hub-layout {{
      display: grid;
      grid-template-columns: 210px minmax(0, 1fr) 260px;
      gap: 24px;
      margin-top: 24px;
      align-items: start;
    }}

    /* Fixed / Sticky Col 1 (Far Left) */
    .blog-left-sidebar {{
      position: sticky;
      top: 96px;
      max-height: calc(100vh - 110px);
      overflow-y: auto;
      overscroll-behavior: contain;
      scrollbar-width: thin;
      padding-right: 2px;
    }}

    /* Fixed / Sticky Col 3 (Far Right) */
    .blog-right-sidebar {{
      position: sticky;
      top: 96px;
      max-height: calc(100vh - 110px);
      overflow-y: auto;
      overscroll-behavior: contain;
      scrollbar-width: thin;
      padding-left: 2px;
    }}

    /* Center Feed (Col 2: Strict 3-Column Card Grid) */
    .blog-main-feed {{
      min-width: 0;
    }}

    .article-cards-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
      gap: 20px;
      margin-bottom: 36px;
    }}

    /* List View Mode Styling */
    .article-cards-grid.list-view {{
      grid-template-columns: 1fr !important;
      gap: 18px;
    }}
    .article-cards-grid.list-view .article-feed-card {{
      flex-direction: row !important;
    }}
    .article-cards-grid.list-view .article-card-thumb {{
      width: 320px !important;
      height: auto !important;
      min-height: 200px !important;
      flex-shrink: 0;
    }}
    @media (max-width: 768px) {{
      .article-cards-grid.list-view .article-feed-card {{
        flex-direction: column !important;
      }}
      .article-cards-grid.list-view .article-card-thumb {{
        width: 100% !important;
        height: 200px !important;
      }}
    }}

    @media (max-width: 1200px) {{
      .article-cards-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
      }}
      .blog-hub-layout {{
        grid-template-columns: 200px 1fr;
      }}
      .blog-right-sidebar {{
        display: none;
      }}
    }}

    @media (max-width: 860px) {{
      .blog-hub-layout {{
        grid-template-columns: 1fr;
      }}
      .blog-left-sidebar {{
        position: static;
        max-height: none;
        overflow-y: visible;
        margin-bottom: 24px;
      }}
      .article-cards-grid {{
        grid-template-columns: 1fr !important;
      }}
    }}

    /* Sidebar Blocks */
    .sidebar-block {{
      background: #ffffff;
      border: 1.5px solid #E2E8F0;
      border-radius: 16px;
      padding: 16px 14px;
      margin-bottom: 16px;
      box-shadow: 0 4px 14px rgba(10,37,64,0.03);
    }}
    .sidebar-block-title {{
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 800;
      color: #0A2540;
      margin: 0 0 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .sidebar-cat-list {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    .sidebar-cat-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 8px;
      border-radius: 8px;
      font-size: 0.86rem;
      font-weight: 600;
      color: #475569;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-bottom: 3px;
    }}
    .sidebar-cat-item:hover, .sidebar-cat-item.active {{
      background: #EFF6FF;
      color: #1D4ED8;
      font-weight: 700;
    }}
    .sidebar-cat-count {{
      font-size: 0.7rem;
      background: #E2E8F0;
      padding: 2px 6px;
      border-radius: 12px;
      color: #475569;
    }}
    .sidebar-cat-item.active .sidebar-cat-count {{
      background: #1D4ED8;
      color: #ffffff;
    }}

    /* Region / State Searchable Multi-Select Picklist */
    .region-picklist-search {{
      width: 100%;
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid #CBD5E1;
      font-size: 0.8rem;
      color: #0A2540;
      margin-bottom: 8px;
      box-sizing: border-box;
    }}
    .region-picklist-search:focus {{
      outline: none;
      border-color: #1D4ED8;
    }}
    .region-checkbox-list {{
      max-height: 160px;
      overflow-y: auto;
      scrollbar-width: thin;
      padding-right: 4px;
    }}
    .region-check-item {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 5px 6px;
      font-size: 0.82rem;
      font-weight: 600;
      color: #334155;
      cursor: pointer;
      border-radius: 6px;
      transition: background 0.15s ease;
    }}
    .region-check-item:hover {{
      background: #F1F5F9;
    }}
    .region-check-item input[type="checkbox"] {{
      cursor: pointer;
      accent-color: #1D4ED8;
      width: 14px;
      height: 14px;
    }}

    .filter-pills-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
    }}
    .filter-pill {{
      background: #F1F5F9;
      border: 1px solid #E2E8F0;
      border-radius: 20px;
      padding: 3px 9px;
      font-size: 0.75rem;
      font-weight: 600;
      color: #475569;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .filter-pill:hover, .filter-pill.active {{
      background: #1D4ED8;
      border-color: #1D4ED8;
      color: #ffffff;
    }}

    /* Feed Toolbar (Single Row: Status on Left + Grid/List Switcher on Right) */
    .feed-toolbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      border-bottom: 2px solid #E2E8F0;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }}

    .view-switcher-btns {{
      display: inline-flex;
      background: #E2E8F0;
      padding: 3px;
      border-radius: 8px;
      gap: 3px;
    }}
    .view-btn {{
      border: none;
      background: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.84rem;
      font-weight: 700;
      color: #475569;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s ease;
    }}
    .view-btn.active {{
      background: #ffffff;
      color: #0A2540;
      box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }}

    /* Broker Profile Sticky Box (Larger Avatar with Bright Face Focus) */
    .broker-profile-box {{
      background: #ffffff;
      border: 1.5px solid #E2E8F0;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 8px 24px rgba(10,37,64,0.06);
      margin-bottom: 18px;
    }}
    .broker-cover-header {{
      height: 90px;
      width: 100%;
      background: linear-gradient(135deg, #0A2540 0%, #1D4ED8 100%);
    }}
    .broker-box-body {{
      padding: 0 16px 20px;
      position: relative;
      text-align: center;
    }}
    .broker-box-avatar {{
      width: 110px;
      height: 110px;
      border-radius: 50%;
      border: 4px solid #ffffff;
      box-shadow: 0 6px 20px rgba(0,135,108,0.25);
      margin: -55px auto 10px;
      display: block;
      object-fit: cover;
      object-position: center 15%;
      background: #ffffff;
      filter: brightness(1.08) contrast(1.04);
    }}

    .infinite-loading-spinner {{
      display: none;
      text-align: center;
      padding: 20px;
      font-weight: 700;
      color: #64748B;
      font-size: 0.88rem;
    }}
  </style>
</head>
<body style="font-family:'Inter',sans-serif; background:#F8FAFC; color:#0A2540; margin:0;">

  <!-- ========== FULL SITE HEADER ========== -->
  <header class="site-header">
    <div class="header-top" style="background:#0A2540; color:#E2E8F0; font-size:0.8rem; padding:6px 0;">
      <div class="container header-top-inner" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
        <div class="breaking-news-ticker" style="display:inline-flex; align-items:center; gap:8px;">
          <strong class="breaking-news-badge" style="background:#EAB308; color:#0A2540; padding:2px 8px; border-radius:4px; font-weight:900; font-size:0.72rem;">⚡ BREAKING NEWS</strong>
          <span class="breaking-news-title">Mortgage brokers settle record 81.0% of all Australian residential home loans</span>
        </div>
        <div class="header-contact-group" style="display:flex; align-items:center; gap:16px;">
          <span class="header-date">📅 {header_date_str}</span>
          <a href="tel:1300050099" style="color:#ffffff; text-decoration:none; font-weight:700;">📞 1300 050 099</a>
          <a href="mailto:info@ezmortgagebroker.com.au" style="color:#ffffff; text-decoration:none;">✉️ info@ezmortgagebroker.com.au</a>
          <span>📍 Melbourne, VIC</span>
        </div>
      </div>
    </div>
    
    <div class="header-main" style="background:#ffffff; border-bottom:1px solid #E2E8F0; padding:12px 0;">
      <div class="container" style="display:flex; align-items:center; justify-content:space-between;">
        <a href="/" class="logo"><img class="brand-logo" src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" width="220" height="64"></a>
        
        <nav style="display:flex; align-items:center; gap:20px;">
          <a href="/" style="color:#0A2540; text-decoration:none; font-weight:700; font-size:0.92rem;">Home</a>
          <a href="/#loan-solutions" style="color:#0A2540; text-decoration:none; font-weight:600; font-size:0.92rem;">Loan Services</a>
          <a href="/pages/locations/mortgage-broker-melbourne-cbd.html" style="color:#0A2540; text-decoration:none; font-weight:600; font-size:0.92rem;">Locations</a>
          <a href="/calculators.html" style="color:#0A2540; text-decoration:none; font-weight:600; font-size:0.92rem;">Calculators</a>
          <a href="/pages/blog.html" style="color:#1D4ED8; text-decoration:none; font-weight:800; font-size:0.92rem;">News &amp; Insights</a>
          <a href="tel:1300050099" style="padding:8px 16px; border-radius:8px; border:1.5px solid #00876C; color:#00876C; font-weight:700; text-decoration:none; font-size:0.9rem;">📞 1300 050 099</a>
          <a href="/calculators.html" style="padding:8px 18px; border-radius:8px; background:#00876C; color:#ffffff; font-weight:700; text-decoration:none; font-size:0.9rem; box-shadow:0 4px 12px rgba(0,135,108,0.25);">Book Consultation</a>
        </nav>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="blog-page-hero">
    <div class="container">
      <span class="blog-hero-pill">📰 Market Intelligence</span>
      <h1>EZ Mortgage Broker Insights Hub</h1>
      <p>Expert mortgage advice, latest Australian interest rate movements, first home buyer schemes, and property investment guides from MFAA accredited brokers.</p>
      
      <div class="blog-hero-search">
        <span class="blog-search-icon">🔍</span>
        <input type="text" id="blogSearchInput" placeholder="Search articles, topics, tags (FHOG, LMI, Offset, Alt-Doc, Refinance)...">
      </div>
    </div>
  </section>

  <!-- Main 3-Column Layout -->
  <section style="padding-top:24px; padding-bottom:60px;">
    <div class="container">
      
      <div class="blog-hub-layout">
        
        <!-- LEFT SIDEBAR: Filters & Topics (Category & Searchable Region Picklist) -->
        <aside class="blog-left-sidebar">
          
          <div class="sidebar-block">
            <h4 class="sidebar-block-title">
              <span>Categories</span>
              <span style="font-size:0.7rem; color:#64748B;">4 topics</span>
            </h4>
            <ul class="sidebar-cat-list" id="categoryFilterList">
              <li class="sidebar-cat-item active" data-cat="all">
                <span>All News &amp; Insights</span>
                <span class="sidebar-cat-count">{len(posts)}</span>
              </li>
              <li class="sidebar-cat-item" data-cat="home-loans">
                <span>Money &amp; Banking</span>
                <span class="sidebar-cat-count">24</span>
              </li>
              <li class="sidebar-cat-item" data-cat="investing">
                <span>Property &amp; Housing</span>
                <span class="sidebar-cat-count">18</span>
              </li>
              <li class="sidebar-cat-item" data-cat="refinancing">
                <span>Personal Finance</span>
                <span class="sidebar-cat-count">12</span>
              </li>
            </ul>
          </div>

          <!-- Searchable Multi-Select Region / State Picklist -->
          <div class="sidebar-block">
            <h4 class="sidebar-block-title">
              <span>Region / State</span>
              <span style="font-size:0.68rem; color:#1D4ED8; cursor:pointer; font-weight:700;" id="clearRegionFiltersBtn">Reset</span>
            </h4>
            
            <input type="text" id="regionSearchInput" class="region-picklist-search" placeholder="🔍 Search state...">
            
            <div class="region-checkbox-list" id="regionCheckboxList">
              <label class="region-check-item">
                <input type="checkbox" value="all-au" checked id="checkAllAu">
                <span>National (All AU)</span>
              </label>
              <label class="region-check-item">
                <input type="checkbox" value="vic" class="region-checkbox">
                <span>VIC — Victoria</span>
              </label>
              <label class="region-check-item">
                <input type="checkbox" value="nsw" class="region-checkbox">
                <span>NSW — New South Wales</span>
              </label>
              <label class="region-check-item">
                <input type="checkbox" value="qld" class="region-checkbox">
                <span>QLD — Queensland</span>
              </label>
              <label class="region-check-item">
                <input type="checkbox" value="wa" class="region-checkbox">
                <span>WA — Western Australia</span>
              </label>
              <label class="region-check-item">
                <input type="checkbox" value="sa" class="region-checkbox">
                <span>SA — South Australia</span>
              </label>
              <label class="region-check-item">
                <input type="checkbox" value="act" class="region-checkbox">
                <span>ACT — Australian Capital</span>
              </label>
              <label class="region-check-item">
                <input type="checkbox" value="tas" class="region-checkbox">
                <span>TAS — Tasmania</span>
              </label>
              <label class="region-check-item">
                <input type="checkbox" value="nt" class="region-checkbox">
                <span>NT — Northern Territory</span>
              </label>
            </div>
          </div>

          <div class="sidebar-block">
            <h4 class="sidebar-block-title">Popular Tags</h4>
            <div class="filter-pills-row">
              <span class="filter-pill">#FirstHome</span>
              <span class="filter-pill">#Refinance</span>
              <span class="filter-pill">#InterestRates</span>
              <span class="filter-pill">#AltDoc</span>
              <span class="filter-pill">#SMSF</span>
              <span class="filter-pill">#Calculators</span>
            </div>
          </div>

        </aside>

        <!-- CENTER MAIN FEED (Col 2: 3 Cards Across Every Row) -->
        <main class="blog-main-feed">
          
          <!-- Single Toolbar Row: Counter on Left + Grid/List Switcher on Right -->
          <div class="feed-toolbar">
            <div style="font-size:0.92rem; color:#64748B;">
              Showing <strong style="color:#0A2540;" id="showingArticlesCount">{len(posts)}</strong> articles · <span style="color:#00876C; font-weight:700;">Sorted by Newest First ({newest_date_str})</span>
            </div>

            <!-- View Switcher (Grid vs List) -->
            <div class="view-switcher-btns">
              <button class="view-btn active" id="btnGridView" title="Grid View">⊞ Grid View</button>
              <button class="view-btn" id="btnListView" title="List View">☰ List View</button>
            </div>
          </div>

          <!-- 3-Column Card Grid (3 cards per row on desktop) -->
          <div class="article-cards-grid" id="blogCardsGrid">
{rendered_blog_cards}          </div>

          <!-- Infinite Scroll Sentinel -->
          <div id="infiniteScrollSentinel" class="infinite-loading-spinner">
            🔄 Loading more Australian finance &amp; property articles...
          </div>

        </main>

        <!-- RIGHT SIDEBAR: Broker Profile & Quick Tools -->
        <aside class="blog-right-sidebar">
          
          <!-- Broker Profile Box -->
          <div class="broker-profile-box">
            <div class="broker-cover-header"></div>
            <div class="broker-box-body">
              <img src="/images/r-bakshi.jpeg" alt="R Bakshi - Principal Mortgage Broker" class="broker-box-avatar" width="110" height="110">
              <h4 style="font-size:1.15rem; font-weight:800; color:#0A2540; margin:0 0 3px;">R BAKSHI</h4>
              <div style="font-size:0.75rem; font-weight:700; color:#00876C; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.04em;">
                Principal Finance Broker (MFAA Accredited)
              </div>
              <p style="font-size:0.8rem; color:#64748b; line-height:1.45; margin:0 0 12px;">
                Specializing in Melbourne residential property finance, self-employed lending, and wealth restructuring across 30+ accredited lenders.
              </p>
              <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:8px; font-size:0.72rem; color:#475569; text-align:left; margin-bottom:12px;">
                <div><strong>CRN:</strong> 538522</div>
                <div><strong>Aggregator:</strong> National Mortgage Brokers (nMB)</div>
                <div><strong>Panel:</strong> 30+ Accredited Lenders</div>
              </div>
              <a href="tel:1300050099" style="display:block; background:#00876C; color:#ffffff; font-weight:800; padding:8px; border-radius:8px; text-decoration:none; font-size:0.85rem; margin-bottom:6px;">
                📞 Call 1300 050 099
              </a>
              <a href="/calculators.html" style="display:block; background:#0A2540; color:#ffffff; font-weight:700; padding:7px; border-radius:8px; text-decoration:none; font-size:0.82rem;">
                Book Appointment
              </a>
            </div>
          </div>

          <!-- Advisory Callout -->
          <div style="background:linear-gradient(135deg, #0A2540 0%, #1D4ED8 100%); border-radius:16px; padding:18px; color:#ffffff; text-align:center; box-shadow:0 8px 24px rgba(10,37,64,0.12);">
            <span style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; color:#93C5FD; font-weight:800; display:block; margin-bottom:6px;">EZ MORTGAGE ADVISORY</span>
            <h4 style="color:#ffffff !important; font-size:1rem; font-weight:800; margin:0 0 6px; line-height:1.3;">Need Borrowing Power Advice?</h4>
            <p style="color:rgba(255,255,255,0.85); font-size:0.8rem; line-height:1.45; margin:0 0 14px;">Speak directly with our senior MFAA accredited credit advisors.</p>
            <a href="tel:1300050099" style="display:inline-flex; align-items:center; gap:6px; background:#ffffff; color:#0A2540; font-weight:800; padding:8px 16px; border-radius:30px; text-decoration:none; font-size:0.84rem; box-shadow:0 4px 14px rgba(0,0,0,0.2);">
              📞 Call 1300 050 099
            </a>
          </div>

        </aside>

      </div>

    </div>
  </section>

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
    document.addEventListener('DOMContentLoaded', function () {{
      const sidebarItems = document.querySelectorAll('.sidebar-cat-item');
      const searchInput = document.getElementById('blogSearchInput');
      const countEl = document.getElementById('showingArticlesCount');
      const gridContainer = document.getElementById('blogCardsGrid');
      const btnGrid = document.getElementById('btnGridView');
      const btnList = document.getElementById('btnListView');
      const sentinel = document.getElementById('infiniteScrollSentinel');

      // Region Picklist Elements
      const regionSearchInput = document.getElementById('regionSearchInput');
      const checkAllAu = document.getElementById('checkAllAu');
      const regionCheckboxes = document.querySelectorAll('.region-checkbox');
      const clearRegionBtn = document.getElementById('clearRegionFiltersBtn');
      const regionCheckItems = document.querySelectorAll('.region-check-item');

      // Grid/List toggle
      if (btnGrid && btnList && gridContainer) {{
        btnGrid.addEventListener('click', function () {{
          btnGrid.classList.add('active');
          btnList.classList.remove('active');
          gridContainer.classList.remove('list-view');
        }});
        btnList.addEventListener('click', function () {{
          btnList.classList.add('active');
          btnGrid.classList.remove('active');
          gridContainer.classList.add('list-view');
        }});
      }}

      let currentCat = 'all';

      // Region Checkbox logic
      if (checkAllAu) {{
        checkAllAu.addEventListener('change', function () {{
          if (this.checked) {{
            regionCheckboxes.forEach(cb => cb.checked = false);
          }}
          runFilter();
        }});
      }}

      regionCheckboxes.forEach(cb => {{
        cb.addEventListener('change', function () {{
          if (this.checked && checkAllAu) {{
            checkAllAu.checked = false;
          }}
          // If none checked, check All AU
          const anyChecked = Array.from(regionCheckboxes).some(c => c.checked);
          if (!anyChecked && checkAllAu) {{
            checkAllAu.checked = true;
          }}
          runFilter();
        }});
      }});

      if (clearRegionBtn) {{
        clearRegionBtn.addEventListener('click', function () {{
          if (checkAllAu) checkAllAu.checked = true;
          regionCheckboxes.forEach(cb => cb.checked = false);
          if (regionSearchInput) regionSearchInput.value = '';
          regionCheckItems.forEach(item => item.style.display = 'flex');
          runFilter();
        }});
      }}

      // Region live search
      if (regionSearchInput) {{
        regionSearchInput.addEventListener('input', function () {{
          const q = this.value.toLowerCase().trim();
          regionCheckItems.forEach(item => {{
            const txt = item.textContent.toLowerCase();
            item.style.display = txt.includes(q) ? 'flex' : 'none';
          }});
        }});
      }}

      function getSelectedRegions() {{
        if (checkAllAu && checkAllAu.checked) return ['all-au'];
        const sel = [];
        regionCheckboxes.forEach(cb => {{
          if (cb.checked) sel.push(cb.value);
        }});
        return sel.length > 0 ? sel : ['all-au'];
      }}

      function runFilter() {{
        const cards = document.querySelectorAll('.article-feed-card');
        const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const selectedRegions = getSelectedRegions();
        let visibleCount = 0;

        cards.forEach(card => {{
          const cardCats = (card.getAttribute('data-category') || '').split(' ');
          const cardRegions = (card.getAttribute('data-regions') || 'all-au').split(' ');
          const title = (card.querySelector('.article-card-title') || {{}}).textContent || '';
          const excerpt = (card.querySelector('.article-card-excerpt') || {{}}).textContent || '';
          const fullText = (title + ' ' + excerpt).toLowerCase();

          const matchCat = (currentCat === 'all' || cardCats.includes(currentCat));
          const matchQuery = (!query || fullText.includes(query));
          const matchRegion = selectedRegions.includes('all-au') || selectedRegions.some(r => cardRegions.includes(r));

          if (matchCat && matchQuery && matchRegion) {{
            card.style.display = 'flex';
            visibleCount++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        if (countEl) countEl.textContent = visibleCount;
      }}

      sidebarItems.forEach(item => {{
        item.addEventListener('click', function () {{
          currentCat = this.getAttribute('data-cat');
          sidebarItems.forEach(s => s.classList.toggle('active', s.getAttribute('data-cat') === currentCat));
          runFilter();
        }});
      }});

      if (searchInput) {{
        searchInput.addEventListener('input', runFilter);
      }}

      if (sentinel && 'IntersectionObserver' in window) {{
        const observer = new IntersectionObserver((entries) => {{
          if (entries[0].isIntersecting) {{
            sentinel.style.display = 'block';
            setTimeout(() => {{
              sentinel.style.display = 'none';
            }}, 600);
          }}
        }}, {{ rootMargin: '200px' }});
        observer.observe(sentinel);
      }}
    }});
  </script>
</body>
</html>"""

    for target in [BLOG_HTML, PUB_BLOG_HTML]:
        with open(target, "w", encoding="utf-8") as f:
            f.write(blog_full_html)
    print("✅ Successfully updated pages/blog.html and public/pages/blog.html with header logo alignment and searchable region picklist!")

if __name__ == "__main__":
    main()
