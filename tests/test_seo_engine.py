#!/usr/bin/env python3
"""
Unit tests for the open-source SEO Algorithmic Engine (Yoast, BoldGrid, Ultimate SEO WP)
"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from scripts.seo_engine import (
    calculate_flesch_reading_ease,
    calculate_transition_words_ratio,
    calculate_passive_voice_ratio,
    check_subheading_distribution,
    calculate_keyword_density,
    verify_heading_hierarchy,
    calculate_content_to_code_ratio,
    verify_lsi_terms,
    verify_meta_description,
    verify_social_graph_parity,
    audit_article_seo
)

SAMPLE_ARTICLE_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>First Home Buyer Suburb Rankings 2026: Melbourne Under 600K</title>
  <meta name="description" content="Discover the top Melbourne suburbs where first home buyers can purchase under 600K in 2026, saving up to $31,070 in stamp duty with APRA buffer modeling.">
  <meta property="og:title" content="First Home Buyer Suburb Rankings 2026">
  <meta property="og:description" content="Sub-600k Melbourne suburbs for first home buyers with real median prices.">
  <meta property="og:image" content="https://ezmortgagebroker.com.au/assets/hero.webp">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="https://ezmortgagebroker.com.au/pages/blog/suburb-rankings.html">
</head>
<body>
  <h1>First Home Buyer Suburb Rankings 2026: Where Melburnians Can Still Buy Under 600K</h1>
  <article class="article-a4-sheet">
    <h2>1. Market Analysis & Suburb Rankings</h2>
    <p>Melbourne first home buyers face significant serviceability hurdles, specifically under the current APRA buffer. However, outer growth corridors like Melton, Werribee, and Frankston North continue to offer median prices under $600,000. Furthermore, purchasers benefit from a complete $0 stamp duty exemption. Consequently, buyers save up to $31,070 in state taxes while maintaining an LVR under 95% with manageable LMI.</p>
    <h2>2. Pricing & Repayment Modeling</h2>
    <p>In addition, our mortgage team analyzed deposit tiers. Specifically, a 5% deposit requires LMI capitalisation, whereas a 20% deposit eliminates LMI entirely. Therefore, borrower affordability improves substantially. Meanwhile, our Best Interests Duty (BID) ensures every loan structure aligns with client financial objectives.</p>
  </article>
</body>
</html>
"""

def test_yoast_flesch_reading_ease():
    text = "The cat sat on the mat. It was a sunny day. We were happy."
    score = calculate_flesch_reading_ease(text)
    assert score >= 70.0, f"Expected high readability, got {score}"

def test_yoast_transition_words():
    text = "Furthermore, home buyers must calculate their deposit. Consequently, they save interest. However, serviceability matters."
    ratio = calculate_transition_words_ratio(text)
    assert ratio == 100.0, f"Expected 100% transitions, got {ratio}"

def test_yoast_subheading_distribution():
    res = check_subheading_distribution(SAMPLE_ARTICLE_HTML)
    assert res["compliant"] is True
    assert len(res["sections"]) == 2

def test_boldgrid_keyword_density():
    text = "first home buyer suburb rankings are important. A first home buyer needs good advice."
    density = calculate_keyword_density(text, "first home buyer")
    assert density > 0.0

def test_boldgrid_heading_hierarchy():
    res = verify_heading_hierarchy(SAMPLE_ARTICLE_HTML)
    assert res["compliant"] is True
    assert res["tags"] == [1, 2, 2]

def test_ultimate_seo_lsi_terms():
    text = "We assess the APRA buffer, LVR, LMI, stamp duty, and statutory Best Interests Duty."
    res = verify_lsi_terms(text)
    assert res["compliant"] is True
    assert res["score"] == 100.0
    assert len(res["missing"]) == 0

def test_ultimate_seo_meta_description():
    meta = "Discover the top Melbourne suburbs where first home buyers can purchase under 600K in 2026, saving up to $31,070 in stamp duty with APRA buffer modeling."
    res = verify_meta_description(meta)
    assert res["compliant"] is True
    assert 140 <= res["length"] <= 165

def test_ultimate_seo_social_parity():
    res = verify_social_graph_parity(SAMPLE_ARTICLE_HTML)
    assert res["compliant"] is True

def test_full_article_seo_audit():
    audit = audit_article_seo(SAMPLE_ARTICLE_HTML, "First Home Buyer Suburb Rankings 2026: Where Melburnians Can Still Buy Under 600K")
    assert audit["passed"] is True
    assert audit["overall_score"] >= 80.0
    assert "yoast" in audit
    assert "boldgrid" in audit
    assert "ultimate_seo" in audit
