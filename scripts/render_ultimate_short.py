#!/usr/bin/env python3
"""
Ultimate YouTube Shorts & Reels Generator
-----------------------------------------
Features:
1. Transparent Brand Logo in Top-Right corner.
2. Google 5.0 Star Reviews Row Badge (★ 5.0 Star Google Reviews).
3. TRUE WORD-BY-WORD TYPING ANIMATION (Netflix/TikTok style progressive typing).
4. Relocated Headline (moved down by ~200px for balanced composition).
5. Contact Badge (📞 Call 1300 050 099 - Contact Us Today) positioned prominently above headline with flashing orange animation.
6. Animated Pulsating Blue CTA Button (Visit ezmortgagebroker.com.au).
7. Loud 44.1kHz Stereo Broadcast Voiceover with +10dB gain & faststart MP4.
"""

import os
import sys
import json
import asyncio
import subprocess
import urllib.request
from PIL import Image
import imageio_ffmpeg
import edge_tts

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"
ASSETS_DIR = os.path.join(BLOGS_DIR, "assets")
VIDEOS_DIR = os.path.join(ASSETS_DIR, "videos")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
CACHE_DIR = os.path.join(BLOGS_DIR, "scripts/asset_cache")

for d in [VIDEOS_DIR, AUDIO_DIR, CACHE_DIR]:
    os.makedirs(d, exist_ok=True)

BRAND_CONFIG = {
    "ezmortgage": {
        "name": "EZ Mortgage Broker",
        "phone": "1300 050 099",
        "cta_domain": "ezmortgagebroker.com.au",
        "logo_raw": os.path.join(ASSETS_DIR, "logos/ezmortgagebroker-logo.webp"),
        "logo_transparent": os.path.join(ASSETS_DIR, "logos/ezmortgagebroker-transparent.png"),
        "rating": "5.0 Star Google Reviews (Verified)"
    },
    "ezsignature": {
        "name": "EZ Signature",
        "phone": "1300 050 099",
        "cta_domain": "ezsignature.com",
        "logo_raw": os.path.join(ASSETS_DIR, "logos/ezsignature-logo.png"),
        "logo_transparent": os.path.join(ASSETS_DIR, "logos/ezsignature-logo.png"),
        "rating": "5.0 Star Enterprise Reviews"
    },
    "procrm": {
        "name": "PRO CRM",
        "phone": "1300 050 099",
        "cta_domain": "procrm.com.au",
        "logo_raw": os.path.join(ASSETS_DIR, "logos/procrm-logo.png"),
        "logo_transparent": os.path.join(ASSETS_DIR, "logos/procrm-logo.png"),
        "rating": "5.0 Star ISO 27001 Reviews"
    },
    "ezconsultants": {
        "name": "EZ Consultants",
        "phone": "1300 050 099",
        "cta_domain": "ezconsultants.com.au",
        "logo_raw": os.path.join(ASSETS_DIR, "logos/ezconsultants-logo.png"),
        "logo_transparent": os.path.join(ASSETS_DIR, "logos/ezconsultants-logo.png"),
        "rating": "5.0 Star Google Reviews (Verified)"
    },
    "finnova": {
        "name": "Finnova Hub",
        "phone": "1300 050 099",
        "cta_domain": "finnova.org.au",
        "logo_raw": os.path.join(ASSETS_DIR, "logos/finnova-logo.webp"),
        "logo_transparent": os.path.join(ASSETS_DIR, "logos/finnova-logo.webp"),
        "rating": "5.0 Star Community Reviews"
    }
}

BRIGHT_PEXELS_IMAGES = [
    "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=1200"
]

def make_transparent_logo(input_path, output_path):
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        return output_path
    if not os.path.exists(input_path):
        return input_path
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] > 235 and item[1] > 235 and item[2] > 235:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(output_path, "PNG")
    return output_path

def download_image(url, filename):
    dest = os.path.join(CACHE_DIR, filename)
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        return dest
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        return dest
    except Exception:
        return None

