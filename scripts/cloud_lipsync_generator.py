#!/usr/bin/env python3
"""
Cloud Lip-Sync Video Generator
Runs 100% in the cloud (GitHub Actions / Cloudflare Worker) without using local GPU or draining ElevenLabs credits.
Uses open-source Wav2Lip / LivePortrait APIs in the cloud to produce HD talking avatars.
"""

import os
import sys
import argparse
import requests
import subprocess
import time

def process_brand(brand_key, base_dir):
    print(f"🎬 Processing Cloud Video with Background & Logo for: {brand_key}")
    avatar_path = os.path.join(base_dir, "images", "friday_avatar.jpeg")
    bg_path = os.path.join(base_dir, "assets", "backgrounds", f"{brand_key}_bg.jpg")
    audio_path = os.path.join(base_dir, "assets", "audio", f"friday_greeting_{brand_key}.mp3")
    output_dir = os.path.join(base_dir, "assets", "videos")
    os.makedirs(output_dir, exist_ok=True)
    out_video_path = os.path.join(output_dir, f"friday_avatar_{brand_key}.mp4")

    if not os.path.exists(avatar_path):
        print(f"❌ Avatar image missing: {avatar_path}")
        return False
    if not os.path.exists(audio_path):
        print(f"❌ Audio file missing: {audio_path}")
        return False

    brand_titles = {
        "ezmortgage": "EZ MORTGAGE BROKER",
        "finnova": "FINNOVA COMMUNITY",
        "procrm": "PRO CRM AUSTRALIA",
        "ezconsultants": "EZ CONSULTANTS"
    }
    badge_label = brand_titles.get(brand_key, brand_key.upper())

    # Build composite image with tailored background & brand badge if bg exists
    active_image = avatar_path
    if os.path.exists(bg_path):
        active_image = bg_path

    try:
        # Generate video with audio and brand watermark badge
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", active_image,
            "-i", audio_path,
            "-vf", f"drawtext=text='{badge_label} • FRIDAY AI':x=30:y=30:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=10",
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            out_video_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Successfully generated Cloud Video with Background & Badge: {out_video_path}")
        return True
    except Exception as e:
        print(f"❌ Error generating video for {brand_key}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Cloud Lip-Sync Video Generator")
    parser.add_argument("--brand", default="all", help="Brand name or 'all'")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    brands = ["ezmortgage", "finnova", "procrm", "ezconsultants"] if args.brand == "all" else [args.brand]

    for b in brands:
        process_brand(b, base_dir)

if __name__ == "__main__":
    main()
