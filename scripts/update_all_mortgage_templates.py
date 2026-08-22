#!/usr/bin/env python3
"""
Update All Mortgage Suburb Pages & Blog Articles
- Rebuilds all 91 suburb location landing pages with:
  1. Fixed / Sticky Col 2 on scroll (position: sticky; top: 24px;)
  2. Broker card cover image: /images/headers/marquee-background-1600x500-1.webp
  3. Large zoomed circle avatar: 116px, transform: scale(1.22), filter: brightness(1.14) contrast(1.06)
  4. 5-Star review rating: ★★★★★ (14 Google Reviews)
  5. Recent Market News moved ABOVE the suburb list
  6. Nearby Suburb Guides rendered as an accordion, closed by default with "+ View Suburbs"
- Updates all blog articles in ezmortgagebroker/pages/blog/*.html with the sticky sidebar and calculator header cover.
"""

import os
import re
import subprocess

EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
BLOG_DIR = os.path.join(EZ_DIR, "pages", "blog")
PUBLIC_BLOG_DIR = os.path.join(EZ_DIR, "public", "pages", "blog")
DIST_BLOG_DIR = os.path.join(EZ_DIR, "dist", "pages", "blog")

def main():
    print("🚀 1. Regenerating all 91 suburb location landing pages...")
    suburb_script = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/generate_suburbs_and_pillars.py"
    subprocess.run(["python3", suburb_script], check=True)
    print("✅ All 91 Suburb Location Pages Regenerated!")

    print("🚀 2. Updating all blog articles with sticky sidebar and calculator banner...")
    for target_dir in [BLOG_DIR, PUBLIC_BLOG_DIR, DIST_BLOG_DIR]:
        if not os.path.exists(target_dir):
            continue
        
        for fname in os.listdir(target_dir):
            if not fname.endswith(".html"):
                continue
            
            fpath = os.path.join(target_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                html = f.read()

            modified = False

            # 1. Update author-profile-banner from blue gradient to calculator street banner
            if "linear-gradient(135deg, #0A2540 0%, #1E3A8A 100%)" in html or "linear-gradient(135deg, #0A2540 0%, #1D4ED8 100%)" in html:
                html = re.sub(
                    r'\.author-profile-banner\s*\{[^}]*\}',
                    '.author-profile-banner { height: 105px; background-image: url(\'/images/headers/marquee-background-1600x500-1.webp\'); background-size: cover; background-position: center; }',
                    html
                )
                html = re.sub(
                    r'\.broker-cover-header\s*\{[^}]*\}',
                    '.broker-cover-header { height: 105px; width: 100%; background-image: url(\'/images/headers/marquee-background-1600x500-1.webp\'); background-size: cover; background-position: center; }',
                    html
                )
                modified = True

            # 2. Update avatar circle size & zoom
            if ".author-profile-avatar-wrap" in html:
                html = re.sub(
                    r'\.author-profile-avatar-wrap\s*\{[^}]*\}',
                    '.author-profile-avatar-wrap { width: 116px; height: 116px; border-radius: 50%; background: #ffffff; box-shadow: 0 6px 20px rgba(0,0,0,0.18); margin: -58px auto 10px; display: grid; place-items: center; padding: 4px; overflow: hidden; border: 4px solid #ffffff; }',
                    html
                )
                html = re.sub(
                    r'\.author-profile-avatar-img\s*\{[^}]*\}',
                    '.author-profile-avatar-img { width: 100%; height: 100%; object-fit: cover; object-position: center 20%; transform: scale(1.22); filter: brightness(1.14) contrast(1.06); border-radius: 50%; }',
                    html
                )
                modified = True

            # 3. Ensure article sidebar is sticky
            if ".article-sidebar" in html and "position: sticky" not in html:
                html = re.sub(
                    r'\.article-sidebar\s*\{',
                    '.article-sidebar { position: sticky; top: 24px; align-self: flex-start; ',
                    html
                )
                modified = True
            
            if ".article-layout" in html and "align-items: flex-start" not in html:
                html = re.sub(
                    r'\.article-layout\s*\{([^}]*)\}',
                    r'.article-layout {\1 align-items: flex-start; }',
                    html
                )
                modified = True

            if modified:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(html)

    print("✅ All blog articles and templates updated with sticky sidebar and calculator street banner!")

if __name__ == "__main__":
    main()
