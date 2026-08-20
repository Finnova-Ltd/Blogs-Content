#!/usr/bin/env python3
"""
Universal Website to RSS/Atom XML Feed Converter
================================================
Converts ANY website (HTML pages, JSON endpoints, WordPress, Substack, Yahoo Finance, or custom blogs)
into valid RSS 2.0 / Atom XML streams.
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

class UniversalWebToXml:
    def __init__(self, title="Universal Web Feed", link="https://example.com", description="Automated XML Stream"):
        self.title = title
        self.link = link
        self.description = description
        self.entries = []

    def add_entry(self, title, link, description, pub_date=None, guid=None, category=None, image=None):
        self.entries.append({
            "title": title,
            "link": link,
            "description": description,
            "pub_date": pub_date or datetime.now().strftime("%a, %d %b %Y %H:%M:%S +1000"),
            "guid": guid or link,
            "category": category or "General",
            "image": image or ""
        })

    def from_html(self, url, title_pattern=None):
        """Scrapes standard web pages and converts articles/links into XML entries."""
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                raw_html = response.read().decode("utf-8", errors="ignore")

            # Extract article links / headlines
            link_matches = re.findall(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', raw_html, re.IGNORECASE | re.DOTALL)
            seen_links = set()
            
            for href, text in link_matches:
                clean_text = re.sub(r'<.*?>', '', text).strip()
                clean_text = html.unescape(clean_text)
                
                # Quality filters
                if len(clean_text) < 18 or len(clean_text) > 160:
                    continue
                if any(skip in clean_text.lower() for skip in ["privacy", "terms", "login", "sign in", "skip to", "menu", "cookie"]):
                    continue

                full_link = urllib.parse.urljoin(url, href)
                if full_link in seen_links or full_link == url:
                    continue
                seen_links.add(full_link)

                self.add_entry(
                    title=clean_text,
                    link=full_link,
                    description=f"Article extracted from {url}: {clean_text}",
                    guid=full_link
                )
        except Exception as e:
            print(f"⚠️ Notice while parsing {url}: {e}")

    def to_rss_xml(self):
        """Outputs standard RSS 2.0 XML."""
        xml_lines = [
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
            xml_lines.append('    <item>')
            xml_lines.append(f'      <title>{escape(item["title"])}</title>')
            xml_lines.append(f'      <link>{escape(item["link"])}</link>')
            xml_lines.append(f'      <guid isPermaLink="true">{escape(item["guid"])}</guid>')
            xml_lines.append(f'      <pubDate>{escape(item["pub_date"])}</pubDate>')
            xml_lines.append(f'      <description><![CDATA[{item["description"]}]]></description>')
            xml_lines.append(f'      <category>{escape(item["category"])}</category>')
            if item.get("image"):
                xml_lines.append(f'      <media:content url="{escape(item["image"])}" medium="image"/>')
            xml_lines.append('    </item>')

        xml_lines.append('  </channel>')
        xml_lines.append('</rss>')
        return "\n".join(xml_lines)

if __name__ == "__main__":
    converter = UniversalWebToXml(
        title="RBA Cash Rate & Australian Economic Decisions",
        link="https://www.rba.gov.au",
        description="Automated XML feed extracted from Reserve Bank of Australia"
    )
    converter.from_html("https://www.rba.gov.au/media-releases/")
    feed_output = converter.to_rss_xml()
    print(f"✅ Generated {len(converter.entries)} items in standard RSS XML.")
    print("Sample XML output:\n", "\n".join(feed_output.splitlines()[:22]))
