#!/usr/bin/env python3
"""
Adobe Firefly Services & Adobe Express Video Generation Client
FINNOVA / EZMORTGAGE BROKERAGE • ADOBE ECOSYSTEM INTEGRATION

Leverages Adobe Firefly & Express Premium Plan (275+ Generative Credits/month)
for programmatic B-roll video and asset generation:
1. Text-to-Video generation using Firefly Video & Google Veo 3.1 models.
2. Text-to-Image high-resolution financial and property visuals.
3. Automatically downloads generated assets into assets/videos/broll/ for
   instant stitching into the broadcast news pipeline.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.adobe_auth_client import get_adobe_headers, ADOBE_CLIENT_ID, ADOBE_ORG_ID

AEST = ZoneInfo("Australia/Melbourne")
BROLL_DIR = ROOT_DIR / "assets" / "videos" / "broll"
IMAGES_DIR = ROOT_DIR / "assets" / "images"

for d in [BROLL_DIR, IMAGES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def get_current_aest_timestamp():
    return datetime.now(timezone.utc).astimezone(AEST).isoformat()

class AdobeFireflyClient:
    """
    Interfaces with Adobe Firefly Services APIs using OAuth Server-to-Server
    credentials from the active Adobe Developer Console project.
    """

    FIREFLY_BASE = "https://firefly-api.adobe.io"

    def __init__(self):
        self.headers = get_adobe_headers()

    def generate_image(self, prompt, aspect_ratio="16:9", num_variations=1):
        """
        Generates photorealistic property and finance visuals using Firefly Image Model.
        """
        url = f"{self.FIREFLY_BASE}/v2/images/generate"
        payload = {
            "prompt": prompt,
            "n": num_variations,
            "size": {"width": 1920, "height": 1080} if aspect_ratio == "16:9" else {"width": 1080, "height": 1920},
            "contentClass": "photo"
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=self.headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                print(f"[{get_current_aest_timestamp()}] Firefly Image generated successfully: {result}")
                return result
        except urllib.error.HTTPError as err:
            err_body = err.read().decode("utf-8")
            print(f"[{get_current_aest_timestamp()}] Firefly Image API HTTP {err.code}: {err_body}")
            return {"error": err.code, "message": err_body}
        except Exception as e:
            print(f"[{get_current_aest_timestamp()}] Firefly Image Error: {e}")
            return {"error": str(e)}

    def generate_video(self, prompt, aspect_ratio="9:16", model="veo_3.1"):
        """
        Submits an asynchronous video generation job to Adobe Firefly / Express Video Services.
        """
        url = f"{self.FIREFLY_BASE}/v3/video/generate"
        payload = {
            "prompt": prompt,
            "aspectRatio": aspect_ratio,
            "model": model,
            "duration": 5.0
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=self.headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                print(f"[{get_current_aest_timestamp()}] Firefly Video Job Dispatched: {result}")
                return result
        except urllib.error.HTTPError as err:
            err_body = err.read().decode("utf-8")
            print(f"[{get_current_aest_timestamp()}] Firefly Video API HTTP {err.code}: {err_body}")
            return {"error": err.code, "message": err_body}
        except Exception as e:
            print(f"[{get_current_aest_timestamp()}] Firefly Video Error: {e}")
            return {"error": str(e)}

    def check_job_status(self, job_url):
        """Polls async status of a video rendering job."""
        req = urllib.request.Request(job_url, headers=self.headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}

    def download_asset(self, asset_url, destination_filename):
        """Downloads rendered video/image directly into local assets repository."""
        target_path = BROLL_DIR / destination_filename
        urllib.request.urlretrieve(asset_url, str(target_path))
        print(f"[{get_current_aest_timestamp()}] Saved Firefly Asset to: {target_path}")
        return target_path


if __name__ == "__main__":
    print("=== Adobe Firefly Services API Client Initializing ===")
    client = AdobeFireflyClient()
    print(f"Client ID: {ADOBE_CLIENT_ID[:8]}...")
    print(f"Org ID: {ADOBE_ORG_ID}")

    test_prompt = "Cinematic 4K drone shot over Melbourne Yarra river and skyscrapers at sunset"
    print(f"\nTesting Firefly API connection with prompt: '{test_prompt}'")
    res = client.generate_image(test_prompt)
    print("Result:", res)
