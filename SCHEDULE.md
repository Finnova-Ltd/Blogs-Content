# 📅 Finnova Ecosystem — Multi-Platform Automated Content & Publishing Schedule

This document serves as the master operating reference for the automated content syndication, ingestion, and deployment schedule across all Finnova digital properties.

---

## ⏰ Master 6x Daily Execution Schedule

All workflows execute **6 times daily** aligned with Australian Eastern Standard Time (**AEST / UTC+10**):

| Execution Cycle | Time (AEST / Melbourne) | Time (UTC) | GitHub Actions Cron | Focus & Target Audience |
| :---: | :---: | :---: | :---: | :--- |
| **Cycle 1** | **4:00 AM AEST** | `18:00 UTC` | `0 18 * * *` | **Early Morning Pre-Market Feed**: RBA market previews, overnight US/UK tech & cybersecurity advisories. |
| **Cycle 2** | **8:00 AM AEST** | `22:00 UTC` | `0 22 * * *` | **Morning Commute Briefing**: Daily mortgage rates, Salesforce release alerts, community workshops. |
| **Cycle 3** | **12:00 PM (Noon) AEST** | `02:00 UTC` | `0 2 * * *` | **Midday Business Lunch Update**: APRA lending policies, enterprise cloud architecture benchmarks, NDIS digital guides. |
| **Cycle 4** | **4:00 PM AEST** | `06:00 UTC` | `0 6 * * *` | **Afternoon Market Close**: Bank pricing movements, CRM strategy guides, youth volunteer spotlight. |
| **Cycle 5** | **8:00 PM AEST** | `10:00 UTC` | `0 10 * * *` | **Evening Prime Reading**: Property investment structuring, Agentforce deep dives, senior anti-scam advisories. |
| **Cycle 6** | **12:00 AM (Midnight) AEST** | `14:00 UTC` | `0 14 * * *` | **Overnight System Maintenance & Batch Ingestion**: Feed cleanup, catalog sorting, cache invalidation. |

---

## 🌐 Platform Content Pillars & Ingestion Matrix

