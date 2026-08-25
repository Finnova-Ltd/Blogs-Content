#!/usr/bin/env python3
import os
import json

PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
site_js_path = os.path.join(PROCRM_DIR, "src", "data", "site.js")

NEW_POST = """export const POSTS = [
  {
    slug: "agentforce-multi-agent-governance-playbook-2026",
    title: "Agentforce Multi-Agent Governance: How Australian CIOs Prevent Hallucinations and Enforce APRA CPS 234 Compliance",
    date: "2026-08-25",
    author: "Robin Bakshi (Principal AI Architect)",
    category: "AI & Innovation",
    subCategory: "Enterprise AI Governance",
    region: "National",
    readTime: "7 min read",
    isNew: true,
    badge: "⚡ New Blueprint",
    tags: ["#Agentforce", "#AIGovernance", "#APRA", "#CPS234", "#Salesforce", "#PROCRM", "#EnterpriseAI"],
    image: "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=80",
    excerpt: "Deploying autonomous AI agents requires rock-solid guardrails. Discover how Australian enterprises enforce zero-retention policies, role-based tool access, and deterministic audit trails across multi-agent Agentforce deployments.",
    highlights: [
      { id: "sec-gov", badge: "01. GOVERNANCE", title: "Einstein Trust Layer Guardrails", text: "Automated masking of PII, credit cards, and TFNs before LLM grounding." },
      { id: "sec-apra", badge: "02. COMPLIANCE", title: "APRA CPS 234 Alignment", text: "Immutable session logging and sovereign Australian data residency." },
      { id: "sec-deploy", badge: "03. ARCHITECTURE", title: "Zero-Copy Data Access", text: "Connecting Data Cloud and Snowflake with zero ETL data movement." }
    ],
    bullets: [
      "Zero-Data-Retention: Enforcing ephemeral LLM sessions with verified Einstein Trust Layer gateways.",
      "APRA CPS 234 & Essential 8: Complete cryptographic audit trails for all agentic tool invocations.",
      "Role-Based Agent Boundaries: Isolating CRM action permissions to prevent privilege escalation.",
      "Production Go-Live: Fixed-sprint governance implementation by certified Australian architects."
    ],
    body: [
      "As Australian enterprise leaders transition from conversational AI pilots to autonomous multi-agent deployments, establishing robust governance frameworks has become the top priority for CIOs and Chief Risk Officers.",
      "Without deterministic guardrails, autonomous agents risk executing unverified database writes or exposing sensitive customer PII. Our Agentforce Governance Playbook provides a structured 4-pillar blueprint that enforces data sovereignty, APRA CPS 234 compliance, and sub-second reasoning verification.",
      "By integrating Salesforce Data Cloud Zero-Copy with verified trust layers, Australian organizations can safely empower autonomous agents to handle complex customer support, billing reconciliations, and field dispatch workflows.",
      "Source: PRO CRM Enterprise AI Governance & Cloud Architecture Practice."
    ]
  },"""

with open(site_js_path, "r", encoding="utf-8") as f:
    content = f.read()

if "agentforce-multi-agent-governance-playbook-2026" not in content:
    content = content.replace("export const POSTS = [", NEW_POST)
    with open(site_js_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Successfully updated site.js with brand new 25-Aug post!")
else:
    print("ℹ️ Post already present in site.js")

# Now trigger generate_rss.js in procrm-app
os.system(f'cd "{PROCRM_DIR}" && node scripts/generate_rss.js')
os.system(f'cd "{PROCRM_DIR}" && git add . && git commit -m "Publish 25-Aug Agentforce Multi-Agent Governance article & refresh RSS feed" && git push origin main')
print("🚀 Pushed latest PRO CRM post to GitHub & live site!")
