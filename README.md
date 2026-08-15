# Blogs Content & High-Converting Landing Hubs Architecture

Welcome to the **Finnova Mortgage & Finance Pillar Blog Engine**.

This repository contains the complete static generation system, high-converting article templates, dynamic scroll-driven accordions, region-specific state hubs, and responsive lead-generation sidebars.

---

## 📁 Repository Structure

```
Blogs-Content/
├── posts.json               # Central content database for all 9 SEO pillar guides
├── state-data.json          # State & Territory FHOG, stamp duty price caps, and revenue links
├── pages/
│   ├── blog.html            # Main Blog & Insights Index
│   ├── blog/                # 9 Deep SEO Pillar Articles (1,500+ words each)
│   │   ├── first-home-buyers-grant-2026-guide.html
│   │   ├── ndis-sda-property-investment-guide.html
│   │   ├── self-employed-home-loans-alt-doc-guide.html
│   │   ├── how-to-refinance-mortgage-australia-playbook.html
│   │   ├── single-parent-guarantee-guide-2-percent-deposit.html
│   │   ├── borrowing-power-decoded-bank-assessment-rules.html
│   │   ├── fixed-vs-variable-navigating-rba-rate-cycle.html
│   │   ├── smsf-property-lending-investing-super-guide.html
│   │   └── property-investment-structuring-tax-wealth.html
│   ├── loans/               # Niche High-Intent Landing Hubs
│   │   ├── ndis-sda-property-finance.html
│   │   └── self-employed-alt-doc-loans.html
│   └── locations/           # Local Suburb Authority Pages
│       └── mortgage-broker-tarneit.html
├── images/                  # Compressed WebP and high-res photography assets
├── js/
│   ├── article-state-tabs.js # Dynamic ScrollSpy accordion engine + State tab switcher
│   └── main.js              # Global navigation, mobile drawer & animations
└── css/
    └── style.css            # Design tokens, pastel benefit cards, sticky sidebars
```

---

## ⚡ Core Engine Features

1. **Default-Open & Dynamic ScrollSpy Accordions**:
   - Every accordion starts **100% open by default** on page load for immediate reading and crawlability.
   - When the user scrolls down, the script calculates which section is in the active reading line (`window.pageYOffset > 80`) and automatically **smoothly closes all other sections** to keep long-form reading clutter-free.
   - Smooth CSS transitions (`cubic-bezier`) for seamless open/collapse.

2. **Mobile Smart Header vs Desktop Sticky Header**:
   - Desktop: Stays fixed at `top: 0` for direct conversions.
   - Mobile: Auto-hides on scroll-down to maximize viewport height, and reappears on scroll-up.

3. **Multi-State Interactive Grant Hub**:
   - Real-time tab switching across VIC, NSW, QLD, WA, SA, ACT, TAS, and NT without page reloads.

4. **Column 2 High-Converting Sticky Sidebar**:
   - Collapsible Google Reviews widget, 24-calculator links, related guides with thumbnails, and a sticky **Obligation-Free Assessment Card**.

---

## 🚀 How to Build & Deploy in Any Project

1. Install dependencies:
   ```bash
   npm install
   ```
2. Build static bundle:
   ```bash
   npm run build
   ```
3. Deploy to Cloudflare Pages, Vercel, or AWS S3.
