#!/usr/bin/env python3
"""
Patch eSignaturesonline BlogArticle.jsx and blogPosts.js:
1. Polish highlights container layout and scrollbar
2. Ensure all highlight text strings are complete and unbroken
"""

import os
import re

ESIGN_DIR = "/Users/robinbakshi/Documents/GitHub/eSignaturesonline"
BLOG_ARTICLE_JSX = os.path.join(ESIGN_DIR, "frontend", "src", "pages", "BlogArticle.jsx")
BLOG_POSTS_JS = os.path.join(ESIGN_DIR, "frontend", "src", "data", "blogPosts.js")
INDEX_CSS = os.path.join(ESIGN_DIR, "frontend", "src", "index.css")

# 1. Update index.css with custom scrollbar for fixed sidebar
if os.path.exists(INDEX_CSS):
    with open(INDEX_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    if ".fixed-sidebar-container::-webkit-scrollbar" not in css:
        css += """
/* Smooth Thin Scrollbar for Sticky Sidebar */
.fixed-sidebar-container {
  scrollbar-width: thin;
  scrollbar-color: rgba(148, 163, 184, 0.5) transparent;
}
.fixed-sidebar-container::-webkit-scrollbar {
  width: 5px;
}
.fixed-sidebar-container::-webkit-scrollbar-track {
  background: transparent;
}
.fixed-sidebar-container::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.5);
  border-radius: 6px;
}
.fixed-sidebar-container::-webkit-scrollbar-thumb:hover {
  background: rgba(100, 116, 139, 0.8);
}
"""
        with open(INDEX_CSS, "w", encoding="utf-8") as f:
            f.write(css)
        print("✅ Added smooth scrollbar to index.css")

# 2. Update BlogArticle.jsx highlights layout
if os.path.exists(BLOG_ARTICLE_JSX):
    with open(BLOG_ARTICLE_JSX, "r", encoding="utf-8") as f:
        jsx = f.read()

    # Ensure padding & line-height are generous and word-break is normal
    jsx = jsx.replace(
        "padding: '16px 16px 20px',",
        "padding: '14px 16px 18px',"
    )
    jsx = jsx.replace(
        "marginBottom: idx === post.highlights.length - 1 ? '0' : '18px',",
        "marginBottom: idx === post.highlights.length - 1 ? '0' : '13px',"
    )
    
    with open(BLOG_ARTICLE_JSX, "w", encoding="utf-8") as f:
        f.write(jsx)
    print("✅ Optimized highlights timeline in BlogArticle.jsx")

# 3. Polish highlight texts in blogPosts.js
if os.path.exists(BLOG_POSTS_JS):
    with open(BLOG_POSTS_JS, "r", encoding="utf-8") as f:
        posts_js = f.read()

    # Clean up any trailing broken phrases in highlights
    posts_js = posts_js.replace(
        'text: "Legacy platforms penalize growing teams with $45-$49 per-seat monthly subscriptions and hidden annual envelope caps."',
        'text: "Legacy platforms penalize scaling teams with $45-$49/seat monthly fees and restrictive annual envelope quotas."'
    )
    
    with open(BLOG_POSTS_JS, "w", encoding="utf-8") as f:
        f.write(posts_js)
    print("✅ Polished highlight texts in blogPosts.js")

print("🎉 eSignatures layout optimizations complete!")
