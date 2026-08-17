# EZ Mortgage Broker — Blog Typography & Editorial Design System

This specification defines the typography standards, responsive font scales, font stacks, and line-height ratios across all EZ Mortgage Broker articles, blog guides, insights, and state calculators.

---

## 1. Font Family Stacks

### A. Editorial & Reading Content (Headings & Article Body)
* **Primary Role**: Article Headlines, Section Subheadings, Lead Paragraphs, and Body Content.
* **Font Family Stack**:
  ```css
  font-family: sueca_hd_regular, Merriweather, Georgia, "Times New Roman", Times, serif;
  ```

### B. UI Elements, Metadata, Badges & Labels
* **Primary Role**: Author Byline, Category Pills, Table Headers, Unit/Widget Headings, Form Labels, and CTA Buttons.
* **Font Family Stack**:
  ```css
  font-family: suecanano_regular, Lato, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, "Lucida Grande", sans-serif;
  ```

---

## 2. Responsive Font Scale & Hierarchy

### 1. Main Article Headline (`<h1>`)
* **Font Family**: `sueca_hd_regular, Merriweather, Georgia, Times, serif`
* **Weight**: `700` / `900`
* **Line Height**: `1.2`
* **Letter Spacing**: `-0.02em`
* **Responsive Breakpoints**:
  * **Mobile (< 768px)**: `1.6875rem` (~27px)
  * **Tablet (≥ 768px)**: `2.5625rem` (~41px)
  * **Desktop (≥ 1020px)**: `3.0000rem` (48px)

### 2. Section Subheadings (`<h2>`)
* **Article Body Subheadings (`<h2>`)**:
  * **Font Family**: `sueca_hd_regular, Merriweather, Georgia, Times, serif`
  * **Font Size**: `1.875rem` (30px)
  * **Font Weight**: `700`
  * **Line Height**: `1.3`
  * **Margin**: `32px 0 16px 0`
* **Widget / Unit Headings (`<h3>` / `.widget-heading` / `.unit-heading`)**:
  * **Font Family**: `suecanano_regular, Lato, Arial, "Lucida Grande", sans-serif`
  * **Font Size**: `0.875rem` (14px)
  * **Font Weight**: `700` / `800`
  * **Text Transform**: `uppercase`
  * **Letter Spacing**: `0.06em`

### 3. Article Body & Narrative Paragraphs (`<p>`)
* **Font Family**: `sueca_hd_regular, Georgia, Times, serif`
* **Font Weight**: `400`
* **Line Height**: `1.6`
* **Paragraph Spacing**: `1.25rem`
* **Responsive Breakpoints**:
  * **Mobile (< 768px)**: `1.000rem` (16px)
  * **Tablet & Desktop (≥ 768px)**: `1.125rem` (18px)

### 4. Lead Paragraph / Executive Summary (`.lead-text`, `.article-summary`)
* **Font Family**: `sueca_hd_regular, Georgia, Times, serif`
* **Font Size**: `1.25rem` (20px)
* **Font Weight**: `400`
* **Line Height**: `1.65`
* **Color**: `#1E293B`

### 5. Metadata, Badges, Table Headers & Captions
* **Category Badges & Section Tags**: `0.8125rem` (13px), `font-weight: 800`, uppercase, sans-serif.
* **Author / Date / Read Time Meta**: `0.875rem` (14px), sans-serif, color `#64748B`.
* **Data Table Headers (`<th>`)**: `0.92rem` (~14.7px), `font-weight: 800`, uppercase, letter-spacing `0.05em`.
* **Data Table Content (`<td>`)**: `0.95rem` (~15.2px), `line-height: 1.6`.

---

## 3. CSS Utility Implementation

```css
/* Core Editorial Typography Tokens */
:root {
  --font-serif-editorial: sueca_hd_regular, Merriweather, Georgia, "Times New Roman", Times, serif;
  --font-sans-ui: suecanano_regular, Lato, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, "Lucida Grande", sans-serif;
  
  --fs-h1-mobile: 1.6875rem;
  --fs-h1-tablet: 2.5625rem;
  --fs-h1-desktop: 3rem;
  
  --fs-h2: 1.875rem;
  --fs-widget-heading: 0.875rem;
  
  --fs-body-mobile: 1rem;
  --fs-body-desktop: 1.125rem;
  
  --lh-body: 1.6;
}

/* Article Heading Scale */
.article-content h1,
.article-header h1 {
  font-family: var(--font-serif-editorial);
  font-size: var(--fs-h1-mobile);
  line-height: 1.2;
  letter-spacing: -0.02em;
  font-weight: 700;
  color: #0A2540;
  margin-bottom: 16px;
}

@media (min-width: 768px) {
  .article-content h1,
  .article-header h1 {
    font-size: var(--fs-h1-tablet);
  }
}

@media (min-width: 1020px) {
  .article-content h1,
  .article-header h1 {
    font-size: var(--fs-h1-desktop);
  }
}

/* Section Subheadings */
.article-content h2 {
  font-family: var(--font-serif-editorial);
  font-size: var(--fs-h2);
  line-height: 1.3;
  font-weight: 700;
  color: #0A2540;
  margin: 36px 0 16px;
}

/* Widget / Unit Headings */
.widget-heading,
.unit-heading,
.sidebar-block-title {
  font-family: var(--font-sans-ui);
  font-size: var(--fs-widget-heading);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #64748B;
}

/* Reading Body Text */
.article-content p,
.article-body-text {
  font-family: var(--font-serif-editorial);
  font-size: var(--fs-body-mobile);
  line-height: var(--lh-body);
  color: #334155;
  margin-bottom: 20px;
}

@media (min-width: 768px) {
  .article-content p,
  .article-body-text {
    font-size: var(--fs-body-desktop);
  }
}
```
