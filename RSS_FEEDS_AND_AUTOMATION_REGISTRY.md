# 📡 Finnova Master RSS Feeds & GitHub Actions Automation Registry

Comprehensive documentation of all active RSS feeds, Google Alerts, data scrapers, target websites, and scheduled GitHub Actions workflows across the entire Finnova enterprise network.

---

## 🌐 Ecosystem Architecture Overview

```
                                    ┌────────────────────────────────────────────────────────┐
                                    │               FINNOVA CENTRAL CONTENT HUB              │
                                    │                    (Blogs-Content)                     │
                                    └───────────────────────────┬────────────────────────────┘
                                                                │
                     ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
                     ▼                                          ▼                                          ▼
    ┌──────────────────────────────────┐      ┌──────────────────────────────────┐      ┌──────────────────────────────────┐
    │       EZ MORTGAGE BROKER         │      │          EZ CONSULTANTS          │      │             PRO CRM              │
    │    (ezmortgagebroker.com.au)     │      │      (ezconsultants.com.au)      │      │         (procrm.com.au)          │
    ├──────────────────────────────────┤      ├──────────────────────────────────┤      ├──────────────────────────────────┤
    │ • RBA Cash Rate & APRA Buffers   │      │ • Salesforce Official News       │      │ • ASD ACSC Cyber Advisories      │
    │ • Australian Lending & FHOG      │      │ • Salesforce Ben Architecture    │      │ • NDIS Compliance Updates        │
    │ • 91 Suburb Location Pages       │      │ • MuleSoft & Agentforce AI       │      │ • Enterprise CRM Guides          │
    └──────────────────────────────────┘      └──────────────────────────────────┘      └──────────────────────────────────┘
```

---

## 1. 🏠 EZ Mortgage Broker (`ezmortgagebroker.com.au`)

### Active Data Ingestion Sources
| Source Name | Type | Feed URL / Query | Update Frequency |
| :--- | :--- | :--- | :--- |
| **Google Alerts — Mortgage** | Atom / RSS | `https://www.google.com/alerts/feeds/14625353401416373956/6439186835690371841` | Daily (4x / day) |
| **Google Alerts — Home Loans** | Atom / RSS | `https://www.google.com/alerts/feeds/14625353401416373956/10202701407179381699` | Daily (4x / day) |
| **Google Alerts — Super & SMSF** | Atom / RSS | `https://www.google.com/alerts/feeds/14625353401416373956/1200677753741493727` | Daily (4x / day) |
| **Yahoo Finance Australia** | RSS / Scraper | `https://au.finance.yahoo.com/news/` (Topics: mortgages, banking, property) | Every 30 mins |
| **Google News AU — RBA** | RSS | `https://news.google.com/rss/search?q=RBA+cash+rate+decision+OR+interest+rates+Australia&hl=en-AU&gl=AU&ceid=AU:en` | 4x / day |
| **Google News AU — First Home** | RSS | `https://news.google.com/rss/search?q=first+home+buyer+grant+Victoria+OR+stamp+duty+changes&hl=en-AU&gl=AU&ceid=AU:en` | 4x / day |
| **Nine News Finance** | Topic RSS | `https://www.nine.com.au/topic/finance-5x8` (via Google News topic feed) | 4x / day |
| **Australian Financial Review (AFR)** | Direct RSS | `https://www.afr.com/rss/property` & `https://www.afr.com/rss/banking-and-finance` | 4x / day |

### Automated GitHub Actions Workflow
* **Workflow File**: [`.github/workflows/daily_rss_publisher.yml`](file:///Users/robinbakshi/Documents/GitHub/Blogs-Content/.github/workflows/daily_rss_publisher.yml)
* **Cron Schedule**: `0 20,2,8,14 * * *` (6 AM, 12 PM, 6 PM, 12 AM AEST)
* **Action Output**:
  - Ingests feeds -> Updates `posts.json` and `/pages/blog/*.html`.
  - Regenerates 91 Suburb Location Pages with full headers & 4cm logo offset.
  - Builds Vite bundle and commits/pushes to `origin main`.
  - Indexes new vectors into Cloudflare Vectorize (`omni-knowledge-index`).

---

## 2. ☁️ EZ Consultants (`ezconsultants.com.au`)

### Active Data Ingestion Sources
| Source Name | Type | Feed URL | Update Frequency |
| :--- | :--- | :--- | :--- |
| **Salesforce Official News** | RSS | `https://www.salesforce.com/news/feed/` | Daily (4x / day) |
| **Salesforce Ben News** | RSS | `https://www.salesforceben.com/category/news/feed/` | Daily (4x / day) |
| **Salesforce Ben Strategy** | RSS | `https://www.salesforceben.com/feed/` | Daily (4x / day) |

### Automated GitHub Actions Workflow
* **Workflow File**: `ezconsultants.com.au/.github/workflows/salesforce_daily_publisher.yml`
* **Cron Schedule**: `0 0,6,12,18 * * *`
* **Action Output**:
  - Ingests Salesforce official articles & ecosystem analysis.
  - Enforces bright light-colored corporate photography.
  - Rebuilds Vite static assets and publishes live.

---

## 3. 🛡️ PRO CRM (`procrm.com.au`)

### Active Data Ingestion Sources
| Source Name | Type | Focus Area | Update Frequency |
| :--- | :--- | :--- | :--- |
| **ASD ACSC Cyber Advisories** | RSS / Scraper | Essential 8, ISO 27001, ISM compliance | Weekly / On Incident |
| **NDIS Quality & Safeguards Commission** | RSS / Scraper | NDIS CRM compliance, audit trail standards | Weekly |
| **CRM Architecture Advisories** | Scraper | Enterprise software integration, Cloud architecture | Weekly |

---

## 4. ✍️ eSignatures Online (`ezsignature.com`)

### Focus Areas & Content Strategy
* **Electronic Signature Laws**: Commonwealth Electronic Transactions Act 1999 (ETA), Section 10 identity rules, US ESIGN Act.
* **Pricing & Value Comparison**: Honest, transparent pricing breakdowns against DocuSign ($45/mo) and PandaDoc ($49/mo).
* **Security & Cryptography**: ISO 27001, Adobe Approved Trust List (AATL), digital audit trails.

---

## 5. 🤖 Cloudflare Agents & RAG Vector Knowledge Base

### Architecture & Storage Strategy
* **Cloudflare Worker**: `omni-agent` (`src/index.ts`)
* **Vectorize Index**: `omni-knowledge-index` (1024-dim `@cf/baai/bge-large-en-v1.5` embeddings)
* **D1 Memory DB**: `omni-chat-db`
* **Auto-RAG Vector Hook**: `scripts/embed_articles_to_vectorize.py`
* **Auto-Sync to Standalone Repo**: `.github/workflows/sync_cloudflare_agents.yml` -> `Finnova-Ltd/cloudflare-agents.git`

---

## 6. 🗄️ 3-Tier Multi-Site Archival Engine

* **Tier 1 (Hot - 0 to 90 Days)**: Cloudflare D1 `articles_hot` table for fast search & live counters.
* **Tier 2 (Static - Permanent Zero Cost)**: Pre-rendered HTML on Cloudflare Pages (unlimited bandwidth).
* **Tier 3 (Cold Archive - >90 Days)**: Monthly automated gzip JSONL snapshot to Cloudflare R2 (`archives/` directory).
* **Monthly Cron**: `.github/workflows/monthly_cold_archive.yml` (Runs 1st of every month).
