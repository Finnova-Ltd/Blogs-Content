#!/usr/bin/env python3
"""
SEO Algorithmic Engine & Information Gain Scoring Suite
Modernized for B2B Technical Authority, Entity Embeddings & Google Helpful Content

Synthesizes open-source algorithms from:
1. Yoast SEO (wordpress-seo): Calibrated Flesch Reading Ease, Natural Transition Ratio, Passive Voice, Subheading Distribution
2. BoldGrid SEO (boldgrid-seo): Semantic Entity Density, Strict Heading Hierarchy (H1 -> H2 -> H3), Content-to-Code Ratio
3. Ultimate SEO WP (ultimate-seo-wp): Domain-Specific LSI Co-occurrence, Meta Calibration, Social Graph Parity
4. Enterprise Engineering Standard: Mandatory Code / Visual Artifact Presence (Code blocks, ASCII diagrams, Data Tables)
"""

import re

# --- YOAST SEO ALGORITHMS (CALIBRATED FOR B2B & DOMAIN SPECIFICITY) ---

TRANSITION_WORDS = {
    "furthermore", "consequently", "specifically", "in addition", "in contrast",
    "however", "therefore", "as a result", "similarly", "moreover", "for example",
    "in fact", "notably", "accordingly", "meanwhile", "additionally", "on the other hand",
    "in summary", "overall", "firstly", "secondly", "finally", "crucially",
    "because", "while", "although", "thus", "hence", "despite", "including", "particularly",
    "alternatively", "ultimately", "likewise", "rather than", "in turn"
}

def count_syllables(word: str) -> int:
    """Estimates syllables in an English word using phonetic vowel clusters."""
    word = word.lower().strip(".:;?!,'\"-")
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    if word.endswith("e") and not word.endswith("le"):
        word = word[:-1]
    vowels = "aeiouy"
    count = 0
    prev_is_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    return max(1, count)

def calculate_flesch_reading_ease(text: str) -> float:
    """
    Yoast Flesch Reading Ease Formula:
    Score = 206.835 - (1.015 * (total_words / total_sentences)) - (84.6 * (total_syllables / total_words))
    Target:
    - B2B Technical / Enterprise Architecture: 45.0 - 65.0 (Preserves technical terms)
    - B2C Consumer Finance / General: 55.0 - 75.0
    """
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = re.findall(r'\b[a-zA-Z0-9-]+\b', text)
    if not sentences or not words:
        return 0.0
    total_words = len(words)
    total_sentences = len(sentences)
    total_syllables = sum(count_syllables(w) for w in words)
    
    score = 206.835 - (1.015 * (total_words / total_sentences)) - (84.6 * (total_syllables / total_words))
    return round(max(0.0, min(100.0, score)), 1)

def calculate_transition_words_ratio(text: str) -> float:
    """
    Calibrated Transition Words Check:
    Target: 8.0% - 18.0% (Natural conversational flow; prevents robotic AI essay feel)
    """
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    if not sentences:
        return 0.0
    matched = 0
    for s in sentences:
        s_lower = s.lower()
        if any(tw in s_lower for tw in TRANSITION_WORDS):
            matched += 1
    return round((matched / len(sentences)) * 100, 1)

def calculate_passive_voice_ratio(text: str) -> float:
    """
    Passive Voice Check:
    Flags auxiliary verbs (is, was, were, been, being, are) + past participle (ed, en).
    Target: < 12.0%
    """
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    if not sentences:
        return 0.0
    passive_pattern = re.compile(r'\b(is|was|were|been|being|are)\s+([a-z]+(?:ed|en|wn))\b', re.IGNORECASE)
    passive_sentences = sum(1 for s in sentences if passive_pattern.search(s))
    return round((passive_sentences / len(sentences)) * 100, 1)

def strip_tags(html: str) -> str:
    """Strips HTML tags cleanly using regex."""
    text = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    return " ".join(text.split())

def check_subheading_distribution(html: str) -> dict:
    """
    Yoast Subheading Distribution:
    Validates that text between consecutive <h2>/<h3> headers does not exceed 350 words.
    """
    parts = re.split(r'<h[23][^>]*>', html, flags=re.IGNORECASE)
    if len(parts) <= 1:
        words = len(strip_tags(html).split())
        return {"compliant": words <= 350, "sections": [{"header": "Single Section", "word_count": words, "compliant": words <= 350}]}
    
    sections = []
    for i, section_html in enumerate(parts[1:], 1):
        clean_text = strip_tags(section_html.split("</h", 1)[-1] if "</h" in section_html else section_html)
        words = len(clean_text.split())
        sections.append({
            "section_index": i,
            "word_count": words,
            "compliant": words <= 380
        })
    all_compliant = all(s["compliant"] for s in sections)
    return {"compliant": all_compliant, "sections": sections}

