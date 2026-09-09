#!/usr/bin/env python3
"""
EZ Mortgage Broker Remediation Script (High-Precision Tuning)
============================================================
1. Analyzes all articles in ezmortgagebroker/pages/blog and ezmortgagebroker/archive/purged_templates
2. Accurately extracts <article> body content:
   - Identifies canned templates: contains "The Reserve Bank of Australia and major retail banks have updated residential mortgage assessment benchmarks"
   - Identifies thin stubs: non-template with < 200 words in <article> body
   - Identifies genuine articles: non-template with >= 200 words in <article> body
3. Restores genuine articles to pages/blog/ and public/pages/blog/
4. Keeps ONLY canned templates and thin stubs in archive/purged_templates/
5. Synchronizes posts.json, public/posts.json, and dist/posts.json with verified genuine articles
6. Updates _redirects and public/_redirects with 301 redirects for purged items
"""

import os
import glob
import json
import re
import shutil

EZ_DIR = "/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker"
BLOG_DIR = os.path.join(EZ_DIR, "pages", "blog")
PUBLIC_BLOG_DIR = os.path.join(EZ_DIR, "public", "pages", "blog")
DIST_BLOG_DIR = os.path.join(EZ_DIR, "dist", "pages", "blog")
ARCHIVE_DIR = os.path.join(EZ_DIR, "archive", "purged_templates")

POSTS_JSON = os.path.join(EZ_DIR, "posts.json")
PUBLIC_POSTS_JSON = os.path.join(EZ_DIR, "public", "posts.json")
DIST_POSTS_JSON = os.path.join(EZ_DIR, "dist", "posts.json")

REDIRECTS_FILE = os.path.join(EZ_DIR, "_redirects")
PUBLIC_REDIRECTS_FILE = os.path.join(EZ_DIR, "public", "_redirects")

TEMPLATE_SIGNATURE = "The Reserve Bank of Australia and major retail banks have updated residential mortgage assessment benchmarks"

