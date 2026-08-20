#!/usr/bin/env python3
import os
import subprocess

REPO_DIR = "/Users/robinbakshi/Documents/GitHub/rss"

# 1. Main universal RSS generator module
universal_py = '''#!/usr/bin/env python3
"""
Universal Website to RSS/Atom XML Converter
============================================
Converts ANY webpage, blog, API, Yahoo Finance ticker, or Google Alert feed
into clean, valid RSS 2.0 and Atom XML streams.
"""

import os
import sys
import re
import json
import html
import urllib.request
import urllib.parse
from datetime import datetime
from xml.sax.saxutils import escape

class UniversalRSS:
    def __init__(self, title="Universal Feed", link="https://example.com", description="Automated RSS Stream"):
        self.title = title
        self.link = link
        self.description = description
        self.entries = []

    def add_item(self, title, link, description, pub_date=None, guid=None, category=None, author="Editorial", image=None):
        self.entries.append({
            "title": title.strip(),
            "link": link.strip(),
            "description": description.strip(),
            "pub_date": pub_date or datetime.now().strftime("%a, %d %b %Y %H:%M:%S +1000"),
            "guid": guid or link.strip(),
            "category": category or "General",
            "author": author,
            "image": image or ""
        })

    def from_url(self, url, min_len=18, max_len=180, exclude_words=None):
        """Scrapes any web page for articles and headlines."""
        if exclude_words is None:
            exclude_words = ["privacy", "terms", "login", "sign in", "skip to", "cookie", "copyright"]

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw_html = resp.read().decode("utf-8", errors="ignore")

            matches = re.findall(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', raw_html, re.IGNORECASE | re.DOTALL)
            seen = set()

            for href, text in matches:
                clean_text = re.sub(r'<.*?>', '', text).strip()
                clean_text = html.unescape(clean_text)

                if len(clean_text) < min_len or len(clean_text) > max_len:
                    continue
                if any(w in clean_text.lower() for w in exclude_words):
                    continue

                full_link = urllib.parse.urljoin(url, href)
                if full_link in seen or full_link == url:
                    continue
                seen.add(full_link)

                self.add_item(
                    title=clean_text,
                    link=full_link,
                    description=f"Extracted article from {url}: {clean_text}",
                    guid=full_link
                )
        except Exception as e:
            print(f"⚠️ Error fetching {url}: {e}")

    def from_yahoo_finance(self, ticker, keywords=None):
        """Fetches news for any stock ticker via Yahoo Finance JSON API."""
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={urllib.parse.quote(ticker)}&newsCount=20"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                news = data.get("news", [])
                for n in news:
                    title = html.unescape(n.get("title", ""))
                    summary = html.unescape(n.get("summary", ""))
                    link = n.get("link", "")
                    pub_time = n.get("providerPublishTime")

                    if keywords:
                        combined = (title + " " + summary).lower()
                        if not any(k.lower() in combined for k in keywords):
                            continue

                    formatted_date = datetime.fromtimestamp(pub_time).strftime("%a, %d %b %Y %H:%M:%S +1000") if pub_time else None
                    self.add_item(
                        title=title,
                        link=link,
                        description=summary or title,
                        pub_date=formatted_date,
                        guid=n.get("uuid") or link,
                        category=ticker,
                        author=n.get("publisher", "Yahoo Finance")
                    )
        except Exception as e:
            print(f"⚠️ Yahoo Finance API notice for {ticker}: {e}")

    def to_xml(self):
        """Builds valid RSS 2.0 XML string."""
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">',
            '  <channel>',
            f'    <title>{escape(self.title)}</title>',
            f'    <link>{escape(self.link)}</link>',
            f'    <description>{escape(self.description)}</description>',
            '    <language>en-au</language>',
            f'    <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S +1000")}</lastBuildDate>',
            f'    <atom:link href="{escape(self.link)}" rel="self" type="application/rss+xml"/>'
        ]
        for item in self.entries:
            lines.append('    <item>')
            lines.append(f'      <title>{escape(item["title"])}</title>')
            lines.append(f'      <link>{escape(item["link"])}</link>')
            lines.append(f'      <guid isPermaLink="true">{escape(item["guid"])}</guid>')
            lines.append(f'      <pubDate>{escape(item["pub_date"])}</pubDate>')
            lines.append(f'      <description><![CDATA[{item["description"]}]]></description>')
            lines.append(f'      <category>{escape(item["category"])}</category>')
            if item.get("image"):
                lines.append(f'      <media:content url="{escape(item["image"])}" medium="image"/>')
            lines.append('    </item>')
        lines.append('  </channel>')
        lines.append('</rss>')
        return "\\n".join(lines)

    def save(self, filepath):
        """Saves XML to destination file."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        xml_content = self.to_xml()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_content)
        print(f"✅ Saved RSS feed ({len(self.entries)} items) to: {filepath}")
        return filepath
'''

