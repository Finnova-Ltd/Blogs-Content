#!/usr/bin/env python3
"""
Full-Article Landscape Video (16:9) & Audio Podcast Generator
--------------------------------------------------------------
1. Converts full blog post into a 2-4 minute widescreen (1920x1080) YouTube Video.
2. Creates an embedded Audio Clip / Podcast (.mp3) with HTML player snippet for website embedding.
3. Uses bright Pexels stock images and natural Australian neural voiceover ($0 API cost).
"""

import os
import sys
import json
import asyncio
import subprocess
import urllib.request
import imageio_ffmpeg
import edge_tts

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
OUTPUT_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/generated_videos"
CACHE_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/asset_cache"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

BRAND_LOGOS = {
    "ezmortgage": "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker/dist/jm-loans-logo-transparent.png",
    "ezsignature": "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend/public/brand/ezsignature-au-logo.png",
    "procrm": "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/dist/assets/procrm-logo.png",
    "finnova": "/Users/robinbakshi/Documents/Imprtant Repos/Finnova/images/finnova-logo-cropped.png"
}

def generate_article_audio_podcast(article_title, full_article_text, brand_name, output_audio_path):
    """
    Generates a full-length broadcast audio clip / podcast (.mp3)
    plus the embeddable HTML audio player code for the blog.
    """
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
    asyncio.run(edge_tts.Communicate(full_article_text, "en-AU-NatashaNeural").save(output_audio_path))
    
    audio_filename = os.path.basename(output_audio_path)
    embed_html = f"""
<!-- 🎙️ Audio Article Player Embed -->
<div class="audio-article-player" style="background: linear-gradient(135deg, #0f172a, #1e293b); padding: 18px 24px; border-radius: 12px; margin: 24px 0; border: 1px solid #334155; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;">
  <div style="display: flex; align-items: center; gap: 12px;">
    <span style="font-size: 28px;">🎧</span>
    <div>
      <div style="font-weight: 700; color: #f8fafc; font-size: 15px;">Listen to this Article</div>
      <div style="font-size: 12px; color: #94a3b8;">Narrated by {brand_name} Audio Desk</div>
    </div>
  </div>
  <audio controls preload="metadata" style="max-width: 320px; height: 36px;">
    <source src="/assets/audio/{audio_filename}" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
</div>
"""
    return {
        "audio_path": output_audio_path,
        "embed_html": embed_html
    }

def render_full_article_landscape_video(
    article_title,
    sections, # List of {"heading": "...", "text": "...", "image_url": "..."}
    brand_key="ezmortgage",
    website_url="https://ezmortgagebroker.com.au",
    output_mp4=os.path.join(OUTPUT_DIR, "full_article_youtube_16x9.mp4")
):
    """
    Renders a 16:9 widescreen YouTube video (1920x1080) covering the full article.
    """
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    full_narration = " ".join([f"{s['heading']}. {s['text']}" for s in sections])
    temp_audio = output_mp4.replace(".mp4", "_full_audio.mp3")
    
    print("🎙️ Generating full article audio narration...")
    asyncio.run(edge_tts.Communicate(full_narration, "en-AU-NatashaNeural").save(temp_audio))
    
    logo_path = BRAND_LOGOS.get(brand_key, BRAND_LOGOS["ezmortgage"])
    bg_image = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker/public/assets/luxury-home-refinance-hero-OeZc7gD4.webp"
    
    font_file = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    if not os.path.exists(font_file):
        font_file = "/System/Library/Fonts/Helvetica.ttc"
        
    clean_title = article_title.replace("'", "").replace(":", " -")[:55]
    domain = website_url.replace("https://", "").split("/")[0]
    
    # 16:9 Widescreen Filter Complex
    filter_complex = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='min(zoom+0.0003,1.15)':d=900:s=1920x1080:fps=30,"
        f"drawbox=y=0:color=white@0.05:width=iw:height=ih:t=fill,"
        f"drawbox=y=0:color=black@0.3:width=iw:height=ih:t=fill,"
        f"drawtext=fontfile='{font_file}':text='{clean_title}':fontcolor=0xfff000:fontsize=52:x=(w-text_w)/2:y=180:box=1:boxcolor=0x0f172a@0.92:boxborderw=24[with_title];"
        f"[1:v]scale=260:-1[logo_scaled];"
        f"[with_title][logo_scaled]overlay=80:60[with_logo];"
        f"[with_logo]drawtext=fontfile='{font_file}':text='👉 Full guide & calculator at {domain}':fontcolor=0xffffff:fontsize=36:x=(w-text_w)/2:y=960:box=1:boxcolor=0x2563eb@0.95:boxborderw=20[outv]"
    )
    
    print("🎬 Rendering 16:9 Widescreen YouTube Video (1920x1080)...")
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-i", bg_image,
        "-i", logo_path,
        "-i", temp_audio,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-shortest",
        output_mp4
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(temp_audio):
        os.remove(temp_audio)
        
    size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"✅ 16:9 Widescreen Video successfully rendered ({size_mb:.2f} MB) at: {output_mp4}")
    return output_mp4

if __name__ == "__main__":
    # Test Podcast Generator
    podcast = generate_article_audio_podcast(
        "RBA Inflation Data & 2026 Cash Rate Forecast",
        "Welcome to the daily mortgage intelligence desk. Today, the Reserve Bank of Australia released headline inflation data showing annual consumer price growth has moderated. Major lenders are adjusting fixed rate tiers. Borrowers should review their current loan buffer.",
        "EZ Mortgage Broker",
        os.path.join(OUTPUT_DIR, "rba_podcast_clip.mp3")
    )
    print("🎧 Generated Audio Podcast & HTML Embed Code:")
    print(podcast["embed_html"])
