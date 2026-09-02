# 🏛️ SEO Content Quality Gates & Editorial Standards (`SEO_CONTENT_QUALITY_GATES.md`)

**Website:** `https://ezmortgagebroker.com.au`  
**Mandate:** Strict pre-flight gates required before any article can be drafted, generated, compiled, or published.  
**Governing Standard:** Google Search Central Essentials (Helpful Content System, E-E-A-T, YMYL Lending Guidelines).

---

## 1. The Core Principle
> **Quality, Authority, and Borrower Utility over Volume.**  
> Under no circumstances may an article be published simply because an external RSS feed or Google Alert published a new headline. Every indexed URL must represent an authoritative, verified mortgage or property-lending resource.

---

## 2. Approved Source Hierarchy & Strict Blacklist

### Approved Tier 1: Primary Australian Authorities (Mandatory for factual claims)
* **Reserve Bank of Australia (RBA)**: Cash rate decisions, Statements on Monetary Policy, Financial Stability Reviews.
* **APRA (Australian Prudential Regulation Authority)**: Serviceability buffers, macroprudential standards, capital framework.
* **ASIC (Australian Securities and Investments Commission)**: National Consumer Credit Protection (NCCP), responsible lending.
* **Housing Australia (NHFIC)**: First Home Guarantee (FHBG), Regional First Home Buyer Guarantee, Help to Buy.
* **State Revenue Office Victoria (SRO Vic)**: Victorian stamp duty thresholds, First Home Owner Grant (FHOG), off-the-plan concessions.
* **Australian Taxation Office (ATO)**: Negative gearing rules, SMSF property lending compliance, division 7A.
* **Australian Bureau of Statistics (ABS)**: Lending indicators, CPI inflation, residential property price indexes.

### Approved Tier 2: Official Accredited Lender Announcements
* Major & Non-Bank Lenders: CBA, NAB, ANZ, Westpac, Macquarie, Pepper Money, Liberty, Bankwest, ING, etc. (Rate changes, policy shifts, turnaround times).

### Approved Tier 3: Discovery & Market Research
* CoreLogic, PropTrack, Domain Research, SQM Research (Market auction clearance rates, median house prices, rental yields).

### ⛔ STRICT BLACKLIST (Immediate Rejection)
Any source or topic containing the following MUST BE REJECTED AT INGESTION:
* Crime, police blotters, arrests, murder trials, court disputes.
* Individual residential property sales or rental listings (e.g. `1a-northmead-avenue...realestatecomau`).
* Family court arguments, inheritance disputes, neighbourhood quarrels.
* Celebrity property gossip, lifestyle clickbait, lottery stories.
* General macroeconomic news without direct, actionable impact on mortgage borrowers.

---

## 3. Mathematical Scoring Gates (Pre-Generation Verification)

Before drafting any content, the ingestion engine must evaluate:
```json
{
  "mortgage_relevance": 0,      // Minimum required: 80 / 100
  "australian_relevance": 0,    // Minimum required: 90 / 100
  "borrower_usefulness": 0,     // Minimum required: 75 / 100
  "original_insight_potential": 0, // Minimum required: 70 / 100
  "factual_confidence": 0       // Minimum required: 95 / 100
}
```
* **RULE:** If `mortgage_relevance < 80`, HALT IMMEDIATELY. Do not generate.
* **RULE:** If facts cannot be traced to Tier 1 or Tier 2 sources, HALT.

---

## 4. Defined Mortgage Topic Clusters (Cluster Requirement)

Every published article must map cleanly to one of these 6 commercial clusters:
1. **First Home Buyers**: Deposit accumulation, LMI waiver policies, FHBG, Victorian stamp duty exemptions.
2. **Refinancing & Equity**: Break-even analysis, fixed vs. variable, debt consolidation, cash-out equity for renovation/investment.
3. **Property Investors**: Serviceability, rental yield calculation, negative gearing, interest-only terms, portfolio structuring.
4. **Self-Employed & Complex Income**: Low-doc, alt-doc, 1-year tax returns, director wages, add-backs.
5. **Specialist Lending**: SMSF property loans, NDIS/SDA property finance, commercial property loans.
6. **Government Schemes & Rate Policy**: Official RBA cash rate repayment modeling, Help to Buy equity scheme.

* **RULE:** If an article does not belong to a defined cluster, it cannot be published.

---

## 5. Mandatory Original Borrower Utility Components

Every published article must contain **at least TWO** of the following high-value components:
1. **Worked Financial Example / Calculation Table**:
   * Example: Impact of an RBA 25 bps rate change on monthly repayments across `$500,000`, `$750,000`, and `$1,000,000` loan sizes with stated interest rate and term assumptions.
2. **Borrower Decision Framework / Comparison Table**:
   * Example: Variable vs. Fixed 2-year vs. Split Loan trade-off matrix.
3. **Broker Commentary by R Bakshi (MFAA Accredited)**:
   * Actionable tactical advice explaining how Australian lenders interpret credit policies.
4. **Interactive Tool / Calculator Integration**:
   * Direct deep-link to the relevant on-site calculator (`/calculators.html`, Borrowing Power, Stamp Duty).
5. **Borrower Action Checklist**:
   * Step-by-step document preparation requirements (e.g. 3 months payslips, 6 months bank statements).

---

## 6. Content Quality, Structure & Semantic Integrity
* **Word Count**: Minimum 600–1,200 words of dense, substantive analysis.
* **Semantic Alignment**: The URL Slug, `<title>`, and `<h1>` must precisely match the core mortgage topic.
* **Zero Duplication**: No repeated paragraphs, boilerplate loops, or templated filler.
* **Clean Termination**: No truncated sentences or broken HTML tags.
* **Internal Linking**: Minimum 3 cluster-relevant internal links to calculators, service pages, and Melbourne suburban landing pages.

---

## 7. Protection of Genuine Brand Assets
* **100% Preservation of Social Proof**: All 5.0-star Google Reviews, genuine client feedback, and verified engagement counters must remain untouched.
* **Location Landing Pages Clean-Up**: Location pages (e.g., *Mortgage Broker Melbourne CBD*, *Point Cook*, *Craigieburn*) must showcase localized lending intelligence (median unit vs house prices, high-density apartment lending criteria, Victorian stamp duty), and must **never** display generic or non-mortgage news feeds.
