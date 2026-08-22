#!/usr/bin/env python3
"""
Replace all dark / black images across EZ Consultants and PRO CRM with high-resolution, light-filled, clean, vibrant, sunny corporate and tech photography.
"""

import os
import json
import re

LIGHT_IMAGES = [
    "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80", # Bright modern collaborative office
    "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1200&q=80", # Sunlit boardroom & strategy discussion
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80", # Bright analytics dashboard & laptop
    "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80", # Minimalist light desk with MacBook & coffee
    "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=1200&q=80", # Bright tech team collaboration
    "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80", # White modern architecture & blue sky
    "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=1200&q=80", # Bright consulting executive
    "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80", # Bright innovation classroom / workshop
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80", # Clean light fintech dashboard
    "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80", # Bright vibrant modern consulting
    "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80", # Sunlit team meeting with whiteboards
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80"  # Clean bright modern workspace
]

DARK_IMAGE_PATTERNS = [
    "photo-1677442136019",
    "photo-1540575467063",
    "photo-1555066931-4365d14bab8c",
    "photo-1550751827-4bd374c3f58b",
    "photo-1526374965328",
    "photo-1504384308090",
    "photo-1558494949",
    "photo-1451187580459",
    "photo-1518770660439",
    "photo-1614064641938",
    "photo-1563089145",
    "photo-1677442136019-21780ecad995"
]

def is_dark_image(url):
    if not url:
        return True
    for p in DARK_IMAGE_PATTERNS:
        if p in url:
            return True
    return False

# 1. Update EZ Consultants
EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au"
EZ_POSTS = os.path.join(EZ_DIR, "posts.json")
EZ_PUB_POSTS = os.path.join(EZ_DIR, "public", "posts.json")
EZ_BLOG_JS = os.path.join(EZ_DIR, "src", "data", "blogPosts.js")

if os.path.exists(EZ_POSTS):
    with open(EZ_POSTS, "r", encoding="utf-8") as f:
        posts = json.load(f)
    
    for i, p in enumerate(posts):
        img = p.get("image", "")
        if is_dark_image(img) or i < len(LIGHT_IMAGES):
            p["image"] = LIGHT_IMAGES[i % len(LIGHT_IMAGES)]
            p["heroImage"] = LIGHT_IMAGES[i % len(LIGHT_IMAGES)]
    
    with open(EZ_POSTS, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)
    if os.path.exists(EZ_PUB_POSTS):
        with open(EZ_PUB_POSTS, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2)
            
    print(f"✅ Updated {len(posts)} posts in EZ Consultants to ultra-bright light photography!")

    # Synchronize blogPosts.js
    if os.path.exists(EZ_BLOG_JS):
        js_content = f"""// Auto-generated from posts.json
export const blogPosts = {json.dumps(posts, indent=2)};

export const BLOG_POSTS = blogPosts;
export default blogPosts;

export function getArticleStats(slug) {{
  if (typeof window === "undefined") return {{ views: 1420, likes: 118, isLiked: false }};
  try {{
    const key = `ez_article_stats_${{slug}}`;
    const stored = localStorage.getItem(key);
    if (stored) return JSON.parse(stored);
    const post = BLOG_POSTS.find(p => p.slug === slug);
    const initial = {{ views: post && post.baseViews ? post.baseViews : 1420, likes: post && post.baseLikes ? post.baseLikes : 118, isLiked: false }};
    localStorage.setItem(key, JSON.stringify(initial));
    return initial;
  }} catch (e) {{
    return {{ views: 1420, likes: 118, isLiked: false }};
  }}
}}

export function incrementArticleView(slug) {{
  if (typeof window === "undefined") return;
  try {{
    const stats = getArticleStats(slug);
    stats.views += 1;
    localStorage.setItem(`ez_article_stats_${{slug}}`, JSON.stringify(stats));
  }} catch (e) {{}}
}}

export function toggleArticleLike(slug) {{
  if (typeof window === "undefined") return {{ delta: 0, isLiked: false }};
  try {{
    const stats = getArticleStats(slug);
    if (stats.isLiked) {{
      stats.likes = Math.max(0, stats.likes - 1);
      stats.isLiked = false;
    }} else {{
      stats.likes += 1;
      stats.isLiked = true;
    }}
    localStorage.setItem(`ez_article_stats_${{slug}}`, JSON.stringify(stats));
    return {{ delta: stats.isLiked ? 1 : -1, isLiked: stats.isLiked }};
  }} catch (e) {{
    return {{ delta: 0, isLiked: false }};
  }}
}}
"""
        with open(EZ_BLOG_JS, "w", encoding="utf-8") as f:
            f.write(js_content)
        print("✅ Synchronized EZ Consultants src/data/blogPosts.js with helper functions")

# 2. Update PRO CRM (both in Imprtant Repos/procrm-app and GitHub/procrm)
for p_dir in ["/Users/robinbakshi/Documents/Imprtant Repos/procrm-app", "/Users/robinbakshi/Documents/GitHub/procrm"]:
    p_site_js = os.path.join(p_dir, "src", "data", "site.js")
    if os.path.exists(p_site_js):
        with open(p_site_js, "r", encoding="utf-8") as f:
            site_js = f.read()
        
        # Replace dark image occurrences
        for idx, dark in enumerate(DARK_IMAGE_PATTERNS):
            replacement = LIGHT_IMAGES[idx % len(LIGHT_IMAGES)]
            # Match any unpslash url containing the dark ID
            pattern = r'https://images\.unsplash\.com/[^\s"\',\)]*' + re.escape(dark) + r'[^\s"\',\)]*'
            site_js = re.sub(pattern, replacement, site_js)
        
        with open(p_site_js, "w", encoding="utf-8") as f:
            f.write(site_js)
        print(f"✅ Updated all dark images in {p_site_js} to bright, light corporate photos!")

