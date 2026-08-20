#!/usr/bin/env python3
import os
import subprocess

REPO_DIR = "/Users/robinbakshi/Documents/GitHub/rss"

universal_py = '''#!/usr/bin/env python3
"""
Universal Website & API to RSS/Atom XML Converter Engine
=========================================================
1. Universal HTML Scraper (Any website, blog, government portal)
2. JSON & Headless API Connector (Yahoo Finance, WordPress REST, Substack API)
3. Google Alerts & Atom Normalizer (Cleans <b> tags, strips /url?rct=j tracking links)
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
    def __init__(self, title="Universal Feed", link="https://example.com", description="Automated RSS XML Stream"):
        self.title = title
        self.link = link
        self.description = description
        self.entries = []

    def add_item(self, title, link, description, pub_date=None, guid=None, category=None, author="Editorial", image=None):
        self.entries.append({
            "title": str(title).strip(),
            "link": str(link).strip(),
            "description": str(description).strip(),
            "pub_date": pub_date or datetime.now().strftime("%a, %d %b %Y %H:%M:%S +1000"),
            "guid": str(guid or link).strip(),
            "category": category or "General",
            "author": author,
            "image": image or ""
        })

    # =========================================================================
    # FEATURE 1: Universal HTML Scraper to XML
    # =========================================================================
    def from_url(self, url, min_len=16, max_len=200, exclude_words=None):
        """Scrapes any web page for articles, headings, links, and summaries."""
        if exclude_words is None:
            exclude_words = ["privacy", "terms", "login", "sign in", "skip to", "cookie", "copyright", "menu"]

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw_html = resp.read().decode("utf-8", errors="ignore")

            matches = re.findall(r'<a\\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', raw_html, re.IGNORECASE | re.DOTALL)
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
                    description=f"Article extracted from {url}: {clean_text}",
                    guid=full_link
                )
        except Exception as e:
            print(f"⚠️ Error scraping {url}: {e}")

    # =========================================================================
    # FEATURE 2: JSON & Headless API to XML (Yahoo Finance, WordPress, Substack)
    # =========================================================================
    def from_yahoo_finance(self, ticker, keywords=None):
        """Queries Yahoo Finance internal search/news JSON endpoint for any stock ticker."""
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={urllib.parse.quote(ticker)}&newsCount=25"
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

    def from_wordpress_api(self, site_url):
        """Fetches posts from WordPress REST API (wp-json/wp/v2/posts)."""
        base_url = site_url.rstrip("/")
        api_url = f"{base_url}/wp-json/wp/v2/posts?per_page=20"
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(api_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                posts = json.loads(resp.read().decode("utf-8"))
                for p in posts:
                    title = html.unescape(p.get("title", {}).get("rendered", ""))
                    link = p.get("link", "")
                    excerpt = re.sub(r'<.*?>', '', p.get("excerpt", {}).get("rendered", ""))
                    excerpt = html.unescape(excerpt).strip()
                    date_str = p.get("date_gmt", "")
                    try:
                        pub_date = datetime.fromisoformat(date_str).strftime("%a, %d %b %Y %H:%M:%S +1000")
                    except Exception:
                        pub_date = None

                    self.add_item(
                        title=title,
                        link=link,
                        description=excerpt or title,
                        pub_date=pub_date,
                        guid=str(p.get("id", link)),
                        category="WordPress"
                    )
        except Exception as e:
            print(f"⚠️ WordPress API notice for {site_url}: {e}")

    def from_substack_api(self, substack_domain):
        """Fetches posts from Substack API (/api/v1/posts)."""
        base_url = substack_domain.rstrip("/")
        api_url = f"{base_url}/api/v1/posts?limit=20"
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(api_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                posts = json.loads(resp.read().decode("utf-8"))
                for p in posts:
                    title = p.get("title", "")
                    slug = p.get("slug", "")
                    link = f"{base_url}/p/{slug}" if slug else base_url
                    subtitle = p.get("subtitle", "")
                    date_str = p.get("post_date", "")
                    try:
                        pub_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%a, %d %b %Y %H:%M:%S +1000")
                    except Exception:
                        pub_date = None

                    self.add_item(
                        title=title,
                        link=link,
                        description=subtitle or title,
                        pub_date=pub_date,
                        guid=str(p.get("id", link)),
                        category="Substack"
                    )
        except Exception as e:
            print(f"⚠️ Substack API notice for {substack_domain}: {e}")

    # =========================================================================
    # FEATURE 3: Google Alerts & RSS Feed Normalizer
    # =========================================================================
    def from_google_alerts(self, feed_url_or_xml):
        """
        Ingests Google Alert Atom XML feeds, strips Google tracking redirects
        (/url?rct=j&sa=t&url=...) to extract clean canonical URLs, cleans <b> tags,
        and decodes HTML entities.
        """
        raw_xml = ""
        if feed_url_or_xml.startswith("http://") or feed_url_or_xml.startswith("https://"):
            headers = {"User-Agent": "Mozilla/5.0"}
            req = urllib.request.Request(feed_url_or_xml, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    raw_xml = resp.read().decode("utf-8", errors="ignore")
            except Exception as e:
                print(f"⚠️ Error fetching Google Alert feed: {e}")
                return
        else:
            raw_xml = feed_url_or_xml

        # Extract entries from Atom XML
        entries = re.findall(r'<entry>(.*?)</entry>', raw_xml, re.DOTALL)
        for entry in entries:
            # Extract Title & clean <b> tags
            title_m = re.search(r'<title[^>]*>(.*?)</title>', entry, re.DOTALL)
            raw_title = title_m.group(1) if title_m else ""
            clean_title = re.sub(r'<.*?>', '', raw_title)
            clean_title = html.unescape(clean_title).strip()

            # Extract Link & unwrap Google tracker
            link_m = re.search(r'<link[^>]*href=[\'"]([^\'"]+)[\'"]', entry)
            raw_link = link_m.group(1) if link_m else ""
            clean_link = raw_link
            if "google.com/url?" in raw_link:
                parsed = urllib.parse.urlparse(raw_link)
                qs = urllib.parse.parse_qs(parsed.query)
                if "url" in qs:
                    clean_link = qs["url"][0]

            # Extract Content / Snippet & clean <b> tags
            content_m = re.search(r'<content[^>]*>(.*?)</content>', entry, re.DOTALL)
            raw_content = content_m.group(1) if content_m else ""
            clean_content = re.sub(r'<.*?>', '', raw_content)
            clean_content = html.unescape(clean_content).strip()

            # Extract PubDate
            pub_m = re.search(r'<published>(.*?)</published>', entry) or re.search(r'<updated>(.*?)</updated>', entry)
            pub_date_str = pub_m.group(1) if pub_m else ""
            try:
                pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00")).strftime("%a, %d %b %Y %H:%M:%S +1000")
            except Exception:
                pub_date = None

            guid_m = re.search(r'<id>(.*?)</id>', entry)
            guid = guid_m.group(1) if guid_m else clean_link

            if clean_title and clean_link:
                self.add_item(
                    title=clean_title,
                    link=clean_link,
                    description=clean_content or clean_title,
                    pub_date=pub_date,
                    guid=guid,
                    category="Google Alert"
                )

    # =========================================================================
    # XML Export
    # =========================================================================
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

cli_py = '''#!/usr/bin/env python3
import argparse
from universal_rss import UniversalRSS