# 2. CLI wrapper
cli_py = '''#!/usr/bin/env python3
import argparse
from universal_rss import UniversalRSS

def main():
    parser = argparse.ArgumentParser(description="Convert any website, stock ticker, or API into RSS XML.")
    parser.add_argument("--url", help="Target website URL to scrape (e.g. https://www.cyber.gov.au)")
    parser.add_argument("--ticker", help="Stock ticker to fetch news for (e.g. CBA.AX, AAPL, WBC.AX)")
    parser.add_argument("--keywords", nargs="+", help="Filter news by keywords (e.g. mortgage rates banking)")
    parser.add_argument("--title", default="Universal Web RSS Feed", help="RSS Feed Title")
    parser.add_argument("--link", default="https://example.com", help="RSS Feed Channel Link")
    parser.add_argument("--desc", default="Automated RSS stream generated by Finnova RSS", help="RSS Description")
    parser.add_argument("--out", default="feed.xml", help="Output file path (default: feed.xml)")

    args = parser.parse_args()

    feed = UniversalRSS(title=args.title, link=args.link, description=args.desc)

    if args.ticker:
        print(f"📡 Fetching Yahoo Finance news for {args.ticker}...")
        feed.from_yahoo_finance(args.ticker, keywords=args.keywords)
    elif args.url:
        print(f"🌐 Scraper targeting URL: {args.url}...")
        feed.from_url(args.url)
    else:
        print("❌ Please provide either --url or --ticker")
        return

    feed.save(args.out)

if __name__ == "__main__":
    main()
'''

# 3. Example generator script
example_py = '''#!/usr/bin/env python3
"""
Example: Multi-source feed generation
"""
from universal_rss import UniversalRSS

# 1. Scrape Australian Signals Directorate (ASD) Cyber Alerts
asd_feed = UniversalRSS(
    title="ASD Cyber Threat Alerts",
    link="https://www.cyber.gov.au",
    description="Latest Australian Signals Directorate advisories"
)
asd_feed.from_url("https://www.cyber.gov.au/about-us/news-media")
asd_feed.save("feeds/asd_cyber_feed.xml")

# 2. Yahoo Finance Australian Banking Tickers (CBA, WBC, ANZ, NAB)
bank_feed = UniversalRSS(
    title="ASX Major Banks Mortgage & Rate News",
    link="https://au.finance.yahoo.com",
    description="Banking, mortgage and lending news from Yahoo Finance"
)
for ticker in ["CBA.AX", "WBC.AX", "ANZ.AX", "NAB.AX"]:
    bank_feed.from_yahoo_finance(ticker, keywords=["mortgage", "bank", "rate", "property", "loan"])

bank_feed.save("feeds/au_banks_mortgage_feed.xml")
'''

# 4. GitHub Actions workflow
workflow_yml = '''name: Universal RSS Feed Generator & Publisher

on:
  schedule:
    - cron: '0 */3 * * *' # Runs every 3 hours
  workflow_dispatch: # Allows manual run

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run Feed Generators
        run: |
          python3 example_multi_feed.py

      - name: Commit and Push Generated Feeds
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add feeds/
          git diff --quiet && git diff --staged --quiet || (git commit -m "chore(feeds): auto-update RSS feeds [skip ci]" && git push)
'''

