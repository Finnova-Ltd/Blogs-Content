# Comprehensive SEO, E-E-A-T & Article Quality Framework (`seo_content_enhancement_strategy.md`)

> **MANDATORY REPOSITORY DIRECTIVE**: This document defines the permanent SEO and content quality standards across **EZ Mortgage Broker**, **EZ Consultants**, **Blogs-Content**, and all related web platforms. All automated generation pipelines, editorial scripts, and manual content creations MUST comply with these rules.

---

## 1. Editorial Integrity & E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)

### A. Author & Credit Representative Disclosure
Every financial and professional article must include a clear, compliant author byline and regulatory disclosure:
* **Author**: `R Bakshi`
* **Title**: `Principal Mortgage & Finance Broker`
* **Accreditations**: `MFAA Accredited Broker | FBAA Member`
* **Compliance Disclosure**: `Australian Credit Representative Number (CRN: 538522) authorized under National Consumer Credit Protection Act 2009.`
* **Timestamps**: Explicit `Published Date` and `Last Reviewed / Verified Date`.

### B. Conditional, Legally Compliant Phrasing (Zero Absolute Promises)
Australian ASIC and NCCP regulations forbid misleading financial statements. Always use conditional language:
* ❌ *Avoid*: "Guaranteed loan approval", "100% full approval without deposit", "0% capital gains tax", "Full ATO compliance".
* ✅ *Use*: "Subject to lender credit assessment, formal valuation, and eligibility criteria", "Eligible borrowers may qualify for...", "Illustrative estimate based on current bank assessment buffers", "Consult your qualified accountant or tax advisor for personal advice".

---

## 2. In-Depth Content Depth & Anti-Thin Content Safeguards

To prevent Google's *Scaled Content Abuse* or *Thin Content* penalties, articles must deliver high-value, original analysis:

1. **Target Word Count**: Minimum **1,200 to 1,800+ words** of substantive analysis per pillar article.
2. **5 Mandatory Content Pillars per Article**:
   * **Pillar 1: Executive Market Context & Data Matrix**: Comprehensive breakdown of current RBA/APRA policies, lender assessment buffers, and an interactive 3-column comparative data table.
   * **Pillar 2: Real-World Borrower Scenarios & Case Studies**: Concrete numerical examples (e.g. $600k purchase vs $900k refinance, LVR brackets, borrowing capacity formulas).
   * **Pillar 3: Bank Policy & Underwriting Deep-Dive**: How Tier-1 banks vs Non-Banks assess overtime, bonuses, self-employed BAS, and rental income shading.
   * **Pillar 4: Regulatory Compliance & Consumer Protection (BID)**: Best Interests Duty (BID) analysis, offset vs redraw mechanics, and a 4-phase borrower hygiene checklist.
   * **Pillar 5: Frequently Asked Questions & Expert Advisory**: 3–5 high-intent FAQ accordion questions with clear, actionable answers + direct consultation booking connection.

---

## 3. SEO Meta Tags & Search Snippet Optimization

| Parameter | Standard / Constraint | Example |
| :--- | :--- | :--- |
| **Title Tag** | 50 – 60 characters (Max 60 chars) | `First Home Buyer Loans Melbourne \| 5% Deposit \| EZ Broker` |
| **Meta Description** | 140 – 160 characters (Max 160 chars) | `Compare 30+ accredited lenders with Melbourne mortgage brokers. Access 5% deposit schemes, VIC stamp duty exemptions, and fast pre-approvals.` |
| **Primary H1** | Exactly one `<h1>` per page | `First Home Buyer Loans Melbourne` |
| **Headings H2/H3** | Keyword-rich, answering user intent | `How Does the Australian 5% Deposit Scheme Work?` |
| **Open Graph** | `og:title`, `og:description`, `og:image`, `og:url`, `og:type="article"` | Included on all pages |
| **Twitter Card** | `twitter:card="summary_large_image"`, `twitter:title`, `twitter:image` | Included on all pages |

---

## 4. Structured Data (Schema.org JSON-LD `@graph`)

Every article and pillar page must include rich, valid JSON-LD structured data matching visible on-page content:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "FinancialService",
      "@id": "https://ezmortgagebroker.com.au/#organization",
      "name": "EZ Mortgage Broker",
      "url": "https://ezmortgagebroker.com.au/",
      "telephone": "+611300050099",
      "priceRange": "$$",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "470 St Kilda Rd",
        "addressLocality": "Melbourne",
        "addressRegion": "VIC",
        "postalCode": "3004",
        "addressCountry": "AU"
      }
    },
    {
      "@type": "BlogPosting",
      "headline": "Target Article Title",
      "description": "Meta description...",
      "datePublished": "2026-08-22T00:00:00+10:00",
      "dateModified": "2026-08-22T00:00:00+10:00",
      "author": {
        "@type": "Person",
        "name": "R BAKSHI",
        "jobTitle": "Principal Mortgage Broker"
      }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Visible FAQ Question 1?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Exact matching visible answer..."
          }
        }
      ]
    }
  ]
}
```

---

## 5. Location Page Quality (Anti-Doorway Safeguards)

To eliminate regional duplication risks across suburb hubs (`/pages/locations/`):
* Every location page must incorporate **unique, sourced local real estate data** (median house vs unit price, rental yields, local council planning zones, major transport corridors).
* Distinct borrower profiles (e.g. CBD = high-density apartment rules & 40sqm limits; Tarneit/Craigieburn = master-planned estates & house-land packages; Geelong = regional construction incentives & sea-change lending).
* Suburb-specific FAQs and genuine client testimonials.

---

## 6. Lead Generation & Consultation Modal Protocol

* All consultation CTA buttons (`Book Meeting`, `Book Free Consultation`, `Request Rate Review`) must connect directly to the interactive booking modal or `/contact` endpoint.
* Form must include: Full Name, Phone Number, Email, Loan Purpose, and Privacy Consent checkbox.
* Real validation and error handling before displaying confirmation state.
