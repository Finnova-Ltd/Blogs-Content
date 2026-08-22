# Multi-Tenant AI Chat Agent (Cloudflare Workers AI + D1 Memory)

An embeddable, stateful AI chat widget powered by Cloudflare Workers AI and Cloudflare D1 SQL database. Designed to run across multiple domains with zero monthly subscription fees ($0/mo on Cloudflare Free Tier).

## Features
- **Multi-Tenant System**: Automatically detects the host domain (`window.location.hostname`) and switches system prompts dynamically.
- **Unlimited Websites Support**: Embed across an unlimited number of domains with 1 central Cloudflare Worker backend.
- **Persistent Memory**: Uses Cloudflare D1 serverless SQL database (`omni-chat-db`) to retain conversation history per user session.
- **Zero Dependencies Widget**: Serves a standalone, lightweight, floating chat widget (`widget.js`).
- **Edge Deployment**: Fast responses powered by Meta Llama 3.1 hosted on Cloudflare Workers AI GPUs.

---

## 🚀 Quick Setup: Embed on Any Website

Add this single `<script>` tag right before the closing `</body>` tag on any website (`procrm.com.au`, `esignatures.online`, etc.):

```html
<script src="https://omni-agent.testcustomer2022.workers.dev/widget.js" defer></script>
```

### Installation by Framework:

#### HTML / Static Sites

Paste the tag directly above `</body>` in your main `index.html` file.

#### WordPress

1. Install and activate the **WPCode** (or **Header and Footer Scripts**) plugin.
2. Go to settings and paste the script snippet into the **Footer / Before `</body>`** field.
3. Save changes.

#### React / Next.js

Add the script to your layout or main page component:

```jsx
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Script src="https://omni-agent.testcustomer2022.workers.dev/widget.js" strategy="lazyOnload"/>
      </body>
    </html>
  );
}
```

---

## 🌐 Adding New Websites & Domain Customization

You can embed this chat widget on **an unlimited number of websites**.

### Key Details:
- **Single Centralized Backend:** Whether you embed it on 5 websites or 5,000 websites, every site communicates with your single Cloudflare Worker (`omni-agent.testcustomer2022.workers.dev`).
- **Dynamic Customization:** To add custom AI prompts for new domains, simply update the `DOMAIN_PROMPTS` object inside `src/index.ts`:

```typescript
const DOMAIN_PROMPTS: Record<string, string> = {
  "procrm.com.au": "You are the AI assistant for Pro CRM Australia...",
  "esignatures.online": "You are the AI assistant for eSignatures Online...",
  "ezmortgagebroker.com.au": "You are the AI assistant for EZ Mortgage Broker...",
  "newwebsite.com": "You are the AI assistant for New Website..." // Add any new domain here
};
```

### Free Tier Limits & Scaling:
- **Cloudflare D1 Database:** Gives you **5,000,000 free read queries per day**, easily handling high volume across many sites.
- **Workers AI:** Provides **10,000 free AI neurons per day** (roughly 1,000 to 3,000 chat responses daily). If your combined traffic across all websites exceeds this limit, Cloudflare seamlessly scales without breaking your widget.

---

## 🛠 Local Development & Deployment

### Environment Requirements

* Node.js 18+
* Cloudflare Wrangler CLI

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Finnova-Ltd/cloudflare-agents.git
cd cloudflare-agents
```

2. Install dependencies:
```bash
npm install
```

3. Deploy changes live to Cloudflare:
```bash
npx wrangler deploy
```

---

## 📊 Live Endpoints

* **Chat API**: `https://omni-agent.testcustomer2022.workers.dev/api/chat`
* **Embed Widget**: `https://omni-agent.testcustomer2022.workers.dev/widget.js`
* **D1 Database**: `omni-chat-db`
