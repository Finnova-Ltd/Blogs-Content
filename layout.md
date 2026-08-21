# Standard Article & Blog Layout Specification (`layout.md`)

> **MANDATORY SYSTEM DIRECTIVE**: All new articles, advisories, market news posts, and blog pages created across EZ Mortgage Broker, EZ Consultants, PRO CRM, and affiliated properties MUST strictly use this standard layout. No single-card or simplified layouts are permitted.

---

## 1. Structural Architecture Blueprint

Every article page consists of a **Full-Bleed Header Banner** followed by a **2-Column Responsive Grid** (Content Left, Sticky Sidebar Right):

```
+-------------------------------------------------------------------------------+
|                      FULL-BLEED HERO BANNER (#0A2540)                        |
|  [Breadcrumbs: Home > News > Category]          [Social Share: FB, X, IN, WA] |
|  [CATEGORY BADGE: e.g. INVESTING STRATEGY]                                    |
|  ARTICLE HEADLINE TITLE (clamp(1.8rem, 3.2vw, 2.6rem))                        |
|  Article Subtitle & Lead-in Summary (max-width: 900px)                        |
|  [📅 Date]   [⏱️ Read Time]   [✍️ Author: R BAKSHI (Principal Broker)]        |
+-------------------------------------------------------------------------------+

+---------------------------------------------------+  +------------------------+
|           LEFT COLUMN: MAIN ARTICLE BODY          |  |   RIGHT COLUMN:        |
|                                                   |  |   STICKY 5-WIDGET      |
|  • Executive Context Lead Paragraph               |  |   SIDEBAR (360px)      |
|                                                   |  |                        |
|  [1. Accordion: Overview & Data Matrix [-]]       |  |  1. Broker Profile Card|
|     - Deep-dive narrative                        |  |     - Avatar & Star (14|
|     - 3-Column Comparative Matrix Data Table      |  |     - 3 Action CTAs    |
|                                                   |  |                        |
|  [2. Accordion: Technical & Policy Deep-Dive [+]] |  |  2. Crimson Highlights |
|     - Underwriting / regulatory standards         |  |     - Date & Bullets   |
|                                                   |  |     - Top of Article ↑ |
|  [3. Accordion: Regulatory Compliance & BID [+]]  |  |                        |
|     - ASIC / APRA / AUSTRAC context               |  |  3. Google Reviews Card|
|                                                   |  |     - 5.0 Rating ⭐     |
|  [4. Accordion: Action Checklist [+]]             |  |                        |
|     - 4-Phase Green Checkmark Box                 |  |  4. Mortgage           |
|                                                   |  |     Calculators Card   |
|  [5. Accordion: Advisory & Source Attribution [+]]|  |                        |
|     - Specialist Help Callout & Citation          |  |  5. Sticky Advisory    |
|                                                   |  |     Direct Call CTA    |
+---------------------------------------------------+  +------------------------+
```

---

## 2. Complete HTML / CSS Component Specifications

### A. Full-Bleed Hero Banner
* **Background Color**: `#0A2540` with blurred dynamic photo layer (`filter: blur(3px) brightness(0.75)`).
* **Overlay**: Linear gradient `rgba(10, 37, 64, 0.65) 0%` to `rgba(10, 37, 64, 0.92) 100%`.
* **Category Tag Color Coding**:
  * `Compliance & Fraud Prevention`: `#DC2626`
  * `Mortgage Broking & Policy`: `#0284C7`
  * `Finance Broking & Rates`: `#16A34A`
  * `Money & Banking`: `#1D4ED8`
  * `Property & Housing`: `#00876C`
  * `Personal Finance & Super`: `#7C3AED`
  * `RBA & Rates`: `#A81127`

### B. Interactive Accordions (`.article-section-accordion`)
* **Behavior**: Clickable header toggles `.open` state, switching icon between `+` and `−`.
* **Default State**: Section 1 is `.open` by default; subsequent sections expand on demand.
* **Header Style**: `#F8FAFC` background, `#0A2540` bold font, clean divider.

### C. Responsive Data Table (`.article-data-table`)
* **Header**: Solid `#0A2540` dark navy with white bold text.
* **Rows**: Alternating light rows with `#334155` text and `#e2e8f0` border.
* **Columns**: 3 columns (e.g. `TIMELINE / SCENARIO`, `ASSESSMENT CRITERIA`, `BORROWER BENEFIT`).

### D. Action Checklist Card (`.article-checklist-card`)
* **Styling**: `#F8FAFC` background with a `4px solid #00876C` green left border.
* **Items**: 4 phases marked with bold green checkmarks (`✓`).

### E. Sticky 5-Widget Sidebar
1. **Author / Broker Profile Card**:
   * Circular avatar, `R Bakshi - EZ Mortgage Broker`, 5-star rating `★★★★★ (14)`.
   * Buttons: `💬 Book Appointment` (`#0A2540`), `📱 Send Message` (`#1D4ED8`), `📇 Contact Card` (`#00876C`).
2. **Crimson Highlights Timeline Widget (`#A81127`)**:
   * Header in dark crimson `#A81127` with `Highlights −`.
   * Red bullet markers (`●`) mapping each section takeaway.
   * `Top of Article ↑` smooth scroll action.
3. **Google Reviews Testimonial Card**:
   * Rating `★ 5.0 (14)` with verified review quote from Jaspreet Sidhu.
4. **Mortgage Calculators Quick-Links**:
   * Direct anchors to Borrowing Power, Loan Repayment, and Stamp Duty calculators.
5. **Sticky Advisory Call CTA**:
   * Navy gradient with high-visibility yellow call button (`📞 Call 1300 050 099`).

---

## 3. Python Automation Integration Rule

When any content script generates an article (e.g. `ingest_authority_sources.py`, `ingest_yahoo_topics.py`, `ingest_salesforce_news.py`), it must call the standardized helper `generate_complete_article_html(...)` to output this exact structure.
