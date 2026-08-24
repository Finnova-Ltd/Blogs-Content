# 📜 Finnova Ecosystem Master Publishing Rules & Editorial Standards (`RULE.md`)

This document establishes the **strict, mandatory editorial and frontend architecture standards** that must be checked and enforced for **every single article** across all Finnova platforms (`procrm.com.au`, `ezconsultants.com.au`, `ezmortgagebroker.com.au`, `finnova.org.au`).

---

## 🛑 1. Word Count & Section Depth Rule (STRICT)

* **Minimum 180–200 words per section**: Every single subsection, key takeaway, or mitigation step must be thoroughly articulated with technical depth, real-world context, and actionable guidance.
* **No Shallow 1-Line Summaries**: Never write a 20-word summary for a critical advisory. Break down the architecture, the threat vector/market condition, the step-by-step fix, and the strategic takeaway.
* **Overall Article Length**: Articles must range between **800 to 1,500+ words** across 3–5 dedicated, high-value sections.

---

## 🚫 2. End-User Tone Rule — NO "Executive Summary" Jargon

* **Never Use "Executive Summary"**: Blog articles are read by practitioners, developers, business owners, and mortgage clients. Avoid dry corporate jargon like *"Executive Summary & Direct Answer"*.
* **Write for the End-User**:
  * Use engaging, descriptive section headings (e.g., *"What This Means for Your Business"*, *"Step-by-Step Fix Guide"*, *"How Our Team Resolves This"*, *"Key Takeaways for Homeowners"*).
  * Speak directly to the reader's real-world operational challenges.
  * Provide plain-language explanations before diving into technical configurations.

---

## 📌 3. Column 2 (Sidebar) Architecture & Sticky Rule

* **Guaranteed Locked Sticky Positioning**:
  * Column 2 must use `position: "sticky", top: "105px"` with clean clearance below the fixed site header (~96px).
  * **Zero Inner Scrolling**: The sidebar must **NEVER** use `overflow-y: auto` or height clipping. It must fit cleanly within a standard laptop viewport (**total height ≤ 500px**) and remain 100% rigidly fixed in full view as the user scrolls Column 1.
* **Col 2 Component Structure**:
  1. **Highlights Timeline Widget**: Compact red header (`Highlights · In this article`), 3–4 linked section anchors.
  2. **Related News Widget**: Compact thumbnails (`36px`–`40px`), 1-line titles, and dates.
  3. **Direct Contact Card**: Compact 1-click CTA button (`Call 1300 ...` or `Book Discovery Call`).

---

## 🎨 4. 100% Crisp Light-Theme Design Rule

* **Zero Dark/Black Boxes**: No `bg-slate-950`, black card containers, or dark overlays on light-theme websites.
* **Card Image Aesthetics**:
  * Every card must use a high-resolution, light-themed, professional image (Unsplash/enterprise photography).
  * Card containers must use soft background gradients (e.g. `bg-gradient-to-br from-blue-50 via-slate-50 to-indigo-50 border border-slate-100`).
  * Automatic `onError` image fallback must be present on every image tag.

---

## 🏷️ 5. Badging, Ratings & Hashtags Rule

* **Official Threat Ratings**: For cybersecurity advisories, prominently feature official ASD ACSC rating badges:
  * **`🚨 Alert Rating: 🟠 High`** or **`🛡️ Threat Advisory: 🟡 Moderate`**.
* **Search & Social Hashtags**: Every article must include at least 4–8 relevant `#hashtags` (e.g., `#ASDACSC`, `#AlertRatingHigh`, `#EssentialEight`, `#SalesforceDevOps`, `#PROCRM`, `#Finnova`).

---

## ⏰ 6. Timezone & Date Formatting Rule

* **Australian Eastern Standard Time (AEST / UTC+10)**: All publication timestamps and date badges must strictly reflect Australian Eastern local dates (e.g., **`25 AUG`**, **`25 August 2026`**).
* **Automated 6x Daily Publishing**: Run triggers at **4:00 AM, 8:00 AM, 12:00 PM, 4:00 PM, 8:00 PM, 12:00 AM AEST**.

---

## 🔍 Pre-Publish Verification Checklist

Before committing and deploying any article:
- [ ] Is every section **at least 180–200 words**?
- [ ] Is corporate jargon like **"Executive Summary" completely removed**?
- [ ] Is **Col 2 sticky and locked at `top: 105px`** without overflow clipping or inner scrollbars?
- [ ] Are all card backgrounds **100% light-theme** with valid image fallbacks?
- [ ] Are official **Alert Rating badges** and **#hashtags** present?
- [ ] Does the date badge match **Australian Eastern Time (AEST)**?
