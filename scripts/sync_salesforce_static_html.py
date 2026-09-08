#!/usr/bin/env python3
"""
Sync static HTML pages for your-three-year-salesforce-backlog with:
- Card 1: Joe Williams profile card with background image (/images/melbourne-bourke-street-header.webp)
- Card 2: Red Highlights Header (#990000) & Navigational Sub-headings
- Card 3: Consultation Card moved to Column 2
- Center-aligned ASCII diagram with green monospace text on deep black
- Code Box: 1 single top row with tabs on left and theme/copy on right
"""

import os
from pathlib import Path

EZ_DIR = Path("/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezconsultants.com.au")
STATIC_FILE = EZ_DIR / "pages" / "blog" / "your-three-year-salesforce-backlog-is-now-this-week-s-sprint.html"
PUBLIC_FILE = EZ_DIR / "public" / "pages" / "blog" / "your-three-year-salesforce-backlog-is-now-this-week-s-sprint.html"
DIST_FILE = EZ_DIR / "dist" / "pages" / "blog" / "your-three-year-salesforce-backlog-is-now-this-week-s-sprint.html"

from enhance_salesforce_article_ui import (
    generate_tabbed_code_box,
    generate_mcp_config_box,
    generate_centered_architecture_diagram,
    generate_centered_cicd_diagram
)

tabbed_code_html = generate_tabbed_code_box()
mcp_box_html = generate_mcp_config_box()
arch_diag_html = generate_centered_architecture_diagram()
cicd_diag_html = generate_centered_cicd_diagram()