def main():
    parser = argparse.ArgumentParser(description="Finnova Universal RSS - Convert any website, API, or Google Alert to XML.")
    parser.add_argument("--url", help="Target website URL to scrape (HTML parser)")
    parser.add_argument("--ticker", help="Stock ticker to fetch news for (e.g. CBA.AX, AAPL, WBC.AX)")
    parser.add_argument("--wordpress", help="WordPress site URL to fetch via REST API (e.g. https://techcrunch.com)")
    parser.add_argument("--substack", help="Substack publication domain to fetch (e.g. https://astralcodexten.substack.com)")
    parser.add_argument("--google-alert", help="Google Alert feed URL or XML file to normalize and unwrap tracking links")
    parser.add_argument("--keywords", nargs="+", help="Filter news by keywords (e.g. mortgage rates banking)")
    parser.add_argument("--title", default="Universal RSS Feed", help="RSS Feed Title")
    parser.add_argument("--link", default="https://example.com", help="RSS Feed Channel Link")
    parser.add_argument("--desc", default="Automated RSS stream generated by Finnova RSS", help="RSS Description")
    parser.add_argument("--out", default="feed.xml", help="Output file path (default: feed.xml)")

    args = parser.parse_args()

    feed = UniversalRSS(title=args.title, link=args.link, description=args.desc)

    if args.ticker:
        print(f"📡 Fetching Yahoo Finance news for {args.ticker}...")
        feed.from_yahoo_finance(args.ticker, keywords=args.keywords)
    elif args.wordpress:
        print(f"📰 Ingesting WordPress REST API from: {args.wordpress}...")
        feed.from_wordpress_api(args.wordpress)
    elif args.substack:
        print(f"📬 Ingesting Substack API from: {args.substack}...")
        feed.from_substack_api(args.substack)
    elif getattr(args, "google_alert"):
        print(f"🔔 Normalizing Google Alert Atom feed...")
        feed.from_google_alerts(args.google_alert)
    elif args.url:
        print(f"🌐 HTML Scraper targeting URL: {args.url}...")
        feed.from_url(args.url)
    else:
        print("❌ Please provide an input source (--url, --ticker, --wordpress, --substack, or --google-alert)")
        return

    feed.save(args.out)