def generate_true_typing_subtitles(sentences, seg_duration, ass_path):
    """
    Creates real word-by-word progressive typing animation (Netflix / TikTok style).
    Each word appears sequentially as spoken!
    """
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,58,&H00FFFFFF,&H000000FF,&H00000000,&HB0000000,-1,0,0,0,100,100,0,0,3,10,2,5,80,80,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    
    for i, s in enumerate(sentences):
        sentence_start = i * seg_duration
        sentence_end = (i + 1) * seg_duration
        words = s.strip().split()
        num_words = len(words)
        if num_words == 0:
            continue
            
        time_per_word = (sentence_end - sentence_start) / num_words
        
        # Output an event for every single progressive word typed!
        for w_idx in range(1, num_words + 1):
            t_sub_start = sentence_start + (w_idx - 1) * time_per_word
            t_sub_end = sentence_start + w_idx * time_per_word if w_idx < num_words else sentence_end
            
            current_words = words[:w_idx]
            
            # Format max 2 lines for clean Netflix readability
            lines = []
            cur = []
            for w in current_words:
                cur.append(w)
                if len(cur) >= 4:
                    lines.append(" ".join(cur))
                    cur = []
            if cur:
                lines.append(" ".join(cur))
            wrapped = "\\N".join(lines)
            
            start_str = f"0:{int(t_sub_start//60):02d}:{int(t_sub_start%60):02d}.{int((t_sub_start%1)*100):02d}"
            end_str = f"0:{int(t_sub_end//60):02d}:{int(t_sub_end%60):02d}.{int((t_sub_end%1)*100):02d}"
            events.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{wrapped}")
            
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
    return ass_path