static_html_content = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Three-Year Salesforce Backlog Is Now This Week’s Sprint | EZ Consultants</title>
  <meta name="description" content="How Agentic IDEs (Claude Code, Cursor), MCP Servers, and Automated CI/CD are eliminating enterprise Salesforce technical debt while maintaining APRA CPS 234 compliance.">
  <link rel="canonical" href="https://ezconsultants.com.au/pages/blog/your-three-year-salesforce-backlog-is-now-this-week-s-sprint.html">
  
  <!-- OpenGraph / Facebook -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="Your Three-Year Salesforce Backlog Is Now This Week’s Sprint">
  <meta property="og:description" content="How Agentic IDEs, MCP Servers, and Automated CI/CD are eliminating enterprise Salesforce technical debt.">
  <meta property="og:url" content="https://ezconsultants.com.au/pages/blog/your-three-year-salesforce-backlog-is-now-this-week-s-sprint.html">
  <meta property="og:image" content="https://images.pexels.com/photos/17489150/pexels-photo-17489150.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Your Three-Year Salesforce Backlog Is Now This Week’s Sprint">
  <meta name="twitter:description" content="How Agentic IDEs, MCP Servers, and Automated CI/CD are eliminating enterprise Salesforce technical debt.">
  <meta name="twitter:image" content="https://images.pexels.com/photos/17489150/pexels-photo-17489150.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --navy-950: #061B2E;
      --navy-900: #0A2540;
      --navy-800: #0F3460;
      --blue-600: #0077C8;
      --blue-700: #005A9C;
      --amber-500: #D97706;
      --slate-50: #F8FAFC;
      --slate-100: #F1F5F9;
      --slate-200: #E2E8F0;
      --slate-600: #475569;
      --slate-800: #1E293B;
      --slate-900: #0F172A;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--slate-50);
      color: var(--slate-900);
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}
    .font-editorial {{ font-family: 'Lora', Georgia, serif; }}
    .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    
    /* Header */
    .site-header {{
      background: #FFFFFF;
      border-bottom: 1px solid var(--slate-200);
      position: sticky;
      top: 0;
      z-index: 1000;
    }}
    .header-inner {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand-logo {{
      font-size: 1.15rem;
      font-weight: 900;
      color: var(--navy-900);
      text-decoration: none;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .brand-logo span {{ color: var(--blue-600); }}
    .nav-links {{
      display: flex;
      gap: 24px;
      font-size: 0.9rem;
      font-weight: 700;
    }}
    .nav-links a {{ color: var(--slate-600); text-decoration: none; transition: color 0.15s ease; }}
    .nav-links a:hover, .nav-links a.active {{ color: var(--blue-600); }}
    .header-actions {{ display: flex; gap: 12px; }}
    .btn-header-outline {{
      padding: 8px 16px;
      border: 1.5px solid var(--navy-900);
      color: var(--navy-900);
      border-radius: 8px;
      font-weight: 700;
      text-decoration: none;
      font-size: 0.82rem;
    }}
    .btn-header-primary {{
      padding: 8px 18px;
      background: var(--blue-600);
      color: #FFFFFF;
      border-radius: 8px;
      font-weight: 700;
      text-decoration: none;
      font-size: 0.82rem;
    }}

    /* Hero Banner with Auto-Changing Blurred Backgrounds */
    .article-hero-section {{
      position: relative;
      background-color: var(--navy-950);
      color: #FFFFFF;
      padding: 56px 0 48px;
      border-bottom: 1px solid var(--slate-800);
      overflow: hidden;
    }}
    .hero-bg-carousel {{
      position: absolute;
      inset: 0;
      z-index: 1;
      pointer-events: none;
      overflow: hidden;
    }}
    .hero-bg-slide {{
      position: absolute;
      inset: -20px;
      background-size: cover;
      background-position: center;
      filter: blur(4px) brightness(0.85);
      transform: scale(1.04);
      opacity: 0;
      animation: heroSlideFade 15s infinite ease-in-out;
    }}
    .hero-bg-slide:nth-child(1) {{
      background-image: url('https://images.pexels.com/photos/1181354/pexels-photo-1181354.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940');
      animation-delay: 0s;
    }}
    .hero-bg-slide:nth-child(2) {{
      background-image: url('https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940');
      animation-delay: 5s;
    }}
    .hero-bg-slide:nth-child(3) {{
      background-image: url('https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940');
      animation-delay: 10s;
    }}
    @keyframes heroSlideFade {{
      0% {{ opacity: 0; transform: scale(1.02); }}
      8% {{ opacity: 0.85; transform: scale(1.04); }}
      33% {{ opacity: 0.85; transform: scale(1.06); }}
      40% {{ opacity: 0; transform: scale(1.08); }}
      100% {{ opacity: 0; transform: scale(1.02); }}
    }}
    .hero-gradient-scrim {{
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, rgba(6, 27, 46, 0.65) 0%, rgba(10, 37, 64, 0.55) 50%, rgba(6, 17, 28, 0.75) 100%);
      z-index: 2;
      pointer-events: none;
    }}
    .article-hero-inner {{
      position: relative;
      z-index: 3;
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 24px;
    }}
    .article-title {{
      font-size: clamp(2rem, 3.5vw, 2.75rem);
      font-weight: 900;
      line-height: 1.2;
      letter-spacing: -0.02em;
      margin: 0 0 16px;
      max-width: 980px;
      text-shadow: 0 2px 10px rgba(0,0,0,0.6);
    }}
    .breadcrumb-nav {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.8rem;
      font-weight: 700;
      color: #93C5FD;
      margin-bottom: 16px;
    }}
    .breadcrumb-nav a {{ color: #BFDBFE; text-decoration: none; }}
    .hero-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      margin-bottom: 16px;
    }}
    .category-badge {{
      background: rgba(0, 119, 200, 0.25);
      border: 1px solid #38BDF8;
      color: #BAE6FD;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .article-title {{
      font-size: clamp(2rem, 3.5vw, 2.75rem);
      font-weight: 900;
      line-height: 1.2;
      letter-spacing: -0.02em;
      margin: 0 0 16px;
      max-width: 980px;
    }}
    .article-lead {{
      font-size: 1.15rem;
      line-height: 1.6;
      color: #CBD5E1;
      max-width: 880px;
      margin: 0;
    }}

    /* 2-Column Continuous Sheet Layout */
    .article-layout-grid {{
      max-width: 1200px;
      margin: 40px auto 60px;
      padding: 0 24px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 340px;
      gap: 36px;
      align-items: start;
    }}
    @media (max-width: 991px) {{
      .article-layout-grid {{ grid-template-columns: 1fr; }}
    }}

    .article-a4-sheet {{
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      border-radius: 18px;
      padding: 44px 48px;
      box-shadow: 0 4px 16px rgba(10, 37, 64, 0.04);
      min-width: 0;
      max-width: 100%;
      overflow: hidden;
    }}
    @media (max-width: 640px) {{
      .article-a4-sheet {{ padding: 24px 20px; }}
    }}

    .summary-card {{
      background: #EFF6FF;
      border-left: 4px solid var(--blue-600);
      border-radius: 0 12px 12px 0;
      padding: 24px;
      margin-bottom: 32px;
    }}
    .summary-title {{
      font-size: 0.78rem;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--blue-600);
      margin-bottom: 8px;
    }}
    .summary-text {{
      font-size: 1.02rem;
      line-height: 1.65;
      color: var(--slate-900);
      margin: 0;
    }}

    html {{
      scroll-behavior: smooth;
      scroll-padding-top: 110px;
    }}
    section[id], h2[id], h3[id], .section-heading, .sub-heading {{
      scroll-margin-top: 110px !important;
    }}

    /* Typography inside article */
    .section-heading {{
      font-size: 1.45rem;
      font-weight: 900;
      color: var(--navy-900);
      margin: 40px 0 16px;
      border-bottom: 2px solid var(--slate-100);
      padding-bottom: 10px;
      letter-spacing: -0.01em;
      scroll-margin-top: 110px !important;
    }}
    .section-heading:first-of-type {{ margin-top: 0; }}
    .sub-heading {{
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--navy-900);
      margin: 28px 0 12px;
      scroll-margin-top: 110px !important;
    }}
    .editorial-p {{
      font-size: 1.02rem;
      line-height: 1.75;
      color: #334155;
      margin: 0 0 18px;
    }}
    .editorial-p strong {{ color: var(--navy-900); }}

    /* Data Tables */
    .data-table-container {{
      overflow-x: auto;
      margin: 24px 0;
      border: 1px solid var(--slate-200);
      border-radius: 12px;
    }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      text-align: left;
    }}
    .data-table th {{
      background: var(--navy-900);
      color: #FFFFFF;
      font-weight: 800;
      padding: 12px 16px;
      border-bottom: 1px solid var(--slate-200);
    }}
    .data-table td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--slate-200);
      color: #334155;
    }}
    .data-table tr:last-child td {{ border-bottom: none; }}
    .data-table tr:nth-child(even) td {{ background: #F8FAFC; }}

    /* Highlights Callout */
    .callout-box {{
      background: #F8FAFC;
      border-left: 4px solid var(--blue-600);
      border-radius: 0 10px 10px 0;
      padding: 16px 20px;
      font-size: 0.92rem;
      color: var(--slate-900);
      margin: 24px 0;
      line-height: 1.55;
    }}

    /* Sticky Sidebar */
    .sticky-sidebar {{
      position: -webkit-sticky;
      position: sticky;
      top: 90px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}

    /* Card 1: Principal Consultant Profile Card */
    .profile-card {{
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 4px 14px rgba(10, 37, 64, 0.06);
      text-align: center;
    }}
    .profile-header-bg {{
      background: linear-gradient(135deg, rgba(8, 69, 130, 0.45) 0%, rgba(6, 40, 77, 0.75) 100%), url('/images/melbourne-bourke-street-header.webp') center/cover no-repeat;
      height: 96px;
      position: relative;
      display: flex;
      justify-content: center;
    }}
    .profile-avatar {{
      position: absolute;
      bottom: -32px;
      width: 64px;
      height: 64px;
      border-radius: 50%;
      border: 2.5px solid #FFFFFF;
      overflow: hidden;
      background: #FFFFFF;
      box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }}
    .profile-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
    .profile-body {{ padding: 40px 16px 18px; }}
    .profile-name {{
      font-size: 1.05rem;
      font-weight: 900;
      color: var(--navy-900);
      margin: 0 0 2px;
      text-transform: uppercase;
      letter-spacing: 0.02em;
    }}
    .profile-role {{
      font-size: 0.7rem;
      font-weight: 800;
      color: var(--blue-600);
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .profile-bio {{
      font-size: 0.76rem;
      color: #475569;
      line-height: 1.42;
      margin: 0 0 12px;
      font-weight: 500;
    }}
    .profile-creds {{
      background: var(--slate-50);
      border: 1px solid var(--slate-200);
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 0.7rem;
      color: var(--slate-800);
      text-align: left;
      margin-bottom: 14px;
      line-height: 1.4;
    }}
    .profile-actions {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      width: 100%;
    }}
    .btn-profile-call {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      background: var(--blue-600);
      color: #FFFFFF !important;
      font-weight: 800;
      padding: 9px 4px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 0.78rem;
      white-space: nowrap;
      box-shadow: 0 2px 6px rgba(0, 119, 200, 0.2);
    }}
    .btn-profile-consult {{
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--navy-900);
      color: #FFFFFF !important;
      font-weight: 800;
      padding: 9px 4px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 0.78rem;
      white-space: nowrap;
    }}

    /* Card 2: Highlights Accordion (Crimson Red Header) */
    .highlights-card {{
      background: #FFFFFF;
      border: 1.5px solid var(--slate-200);
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .highlights-header {{
      background: #990000;
      padding: 12px 18px;
      color: #FFFFFF !important;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .highlights-title {{
      font-size: 0.82rem;
      font-weight: 900;
      text-transform: uppercase;
      margin: 0;
      letter-spacing: 0.04em;
      color: #FFFFFF !important;
    }}
    .highlights-tag {{
      font-size: 0.68rem;
      font-weight: 800;
      color: #FFFFFF !important;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      opacity: 0.9;
    }}
    .highlights-body {{ padding: 18px; }}
    .highlights-date {{
      font-size: 0.74rem;
      font-weight: 800;
      color: #64748B;
      margin-bottom: 14px;
    }}
    .highlights-timeline {{
      border-left: 2px solid var(--slate-200);
      padding-left: 16px;
      margin-left: 4px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .timeline-item {{
      position: relative;
      text-decoration: none;
      display: block;
      cursor: pointer;
    }}
    .timeline-bullet {{
      position: absolute;
      left: -21px;
      top: 3px;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #990000;
      border: 2px solid #FFFFFF;
      box-shadow: 0 0 0 2px #FEE2E2;
      transition: transform 0.15s ease;
    }}
    .timeline-item:hover .timeline-bullet {{
      transform: scale(1.3);
    }}
    .timeline-label {{
      font-size: 0.7rem;
      font-weight: 900;
      color: #990000;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    .timeline-heading {{
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--slate-900);
      line-height: 1.3;
      transition: color 0.15s ease;
    }}
    .timeline-item:hover .timeline-heading {{
      color: #990000;
    }}

    /* Card 3: Consultation CTA Card */
    .sidebar-cta-card {{
      background: linear-gradient(135deg, var(--navy-900) 0%, var(--navy-950) 100%);
      border: 2px solid rgba(0, 119, 200, 0.4);
      border-radius: 18px;
      padding: 20px;
      color: #FFFFFF;
      box-shadow: 0 4px 14px rgba(10,37,64,0.06);
    }}
    .btn-cta-gold {{
      display: block !important;
      text-align: center !important;
      padding: 12px 18px !important;
      font-size: 0.85rem !important;
      font-weight: 800 !important;
      width: 100% !important;
      background: linear-gradient(135deg, #0077C8 0%, #005A9C 100%) !important;
      color: #FFFFFF !important;
      text-decoration: none !important;
      border-radius: 10px !important;
      box-shadow: 0 4px 14px rgba(0, 119, 200, 0.4) !important;
      border: 1px solid rgba(255, 255, 255, 0.25) !important;
      text-transform: uppercase !important;
      letter-spacing: 0.03em !important;
      transition: transform 0.15s ease, background 0.15s ease !important;
    }}
    .btn-cta-gold:hover {{
      background: linear-gradient(135deg, #0088E8 0%, #006AB8 100%) !important;
      transform: translateY(-1px) !important;
      color: #FFFFFF !important;
    }}

    /* Section Flash Animation */
    @keyframes sectionFlash {{
      0% {{
        background-color: rgba(0, 119, 200, 0.25);
        border-radius: 12px;
        box-shadow: 0 0 0 8px rgba(0, 119, 200, 0.2);
        transform: scale(1.01);
      }}
      50% {{
        background-color: rgba(0, 119, 200, 0.08);
      }}
      100% {{
        background-color: transparent;
        box-shadow: none;
        transform: scale(1);
      }}
    }}
    .section-highlight-flash {{
      animation: sectionFlash 1.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    /* Center-Aligned Architecture Diagram */
    .ascii-diagram-container {{
      background: #06111C !important;
      border: 1px solid #1e293b !important;
      border-radius: 14px !important;
      padding: 24px !important;
      margin: 28px 0 !important;
      display: flex !important;
      justify-content: center !important;
      text-align: center !important;
      overflow-x: auto !important;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
    }}
    .ascii-diagram-container pre {{
      color: #10B981 !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.78rem !important;
      line-height: 1.35 !important;
      margin: 0 auto !important;
      display: inline-block !important;
      text-align: left !important;
    }}

    /* Salesforce Developer Code Playground & Theme Modes */
    .code-box-wrapper {{
      box-shadow: 0 4px 14px rgba(10,37,64,0.06);
    }}
    .code-viewport {{
      transition: background 0.2s ease, color 0.2s ease;
    }}
    .code-theme-light .code-viewport {{
      background: #F8FAFC !important;
      color: #0F172A !important;
      border-top: 1px solid #E2E8F0 !important;
    }}
    .code-theme-light .line-number {{
      color: #94A3B8 !important;
    }}
    .hidden {{ display: none !important; }}

    /* Footer */
    .site-footer {{
      border-top: 1px solid var(--slate-200);
      background: #FFFFFF;
      padding: 32px 24px;
      text-align: center;
      font-size: 0.82rem;
      color: var(--slate-600);
      margin-top: 60px;
    }}
    .site-footer a {{ color: var(--blue-600); text-decoration: none; }}
  </style>
</head>
<body>

  <!-- Site Header -->
  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="brand-logo">
        EZ CONSULTANTS <span>AU</span>
      </a>
      <nav class="nav-links">
        <a href="/">Home</a>
        <a href="/services">Services</a>
        <a href="/solutions">Solutions</a>
        <a href="/pages/blog.html" class="active">Insights</a>
        <a href="/contact">Contact</a>
      </nav>
      <div class="header-actions">
        <a href="tel:1300050099" class="btn-header-outline">1300 050 099</a>
        <a href="/contact" class="btn-header-primary">Book Consultation</a>
      </div>
    </div>
  </header>

  <!-- Hero Banner with Auto-Changing Blurred Background -->
  <section class="article-hero-section">
    <div class="hero-bg-carousel">
      <div class="hero-bg-slide"></div>
      <div class="hero-bg-slide"></div>
      <div class="hero-bg-slide"></div>
    </div>
    <div class="hero-gradient-scrim"></div>
    <div class="article-hero-inner">
      <nav class="breadcrumb-nav">
        <a href="/">Home</a>
        <span>/</span>
        <a href="/pages/blog.html">Insights</a>
        <span>/</span>
        <span>CRM Architecture &amp; DevOps</span>
      </nav>
      <div class="hero-meta">
        <span class="category-badge">CRM Architecture &amp; DevOps</span>
        <span style="font-size:0.8rem; color:#94A3B8;">Published: 08-Sep-2026</span>
        <span style="font-size:0.8rem; color:#94A3B8;">•</span>
        <span style="font-size:0.8rem; color:#94A3B8;">Author: Joe Williams (Lead Technical Architect)</span>
        <span style="font-size:0.8rem; color:#94A3B8;">•</span>
        <a href="https://buy.nsw.gov.au/supplier/profile/180179" target="_blank" style="color:#38BDF8; font-weight:700; text-decoration:none; font-size:0.8rem;">buy.nsw Supplier 180179 ↗</a>
      </div>
      <h1 class="article-title">Your Three-Year Salesforce Backlog Is Now This Week’s Sprint</h1>
      <p class="font-editorial article-lead">
        How Agentic IDEs (Claude Code, Cursor), Model Context Protocol (MCP) servers, and automated CI/CD pipelines are eliminating enterprise Salesforce technical debt while maintaining APRA CPS 234 and ISO 27001 compliance.
      </p>
    </div>
  </section>

  <!-- Main Article Layout -->
  <main class="article-layout-grid">
    
    <!-- Left Column: Single Continuous A4-Style Editorial Sheet -->
    <article class="article-a4-sheet">
      
      <!-- Section 1 -->
      <section id="mcp-workspace">
        <h2 class="section-heading">1. The Architectural Shift: The Agentic Developer Workspace</h2>
        <p class="editorial-p">
          Traditional LLM coding assistants act as intelligent autocomplete engines: they suggest functions based on the open file. Agentic IDEs behave as autonomous engineers: they parse Abstract Syntax Trees (ASTs), execute terminal commands, crawl dependencies across your repository, and iteratively test their work.
        </p>

        {arch_diag_html}

        <p class="editorial-p">
          The catalyst bridging the IDE to the Salesforce platform is <strong>Model Context Protocol (MCP)</strong>. MCP standardizes how local development environments expose tools, resources, and contextual prompts to language models.
        </p>

        <h3 class="sub-heading">Connecting the Org via MCP</h3>
        <p class="editorial-p">
          Rather than pasting Apex classes and object schema definitions into chat windows, an enterprise MCP server exposes read/write platform operations directly to the agent runtime:
        </p>

        {mcp_box_html}

        <p class="editorial-p">Through this abstraction, the agent has native access to:</p>
        <ul style="color:#334155; line-height:1.7; margin-bottom:24px;">
          <li><strong>get_object_metadata(sobjectApiName):</strong> Pulls picklist values, record types, and relationship schemas.</li>
          <li><strong>query_tooling_api(soql):</strong> Inspects SymbolTable, ApexClass, and CoverageItem.</li>
          <li><strong>fetch_debug_logs(userId):</strong> Ingests platform logs to triage exceptions during local test runs.</li>
        </ul>
      </section>

      <!-- Section 2 -->
      <section id="fflib-refactoring">
        <h2 class="section-heading">2. Tackling the Debt: Concrete Remediations</h2>
        <p class="editorial-p">
          When configured with an understanding of Salesforce architecture, the agent can systematically work down legacy backlogs.
        </p>

        <h3 class="sub-heading">Scenario A: Refactoring Monolithic Triggers to Domain Frameworks (fflib)</h3>
        <p class="editorial-p">
          Legacy orgs frequently house 1,500-line triggers intermixing SOQL queries, business logic, and DML operations. Below are the decoupled LWC and Apex test mocking patterns generated by the agentic toolchain:
        </p>

        {tabbed_code_html}

        <p class="editorial-p">
          Using the agentic toolchain for enterprise refactoring:
        </p>
        <ul style="color:#334155; line-height:1.7; margin-bottom:24px;">
          <li><strong>Context Ingestion:</strong> The agent uses MCP to crawl the legacy trigger, its companion test classes, and all referenced SObject fields.</li>
          <li><strong>Structural Decomposition:</strong> The agent partitions the logic into enterprise patterns (Trigger Handler dispatch, Domain validation, Selector cached SOQL, and Service orchestration).</li>
          <li><strong>Execution:</strong> The agent builds new files, updates references, and verifies that no Governor Limits are introduced via nested loops.</li>
        </ul>
      </section>

      <!-- Section 3 -->
      <section id="governance-cicd">
        <h2 class="section-heading">3. Governance, CI/CD, and Compliance (APRA CPS 234 / ISO 27001)</h2>
        <p class="editorial-p">
          Autonomous code generation without rigorous verification risks generating hallucinations: hallucinated custom fields, bypassing object permissions (<code>with sharing</code>), or ignoring SOQL injection vectors. Deploying agent-generated code directly to persistent sandboxes is strictly prohibited. The deployment model must rely on ephemeral environments and automated static analysis.
        </p>

        {cicd_diag_html}

        <h3 class="sub-heading">Key Guardrails for Autonomous Delivery</h3>
        <div class="data-table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Layer</th>
                <th>Tool / Mechanism</th>
                <th>Enforcement Standard</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Static Analysis</strong></td>
                <td>Salesforce Code Analyzer / PMD</td>
                <td>Rejects any code missing <code>with sharing</code>, containing unescaped dynamic SOQL, or introducing hardcoded IDs.</td>
              </tr>
              <tr>
                <td><strong>Ephemeral Test Bed</strong></td>
                <td>Salesforce Scratch Orgs</td>
                <td>The agent must prove its refactoring runs cleanly in a pristine org, completely isolated from shared dev environments.</td>
              </tr>
              <tr>
                <td><strong>Coverage Floor</strong></td>
                <td>Apex Test Framework</td>
                <td>Minimum 85% real branch coverage; zero tolerance for dummy assertion blocks (<code>System.assert(true)</code>).</td>
              </tr>
              <tr>
                <td><strong>Data Protection</strong></td>
                <td>MCP Scope Restrictions</td>
                <td>Prevent LLM processes from accessing production data pools; limit MCP access strictly to metadata endpoints to maintain compliance with <strong>Australian Privacy Principles (APP)</strong>.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Section 4 -->
      <section id="engineering-protocol">
        <h2 class="section-heading">4. The New Engineering Protocol</h2>
        <p class="editorial-p">
          Agentic tooling does not eliminate developers; it elevates them into technical architects and code reviewers. A team of four developers operating with well-configured MCP toolchains and rigid CI/CD validation can deliver the throughput of a 20-person legacy offshore maintenance pod.
        </p>
        <p class="editorial-p">
          The organizations clearing multi-year backlogs in 2026 are not writing code line-by-line. They are building the <strong>prompt contexts, MCP boundaries, and automated validation pipelines</strong> that allow autonomous agents to execute safe refactoring at scale.
        </p>
        <div class="callout-box">
          <strong>💡 Enterprise Architecture Rule:</strong> Under APRA CPS 234 and Australian data sovereignty mandates, agentic tooling must be locked to metadata-only access. Production data synthesis must occur strictly within isolated scratch org sandboxes.
        </div>
      </section>

    </article>

    <!-- Right Column: Sticky Sidebar Card 1, Card 2, Card 3 -->
    <aside class="sticky-sidebar">
      
      <!-- Card 1: Principal Technical Architect Profile Card (With Header BG) -->
      <div class="profile-card">
        <div class="profile-header-bg">
          <div class="profile-avatar">
            <img src="/images/ez-consultants-avatar.svg" alt="Joe Williams">
          </div>
        </div>
        <div class="profile-body">
          <h3 class="profile-name">JOE WILLIAMS</h3>
          <div class="profile-role">
            LEAD TECHNICAL ARCHITECT &amp; CONSULTANT
          </div>
          <p class="profile-bio">
            Specializing in Salesforce enterprise architecture, Agentforce, MuleSoft integrations, and APRA CPS 234 compliant DevOps pipelines.
          </p>
          <div class="profile-creds">
            <div><strong>Supplier:</strong> NSW Government (buy.nsw 180179)</div>
            <div><strong>Certifications:</strong> Salesforce CTA Track, MuleSoft</div>
            <div><strong>Compliance:</strong> APRA CPS 234, ISO 27001</div>
          </div>
          <div class="profile-actions">
            <a href="tel:1300050099" class="btn-profile-call">
              <span>📞 Call Us</span>
            </a>
            <a href="/contact" class="btn-profile-consult">
              📅 Book Consult
            </a>
          </div>
        </div>
      </div>

      <!-- Card 2: Highlights Accordion (Red Header - Image 1 Format) -->
      <div class="highlights-card">
        <div class="highlights-header">
          <h3 class="highlights-title">Highlights</h3>
          <span class="highlights-tag">In this article</span>
        </div>
        <div class="highlights-body">
          <div class="highlights-date">— 08 September 2026</div>
          <div class="highlights-timeline">
            <a href="#mcp-workspace" onclick="scrollToSection(event, 'mcp-workspace')" class="timeline-item">
              <span class="timeline-bullet"></span>
              <div class="timeline-label">01. THE ARCHITECTURAL SHIFT</div>
              <div class="timeline-heading">The Agentic Developer Workspace</div>
            </a>
            <a href="#fflib-refactoring" onclick="scrollToSection(event, 'fflib-refactoring')" class="timeline-item">
              <span class="timeline-bullet"></span>
              <div class="timeline-label">02. TACKLING THE DEBT</div>
              <div class="timeline-heading">Refactoring Monolithic Triggers to fflib</div>
            </a>
            <a href="#governance-cicd" onclick="scrollToSection(event, 'governance-cicd')" class="timeline-item">
              <span class="timeline-bullet"></span>
              <div class="timeline-label">03. GOVERNANCE &amp; COMPLIANCE</div>
              <div class="timeline-heading">APRA CPS 234 &amp; ISO 27001 Guardrails</div>
            </a>
            <a href="#engineering-protocol" onclick="scrollToSection(event, 'engineering-protocol')" class="timeline-item">
              <span class="timeline-bullet"></span>
              <div class="timeline-label">04. ENGINEERING PROTOCOL</div>
              <div class="timeline-heading">The New AI-First Delivery Paradigm</div>
            </a>
          </div>
        </div>
      </div>

      <!-- Card 3: Enterprise Consultation Card (Moved to Column 2) -->
      <div class="sidebar-cta-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
          <div style="width:48px; height:58px; flex-shrink:0; background:#FFFFFF; padding:4px; border-radius:8px; display:flex; align-items:center; justify-content:center;">
            <img src="/images/nsw-government-approved-supplier.svg" alt="NSW Government Supplier" style="max-width:100%; max-height:100%; object-fit:contain;" />
          </div>
          <div>
            <div style="font-size:0.68rem; font-weight:800; color:#38BDF8; text-transform:uppercase; letter-spacing:0.04em;">Accredited NSW Supplier</div>
            <h4 style="font-size:0.92rem; font-weight:900; margin:2px 0 0; line-height:1.25; color:#FFFFFF;">Ready to Modernize Your Salesforce Architecture?</h4>
          </div>
        </div>
        <p style="font-size:0.75rem; color:#CBD5E1; margin:0 0 14px; line-height:1.45;">
          EZ Consultants delivers ISO 27001 &amp; APRA CPS 234 compliant Salesforce implementations and CI/CD pipelines.
        </p>
        <a href="/contact" class="btn-cta-gold" style="display:block; text-align:center; padding:10px 16px; font-size:0.8rem; width:100%;">Book Architecture Audit ↗</a>
      </div>

    </aside>
  </main>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div style="max-width:1200px; margin:0 auto; display:flex; flex-direction:column; sm:flex-direction:row; justify-content:space-between; align-items:center; gap:12px;">
      <div>&copy; 2026 EZ Consultants Australia. All rights reserved.</div>
      <div>
        <a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms of Service</a> · <a href="/rss.xml">RSS Feed</a>
      </div>
    </div>
  </footer>

  <script>
    function scrollToSection(e, id) {{
      if (e && e.preventDefault) e.preventDefault();
      const cleanId = id ? id.replace(/^#/, '') : '';
      const el = document.getElementById(cleanId);
      if (el) {{
        const headerOffset = 110;
        const elementPosition = el.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
        window.scrollTo({{
          top: offsetPosition,
          behavior: 'smooth'
        }});
        el.classList.remove('section-highlight-flash');
        void el.offsetWidth;
        el.classList.add('section-highlight-flash');
      }}
    }}

    function switchSubTab(e, subtargetId) {{
      const wrapper = e.currentTarget.closest('.code-box-wrapper');
      if (!wrapper) return;
      wrapper.querySelectorAll('.subtab-btn').forEach(btn => {{
        btn.classList.remove('active-subtab');
        btn.style.borderBottom = '2px solid transparent';
        btn.style.color = '#64748b';
        btn.style.fontWeight = '700';
      }});
      e.currentTarget.classList.add('active-subtab');
      e.currentTarget.style.borderBottom = '2px solid #0077c8';
      e.currentTarget.style.color = '#0077c8';
      e.currentTarget.style.fontWeight = '800';

      wrapper.querySelectorAll('.subtab-pane').forEach(p => {{
        p.classList.add('hidden');
        p.style.display = 'none';
      }});
      const targetPane = wrapper.querySelector('#' + subtargetId);
      if (targetPane) {{
        targetPane.classList.remove('hidden');
        targetPane.style.display = 'block';
      }}
    }}

    function toggleCodeTheme(e) {{
      const wrapper = e.currentTarget.closest('.code-box-wrapper');
      if (!wrapper) return;
      wrapper.classList.toggle('code-theme-light');
      const icon = wrapper.querySelector('.theme-icon');
      const label = wrapper.querySelector('.theme-label');
      const isLight = wrapper.classList.contains('code-theme-light');
      if (icon) {{
        icon.textContent = isLight ? '☀️' : '🌙';
      }}
      if (label) {{
        label.textContent = isLight ? 'Light' : 'Dark';
      }}
    }}

    function copyActiveCode(e) {{
      const wrapper = e.currentTarget.closest('.code-box-wrapper');
      if (!wrapper) return;
      let codeEl = wrapper.querySelector('.subtab-pane:not(.hidden):not([style*="display: none"]) code') || wrapper.querySelector('pre code');
      if (codeEl) {{
        const text = codeEl.innerText || codeEl.textContent;
        navigator.clipboard.writeText(text);
        const label = e.currentTarget.querySelector('.copy-label') || e.currentTarget;
        const originalText = label.innerHTML;
        label.innerHTML = 'Copied! ✓';
        e.currentTarget.style.background = '#10b981';
        setTimeout(() => {{
          label.innerHTML = originalText;
          e.currentTarget.style.background = '#0077c8';
        }}, 2000);
      }}
    }}
  </script>
</body>
</html>
"""

for target in [STATIC_FILE, PUBLIC_FILE, DIST_FILE]:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(static_html_content, encoding="utf-8")
    print(f"✓ Updated: {target}")

print("Static HTML synchronization complete.")
