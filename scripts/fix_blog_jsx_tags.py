#!/usr/bin/env python3
"""
Fix closing tag in Blog.jsx
"""

BLOG_JSX = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/pages/Blog.jsx"

with open(BLOG_JSX, "r", encoding="utf-8") as f:
    content = f.read()

target = """            <NeverMissAnAlert />

            {/* Sidebar with Highlights Widget (Column 2 - 4 cols) */}"""

replacement = """            <NeverMissAnAlert />
          </main>

          {/* Sidebar with Highlights Widget (Column 2 - 4 cols) */}"""

if target in content:
    content = content.replace(target, replacement)
    with open(BLOG_JSX, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Fixed closing main tag in Blog.jsx!")
else:
    print("⚠️ Target string not found")
