#!/usr/bin/env python3
import os
import re
import subprocess
import json

EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
SCRIPTS_DIR = os.path.join(EZ_DIR, "scripts")
FETCH_SCRIPT = os.path.join(SCRIPTS_DIR, "fetch_google_alerts.py")

print("Checking ezmortgagebroker fetch_google_alerts.py...")
with open(FETCH_SCRIPT, "r", encoding="utf-8") as f:
    code = f.read()

# Add the new Google Alert feed URL if not present
new_feed_code = """    {
        "category": "Home Loans",
        "badge": "MORTGAGE MARKET ALERT",
        "url": "https://www.google.com/alerts/feeds/14625353401416373956/18413967573759855438",
        "feed_type": "google_alerts"
    },"""

if "18413967573759855438" not in code:
    code = code.replace("TARGET_FEEDS = [\n", "TARGET_FEEDS = [\n" + new_feed_code + "\n")
    with open(FETCH_SCRIPT, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Added Google Alert 18413967573759855438 to TARGET_FEEDS")
else:
    print("ℹ️ Feed already in TARGET_FEEDS")

# Also ensure fetch_google_alerts.py automatically triggers syndicate_to_make.py when new posts are published
syndicate_hook = """
        # Auto-syndicate newly published posts to Make.com flow
        if new_posts_to_add:
            try:
                from syndicate_to_make import syndicate_article
                print(f"\\n🚀 Auto-Syndicating {len(new_posts_to_add)} new articles to Make.com flow...")
                for np in new_posts_to_add:
                    syndicate_article(np)
            except Exception as se:
                print(f"⚠️ Make syndication hook notice: {se}")
"""

if "Auto-Syndicating" not in code:
    code = code.replace("print(f\"\\n🎉 Published {published_count}", syndicate_hook + "\n        print(f\"\\n🎉 Published {published_count}")
    with open(FETCH_SCRIPT, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Integrated Make flow syndication directly into publishing pipeline")

# Run fetch_google_alerts.py --publish
print("Running fetch_google_alerts.py --publish...")
res = subprocess.run(["python3", "fetch_google_alerts.py", "--publish"], cwd=SCRIPTS_DIR, capture_output=True, text=True)
print("Publisher stdout:\n", res.stdout)
if res.stderr:
    print("Publisher stderr:\n", res.stderr)

# Run RSS generator
print("Generating RSS and Sitemap...")
subprocess.run(["python3", "generate_rss_feed.py"], cwd=SCRIPTS_DIR, capture_output=True)

# Run syndicate_to_make.py directly on latest post
print("Running syndicate_to_make.py...")
res_make = subprocess.run(["python3", "syndicate_to_make.py"], cwd=SCRIPTS_DIR, capture_output=True, text=True)
print("Make flow stdout:\n", res_make.stdout)
if res_make.stderr:
    print("Make flow stderr:\n", res_make.stderr)

# Build site
print("Building ezmortgagebroker...")
res_build = subprocess.run(["npm", "run", "build"], cwd=EZ_DIR, capture_output=True, text=True)
print("Build stdout:\n", res_build.stdout)
if res_build.returncode != 0:
    print("Build stderr:\n", res_build.stderr)
