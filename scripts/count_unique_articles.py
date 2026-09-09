import json, os, glob, re, subprocess

finnova_path = "/Volumes/Samsung SSD 2TB/03. Documents/Imprtant Repos/Finnova/posts.json"
ezmortgage_path = "/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker/posts.json"
ezconsultants_html = "/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezconsultants.com.au/pages/blog"

with open(finnova_path) as f:
    finnova = {p["slug"]: p["title"] for p in json.load(f)}

with open(ezmortgage_path) as f:
    ezmortgage = {p["slug"]: p["title"] for p in json.load(f)}

ezconsultants = {}
for f in glob.glob(os.path.join(ezconsultants_html, "*.html")):
    slug = os.path.basename(f).replace(".html", "")
    with open(f, encoding="utf-8", errors="ignore") as fh:
        c = fh.read()
    m = re.search(r"<title>(.*?)</title>", c)
    ezconsultants[slug] = m.group(1).split("|")[0].strip() if m else slug

procrm_json = subprocess.check_output([
    "node", "-e",
    "import('./src/data/site.js').then(m => console.log(JSON.stringify(m.POSTS.map(p => ({slug: p.slug, title: p.title})))))"
], cwd="/Volumes/Samsung SSD 2TB/03. Documents/Imprtant Repos/procrm-app")
procrm_posts = json.loads(procrm_json)
procrm = {p["slug"]: p["title"] for p in procrm_posts}

brands = {
    "Finnova (finnova.org.au)": finnova,
    "EZ Mortgage Broker (ezmortgagebroker.com.au)": ezmortgage,
    "EZ Consultants (ezconsultants.com.au)": ezconsultants,
    "PRO CRM (procrm.com.au)": procrm
}

total_instances = 0
all_slugs = {}
for brand, posts in brands.items():
    total_instances += len(posts)
    for slug, title in posts.items():
        if slug not in all_slugs:
            all_slugs[slug] = {"title": title, "brands": []}
        all_slugs[slug]["brands"].append(brand)

print("=== ACTIVE ARTICLE COUNTS BY SITE ===")
for brand, posts in brands.items():
    print(f"• {brand}: {len(posts)} articles")

print(f"\nTotal Published Article Instances Across All Sites: {total_instances}")
print(f"Total Unique Articles Across Ecosystem: {len(all_slugs)}")

shared = {s: d for s, d in all_slugs.items() if len(d["brands"]) > 1}
print(f"\nArticles Syndicated Across Multiple Sites: {len(shared)}")
for s, d in shared.items():
    b_str = ", ".join(d["brands"])
    t = d["title"]
    print(f"  - [{s}]: {t[:60]}... -> ({b_str})")

exclusive = {b: sum(1 for d in all_slugs.values() if d["brands"] == [b]) for b in brands}
print("\nExclusive Articles Unique to a Single Site:")
for b, count in exclusive.items():
    print(f"  - {b}: {count}")
