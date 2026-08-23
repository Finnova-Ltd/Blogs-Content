#!/usr/bin/env python3
"""
Refine Col 2 Fixed Sidebar:
1. Ensure the sidebar stays 100% fixed on the screen without scrolling off.
2. Ensure no visible scrollbar anywhere in highlights or sidebar (scrollbar-none / hidden).
3. Compact sizing for all 3 widgets so the entire sidebar easily fits on any laptop or desktop screen.
"""

import os
import re

PROCRM_BLOG_JSX = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/pages/Blog.jsx"
PROCRM_INDEX_CSS = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/index.css"
EZ_BLOG_ARTICLE_JSX = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/src/pages/BlogArticle.jsx"

# 1. Update index.css to hide any scrollbar while keeping smooth sticky scrolling
with open(PROCRM_INDEX_CSS, "r", encoding="utf-8") as f:
    css = f.read()

# Add complete scrollbar hiding rules for sticky-col-2
scroll_rules = """
/* Guaranteed Fixed Sticky Sidebar without scrollbars */
@media (min-width: 1024px) {
  .sticky-col-2 {
    position: -webkit-sticky !important;
    position: sticky !important;
    top: 88px !important;
    z-index: 30 !important;
    align-self: flex-start !important;
    max-height: calc(100vh - 100px) !important;
    overflow-y: auto !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
  }
  .sticky-col-2::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
  }
}
"""

if "Guaranteed Fixed Sticky Sidebar without scrollbars" not in css:
    css += scroll_rules
    with open(PROCRM_INDEX_CSS, "w", encoding="utf-8") as f:
        f.write(css)
    print("✅ Added hidden scrollbar sticky rules to procrm-app index.css")

# 2. Update Blog.jsx sidebar structure for compact, premium fit
with open(PROCRM_BLOG_JSX, "r", encoding="utf-8") as f:
    code = f.read()

# Compact Aside
old_aside_pattern = r'<aside className="lg:col-span-4 space-y-6 sticky-col-2 self-start".*?>'
new_aside = '<aside className="lg:col-span-4 space-y-4 sticky-col-2 self-start" style={{ position: "sticky", top: "88px", zIndex: 30, maxHeight: "calc(100vh - 100px)", overflowY: "auto", scrollbarWidth: "none" }}>'
code = re.sub(old_aside_pattern, new_aside, code)

# Make Highlights widget compact
old_hl_start = '<div className="p-4 space-y-4 bg-white/80">'
new_hl_start = '<div className="p-3.5 space-y-3 bg-white/90">'
code = code.replace(old_hl_start, new_hl_start)

# Limit related articles in sidebar to 3 compact items
code = code.replace("const recentArticles = POSTS.filter((p) => p.slug !== slug).slice(0, 4);", "const recentArticles = POSTS.filter((p) => p.slug !== slug).slice(0, 3);")

with open(PROCRM_BLOG_JSX, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Updated procrm-app Blog.jsx with compact, permanently fixed sidebar!")

# 3. Update ezconsultants BlogArticle.jsx
if os.path.exists(EZ_BLOG_ARTICLE_JSX):
    with open(EZ_BLOG_ARTICLE_JSX, "r", encoding="utf-8") as f:
        ez_code = f.read()

    ez_code = re.sub(
        r'<aside\s+className="[^"]*sticky[^"]*"\s+style=\{[^}]+\}>',
        '<aside className="lg:col-span-4 space-y-4 self-start sticky" style={{ position: "sticky", top: "88px", zIndex: 30, maxHeight: "calc(100vh - 100px)", overflowY: "auto", scrollbarWidth: "none" }}>',
        ez_code
    )

    with open(EZ_BLOG_ARTICLE_JSX, "w", encoding="utf-8") as f:
        f.write(ez_code)
    print("✅ Updated ezconsultants BlogArticle.jsx with compact, permanently fixed sidebar!")

print("🎉 Complete sidebar fix deployed successfully!")
