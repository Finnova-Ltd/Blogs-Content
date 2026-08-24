#!/usr/bin/env python3
"""
Master Visual HTML Sitemap Builder across all 5 Finnova Platforms:
1. EZ Mortgage Broker (ezmortgagebroker.com.au/sitemap.html)
2. EZ Consultants (ezconsultants.com.au/sitemap)
3. PRO CRM (procrm.com.au/sitemap)
4. Finnova Community Hub (finnova.org.au/sitemap.html)
5. EZ Signature Online (ezsignature.com/sitemap)

Features:
- Exact 2-Column layout inspired by Image 1 (Creare style)
- Structured nested hierarchy (Main Pages, Core Services, Calculators/Tools, Blog Categories, Legal, XML Feeds)
- Interactive Right Sidebar (Instant Live Search Filter, Category Pills, Quick Enquiry Form, Direct 1300/Call CTA)
- 100% Crisp Light-Theme design
"""

import os
import json

EZ_MORTGAGE_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
EZ_CONSULTANTS_DIR = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au"
PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
FINNOVA_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova"
EZSIGNATURE_DIR = "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend"

# ==============================================================================
# 1. BUILD EZ MORTGAGE BROKER (sitemap.html)
# ==============================================================================
def build_ezmortgagebroker_sitemap():
    posts_path = os.path.join(EZ_MORTGAGE_DIR, "posts.json")
    posts = []
    if os.path.exists(posts_path):
        with open(posts_path, "r", encoding="utf-8") as f:
            posts = json.load(f)

    blog_links_html = ""
    for p in posts:
        slug = p.get("slug", "")
        title = p.get("title", "")
        blog_links_html += f'                <li><a href="/pages/article.html?slug={slug}">{title}</a></li>\n'

    sitemap_html = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4107133850485301" crossorigin="anonymous"></script>
  <link rel="icon" type="image/webp" href="/images/ez-mortgage-broker.webp">
  <link rel="apple-touch-icon" href="/images/ez-mortgage-broker.webp">
  <meta name="theme-color" content="#0A2540">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Explore the comprehensive HTML sitemap of EZ Mortgage Broker. Browse all home loan options, refinance guides, property calculators, state locations, and market intelligence articles.">
  <title>Sitemap | EZ Mortgage Broker Australia</title>
  <link rel="canonical" href="https://ezmortgagebroker.com.au/sitemap.html">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">

  <style>
    :root {{
      --primary: #0A2540;
      --accent: #FF5A1F;
      --accent-hover: #E04810;
      --teal: #0D9488;
      --slate-50: #F8FAFC;
      --slate-100: #F1F5F9;
      --slate-200: #E2E8F0;
      --slate-700: #334155;
      --slate-900: #0F172A;
    }}
    body {{
      background-color: #FAFAFA;
      color: var(--slate-900);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .sitemap-header-banner {{
      background: linear-gradient(135deg, #0A2540 0%, #0F172A 100%);
      color: #ffffff;
      padding: 48px 0 40px;
      border-bottom: 3px solid var(--accent);
    }}
    .sitemap-layout {{
      max-width: 1240px;
      margin: 40px auto 80px;
      padding: 0 20px;
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 48px;
    }}
    @media (max-width: 900px) {{
      .sitemap-layout {{
        grid-template-columns: 1fr;
        gap: 32px;
      }}
    }}
    .sitemap-content h1 {{
      font-size: 2.5rem;
      font-weight: 900;
      color: var(--slate-900);
      margin-bottom: 8px;
      letter-spacing: -0.02em;
    }}
    .sitemap-subtitle {{
      color: #64748B;
      font-size: 1.05rem;
      margin-bottom: 32px;
    }}
    .sitemap-tree {{
      background: #ffffff;
      border: 1px solid var(--slate-200);
      border-radius: 20px;
      padding: 36px 40px;
      box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.05);
    }}
    .sitemap-tree ul {{
      list-style-type: none;
      padding-left: 20px;
      position: relative;
    }}
    .sitemap-tree > ul {{
      padding-left: 0;
    }}
    .sitemap-tree li {{
      position: relative;
      margin: 10px 0;
      line-height: 1.6;
    }}
    .sitemap-tree > ul > li {{
      margin-top: 24px;
      font-weight: 800;
      font-size: 1.15rem;
      color: var(--primary);
    }}
    .sitemap-tree > ul > li > a {{
      color: var(--primary);
      text-decoration: none;
    }}
    .sitemap-tree > ul > li > a:hover {{
      color: var(--accent);
    }}
    .sitemap-tree ul ul li {{
      font-weight: 500;
      font-size: 0.95rem;
    }}
    .sitemap-tree ul ul li::before {{
      content: "•";
      color: var(--accent);
      font-weight: bold;
      display: inline-block;
      width: 1em;
      margin-left: -1em;
    }}
    .sitemap-tree a {{
      color: #334155;
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    .sitemap-tree a:hover {{
      color: var(--accent);
      padding-left: 4px;
    }}
    
    /* Sidebar Widgets */
    .sidebar-widget {{
      background: #ffffff;
      border: 1px solid var(--slate-200);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.04);
    }}
    .search-input-group {{
      display: flex;
      border-radius: 10px;
      overflow: hidden;
      border: 2px solid var(--slate-200);
    }}
    .search-input-group input {{
      flex: 1;
      padding: 12px 14px;
      border: none;
      outline: none;
      font-size: 0.9rem;
    }}
    .search-input-group button {{
      background: var(--accent);
      color: white;
      border: none;
      padding: 0 20px;
      font-weight: 800;
      cursor: pointer;
      text-transform: uppercase;
      font-size: 0.85rem;
    }}
    .category-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
    }}
    .category-pill {{
      display: inline-block;
      background: var(--teal);
      color: white;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 700;
      text-decoration: none;
      transition: transform 0.15s ease;
    }}
    .category-pill:hover {{
      transform: translateY(-2px);
      background: #0F766E;
    }}
    .quick-form input, .quick-form textarea {{
      width: 100%;
      padding: 10px 14px;
      margin-bottom: 12px;
      border: 1px solid var(--slate-200);
      border-radius: 8px;
      font-size: 0.88rem;
      box-sizing: border-box;
    }}
    .quick-form button {{
      width: 100%;
      background: var(--primary);
      color: white;
      border: none;
      padding: 12px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 0.95rem;
      cursor: pointer;
      transition: background 0.2s;
    }}
    .quick-form button:hover {{
      background: var(--accent);
    }}
  </style>
</head>
<body>

  <!-- Site Header -->
  <header class="site-header">
    <div class="header-main">
      <div class="container">
        <div class="header-inner">
          <a href="/" class="logo"><img class="brand-logo" src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" style="height: clamp(68px, 6.5vw, 84px); width: auto; max-width: 300px; display: inline-block;"></a>
          <nav aria-label="Primary navigation">
            <ul class="nav-primary">
              <li><a href="/">Home</a></li>
              <li><a href="/pages/buying-a-home.html">Personal</a></li>
              <li><a href="/pages/business-finance.html">Business</a></li>
              <li><a href="/calculators.html">Calculators</a></li>
              <li><a href="/pages/blog.html">Blog</a></li>
              <li><a href="/locations.html">Locations</a></li>
              <li><a href="/#contact">Contact</a></li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </header>

  <!-- Banner -->
  <section class="sitemap-header-banner">
    <div class="container" style="max-width: 1240px; margin: 0 auto; padding: 0 20px;">
      <span style="background: rgba(255,255,255,0.15); color: #FFDC4A; padding: 4px 12px; border-radius: 50px; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">Website Directory &amp; Navigation</span>
      <h1 style="color: #ffffff; font-size: 2.4rem; font-weight: 900; margin: 10px 0 6px;">EZ Mortgage Broker Sitemap</h1>
      <p style="color: #E2E8F0; font-size: 1.05rem; margin: 0;">Comprehensive index of all mortgage solutions, borrowing calculators, state guides, and articles.</p>
    </div>
  </section>

  <!-- 2-Column Layout -->
  <main class="sitemap-layout">
    
    <!-- Left Column: Content Tree -->
    <div class="sitemap-content">
      <h1>Sitemap</h1>
      <p class="sitemap-subtitle">Browse through the pages on our site below.</p>

      <div class="sitemap-tree" id="sitemapTree">
        <ul>
          <li><a href="/">Home Page</a></li>
          <li><a href="/#about">About Us &amp; Our Accredited Broker Team</a></li>
          
          <li>
            <a href="/pages/buying-a-home.html">Personal &amp; Residential Home Loans</a>
            <ul>
              <li><a href="/pages/first_home_buyers.html">First Home Buyers Grant (FHOG) &amp; 5% Scheme</a></li>
              <li><a href="/pages/refinancing.html">Mortgage Refinancing &amp; Rate Reduction</a></li>
              <li><a href="/pages/investment_loans.html">Property Investment &amp; Equity Cash-Out</a></li>
              <li><a href="/pages/loans/ndis-sda-property-finance.html">NDIS SDA Property Specialist Finance</a></li>
              <li><a href="/pages/loans/self-employed-alt-doc-loans.html">Self-Employed &amp; Alt-Doc Home Loans</a></li>
            </ul>
          </li>

          <li>
            <a href="/pages/business-finance.html">Business, Commercial &amp; SMSF Lending</a>
            <ul>
              <li><a href="/pages/business_finance.html">Commercial Real Estate Mortgages</a></li>
              <li><a href="/pages/business_finance.html#asset">Asset, Vehicle &amp; Equipment Finance</a></li>
              <li><a href="/pages/business_finance.html#smsf">SMSF Limited Recourse Property Loans</a></li>
              <li><a href="/pages/business_finance.html#working-capital">SME Working Capital &amp; Invoice Lines</a></li>
            </ul>
          </li>

          <li>
            <a href="/calculators.html">Mortgage &amp; Financial Calculators</a>
            <ul>
              <li><a href="/calculators.html#borrowing-power">Borrowing Power Calculator</a></li>
              <li><a href="/calculators.html#loan-repayment">Loan Repayment Estimator</a></li>
              <li><a href="/calculators.html#stamp-duty">State Stamp Duty &amp; Concessions Calculator</a></li>
              <li><a href="/calculators.html#extra-repayments">Extra Repayments &amp; Lump Sum Savings</a></li>
              <li><a href="/calculators.html#offset">Offset Account Interest Savings Calculator</a></li>
              <li><a href="/calculators.html#refinance">Refinance Break-Even &amp; Cash Savings</a></li>
            </ul>
          </li>

          <li><a href="/locations.html">Locations &amp; State Service Areas (VIC, NSW, QLD, WA, SA)</a></li>

          <li>
            <a href="/pages/blog.html">Market Insights &amp; Knowledge Base (All Articles)</a>
            <ul id="blogLinksList">
{blog_links_html}
            </ul>
          </li>

          <li>
            Compliance, Governance &amp; Machine Feeds
            <ul>
              <li><a href="/privacy-policy.html">Privacy Policy &amp; Credit Reporting Guide</a></li>
              <li><a href="/terms-of-use.html">Terms of Use &amp; Regulatory Disclaimer</a></li>
              <li><a href="/cookie-policy.html">Cookie Policy &amp; Tracking Consent</a></li>
              <li><a href="/sitemap.xml">XML Search Engine Sitemap (sitemap.xml)</a></li>
              <li><a href="/sitemap-news.xml">Google News XML Sitemap (sitemap-news.xml)</a></li>
              <li><a href="/sitemap_index.xml">Master Sitemap Index (sitemap_index.xml)</a></li>
              <li><a href="/feed.xml">RSS / Atom News Feed (feed.xml)</a></li>
            </ul>
          </li>

        </ul>
      </div>
    </div>

    <!-- Right Column: Sidebar (Image 1 Style) -->
    <aside class="sitemap-sidebar">
      
      <!-- Search Widget -->
      <div class="sidebar-widget">
        <h3 style="font-size: 1rem; font-weight: 800; margin-bottom: 12px; color: var(--primary);">Search Sitemap</h3>
        <div class="search-input-group">
          <input type="text" id="sitemapSearchInput" placeholder="Filter pages or topics..." onkeyup="filterSitemap()">
          <button type="button">GO</button>
        </div>
      </div>

      <!-- Categories Cloud -->
      <div class="sidebar-widget">
        <h3 style="font-size: 1rem; font-weight: 800; margin-bottom: 8px; color: var(--primary); text-align: center;">Categories</h3>
        <div class="category-pills">
          <a href="/pages/first_home_buyers.html" class="category-pill">First Home Buyers</a>
          <a href="/pages/refinancing.html" class="category-pill">Refinancing</a>
          <a href="/pages/investment_loans.html" class="category-pill">Property Investment</a>
          <a href="/calculators.html" class="category-pill">Calculators</a>
          <a href="/pages/loans/self-employed-alt-doc-loans.html" class="category-pill">Self-Employed</a>
          <a href="/pages/business_finance.html" class="category-pill">SMSF Loans</a>
          <a href="/pages/loans/ndis-sda-property-finance.html" class="category-pill">NDIS SDA Finance</a>
          <a href="/locations.html" class="category-pill">State Guides</a>
          <a href="/pages/blog.html" class="category-pill">RBA Rate Updates</a>
        </div>
      </div>

      <!-- Quick Question Form (Image 1 Style) -->
      <div class="sidebar-widget">
        <h3 style="font-size: 1.1rem; font-weight: 900; margin-bottom: 16px; color: var(--primary); text-align: center; border-bottom: 2px solid var(--slate-100); padding-bottom: 8px;">Questions?</h3>
        <form class="quick-form" onsubmit="event.preventDefault(); alert('Thank you! Our accredited MFAA broker team will contact you shortly.');">
          <input type="text" placeholder="Your Name..." required>
          <input type="email" placeholder="Your Email..." required>
          <input type="text" placeholder="Question Title...">
          <textarea rows="3" placeholder="Your Question or Scenario..."></textarea>
          <button type="submit">Submit Question</button>
        </form>
        <div style="margin-top: 16px; text-align: center;">
          <span style="font-size: 0.8rem; color: #64748B;">Prefer direct phone advice?</span>
          <div style="font-size: 1.1rem; font-weight: 900; color: var(--accent); margin-top: 4px;">📞 1300 050 099</div>
        </div>
      </div>

    </aside>

  </main>

  <footer style="background:#0F172A; color:#E2E8F0; padding:40px 20px; text-align:center; font-size:0.88rem;">
    <div style="max-width:1240px; margin:0 auto; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:20px;">
      <div>&copy; 2026 EZ Mortgage Broker (ABN 28 657 661 615). All Rights Reserved.</div>
      <div style="display:flex; gap:16px;">
        <a href="/sitemap.html" style="color:#FFDC4A; font-weight:700;">HTML Sitemap</a>
        <a href="/privacy-policy.html" style="color:#93C5FD;">Privacy Policy</a>
        <a href="/terms-of-use.html" style="color:#93C5FD;">Terms of Use</a>
      </div>
    </div>
  </footer>

  <script>
    function filterSitemap() {{
      const query = document.getElementById('sitemapSearchInput').value.toLowerCase();
      const listItems = document.querySelectorAll('#sitemapTree li');
      listItems.forEach(li => {{
        const text = li.textContent.toLowerCase();
        if (text.includes(query) || query === '') {{
          li.style.display = '';
        }} else {{
          li.style.display = 'none';
        }}
      }});
    }}
  </script>
</body>
</html>
"""
    with open(os.path.join(EZ_MORTGAGE_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(sitemap_html)
    with open(os.path.join(EZ_MORTGAGE_DIR, "public", "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(sitemap_html)
    print("✅ Created ezmortgagebroker.com.au/sitemap.html")

# ==============================================================================
# 2. BUILD EZ CONSULTANTS (src/pages/Sitemap.jsx)
# ==============================================================================
def build_ezconsultants_sitemap():
    sitemap_jsx = """import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, Sparkles, Mail, Phone, ArrowRight, Compass, ShieldCheck } from 'lucide-react';

