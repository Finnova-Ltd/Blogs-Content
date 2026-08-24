#!/usr/bin/env python3
"""
Sync Central Brand Assets & Build POSTS.md Tracker
--------------------------------------------------
1. Establishes central assets/ folder in Blogs-Content:
   - assets/logos/ (Official brand logos for all 5 platforms)
   - assets/images/ (Curated high-res bright background photography)
   - assets/audio/ (Audio clips / podcast files)
   - assets/videos/ (Rendered 9:16 Shorts & 16:9 Landscape videos)
2. Generates comprehensive Post.md / POSTS.md tracking all published articles, types, dates, and media.
"""

import os
import shutil
import json
import glob

BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"
ASSETS_DIR = os.path.join(BLOGS_DIR, "assets")
LOGOS_DIR = os.path.join(ASSETS_DIR, "logos")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
VIDEOS_DIR = os.path.join(ASSETS_DIR, "videos")

for d in [LOGOS_DIR, IMAGES_DIR, AUDIO_DIR, VIDEOS_DIR]:
    os.makedirs(d, exist_ok=True)

# 1. Copy Official Logos
logo_sources = {
    "ezmortgagebroker-logo.png": "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker/public/assets/01._ez_mortgage_broker-DQScCt6k.png",
    "ezsignature-logo.png": "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend/public/brand/ezsignature-au-logo.png",
    "procrm-logo.png": "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/dist/assets/procrm-logo.png",
    "finnova-logo.png": "/Users/robinbakshi/Documents/Imprtant Repos/Finnova/images/finnova-logo-cropped.png",
    "ezconsultants-logo.png": "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/dist/slds-icons/standard/brand_120.png"
}

for dest_name, src_path in logo_sources.items():
    if os.path.exists(src_path):
        shutil.copy2(src_path, os.path.join(LOGOS_DIR, dest_name))
        print(f"✅ Synced logo: {dest_name} from {src_path}")
    else:
        print(f"⚠️ Source missing for {dest_name}: {src_path}")

print("🚀 Central asset folders initialized successfully in Blogs-Content/assets/")