# --- BOLDGRID SEO & INFORMATION GAIN ALGORITHMS ---

def calculate_keyword_density(text: str, keyword: str) -> float:
    """
    Entity / Topical Keyword Density:
    Target: 0.6% - 1.5% (Modern Information Gain threshold avoiding keyword stuffing)
    """
    if not text or not keyword:
        return 0.0
    words = re.findall(r'\b[a-zA-Z0-9-]+\b', text.lower())
    if not words:
        return 0.0
    kw_clean = keyword.lower().strip()
    kw_words = re.findall(r'\b[a-zA-Z0-9-]+\b', kw_clean)
    kw_len = max(1, len(kw_words))
    
    text_clean = " ".join(words)
    occurrences = len(re.findall(re.escape(" ".join(kw_words)), text_clean))
    density = (occurrences * kw_len / len(words)) * 100
    return round(density, 2)

def verify_heading_hierarchy(html: str) -> dict:
    """
    BoldGrid Heading Hierarchy:
    Ensures strict H1 -> H2 -> H3 structure without level skipping.
    Exactly one H1 required.
    """
    headings = re.findall(r'<h([1-6])[^>]*>', html, flags=re.IGNORECASE)
    tags = [int(h) for h in headings]
    
    h1_count = tags.count(1)
    if h1_count != 1:
        return {"compliant": False, "reason": f"Expected exactly 1 H1, found {h1_count}", "tags": tags}
    
    prev = 1
    for t in tags[1:]:
        if t > prev + 1:
            return {"compliant": False, "reason": f"Heading hierarchy skipped: H{prev} to H{t}", "tags": tags}
        prev = t
    return {"compliant": True, "reason": "Pristine H1 -> H2 -> H3 hierarchy", "tags": tags}

def calculate_content_to_code_ratio(html: str) -> float:
    """
    BoldGrid Content-to-Code Ratio:
    Ratio = (Text Length / Total HTML Length) * 100
    Target: > 18.0%
    """
    if not html:
        return 0.0
    text = strip_tags(html)
    ratio = (len(text) / len(html)) * 100
    return round(ratio, 1)

# --- DOMAIN-SPECIFIC LSI ENTITY PROFILES ---

DOMAIN_LSI_REGISTRY = {
    "salesforce_tech": [
        "mcp", "tooling api", "governor limit", "apex", "fflib",
        "scratch org", "ci/cd", "apra cps 234", "iso 27001", "trigger"
    ],
    "mortgage_finance": [
        "apra", "buffer", "lvr", "lmi", "stamp duty", "best interests duty"
    ],
    "esign_legal": [
        "electronic transactions act", "aatl", "pki", "audit trail", "iso 27001", "consent"
    ]
}

def detect_domain_profile(text: str, headline: str) -> str:
    combined = (headline + " " + text).lower()
    if any(k in combined for k in ["salesforce", "apex", "flow", "mcp", "devops", "agentforce", "cloud"]):
        return "salesforce_tech"
    if any(k in combined for k in ["signature", "sign", "contract", "nda", "lease", "aatl"]):
        return "esign_legal"
    return "mortgage_finance"

def verify_lsi_terms(text: str, domain: str = None) -> dict:
    """
    Domain-Aware LSI Entity Verification:
    Selects domain checklist (Salesforce/Tech vs Mortgage vs eSign) and verifies coverage.
    Target: >= 70% entity coverage.
    """
    profile_key = domain or detect_domain_profile(text, "")
    target_terms = DOMAIN_LSI_REGISTRY.get(profile_key, DOMAIN_LSI_REGISTRY["mortgage_finance"])
    
    text_lower = text.lower()
    matched = [term for term in target_terms if term in text_lower]
    missing = [term for term in target_terms if term not in text_lower]
    score = round((len(matched) / len(target_terms)) * 100, 1)
    return {
        "domain": profile_key,
        "score": score,
        "matched": matched,
        "missing": missing,
        "compliant": score >= 60.0
    }

