#!/usr/bin/env python3
import os
import sys
import shutil

BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"
PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"

sys.path.insert(0, os.path.join(BLOGS_DIR, "scripts"))
from render_ultimate_short import render_ultimate_video

print("🎬 Rendering dedicated PRO CRM YouTube Short...")
output_mp4 = render_ultimate_video(
    title="Agentforce Multi-Agent AI Governance",
    sentences=[
        "Are you deploying autonomous AI agents across your enterprise workflows?",
        "Australian CIOs are enforcing zero-data-retention and APRA CPS 234 compliance guardrails.",
        "Partner with PRO CRM Australia to implement governed Agentforce architectures today."
    ],
    brand_key="procrm"
)

# Also copy to procrm-app public assets folder
procrm_videos_dir = os.path.join(PROCRM_DIR, "public", "assets", "videos")
os.makedirs(procrm_videos_dir, exist_ok=True)
dest_path = os.path.join(procrm_videos_dir, "procrm_agentforce_governance.mp4")
shutil.copy2(output_mp4, dest_path)

# Also copy standard name in Blogs-Content
blogs_std_path = os.path.join(BLOGS_DIR, "assets", "videos", "procrm_agentforce_governance.mp4")
shutil.copy2(output_mp4, blogs_std_path)

print(f"✅ Copied to PRO CRM public assets: {dest_path}")
print(f"✅ Copied to Blogs-Content assets: {blogs_std_path}")

# Git commit and push both
os.system(f'cd "{BLOGS_DIR}" && git add assets/videos/ && git commit -m "Add PRO CRM Agentforce Short MP4" && git push origin main')
os.system(f'cd "{PROCRM_DIR}" && git add public/assets/videos/ && git commit -m "Add PRO CRM Agentforce Short MP4" && git push origin main')
print("🚀 Both GitHub repositories updated and pushed!")
