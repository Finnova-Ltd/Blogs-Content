#!/usr/bin/env python3
"""
Purge All 1,426 Template / Hollow Blog Articles (Option 3)
FINNOVA / EZMORTGAGE BROKERAGE • CONTENT PURITY & REPUTATION ENGINE

1. Deletes all 1,426 identified hollow/template HTML articles from ezmortgagebroker/pages/blog/.
2. Establishes 301 Permanent Redirects for all deleted URLs pointing to /pages/blog.html
   to protect search ranking and prevent 404 crawl errors.
3. Updates posts.json and blog index to ensure 100% clean, non-templated content.
"""

import os
import sys
import json
import glob
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EZ_DIR = Path("/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker")
AUDIT_FILE = BASE_DIR / "scripts" / "asset_cache" / "template_articles_audit.json"
POSTS_FILE = BASE_DIR / "posts.json"
EZ_POSTS_FILE = EZ_DIR / "posts.json"

def purge_template_articles():
    if not AUDIT_FILE.exists():
        print(f"Audit file not found: {AUDIT_FILE}")
        return

    with open(AUDIT_FILE, "r") as f:
        template_articles = json.load(f)

    print(f"Loaded {len(template_articles)} template articles targeted for deletion.")

    deleted_count = 0
    deleted_filenames = set()
    redirect_rules = []

    # 1. Delete files from ezmortgagebroker/pages/blog
    blog_dir = EZ_DIR / "pages" / "blog"
    for item in template_articles:
        fname = item["filename"]
        fpath = blog_dir / fname
        if fpath.exists():
            fpath.unlink()
            deleted_count += 1
            deleted_filenames.add(fname)
            # Create 301 redirect rule: /pages/blog/slug.html -> /pages/blog.html
            redirect_rules.append(f"/pages/blog/{fname} /pages/blog.html 301")

    print(f"✅ Successfully deleted {deleted_count} template HTML files from {blog_dir}")

    # 2. Append 301 redirect rules to _redirects files
    redirect_targets = [
        EZ_DIR / "_redirects",
        EZ_DIR / "public" / "_redirects"
    ]
    
    redirect_block = "\n# --- Deleted Template Articles 301 Redirects ---\n" + "\n".join(redirect_rules) + "\n"

    for r_file in redirect_targets:
        if r_file.exists():
            with open(r_file, "r") as rf:
                existing = rf.read()
            if "# --- Deleted Template Articles 301 Redirects ---" not in existing:
                with open(r_file, "a") as rf:
                    rf.write(redirect_block)
                print(f"✅ Added {len(redirect_rules)} 301 redirect rules to {r_file}")
        else:
            with open(r_file, "w") as rf:
                rf.write(redirect_block)
            print(f"✅ Created {r_file} with {len(redirect_rules)} 301 redirect rules.")

    # 3. Clean posts.json
    deleted_slugs = {f.replace(".html", "") for f in deleted_filenames}
    if POSTS_FILE.exists():
        with open(POSTS_FILE, "r") as pf:
            posts = json.load(pf)
        original_len = len(posts)
        clean_posts = [p for p in posts if p.get("slug") not in deleted_slugs]
        with open(POSTS_FILE, "w") as pf:
            json.dump(clean_posts, pf, indent=2)
        print(f"✅ Updated {POSTS_FILE}: reduced from {original_len} to {len(clean_posts)} posts.")
        if EZ_POSTS_FILE.exists():
            with open(EZ_POSTS_FILE, "w") as epf:
                json.dump(clean_posts, epf, indent=2)

    # 4. Check remaining articles
    remaining_files = list(blog_dir.glob("*.html"))
    # exclude index.html
    remaining_articles = [f for f in remaining_files if f.name not in ["index.html"]]
    print(f"📊 Remaining Genuine Articles in ezmortgagebroker/pages/blog: {len(remaining_articles)}")

if __name__ == "__main__":
    purge_template_articles()
