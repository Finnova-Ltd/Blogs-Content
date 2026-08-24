#!/usr/bin/env python3
"""
Write daily_community_publisher.yml in Finnova and execute update
"""

import os
from update_finnova_25_aug import update_finnova

update_finnova()

workflow_dir = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova/.github/workflows"
os.makedirs(workflow_dir, exist_ok=True)
workflow_file = os.path.join(workflow_dir, "daily_community_publisher.yml")

content = """name: Daily Community News & Article Publisher

on:
  schedule:
    - cron: '0 20 * * *' # 6:00 AM AEST (UTC+10)
    - cron: '0 2 * * *'  # 12:00 PM AEST
    - cron: '0 8 * * *'  # 6:00 PM AEST
    - cron: '0 14 * * *' # 12:00 AM AEST
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Finnova Repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Python Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4 feedparser lxml feedgen

      - name: Sync Latest Community Articles
        run: |
          python3 -c "
          import urllib.request, json
          try:
              url = 'https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/posts.json'
              req = urllib.request.urlopen(url)
              data = json.loads(req.read().decode('utf-8'))
              with open('posts.json', 'w', encoding='utf-8') as f:
                  json.dump(data, f, indent=2)
              print('✅ Successfully synchronized posts.json from Blogs-Content Hub!')
          except Exception as e:
              print('Sync warning:', e)
          "

      - name: Commit and Push Updates
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add posts.json
          git diff --quiet && git diff --staged --quiet || (git commit -m "Auto-Publish: Daily Community & Inclusion updates [skip ci]" && git push)
"""

with open(workflow_file, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Successfully wrote daily_community_publisher.yml to Finnova!")
