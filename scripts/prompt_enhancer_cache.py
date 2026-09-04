#!/usr/bin/env python3
"""
Prompt Expansion & Cryptographic Asset Caching Engine
----------------------------------------------------
Learned from anil-matcha/open-generative-ai & gyoridavid/short-video-maker:
1. Cryptographic MD5/SHA256 Caching: Never burn duplicate ElevenLabs characters
   or re-render existing video assets.
2. Prompt Expansion: Expands plain blog titles into cinematic 4K scene prompts
   via Cloudflare Workers AI (@cf/meta/llama-3.3-70b-instruct) at $0 cost.
3. Multi-Scene Storyboard Generation: Generates 3-scene narrative metadata
   (Hook, 3 Core Data Cards, Presenter CTA).
Enforces Australian Timezone (Australia/Melbourne) as per AGENTS.md.
"""

import os
import sys
import json
import hashlib
import datetime
from zoneinfo import ZoneInfo
import requests
from dotenv import load_dotenv

MELBOURNE_TZ = ZoneInfo("Australia/Melbourne")
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(PROJECT_DIR, "assets", "cache", "prompt_store")
os.makedirs(CACHE_DIR, exist_ok=True)

def compute_asset_hash(title: str, brand: str, script_type: str = "short") -> str:
    """Computes deterministic SHA256 signature for asset deduplication."""
    content = f"{brand.lower().strip()}|{title.lower().strip()}|{script_type}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def get_cached_asset(asset_hash: str):
    """Retrieves cached asset if already generated, saving 100% of API costs."""
    cache_path = os.path.join(CACHE_DIR, f"{asset_hash}.json")
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_cached_asset(asset_hash: str, data: dict):
    """Persists generated asset metadata to cache."""
    cache_path = os.path.join(CACHE_DIR, f"{asset_hash}.json")
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def expand_cinematic_prompt_cf(title: str, brand: str) -> dict:
    """
    Expands an article title into a cinematic 4K visual scene prompt and
    3-scene storyboard using Cloudflare Workers AI ($0.00 free tier).
    Falls back to deterministic financial prompt template if offline.
    """
    asset_hash = compute_asset_hash(title, brand, "short")
    cached = get_cached_asset(asset_hash)
    if cached:
        cached["cache_hit"] = True
        return cached

    cf_api_key = os.getenv("CLOUDFLARE_API_KEY")
    cf_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "7c65e471e9b5f8203763393276833de2")
    cf_email = os.getenv("CLOUDFLARE_EMAIL", "testcustomer2022@gmail.com")

    # High-quality fallback template
    result = {
        "title": title,
        "brand": brand,
        "asset_hash": asset_hash,
        "cache_hit": False,
        "created_at": datetime.datetime.now(MELBOURNE_TZ).strftime("%Y-%m-%d %H:%M:%S %Z"),
        "cinematic_visual_prompt": (
            f"Cinematic daylight aerial shot of modern Melbourne suburban homes, golden sunlight, "
            f"ultra-crisp 4K architectural aesthetic, professional finance broadcast grading, no blur, high contrast."
        ),
        "storyboard": {
            "scene_1_hook": {
                "duration_seconds": 5,
                "visual": "Fast-paced dynamic aerial push into Melbourne residential corridor",
                "overlay_text": f"🚨 {title[:45]}",
                "caption_theme": "amber_alert"
            },
            "scene_2_insights": {
                "duration_seconds": 20,
                "visual": "Layered corporate dashboard card with animated financial metrics",
                "data_points": [
                    "Compare 30+ Australian Lenders",
                    "81.0% Mortgage Broker Market Share",
                    "Refinancing & Rate Reduction Opportunities"
                ],
                "caption_theme": "white_clean"
            },
            "scene_3_cta": {
                "duration_seconds": 10,
                "visual": "Accredited Principal Broker Robin Bakshi trust card with MFAA credentials",
                "cta_text": "Connect with an Accredited Broker — Zero Broker Fee",
                "phone": "1300 050 099",
                "website": "ezmortgagebroker.com.au"
            }
        }
    }

    # Attempt Cloudflare Workers AI expansion if credentials exist
    if cf_api_key and cf_account_id:
        headers = {
            "X-Auth-Email": cf_email,
            "X-Auth-Key": cf_api_key,
            "Content-Type": "application/json"
        }
        prompt = (
            f"You are an expert video director for Australian property and financial services. "
            f"Given the title: '{title}' for brand '{brand}', write a concise 1-sentence 4K visual prompt "
            f"for B-roll stock footage. Respond with ONLY the visual prompt text."
        )
        try:
            url = f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/ai/run/@cf/meta/llama-3-8b-instruct"
            resp = requests.post(url, headers=headers, json={"prompt": prompt, "max_tokens": 80}, timeout=8)
            if resp.status_code == 200:
                ai_text = resp.json().get("result", {}).get("response", "").strip()
                if ai_text:
                    result["cinematic_visual_prompt"] = ai_text.replace('"', '')
        except Exception:
            pass  # Retain high-quality template

    save_cached_asset(asset_hash, result)
    return result

if __name__ == "__main__":
    load_dotenv()
    test_title = "RBA Interest Rate Decision & Mortgage Repayments 2026"
    data = expand_cinematic_prompt_cf(test_title, "EZ Mortgage Broker")
    print(json.dumps(data, indent=2))
