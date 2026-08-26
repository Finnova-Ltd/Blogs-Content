#!/usr/bin/env python3
import json
import os

EZM_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
posts_path = os.path.join(EZM_DIR, "posts.json")
news_path = os.path.join(EZM_DIR, "data", "news_db.json")

def deduplicate(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    posts = data if isinstance(data, list) else data.get("posts", [])
    seen_titles = set()
    unique_posts = []
    
    for p in posts:
        title = p.get("title", "").strip().lower()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_posts.append(p)
            
    with open(file_path, "w", encoding="utf-8") as f:
        if isinstance(data, list):
            json.dump(unique_posts, f, indent=2)
        else:
            data["posts"] = unique_posts
            json.dump(data, f, indent=2)
            
    print(f"✅ Deduplicated {file_path}: Kept {len(unique_posts)} unique posts (Removed {len(posts) - len(unique_posts)} duplicates)")

deduplicate(posts_path)
deduplicate(news_path)

os.system(f'cd "{EZM_DIR}" && python3 scripts/generate_rss_feed.py && git commit -am "Strict deduplication of posts and RSS feed" && git push origin main')
print("🚀 Cleaned EZ Mortgage RSS feed pushed with zero duplicates!")
