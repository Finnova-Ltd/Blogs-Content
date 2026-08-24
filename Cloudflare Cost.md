# ☁️ Cloudflare Architecture & Zero-Cost Ledger (`Cloudflare Cost.md`)

> **Cost Target**: **$0.00 / month** across all operations.  
> This document logs every Cloudflare service utilized in the Finnova multi-brand ecosystem, along with strict usage limits, daily resets, and automatic safeguards to guarantee we never incur surprise bills.

---

## 📊 1. Cloudflare Services Inventory & Free Quotas

| Service / Tool | Active Role in Ecosystem | Free Plan Allowance | Our Daily / Monthly Usage | Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Workers AI** | Serverless LLM Scriptwriting (`@cf/meta/llama-3-8b-instruct`) & Audio | **10,000 Neurons / Day** (~200+ blog scripts daily) | ~50 to 500 Neurons / Day (<5% of free quota) | **$0.00** |
| **Cloudflare Images** | Fast responsive image resizing, WebP delivery & CDN caching | **5,000 Unique Transformations / Month** | ~300 to 800 Transformations / Month | **$0.00** |
| **D1 SQL Databases** | Serverless state tracking, publishing logs & content sync | **5,000,000 Read Rows / Day**; **100,000 Write Rows / Day** | ~500 Reads & 50 Writes / Day | **$0.00** |
| **Workers & Edge Compute** | Webhook routing, API handlers & reverse proxying | **100,000 Requests / Day** (Free tier) | ~1,500 Requests / Day | **$0.00** |
| **Turnstile** | Privacy-friendly, frictionless anti-bot protection on forms | **Unlimited Free Verifications** | ~100 to 500 Verifications / Day | **$0.00** |
| **DNS, CDN & SSL** | Global Anycast DNS, free Edge SSL & DDoS mitigation | **Unlimited Bandwidth & SSL Certificates** | Entire multi-site traffic | **$0.00** |

---

## 🛡️ 2. Multi-Account Safeguards & Failover Protocol

1. **Neuron Guard Engine (`scripts/cf_neuron_guard.py`)**:
   * Caps execution at **8,500 Neurons / Day** per account (15% safety buffer before the 10,000 threshold).
2. **Multi-Instance Account Rotation**:
   * If Account 1 reaches 8,500 Neurons, traffic automatically switches to Account 2 (`CLOUDFLARE_BACKUP_ACCOUNT_ID`), providing a combined **20,000+ free Neurons daily**.
3. **Zero-Cloud Fallback**:
   * If all cloud instances are exhausted, scripts immediately fall back to local rule-based NLP + Microsoft Edge Neural TTS on your Mac for **unlimited $0.00 offline execution**.

---

## 🔑 3. Environment Variables Reference

```env
# Primary Cloudflare Account (10,000 Free Neurons/Day)
CLOUDFLARE_ACCOUNT_ID="your_primary_account_id"
CLOUDFLARE_API_TOKEN="your_primary_api_token"

# Secondary Backup Account (10,000 Free Neurons/Day)
CLOUDFLARE_BACKUP_ACCOUNT_ID="your_backup_account_id"
CLOUDFLARE_BACKUP_API_TOKEN="your_backup_api_token"
```
