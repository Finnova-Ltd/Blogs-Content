# 🏛️ Multi-Brand Autonomous Content & Video Engine Architecture (`architecture.md`)

Comprehensive technical architecture for the Finnova multi-brand publishing, video generation, and autonomous agent network (EZ Mortgage Broker, Finnova, PRO CRM, EZ Consultants, eSignatures Online).

---

## 1. Core System Architecture

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

## 2. Short-Video-Maker Plan of Action: Option A + Option B Fallover

As agreed, we have codified the dual-engine strategy controlled by the **Antigravity Agent Brain**:

```
                               ┌─────────────────────────────────────────┐
                               │         ANTIGRAVITY AGENT BRAIN         │
                               │   (Scriptwriting, Hooks & Storyboard)   │
                               └────────────────────┬────────────────────┘
                                                    │
                         ┌──────────────────────────┴──────────────────────────┐
                         ▼                                                     ▼
        ┌──────────────────────────────────┐                  ┌──────────────────────────────────┐
        │       OPTION A (PRIMARY)         │                  │      OPTION B (LOCAL FALLOVER)   │
        │      GitHub Actions Cloud        │                  │      Local Apple Silicon Mac     │
        ├──────────────────────────────────┤                  ├──────────────────────────────────┤
        │ • Runs on scheduled cron         │  Failover / Dev  │ • M-series hardware acceleration │
        │ • Pre-installed Ubuntu FFmpeg    │ ◄──────────────► │ • `h264_videotoolbox` encoder    │
        │ • $0.00 Cloud Compute Cost       │                  │ • Renders 45s Short in < 4 secs  │
        └──────────────────────────────────┘                  └──────────────────────────────────┘
```

### Execution Responsibilities:
1. **Antigravity Agent Brain**:
   - Analyzes newly ingested blog articles and financial news.
   - Generates 3-scene narrative storyboards (Hook ➔ 3 Insights ➔ Principal Broker CTA).
   - Enforces brand voice assignment (EZ Mortgage: `Dh68koMHNSYl8A1jH9Je`, Finnova: `7xOqQceOZC5dhvkaqKtD`).
   - Slices script into max 75–90 words (~450 characters) to optimize ElevenLabs credits.
2. **Option A (GitHub Actions Primary)**:
   - Automated cloud rendering during 4-hourly CI/CD runs.
   - Pre-installed FFmpeg on Ubuntu runners for $0.00 cloud compute cost.
   - Outputs vertical 9:16 (1080x1920) MP4s and commits them to `assets/videos/`.
   - Generates standard RSS `<enclosure url="...mp4" length="..." type="video/mp4" />` tags for automated Make.com distribution.
3. **Option B (Local Apple Silicon Fallover)**:
   - Local on-device execution on Robin Bakshi's Mac workstation.
   - Utilizes Apple Silicon hardware acceleration (`-c:v h264_videotoolbox`) for sub-4-second video rendering.
   - Serves as developer preview and offline fallback when GitHub Actions queue is busy or undergoing maintenance.

---

## 3. Dynamic Visual Assets & Multi-Source Image Engine

> **Rule**: Never repeat identical static images across articles. A mortgage brokerage service requires authentic lending, finance, advisory, and banking imagery—not generic repetitive houses with swimming pools.

### Contextual Category-to-Asset Mapping Matrix:
| Article Category / Topic | Primary Image Visual | Contextual Asset Path | Free Stock Query (Pexels / Pixabay) |
| :--- | :--- | :--- | :--- |
| **RBA & Rates / Cash Rate** | Financial charts, calculator, Australian currency, interest rate review | `/images/assets-ez-mortgage-broker/rba-cash-rate-banking-analysis.jpg` | `"interest rates finance graph calculator desk"` |
| **Broker Advisory / Home Loans** | Accredited broker consultation, loan contract review, Australian family meeting broker | `/images/assets-ez-mortgage-broker/broker-consultation-rate-review.jpg` | `"mortgage broker meeting client office"` |
| **Refinancing / Repayments** | Mortgage refinancing savings comparison, bank statement review | `/images/assets-ez-mortgage-broker/mortgage-refinancing-savings-calculator.jpg` | `"refinance loan calculator banking savings"` |
| **First Home Buyers / FHOG** | Keys handover, young Australian couple holding house keys outside home | `/images/assets-ez-mortgage-broker/first-home-buyers-keys-handover.jpg` | `"first home buyers keys handover front door"` |
| **APRA & Lending Standards** | Credit underwriting, serviceability assessment, banking tablet app | `/images/assets-ez-mortgage-broker/digital-banking-app-loan-tracking.jpg` | `"bank loan approval document tablet meeting"` |
| **Super & SMSF Property** | Commercial property portfolio, superannuation wealth advisory | `/images/assets-ez-mortgage-broker/smsf-property-investment-portfolio.jpg` | `"commercial property finance portfolio meeting"` |
| **Commercial / Business** | Corporate office finance, commercial lending negotiation | `/images/assets-ez-mortgage-broker/commercial-business-property-finance.jpg` | `"commercial finance business contract handshake"` |

---

## 4. Multi-Channel Distribution & Make.com Automation

* **Make.com Trigger**: Listens to `https://ezmortgagebroker.com.au/feed.xml` and `rss.xml`.
* **Media Enclosures**:
  - `enclosure`: 9:16 vertical MP4 for YouTube Shorts, Instagram Reels, and Facebook Reels.
  - `media:content`: 16:9 full 10-minute masterclass MP4 for long-form YouTube channel distribution.
* **Auto-Deduplication**: Watermarked GUID tracking ensures zero duplicate social posts.
