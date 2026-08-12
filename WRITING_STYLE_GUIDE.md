# Finnova Group — Content Writing Style Guide & Component Blueprint
> **Version**: 1.0.0  
> **Last Updated**: 13-Aug-2026  
> **Applicable Projects**: JM Loans, ProCRM, ECRM Australia, and Finnova Group Web Applications.

---

## 1. Executive Summary & Tone of Voice

Our content strategy bridges complex financial, mortgage, and legal concepts with clear, approachable, and actionable guidance for Australian clients.

### Core Content Pillars
* **Authoritative & Compliant**: Aligned with ASIC regulations, NCCP guidelines, ATO tax rules, and post-2026 superannuation LRBA reforms.
* **Empowering & Plain-English**: Demystify mortgage terms (LMI, LVR, Offset vs Redraw, LRBA, FHOG) without financial jargon.
* **Structured for Skimmability**: Use callout boxes, bulleted checklists with visual checkmarks (`✅`), comparison tables, and FAQ accordions.
* **Action-Oriented**: Every article or service page ends with clear primary and secondary Call-To-Action (CTA) buttons (*Book Consultation*, *Compare Rates*, *Talk to a Broker*).

---

## 2. Standard Page Blueprint & Structure

Every Service Detail page (`/services/:slug`) and Blog Article (`/blog/:slug`) MUST follow this 7-part structural framework:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. BREADCRUMB NAVIGATION & HERO OVERLAY BANNER                         │
│    - Top-Left: Date Badge (📅 Last Updated: 13-Aug-2026)              │
│    - Bottom-Left: Category Badge (e.g. Superannuation & Property)      │
│    - Top-Right: Glassmorphism Social Share Bar                         │
├────────────────────────────────────────────────────────────────────────┤
│ 2. HEADER META & AUTHOR PROFILE                                        │
│    - Title (H1), Tagline/Excerpt, Author Avatar, Role, Read Time       │
│    - Topic Highlight Pills / Tags                                      │
├────────────────────────────────────────────────────────────────────────┤
│ 3. EXECUTIVE INTRO & HIGHLIGHT CALLOUT BOX                             │
│    - High-impact introduction paragraph                                │
│    - Light green/blue callout box (service-callout-box)                │
├────────────────────────────────────────────────────────────────────────┤
│ 4. DEEP-DIVE SECTIONS (H2 & H3 HIERARCHY)                              │
│    - Clear section titles with anchor headings                         │
│    - Checkmark lists (service-check-list) with bold lead text          │
├────────────────────────────────────────────────────────────────────────┤
│ 5. COMPARISON TABLE & DATA VISUALIZATION                               │
│    - Responsive table wrapper (.table-responsive-wrapper)             │
│    - High-contrast headers, alternating rows, bold feature names      │
├────────────────────────────────────────────────────────────────────────┤
│ 6. FREQUENTLY ASKED QUESTIONS (FAQ)                                    │
│    - 3-4 structured FAQ cards (.service-faq-item)                      │
├────────────────────────────────────────────────────────────────────────┤
│ 7. FOOTER CALL TO ACTION (CTA) & SIDEBAR                               │
│    - Booking CTA card + All Services/Articles button                   │
│    - Sidebar: Broker Profile Card + Google Reviews Card                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Date & Localization Standards

* **Australian Date Format**: Always use **`DD-MMM-YYYY`** (e.g., `13-Aug-2026`).
* **Currency**: Use AUD (`$`) with proper comma formatting (e.g., `$500,000`).
* **Spelling**: Use Australian English (e.g., *Annualisation*, *Organise*, *Concessional*, *Licence*).

---

## 4. Reusable HTML & JSX Components

### A. Highlight Callout Box (`.service-callout-box`)
```html
<div class="service-callout-box">
  <h4>💡 Key Benefits of Commercial SMSF Investing:</h4>
  <ul class="service-check-list">
    <li>✅ <strong>Commercial Leaseback:</strong> Business owners can purchase premises through SMSF and lease back at market rates.</li>
    <li>✅ <strong>Asset Protection:</strong> LRBA structure shields cash and share assets from liabilities.</li>
    <li>✅ <strong>Tax Efficiency:</strong> Concessional super tax rates (15% accumulation, 0% pension).</li>
  </ul>
</div>
```

### B. Responsive Comparison Table (`.service-comparison-table`)
```html
<div class="table-responsive-wrapper">
  <table class="service-comparison-table">
    <thead>
      <tr>
        <th>Feature</th>
        <th>Residential SMSF Property</th>
        <th>Commercial SMSF Loan</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>New LRBA Borrowing</strong></td>
        <td><strong>Restricted</strong> (Outright cash purchase only)</td>
        <td><strong>Permitted</strong> (Up to 75% – 80% LVR)</td>
      </tr>
      <tr>
        <td><strong>Existing LRBA Loans</strong></td>
        <td>Grandfathered (Signed prior to 10-Aug-2026)</td>
        <td>Fully active under LRBA rules</td>
      </tr>
    </tbody>
  </table>
</div>
```

### C. FAQ Items (`.service-faq-item`)
```html
<div class="service-faq-item">
  <strong>Can I still buy residential property through my SMSF?</strong>
  <p><strong>Yes, but without borrowing.</strong> SMSFs cannot establish new LRBA loans for residential property, but can buy outright if cash reserves permit.</p>
</div>
```

---

## 5. Production CSS Design Tokens

```css
/* Service & Article Design System */
.service-callout-box {
  background: #f0fdf4;
  border-left: 4px solid #16a34a;
  border-radius: 12px;
  padding: 24px;
  margin: 28px 0;
}

.service-check-list {
  list-style: none;
  padding: 0;
  margin: 16px 0;
}

.service-check-list li {
  margin-bottom: 12px;
  font-size: 15.5px;
  line-height: 1.65;
  color: #334155;
}

.table-responsive-wrapper {
  overflow-x: auto;
  margin: 24px 0;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.service-comparison-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14.5px;
}

.service-comparison-table th {
  background: #0f2b48;
  color: #ffffff;
  padding: 14px 18px;
  text-align: left;
  font-weight: 700;
}

.service-comparison-table td {
  padding: 14px 18px;
  border-bottom: 1px solid #e2e8f0;
  color: #334155;
}

.service-faq-item {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.service-faq-item strong {
  display: block;
  font-size: 16px;
  color: #0f172a;
  margin-bottom: 8px;
}
```
