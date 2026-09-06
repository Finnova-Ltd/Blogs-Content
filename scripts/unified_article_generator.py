#!/usr/bin/env python3
"""
Unified AI Article Generator Engine (Cloud-Backed: DeepSeek + Gemini Flash)
FINNOVA / EZMORTGAGE BROKERAGE • CONTENT EXCELLENCE PIPELINE

Multi-tier Cloud AI Architecture (0 MB Local Mac RAM, $0.00/Month Cost):
- Tier 1: deepseek-v4-flash:cloud (via Ollama Cloud)
- Tier 2: gemini-3.6-flash (via Google AI Studio Free Tier)

Generates 450-600 word authentic, value-dense Australian financial articles
complying with all repository agent rules, MFAA Best Interests Duty (BID),
and the Image 3 Standard layout (1-row Call Us/Book Consult buttons).
"""

import os
import re
import sys
import json
import argparse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime, timezone
from dotenv import load_dotenv

AEST = ZoneInfo("Australia/Melbourne")
BASE_DIR = Path(__file__).resolve().parent.parent
EZ_DIR = Path("/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker")
BLOG_DIR = EZ_DIR / "pages" / "blog"
POSTS_FILE = BASE_DIR / "posts.json"
EZ_POSTS_FILE = EZ_DIR / "posts.json"

load_dotenv(BASE_DIR / ".env")

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEEPSEEK_MODEL = "deepseek-v4-flash:cloud"
GEMINI_KEYS = [
    os.getenv("GEMINI_KEY_FREE_1"),
    os.getenv("GEMINI_KEY_FREE_2"),
    os.getenv("GEMINI_KEY_FREE_3"),
    os.getenv("GEMINI_API_KEY")
]
GEMINI_KEYS = [k for k in GEMINI_KEYS if k]

def get_current_date_str():
    return datetime.now(timezone.utc).astimezone(AEST).strftime("%d-%b-%Y")

def query_deepseek_cloud(prompt: str) -> str:
    payload = {
        "model": DEEPSEEK_MODEL,
        "prompt": prompt,
        "stream": False
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=40) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res.get("response", "").strip()

def query_gemini_flash(prompt: str) -> str:
    for key in GEMINI_KEYS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            print(f"Gemini key rotation notice: {e}")
            continue
    raise RuntimeError("All Gemini API keys exhausted.")

def generate_article_content(headline: str) -> dict:
    prompt = f"""
You are a senior Australian mortgage analyst and MFAA-accredited finance writer for EZ Mortgage Broker in Melbourne.
Write an authentic, value-dense 450-word financial analysis article based on this headline:
'{headline}'

Requirements:
1. Minimum 400-500 words across 4 distinct sections.
2. NO generic boilerplate, no empty marketing repetition.
3. Provide realistic rate calculations on a $650,000 mortgage (e.g. comparing a competitive 5.89% variable rate to a 6.45% major bank rate, saving $238/mo or $2,856/year).
4. Focus on Melbourne growth corridors (e.g. Western corridor: Tarneit, Point Cook; Northern corridor: Craigieburn; Bayside or Eastern suburbs).
5. Address Victoria's $10,000 First Home Owner Grant and stamp duty exemptions up to $600,000.
6. Statutory Best Interests Duty (BID) advisory for prospective buyers and refinancers.

Output strictly valid JSON with these keys:
"summary": "1-2 sentence executive summary (max 35 words)",
"market_analysis": "2-3 comprehensive paragraphs examining macroeconomic context, RBA policy, and borrower debt serviceability (approx 180 words)",
"rate_repayment_math": "Mathematical comparison table text and repayment breakdown (approx 120 words)",
"strategic_advisory": "MFAA Principal Broker recommendations under Best Interests Duty (approx 100 words)"
Do NOT wrap in markdown code blocks. Output JSON only.
"""
    # Try Tier 1: DeepSeek Cloud
    try:
        raw = query_deepseek_cloud(prompt)
        clean = raw.strip()
        if clean.startswith("```json"): clean = clean[7:]
        if clean.startswith("```"): clean = clean[3:]
        if clean.endswith("```"): clean = clean[:-3]
        return json.loads(clean.strip())
    except Exception as e:
        print(f"DeepSeek Cloud failed or offline ({e}). Falling back to Tier 2: Gemini 3.6 Flash...")
        raw = query_gemini_flash(prompt)
        clean = raw.strip()
        if clean.startswith("```json"): clean = clean[7:]
        if clean.startswith("```"): clean = clean[3:]
        if clean.endswith("```"): clean = clean[:-3]
        return json.loads(clean.strip())

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text[:75]

