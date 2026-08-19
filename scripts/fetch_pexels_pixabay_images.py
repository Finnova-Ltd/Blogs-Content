#!/usr/bin/env python3
"""
Content Publishing Engine - High-Resolution Image Fetcher
=========================================================
Supports Pexels API, Pixabay API, and Curated Unsplash Fallbacks.
Used for automated hero banner and article body image generation.

Environment Variables:
- PEXELS_API_KEY (optional, from https://www.pexels.com/api/)
- PIXABAY_API_KEY (optional, from https://pixabay.com/api/docs/)
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "images", "assets-ez-mortgage-broker")

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY", "")

CURATED_BACKUPS = {
    "property": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=85",
    "mortgage": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=85",
    "refinancing": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=85",
    "rates": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=85",
    "business": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=85",
    "investing": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=85"
}

def fetch_from_pexels(query, per_page=1):
    if not PEXELS_API_KEY:
        return None
    try:
        url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&orientation=landscape&per_page={per_page}"
        req = urllib.request.Request(url, headers={"Authorization": PEXELS_API_KEY, "User-Agent": "ContentPublishingEngine/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('photos'):
                return data['photos'][0]['src']['large2x']
    except Exception as e:
        print(f"[Pexels API] Error: {e}", file=sys.stderr)
    return None

def fetch_from_pixabay(query, per_page=3):
    if not PIXABAY_API_KEY:
        return None
    try:
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={urllib.parse.quote(query)}&image_type=photo&orientation=horizontal&safesearch=true&per_page={per_page}"
        req = urllib.request.Request(url, headers={"User-Agent": "ContentPublishingEngine/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('hits'):
                return data['hits'][0]['largeImageURL']
    except Exception as e:
        print(f"[Pixabay API] Error: {e}", file=sys.stderr)
    return None

def download_image(image_url, target_path):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    req = urllib.request.Request(image_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        with open(target_path, 'wb') as f:
            f.write(resp.read())
    return target_path

def get_image_for_topic(query_topic, output_filename=None, output_dir=DEFAULT_OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)
    if not output_filename:
        safe_name = urllib.parse.quote_plus(query_topic.lower()[:30])
        output_filename = f"{safe_name}-{int(datetime.now().timestamp())}.jpg"
    
    target_path = os.path.join(output_dir, output_filename)
    
    img_url = fetch_from_pexels(query_topic)
    source = "Pexels API"
    
    if not img_url:
        img_url = fetch_from_pixabay(query_topic)
        source = "Pixabay API"
        
    if not img_url:
        source = "Curated High-Res Fallback"
        img_url = CURATED_BACKUPS.get("property")
        for key in CURATED_BACKUPS:
            if key in query_topic.lower():
                img_url = CURATED_BACKUPS[key]
                break

    print(f"📥 Fetching image from {source}: {query_topic} -> {output_filename}")
    download_image(img_url, target_path)
    return target_path

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Australian real estate modern home"
    fn = sys.argv[2] if len(sys.argv) > 2 else "sample-downloaded-hero.jpg"
    saved = get_image_for_topic(query, fn)
    print(f"✅ Image saved successfully: {saved}")
