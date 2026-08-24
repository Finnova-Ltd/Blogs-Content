#!/usr/bin/env python3
"""
Fix dynamic date badge parsing in sync_blog_hub.py and refresh ezmortgagebroker & procrm
"""

import os
import re

SYNC_SCRIPT = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/sync_blog_hub.py"

with open(SYNC_SCRIPT, "r", encoding="utf-8") as f:
    code = f.read()

# Replace hardcoded 23 AUG with dynamic p_date day and month
old_date_badge = """            <!-- 1. Top-Left: Date Badge (23 AUG) -->
            <div style="position:absolute; top:10px; left:10px; background:#ffffff; border-radius:8px; padding:4px 10px; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.22); line-height:1.1; pointer-events:none; z-index:3;">
              <span style="display:block; font-size:1.1rem; font-weight:900; color:#0A2540;">23</span>
              <span style="display:block; font-size:0.65rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.04em;">AUG</span>
            </div>"""

new_date_badge = """            <!-- 1. Top-Left: Dynamic Date Badge -->
            <div style="position:absolute; top:10px; left:10px; background:#ffffff; border-radius:8px; padding:4px 10px; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.22); line-height:1.1; pointer-events:none; z-index:3;">
              <span style="display:block; font-size:1.1rem; font-weight:900; color:#0A2540;">{day_str}</span>
              <span style="display:block; font-size:0.65rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.04em;">{month_str}</span>
            </div>"""

if old_date_badge in code:
    # also define day_str and month_str in generate_card_markup
    code = code.replace(old_date_badge, new_date_badge)
    code = code.replace(
        'def generate_card_markup(p, idx, is_blog_hub=True):',
        'def generate_card_markup(p, idx, is_blog_hub=True):\n    p_date = parse_date(p)\n    day_str = p_date.strftime("%d")\n    month_str = p_date.strftime("%b").upper()'
    )
    with open(SYNC_SCRIPT, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Successfully patched sync_blog_hub.py with dynamic date badges!")
else:
    print("ℹ️ Badge snippet not found directly, checking regex replacement...")
    code = re.sub(
        r'<span style="[^"]*color:#0A2540;">\d+</span>\s*<span style="[^"]*color:#64748B;[^"]*">[A-Z]+</span>',
        '<span style="display:block; font-size:1.1rem; font-weight:900; color:#0A2540;">{day_str}</span>\n              <span style="display:block; font-size:0.65rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.04em;">{month_str}</span>',
        code
    )
    if "day_str" not in code:
        code = code.replace(
            'def generate_card_markup(p, idx, is_blog_hub=True):',
            'def generate_card_markup(p, idx, is_blog_hub=True):\n    p_date = parse_date(p)\n    day_str = p_date.strftime("%d")\n    month_str = p_date.strftime("%b").upper()'
        )
    with open(SYNC_SCRIPT, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Successfully patched sync_blog_hub.py via regex!")
