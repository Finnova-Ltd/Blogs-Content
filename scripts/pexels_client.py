"""
Pexels API Integration Helper
Fetches context-aware, high-resolution, royalty-free enterprise photography for articles, banners, and blog posts.
"""

import os
import urllib.request
import urllib.parse
import json
import random

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "tyRzLEE5qX30IYR57baFHF6YxjNiVOoUftDC996z85bZ1089oK6LNE6k")

FALLBACK_IMAGES = [
    "https://images.pexels.com/photos/1181354/pexels-photo-1181354.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/139387/pexels-photo-139387.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
]

def fetch_pexels_image(query="cloud computing salesforce technology", orientation="landscape"):
    """
    Search Pexels API for a relevant high-res landscape image based on the article query.
    Returns direct CDN image URL.
    """
    if not PEXELS_API_KEY:
        return random.choice(FALLBACK_IMAGES)
    
    clean_query = query.strip()
    # If query is too long, extract first few key phrases
    keywords = [w for w in clean_query.split() if len(w) > 3][:4]
    search_term = " ".join(keywords) if keywords else "cloud computing enterprise tech"
    
    encoded = urllib.parse.quote(search_term)
    url = f"https://api.pexels.com/v1/search?query={encoded}&per_page=10&orientation={orientation}"
    
    req = urllib.request.Request(url, headers={
        "Authorization": PEXELS_API_KEY,
        "User-Agent": "Finnova-Pexels-Fetcher/1.0"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            photos = data.get("photos", [])
            if photos:
                # Pick a random photo among the top results for variety
                choice = random.choice(photos[:5])
                src = choice.get("src", {})
                return src.get("large2x") or src.get("large") or src.get("original")
    except Exception as e:
        print(f"Pexels fetch warning ({search_term}): {e}")
    
    return random.choice(FALLBACK_IMAGES)

if __name__ == "__main__":
    test_img = fetch_pexels_image("cybersecurity data cloud")
    print("Test Image URL:", test_img)
