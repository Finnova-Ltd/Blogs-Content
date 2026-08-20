#!/usr/bin/env python3
import urllib.request
import re
import html

urls = [
    "https://au.finance.yahoo.com/topic/money/",
    "https://au.finance.yahoo.com/topic/property/",
    "https://au.finance.yahoo.com/topic/personal-finance/"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            # Find links containing news or articles
            matches = re.findall(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL)
            print(f"\n--- URL: {u} ---")
            found = 0
            for href, text in matches:
                clean_text = re.sub(r'<.*?>', '', text).strip()
                clean_text = html.unescape(clean_text)
                if len(clean_text) > 25 and not any(skip in clean_text.lower() for skip in ["privacy", "terms", "sign in", "yahoo", "cookie"]):
                    print(f"  • [{href[:45]}...] {clean_text[:80]}")
                    found += 1
                    if found >= 5:
                        break
    except Exception as e:
        print(f"⚠️ Error {u}: {e}")
