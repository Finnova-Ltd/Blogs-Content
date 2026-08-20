#!/usr/bin/env python3
import os
import subprocess

REPO_DIR = "/Users/robinbakshi/Documents/GitHub/rss"

setup_py = '''from setuptools import setup, find_packages

setup(
    name="finnova-rss",
    version="1.0.0",
    description="Universal Website, Yahoo Finance & API to RSS/XML Converter and Multi-Source Content Engine",
    author="Finnova Ltd",
    packages=find_packages(),
    py_modules=["universal_rss", "content_engine", "cli"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "finnova-rss=cli:main",
            "finnova-content=content_engine:main"
        ]
    },
    python_requires=">=3.8",
)
'''

with open(os.path.join(REPO_DIR, "setup.py"), "w", encoding="utf-8") as f:
    f.write(setup_py)

# Update projects_config.example.json in rss repo with the 3 Yahoo Finance topic URLs
config_json = '''{
  "projects": [
    {
      "name": "EZ Mortgage Broker",
      "brand_name": "EZ Mortgage Broker",
      "brand_url": "https://ezmortgagebroker.com.au",
      "author": "R BAKSHI",
      "brand_voice": "Accredited Australian Mortgage Broker & Home Loan Specialist",
      "target_daily_articles_per_category": 4,
      "categories": [
        {
          "name": "Money & Banking",
          "url": "https://au.finance.yahoo.com/topic/money/",
          "target_count": 4,
          "keywords": ["mortgage", "rate", "interest", "bank", "buyer", "money", "loan", "lender", "cash", "super"]
        },
        {
          "name": "Property & Housing",
          "url": "https://au.finance.yahoo.com/topic/property/",
          "target_count": 4,
          "keywords": ["property", "housing", "mortgage", "home", "buyer", "landlord", "rent", "investor", "build", "estate"]
        },
        {
          "name": "Personal Finance & Centrelink",
          "url": "https://au.finance.yahoo.com/topic/personal-finance/",
          "target_count": 4,
          "keywords": ["centrelink", "tax", "finance", "superannuation", "saving", "cgt", "budget", "retirement", "debt", "wealth"]
        }
      ],
      "sources": [
        { "type": "url", "value": "https://au.finance.yahoo.com/topic/money/", "category": "Money & Banking" },
        { "type": "url", "value": "https://au.finance.yahoo.com/topic/property/", "category": "Property & Housing" },
        { "type": "url", "value": "https://au.finance.yahoo.com/topic/personal-finance/", "category": "Personal Finance & Centrelink" },
        { "type": "yahoo_finance", "value": "CBA.AX", "category": "Banking & Rates" },
        { "type": "yahoo_finance", "value": "WBC.AX", "category": "Banking & Rates" },
        { "type": "rss", "value": "https://www.google.com/alerts/feeds/14625353401416373956/18413967573759855438", "category": "Home Loans" }
      ],
      "max_publish_per_run": 12,
      "posts_json_path": "posts.json",
      "html_dir": "pages/blog",
      "make_webhook_url": ""
    }
  ]
}
'''

with open(os.path.join(REPO_DIR, "projects_config.example.json"), "w", encoding="utf-8") as f:
    f.write(config_json)

# Git commit and push to Finnova-Ltd/rss
subprocess.run(["git", "add", "."], cwd=REPO_DIR)
subprocess.run(["git", "commit", "-m", "feat(pkg): add setup.py for pip install reusability and configure Yahoo Finance Money, Property & Personal Finance topic presets (4 articles/category quota)"], cwd=REPO_DIR)
subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR)

print("✅ Updated and pushed Finnova-Ltd/rss with reusable packaging & Yahoo Finance topic presets!")
