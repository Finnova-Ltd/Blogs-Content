#!/usr/bin/env python3
import os
import subprocess

EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
ROOT_404 = os.path.join(EZ_DIR, "404.html")
PUB_404 = os.path.join(EZ_DIR, "public", "404.html")

html_content = """<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>404 - Page Not Found | EZ Mortgage Broker</title>
  <meta name="description" content="Oops, the page you're trying to view isn't here. But you're still on the path to securing the lowest home loan rate and maximizing your borrowing power with EZ Mortgage Broker.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/calculators.css">
  
  <!-- Lottie Player for 404 Interactive Animation -->
  <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>

  <style>
    :root {
      --ez-navy: #084582;
      --ez-navy-dark: #052a50;
      --ez-blue-light: #f0f7ff;
      --ez-amber: #f59e0b;
      --ez-amber-hover: #d97706;
      --ez-teal: #00a884;
    }
    
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
      margin: 0;
      padding: 0;
    }

    /* Global Header */
    .top-nav {
      background: #ffffff;
      border-bottom: 1px solid #e2e8f0;
      position: sticky;
      top: 0;
      z-index: 1000;
    }
    .top-nav-inner {
      max-width: 1240px;
      margin: 0 auto;
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .logo-brand {
      display: flex;
      align-items: center;
      text-decoration: none;
    }
    .brand-logo-img {
      height: clamp(52px, 5.5vw, 68px);
      width: auto;
      max-width: 260px;
      display: inline-block;
      object-fit: contain;
    }
    .nav-links {
      display: flex;
      align-items: center;
      gap: 24px;
    }
    .nav-links a {
      color: #334155;
      text-decoration: none;
      font-size: 0.92rem;
      font-weight: 600;
      transition: color 0.15s ease;
    }
    .nav-links a:hover {
      color: var(--ez-navy);
    }
    .btn-consult-nav {
      background: var(--ez-navy);
      color: #ffffff !important;
      padding: 10px 22px;
      border-radius: 9999px;
      font-weight: 700;
      font-size: 0.85rem;
      transition: all 0.2s ease;
    }
    .btn-consult-nav:hover {
      background: var(--ez-navy-dark);
      transform: translateY(-1px);
    }

    /* Hero Section */
    .hero-404 {
      padding: 48px 24px 36px;
      text-align: center;
      background: radial-gradient(circle at 50% 10%, #e0f2fe 0%, #f8fafc 65%);
    }
    .hero-container {
      max-width: 860px;
      margin: 0 auto;
    }
    
    /* Lottie Animation Wrapper */
    .animation-wrapper {
      width: 260px;
      height: 220px;
      margin: 0 auto 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }
    .animation-wrapper lottie-player {
      width: 100%;
      height: 100%;
    }
    
    /* Fallback Floating SVG Animation in case player is loading */
    .floating-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #ffffff;
      color: var(--ez-navy);
      font-weight: 800;
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 8px 18px;
      border-radius: 9999px;
      margin-bottom: 20px;
      border: 1px solid #bae6fd;
      box-shadow: 0 4px 14px rgba(8, 69, 130, 0.06);
      animation: floatBadge 3s ease-in-out infinite;
    }
    @keyframes floatBadge {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-4px); }
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      background: #0284c7;
      border-radius: 50%;
      animation: pulseDot 1.5s ease-in-out infinite;
    }
    @keyframes pulseDot {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.5); opacity: 0.4; }
    }

    .headline-404 {
      font-size: clamp(2rem, 3.8vw, 2.75rem);
      font-weight: 900;
      color: var(--ez-navy);
      line-height: 1.2;
      letter-spacing: -0.03em;
      margin: 0 0 16px;
    }
    .subheadline-404 {
      font-size: clamp(1.2rem, 2.2vw, 1.55rem);
      font-weight: 800;
      color: #1e293b;
      line-height: 1.35;
      margin: 0 auto 16px;
      letter-spacing: -0.02em;
      max-width: 780px;
    }
    .desc-404 {
      font-size: 1.05rem;
      color: #475569;
      line-height: 1.6;
      max-width: 700px;
      margin: 0 auto 28px;
    }
    .hero-ctas {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      justify-content: center;
      margin-bottom: 24px;
    }
    .btn-primary-ez {
      background: #0284c7;
      color: #ffffff !important;
      padding: 14px 32px;
      border-radius: 12px;
      font-weight: 800;
      font-size: 1rem;
      text-decoration: none;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3);
      transition: all 0.2s ease;
    }
    .btn-primary-ez:hover {
      background: #0369a1;
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(2, 132, 199, 0.4);
    }
    .btn-outline-ez {
      background: #ffffff;
      color: var(--ez-navy) !important;
      border: 2px solid var(--ez-navy);
      padding: 14px 28px;
      border-radius: 12px;
      font-weight: 800;
      font-size: 1rem;
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .btn-outline-ez:hover {
      background: var(--ez-navy);
      color: #ffffff !important;
      transform: translateY(-2px);
    }

    /* Blog & Guides Preview Section (Exact Image 2 Match) */
    .guides-section {
      max-width: 1200px;
      margin: 20px auto 64px;
      padding: 0 24px;
      text-align: center;
    }
    .guides-eyebrow {
      font-size: 0.8rem;
      font-weight: 800;
      color: #0284c7;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 8px;
      display: block;
    }
    .guides-title {
      font-size: clamp(1.75rem, 3vw, 2.25rem);
      font-weight: 900;
      color: #0f172a;
      letter-spacing: -0.02em;
      margin: 0 0 10px;
    }
    .guides-desc {
      font-size: 1rem;
      color: #64748b;
      max-width: 650px;
      margin: 0 auto 36px;
      line-height: 1.5;
    }
    .guides-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      text-align: left;
    }
    @media (max-width: 960px) {
      .guides-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }
    @media (max-width: 640px) {
      .guides-grid {
        grid-template-columns: 1fr;
      }
      .nav-links {
        display: none;
      }
    }
    .guide-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
      display: flex;
      flex-direction: column;
      transition: all 0.25s ease;
    }
    .guide-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 30px rgba(8, 69, 130, 0.1);
      border-color: #cbd5e1;
    }
    .guide-img-wrap {
      position: relative;
      height: 180px;
      background: #e2e8f0;
      overflow: hidden;
    }
    .guide-img-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }
    .guide-card:hover .guide-img-wrap img {
      transform: scale(1.03);
    }
    .guide-category-badge {
      position: absolute;
      bottom: 12px;
      left: 14px;
      background: #f59e0b;
      color: #ffffff;
      font-size: 0.7rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 4px 12px;
      border-radius: 9999px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .guide-content {
      padding: 24px;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
    }
    .guide-meta {
      font-size: 0.75rem;
      font-weight: 600;
      color: #94a3b8;
      margin-bottom: 10px;
    }
    .guide-headline {
      font-size: 1.1rem;
      font-weight: 800;
      color: #084582;
      line-height: 1.4;
      margin-bottom: 12px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .guide-excerpt {
      font-size: 0.88rem;
      color: #475569;
      line-height: 1.55;
      margin-bottom: 20px;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .guide-link {
      font-size: 0.88rem;
      font-weight: 800;
      color: #0284c7;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: gap 0.2s ease;
    }
    .guide-link:hover {
      gap: 10px;
      color: #0369a1;
    }

    /* Popular Destinations Directory */
    .destinations-section {
      background: #ffffff;
      border-top: 1px solid #e2e8f0;
      padding: 64px 24px;
    }
    .destinations-container {
      max-width: 1100px;
      margin: 0 auto;
    }
    .dest-title {
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--ez-navy);
      margin-bottom: 32px;
      text-align: center;
    }
    .dest-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 32px;
    }
    .dest-column h4 {
      font-size: 0.95rem;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 16px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
    }
    .dest-column ul {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .dest-column a {
      color: #475569;
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 500;
      transition: color 0.15s ease;
    }
    .dest-column a:hover {
      color: #0284c7;
      text-decoration: underline;
    }

    /* Footer */
    .footer-404 {
      background: var(--ez-navy-dark);
      color: #94a3b8;
      padding: 32px 24px;
      text-align: center;
      font-size: 0.85rem;
    }
    .footer-404 a {
      color: #cbd5e1;
      text-decoration: none;
    }
  </style>
</head>
<body>

  <!-- Top Navigation Bar -->
  <header class="top-nav">
    <div class="top-nav-inner">
      <a href="/" class="logo-brand">
        <img src="/images/ez-mortgage-broker.webp" alt="EZ Mortgage Broker" class="brand-logo-img">
      </a>
      <nav class="nav-links">
        <a href="/">Home</a>
        <a href="/pages/loans/first-home-buyers.html">First Home Buyers</a>
        <a href="/pages/refinancing.html">Refinancing</a>
        <a href="/calculators.html">Calculators</a>
        <a href="/pages/blog">News & Insights</a>
        <a href="/#contact" class="btn-consult-nav">Book Consultation</a>
      </nav>
    </div>
  </header>

  <!-- Main Hero 404 Section with Lottie Animation -->
  <main>
    <section class="hero-404">
      <div class="hero-container">
        
        <!-- Interactive Lottie Animation -->
        <div class="animation-wrapper">
          <lottie-player 
            src="https://assets5.lottiefiles.com/packages/lf20_kjixtysj.json" 
            background="transparent" 
            speed="1" 
            loop 
            autoplay>
          </lottie-player>
        </div>

        <div class="floating-badge">
          <span class="pulse-dot"></span>
          <span>404 • Page Moved or Missing</span>
        </div>
        
        <h1 class="headline-404">
          Oops, the page you're trying to view isn't here.
        </h1>
        
        <h2 class="subheadline-404">
          But you’re still on the path to securing the lowest rate, maximizing your borrowing power, and owning your dream property.
        </h2>
        
        <p class="desc-404">
          See how EZ Mortgage Broker, Australia's trusted mortgage brokerage, helps you compare 50+ Australian lenders, eliminate bank loyalty tax, and fast-track your home loan approval with zero broker fees.
        </p>
        
        <div class="hero-ctas">
          <a href="/calculators.html#borrowing-power" class="btn-primary-ez">
            Calculate Borrowing Power ↗
          </a>
          <a href="/#contact" class="btn-outline-ez">
            Book Free Consultation
          </a>
        </div>
      </div>
    </section>

    <!-- Mortgage Guides & Insights Preview Section (Exact Image 2 Match) -->
    <section class="guides-section">
      <span class="guides-eyebrow">RESOURCES & RESEARCH</span>
      <h3 class="guides-title">Mortgage Guides & Insights</h3>
      <p class="guides-desc">Free resources, government grant guides, and strategy playbooks to help you make smarter loan decisions.</p>

      <div class="guides-grid">
        <!-- Card 1: First Home Buyer Grants -->
        <article class="guide-card">
          <div class="guide-img-wrap">
            <img src="/images/first-home-buyers-hero-BWDoVOZm.jpg" alt="First Home Buyer Grants Guide" onerror="this.src='https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=600&q=80'">
            <span class="guide-category-badge">HOME BUYING</span>
          </div>
          <div class="guide-content">
            <div>
              <div class="guide-meta">By R BAKSHI • 6 min read</div>
              <h4 class="guide-headline">First Home Buyer's Complete Guide to Australian Government Grants</h4>
              <p class="guide-excerpt">A complete breakdown of every grant and scheme available across VIC, NSW, QLD, WA, SA, including the 5% Deposit Guarantee and stamp duty waivers.</p>
            </div>
            <a href="/pages/blog/first-home-buyers-grant-2026-guide.html" class="guide-link">Read full guide →</a>
          </div>
        </article>

        <!-- Card 2: How to Refinance -->
        <article class="guide-card">
          <div class="guide-img-wrap">
            <img src="/images/assets-ez-mortgage-broker/06._refinance.png" alt="Refinance Playbook" onerror="this.src='https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=600&q=80'">
            <span class="guide-category-badge">REFINANCING</span>
          </div>
          <div class="guide-content">
            <div>
              <div class="guide-meta">By R BAKSHI • 7 min read</div>
              <h4 class="guide-headline">How to Refinance Your Mortgage in Australia: Step-by-Step Playbook</h4>
              <p class="guide-excerpt">How to renegotiate your interest rate, switch lenders without penalties, and structure offset accounts to save thousands over your loan term.</p>
            </div>
            <a href="/pages/blog/how-to-refinance-mortgage-australia-playbook.html" class="guide-link">Read full guide →</a>
          </div>
        </article>

        <!-- Card 3: Property Investment Structuring -->
        <article class="guide-card">
          <div class="guide-img-wrap">
            <img src="/images/assets-ez-mortgage-broker/cgt-property-investment-australia-2027.jpg" alt="Property Investment Structuring" onerror="this.src='https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80'">
            <span class="guide-category-badge">INVESTMENT</span>
          </div>
          <div class="guide-content">
            <div>
              <div class="guide-meta">By R BAKSHI • 8 min read</div>
              <h4 class="guide-headline">Property Investment Structuring, Tax Strategy & Wealth Creation</h4>
              <p class="guide-excerpt">Using usable equity, interest-only buffers, and portfolio structuring to build a scalable Australian property investment portfolio.</p>
            </div>
            <a href="/pages/blog/property-investment-structuring-tax-wealth.html" class="guide-link">Read full guide →</a>
          </div>
        </article>
      </div>
    </section>

    <!-- Popular Destinations Links Directory -->
    <section class="destinations-section">
      <div class="destinations-container">
        <h3 class="dest-title">Popular Destinations & Tools</h3>
        
        <div class="dest-grid">
          <!-- Column 1: Loan Solutions -->
          <div class="dest-column">
            <h4>Loan Solutions</h4>
            <ul>
              <li><a href="/pages/loans/first-home-buyers.html">First Home Buyer Loans</a></li>
              <li><a href="/pages/refinancing.html">Refinance & Rate Bargaining</a></li>
              <li><a href="/pages/loans/self-employed-alt-doc-loans.html">Self-Employed Alt-Doc Loans</a></li>
              <li><a href="/pages/loans/ndis-sda-property-finance.html">NDIS / SDA Property Finance</a></li>
              <li><a href="/pages/blog/smsf-property-lending-investing-super-guide.html">SMSF Property Lending</a></li>
            </ul>
          </div>

          <!-- Column 2: Calculators & Tools -->
          <div class="dest-column">
            <h4>Financial Calculators</h4>
            <ul>
              <li><a href="/calculators.html#borrowing-power">Borrowing Power Calculator</a></li>
              <li><a href="/calculators.html#loan-repayment">Mortgage Repayment Calculator</a></li>
              <li><a href="/calculators.html#stamp-duty">Stamp Duty & Concessions Tool</a></li>
              <li><a href="/calculators.html#refinance-savings">Refinance Savings Estimator</a></li>
              <li><a href="/calculators.html#extra-repayments">Extra Repayments & Offset Tool</a></li>
            </ul>
          </div>

          <!-- Column 3: Market News & Guides -->
          <div class="dest-column">
            <h4>Market Intelligence</h4>
            <ul>
              <li><a href="/pages/blog">All News & Market Alerts</a></li>
              <li><a href="/pages/blog/rba-cash-rate-decision-mortgage-repayments-2026.html">RBA Cash Rate Forecasts</a></li>
              <li><a href="/pages/blog/mortgage-brokers-settle-80-percent-australian-home-loans-mfaa.html">Why 80% Choose Brokers (BID)</a></li>
              <li><a href="/pages/blog/apra-serviceability-buffer-borrowing-power-2026-guide.html">APRA 3% Buffer Guidelines</a></li>
              <li><a href="/pages/blog/first-home-buyers-grant-2026-guide.html">First Home Guarantee Concessions</a></li>
            </ul>
          </div>

          <!-- Column 4: Broker Support -->
          <div class="dest-column">
            <h4>Broker Support</h4>
            <ul>
              <li><a href="/#contact">Book Free Strategy Consult</a></li>
              <li><a href="tel:1300050099">Call 1300 050 099</a></li>
              <li><a href="/pages/locations/mortgage-broker-tarneit.html">Mortgage Broker Tarneit</a></li>
              <li><a href="/pages/locations/mortgage-broker-point-cook.html">Mortgage Broker Point Cook</a></li>
              <li><a href="/pages/locations/mortgage-broker-werribee.html">Mortgage Broker Werribee</a></li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="footer-404">
    <p>© 2026 EZ Mortgage Broker. All rights reserved. | Australian Credit License Representative | <a href="/privacy-policy.html">Privacy Policy</a> | <a href="/cookie-policy.html">Cookie Policy</a></p>
  </footer>

</body>
</html>
"""

with open(ROOT_404, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(PUB_404, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Saved standard 404 template with Lottie animation, proper headline hierarchy, brand logo, and guides preview")

# Build
print("Building ezmortgagebroker with Vite...")
res = subprocess.run(["npm", "run", "build"], cwd=EZ_DIR, capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print(res.stderr)
