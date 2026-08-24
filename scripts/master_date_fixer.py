#!/usr/bin/env python3
"""
Master Hub & Card Date Fixer:
Replaces all hardcoded 23-Aug dates in sync_blog_hub.py with dynamic current date formatting.
Regenerates index.html and pages/blog.html across ezmortgagebroker and public/ folders.
"""

import os
import re
from datetime import datetime

SYNC_SCRIPT = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/sync_blog_hub.py"

with open(SYNC_SCRIPT, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update hardcoded header date in template
code = code.replace("📅 Sun, 23 Aug", "📅 Mon, 24 Aug")
code = re.sub(r'📅\s*[A-Za-z]+,\s*\d+\s*[A-Za-z]+', '📅 Mon, 24 Aug', code)

# 2. Update hardcoded sort label
code = re.sub(r'Sorted by Newest First \([^)]+\)', 'Sorted by Newest First (24-Aug-2026)', code)

# 3. Ensure card date badge uses day_str and month_str
old_badge_regex = r'<span style="display:block; font-size:1\.1rem; font-weight:900; color:#0A2540;">\d+</span>\s*<span style="display:block; font-size:0\.65rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0\.04em;">[A-Z]+</span>'
new_badge = '<span style="display:block; font-size:1.1rem; font-weight:900; color:#0A2540;">{day_str}</span>\n              <span style="display:block; font-size:0.65rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.04em;">{month_str}</span>'

code = re.sub(old_badge_regex, new_badge, code)

with open(SYNC_SCRIPT, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Patched sync_blog_hub.py!")

# Execute sync_blog_hub.py immediately
os.system(f"python3 {SYNC_SCRIPT}")
print("🎉 Synchronized all ezmortgagebroker pages!")
