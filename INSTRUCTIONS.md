# 📖 Master Developer Instructions & Article Construction Formula (`INSTRUCTIONS.md`)

This document is the **mandatory developer and automated agent blueprint** for researching, structuring, writing, and publishing short-form, high-impact articles across the Finnova digital ecosystem (`procrm.com.au`, `ezconsultants.com.au`, `finnova.org.au`, `ezmortgagebroker.com.au`).

---

## 🏗️ 1. The Rigid 180–200 Word Article Structure

Every article must strictly follow this high-utility, four-part layout to maximize readability, retention, and search ranking:

```
[H1: Main Title Containing Primary SEO Keyword]

[Hook & Core Keyword (30–40 words)]
Start with a bold, direct statement. Place the primary SEO keyword in the very first sentence.

[H2: Single Subheader Breaking Down the Problem/Context]

[The Problem / Context (40–50 words)]
Briefly explain why this news or topic matters right now based on the researched sources. Keep sentences under 15 words.

[Punchy Value List (60–70 words)]
• Key Point 1: Bold technical takeaway with high-SEO terminology.
• Key Point 2: Quantifiable metric, release feature, or mitigation step.
• Key Point 3: Strategic enterprise or homeowner advantage.

[Call to Action / Next Step (30–40 words)]
Clear conclusion with an outgoing link, phone CTA, or engaging question to drive user interaction.
```

---

## ⏱️ Section-by-Section Breakdown

| Section | Target Word Count | Purpose & Formatting Rules |
| :--- | :---: | :--- |
| **1. Hook & Core Keyword** | **30–40 words** | • Single opening paragraph.<br>• Must place the primary SEO keyword in sentence #1.<br>• Bold key phrases using `<strong>` tags. |
| **2. Problem / Context** | **40–50 words** | • Sits under the single `<h2>` subheader.<br>• Synthesizes current industry challenge, ASD advisory, or market release.<br>• Sentences strictly under 15 words. |
| **3. Punchy Value List** | **60–70 words** | • Exactly **3 bullet points** (`<ul><li>`).<br>• Highly scannable, dense value, zero fluff.<br>• Bolds the leading 2–3 words of each bullet. |
| **4. Call to Action / Next Step** | **30–40 words** | • Closing takeaway.<br>• Direct phone CTA (`1300 050 099`) or interactive consultation link. |
| **Total Article Target** | **180–200 words** | **Mathematically balanced for maximum user engagement and SEO snippet indexing.** |

---

## 🎯 2. High-SEO Keyword Strategy (No Guesswork)

1. **Source Synthesis**:
   * Scrape and synthesize the top 3 ranking articles for the target topic across our verified source list.
2. **Extract Terminology**:
   * Identify the recurring technical terms, official CVE identifiers, platform versions, and product names (e.g., *Salesforce Agentforce*, *Zero-Copy Architecture*, *Essential Eight Level 3*, *First Home Guarantee*).
3. **Natural Insertion**:
   * Blend primary keywords seamlessly into the `<h1>`, the opening sentence of paragraph 1, the `<h2>`, and throughout the 3 bullet points.
   * **Never keyword-stuff**—preserve a natural, authoritative voice.

---

## 🏷️ 3. Semantic HTML & Tagging Best Practices

* **Single `<h1>` Tag**: The article headline. Must contain the primary search keyword.
* **Single `<h2>` Tag**: Exactly one `<h2>` tag for the entire article to maintain pristine semantic hierarchy.
* **`<strong>` Tags**: Bold critical terminology, platform components, and statutory references to anchor the reader’s eye.
* **Sentence Length**: Keep sentences **under 15 words** for maximum readability and high readability scores.
* **Meta Tags**: Always generate a backend `meta_description` strictly **under 160 characters** containing the primary keyword.
* **Tags Array**: Include 4–8 relevant `#hashtags` (e.g., `#SalesforceDevOps`, `#Agentforce`, `#ASDACSC`, `#EssentialEight`, `#PROCRM`).

---

## 📋 Developer Brief Template (Copy & Paste)

When creating or synthesizing an article, use this brief:

> *"Please write a 180–200 word summary on [Topic]. Research the top 3 Google News / industry sources for this topic. Use a clean HTML structure: one H1, one H2, and a 3-item bulleted list. Place the primary high-SEO keyword in the H1 and the first sentence. Bold key terms using `<strong>` tags for scannability. Keep sentences under 15 words to ensure high readability and maximum user engagement."*

---

## 🌐 4. Authoritative Ingestion Sources by Domain

All automated pipelines poll and synthesize from these verified source endpoints on our **6x daily schedule** (**4 AM, 8 AM, 12 PM, 4 PM, 8 PM, 12 AM AEST**):

### A. Salesforce & Enterprise Cloud Sources (`procrm.com.au` & `ezconsultants.com.au` only)
1. `https://www.salesforce.com/news/` (Official Salesforce Newsroom)
2. `https://www.salesforce.com/blog/` (Salesforce 360 Blog)
3. `https://adm-blog-prod.herokuapp.com/blog` (Salesforce Admins Official Blog)
4. `https://developer.salesforce.com/blogs` (Salesforce Developer Blog)
5. `https://www.salesforceben.com/category/news/` (Salesforce Ben Ecosystem News)
6. `https://salesforcedevops.net/index.php/posts/` (Salesforce DevOps & CI/CD)
7. `https://techcrunch.com/tag/salesforce/` (TechCrunch Enterprise Cloud)
8. `https://www.reuters.com/technology/` (Reuters Global Technology Desk)

### B. Cybersecurity & Threat Intelligence Sources (`procrm.com.au`, `ezconsultants.com.au`, `finnova.org.au`)
1. `https://thehackernews.com/` (The Hacker News — Global Zero-Days & Exploit Telemetry)
2. `https://www.itnews.com.au/technology/security` (iTnews Australia — Enterprise Security & Government Tech)
3. `https://www.cyber.gov.au/` (Australian Signals Directorate / ASD ACSC Official Advisories)
4. `https://www.cyberdaily.au/` (Cyber Daily Australia — National Threat Reports & Data Breaches)
5. `https://www.securityweek.com/` (SecurityWeek — Enterprise Cyber Defence & ICS/SCADA Security)
