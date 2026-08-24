#!/usr/bin/env python3
"""
Implement Master Technical SEO across all 4 websites:
- procrm.com.au
- ezconsultants.com.au
- finnova.org.au
- ezmortgagebroker.com.au

Actions:
1. Generate standard-compliant RFC 9309 `robots.txt` in root and `public/`.
2. Generate comprehensive `sitemap.xml` and `sitemap-news.xml` with Google News schema.
3. Generate `sitemap_index.xml` (Master Sitemap Index).
4. Synchronize across all project roots and `public/` build directories.
"""

import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

NOW_ISO = datetime.now(timezone.utc).astimezone().isoformat()

SITES_CONFIG = {
    "procrm": {
        "domain": "https://procrm.com.au",
        "name": "PRO CRM Australia",
        "repo_dir": "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app",
        "public_dirs": ["public", ""],
        "posts_json": "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/posts.json",
        "static_routes": [
            {"path": "/", "priority": "1.0", "changefreq": "daily"},
            {"path": "/blog", "priority": "0.9", "changefreq": "daily"},
            {"path": "/about", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/contact", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/pricing", "priority": "0.8", "changefreq": "weekly"},
            {"path": "/features", "priority": "0.8", "changefreq": "weekly"},
            {"path": "/security", "priority": "0.8", "changefreq": "monthly"},
        ]
    },
    "ezconsultants": {
        "domain": "https://ezconsultants.com.au",
        "name": "EZ Consultants Australia",
        "repo_dir": "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au",
        "public_dirs": ["public", "dist", ""],
        "posts_json": "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/posts.json",
        "static_routes": [
            {"path": "/", "priority": "1.0", "changefreq": "daily"},
            {"path": "/blog", "priority": "0.9", "changefreq": "daily"},
            {"path": "/about", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/contact", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/services", "priority": "0.8", "changefreq": "weekly"},
            {"path": "/case-studies", "priority": "0.8", "changefreq": "monthly"},
        ]
    },
    "ezmortgagebroker": {
        "domain": "https://ezmortgagebroker.com.au",
        "name": "EZ Mortgage Broker",
        "repo_dir": "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker",
        "public_dirs": ["public", "dist", ""],
        "posts_json": "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker/posts.json",
        "static_routes": [
            {"path": "/", "priority": "1.0", "changefreq": "daily"},
            {"path": "/pages/blog.html", "priority": "0.9", "changefreq": "daily"},
            {"path": "/calculators.html", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/locations.html", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/privacy-policy.html", "priority": "0.5", "changefreq": "yearly"},
            {"path": "/terms-of-use.html", "priority": "0.5", "changefreq": "yearly"},
        ]
    },
    "finnova": {
        "domain": "https://finnova.org.au",
        "name": "Finnova Australia",
        "repo_dir": "/Users/robinbakshi/Documents/Imprtant Repos/Finnova",
        "public_dirs": ["public", "dist", ""],
        "posts_json": "/Users/robinbakshi/Documents/Imprtant Repos/Finnova/posts.json",
        "static_routes": [
            {"path": "/", "priority": "1.0", "changefreq": "daily"},
            {"path": "/blog", "priority": "0.9", "changefreq": "daily"},
            {"path": "/about", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/contact", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/services", "priority": "0.8", "changefreq": "weekly"},
        ]
    },
    "ezsignature": {
        "domain": "https://ezsignature.com",
        "name": "EZ Signature Online",
        "repo_dir": "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend",
        "public_dirs": ["public", "dist", ""],
        "posts_json": "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend/public/posts.json",
        "static_routes": [
            {"path": "/", "priority": "1.0", "changefreq": "daily"},
            {"path": "/blog", "priority": "0.9", "changefreq": "daily"},
            {"path": "/pricing", "priority": "0.9", "changefreq": "weekly"},
            {"path": "/developer", "priority": "0.8", "changefreq": "weekly"},
            {"path": "/integrations", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/audit-trail", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/docusign-alternative", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/pandadoc-alternative", "priority": "0.8", "changefreq": "monthly"},
            {"path": "/about", "priority": "0.7", "changefreq": "monthly"},
        ]
    }
}

def generate_robots_txt(domain: str) -> str:
    return f"""# ==============================================================================
# Master Robots Exclusion Protocol (REP - RFC 9309 Standard)
# Domain: {domain}
# Generated: {NOW_ISO}
# ==============================================================================

User-agent: *
Allow: /
Allow: /assets/
Allow: /dist/
Allow: /images/
Allow: /css/
Allow: /js/
Disallow: /*?*filter=
Disallow: /*?*sort=
Disallow: /*?*sessionid=
Disallow: /admin/
Disallow: /api/private/

# Google Common Crawlers (Search, Images, Video, News)
User-agent: Googlebot
User-agent: Googlebot-Image
User-agent: Googlebot-Video
User-agent: Googlebot-News
User-agent: Storebot-Google
User-agent: Google-InspectionTool
Allow: /

# Google Gemini / Vertex AI Grounding & Training Permissions
User-agent: Google-Extended
Allow: /

# User-Triggered AI Agents & Fetchers
User-agent: Google-Agent
User-agent: Google-GeminiNotebook
Allow: /

# Sitemaps
Sitemap: {domain}/sitemap_index.xml
Sitemap: {domain}/sitemap.xml
Sitemap: {domain}/sitemap-news.xml
"""

def generate_sitemaps(site_key: str, config: dict):
    domain = config["domain"]
    posts_file = config["posts_json"]
    posts = []
    
    if os.path.exists(posts_file):
        try:
            with open(posts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    posts = data
                elif isinstance(data, dict) and "posts" in data:
                    posts = data["posts"]
        except Exception as e:
            print(f"Error loading posts for {site_key}: {e}")

    # 1. Main sitemap.xml
    urlset_main = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9", **{"xmlns:image": "http://www.google.com/schemas/sitemap-image/1.1"})
    
    for route in config["static_routes"]:
        url_el = ET.SubElement(urlset_main, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = f"{domain}{route['path']}"
        lastmod_el = ET.SubElement(url_el, "lastmod")
        lastmod_el.text = NOW_ISO
        priority_el = ET.SubElement(url_el, "priority")
        priority_el.text = route["priority"]

    # Add posts to main sitemap
    for post in posts:
        slug = post.get("slug") or post.get("id")
        if not slug:
            continue
        url_el = ET.SubElement(urlset_main, "url")
        loc_el = ET.SubElement(url_el, "loc")
        
        # Specific routing for ezmortgagebroker vs standard SPA
        if site_key == "ezmortgagebroker":
            loc_el.text = f"{domain}/pages/article.html?slug={slug}"
        else:
            loc_el.text = f"{domain}/blog/{slug}"
            
        lastmod_el = ET.SubElement(url_el, "lastmod")
        lastmod_el.text = post.get("date") or NOW_ISO
        priority_el = ET.SubElement(url_el, "priority")
        priority_el.text = "0.8"
        
        if post.get("image"):
            img_el = ET.SubElement(url_el, "image:image")
            img_loc = ET.SubElement(img_el, "image:loc")
            img_loc.text = post.get("image")

    sitemap_xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset_main, encoding="utf-8").decode("utf-8")

    # 2. News sitemap (sitemap-news.xml) for recent breaking articles (<48h)
    urlset_news = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9", **{"xmlns:news": "http://www.google.com/schemas/sitemap-news/0.9"})
    
    for post in posts[:15]: # Top 15 recent
        slug = post.get("slug") or post.get("id")
        if not slug:
            continue
        url_el = ET.SubElement(urlset_news, "url")
        loc_el = ET.SubElement(url_el, "loc")
        if site_key == "ezmortgagebroker":
            loc_el.text = f"{domain}/pages/article.html?slug={slug}"
        else:
            loc_el.text = f"{domain}/blog/{slug}"
            
        news_el = ET.SubElement(url_el, "news:news")
        pub_el = ET.SubElement(news_el, "news:publication")
        name_el = ET.SubElement(pub_el, "news:name")
        name_el.text = config["name"]
        lang_el = ET.SubElement(pub_el, "news:language")
        lang_el.text = "en"
        
        pub_date_el = ET.SubElement(news_el, "news:publication_date")
        pub_date_el.text = post.get("date") or NOW_ISO
        
        title_el = ET.SubElement(news_el, "news:title")
        title_el.text = post.get("title") or "Market & Technology Intelligence"

    sitemap_news_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset_news, encoding="utf-8").decode("utf-8")

    # 3. Master Sitemap Index (sitemap_index.xml)
    sitemapindex = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    s1 = ET.SubElement(sitemapindex, "sitemap")
    loc1 = ET.SubElement(s1, "loc")
    loc1.text = f"{domain}/sitemap.xml"
    lm1 = ET.SubElement(s1, "lastmod")
    lm1.text = NOW_ISO

    s2 = ET.SubElement(sitemapindex, "sitemap")
    loc2 = ET.SubElement(s2, "loc")
    loc2.text = f"{domain}/sitemap-news.xml"
    lm2 = ET.SubElement(s2, "lastmod")
    lm2.text = NOW_ISO

    sitemap_index_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(sitemapindex, encoding="utf-8").decode("utf-8")

    return sitemap_xml_str, sitemap_news_str, sitemap_index_str

def deploy():
    print(f"🚀 Deploying Master Technical SEO standards across all sites...")
    
    for site_key, config in SITES_CONFIG.items():
        repo_dir = config["repo_dir"]
        if not os.path.exists(repo_dir):
            print(f"Skipping missing repo: {repo_dir}")
            continue
            
        print(f"\n📂 Processing {site_key} ({config['domain']})...")
        robots_txt = generate_robots_txt(config["domain"])
        sitemap_xml, sitemap_news, sitemap_index = generate_sitemaps(site_key, config)

        for p_sub in config["public_dirs"]:
            target_dir = os.path.join(repo_dir, p_sub) if p_sub else repo_dir
            if not os.path.exists(target_dir):
                try:
                    os.makedirs(target_dir, exist_ok=True)
                except Exception:
                    continue

            # Write robots.txt
            with open(os.path.join(target_dir, "robots.txt"), "w", encoding="utf-8") as f:
                f.write(robots_txt)
            
            # Write sitemap.xml
            with open(os.path.join(target_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
                f.write(sitemap_xml)
                
            # Write sitemap-news.xml
            with open(os.path.join(target_dir, "sitemap-news.xml"), "w", encoding="utf-8") as f:
                f.write(sitemap_news)

            # Write sitemap_index.xml
            with open(os.path.join(target_dir, "sitemap_index.xml"), "w", encoding="utf-8") as f:
                f.write(sitemap_index)

            print(f"  ✅ Written robots.txt & multi-sitemaps to {target_dir}")

if __name__ == "__main__":
    deploy()
