import os
import re
import json

def audit_procrm():
    site_js = "/Volumes/Samsung SSD 2TB/03. Documents/Imprtant Repos/procrm-app/src/data/site.js"
    if not os.path.exists(site_js):
        return {"error": "site.js not found"}
        
    with open(site_js, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    # Extract POSTS array
    posts_match = re.search(r'export\s+const\s+POSTS\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not posts_match:
        # try without export
        posts_match = re.search(r'const\s+POSTS\s*=\s*\[(.*?)\];', content, re.DOTALL)
        
    posts = []
    if posts_match:
        posts_raw = posts_match.group(1)
        # find individual post objects
        # match slug, title, content / excerpt
        items = re.findall(r'\{\s*slug:\s*["\']([^"\']+)["\'],\s*title:\s*["\']([^"\']+)["\'](.*?)\}', posts_raw, re.DOTALL)
        for slug, title, rest in items:
            excerpt_m = re.search(r'excerpt:\s*["\'](.*?)["\']', rest, re.DOTALL)
            excerpt = excerpt_m.group(1) if excerpt_m else ""
            content_m = re.search(r'content:\s*["\'](.*?)["\']', rest, re.DOTALL)
            body = content_m.group(1) if content_m else ""
            posts.append({
                "slug": slug,
                "title": title,
                "excerpt": excerpt,
                "body_len": len(body.split())
            })
            
    # Check static HTML in procrm if any
    static_html_files = []
    for root_cand in ["/Volumes/Samsung SSD 2TB/03. Documents/Imprtant Repos/procrm-app/public", "/Volumes/Samsung SSD 2TB/03. Documents/Imprtant Repos/procrm-app/dist"]:
        if os.path.exists(root_cand):
            for r, d, files in os.walk(root_cand):
                for fl in files:
                    if fl.endswith(".html") and "blog" in r:
                        static_html_files.append(os.path.join(r, fl))
                        
    return {
        "total_posts_in_code": len(posts),
        "posts": posts,
        "static_html_files": len(static_html_files)
    }

def audit_ezconsultants():
    ez_dir = "/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezconsultants.com.au"
    blog_dir = os.path.join(ez_dir, "pages", "blog")
    posts_json = os.path.join(ez_dir, "public", "posts.json")
    posts_data_js = os.path.join(ez_dir, "src", "data", "blogPosts.js")
    
    html_files = []
    if os.path.exists(blog_dir):
        html_files = [f for f in os.listdir(blog_dir) if f.endswith(".html")]
        
    posts_json_items = []
    if os.path.exists(posts_json):
        try:
            with open(posts_json, "r", encoding="utf-8") as fp:
                posts_json_items = json.load(fp)
        except Exception:
            pass
            
    posts_js_items = []
    if os.path.exists(posts_data_js):
        with open(posts_data_js, "r", encoding="utf-8", errors="ignore") as fp:
            c = fp.read()
            slugs = re.findall(r'slug:\s*["\']([^"\']+)["\']', c)
            posts_js_items = slugs
            
    # Audit each HTML file
    audit_results = {
        "total_html_files": len(html_files),
        "total_posts_json": len(posts_json_items),
        "total_posts_js": len(posts_js_items),
        "blank_or_thin": [],
        "canned_boilerplate": [],
        "brand_mismatch": [],
        "verified_high_quality": []
    }
    
    for fname in sorted(html_files):
        fpath = os.path.join(blog_dir, fname)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
            html = fp.read()
            
        t_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = t_match.group(1).split('|')[0].strip() if t_match else fname
        
        # Word count approximation
        clean_text = re.sub(r'<[^>]+>', ' ', html)
        words = clean_text.split()
        word_count = len(words)
        
        # Canned check
        is_canned = False
        if "the reserve bank of australia" in html.lower() or "variable mortgage rates" in html.lower():
            is_canned = True
            
        is_mismatch = False
        if "r bakshi" in html.lower() and "mfaa" in html.lower():
            is_mismatch = True
            
        meta = {"file": fname, "title": title, "word_count": word_count}
        if is_canned:
            audit_results["canned_boilerplate"].append(meta)
        elif is_mismatch:
            audit_results["brand_mismatch"].append(meta)
        elif word_count < 300:
            audit_results["blank_or_thin"].append(meta)
        else:
            audit_results["verified_high_quality"].append(meta)
            
    return audit_results

print("--- AUDITING PROCRM.COM.AU ---")
procrm_res = audit_procrm()
print(f"Procrm Total In-Code Posts: {procrm_res['total_posts_in_code']}")
print(f"Procrm Static HTML Blog Files: {procrm_res['static_html_files']}")
for p in procrm_res['posts'][:10]:
    print(f" - [{p['slug']}] {p['title']} ({p['body_len']} words)")

print("\n--- AUDITING EZCONSULTANTS.COM.AU ---")
ezc_res = audit_ezconsultants()
print(f"EZ Consultants Total HTML Blog Files: {ezc_res['total_html_files']}")
print(f"EZ Consultants Total Posts in posts.json: {ezc_res['total_posts_json']}")
print(f"EZ Consultants Total Posts in blogPosts.js: {ezc_res['total_posts_js']}")
print(f" ❌ Canned Boilerplate: {len(ezc_res['canned_boilerplate'])}")
print(f" ❌ Brand Mismatch: {len(ezc_res['brand_mismatch'])}")
print(f" ❌ Blank / Thin (<300 words): {len(ezc_res['blank_or_thin'])}")
print(f" ✅ Verified High Quality: {len(ezc_res['verified_high_quality'])}")

if ezc_res['brand_mismatch']:
    print("\nEZ Consultants Brand Mismatches:")
    for m in ezc_res['brand_mismatch']:
        print(f" - {m['file']}: {m['title']}")