def render_ultimate_video(
    title,
    sentences,
    brand_key="ezmortgage",
    output_filename=None
):
    cfg = BRAND_CONFIG.get(brand_key, BRAND_CONFIG["ezmortgage"])
    slug = "".join(c if c.isalnum() else "-" for c in title.lower())[:32].strip("-")
    
    if not output_filename:
        output_filename = f"{brand_key}_{slug}.mp4"
        
    output_mp4 = os.path.join(VIDEOS_DIR, output_filename)
    output_audio = os.path.join(AUDIO_DIR, f"{brand_key}_{slug}.mp3")
    temp_wav = os.path.join(CACHE_DIR, f"{slug}_loud.wav")
    rel_ass = "temp_typing.ass"
    
    print(f"\n=======================================================")
    print(f"🎬 Rendering Ultimate Short with True Typing Animation for: {cfg['name']}")
    print(f"📄 Title: {title}")
    print(f"=======================================================")
    
    # 1. Synthesize Voiceover
    print("🎙️ 1. Synthesizing broadcast Australian voiceover...")
    full_text = " ".join(sentences)
    asyncio.run(edge_tts.Communicate(full_text, "en-AU-WilliamNeural").save(output_audio))
    
    # Convert to 44.1kHz Stereo with volume gain
    subprocess.run([
        ffmpeg_exe, "-y", "-i", output_audio,
        "-ar", "44100", "-ac", "2", "-af", "volume=3.5",
        temp_wav
    ], check=True)
    
    # 2. Audio Duration
    probe_cmd = [ffmpeg_exe, "-i", temp_wav]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    duration = 15.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            try:
                dur_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = dur_str.split(":")
                duration = int(h) * 3600 + int(m) * 60 + float(s)
                break
            except Exception:
                pass
    print(f"⏱️ Spoken Duration: {duration:.2f}s")
    
    # 3. TRUE Word-by-Word Typing Subtitles
    seg_dur = duration / max(len(sentences), 1)
    generate_true_typing_subtitles(sentences, seg_dur, rel_ass)
    
    # 4. Transparent Logo in Top-Right
    logo_trans = make_transparent_logo(cfg["logo_raw"], cfg["logo_transparent"])
    
    # 5. Bright Images
    img1 = download_image(BRIGHT_PEXELS_IMAGES[0], "bright_home_1.jpg")
    img2 = download_image(BRIGHT_PEXELS_IMAGES[1], "bright_home_2.jpg")
    img3 = download_image(BRIGHT_PEXELS_IMAGES[2], "bright_office.jpg")
    
    font_file = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    if not os.path.exists(font_file):
        font_file = "/System/Library/Fonts/Helvetica.ttc"
        
    # Clean and wrap title gracefully on word boundaries without cutting words
    clean_title = title.replace("'", "").replace(":", " -").strip()
    words = clean_title.split()
    lines = []
    cur = []
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) > 26:
            lines.append(" ".join(cur))
            cur = []
    if cur:
        lines.append(" ".join(cur))
    title_text = "\\\n".join(lines[:2])
    
    domain = cfg["cta_domain"]
    phone = cfg["phone"]
    reviews_badge = "5.0 Star Google Reviews (Verified)"
    
    # 6. Layout Coordinates:
    # - Top-Left: Google 5-Star Review Badge (y=80)
    # - Top-Right: Transparent Brand Logo (y=60)
    # - Above-Headline: Flashing Light Orange Contact Badge (y=320)
    # - Main Headline: Lowered with full intact words (y=440)
    # - Center: Real Word-by-Word Progressive Typing Animated Subtitles
    # - Bottom Animated Button: Pulsating Scale & Glow for Visit Domain (y=1660)
    t_scene = duration / 3.0
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v0];"
        f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v1];"
        f"[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v2];"
        f"[v0][v1][v2]concat=n=3:v=1:a=0[bg_all];"
        f"[bg_all]drawbox=y=0:color=white@0.05:width=iw:height=ih:t=fill,"
        f"drawbox=y=0:color=black@0.08:width=iw:height=ih:t=fill,"
        f"drawtext=fontfile='{font_file}':text='{reviews_badge}':fontcolor=0xffd700:fontsize=32:x=60:y=80:box=1:boxcolor=0x0f172a@0.92:boxborderw=14,"
        f"drawtext=fontfile='{font_file}':text='Call {phone}  -  Contact Us Today':fontcolor=0x000000:fontsize=38:x=(w-text_w)/2:y=320:box=1:boxcolor=0xfb923c@0.95:boxborderw=18:enable='lt(mod(t\\,0.8)\\,0.65)',"
        f"drawtext=fontfile='{font_file}':text='{clean_title}':fontcolor=0xffffff:fontsize=42:x=(w-text_w)/2:y=440:box=1:boxcolor=0x1e293b@0.92:boxborderw=18[with_header];"
        f"[3:v]scale=220:-1[logo_scaled];"
        f"[with_header][logo_scaled]overlay=W-w-60:60[with_logo];"
        f"[with_logo]subtitles={rel_ass},"
        f"drawtext=fontfile='{font_file}':text='👉 Visit {domain}':fontcolor=0xffffff:fontsize=42:x=(w-text_w)/2:y=1660:box=1:boxcolor=0x2563eb@0.95:boxborderw=24:enable='lt(mod(t\\,1.2)\\,0.95)'[outv]"
    )
    
    print("🎬 2. Compositing ultimate 1080x1920 Short with true typing animation...")
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-t", f"{t_scene}", "-i", img1,
        "-loop", "1", "-t", f"{t_scene}", "-i", img2,
        "-loop", "1", "-t", f"{t_scene+1}", "-i", img3,
        "-i", logo_trans,
        "-i", temp_wav,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "4:a",
        "-c:v", "libx264", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "256k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p", "-shortest",
        output_mp4
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(rel_ass):
        os.remove(rel_ass)
        
    desktop_copy = "/Users/robinbakshi/Desktop/Latest_YouTube_Short.mp4"
    import shutil
    shutil.copy2(output_mp4, desktop_copy)
    shutil.copy2(temp_wav, "/Users/robinbakshi/Desktop/Latest_Voice_Audio.wav")
    print(f"🖥️ Video copied directly to your Desktop: {desktop_copy}")
    print(f"🎧 Audio WAV copied directly to your Desktop: /Users/robinbakshi/Desktop/Latest_Voice_Audio.wav")
    
    size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"✅ Ultimate Video Rendered: {output_mp4} ({size_mb:.2f} MB)")
    return output_mp4

if __name__ == "__main__":
    render_ultimate_video(
        title="RBA Cash Rate Outlook & Refinancing 2026",
        sentences=[
            "Did you know the latest Reserve Bank rate announcement could save you thousands on your mortgage?",
            "Major Australian lenders are adjusting fixed and variable refinancing tiers right now.",
            "Contact our accredited broker team today to lock in your lowest monthly repayment."
        ],
        brand_key="ezmortgage"
    )
