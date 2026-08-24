#!/usr/bin/env python3
"""
Australia Google Trends Crawler & Content Discovery Engine
----------------------------------------------------------
Monitors https://trends.google.com/trending?geo=AU&hl=en-GB&category=3 (Business & Finance)
Filters high-velocity breakout queries in Australia across:
- Mortgages & Interest Rates (RBA, CBA, Westpac, Refinance, Property) -> EZ Mortgage Broker
- Salesforce, AI & Enterprise Cloud (Agentforce, Data Cloud, buy.nsw) -> EZ Consultants
- Cyber Security & ASD Essential Eight (Threats, APRA CPS 234, NDIS)   -> PRO CRM
- Digital Signatures, Compliance & Legal (eSign, ETA 1999, Contracts)   -> EZ Signature
- Financial Inclusion, Literacy & Grants (Seniors, Anti-Scam)          -> Finnova Hub
"""

import os
import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

TRENDS_URLS = [
    {"category": "Business & Finance (AU)", "url": "https://trends.google.com/trending/rss?geo=AU&category=3"},
    {"category": "All Australia Breakout Trends", "url": "https://trends.google.com/trending/rss?geo=AU"},
    {"category": "AU Daily Trending Searches", "url": "https://trends.google.com/trends/trendingsearches/daily/rss?geo=AU"}
]

BRAND_KEYWORDS = {
    "ezmortgagebroker": ["mortgage", "rba", "interest rate", "rate cut", "cash rate", "housing", "property", "refinance", "first home", "super", "banks", "cba", "anz", "nab", "westpac", "inflation"],
    "ezconsultants": ["salesforce", "agentforce", "cloud", "crm", "ai", "enterprise", "saas", "digital transformation", "government tech", "buy.nsw", "data cloud"],
    "procrm": ["cyber", "security", "hack", "scam", "data breach", "malware", "privacy", "essential eight", "apra", "ndis", "healthcare tech"],
    "ezsignature": ["digital signature", "esignature", "docusign", "contracts", "electronic transactions", "pdf sign", "audit trail", "legaltech"],
    "finnova": ["scam alert", "senior tech", "digital literacy", "banking app", "multicultural", "fintech", "community grant"]
}

def fetch_australia_trends():
    trends_found = []
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    for item in TRENDS_URLS:
        try:
            req = urllib.request.Request(item["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                root = ET.fromstring(resp.read())
                for entry in root.findall(".//item"):
                    title = entry.find("title").text if entry.find("title") is not None else ""
                    approx_traffic = entry.find("{https://trends.google.com/trending/rss}approx_traffic")
                    traffic = approx_traffic.text if approx_traffic is not None else "100+"
                    pubDate = entry.find("pubDate").text if entry.find("pubDate") is not None else ""
                    description = entry.find("description").text if entry.find("description") is not None else ""
                    link = entry.find("link").text if entry.find("link") is not None else ""
                    
                    trends_found.append({
                        "category_feed": item["category"],
                        "topic": title,
                        "traffic": traffic,
                        "published": pubDate,
                        "description": description,
                        "link": link
                    })
        except Exception as e:
            print(f"Notice: Trend fetch error for {item['category']}: {e}")
            
    return trends_found

def match_trends_to_brands(trends):
    matched = {brand: [] for brand in BRAND_KEYWORDS}
    for t in trends:
        topic_lower = (t["topic"] + " " + t["description"]).lower()
        for brand, keywords in BRAND_KEYWORDS.items():
            if any(k in topic_lower for k in keywords):
                matched[brand].append(t)
    return matched

if __name__ == "__main__":
    print("🇦🇺 Fetching Live Australia Google Trends...")
    trends = fetch_australia_trends()
    print(f"✅ Retrieved {len(trends)} trending search topics from Google Trends Australia.")
    matched = match_trends_to_brands(trends)
    for b, items in matched.items():
        if items:
            print(f"🎯 Matched {len(items)} trending topics for [{b}]:")
            for it in items[:3]:
                print(f"   - {it['topic']} ({it['traffic']})")