def get_article_metrics(content):
    is_template = TEMPLATE_SIGNATURE in content
    
    match = re.search(r"<article[^>]*>(.*?)</article>", content, re.DOTALL)
    if match:
        body_html = match.group(1)
    else:
        body_html = content
        
    clean_text = re.sub(r"<script.*?</script>", "", body_html, flags=re.DOTALL)
    clean_text = re.sub(r"<style.*?</style>", "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"<[^>]+>", " ", clean_text)
    words = clean_text.split()
    article_words = len(words)
    
    return {
        "is_template": is_template,
        "is_thin": (article_words < 200) and not is_template,
        "is_genuine": (article_words >= 200) and not is_template,
        "words": article_words
    }

def main():
    print("🚀 Running High-Precision EZ Mortgage Broker Remediation...")
    
    # Collect all HTML files from both active blog dir and archive dir
    active_files = glob.glob(os.path.join(BLOG_DIR, "*.html"))
    archived_files = glob.glob(os.path.join(ARCHIVE_DIR, "*.html"))
    all_files = list(set(active_files + archived_files))
    
    print(f"Total files examined: {len(all_files)}")
    
    genuine_files = []
    purged_files = []
    
    for fpath in all_files:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
            content = fh.read()
            
        metrics = get_article_metrics(content)
        fname = os.path.basename(fpath)
        
        if metrics["is_genuine"]:
            genuine_files.append((fname, fpath))
        else:
            purged_files.append((fname, fpath, "template" if metrics["is_template"] else "thin_stub"))
            
    print(f"🌟 Verified Genuine Articles: {len(genuine_files)}")
    print(f"🗑️ Purged (Templates & Thin Stubs): {len(purged_files)}")
    
    # Move genuine files into pages/blog/ and public/pages/blog/
    for fname, source_path in genuine_files:
        dest_active = os.path.join(BLOG_DIR, fname)
        if source_path != dest_active:
            shutil.move(source_path, dest_active)
        # Copy to public
        pub_dest = os.path.join(PUBLIC_BLOG_DIR, fname)
        shutil.copy2(dest_active, pub_dest)
        
    # Move purged files into archive/purged_templates/
    for fname, source_path, reason in purged_files:
        dest_arch = os.path.join(ARCHIVE_DIR, fname)
        if source_path != dest_arch:
            shutil.move(source_path, dest_arch)
        # Remove from active public/dist if present
        pub_dest = os.path.join(PUBLIC_BLOG_DIR, fname)
        if os.path.exists(pub_dest):
            os.remove(pub_dest)
        dist_dest = os.path.join(DIST_BLOG_DIR, fname)
        if os.path.exists(dist_dest):
            os.remove(dist_dest)

    # Reconstruct posts.json from genuine files
    genuine_slugs = {fname.replace(".html", "") for fname, _ in genuine_files}
    purged_slugs = {fname.replace(".html", "") for fname, _, _ in purged_files}
    
    # Load original master posts if available, or build metadata from HTML
    # We load from Blogs-Content/posts.json as the baseline pool
    blogs_posts_path = "/Volumes/Samsung SSD 2TB/03. Documents/GitHub/Blogs-Content/posts.json"
    with open(blogs_posts_path, "r", encoding="utf-8") as f:
        blogs_posts = json.load(f)
        
    # Index posts by slug/id
    post_map = {}
    for p in blogs_posts:
        s = p.get("slug") or p.get("id")
        if s:
            post_map[s] = p
            
    new_ez_posts = []
    for fname, _ in genuine_files:
        slug = fname.replace(".html", "")
        if slug in post_map:
            new_ez_posts.append(post_map[slug])
        else:
            # Extract basic metadata from HTML
            with open(os.path.join(BLOG_DIR, fname), "r", encoding="utf-8", errors="ignore") as fh:
                html = fh.read()
            title_m = re.search(r"<title>(.*?)</title>", html)
            title = title_m.group(1).split("|")[0].strip() if title_m else slug.replace("-", " ").title()
            desc_m = re.search(r'<meta name="description" content="(.*?)">', html)
            desc = desc_m.group(1).strip() if desc_m else ""
            
            new_ez_posts.append({
                "id": slug,
                "slug": slug,
                "title": title,
                "category": "Mortgage Advisory",
                "badge": "VERIFIED BRIEF",
                "date": "03-Sep-2026",
                "iso_date": "2026-09-03T05:30:00Z",
                "readTime": "5 min read",
                "author": "R BAKSHI",
                "authorRole": "Principal Mortgage Broker",
                "authorImg": "/images/ez-mortgage-broker.webp",
                "excerpt": desc[:220] if desc else title,
                "image": "/images/assets-ez-mortgage-broker/australian-home-mortgage-approval.jpg",
                "url": f"/pages/blog/{slug}.html"
            })
            
    print(f"✅ Generated {len(new_ez_posts)} active posts for ezmortgagebroker posts.json")
    
    for pjson_path in [POSTS_JSON, PUBLIC_POSTS_JSON, DIST_POSTS_JSON]:
        if os.path.exists(os.path.dirname(pjson_path)):
            with open(pjson_path, "w", encoding="utf-8") as f:
                json.dump(new_ez_posts, f, indent=2)
            print(f"  Saved {pjson_path}")
            
    # Update _redirects
    for red_path in [REDIRECTS_FILE, PUBLIC_REDIRECTS_FILE]:
        existing_lines = []
        if os.path.exists(red_path):
            with open(red_path, "r", encoding="utf-8") as f:
                existing_lines = [line.strip() for line in f if line.strip()]
                
        # Remove any redirect for genuine slugs
        cleaned_lines = []
        for line in existing_lines:
            match = re.match(r"^/pages/blog/([^.]+)\.html", line)
            if match and match.group(1) in genuine_slugs:
                continue # Do not redirect genuine active posts!
            cleaned_lines.append(line)
            
        # Ensure all purged slugs have a 301 redirect
        current_redirect_sources = {line.split()[0] for line in cleaned_lines if " " in line}
        new_rules = []
        for slug in purged_slugs:
            src = f"/pages/blog/{slug}.html"
            if src not in current_redirect_sources:
                new_rules.append(f"{src} /pages/blog.html 301")
                
        final_redirects = "\n".join(new_rules + cleaned_lines)
        with open(red_path, "w", encoding="utf-8") as f:
            f.write(final_redirects + "\n")
        print(f"✅ Updated {red_path} (removed active redirects, ensured {len(new_rules)} purged redirects)")

    print("🎉 High-Precision EZ Mortgage Broker Remediation Complete!")

if __name__ == "__main__":
    main()