export default function Sitemap() {
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    { title: 'Salesforce Consulting', link: '/services' },
    { title: 'Agentforce & AI', link: '/services' },
    { title: 'Data Cloud & Zero-Copy', link: '/services' },
    { title: 'AppExchange Apps', link: '/solutions' },
    { title: 'buy.nsw Government', link: '/services' },
    { title: 'Market Insights', link: '/blog' },
    { title: 'Client Case Studies', link: '/resources' }
  ];

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 py-12 px-4 sm:px-8 font-sans">
      <div className="max-w-7xl mx-auto">
        
        {/* Header Hero */}
        <div className="bg-gradient-to-br from-[#0A2540] via-[#0F172A] to-[#1E293B] text-white p-8 sm:p-12 rounded-3xl mb-12 shadow-xl border border-cyan-500/20">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 text-cyan-400 font-bold text-xs uppercase tracking-wider mb-4">
            <Compass className="w-4 h-4" />
            Website Directory &amp; Navigation Tree
          </div>
          <h1 className="text-3xl sm:text-5xl font-black tracking-tight mb-4 text-white">
            Ez Consultants Sitemap
          </h1>
          <p className="text-slate-300 max-w-2xl text-base sm:text-lg">
            Complete structural overview of all Salesforce professional services, cloud solutions, government advisory frameworks, and market research articles.
          </p>
        </div>

        {/* 2-Column Content Layout (Image 1 Style) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          
          {/* Left Column: Interactive Tree (Col 8) */}
          <div className="lg:col-span-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 sm:p-10 shadow-sm">
            <h2 className="text-2xl font-black text-slate-900 dark:text-white mb-2">Sitemap</h2>
            <p className="text-slate-500 dark:text-slate-400 text-sm mb-8">Browse through the pages on our site below.</p>

            <div className="space-y-8 text-sm">
              
              {/* Section 1: Main Pages */}
              <div>
                <Link to="/" className="text-lg font-black text-cyan-700 dark:text-cyan-400 hover:underline">
                  Home Page
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100 dark:border-slate-800">
                  <li><Link to="/about-us" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">About Ez Consultants &amp; Certified Australian Team</Link></li>
                  <li><Link to="/contact-us" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Contact Us &amp; Discovery Session Booking</Link></li>
                </ul>
              </div>

              {/* Section 2: Core Salesforce Services */}
              <div>
                <Link to="/services" className="text-lg font-black text-cyan-700 dark:text-cyan-400 hover:underline">
                  Salesforce Professional Services &amp; Architecture
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100 dark:border-slate-800">
                  <li><Link to="/services#consulting" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Salesforce Advisory &amp; Architecture Strategy</Link></li>
                  <li><Link to="/services#agentforce" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Agentforce Autonomous AI Deployment &amp; Trust Layer</Link></li>
                  <li><Link to="/services#analytics" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Data Cloud Zero-Copy Integration (Snowflake/BigQuery)</Link></li>
                  <li><Link to="/services#integration" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">MuleSoft &amp; Boomi Enterprise Middleware</Link></li>
                  <li><Link to="/services#managed" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Managed Services &amp; 24/7 DevOps Support</Link></li>
                </ul>
              </div>

              {/* Section 3: AppExchange & Products */}
              <div>
                <Link to="/solutions" className="text-lg font-black text-cyan-700 dark:text-cyan-400 hover:underline">
                  AppExchange Solutions &amp; Accelerators
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100 dark:border-slate-800">
                  <li><Link to="/solutions" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Salesforce eSignatures LWC Native Integration</Link></li>
                  <li><Link to="/solutions" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Industry Cloud Accelerators for Financial &amp; NDIS</Link></li>
                </ul>
              </div>

              {/* Section 4: Public Sector */}
              <div>
                <Link to="/services" className="text-lg font-black text-cyan-700 dark:text-cyan-400 hover:underline">
                  Public Sector &amp; NSW Government (buy.nsw)
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100 dark:border-slate-800">
                  <li><a href="https://buy.nsw.gov.au/supplier/profile/180179" target="_blank" rel="noopener noreferrer" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">buy.nsw Approved Supplier Profile (ID: 180179) ↗</a></li>
                </ul>
              </div>

              {/* Section 5: Blog & Research */}
              <div>
                <Link to="/blog" className="text-lg font-black text-cyan-700 dark:text-cyan-400 hover:underline">
                  Market Insights &amp; Engineering Research
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100 dark:border-slate-800">
                  <li><Link to="/blog" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Latest Salesforce Release Analyses &amp; Cloud Telemetry</Link></li>
                </ul>
              </div>

              {/* Section 6: Machine Sitemaps */}
              <div>
                <span className="text-lg font-black text-slate-900 dark:text-white">
                  Technical XML &amp; Machine Feeds
                </span>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100 dark:border-slate-800">
                  <li><a href="/sitemap.xml" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">XML Search Sitemap (sitemap.xml)</a></li>
                  <li><a href="/sitemap-news.xml" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Google News XML Sitemap (sitemap-news.xml)</a></li>
                  <li><a href="/sitemap_index.xml" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">Master Sitemap Index (sitemap_index.xml)</a></li>
                  <li><a href="/feed.xml" className="text-slate-700 dark:text-slate-300 hover:text-cyan-600">RSS 2.0 Feed (feed.xml)</a></li>
                </ul>
              </div>

            </div>
          </div>

          {/* Right Column: Sidebar (Col 4 - Image 1 Style) */}
          <div className="lg:col-span-4 space-y-6">
            
            {/* Search Widget */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider mb-3">Search the site...</h3>
              <div className="flex rounded-xl overflow-hidden border-2 border-slate-200 dark:border-slate-700">
                <input
                  type="text"
                  placeholder="Type to search..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="flex-grow px-3.5 py-2.5 bg-transparent text-sm focus:outline-none dark:text-white"
                />
                <button className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold px-4 text-xs uppercase tracking-wider">
                  GO
                </button>
              </div>
            </div>

            {/* Categories Cloud Widget */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm text-center">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider mb-4">Categories</h3>
              <div className="flex flex-wrap gap-2 justify-center">
                {categories.map((c, i) => (
                  <Link
                    key={i}
                    to={c.link}
                    className="px-3 py-1.5 rounded-lg bg-cyan-700 hover:bg-cyan-600 text-white text-xs font-semibold transition-transform hover:-translate-y-0.5"
                  >
                    {c.title}
                  </Link>
                ))}
              </div>
            </div>

            {/* Questions Form Widget (Image 1 Style) */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
              <h3 className="text-base font-black text-slate-900 dark:text-white text-center pb-3 border-b border-slate-100 dark:border-slate-800 mb-4">
                Questions?
              </h3>
              <form className="space-y-3" onSubmit={(e) => { e.preventDefault(); alert('Thank you! Our Salesforce architects will contact you shortly.'); }}>
                <input
                  type="text"
                  placeholder="Your Name..."
                  required
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white focus:outline-none"
                />
                <input
                  type="email"
                  placeholder="Your Email..."
                  required
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white focus:outline-none"
                />
                <input
                  type="text"
                  placeholder="Question Title / Salesforce Scope..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white focus:outline-none"
                />
                <textarea
                  rows="3"
                  placeholder="Your Question..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white focus:outline-none"
                ></textarea>
                <button
                  type="submit"
                  className="w-full py-3 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-xl text-xs uppercase tracking-wider shadow-md"
                >
                  Submit Question
                </button>
              </form>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
"""
    with open(os.path.join(EZ_CONSULTANTS_DIR, "src", "pages", "Sitemap.jsx"), "w", encoding="utf-8") as f:
        f.write(sitemap_jsx)
    print("✅ Created ezconsultants.com.au/src/pages/Sitemap.jsx")

# ==============================================================================
# 3. BUILD PRO CRM (src/pages/Sitemap.jsx)
# ==============================================================================
def build_procrm_sitemap():
    sitemap_jsx = """import React, { useState } from "react";
import { Link } from "react-router-dom";

export default function Sitemap() {
  const [searchTerm, setSearchTerm] = useState("");

  const categories = [
    { title: "Enterprise CRM", link: "/" },
    { title: "Cybersecurity & ASD", link: "/cyber-security" },
    { title: "Compliance & CPS 234", link: "/compliance" },
    { title: "Cyber Insurance", link: "/cyber-insurance" },
    { title: "NDIS Care CRM", link: "/ndis-crm" },
    { title: "Intelligence Blog", link: "/blog" },
    { title: "Trust & Security", link: "/trust" }
  ];

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-8 font-sans text-slate-900">
      <div className="max-w-7xl mx-auto">
        
        {/* Banner */}
        <div className="bg-gradient-to-br from-[#084582] via-[#0F172A] to-[#1E293B] text-white p-8 sm:p-12 rounded-3xl mb-12 shadow-xl border border-blue-400/20">
          <span className="inline-block px-3.5 py-1.5 rounded-full bg-blue-500/20 text-blue-300 font-bold text-xs uppercase tracking-wider mb-4 border border-blue-400/30">
            Platform Architecture &amp; Sitemap
          </span>
          <h1 className="text-3xl sm:text-5xl font-black tracking-tight mb-4 text-white">
            PRO CRM HTML Sitemap
          </h1>
          <p className="text-blue-100 max-w-2xl text-base sm:text-lg">
            Browse through all enterprise CRM modules, cybersecurity services, APRA compliance portals, and real-time threat intelligence advisories.
          </p>
        </div>

        {/* 2-Column Content Layout (Image 1 Style) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          
          {/* Left Column: Interactive Tree */}
          <div className="lg:col-span-8 bg-white border border-slate-200 rounded-3xl p-8 sm:p-10 shadow-sm">
            <h2 className="text-2xl font-black text-slate-900 mb-2">Sitemap</h2>
            <p className="text-slate-500 text-sm mb-8">Browse through the pages on our platform below.</p>

            <div className="space-y-8 text-sm">
              
              {/* Section 1: Main Platform */}
              <div>
                <Link to="/" className="text-lg font-black text-[#084582] hover:underline">
                  Home Page &amp; Platform Overview
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/trust" className="text-slate-700 hover:text-[#084582]">Trust &amp; Sovereign Security Architecture</Link></li>
                  <li><Link to="/security" className="text-slate-700 hover:text-[#084582]">Essential Eight Level 3 Alignment</Link></li>
                </ul>
              </div>

              {/* Section 2: Cyber Security & Advisory */}
              <div>
                <Link to="/cyber-security" className="text-lg font-black text-[#084582] hover:underline">
                  Cybersecurity Services &amp; Defence
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/penetration-testing" className="text-slate-700 hover:text-[#084582]">Enterprise Penetration Testing &amp; Vulnerability Scanning</Link></li>
                  <li><Link to="/security-assessment" className="text-slate-700 hover:text-[#084582]">ASD Essential Eight Maturity Assessments</Link></li>
                  <li><Link to="/managed-security" className="text-slate-700 hover:text-[#084582]">24/7 Managed SOC &amp; Threat Telemetry</Link></li>
                  <li><Link to="/incident-response" className="text-slate-700 hover:text-[#084582]">Incident Response &amp; Breach Containment</Link></li>
                </ul>
              </div>

              {/* Section 3: Compliance & Insurance */}
              <div>
                <Link to="/compliance" className="text-lg font-black text-[#084582] hover:underline">
                  Regulatory Compliance &amp; Cyber Insurance
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/compliance" className="text-slate-700 hover:text-[#084582]">APRA CPS 234 &amp; ISO 27001 Readiness</Link></li>
                  <li><Link to="/cyber-insurance" className="text-slate-700 hover:text-[#084582]">Cyber Liability Insurance Gap Assessment</Link></li>
                </ul>
              </div>

              {/* Section 4: NDIS Healthcare CRM */}
              <div>
                <Link to="/ndis-crm" className="text-lg font-black text-[#084582] hover:underline">
                  Healthcare &amp; NDIS Participant CRM
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/ndis-crm" className="text-slate-700 hover:text-[#084582]">SCHADS Award Roster Costing &amp; PACE API Integration</Link></li>
                </ul>
              </div>

              {/* Section 5: Blog & Research */}
              <div>
                <Link to="/blog" className="text-lg font-black text-[#084582] hover:underline">
                  Threat Intelligence &amp; Newsroom
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/blog" className="text-slate-700 hover:text-[#084582]">ASD ACSC Alerts &amp; Zero-Day Exploit Telemetry</Link></li>
                </ul>
              </div>

              {/* Section 6: Legal & XML */}
              <div>
                <span className="text-lg font-black text-slate-900">
                  Legal &amp; Machine Feeds
                </span>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/privacy" className="text-slate-700 hover:text-[#084582]">Privacy Policy</Link></li>
                  <li><Link to="/terms" className="text-slate-700 hover:text-[#084582]">Terms of Service</Link></li>
                  <li><Link to="/cookies" className="text-slate-700 hover:text-[#084582]">Cookie Policy</Link></li>
                  <li><a href="/sitemap.xml" className="text-slate-700 hover:text-[#084582]">XML Search Sitemap (sitemap.xml)</a></li>
                  <li><a href="/sitemap-news.xml" className="text-slate-700 hover:text-[#084582]">Google News XML Sitemap (sitemap-news.xml)</a></li>
                  <li><a href="/sitemap_index.xml" className="text-slate-700 hover:text-[#084582]">Master Sitemap Index (sitemap_index.xml)</a></li>
                </ul>
              </div>

            </div>
          </div>

          {/* Right Column: Sidebar */}
          <div className="lg:col-span-4 space-y-6">
            
            {/* Search Widget */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-3">Search PRO CRM...</h3>
              <div className="flex rounded-xl overflow-hidden border-2 border-slate-200">
                <input
                  type="text"
                  placeholder="Search articles or solutions..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="flex-grow px-3.5 py-2.5 bg-transparent text-sm focus:outline-none"
                />
                <button className="bg-[#084582] hover:bg-[#063360] text-white font-bold px-4 text-xs uppercase tracking-wider">
                  GO
                </button>
              </div>
            </div>

            {/* Categories Cloud */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm text-center">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">Categories</h3>
              <div className="flex flex-wrap gap-2 justify-center">
                {categories.map((c, i) => (
                  <Link
                    key={i}
                    to={c.link}
                    className="px-3 py-1.5 rounded-lg bg-[#084582] hover:bg-[#063360] text-white text-xs font-semibold transition-transform hover:-translate-y-0.5"
                  >
                    {c.title}
                  </Link>
                ))}
              </div>
            </div>

            {/* Questions Form */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
              <h3 className="text-base font-black text-slate-900 text-center pb-3 border-b border-slate-100 mb-4">
                Questions?
              </h3>
              <form className="space-y-3" onSubmit={(e) => { e.preventDefault(); alert('Thank you! Our Cyber & CRM architects will contact you.'); }}>
                <input type="text" placeholder="Your Name..." required className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:outline-none" />
                <input type="email" placeholder="Your Email..." required className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:outline-none" />
                <input type="text" placeholder="Subject / Service Requirement..." className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:outline-none" />
                <textarea rows="3" placeholder="Your Question..." className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:outline-none"></textarea>
                <button type="submit" className="w-full py-3 bg-[#084582] hover:bg-[#063360] text-white font-bold rounded-xl text-xs uppercase tracking-wider shadow-md">
                  Submit Question
                </button>
              </form>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
"""
    with open(os.path.join(PROCRM_DIR, "src", "pages", "Sitemap.jsx"), "w", encoding="utf-8") as f:
        f.write(sitemap_jsx)
    print("✅ Created procrm-app/src/pages/Sitemap.jsx")

# ==============================================================================
# 4. BUILD FINNOVA (sitemap.html)
# ==============================================================================
def build_finnova_sitemap():
    posts_path = os.path.join(FINNOVA_DIR, "posts.json")
    posts = []
    if os.path.exists(posts_path):
        with open(posts_path, "r", encoding="utf-8") as f:
            posts = json.load(f)

    blog_links_html = ""
    for p in posts:
        slug = p.get("id", "")
        title = p.get("title", "")
        blog_links_html += f'                <li><a href="/en_AU.html#{slug}">{title}</a></li>\n'

    sitemap_html = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sitemap | Finnova Community Hub</title>
  <link rel="canonical" href="https://finnova.org.au/sitemap.html">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', sans-serif; background: #FAFAFA; color: #0F172A; margin: 0; padding: 0; }}
    .header {{ background: #0A2540; color: white; padding: 40px 20px; }}
    .container {{ max-width: 1200px; margin: 40px auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 320px; gap: 40px; }}
    @media(max-width: 800px) {{ .container {{ grid-template-columns: 1fr; }} }}
    .tree {{ background: white; border: 1px solid #E2E8F0; border-radius: 16px; padding: 32px; }}
    .tree ul {{ list-style: none; padding-left: 20px; }}
    .tree > ul {{ padding-left: 0; }}
    .tree li {{ margin: 8px 0; }}
    .tree a {{ color: #084582; text-decoration: none; font-weight: 500; }}
    .tree a:hover {{ text-decoration: underline; }}
    .sidebar-card {{ background: white; border: 1px solid #E2E8F0; border-radius: 16px; padding: 20px; margin-bottom: 20px; }}
  </style>
</head>
<body>
  <div class="header">
    <div style="max-width:1200px; margin:0 auto;">
      <h1 style="margin:0 0 8px;">Finnova Community Hub Sitemap</h1>
      <p style="margin:0; color:#E2E8F0;">Complete index of all digital literacy programs, senior anti-scam clinics, and guides.</p>
    </div>
  </div>

  <div class="container">
    <div class="tree">
      <h2>Website Directory</h2>
      <ul>
        <li><a href="/en_AU.html">English Portal (en_AU.html)</a></li>
        <li><a href="/hi_IN.html">Hindi Portal (हिंदी)</a></li>
        <li><a href="/pa_IN.html">Punjabi Portal (ਪੰਜਾਬੀ)</a></li>
        <li><a href="/ar_AE.html">Arabic Portal (العربية)</a></li>
        <li><a href="/es_ES.html">Spanish Portal (Español)</a></li>
        <li><a href="/vi_VN.html">Vietnamese Portal (Tiếng Việt)</a></li>
        <li><a href="/zh_CN.html">Mandarin Portal (中文)</a></li>
        <li>
          <strong>Community Intelligence &amp; Advisories</strong>
          <ul>
{blog_links_html}
          </ul>
        </li>
        <li>
          <strong>Feeds &amp; Technical Specifications</strong>
          <ul>
            <li><a href="/sitemap.xml">XML Sitemap (sitemap.xml)</a></li>
            <li><a href="/sitemap-news.xml">Google News Sitemap (sitemap-news.xml)</a></li>
            <li><a href="/sitemap_index.xml">Master Sitemap Index (sitemap_index.xml)</a></li>
            <li><a href="/feed.xml">RSS Feed (feed.xml)</a></li>
          </ul>
        </li>
      </ul>
    </div>

    <div>
      <div class="sidebar-card">
        <h3>Categories</h3>
        <p style="font-size:0.9rem; color:#64748B;">• Cyber Safety &amp; Scams<br>• myGov &amp; Digital Literacy<br>• Youth Mentorship</p>
      </div>
      <div class="sidebar-card">
        <h3>Contact Finnova</h3>
        <p style="font-size:0.85rem; color:#475569;">Email: community@finnova.org.au<br>Location: Wyndham, Victoria</p>
      </div>
    </div>
  </div>
</body>
</html>
"""
    with open(os.path.join(FINNOVA_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(sitemap_html)
    with open(os.path.join(FINNOVA_DIR, "public", "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(sitemap_html)
    print("✅ Created finnova.org.au/sitemap.html")

# ==============================================================================
# 5. BUILD EZ SIGNATURE (src/pages/Sitemap.jsx)
# ==============================================================================
def build_ezsignature_sitemap():
    sitemap_jsx = """import React, { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Sitemap() {
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    { title: 'DocuSign Alternative', link: '/docusign-alternative' },
    { title: 'PandaDoc Alternative', link: '/pandadoc-alternative' },
    { title: 'Pricing & Value', link: '/pricing' },
    { title: 'Developer API & Webhooks', link: '/developer' },
    { title: 'Tamper-Proof Audit Trail', link: '/audit-trail' },
    { title: 'Document Templates', link: '/templates' },
    { title: 'Sign PDF Online Free', link: '/sign-pdf-online' }
  ];

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-8 font-sans text-slate-900">
      <div className="max-w-7xl mx-auto">
        
        {/* Banner */}
        <div className="bg-gradient-to-br from-[#1E1B4B] via-[#0F172A] to-[#0A2540] text-white p-8 sm:p-12 rounded-3xl mb-12 shadow-xl border border-indigo-500/20">
          <span className="inline-block px-3.5 py-1.5 rounded-full bg-indigo-500/20 text-indigo-300 font-bold text-xs uppercase tracking-wider mb-4 border border-indigo-400/30">
            Platform Directory &amp; Navigation Tree
          </span>
          <h1 className="text-3xl sm:text-5xl font-black tracking-tight mb-4 text-white">
            EZ Signature HTML Sitemap
          </h1>
          <p className="text-indigo-100 max-w-2xl text-base sm:text-lg">
            Browse all electronic signature tools, developer REST APIs, legal compliance certifications, and DocuSign comparison guides.
          </p>
        </div>

        {/* 2-Column Content Layout (Image 1 Style) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          
          {/* Left Column: Interactive Tree */}
          <div className="lg:col-span-8 bg-white border border-slate-200 rounded-3xl p-8 sm:p-10 shadow-sm">
            <h2 className="text-2xl font-black text-slate-900 mb-2">Sitemap</h2>
            <p className="text-slate-500 text-sm mb-8">Browse through the pages on our platform below.</p>

            <div className="space-y-8 text-sm">
              
              <div>
                <Link to="/" className="text-lg font-black text-indigo-700 hover:underline">
                  Home &amp; Digital Signature Platform
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/pricing" className="text-slate-700 hover:text-indigo-600">Fair Usage Pricing &amp; Unlimited Plans</Link></li>
                  <li><Link to="/non-profits" className="text-slate-700 hover:text-indigo-600">Non-Profit &amp; Charity Pricing (50% Off)</Link></li>
                  <li><Link to="/about" className="text-slate-700 hover:text-indigo-600">About EZ Signature &amp; Cryptographic Standards</Link></li>
                </ul>
              </div>

              <div>
                <Link to="/docusign-alternative" className="text-lg font-black text-indigo-700 hover:underline">
                  Competitor Alternatives &amp; Cost Comparisons
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/docusign-alternative" className="text-slate-700 hover:text-indigo-600">DocuSign Alternative (No Envelope Limits)</Link></li>
                  <li><Link to="/pandadoc-alternative" className="text-slate-700 hover:text-indigo-600">PandaDoc Alternative</Link></li>
                  <li><Link to="/signnow-alternative" className="text-slate-700 hover:text-indigo-600">SignNow Alternative</Link></li>
                  <li><Link to="/best-esignature-software-alternatives" className="text-slate-700 hover:text-indigo-600">Best eSignature Software Guide 2026</Link></li>
                </ul>
              </div>

              <div>
                <Link to="/developer" className="text-lg font-black text-indigo-700 hover:underline">
                  Developer Hub &amp; Integrations
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/developer" className="text-slate-700 hover:text-indigo-600">REST API Reference &amp; Webhook Signatures</Link></li>
                  <li><Link to="/integrations" className="text-slate-700 hover:text-indigo-600">Salesforce, Zapier &amp; Custom Webhooks</Link></li>
                  <li><Link to="/audit-trail" className="text-slate-700 hover:text-indigo-600">Court-Admissible Forensic Audit Trail</Link></li>
                  <li><Link to="/security" className="text-slate-700 hover:text-indigo-600">Post-Quantum Cryptography (NIST PQC) Security</Link></li>
                </ul>
              </div>

              <div>
                <Link to="/templates" className="text-lg font-black text-indigo-700 hover:underline">
                  Legal &amp; Business Document Templates
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/templates/nda" className="text-slate-700 hover:text-indigo-600">Standard Non-Disclosure Agreement (NDA)</Link></li>
                  <li><Link to="/templates/employment-contract" className="text-slate-700 hover:text-indigo-600">Employment Contract Agreement</Link></li>
                  <li><Link to="/templates/consulting-agreement" className="text-slate-700 hover:text-indigo-600">Professional Consulting Agreement</Link></li>
                  <li><Link to="/templates/commercial-lease" className="text-slate-700 hover:text-indigo-600">Commercial Property Lease Template</Link></li>
                </ul>
              </div>

              <div>
                <Link to="/blog" className="text-lg font-black text-indigo-700 hover:underline">
                  Knowledge Base &amp; Legal Guides
                </Link>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><Link to="/blog" className="text-slate-700 hover:text-indigo-600">Australian Electronic Transactions Act 1999 Legality</Link></li>
                </ul>
              </div>

              <div>
                <span className="text-lg font-black text-slate-900">
                  Feeds &amp; Technical Sitemaps
                </span>
                <ul className="mt-3 pl-6 space-y-2 border-l-2 border-slate-100">
                  <li><a href="/sitemap.xml" className="text-slate-700 hover:text-indigo-600">XML Search Sitemap (sitemap.xml)</a></li>
                  <li><a href="/sitemap-news.xml" className="text-slate-700 hover:text-indigo-600">Google News XML Sitemap (sitemap-news.xml)</a></li>
                  <li><a href="/sitemap_index.xml" className="text-slate-700 hover:text-indigo-600">Master Sitemap Index (sitemap_index.xml)</a></li>
                  <li><a href="/rss.xml" className="text-slate-700 hover:text-indigo-600">RSS Feed (rss.xml)</a></li>
                </ul>
              </div>

            </div>
          </div>

          {/* Right Column: Sidebar */}
          <div className="lg:col-span-4 space-y-6">
            
            {/* Search Widget */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-3">Search ezSignature...</h3>
              <div className="flex rounded-xl overflow-hidden border-2 border-slate-200">
                <input
                  type="text"
                  placeholder="Search templates or tools..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="flex-grow px-3.5 py-2.5 bg-transparent text-sm focus:outline-none"
                />
                <button className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-4 text-xs uppercase tracking-wider">
                  GO
                </button>
              </div>
            </div>

            {/* Categories Cloud */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm text-center">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">Categories</h3>
              <div className="flex flex-wrap gap-2 justify-center">
                {categories.map((c, i) => (
                  <Link
                    key={i}
                    to={c.link}
                    className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition-transform hover:-translate-y-0.5"
                  >
                    {c.title}
                  </Link>
                ))}
              </div>
            </div>

            {/* Questions Form */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
              <h3 className="text-base font-black text-slate-900 text-center pb-3 border-b border-slate-100 mb-4">
                Questions?
              </h3>
              <form className="space-y-3" onSubmit={(e) => { e.preventDefault(); alert('Thank you! Our eSignature engineers will reach out.'); }}>
                <input type="text" placeholder="Your Name..." required className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:outline-none" />
                <input type="email" placeholder="Your Email..." required className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:outline-none" />
                <input type="text" placeholder="Topic / API Question..." className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:outline-none" />
                <textarea rows="3" placeholder="Your Question..." className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:outline-none"></textarea>
                <button type="submit" className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl text-xs uppercase tracking-wider shadow-md">
                  Submit Question
                </button>
              </form>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
"""
    with open(os.path.join(EZSIGNATURE_DIR, "src", "pages", "Sitemap.jsx"), "w", encoding="utf-8") as f:
        f.write(sitemap_jsx)
    print("✅ Created ezsignature.com/src/pages/Sitemap.jsx")

if __name__ == "__main__":
    build_ezmortgagebroker_sitemap()
    build_ezconsultants_sitemap()
    build_procrm_sitemap()
    build_finnova_sitemap()
    build_ezsignature_sitemap()
