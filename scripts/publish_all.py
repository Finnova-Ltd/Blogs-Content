#!/usr/bin/env python3
"""
Master Multi-Site Publisher & Automation Orchestrator
Single CLI command to ingest, validate, pre-render, vectorize, build, and publish across all Finnova enterprise websites.

Usage:
  python3 scripts/publish_all.py [--site all|ezmortgage|ezconsultants|procrm|suburbs]
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

ROOT_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

def run_step(step_name, cmd, cwd=ROOT_DIR):
    print(f"\n========================================================")
    print(f"▶️ [{step_name}] Running: {cmd}")
    print(f"========================================================")
    res = subprocess.run(cmd, shell=True, cwd=cwd, text=True)
    if res.returncode != 0:
        print(f"❌ Step [{step_name}] failed with code {res.returncode}")
        # Trigger failure alert
        subprocess.run(f"python3 scripts/notify_failure.py '{step_name} failed'", shell=True, cwd=ROOT_DIR)
        return False
    print(f"✅ [{step_name}] Completed Successfully!")
    return True

def publish_ezmortgage():
    # 1. Ingest Yahoo Topics & Australian Lending News
    run_step("EZMortgage: Ingest News", "python3 scripts/ingest_yahoo_topics.py")
    # 2. Sync Blog Hub & Home Cards with Overlay Standards
    run_step("EZMortgage: Sync Blog Hub", "python3 scripts/sync_blog_hub.py")
    # 3. Generate 91 Suburb Location Pages with Full Header & 4cm Logo
    run_step("EZMortgage: Generate 91 Suburbs", "python3 scripts/generate_suburbs_and_pillars.py")
    # 4. Build Vite Bundle
    ez_dir = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
    run_step("EZMortgage: Vite Build", "npm run build", cwd=ez_dir)
    # 5. Git Commit & Push
    run_step("EZMortgage: Git Push", "git add -A && (git diff --quiet && git diff --staged --quiet || git commit -m 'Auto-Publish: Daily mortgage news & 91 suburb updates [skip ci]') && (git pull --rebase origin main 2>/dev/null || true) && (git push origin main || true)", cwd=ez_dir)

def publish_ezconsultants():
    ezc_dir = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au"
    # 1. Ingest Salesforce & Enterprise News
    run_step("EZConsultants: Ingest News", "python3 scripts/ingest_salesforce_news.py", cwd=ezc_dir)
    # 2. Replace dark images with light corporate photos
    run_step("EZConsultants: Light Image Validator", "python3 scripts/replace_dark_images.py")
    # 3. Build Vite Bundle
    run_step("EZConsultants: Vite Build", "npm run build", cwd=ezc_dir)
    # 4. Git Commit & Push
    run_step("EZConsultants: Git Push", "git add -A && (git diff --quiet && git diff --staged --quiet || git commit -m 'Auto-Publish: Daily Salesforce & Cloud articles [skip ci]') && (git pull --rebase origin main 2>/dev/null || true) && (git push origin main || true)", cwd=ezc_dir)

def sync_ai_agents():
    # 1. Auto-RAG Vectorize Articles into Cloudflare Vectorize
    run_step("AI Agents: Auto-RAG Vectorize", "python3 scripts/embed_articles_to_vectorize.py")
    # 2. Sync Chat Agent to Standalone Repository
    run_step("AI Agents: Standalone Repo Sync", "python3 scripts/sync_cloudflare_agents.py")

def main():
    parser = argparse.ArgumentParser(description="Master Multi-Site Publisher CLI")
    parser.add_argument("--site", default="all", choices=["all", "ezmortgage", "ezconsultants", "suburbs", "ai"], help="Target website or subsystem")
    args = parser.parse_args()

    start_time = datetime.now()
    print(f"🚀 [FINNOVA AUTOMATION HUB] Starting Master Multi-Site Publish for: {args.site.upper()}")

    if args.site in ["all", "ezmortgage"]:
        publish_ezmortgage()

    if args.site in ["all", "ezconsultants"]:
        publish_ezconsultants()

    if args.site in ["all", "ai"]:
        sync_ai_agents()

    if args.site == "suburbs":
        run_step("EZMortgage: Generate 91 Suburbs", "python3 scripts/generate_suburbs_and_pillars.py")
        run_step("EZMortgage: Vite Build", "npm run build", cwd="/Users/robinbakshi/Documents/GitHub/ezmortgagebroker")

    # Final sync on Blogs-Content monorepo
    run_step("Blogs-Content: Git Push", "git add -A && (git diff --quiet && git diff --staged --quiet || git commit -m 'Auto-Publish: Multi-site sync & vector cache update [skip ci]') && (git pull --rebase origin main 2>/dev/null || true) && (git push origin main || true)")

    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n🎉 [FINNOVA AUTOMATION HUB] Master Multi-Site Publish Completed in {elapsed:.1f}s!")

if __name__ == "__main__":
    main()
