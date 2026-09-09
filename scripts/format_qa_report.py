import json

with open('/Volumes/Samsung SSD 2TB/03. Documents/GitHub/Blogs-Content/audit_report_all_sites.json', 'r') as fp:
    audit_data = json.load(fp)

md = """# 🛡️ Global Website QA Audit: Template, Canned & Low-Quality Content Report

**Audit Date:** 10-Sep-2026  
**Standards Applied:** Google Search Central Helpful Content System, E-E-A-T, YMYL Financial & Charity Guidelines, and Strict Zero-Template Criteria.

---

## Executive Summary

An exhaustive automated QA audit was conducted across all brand websites:
1. **Finnova (`finnova.org.au`)**
2. **EZ Mortgage Broker (`ezmortgagebroker.com.au`)**
3. **EZ Consultants (`ezconsultants.com.au`)**
4. **Blogs-Content Central Repository**

### Key Findings:
- **`finnova.org.au` Breakdown**: `posts.json` references 15 blog posts, but **0 static HTML files exist** in `pages/blog/`. When users click articles, the live site renders an empty template shell (as seen in the screenshot with missing body content). Furthermore, posts 14 & 15 are toxic mortgage/real-estate scraper stubs.
- **`ezmortgagebroker.com.au` Breakdown**: Out of 661 articles in `pages/blog/`:
  - **169 Articles** are high-quality, authentic, value-dense pieces.
  - **163 Articles** are repetitive canned boilerplate templates ("The Reserve Bank of Australia and major retail banks have updated residential mortgage assessment benchmarks...").
  - **329 Articles** are thin stubs or factsheet templates (< 250 words) that dilute SEO crawl equity.
- **`ezconsultants.com.au` Breakdown**: 87 articles are clean, high-quality, and verified.

---

## 1. Finnova (`finnova.org.au`) QA Audit Breakdown

| # | Article Title | Slug | Status / Issue | Recommended Action |
|---|---|---|---|---|
| 1 | Census 2026 Digital Assistance & Multilingual Support | `census-2026-digital-assistance-multilingual-support` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Charity article |
| 2 | Essential Eight Cyber Resilience 2026 | `essential-eight-cyber-resilience-community-non-profits-2026` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Cyber Safety article |
| 3 | Free Refurbished Laptops & Digital Hardware | `free-refurbished-laptops-bridging-digital-divide-2026` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Hardware Rehoming article |
| 4 | ASD ACSC Alert: Active Exploitation of Software Platforms | `asd-acsc-alert-software-platform-exploitation-2026` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Cyber Defense article |
| 5 | AI-Powered Voice & SMS Scams Surge in Victoria | `ai-voice-scams-senior-cyber-defense-2026` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Senior Workshop article |
| 6 | Digital Literacy for NDIS Participants (Tarneit) | `digital-inclusion-ndis-participants-tarneit-2026` | ❌ Blank / Missing HTML File | Generate authentic 800+ word NDIS Mentoring article |
| 7 | Wyndham Youth Tech Mentorship | `wyndham-youth-tech-mentorship-bridging-divide-2026` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Volunteer article |
| 8 | Practical Ways to Protect Yourself Online | `practical-ways-to-protect-yourself-online-cyber-security-guide` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Guide |
| 9 | Automated Patch Management | `automated-device-updates-patch-management-guide` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Guide |
| 10 | The 3-2-1 Cloud Backup Strategy | `cloud-backups-immutable-storage-ransomware-protection` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Guide |
| 11 | Multi-Factor Authentication (MFA) & Passkeys | `multi-factor-authentication-fido2-passkeys-guide` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Guide |
| 12 | Passphrase Security (4 Random Words) | `secure-passphrases-vs-legacy-passwords-guide` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Guide |
| 13 | Recognising & Defeating Social Engineering | `recognise-and-report-scams-phishing-prevention-guide` | ❌ Blank / Missing HTML File | Generate authentic 800+ word Guide |
| 14 | What Does They rejected the Aussie dream... SBS News Mean | `they-rejected-the-aussie-dream-what-they-bought-instead-cost-130000-sbs-new` | ⛔ Brand Mismatch / Scraper Stub | **PURGE / 410** |
| 15 | Real Estate Open for Inspection Gladstone Central... | `real-estate-open-for-inspection-in-35-state-route-58-gladstone-central-qld-` | ⛔ Toxic Real Estate Ad Stub | **PURGE / 410** |

---

## 2. EZ Mortgage Broker (`ezmortgagebroker.com.au`) Template Audit

### A. Canned Boilerplate Templates (163 Articles)
*These articles feature identical generic text ("The Reserve Bank of Australia and major retail banks have updated residential mortgage assessment benchmarks...") repeated across multiple headlines without unique calculations or suburb data.*

**Top 30 Identified Canned Templates:**
"""

canned_list = audit_data['EZ Mortgage Broker (ezmortgagebroker.com.au)']['canned_boilerplate_templates']
for i, item in enumerate(canned_list[:30]):
    md += f"\n{i+1}. `{item['file']}` — *{item['title']}* ({item['word_count']} words)"

md += f"\n\n*(Total canned boilerplate articles: {len(canned_list)})*\n\n"

md += """### B. Thin Content & Factsheet Stubs (< 250 Words, 329 Articles)
*These files contain minimal text, factsheet fragments, or incomplete stubs that do not satisfy the 600–1,200 word Helpful Content standard.*

**Sample of Identified Thin Stubs:**
"""

thin_list = audit_data['EZ Mortgage Broker (ezmortgagebroker.com.au)']['blank_or_under_250_words']
for i, item in enumerate(thin_list[:30]):
    md += f"\n{i+1}. `{item['file']}` — *{item['title']}* ({item['word_count']} words)"

md += f"\n\n*(Total thin stubs: {len(thin_list)})*\n\n"

md += """---

## 3. High-Quality Verified Articles (Whitelisted for Retention)

**169 Articles** meet all quality gates (word count > 450 words, unique financial calculations, proper heading structure, and genuine broker commentary).

**Sample of Verified Articles:**
"""

verified_list = audit_data['EZ Mortgage Broker (ezmortgagebroker.com.au)']['high_quality_verified']
for i, item in enumerate(verified_list[:20]):
    md += f"\n{i+1}. `{item['file']}` — *{item['title']}* ({item['word_count']} words)"

md += f"\n\n*(Total verified high-quality articles: {len(verified_list)})*\n\n"

md += """---

## 4. Proposed Remediation Strategy

1. **For `finnova.org.au`**:
   - Purge toxic scraper posts #14 & #15 from `posts.json`.
   - Generate full, rich, authentic static HTML articles (800+ words) for the 13 genuine Finnova charity topics (Census Assistance, Cyber Resilience, Refurbished Laptops, Senior Workshops, MFA/Passkeys).
   - Sync `posts.json` and static HTML into `Finnova/pages/blog/` and `Finnova/dist/pages/blog/`.
2. **For `ezmortgagebroker.com.au`**:
   - Safely move the 163 canned boilerplate articles and 329 thin stubs into `archive/purged_templates/`.
   - Remove purged articles from `posts.json` and `sitemap.xml`.
   - Add clean 301/410 redirect rules so search engines de-index templates without 404 penalties.
   - Retain and elevate the **169 verified high-quality articles**.
"""

with open('/Volumes/Samsung SSD 2TB/03. Documents/GitHub/Blogs-Content/QA_AUDIT_REPORT.md', 'w', encoding='utf-8') as fp:
    fp.write(md)

print("✅ Saved QA_AUDIT_REPORT.md successfully.")
