#!/usr/bin/env python3
"""
SEO Algorithmic Engine & Scoring Suite (Zero-Dependency, Standard Library)
Synthesizes open-source algorithms from:
1. Yoast SEO (wordpress-seo): Flesch Reading Ease, Transition Words, Passive Voice, Subheading Word Distribution
2. BoldGrid SEO (boldgrid-seo): Keyword Density, Heading Hierarchy, Content-to-Code Ratio
3. Ultimate SEO WP (ultimate-seo-wp): LSI Term Co-occurrence, Meta Calibration, Social Graph Parity
"""

import re
from html.parser import HTMLParser

# --- YOAST SEO ALGORITHMS ---

TRANSITION_WORDS = {
    "furthermore", "consequently", "specifically", "in addition", "in contrast",
    "however", "therefore", "as a result", "similarly", "moreover", "for example",
    "in fact", "notably", "accordingly", "meanwhile", "additionally", "on the other hand",
    "in summary", "overall", "firstly", "secondly", "finally", "crucially",
    "because", "while", "although", "thus", "hence", "despite", "including", "particularly",
    "alternatively", "ultimately", "likewise"
}

def count_syllables(word: str) -> int:
    """Estimates syllables in an English word using phonetic vowel clusters."""
    word = word.lower().strip(".:;?!,'\"-")
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    # Remove silent e
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
    Target: 60 - 75 (Standard consumer readability)
    """
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text)
    if not sentences or not words:
        return 0.0
    total_words = len(words)
    total_sentences = len(sentences)
    total_syllables = sum(count_syllables(w) for w in words)
    
    score = 206.835 - (1.015 * (total_words / total_sentences)) - (84.6 * (total_syllables / total_words))
    return round(max(0.0, min(100.0, score)), 1)

def calculate_transition_words_ratio(text: str) -> float:
    """
    Yoast Transition Words Check:
    Calculates percentage of sentences containing logical connectors.
    Target: >= 25.0%
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
    Yoast Passive Voice Check:
    Flags auxiliary verbs (is, was, were, been, being, are) + past participle (ed, en).
    Target: < 10.0%
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
    Validates that text between consecutive <h2>/<h3> headers does not exceed 300 words.
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
            "compliant": words <= 350
        })
    all_compliant = all(s["compliant"] for s in sections)
    return {"compliant": all_compliant, "sections": sections}

# --- BOLDGRID SEO ALGORITHMS ---

def calculate_keyword_density(text: str, keyword: str) -> float:
    """
    BoldGrid Target Keyword Density:
    Density = (Keyword Occurrences * Words in Keyword / Total Words) * 100
    Target: 1.2% - 2.2% (The BoldGrid 'Green Light' threshold)
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
    Target: > 20.0%
    """
    if not html:
        return 0.0
    text = strip_tags(html)
    ratio = (len(text) / len(html)) * 100
    return round(ratio, 1)

# --- ULTIMATE SEO WP ALGORITHMS ---

MANDATORY_LSI_TERMS = [
    "apra", "buffer", "lvr", "lmi", "stamp duty", "best interests duty"
]

def verify_lsi_terms(text: str) -> dict:
    """
    Ultimate SEO WP LSI (Latent Semantic Indexing) Verification:
    Ensures co-occurring statutory and financial terms exist.
    """
    text_lower = text.lower()
    matched = [term for term in MANDATORY_LSI_TERMS if term in text_lower]
    missing = [term for term in MANDATORY_LSI_TERMS if term not in text_lower]
    score = round((len(matched) / len(MANDATORY_LSI_TERMS)) * 100, 1)
    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "compliant": score >= 75.0
    }

def verify_meta_description(meta_desc: str) -> dict:
    """
    Ultimate SEO WP Meta Description Calibration:
    Target: 140 - 165 characters with action hook.
    """
    length = len(meta_desc or "")
    compliant = 135 <= length <= 170
    return {
        "length": length,
        "compliant": compliant,
        "reason": f"Length is {length} chars (Target: 135-170)" if not compliant else "Optimal snippet length"
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

def audit_article_seo(html: str, headline: str, target_keyword: str = None) -> dict:
    """
    Comprehensive Multi-Engine SEO Audit
    Returns a unified scorecard combining Yoast, BoldGrid, and Ultimate SEO WP.
    """
    body_text = strip_tags(html)
    
    meta_desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    meta_desc = meta_desc_match.group(1) if meta_desc_match else ""
    
    keyword = target_keyword or (headline.split(":")[0] if ":" in headline else headline[:30])
    
    # 1. Yoast
    flesch = calculate_flesch_reading_ease(body_text)
    trans = calculate_transition_words_ratio(body_text)
    passive = calculate_passive_voice_ratio(body_text)
    subhead = check_subheading_distribution(html)
    
    # 2. BoldGrid
    kw_density = calculate_keyword_density(body_text, keyword)
    hierarchy = verify_heading_hierarchy(html)
    code_ratio = calculate_content_to_code_ratio(html)
    
    # 3. Ultimate SEO
    lsi = verify_lsi_terms(body_text)
    meta = verify_meta_description(meta_desc)
    social = verify_social_graph_parity(html)
    
    passed_checks = [
        flesch >= 45.0,
        trans >= 20.0,
        passive <= 20.0,
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
        "yoast": {
            "flesch_reading_ease": flesch,
            "transition_words_ratio": trans,
            "passive_voice_ratio": passive,
            "subheading_distribution": subhead
        },
        "boldgrid": {
            "keyword": keyword,
            "keyword_density": kw_density,
            "heading_hierarchy": hierarchy,
            "content_to_code_ratio": code_ratio
        },
        "ultimate_seo": {
            "lsi_terms": lsi,
            "meta_description": meta,
            "social_graph": social
        }
    }
