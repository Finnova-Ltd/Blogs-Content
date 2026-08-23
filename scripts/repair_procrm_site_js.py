#!/usr/bin/env python3
"""
Clean surgical repair of procrm-app/src/data/site.js
"""

import os
import re

PROCRM_SITE_JS = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/data/site.js"

with open(PROCRM_SITE_JS, "r", encoding="utf-8") as f:
    content = f.read()

# Locate export const POSTS = [ and the next post: slug: "practical-ways-to-protect-yourself-online-cyber-security-guide"
prefix_target = "export const POSTS = [\n"
prefix_pos = content.find(prefix_target)

next_post_target = '  {\n    slug: "practical-ways-to-protect-yourself-online-cyber-security-guide",'
next_pos = content.find(next_post_target)

if prefix_pos != -1 and next_pos != -1:
    from apply_comprehensive_blog_layout_fix import generate_comprehensive_article_html, SLUG, TITLE, TODAY_DATE, HERO_IMAGE, EXCERPT
    rich_html = generate_comprehensive_article_html("PRO CRM Australia", "1300 050 099", "info@procrm.com.au")
    
    clean_post_entry = f"""  {{
    slug: "{SLUG}",
    title: "{TITLE}",
    date: "{TODAY_DATE}",
    author: "Robin Bakshi (Principal Architect)",
    category: "Enterprise AI & Cloud",
    subCategory: "Agentforce Integration",
    region: "National",
    readTime: "6 min read",
    isNew: true,
    badge: "⚡ 4-Week Rapid Sprint",
    tags: ["Agentforce", "Salesforce Consulting", "Enterprise AI", "Cost Optimization", "Australia"],
    image: "{HERO_IMAGE}",
    excerpt: "{EXCERPT}",
    highlights: [
      {{ id: "sec-metrics", time: "10:00 AM", title: "Key Performance Metrics", text: "93% reduced time to outcomes, 96% lower management costs, and 58% faster time to value." }},
      {{ id: "sec-1", time: "09:30 AM", title: "Traditional Consulting Trap", text: "Why $250k+ legacy retainers fail in the rapidly evolving AI landscape." }},
      {{ id: "sec-2", time: "09:00 AM", title: "3-Phase Sprint Model", text: "Scoping in Week 1, Atlas Engine & Flow wiring in Weeks 2-3, and Canary Go-Live in Week 4." }},
      {{ id: "sec-3", time: "08:30 AM", title: "Technical Architecture", text: "Zero-Copy Data Cloud lakehouse grounding with strict Einstein Trust Layer security guardrails." }},
      {{ id: "sec-4", time: "08:00 AM", title: "Comparison Matrix", text: "Big 4 $250k+ 9-month retainers vs. our agile squad deployed in under 4 weeks." }},
      {{ id: "sec-5", time: "07:30 AM", title: "Australian Compliance", text: "APRA CPS 234, Essential Eight, and ISO 27001:2022 certified architecture." }}
    ],
    bullets: [
      "93% Reduced Time: Agile 4-week sprint delivery eliminating bloated multi-month discovery phases.",
      "96% Reduced Long-Term Costs: Direct senior architect access with zero vendor lock-in.",
      "Atlas Reasoning Engine: Deterministic topic configuration and Einstein Trust Layer data grounding.",
      "Zero-Copy Federation: Real-time Data Cloud lakehouse integration without ETL software licenses."
    ],
    body: [
      "Traditional Tier-1 consulting firms routinely quote $250,000+ and 6 to 9-month timelines for enterprise AI integrations. By contrast, our specialized engineering methodology deploys fully grounded, compliant Agentforce autonomous agents into production in under 4 weeks at up to 70% lower upfront investment and 96% reduced ongoing overhead.",
      "Here is how it works: Week 1 (ROI-Driven Roadmap), Weeks 2–3 (Atlas Reasoning & Flow Automation Wiring), and Week 4 (Canary Go-Live & Usage Forecasting).",
      "Why We Cost a Fraction of Big Consulting Houses: 100% Senior Certified Principal Architects with zero junior trainees billing on your invoice.",
      "Source: PRO CRM Enterprise AI Solutions & Australian Cloud Architecture Desk."
    ],
    htmlContent: `{rich_html.replace('`', '\\`')}`
  }},
"""
    new_content = content[:prefix_pos + len(prefix_target)] + clean_post_entry + content[next_pos:]
    with open(PROCRM_SITE_JS, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ Successfully repaired procrm-app/src/data/site.js cleanly!")
else:
    print(f"❌ Could not locate boundaries: prefix_pos={prefix_pos}, next_pos={next_pos}")
