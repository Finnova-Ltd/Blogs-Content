#!/usr/bin/env python3
import os
import time

PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
site_js_path = os.path.join(PROCRM_DIR, "src", "data", "site.js")

ts = int(time.time())
slug = f"procrm-ai-lakehouse-governance-{ts}"
title = f"PRO CRM Autonomous Lakehouse AI Governance ({ts})"

NEW_POST = f"""export const POSTS = [
  {{
    slug: "{slug}",
    title: "{title}",
    date: "2026-08-26",
    author: "Robin Bakshi (Principal AI Architect)",
    category: "AI & Innovation",
    subCategory: "Enterprise AI Architecture",
    region: "National",
    readTime: "5 min read",
    isNew: true,
    badge: "⚡ Governed AI",
    tags: ["#PROCRM", "#EnterpriseAI", "#Shorts", "#Agentforce"],
    image: "https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=1200",
    videoUrl: "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/procrm_pro_crm_autonomous_multi__ultimate_avatar.mp4",
    excerpt: "Enterprise multi-agent architectures empower organizations to automate complex workflows with complete governance.",
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

os.system(f'cd "{PROCRM_DIR}" && node scripts/generate_rss.js && git commit -am "Publish fresh live trigger post {slug}" && git push origin main')
print(f"🚀 Fresh post published for instant trigger: {title}")
