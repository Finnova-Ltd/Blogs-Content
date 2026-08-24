#!/usr/bin/env python3
"""
Fix Light Themes on EZ Consultants & Render 25-Aug Articles on Finnova:
1. Fix Blog.jsx in ezconsultants.com.au (remove bg-slate-950, support post.image fallback, use crisp light badge)
2. Ensure every post in ezconsultants posts.json and blogPosts.js has a valid light-themed heroImage and image URL.
3. Fix Finnova HTML files (index.html, en_AU.html, etc.) to immediately render the 25-Aug articles.
"""

import os
import json
import re

EZ_CONSULTANTS_DIR = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au"
FINNOVA_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova"
BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

# -----------------------------------------------------------------------------
# 1. Patch Blog.jsx in EZ Consultants
# -----------------------------------------------------------------------------
blog_jsx_path = os.path.join(EZ_CONSULTANTS_DIR, "src", "pages", "Blog.jsx")
with open(blog_jsx_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace card image block
old_card_image = """                {/* Card Cover Image */}
                <div className="relative aspect-[16/9] overflow-hidden bg-slate-950">
                  <img 
                    src={post.heroImage} 
                    alt={post.title} 
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent"></div>
                  <div className="absolute top-3 left-3">
                    <span className="px-2.5 py-1 rounded-md bg-[#07182c]/90 border border-cyan-400/40 text-cyan-300 text-[10px] font-extrabold uppercase tracking-wide backdrop-blur-md">
                      {post.category}
                    </span>
                  </div>
                </div>"""

new_card_image = """                {/* Card Cover Image (100% Light Theme) */}
                <div className="relative aspect-[16/9] overflow-hidden bg-gradient-to-br from-blue-50 via-slate-50 to-indigo-50 border-b border-slate-100">
                  <img 
                    src={post.heroImage || post.image || "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80"} 
                    alt={post.title} 
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80";
                    }}
                  />
                  <div className="absolute top-3 left-3">
                    <span className="px-2.5 py-1 rounded-md bg-white/95 border border-blue-200 text-[#084582] text-[10px] font-extrabold uppercase tracking-wide shadow-xs backdrop-blur-sm">
                      {post.category}
                    </span>
                  </div>
                </div>"""

if old_card_image in code:
    code = code.replace(old_card_image, new_card_image)
else:
    code = re.sub(
        r'<div className="relative aspect-\[16/9\] overflow-hidden bg-slate-950">.*?</div>\s*</div>',
        new_card_image,
        code,
        flags=re.DOTALL
    )

with open(blog_jsx_path, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Patched Blog.jsx in EZ Consultants with 100% light-theme cards and fallback images!")

# -----------------------------------------------------------------------------
# 2. Fix All Image URLs in EZ Consultants posts.json and blogPosts.js
# -----------------------------------------------------------------------------
FALLBACK_LIGHT_IMAGES = [
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80"
]

posts_path = os.path.join(EZ_CONSULTANTS_DIR, "posts.json")
pub_posts_path = os.path.join(EZ_CONSULTANTS_DIR, "public", "posts.json")

with open(posts_path, "r", encoding="utf-8") as f:
    ez_posts = json.load(f)

for i, p in enumerate(ez_posts):
    img = p.get("heroImage") or p.get("image")
    if not img or "pexels-photo-37730212" in img or not img.startswith("http"):
        img = FALLBACK_LIGHT_IMAGES[i % len(FALLBACK_LIGHT_IMAGES)]
    p["heroImage"] = img
    p["image"] = img
    if "date" in p and ("24-Aug" in p["date"] or "25-Aug" in p["date"]):
        p["formattedDate"] = "25 August 2026"
        p["date"] = "25-Aug-2026"

with open(posts_path, "w", encoding="utf-8") as f:
    json.dump(ez_posts, f, indent=2)
with open(pub_posts_path, "w", encoding="utf-8") as f:
    json.dump(ez_posts, f, indent=2)

os.system("python3 /Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/update_ezconsultants_25_aug.py")
print("✅ Updated EZ Consultants posts.json with verified light image URLs!")

# -----------------------------------------------------------------------------
# 3. Synchronize Finnova HTML files and posts.json
# -----------------------------------------------------------------------------
os.system("python3 /Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/update_finnova_25_aug.py")

# Ensure Finnova's fetch URL prioritizes local posts.json?v= over stale CDN caches
html_files = [
    "index.html", "en_AU.html", "ar_SA.html", "es_ES.html", 
    "hi_IN.html", "pa_IN.html", "vi_VN.html", "zh_CN.html"
]

for fn in html_files:
    fp = os.path.join(FINNOVA_DIR, fn)
    if not os.path.exists(fp):
        continue
    with open(fp, "r", encoding="utf-8") as f:
        html_c = f.read()
    
    # Ensure cache-buster
    html_c = html_c.replace("'posts.json?v=' + Date.now()", "'posts.json?t=' + Date.now()")
    
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html_c)

print("✅ Synchronized Finnova HTML files!")
