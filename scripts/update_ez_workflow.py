#!/usr/bin/env python3
import os
import subprocess

EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
RSS_DIR = "/Users/robinbakshi/Documents/GitHub/rss"

# Update workflow in ezmortgagebroker
ez_workflow_path = os.path.join(EZ_DIR, ".github", "workflows", "yahoo_finance_publisher.yml")
workflow_code = '''name: Yahoo Finance Australia & Mortgage Daily Publisher

on:
  schedule:
    - cron: '*/30 * * * *' # Runs every 30 minutes
  workflow_dispatch:

permissions:
  contents: write

jobs:
  publish-and-syndicate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Set up Node.js for Vite build
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'

      - name: Install dependencies
        run: |
          npm ci || npm install
          pip install --upgrade feedgen requests

      - name: Run Multi-Topic Ingestion (Money, Property, Personal Finance & Tickers)
        run: |
          python3 scripts/ingest_yahoo_topics.py
          python3 scripts/fetch_yahoo_finance_news.py
          python3 scripts/generate_rss_feed.py
          npm run build

      - name: Commit and Push Updates
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add posts.json public/posts.json feed.xml rss.xml public/feed.xml public/rss.xml pages/blog/ public/pages/blog/ dist/
          git diff --quiet && git diff --staged --quiet || (git commit -m "Auto-Publish: Daily Yahoo Finance Money, Property & Personal Finance articles [skip ci]" && git push origin main)
'''

with open(ez_workflow_path, "w", encoding="utf-8") as f:
    f.write(workflow_code)

# Copy the ingestion script into ezmortgagebroker/scripts/ingest_yahoo_topics.py
with open("/Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/ingest_yahoo_topics_ez.py", "r", encoding="utf-8") as f:
    ingest_script_content = f.read()

with open(os.path.join(EZ_DIR, "scripts", "ingest_yahoo_topics.py"), "w", encoding="utf-8") as f:
    f.write(ingest_script_content)

print("✅ Updated ezmortgagebroker workflow and scripts with 30-min automated multi-topic publisher!")
