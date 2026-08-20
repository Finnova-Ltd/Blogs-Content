#!/usr/bin/env python3
import os

REPO_DIR = "/Users/robinbakshi/Documents/GitHub/rss"
universal_py_path = os.path.join(REPO_DIR, "universal_rss.py")

with open(universal_py_path, "r", encoding="utf-8") as f:
    code = f.read()

# Fix regex escape
bad_line = 'matches = re.findall(r\'<a\\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>\', raw_html, re.IGNORECASE | re.DOTALL)'
good_line = 'matches = re.findall(r\'<a\\s+[^>]*href=[\"\\\']([^\"\\\']+)[\"\\\'][^>]*>(.*?)</a>\', raw_html, re.IGNORECASE | re.DOTALL)'

code = code.replace(bad_line, good_line)
# Also fix link_m regex in from_google_alerts
bad_link_m = 'link_m = re.search(r\'<link[^>]*href=[\'"]([^\'"]+)[\'"]\', entry)'
good_link_m = 'link_m = re.search(r\'<link[^>]*href=[\"\\\']([^\"\\\']+)[\"\\\']\', entry)'
code = code.replace(bad_link_m, good_link_m)

with open(universal_py_path, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Fixed universal_rss.py regex patterns")
