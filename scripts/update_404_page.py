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
  <title>Oops, the page you're trying to view isn't here | EZ Mortgage Broker</title>
  <meta name="description" content="Oops, the page you're trying to view isn't here. But you're still on the path to securing the lowest home loan rate and maximizing your borrowing power with EZ Mortgage Broker.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/calculators.css">
  
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
      max-width: 1200px;
      margin: 0 auto;
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .logo-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
    }
    .logo-brand span {
      font-weight: 900;
      font-size: 1.25rem;
      letter-spacing: -0.03em;
      color: var(--ez-navy);
    }
    .nav-links {
      display: flex;
      align-items: center;
      gap: 24px;
    }
    .nav-links a {
      color: #334155;
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 600;
      transition: color 0.15s ease;
    }
    .nav-links a:hover {
      color: var(--ez-navy);
    }
    .btn-consult-nav {
      background: var(--ez-navy);
      color: #ffffff !important;
      padding: 10px 20px;
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
      padding: 64px 24px 48px;
      text-align: center;
      background: radial-gradient(circle at 50% 20%, #e0f2fe 0%, #f8fafc 70%);
    }
    .hero-container {
      max-width: 900px;
      margin: 0 auto;
    }
    .badge-404 {
      display: inline-block;
      background: #e0f2fe;
      color: var(--ez-navy);
      font-weight: 800;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 6px 16px;
      border-radius: 9999px;
      margin-bottom: 20px;
      border: 1px solid #bae6fd;
    }
    .headline-404 {
      font-size: 2.75rem;
      font-weight: 900;
      color: var(--ez-navy);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 18px;
    }
    .subheadline-404 {
      font-size: 1.5rem;
      font-weight: 800;
      color: #1e293b;
      line-height: 1.35;
      margin-bottom: 16px;
      letter-spacing: -0.02em;
    }
    .desc-404 {
      font-size: 1.1rem;
      color: #475569;
      line-height: 1.6;
      max-width: 680px;
      margin: 0 auto 32px;
    }
    .hero-ctas {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      justify-content: center;
      margin-bottom: 48px;
    }
    .btn-primary-ez {
      background: #0284c7;
      color: #ffffff;
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
      color: var(--ez-navy);
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
      color: #ffffff;
      transform: translateY(-2px);
    }

    /* Visual Dashboard Illustration */
    .dashboard-preview-wrapper {
      max-width: 860px;
      margin: 0 auto 64px;
      padding: 16px;
      position: relative;
    }
    .dashboard-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 24px;
      box-shadow: 0 20px 50px -10px rgba(8, 69, 130, 0.12);
      overflow: hidden;
      display: grid;
      grid-template-columns: 1fr 1fr;
      text-align: left;
    }
    @media (max-width: 768px) {
      .dashboard-card {
        grid-template-columns: 1fr;
      }
      .headline-404 {
        font-size: 2rem;
      }
      .subheadline-404 {
        font-size: 1.25rem;
      }
      .nav-links {
        display: none;
      }
    }
    .dash-left {
      padding: 32px;
      background: #f8fafc;
      border-right: 1px solid #e2e8f0;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 20px;
    }
    .dash-right {
      padding: 32px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 16px;
    }
    .metric-pill {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 14px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .metric-label {
      font-size: 0.8rem;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .metric-val {
      font-size: 1.15rem;
      font-weight: 900;
      color: var(--ez-navy);
    }
    .metric-tag {
      font-size: 0.75rem;
      font-weight: 800;
      background: #dcfce7;
      color: #15803d;
      padding: 4px 10px;
      border-radius: 9999px;
    }
    .lender-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .lender-badge {
      background: #f1f5f9;
      color: #334155;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 6px 12px;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
    }
    .advisor-bubble {
      background: #e0f2fe;
      border: 1px solid #bae6fd;
      border-radius: 16px;
      padding: 16px;
      position: relative;
    }
    .advisor-header {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 8px;
    }
    .advisor-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: var(--ez-navy);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 0.85rem;
    }
    .advisor-name {
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--ez-navy);
    }
    .advisor-role {
      font-size: 0.75rem;
      color: #64748b;
    }
    .advisor-text {
      font-size: 0.85rem;
      color: #1e293b;
      line-height: 1.5;
      margin: 0;
    }

    /* Popular Destinations Grid */
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
        <span style="display:flex; align-items:center; gap:8px;">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 9.5L12 3L21 9.5V20C21 20.5523 20.5523 21 20 21H4C3.44772 21 3 20.5523 3 20V9.5Z" stroke="#084582" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 21V12H15V21" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          EZ MORTGAGE BROKER
        </span>
      </a>
      <nav class="nav-links">
        <a href="/">Home</a>
        <a href="/pages/loans/first-home-buyers.html">First Home Buyers</a>
        <a href="/pages/refinancing.html">Refinancing</a>
        <a href="/calculators.html">Calculators</a>
        <a href="/pages/blog">Blog & Insights</a>
        <a href="/#contact" class="btn-consult-nav">Book Consultation</a>
      </nav>
    </div>
  </header>

  <!-- Main Hero 404 Section -->
  <main>
    <section class="hero-404">
      <div class="hero-container">
        <span class="badge-404">Error 404 • Page Moved Or Missing</span>
        
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

      <!-- Encouraging Feature Dashboard Mockup -->
      <div class="dashboard-preview-wrapper">
        <div class="dashboard-card">
          <!-- Left Panel -->
          <div class="dash-left">
            <div>
              <div style="font-size: 0.75rem; font-weight: 800; color: #0284c7; text-transform: uppercase; margin-bottom: 6px;">Live Market Benchmarks</div>
              <h3 style="font-size: 1.1rem; font-weight: 900; color: #0f172a; margin: 0 0 16px;">Australian Loan Assessment Center</h3>
            </div>
            
            <div class="metric-pill">
              <div>
                <div class="metric-label">Estimated Rate Discount</div>
                <div class="metric-val">Up to 0.85% p.a.</div>
              </div>
              <span class="metric-tag">Discretionary Cut</span>
            </div>

            <div class="metric-pill">
              <div>
                <div class="metric-label">Wholesale Lender Panel</div>
                <div class="metric-val">50+ Accredited Lenders</div>
              </div>
              <span class="metric-tag">Best Interests Duty</span>
            </div>

            <div>
              <div style="font-size: 0.75rem; font-weight: 700; color: #64748b; margin-bottom: 8px;">Direct Tier-1 & Tier-2 Panel:</div>
              <div class="lender-row">
                <span class="lender-badge">CBA</span>
                <span class="lender-badge">Westpac</span>
                <span class="lender-badge">ANZ</span>
                <span class="lender-badge">NAB</span>
                <span class="lender-badge">Macquarie</span>
                <span class="lender-badge">Pepper Money</span>
                <span class="lender-badge">Liberty</span>
              </div>
            </div>
          </div>

          <!-- Right Panel -->
          <div class="dash-right">
            <div class="advisor-bubble">
              <div class="advisor-header">
                <div class="advisor-avatar">RB</div>
                <div>
                  <div class="advisor-name">Robin Bakshi</div>
                  <div class="advisor-role">Principal Mortgage Broker • MFAA Accredited</div>
                </div>
              </div>
              <p class="advisor-text">
                "Lost your way? Don't worry! Whether you need to calculate maximum borrowing capacity, review your current interest rate, or explore first-home grants, our team is ready to structure your loan for approval."
              </p>
            </div>

            <div style="display: flex; gap: 12px; justify-content: flex-start; margin-top: 8px;">
              <a href="/pages/blog" style="font-size: 0.85rem; font-weight: 700; color: #0284c7; text-decoration: none;">
                Browse Market Insights & Guides →
              </a>
            </div>
          </div>
        </div>
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

          <!-- Column 4: Contact & Locations -->
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

print("✅ Saved customized encouraging 404.html to root and public/")

# Run build
print("Building ezmortgagebroker...")
res = subprocess.run(["npm", "run", "build"], cwd=EZ_DIR, capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print(res.stderr)