def render_article_html(slug: str, title: str, category: str, date_str: str, data: dict) -> str:
    summary = data.get("summary", "")
    market_analysis = data.get("market_analysis", "").replace("\n\n", "</p><p class='font-editorial' style='font-size:1.05rem; line-height:1.65; color:#334155; margin:14px 0 0;'>")
    rate_math = data.get("rate_repayment_math", "")
    advisory = data.get("strategic_advisory", "")

    html = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | EZ Mortgage Broker Melbourne</title>
  <meta name="description" content="{summary}">
  <link rel="canonical" href="https://ezmortgagebroker.com.au/pages/blog/{slug}.html">
  <link rel="stylesheet" href="/css/styles.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #F8FAFC; color: #0F172A; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }}
    .font-editorial {{ font-family: 'Lora', Georgia, serif; }}
    .article-hero-section {{ background: linear-gradient(135deg, #0A2540 0%, #061B2E 100%); color: #FFFFFF; padding: 48px 0 40px; border-bottom: 1px solid #1E293B; }}
    .article-hero-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
    .article-layout-grid {{ max-width: 1200px; margin: 40px auto 80px; padding: 0 24px; display: grid; grid-template-columns: 1fr 340px; gap: 40px; align-items: start; }}
    @media (max-width: 991px) {{ .article-layout-grid {{ grid-template-columns: 1fr; }} }}
    .content-box-body {{ background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 28px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(10,37,64,0.03); }}
    .content-box-advisory {{ background: #EFF6FF; border: 1.5px solid #BFDBFE; border-left: 5px solid #1D4ED8; border-radius: 16px; padding: 24px; margin-bottom: 24px; }}
  </style>
</head>
<body>

  <!-- Header Navigation -->
  <header style="background:#ffffff; border-bottom:1px solid #E2E8F0; position:sticky; top:0; z-index:1000;">
    <div style="max-width:1200px; margin:0 auto; padding:10px 20px; display:flex; justify-content:space-between; align-items:center;">
      <a href="/"><img width="160" height="40" src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" style="height:40px; width:auto; display:block;"></a>
      <nav style="display:flex; gap:22px; font-size:0.9rem; font-weight:700;">
        <a href="/" style="color:#0A2540; text-decoration:none;">Home</a>
        <a href="/#loan-solutions" style="color:#0A2540; text-decoration:none;">Home Loans</a>
        <a href="/locations.html" style="color:#0A2540; text-decoration:none;">Locations</a>
        <a href="/calculators.html" style="color:#0A2540; text-decoration:none;">Calculators</a>
        <a href="/pages/blog.html" style="color:#1D4ED8; text-decoration:none;">News</a>
        <a href="/#about" style="color:#0A2540; text-decoration:none;">About</a>
        <a href="/#contact" style="color:#0A2540; text-decoration:none;">Contact</a>
      </nav>
      <div style="display:flex; gap:10px; flex-shrink:0; white-space:nowrap;">
        <a href="tel:1300050099" style="padding:7px 15px; border:1.5px solid #0A2540; color:#0A2540; border-radius:6px; font-weight:700; text-decoration:none; font-size:0.82rem; white-space:nowrap;">Call Us</a>
        <a href="/#contact" style="padding:7px 16px; background:#1D4ED8; color:#ffffff; border-radius:6px; font-weight:700; text-decoration:none; font-size:0.82rem; white-space:nowrap;">Book Consult</a>
      </div>
    </div>
  </header>

  <!-- Hero Banner -->
  <section class="article-hero-section">
    <div class="article-hero-inner">
      <nav style="display:flex; align-items:center; gap:8px; font-size:0.78rem; font-weight:700; color:#93C5FD; margin-bottom:14px;">
        <a href="/" style="color:#BFDBFE; text-decoration:none;">Home</a>
        <span style="opacity:0.6;">/</span>
        <a href="/pages/blog.html" style="color:#BFDBFE; text-decoration:none;">News &amp; Insights</a>
        <span style="opacity:0.6;">/</span>
        <span style="color:#FFFFFF;">{category}</span>
      </nav>
      <div style="display:flex; gap:12px; align-items:center; margin-bottom:14px;">
        <span style="background:rgba(29,78,216,0.3); border:1px solid #3B82F6; color:#93C5FD; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:800; text-transform:uppercase;">{category}</span>
        <span style="font-size:0.78rem; color:#94A3B8;">Published: {date_str}</span>
        <span style="font-size:0.78rem; color:#94A3B8;">•</span>
        <span style="font-size:0.78rem; color:#94A3B8;">Author: R Bakshi (MFAA Accredited)</span>
      </div>
      <h1 style="font-size:clamp(1.8rem, 3.2vw, 2.6rem); font-weight:900; line-height:1.22; margin:0 0 16px; max-width:960px;">{title}</h1>
      <p class="font-editorial" style="font-size:1.15rem; line-height:1.6; color:#CBD5E1; max-width:880px; margin:0;">{summary}</p>
    </div>
  </section>

  <!-- Main Article Layout -->
  <main class="article-layout-grid">
    
    <!-- Left Column: Editorial Analysis -->
    <article>
      <!-- Section 1: Market Analysis -->
      <div class="content-box-body">
        <h2 style="font-size:1.25rem; font-weight:900; color:#0A2540; margin:0 0 14px;">1. Market Landscape &amp; Policy Context</h2>
        <p class="font-editorial" style="font-size:1.05rem; line-height:1.65; color:#334155; margin:0;">{market_analysis}</p>
      </div>

      <!-- Section 2: Rate & Repayment Differential -->
      <div class="content-box-body">
        <h2 style="font-size:1.25rem; font-weight:900; color:#0A2540; margin:0 0 14px;">2. Rate Spread &amp; Repayment Modeling</h2>
        <p class="font-editorial" style="font-size:1.05rem; line-height:1.65; color:#334155; margin:0 0 16px;">{rate_math}</p>
        <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:12px; padding:16px; font-size:0.85rem; color:#0F172A;">
          <strong>💡 Melbourne Borrower Benchmark:</strong> Comparing 30+ lenders frequently reveals variable rate discounts of 0.40% to 0.65% below major bank headline pricing, saving over $2,800 annually on standard $650k loans.
        </div>
      </div>

      <!-- Section 3: Strategic Broker Advisory -->
      <div class="content-box-advisory">
        <h2 style="font-size:1.25rem; font-weight:900; color:#1E3A8A; margin:0 0 12px;">3. MFAA Broker Advisory (Best Interests Duty)</h2>
        <p class="font-editorial" style="font-size:1.05rem; line-height:1.65; color:#1E3A8A; margin:0;">{advisory}</p>
      </div>
    </article>

    <!-- Right Column: Sticky Sidebar Card 1 & Card 2 (Image 3 Standard) -->
    <aside style="position:-webkit-sticky; position:sticky; top:90px; display:flex; flex-direction:column; gap:20px;">
      
      <!-- Card 1: Principal Broker Profile Card (Image 3 Exact Replication) -->
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; overflow:hidden; box-shadow:0 4px 14px rgba(10,37,64,0.06); text-align:center;">
        <div style="background: linear-gradient(135deg, rgba(8, 69, 130, 0.35) 0%, rgba(6, 40, 77, 0.55) 100%), url('/images/melbourne-bourke-street-header.webp') center/cover no-repeat; height:90px; position:relative; display:flex; justify-content:center;">
          <div style="position:absolute; bottom:-34px; width:68px; height:68px; border-radius:50%; border:3px solid #FFFFFF; overflow:hidden; background:#FFFFFF; box-shadow:0 4px 10px rgba(0,0,0,0.2);">
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
          <!-- 1-Row Action Grid -->
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; width:100%; margin-top:8px;">
            <a href="tel:1300050099" style="display:flex; align-items:center; justify-content:center; gap:4px; background:#00876C; color:#FFFFFF !important; font-weight:800; padding:9px 4px; border-radius:8px; text-decoration:none; font-size:0.78rem; white-space:nowrap; box-shadow:0 2px 6px rgba(0,135,108,0.2);">
              <span>📞 Call Us</span>
            </a>
            <a href="/#contact" style="display:flex; align-items:center; justify-content:center; background:#0A2540; color:#FFFFFF !important; font-weight:800; padding:9px 4px; border-radius:8px; text-decoration:none; font-size:0.78rem; white-space:nowrap;">
              📅 Book Consult
            </a>
          </div>
        </div>
      </div>

      <!-- Card 2: Highlights Accordion -->
      <div style="background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:18px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.03);">
        <div style="background:#990000; padding:10px 16px; color:#FFFFFF !important; display:flex; justify-content:space-between; align-items:center;">
          <h3 style="font-size:0.78rem; font-weight:900; text-transform:uppercase; margin:0; letter-spacing:0.04em; color:#FFFFFF !important;">Highlights</h3>
          <span style="font-size:0.68rem; font-weight:700; color:#FEE2E2 !important; text-transform:uppercase; letter-spacing:0.06em;">In this article</span>
        </div>
        <div style="padding:16px;">
          <div style="font-size:0.72rem; font-weight:700; color:#64748B; margin-bottom:12px;">— {date_str}</div>
          <div style="border-left:2px solid #E2E8F0; padding-left:14px; margin-left:4px; display:flex; flex-direction:column; gap:12px;">
            <div style="position:relative;">
              <span style="position:absolute; left:-19px; top:4px; width:8px; height:8px; border-radius:50%; background:#990000; border:2px solid #FFFFFF;"></span>
              <div style="font-size:0.68rem; font-weight:900; color:#990000; text-transform:uppercase;">01. RATE BUFFER</div>
              <div style="font-size:0.8rem; font-weight:700; color:#0F172A; line-height:1.2;">Serviceability &amp; Pricing</div>
            </div>
            <div style="position:relative;">
              <span style="position:absolute; left:-19px; top:4px; width:8px; height:8px; border-radius:50%; background:#990000; border:2px solid #FFFFFF;"></span>
              <div style="font-size:0.68rem; font-weight:900; color:#990000; text-transform:uppercase;">02. LOCAL CORRIDORS</div>
              <div style="font-size:0.8rem; font-weight:700; color:#0F172A; line-height:1.2;">Melbourne Suburbs</div>
            </div>
          </div>
        </div>
      </div>

    </aside>
  </main>

  <script src="/js/widget.js" defer></script>
</body>
</html>
"""
    return html

def publish_article(headline: str, category: str = "Home Loans"):
    date_str = get_current_date_str()
    slug = slugify(headline)
    print(f"[{date_str}] Generating rich financial article for: '{headline}'...")
    data = generate_article_content(headline)
    html_content = render_article_html(slug, headline, category, date_str, data)

    out_file = BLOG_DIR / f"{slug}.html"
    with open(out_file, "w", encoding="utf-8") as fp:
        fp.write(html_content)
    print(f"✅ Created: {out_file}")

    # Add to posts.json at the top
    post_item = {
        "slug": slug,
        "title": headline,
        "category": category,
        "date": date_str,
        "publishedDate": date_str,
        "excerpt": data.get("summary", ""),
        "content": data.get("summary", ""),
        "image": "/assets/luxury-home-refinance-hero-OeZc7gD4.webp",
        "url": f"/pages/blog/{slug}.html"
    }

    for p_file in [POSTS_FILE, EZ_POSTS_FILE]:
        if p_file.exists():
            with open(p_file, "r") as fp:
                posts = json.load(fp)
            # Remove any existing with same slug
            posts = [p for p in posts if p.get("slug") != slug]
            posts.insert(0, post_item)
            with open(p_file, "w") as fp:
                json.dump(posts, fp, indent=2)

    # Trigger blog hub sync
    os.system(f"python3 '{BASE_DIR}/scripts/sync_blog_hub.py'")
    print(f"🚀 Article '{headline}' published successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish deep analysis article using Cloud AI")
    parser.add_argument("--headline", type=str, default="Melbourne Property Market Defies High Rates as Buyers Pivot to Outer Corridors")
    parser.add_argument("--category", type=str, default="Home Loans")
    args = parser.parse_args()

    publish_article(args.headline, args.category)
