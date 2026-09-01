# 📜 Finnova Ecosystem Global Publishing Rules & Standards (`RULES.md`)

This document establishes the **mandatory, non-negotiable global publishing rules** that MUST be checked and strictly enforced across all Finnova digital properties (`ezmortgagebroker.com.au`, `ezconsultants.com.au`, `procrm.com.au`, `finnova.org.au`, `ezsignature.com`).

---

## 👤 1. Official Author & Publishing Identity (MANDATORY)

* **All Articles MUST be Published by `R Bakshi`**:
  * **EZ Mortgage Broker**: `R Bakshi (Principal Mortgage Broker MFAA)` / `authorRole: "Principal Mortgage Broker MFAA"`
  * **EZ Consultants**: `R Bakshi (Principal CRM & AI Solutions Architect)` / `authorRole: "Principal Solutions Architect"`
  * **PRO CRM & Finnova**: `R Bakshi (Principal Enterprise Architect & Cyber Specialist)`
* **Zero Third-Party Authors/Bylines**:
  * **STRICT PROHIBITION**: Never use third-party journalist names, syndication bylines, or scraper author names (e.g., **NEVER** mention "Mina Martin", "Staff Reporter", "Anonymous", or any freelance byline).

---

## 🚫 2. Zero 3rd-Party Media Platform References (STRICT)

* **STRICT PROHIBITION of Commercial Media & Competitor Names**:
  * **NEVER** mention or cite commercial media portals or third-party lead generation sites in titles, excerpts, card snippets, headers, body text, or schema:
    * ❌ Prohibited: `news.com.au`, `Your Mortgage`, `InfoChoice`, `The Adviser`, `Broker News`, `Broker Daily`, `The Mercury`, `realestate.com.au`, `Domain`, `Finder`, `Canstar`, `Savings.com.au`, `Yahoo Finance`, `RateCity`, etc.
  * **ONLY Official Government & Regulatory Entities Allowed**:
    * ✅ Permitted Sources & References:
      * **Reserve Bank of Australia (RBA)** (`rba.gov.au`)
      * **Australian Prudential Regulation Authority (APRA)** (`apra.gov.au`)
      * **Australian Securities and Investments Commission (ASIC)** (`asic.gov.au`)
      * **Australian Taxation Office (ATO)** (`ato.gov.au`)
      * **Housing Australia / Home Guarantee Scheme** (`housingaustralia.gov.au`)
      * **Australian Cyber Security Centre (ASD ACSC)** (`cyber.gov.au`)
      * **NDIS Quality and Safeguards Commission** (`ndiscommission.gov.au`)
      * **State Revenue Offices (SRO Victoria, Revenue NSW, etc.)**
      * **Mortgage & Finance Association of Australia (MFAA)** / **FBAA**

---

## ⏰ 3. Explicit Publication Date & Time on All Cards & Articles

* **Mandatory Date + Time Display**:
  * Every article page, card thumbnail, and preview badge **MUST display the exact Publication Date and Time** in Australian Eastern Standard Time (AEST/AEDT).
  * **Format**: `📅 DD-Mon-YYYY · HH:MM AM AEST` (e.g., `📅 02-Sep-2026 · 05:45 AM AEST`).
  * **Zero Placeholders**: **NEVER** display vague phrases like *"Added recently"*, *"Just now"*, or static outdated dates.
  * The top website ticker date **MUST dynamically reflect today's local date**.

---

## 🏷️ 4. Concise, High-Authority Title Standards ($\le 80$ Chars)

* **Strict Character Limit**: Every article title must be **$\le 80$ characters** (cleanly formatted, no awkward word cuts).
* **No Clumsy Boilerplate Wrappers**:
  * Do **NOT** wrap raw news headlines with long boilerplate like `"What Does [Headline] Mean for Australian Borrowers?"`.
  * Use authoritative, direct action headlines (e.g., *"Housing Australia Expands $47B Mandate for First Home Buyers"* or *"RBA Cash Rate Strategy: Refinancing Benchmarks for 2026"*).

---

## 📝 5. Section Depth & Content Quality

* **Minimum 180–200 words per section**: Provide comprehensive technical, regulatory, and credit policy depth.
* **No Scraper Leftovers in Excerpts**:
  * Strip out all RSS newsletter promo text, email subscription CTAs, cookie notices, and social share prompts from excerpts and summaries.
  * All card excerpts must deliver clear, actionable credit/market intelligence written from the perspective of **R Bakshi**.

---

## ✅ Pre-Publishing Checklist

Before pushing any automated or manual updates to GitHub or live sites:
- [ ] Is the author strictly **`R Bakshi`**?
- [ ] Are all 3rd-party media names (`news.com.au`, `Mina Martin`, `InfoChoice`, etc.) **100% eliminated**?
- [ ] Are references restricted solely to **official Government/Regulatory bodies** (RBA, APRA, ASIC, ATO, Housing Australia)?
- [ ] Do all cards and headers display the **exact Date & Time** (e.g. `02-Sep-2026 · 05:45 AM AEST`)?
- [ ] Is the title length strictly **$\le 80$ characters**?
- [ ] Is the production bundle built and deployed **without `[skip ci]`**?