### 1. 🏠 EZ Mortgage Broker (`ezmortgagebroker.com.au`)
* **Live URL**: [`https://ezmortgagebroker.com.au/pages/blog`](https://ezmortgagebroker.com.au/pages/blog)
* **Workflow**: [`.github/workflows/daily_rss_publisher.yml`](file:///Users/robinbakshi/Documents/GitHub/ezmortgagebroker/.github/workflows/daily_rss_publisher.yml)
* **Local Repo Path**: `/Users/robinbakshi/Documents/GitHub/ezmortgagebroker`
* **Content Pillars**:
  * **Interest Rates & RBA**: Official Cash Rate decisions, Big 4 bank rate changes, fixed vs variable forecasting.
  * **Refinancing & Equity Cash-Out**: Debt consolidation strategies, 80% LVR negotiation, fee/cashback comparisons.
  * **First Home Buyers**: Federal First Home Guarantee (5% deposit, zero LMI), stamp duty waivers in VIC/NSW/QLD.
  * **Commercial & SMSF Lending**: Limited Recourse Borrowing Arrangements (LRBAs) for SME warehouse/office purchases.
  * **Self-Employed & Alt-Doc**: Low-doc, bank statement verification, and specialized credit solutions.
* **Format & UI Rules**:
  * Top-left date badge format: `DD` (top large) / `MMM` (bottom bold uppercase) e.g., **`25 AUG`**.
  * Light-theme card styling with subtle hover lift and direct MFAA-accredited broker contact panel.

---

### 2. ⚡ PRO CRM (`procrm.com.au`)
* **Live URL**: [`https://procrm.com.au/blog`](https://procrm.com.au/blog)
* **Workflow**: [`.github/workflows/daily_tech_news_sync.yml`](file:///Users/robinbakshi/Documents/Imprtant%20Repos/procrm-app/.github/workflows/daily_tech_news_sync.yml)
* **Local Repo Path**: `/Users/robinbakshi/Documents/Imprtant Repos/procrm-app`
* **Content Pillars**:
  * **Enterprise AI & Agentforce**: Autonomous agent deployment, trust layer guardrails, sub-4-week sprint execution.
  * **Data Cloud & Zero-Copy**: Data virtualization connecting Snowflake, Google BigQuery, and Databricks.
  * **NDIS & Healthcare CRM**: Participant care management, SCHADS award compliance, and automated roster costing.
  * **Cyber Defence & Compliance**: APRA CPS 234, ASD Essential Eight, zero-trust password policies, and automated patch management.
* **Format & UI Rules**:
  * Interactive auto-playing news carousel on homepage with region and category tags.
  * Col 2 fixed/sticky table of contents and highlight cards with zero scrollbars on desktop.

---

### 3. 💼 EZ Consultants (`ezconsultants.com.au`)
* **Live URL**: [`https://ezconsultants.com.au/blog`](https://ezconsultants.com.au/blog)
* **Workflow**: [`.github/workflows/salesforce_daily_publisher.yml`](file:///Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/.github/workflows/salesforce_daily_publisher.yml)
* **Local Repo Path**: `/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au`
* **Content Pillars**:
  * **Salesforce Architecture & Releases**: Spring/Summer release analyses, reactive screen components, governor limit telemetry.
  * **Public Sector & buy.nsw**: Accredited supplier delivery models, cloud governance, and audit-ready pipelines.
  * **CRM Strategy & Multi-Cloud**: Marketing Cloud Growth, Service Cloud Voice, and Revenue Lifecycle Management.
* **Format & UI Rules**:
  * 100% Light-Theme cards (`bg-gradient-to-br from-blue-50 to-indigo-50`, no dark/black boxes).
  * High-resolution cloud architecture photography with automatic `onError` image recovery.

---

### 4. 🌟 Finnova Community Hub (`finnova.org.au`)
* **Live URL**: [`https://finnova.org.au/en_AU.html`](https://finnova.org.au/en_AU.html)
* **Workflow**: [`.github/workflows/daily_community_publisher.yml`](file:///Users/robinbakshi/Documents/Imprtant%20Repos/Finnova/.github/workflows/daily_community_publisher.yml)
* **Local Repo Path**: `/Users/robinbakshi/Documents/Imprtant Repos/Finnova`
* **Content Pillars**:
  * **Cyber Safety & Scam Protection**: Plain-language workshops for seniors on AI voice scams, fake SMS links, and passphrases.
  * **Digital Literacy & NDIS Access**: 1-on-1 coaching for myGov, Medicare linking, and My NDIS mobile app navigation.
  * **Youth Tech Mentorship**: Weekend volunteer programs connecting high school/university students with local elders in Wyndham.
  * **Multilingual Support**: Community guides published in English, Hindi, Punjabi, Arabic, Spanish, Vietnamese, and Mandarin.
* **Format & UI Rules**:
  * Embedded and dynamic `posts.json?t=` cache-busting loader with instant fallback rendering.

---

### 5. ✍️ EZ Signature Online (`ezsignature.com`)
* **Live URL**: [`https://ezsignature.com/blog`](https://ezsignature.com/blog)
* **Local Repo Path**: `/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend`
* **Content Pillars**:
  * **Post-Quantum Cryptography & NIST PQC**: Kyber/Dilithium algorithms, long-term non-repudiation, tamper-evident audit trails.
  * **eIDAS & Electronic Transactions Act**: Legal validity under Australian Electronic Transactions Act 1999, Section 10 compliance, court-admissible audit logs.
  * **DocuSign & PandaDoc Alternative**: Fair usage pricing, zero per-envelope surcharges, native Salesforce LWC integration.
  * **Developer API & Webhooks**: HMAC SHA-256 signature verification, embedded signing iframes, zero-retention privacy mode.
* **Format & UI Rules**:
  * Clean modern SaaS layout, developer documentation links, interactive pricing calculator, and high-contrast light theme.


---

## 🛡️ Mandatory Content Quality & Design Standards

Every published article must strictly satisfy the following criteria:
1. **Length & Depth**: Minimum **180–200+ words per section** with actionable data, Australian statutory references, and strategic takeaways.
2. **Visual Design**: **100% Crisp Light Theme** — pure white background, subtle slate-200 borders, soft blue/indigo header gradients. No dark/black background boxes.
3. **Layout & Usability**:
   * **Sticky Col 2**: Table of Contents, Highlights, and Quick Contact cards remain permanently visible when scrolling Col 1 on desktop screens.
   * **Zero Scrollbars**: Visible scrollbars in widgets and highlights are hidden (`scrollbar-width: none;`).
4. **Timezone Integrity**: All dates must be computed using Australian Eastern Time (`AEST = UTC+10`) to prevent UTC calendar discrepancies.

---

## 🛠️ CLI Quick Reference & Manual Sync Commands

If you ever need to trigger a manual synchronization or rebuild locally:

```bash
# 1. Synchronize all articles & enforce AEST dates
python3 /Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/fix_aest_dates_and_sync.py

# 2. Deploy 25-Aug (or current date) content across all 4 sites
python3 /Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/publish_25_aug_all_sites.py

# 3. Build EZ Mortgage Broker
cd "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker" && npm run build && git push origin main

# 4. Build PRO CRM
cd "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app" && npm run build && git push origin main

# 5. Build EZ Consultants
cd "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au" && npm run build && git push origin main

# 6. Deploy Finnova Community Hub
cd "/Users/robinbakshi/Documents/Imprtant Repos/Finnova" && git push origin main
```
