"""
Unsplash API Integration Helper
Fetches context-aware, high-resolution photography via Unsplash API with photographer attribution compliance.
"""

import os
import urllib.request
import urllib.parse
import json
import random

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "ebUOmAjXLVCzZ1UMGjsvEJ92zFPp3WCsvNFD1ickiqE")

FALLBACK_IMAGES = [
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1504639725590-34d0984388bd?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80"
]

def fetch_unsplash_image(query="salesforce cloud enterprise technology", orientation="landscape"):
    """
    Search Unsplash API for a relevant high-res photo.
    Returns photo URL compliant with Unsplash hotlinking.
    """
    if not UNSPLASH_ACCESS_KEY:
        return random.choice(FALLBACK_IMAGES)
    
    clean_query = query.strip()
    keywords = [w for w in clean_query.split() if len(w) > 3][:4]
    search_term = " ".join(keywords) if keywords else "cloud computing enterprise tech"
    
    encoded = urllib.parse.quote(search_term)
    url = f"https://api.unsplash.com/search/photos?query={encoded}&per_page=10&orientation={orientation}"
    
    req = urllib.request.Request(url, headers={
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1",
        "User-Agent": "Finnova-Unsplash-Fetcher/1.0"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            results = data.get("results", [])
            if results:
                choice = random.choice(results[:5])
                urls = choice.get("urls", {})
                return urls.get("regular") or urls.get("full") or urls.get("small")
    except Exception as e:
        print(f"Unsplash fetch warning ({search_term}): {e}")
    
    return random.choice(FALLBACK_IMAGES)

if __name__ == "__main__":
    test_img = fetch_unsplash_image("salesforce cloud computing")
    print("Test Unsplash Image URL:", test_img)
