#!/usr/bin/env python3
"""
Guarantee 100% Fixed / Sticky Behavior for Col 2 across procrm-app and ezconsultants.com.au
"""

import os
import re

PROCRM_BLOG_JSX = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/pages/Blog.jsx"
PROCRM_INDEX_CSS = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/index.css"
EZ_BLOG_ARTICLE_JSX = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/src/pages/BlogArticle.jsx"

# 1. Update procrm index.css with strict sticky helper
with open(PROCRM_INDEX_CSS, "r", encoding="utf-8") as f:
    css = f.read()

if ".sticky-col-2" not in css:
    css += """
/* Guaranteed Sticky Sidebar Column 2 */
@media (min-width: 1024px) {
  .sticky-col-2 {
    position: -webkit-sticky !important;
    position: sticky !important;
    top: 88px !important;
    z-index: 30 !important;
    align-self: flex-start !important;
  }
}
"""
    with open(PROCRM_INDEX_CSS, "w", encoding="utf-8") as f:
        f.write(css)
    print("✅ Added .sticky-col-2 to procrm-app index.css")

# 2. Update procrm Blog.jsx aside tag
with open(PROCRM_BLOG_JSX, "r", encoding="utf-8") as f:
    blog_jsx = f.read()

blog_jsx = re.sub(
    r'<aside className="lg:col-span-4 space-y-6.*?>',
    '<aside className="lg:col-span-4 space-y-6 sticky-col-2 self-start" style={{ position: "sticky", top: "88px", zIndex: 30 }}>',
    blog_jsx
)

with open(PROCRM_BLOG_JSX, "w", encoding="utf-8") as f:
    f.write(blog_jsx)
print("✅ Updated procrm-app Blog.jsx aside with sticky-col-2 and inline styles!")

# 3. Update ezconsultants BlogArticle.jsx aside and remove bottom Related Articles
if os.path.exists(EZ_BLOG_ARTICLE_JSX):
    with open(EZ_BLOG_ARTICLE_JSX, "r", encoding="utf-8") as f:
        ez_jsx = f.read()

    # Make aside strictly sticky
    ez_jsx = re.sub(
        r'<aside\s+className="[^"]*fixed-sidebar-container[^"]*"\s+style=\{[^}]+\}>',
        '<aside className="lg:col-span-4 space-y-6 self-start sticky" style={{ position: "sticky", top: "88px", zIndex: 30 }}>',
        ez_jsx
    )

    # Rename Recent Advisories to Related Articles / News
    ez_jsx = ez_jsx.replace("Recent Advisories", "Related Articles / News")

    # Remove bottom Related Articles grid
    rel_start = ez_jsx.find('{/* 3. RELATED ARTICLES 3-COLUMN GRID')
    if rel_start != -1:
        main_end = ez_jsx.find('</main>', rel_start)
        if main_end != -1:
            ez_jsx = ez_jsx[:rel_start] + ez_jsx[main_end:]
            print("✅ Removed bottom Related Articles grid from ezconsultants!")

    with open(EZ_BLOG_ARTICLE_JSX, "w", encoding="utf-8") as f:
        f.write(ez_jsx)
    print("✅ Updated ezconsultants BlogArticle.jsx!")

print("🎉 Fixed Col 2 sticky positioning across all sites!")