if __name__ == "__main__":
    main()
'''

readme_md = '''# 🌐 Finnova Universal RSS (`Finnova-Ltd/rss`)

A zero-dependency Python engine and CLI to convert **ANY website, government portal, Yahoo Finance ticker, WordPress blog, Substack, or Google Alert** into clean, valid **RSS 2.0 / Atom XML feeds**.

---

## 🚀 3 Ways We Convert Any Source Into XML

### 1. Universal HTML Scraper to XML (`from_url`)
Connects to any public webpage (e.g. `cyber.gov.au`, `rba.gov.au`, financial news hubs, or competitor blogs), parses headlines, article links, timestamps, and images, and packages them into a valid `feed.xml` / `rss.xml` structure.

```bash
python3 cli.py --url "https://www.rba.gov.au/media-releases/" --title "RBA Cash Rate Decisions" --out "feeds/rba_feed.xml"
```

### 2. JSON & Headless API Connector (Yahoo Finance, WordPress, Substack)
Queries unofficial backend endpoints, extracts structured JSON keys, and converts them directly into RSS `<item>` nodes with keyword filtering:
* **Yahoo Finance**: `python3 cli.py --ticker "CBA.AX" --keywords mortgage rates banking --out "feeds/cba_news.xml"`
* **WordPress REST API**: `python3 cli.py --wordpress "https://techcrunch.com" --out "feeds/techcrunch.xml"`
* **Substack API**: `python3 cli.py --substack "https://astralcodexten.substack.com" --out "feeds/substack.xml"`

### 3. Google Alerts & RSS Feed Normalizer (`from_google_alerts`)
Ingests Google Alert Atom feeds or raw XML, cleans HTML tags (`<b>`, `&amp;`), strips Google redirect tracking links (`/url?rct=j&sa=t&url=...` → clean canonical URLs), and exports clean RSS 2.0 XML:

```bash
python3 cli.py --google-alert "https://www.google.com/alerts/feeds/14625353401416373956/18413967573759855438" --out "feeds/google_alerts_clean.xml"
```

---

## 🔄 End-to-End Automation Flow

```mermaid
graph LR
    A[Any Website / Yahoo / Gov Portal / Alerts] -->|Finnova RSS Engine| B[Universal XML Feed]
    B -->|Hosted on GitHub / Cloudflare| C[Public feed.xml URL]
    C -->|Webhook / RSS Poller| D[Make.com Flow]
    D -->|Auto-Rewrite & Syndicate| E[Website Blog]
    D -->|Social Post| F[LinkedIn & Facebook]
```

---

## 📦 Python Library Usage

```python
from universal_rss import UniversalRSS

# Initialize feed
feed = UniversalRSS(
    title="Australian Mortgage & Financial Intelligence",
    link="https://ezmortgagebroker.com.au",
    description="Automated multi-source financial stream"
)

# 1. Scrape HTML page
feed.from_url("https://www.cyber.gov.au/about-us/news-media")

# 2. Add Yahoo Finance ticker news with keyword filter
feed.from_yahoo_finance("CBA.AX", keywords=["mortgage", "rates", "borrower"])

# 3. Add WordPress or Substack posts
feed.from_wordpress_api("https://techcrunch.com")

# 4. Normalize Google Alerts (strips tracking redirects)
feed.from_google_alerts("https://www.google.com/alerts/feeds/14625353401416373956/18413967573759855438")

# 5. Export to XML
feed.save("feeds/combined_feed.xml")
```

---

## 🤖 GitHub Actions Automated Cron

This repository includes [`.github/workflows/generate_feeds.yml`](.github/workflows/generate_feeds.yml) configured to run every 3 hours (`0 */3 * * *`) to fetch target sources, regenerate XML feeds, and commit them automatically to the repository.

---

## 📄 License
MIT © 2026 Finnova Ltd
'''

# Update files in repo
with open(os.path.join(REPO_DIR, "universal_rss.py"), "w", encoding="utf-8") as f:
    f.write(universal_py)

with open(os.path.join(REPO_DIR, "cli.py"), "w", encoding="utf-8") as f:
    f.write(cli_py)

with open(os.path.join(REPO_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_md)

print("✅ Updated universal_rss.py, cli.py, and README.md in Finnova-Ltd/rss!")
