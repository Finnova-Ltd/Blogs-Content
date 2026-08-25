#!/usr/bin/env python3
import os
import time

PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
site_js_path = os.path.join(PROCRM_DIR, "src", "data", "site.js")

ts = int(time.time())
slug = f"autonomous-enterprise-workflows-procrm-{ts}"
title = f"Autonomous Enterprise Workflows: How PRO CRM Multi-Agent Architecture Slashes Operational Costs ({ts})"

NEW_POST = f"""export const POSTS = [
  {{
    slug: "{slug}",
    title: "{title}",
    date: "2026-08-25",
    author: "Robin Bakshi (Principal AI Architect)",
    category: "AI & Innovation",
    subCategory: "Enterprise AI Architecture",
    region: "National",
    readTime: "6 min read",
    isNew: true,
    badge: "🚀 Live Automation",
    tags: ["#PROCRM", "#Agentforce", "#EnterpriseAI", "#Shorts"],
    image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=80",
    excerpt: "Enterprise AI multi-agent orchestration delivers verified operational efficiency. Learn how PRO CRM deploys autonomous workflows across Australian enterprises.",
    highlights: [
      {{ id: "sec-1", badge: "01. ARCHITECTURE", title: "Governed Workflows", text: "Zero-data retention and immutable audit logs." }}
    ],
    bullets: [
      "Zero-Data-Retention: Ephemeral model sessions.",
      "APRA CPS 234 Compliance: Local sovereign boundaries."
    ],
    body: [
      "Enterprise multi-agent architectures empower organizations to automate complex workflows with complete governance.",
      "Source: PRO CRM Enterprise AI Practice."
    ]
  }},"""

with open(site_js_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("export const POSTS = [", NEW_POST)
with open(site_js_path, "w", encoding="utf-8") as f:
    f.write(content)

os.system(f'cd "{PROCRM_DIR}" && node scripts/generate_rss.js')
os.system(f'cd "{PROCRM_DIR}" && git commit -am "Publish fresh test post {slug}" && git push origin main')
print(f"🚀 Published fresh post {slug} and updated live RSS feed!")
