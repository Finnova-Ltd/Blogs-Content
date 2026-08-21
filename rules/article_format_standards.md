# Article & Content Formatting Standards (Finnova / EZ Mortgage Broker / EZ Consultants)

## Overview
All new articles, blog posts, advisories, and industry updates across EZ Mortgage Broker, EZ Consultants, and related platforms MUST adhere strictly to the established high-authority editorial layout.

---

## Mandatory Layout Specifications

### 1. Full-Bleed Article Header Banner
* **Visual Styling**: Full-width dark navy backdrop (`#0A2540`) with blurred topic photography background and gradient overlay.
* **Top Toolbar**:
  * Left: Responsive breadcrumbs (`Home > News > [Category]`).
  * Right: Social share icon pill bar (Facebook, X/Twitter, LinkedIn, WhatsApp, Copy Link).
* **Category Pill**: High-contrast uppercase badge (e.g. `INVESTING STRATEGY` `#00876C`, `SUPER & SMSF` `#1D4ED8`, `RBA & RATES` `#A81127`, `COMPLIANCE` `#DC2626`).
* **Headlines**: Prominent, high-contrast title and informative 2-sentence executive summary.
* **Author Metadata Row**: Date (`📅 DD-Mmm-YYYY`), Reading Time (`⏱️ X min read`), and Author Badge (`✍️ R BAKSHI (Principal Broker)`).

### 2. Main Article Content (Left Column)
* **Lead In**: Georgia/Inter serif lead paragraph.
* **Interactive Accordion Sections (`.article-section-accordion`)**:
  * 4 to 5 structured sections with toggle headers (`+` / `-`).
  * Default state: First section open, subsequent sections expandable.
* **Structured Data Tables (`.article-data-table`)**:
  * At least one responsive comparative matrix table in Section 1 or 2 with dark navy table headers (`#0A2540`) and light alternating rows.
* **Actionable Checklist (`.article-checklist-card`)**:
  * 3–4 bullet checklist with green checkmarks (`✓`) in Section 4.
* **Advisory & Source Attribution Card**:
  * Blue callout box detailing how EZ Mortgage Broker / EZ Consultants assists.
  * Formal source attribution citation.

### 3. Sticky 5-Widget Sidebar (Right Column)
1. **Author / Broker Profile Card**:
   * Brand avatar, Name (`R Bakshi`), Title (`Principal Broker`), 5-star rating (`⭐⭐⭐⭐⭐ (14)`).
   * 3 action CTAs: `💬 Book Appointment`, `📱 Send Message`, `📇 Contact Card`.
2. **Highlights Timeline Widget (`.article-highlights-widget`)**:
   * Crimson header (`#A81127`).
   * Chronological key takeaway points with red bullet markers.
   * `Top of Article ↑` link.
3. **Google Reviews Card**:
   * Verified 5.0 ⭐ customer testimonial.
4. **Calculators Quick-Links Card**:
   * Direct links to Borrowing Power, Loan Repayment, and Stamp Duty Calculators.
5. **Sticky Advisory Call Card (`.sidebar-sticky-cta-card`)**:
   * Navy gradient with yellow direct phone button (`📞 Call 1300 050 099`).

---

## Automation Rule
Whenever an automated script (e.g. `ingest_authority_sources.py`, `ingest_yahoo_topics.py`, `ingest_salesforce_news.py`) generates a standalone HTML page or blog post object, it MUST generate the full markup with these accordions, tables, and sidebar widgets.
