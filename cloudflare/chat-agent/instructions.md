# 📚 Finnova AI Platform — Architecture, Integration & Feature Matrix Guide

## 1. Universal Embed Scripts (Zero-Config)

When a customer or site owner deploys your chatbot on their website, they **only need to insert these three script tags once**:

```html
<!-- Central Cloudflare Promotional Banner, Cookie Consent & AI Widget -->
<script src="https://omni-agent.procrm.com.au/promo-banner.js" defer></script>
<script src="https://omni-agent.procrm.com.au/cookie-consent.js" defer></script>
<script src="https://omni-agent.procrm.com.au/widget.js" defer></script>
```

---

## 2. Why We Don't Need Site Owners to Edit Code Later

### ⚡ 100% Remote Control via Central Worker
Once those script tags are added to a site, **you never need to edit the website code again** to add new features or run campaigns:

1. **Domain Auto-Discovery**: When the scripts load, they inspect `window.location.hostname` (`finnova.org.au`, `ecrm.com.au`, `procrm.com.au`, `ezmortgagebroker.com.au`, `esignatures.online`).
2. **Server Configuration Resolution (`/api/config`)**: The scripts query your central Cloudflare Worker backend to retrieve brand identity, ABN, colors, proactive greetings, and feature flags.
3. **Instant Remote Updates**:
   - Want to launch a new promo banner? Enable it in `DOMAIN_CONFIGS` — it renders immediately on the client site.
   - Want to change the AI's personality or knowledge base? Update Cloudflare Vectorize/D1 — answers update live across all websites without redeploying frontend sites.
   - Want to change light/dark theme colors? Managed automatically from the Cloudflare Worker server response.

---

## 3. Automated User Signup & Welcome Onboarding Flow

When a new user signs up or requests integration:

```
[ New User Signs Up / Submits Form ]
                 │
                 ▼
[ Cloudflare D1 Ingestion (`/api/lead`) ]
  • Assigns Unique Session & Lead ID
  • Captures Domain, Contact Info & Initial Lead Score
                 │
                 ▼
[ Automated Onboarding Email Dispatch ]
  • Dispatches Welcome Email via Cloudflare Email Routing / Mailgun Webhook
  • Sends API Documentation & Script Embed Snippet
  • Provides Admin Portal Access Link for Lead Management
```

### Onboarding Information Sent to New Users:
- **Universal Script Embed Code Snippet** (Ready for paste into `<head>` or `<body>`).
- **Domain Verification Token** for domain ownership validation.
- **Admin Dashboard Credentials** to review real-time chat transcripts and lead submissions.

---

## 4. Google Analytics GA4 & Google Tag Manager Integration

`cookie-consent.js` automatically integrates with **Google Analytics GA4 (Consent Mode v2)** and **Google Tag Manager**:

### 📊 How It Operates:
1. **Default State**: Before user consent, optional analytics and advertising cookies remain blocked.
2. **User Grants Consent**: When the user clicks **"Accept Cookies"**, `cookie-consent.js` executes:
   ```javascript
   // Updates GA4 Consent Mode v2 Signals
   if (typeof window.gtag === 'function') {
     window.gtag('consent', 'update', {
       'analytics_storage': 'granted',
       'ad_storage': 'granted',
       'ad_user_data': 'granted',
       'ad_personalization': 'granted'
     });
   }
   // Pushes Custom GTM Event
   window.dataLayer.push({
     'event': 'cookie_consent_update',
     'analytics_consent': 'granted',
     'advertising_consent': 'granted'
   });
   ```
3. **User Rejects Optional Cookies**: Dispatches `'denied'` status to GA4, enforcing Australian Privacy Principles (APP) compliance.

---

## 5. Complete Platform Feature Matrix & Progress Status

| Feature / Component | Completion % | Status | Key Highlights & Strategic Suggestions |
| :--- | :---: | :---: | :--- |
| **Cloudflare Worker Core AI Engine** | `100%` | ✅ Live | Powered by Llama 3.1 8B Instruct with stream-ready response generation. |
| **Cloudflare Vectorize (RAG)** | `100%` | ✅ Live | Vector embeddings for domain-specific FAQs and site docs (`/api/admin/knowledge`). |
| **Cloudflare D1 Database Storage** | `100%` | ✅ Live | Real-time chat logs, consent audit receipts, and CRM lead persistence. |
| **Universal Standalone Widget (`widget.js`)** | `100%` | ✅ Live | Dynamic light/dark theme matching, screen awareness, image attachments, and markdown formatting. |
| **Cookie Consent Banner (`cookie-consent.js`)** | `100%` | ✅ Live | Australian APP compliance, GPC header detection, and automatic GA4 Consent Mode v2 sync. |
| **Behavioral Lead Scoring Engine** | `100%` | ✅ Live | Session-deduplicated path scoring (`+30` pricing, `-10` job seekers, `+15` scroll depth). |
| **Proactive AI Popup Triggers** | `100%` | ✅ Live | Automatically opens chat when visitor score reaches $\ge 35$ points with domain greetings. |
| **Promotional Announcement Banner (`promo-banner.js`)** | `100%` | ✅ Live | Google Workspace-style banner with responsive vector graphics and dismiss memory. |
| **Multi-Tenant Domain Registry** | `100%` | ✅ Live | Centralized server config for `finnova.org.au`, `ecrm.com.au`, `procrm.com.au`, `ezmortgagebroker.com.au`, `esignatures.online`. |
| **Automated Onboarding Email Dispatch** | `100%` | ✅ Live | Automated onboarding endpoint (`POST /api/onboard`) dispatches welcome HTML emails with script tags & cockpit link. |
| **Admin Analytics Cockpit Dashboard** | `100%` | ✅ Live | Live dashboard served at `/admin` displaying lead score distribution, cookie consent rates, and D1 lead records. |

---

### 🚀 Summary
With the universal script architecture, once site owners add the 3 script tags, **your Cloudflare Workers platform has 100% remote authority** over AI chat, lead scoring, cookie compliance, and promotional banners across all client websites without ever needing to touch their code again!
