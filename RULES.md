# 📜 Finnova Ecosystem Global Publishing Rules & Standards (`RULES.md`)

This document establishes the **mandatory, non-negotiable global publishing rules, local SEO standards, and layout specifications** that MUST be checked and strictly enforced across all Finnova digital properties (`ezmortgagebroker.com.au`, `ezconsultants.com.au`, `procrm.com.au`, `finnova.org.au`, `ezsignature.com`).

---

## 👤 1. Official Author & Publishing Identity (MANDATORY)

* **All Articles MUST be Published by `R Bakshi`**:
  * **EZ Mortgage Broker**: `R Bakshi (Principal Mortgage Broker MFAA)` / `authorRole: "Principal Mortgage Broker MFAA"`
  * **EZ Consultants**: `R Bakshi (Principal CRM & AI Solutions Architect)` / `authorRole: "Principal Solutions Architect"`
  * **PRO CRM & Finnova**: `R Bakshi (Principal Enterprise Architect & Cyber Specialist)`
* **Zero Third-Party Authors/Bylines**:
  * **STRICT PROHIBITION**: Never use third-party journalist names, syndication bylines, or scraper author names (e.g., **NEVER** mention "Mina Martin", "Staff Reporter", "Anonymous", or any freelance byline).

---

## 📍 2. Local Melbourne & Suburb SEO Keywords (MANDATORY)

Every mortgage and finance article MUST weave in **Melbourne Metropolitan & Regional Growth Corridor Keywords** into the body copy, comparison tables, and metadata to capture high-intent localized search traffic:

* **Western Melbourne Growth Corridors**: `Tarneit`, `Truganina`, `Point Cook`, `Werribee`, `Williams Landing`, `Caroline Springs`, `Manor Lakes`, `Melton`.
* **Northern Melbourne Corridors**: `Craigieburn`, `Wollert`, `South Morang`, `Mernda`, `Bundoora`, `Preston`, `Coburg`, `Roxburgh Park`.
* **Eastern & Inner Suburbs**: `Camberwell`, `Balwyn`, `Glen Waverley`, `Mount Waverley`, `Hawthorn`, `Kew`, `Doncaster`, `Richmond`, `Melbourne CBD`.
* **Bayside & South-Eastern**: `Brighton`, `Sandringham`, `Cheltenham`, `St Kilda`, `Frankston`, `Berwick`, `Dandenong`.

---

## 📌 3. Column 2 (Sticky Sidebar) Architecture & Widgets

* **Card #1 in Column 2 MUST ALWAYS be the Author Profile Card**:
  * Positioned at **Card #1 in Column 2 (Top of Sticky Sidebar)**.
  * Features the **Calculators photo cover header** (`/images/ez-broker-cover-header.jpg`), the **isolated EZ Hut icon in the circular avatar** (`/images/ez-icon-circle.webp`), and 1-click contact buttons (`📞 Call 1300 050 099`, `📅 Book Consultation`).
* **Card #2: Multi-Point Highlights Accordion**:
  * Must contain **3 to 4 actionable key takeaways** structured inside expandable/collapsible `<details>` accordion items (Rate Policy, Suburb Impact, Cash Flow, Broker Audit) rather than a single static bullet.
* **Sticky Positioning**: Configured with `position: -webkit-sticky !important; position: sticky !important; top: 105px !important; align-self: flex-start !important; max-height: calc(100vh - 120px) !important; overflow-y: auto !important;`.

---

## 🎨 4. Header & Navigation Standards

* **Logo Sizing & Placement**:
  * Logo width must be prominent and unsquished: `width: auto; height: clamp(52px, 5.5vw, 68px); max-width: 260px; object-fit: contain;`.
  * Shifted right towards navigation: `margin-left: clamp(16px, 3.5vw, 60px);`.
* **Header CTA Buttons in 1 Row**:
  * `Call Us` and `Book Consult` buttons MUST appear side-by-side in **1 single horizontal row**: `display: flex; flex-direction: row; align-items: center; gap: 10px; flex-wrap: nowrap;`.
* **Article Header Banner**:
  * Uses the rich Melbourne Bourke street background image with gradient overlay: `background: linear-gradient(135deg, rgba(6, 40, 77, 0.88) 0%, rgba(8, 69, 130, 0.78) 50%, rgba(6, 53, 101, 0.92) 100%), url('/images/melbourne-bourke-street-header.webp') center/cover no-repeat;`.

---

## 🎯 5. Mandatory Article Engagement Criteria

Plain walls of passive text are strictly prohibited. Every article must actively engage the reader and drive micro-conversions using the following **4 Engagement Pillars**:

1. **Mid-Article Financial Impact Table (Visual Comparison)**:
   * Displays structured tables comparing standard assessment vs streamlined exceptions (<80% LVR) vs SMSF/Commercial policies.
2. **Interactive 1-Click Utilities (Copy / Download / Calculators)**:
   * Actionable utility blocks (e.g., 1-Click Copy tools with clipboard feedback, or calculator links).
3. **Mid-Stream Expert Intercept Banners**:
   * Contextual broker advisory callouts (e.g. *"Need 2 to 3 Settled Comparable Sales for Your Street? Call R Bakshi on 1300 050 099"*).
4. **Actionable Step-by-Step Breakdowns**:
   * Numbered visual step badges (`[1]`, `[2]`, `[3]`) and structured statutory grounds.

---

## 🚫 6. Zero 3rd-Party Media Platform References (STRICT)

* **STRICT PROHIBITION of Commercial Media & Competitor Names**:
  * **NEVER** mention or cite commercial media portals or third-party lead generation sites:
    * ❌ Prohibited: `news.com.au`, `Your Mortgage`, `InfoChoice`, `The Adviser`, `Broker News`, `The Mercury`, `realestate.com.au`, `Domain`, `Finder`, `Canstar`, `Savings.com.au`, `AFR`, `Nine.com.au`, etc.
  * **ONLY Official Government & Regulatory Entities Allowed**:
    * ✅ Permitted: **RBA**, **APRA**, **ASIC**, **ATO**, **Housing Australia**, **SRO Victoria / Land Use Victoria**, **MFAA** / **FBAA**.

---

## ⏰ 7. Explicit Publication Date & Time

* Every article page, card thumbnail, and preview badge **MUST display the exact Publication Date and Time**:
  * **Format**: `📅 DD-Mon-YYYY · HH:MM AM AEST` (e.g., `📅 02-Sep-2026 · 10:55 AM AEST`).
  * The top website ticker date **MUST dynamically reflect today's local date**.

---

## ✅ Pre-Publishing Checklist

Before pushing any automated or manual updates to GitHub or live sites:
- [ ] Are **Call Us & Book Consult** buttons in **1 single horizontal row**?
- [ ] Is the header logo prominent and unsquished (`max-width: 260px`, `height: clamp(52px, 5.5vw, 68px)`)?
- [ ] Does the article hero banner use the **Bourke Street Melbourne image + gradient**?
- [ ] Does Column 2 feature the **Author Profile Card (Card 1)** + **Multi-Point Highlights Accordion (Card 2)**?
- [ ] Does the body copy include **Melbourne & local suburb geographical keywords**?
- [ ] Is the author strictly **`R Bakshi`** with zero 3rd-party media names?
- [ ] Do all cards display the **exact Date & Time**?
- [ ] Is the production bundle built and deployed **without `[skip ci]`**?