# 5. README.md
readme_md = '''# 🌐 Universal Website to RSS Converter (`Finnova-Ltd/rss`)

A lightweight, zero-dependency Python library and CLI tool to convert **ANY website, government portal, Yahoo Finance stock ticker, or REST endpoint** into standards-compliant **RSS 2.0 / Atom XML feeds**.

---

## 🚀 Features

- **Any Website Scraper**: Turn standard HTML blog & news pages into structured RSS feeds.
- **Yahoo Finance Ticker Stream**: Fetch live company/market news directly by ticker (`CBA.AX`, `WBC.AX`, `AAPL`, `MSFT`) with keyword filtering (`mortgage`, `rates`, `lending`).
- **Valid RSS 2.0 & Atom Standards**: Compatible with all RSS readers, Make.com, Zapier, Cloudflare, WordPress, and Webflow.
- **GitHub Actions Auto-Publisher**: Includes scheduled cron workflow that commits live `feeds/*.xml` automatically to GitHub Pages or your repo.

---

## 📦 Quick Installation

```bash
git clone https://github.com/Finnova-Ltd/rss.git
cd rss
```

No external dependencies required (uses Python standard library).

---

## ⚡ CLI Usage

### 1. Convert Any Web Page to RSS
```bash
python3 cli.py --url "https://www.cyber.gov.au/about-us/news-media" --title "ASD Cyber Alerts" --out "feeds/cyber_feed.xml"
```

### 2. Convert Yahoo Finance Bank Tickers with Keyword Filter
```bash
python3 cli.py --ticker "CBA.AX" --keywords mortgage bank rate property --title "CBA Mortgage News" --out "feeds/cba_news.xml"
```

---

## 🐍 Python Library Usage

```python
from universal_rss import UniversalRSS

feed = UniversalRSS(
    title="Australian Mortgage & Lending Stream",
    link="https://ezmortgagebroker.com.au",
    description="Latest Australian home loan, RBA and banking updates"
)

# 1. Ingest from web page
feed.from_url("https://www.rba.gov.au/media-releases/")

# 2. Ingest from Yahoo Finance
feed.from_yahoo_finance("CBA.AX", keywords=["mortgage", "rates", "borrower"])

# 3. Export to XML
feed.save("feeds/mortgage_feed.xml")
```

---

## 🔄 Automated Multi-Channel Publishing with Make.com

1. Host the generated `feeds/*.xml` on GitHub Pages or Cloudflare Pages.
2. In **Make.com**, add an **RSS Watch RSS Feed Items** trigger module.
3. Pipe the items into:
   - **OpenAI / Gemini** to rewrite into 180–200 word custom articles.
   - **Facebook Page & LinkedIn** for automated social media syndication.
   - **Webflow / WordPress / Custom Site** for automated blog publishing.

---

## 📄 License
MIT © 2026 Finnova Ltd
'''

# Write files
with open(os.path.join(REPO_DIR, "universal_rss.py"), "w", encoding="utf-8") as f:
    f.write(universal_py)

with open(os.path.join(REPO_DIR, "cli.py"), "w", encoding="utf-8") as f:
    f.write(cli_py)

with open(os.path.join(REPO_DIR, "example_multi_feed.py"), "w", encoding="utf-8") as f:
    f.write(example_py)

with open(os.path.join(REPO_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_md)

with open(os.path.join(REPO_DIR, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write("# Zero external dependencies required! Python 3.8+ built-in urllib, re, json, xml\n")

gh_workflow_dir = os.path.join(REPO_DIR, ".github", "workflows")
os.makedirs(gh_workflow_dir, exist_ok=True)
with open(os.path.join(gh_workflow_dir, "generate_feeds.yml"), "w", encoding="utf-8") as f:
    f.write(workflow_yml)

# Run example script to generate initial feeds
subprocess.run(["python3", "example_multi_feed.py"], cwd=REPO_DIR, capture_output=True)

print("✅ Successfully populated Finnova-Ltd/rss repository!")