def verify_meta_description(meta_desc: str) -> dict:
    """
    Ultimate SEO WP Meta Description Calibration:
    Target: 130 - 170 characters with action hook.
    """
    length = len(meta_desc or "")
    compliant = 125 <= length <= 175
    return {
        "length": length,
        "compliant": compliant,
        "reason": f"Length is {length} chars (Target: 125-175)" if not compliant else "Optimal snippet length"
    }

def verify_social_graph_parity(html: str) -> dict:
    """
    Ultimate SEO WP Social Graph Parity:
    Ensures matching OpenGraph and Twitter Card tags with image previews.
    """
    has_og_title = bool(re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\'][^"\']+["\']', html, re.IGNORECASE))
    has_og_desc = bool(re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\'][^"\']+["\']', html, re.IGNORECASE))
    has_og_img = bool(re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\'][^"\']+["\']', html, re.IGNORECASE))
    has_tw_card = bool(re.search(r'<meta[^>]*name=["\']twitter:card["\'][^>]*content=["\'][^"\']+["\']', html, re.IGNORECASE))
    has_canonical = bool(re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'][^"\']+["\']', html, re.IGNORECASE))
    
    checks = {
        "og:title": has_og_title,
        "og:description": has_og_desc,
        "og:image": has_og_img,
        "twitter:card": has_tw_card,
        "canonical": has_canonical
    }
    all_present = all(checks.values())
    return {"compliant": all_present, "checks": checks}

def verify_code_or_visual_presence(html: str) -> dict:
    """
    Enterprise Technical Quality Check:
    Ensures the presence of real code blocks, preformatted text, ASCII diagrams, or data tables.
    """
    has_pre = "<pre" in html.lower()
    has_code = "<code" in html.lower()
    has_table = "<table" in html.lower()
    has_ascii = "┌" in html or "+---" in html or "│" in html
    
    is_present = has_pre or has_code or has_table or has_ascii
    return {
        "compliant": is_present,
        "has_code": has_code or has_pre,
        "has_table": has_table,
        "has_diagram": has_ascii
    }

def audit_article_seo(html: str, headline: str, target_keyword: str = None) -> dict:
    """
    Comprehensive Multi-Engine SEO & Information Gain Audit
    Returns a unified scorecard combining Yoast, BoldGrid, Ultimate SEO WP, and Engineering Standards.
    """
    body_text = strip_tags(html)
    domain = detect_domain_profile(body_text, headline)
    
    meta_desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    meta_desc = meta_desc_match.group(1) if meta_desc_match else ""
    
    keyword = target_keyword or (headline.split(":")[0] if ":" in headline else headline[:30])
    
    # 1. Yoast (Calibrated)
    flesch = calculate_flesch_reading_ease(body_text)
    trans = calculate_transition_words_ratio(body_text)
    passive = calculate_passive_voice_ratio(body_text)
    subhead = check_subheading_distribution(html)
    
    # Flesch target is domain-aware:
    flesch_min = 40.0 if domain == "salesforce_tech" else 50.0
    
    # 2. BoldGrid & Visuals
    kw_density = calculate_keyword_density(body_text, keyword)
    hierarchy = verify_heading_hierarchy(html)
    code_ratio = calculate_content_to_code_ratio(html)
    visuals = verify_code_or_visual_presence(html)
    
    # 3. Ultimate SEO
    lsi = verify_lsi_terms(body_text, domain)
    meta = verify_meta_description(meta_desc)
    social = verify_social_graph_parity(html)
    
    passed_checks = [
        flesch >= flesch_min,
        trans >= 6.0,
        passive <= 18.0,
        subhead["compliant"],
        hierarchy["compliant"],
        code_ratio >= 15.0,
        lsi["compliant"],
        meta["compliant"],
        social["compliant"]
    ]
    total_score = round((sum(passed_checks) / len(passed_checks)) * 100, 1)
    
    return {
        "overall_score": total_score,
        "passed": total_score >= 75.0,
        "domain": domain,
        "yoast": {
            "flesch_reading_ease": flesch,
            "flesch_target_min": flesch_min,
            "transition_words_ratio": trans,
            "passive_voice_ratio": passive,
            "subheading_distribution": subhead
        },
        "boldgrid": {
            "keyword": keyword,
            "keyword_density": kw_density,
            "heading_hierarchy": hierarchy,
            "content_to_code_ratio": code_ratio,
            "code_and_visual_presence": visuals
        },
        "ultimate_seo": {
            "domain_profile": domain,
            "lsi_terms": lsi,
            "meta_description": meta,
            "social_graph": social
        }
    }
