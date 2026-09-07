#!/usr/bin/env python3
"""
Unit tests for the calibrated SEO Algorithmic & Information Gain Engine
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
    verify_code_or_visual_presence,
    detect_domain_profile,
    audit_article_seo
)

SAMPLE_TECH_ARTICLE_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Your Three-Year Salesforce Backlog Is Now This Week's Sprint | EZ Consultants</title>
  <meta name="description" content="Learn how Agentic IDEs, MCP servers, and automated CI/CD pipelines eliminate enterprise Salesforce technical debt while maintaining APRA CPS 234 compliance.">
  <meta property="og:title" content="Your Three-Year Salesforce Backlog Is Now This Week's Sprint">
  <meta property="og:description" content="Eliminate Salesforce technical debt with Claude Code, Cursor, and MCP Tooling API integration.">
  <meta property="og:image" content="https://ezconsultants.com.au/assets/salesforce-mcp-hero.webp">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="https://ezconsultants.com.au/pages/blog/your-three-year-salesforce-backlog-is-now-this-week-s-sprint.html">
</head>
<body>
  <h1>Your Three-Year Salesforce Backlog Is Now This Week's Sprint</h1>
  <article class="article-a4-sheet">
    <h2>1. The Architectural Shift: The Agentic Developer Workspace</h2>
    <p>Enterprise Salesforce teams struggle with technical debt, specifically legacy triggers and untested batches. However, agentic coding tools like Claude Code and Cursor connect via MCP to query the Tooling API and scratch org metadata directly.</p>
    <pre><code>{ "mcpServers": { "salesforce-tooling": { "command": "node" } } }</code></pre>
    <h2>2. Refactoring Monolithic Triggers to fflib</h2>
    <p>Furthermore, autonomous refactoring decomposes 1,500-line triggers into domain and selector classes, ensuring governor limits remain protected under APRA CPS 234 and ISO 27001 data governance.</p>
    <table><tr><th>Layer</th><th>Tool</th><th>Standard</th></tr><tr><td>Static Analysis</td><td>PMD</td><td>with sharing</td></tr></table>
  </article>
</body>
</html>
"""

def test_calibrated_flesch_reading_ease():
    text = "Enterprise engineering teams must tackle technical debt across their Salesforce orgs. Using MCP servers with Claude Code helps developers deploy clean code to scratch orgs."
    score = calculate_flesch_reading_ease(text)
    assert score >= 40.0, f"Expected B2B readability >= 40.0, got {score}"

def test_calibrated_transition_words():
    text = "Enterprise teams face technical debt. However, MCP servers bridge the platform gap. Furthermore, automated CI pipelines validate branch coverage."
    ratio = calculate_transition_words_ratio(text)
    assert 50.0 <= ratio <= 100.0

def test_domain_detection():
    tech_text = "Salesforce Apex triggers and MCP servers with Tooling API integration"
    fin_text = "Melbourne home buyers calculate stamp duty and APRA buffer repayments"
    assert detect_domain_profile(tech_text, "Salesforce") == "salesforce_tech"
    assert detect_domain_profile(fin_text, "Mortgage") == "mortgage_finance"

def test_domain_specific_lsi_terms():
    tech_text = "We use MCP, Tooling API, governor limits, Apex, fflib, scratch orgs, CI/CD, and APRA CPS 234."
    res = verify_lsi_terms(tech_text, "salesforce_tech")
    assert res["compliant"] is True
    assert res["score"] >= 70.0

def test_code_and_visual_presence():
    res = verify_code_or_visual_presence(SAMPLE_TECH_ARTICLE_HTML)
    assert res["compliant"] is True
    assert res["has_code"] is True
    assert res["has_table"] is True

def test_full_b2b_seo_audit():
    audit = audit_article_seo(SAMPLE_TECH_ARTICLE_HTML, "Your Three-Year Salesforce Backlog Is Now This Week's Sprint")
    assert audit["passed"] is True
    assert audit["overall_score"] >= 80.0
    assert audit["domain"] == "salesforce_tech"
    assert audit["boldgrid"]["code_and_visual_presence"]["compliant"] is True
