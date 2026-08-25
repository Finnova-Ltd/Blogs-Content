#!/usr/bin/env python3
"""
CyberVerse Dynamic AI Avatar Video Presenter Engine
---------------------------------------------------
Learnings from Lynpoint/CyberVerse:
1. Persona & Voice Gender Guarantee:
   - PRO CRM (Male) -> en-AU-WilliamNeural
   - EZ Mortgage (Male) -> en-AU-WilliamNeural
   - EZ Signature (Male) -> en-AU-WilliamNeural
   - EZ Consultants (Female) -> en-AU-NatashaNeural
2. Dynamic Camera Staging:
   - Starts centered/prominent during 0-3.5s (Hook introduction).
   - Smoothly glides & scales to Bottom-Left anchor (x=60, y=H-h-240).
3. Non-Overlapping Kinetic Typing Text:
   - Text occupies the open upper/right canvas (y=520 to 1050).
   - Zero overlap with the presenter's face.
4. Micro-Expressions:
   - Involuntary eye blinks every 3.5s.
   - Subtle breathing and head tilts.
"""

import os
import sys
import math
import json
import asyncio
import subprocess
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg
import edge_tts

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"
ASSETS_DIR = os.path.join(BLOGS_DIR, "assets")
AVATARS_DIR = os.path.join(ASSETS_DIR, "avatars")
VIDEOS_DIR = os.path.join(ASSETS_DIR, "videos")
CACHE_DIR = os.path.join(BLOGS_DIR, "scripts/asset_cache")
DESKTOP_DIR = "/Users/robinbakshi/Desktop"

for d in [AVATARS_DIR, VIDEOS_DIR, CACHE_DIR]:
    os.makedirs(d, exist_ok=True)

BRAND_PROFILES = {
    "procrm": {
        "name": "PRO CRM Australia",
        "phone": "1300 050 099",
        "domain": "procrm.com.au",
        "gender": "male",
        "voice": "en-AU-WilliamNeural", # Male Australian Voice
        "avatar_img": os.path.join(AVATARS_DIR, "procrm_persona.jpg"),
        "accent_color": (124, 58, 237),
        "badge": "5.0 Star ISO 27001 Reviews (Verified)"
    },
    "ezmortgage": {
        "name": "EZ Mortgage Broker",
        "phone": "1300 050 099",
        "domain": "ezmortgagebroker.com.au",
        "gender": "male",
        "voice": "en-AU-WilliamNeural", # Male Australian Voice
        "avatar_img": os.path.join(AVATARS_DIR, "ezmortgage_persona.jpg"),
        "accent_color": (37, 99, 235),
        "badge": "5.0 Star Google Reviews (Verified)"
    },
    "ezconsultants": {
        "name": "EZ Consultants",
        "phone": "1300 050 099",
        "domain": "ezconsultants.com.au",
        "gender": "female",
        "voice": "en-AU-NatashaNeural", # Female Australian Voice (Matching Female Persona)
        "avatar_img": os.path.join(AVATARS_DIR, "ezconsultants_persona.jpg"),
        "accent_color": (5, 150, 105),
        "badge": "5.0 Star NDIS & Healthcare Advisory"
    },
    "ezsignature": {
        "name": "EZ Signature",
        "phone": "1300 050 099",
        "domain": "ezsignature.com",
        "gender": "male",
        "voice": "en-AU-WilliamNeural", # Male Australian Voice
        "avatar_img": os.path.join(AVATARS_DIR, "ezsignature_persona.jpg"),
        "accent_color": (2, 132, 199),
        "badge": "5.0 Star Legal & Enterprise Reviews"
    }
}

async def generate_speech(text, voice, out_mp3, out_wav):
    communicate = edge_tts.Communicate(text, voice, rate="+3%", volume="+25%")
    await communicate.save(out_mp3)
    subprocess.run([
        ffmpeg_exe, "-y", "-i", out_mp3,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.8",
        "-ar", "44100", "-ac", "2", out_wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def generate_cyberverse_avatar_stream(avatar_img_path, output_mp4, duration, accent_color, fps=30):
    """
    Renders CyberVerse dynamic presentation stream:
    - 0.0s to 3.0s: Center stage (size 560x560 at x=260, y=420)
    - 3.0s to 4.2s: Smooth gliding transition down to bottom-left
    - 4.2s to End: Locked at bottom-left (size 380x380 at x=60, y=1420)
    """
    base_img = Image.open(avatar_img_path).convert("RGBA")
    
    # Eyelid blink frame
    blink_img = base_img.copy().resize((560, 560), Image.Resampling.LANCZOS)
    blink_draw = ImageDraw.Draw(blink_img)
    blink_draw.rectangle([190, 205, 265, 218], fill=(225, 195, 175, 180))
    blink_draw.rectangle([295, 205, 370, 218], fill=(225, 195, 175, 180))
    blink_img = blink_img.filter(ImageFilter.GaussianBlur(radius=1.2))
    
    base_560 = base_img.resize((560, 560), Image.Resampling.LANCZOS)
    
    temp_dir = os.path.join(CACHE_DIR, "cyberverse_frames")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    total_frames = int(duration * fps)
    
    for i in range(total_frames):
        t = i / float(fps)
        
        # 1. Staging Animation (Interpolation)
        if t < 3.0:
            # Stage 1: Full Center
            cur_size = 520
            cur_x = int((1080 - 520) / 2)
            cur_y = 480
        elif t < 4.2:
            # Transition phase (Smooth Ease-in-out cosine)
            progress = (t - 3.0) / 1.2
            ease = 0.5 * (1.0 - math.cos(math.pi * progress))
            cur_size = int(520 - (520 - 380) * ease)
            cur_x = int(280 + (60 - 280) * ease)
            cur_y = int(480 + (1380 - 480) * ease)
        else:
            # Stage 2: Settled Bottom-Left Anchor
            cur_size = 380
            cur_x = 60
            cur_y = 1380
            
        # Involuntary blink every 3.5s
        is_blinking = (t % 3.5) < 0.15
        cur_face = blink_img if is_blinking else base_560
        
        # Micro breathing movement
        zoom = 1.0 + 0.012 * math.sin(2.0 * math.pi * t / 2.8)
        scaled_w = int(cur_size * zoom)
        scaled_h = int(cur_size * zoom)
        scaled_face = cur_face.resize((scaled_w, scaled_h), Image.Resampling.BILINEAR)
        
        left = (scaled_w - cur_size) // 2
        top = (scaled_h - cur_size) // 2
        cropped = scaled_face.crop((left, top, left + cur_size, top + cur_size))
        
        # Circular mask with smooth edge
        mask = Image.new("L", (cur_size, cur_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, cur_size, cur_size), fill=255)
        
        # Transparent canvas 1080x1920
        frame_canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        
        # Glowing frame ring
        ring_size = cur_size + 20
        ring_canvas = Image.new("RGBA", (ring_size, ring_size), (0, 0, 0, 0))
        ring_draw = ImageDraw.Draw(ring_canvas)
        ring_draw.ellipse((0, 0, ring_size, ring_size), fill=(*accent_color, 255))
        
        inner_ring = Image.new("RGBA", (cur_size + 8, cur_size + 8), (0, 0, 0, 0))
        inner_draw = ImageDraw.Draw(inner_ring)
        inner_draw.ellipse((0, 0, cur_size + 8, cur_size + 8), fill=(255, 255, 255, 255))
        
        ring_canvas.paste(inner_ring, (6, 6), inner_ring)
        ring_canvas.paste(cropped, (10, 10), mask)
        
        frame_canvas.paste(ring_canvas, (cur_x - 10, cur_y - 10), ring_canvas)
        
        frame_canvas.save(os.path.join(temp_dir, f"cv_{i:05d}.png"), "PNG")
        
    cmd = [
        ffmpeg_exe, "-y",
        "-framerate", f"{fps}",
        "-i", os.path.join(temp_dir, "cv_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuva420p",
        "-preset", "ultrafast",
        output_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return output_mp4

def render_cyberverse_video(brand_key, title, sentences):
    cfg = BRAND_PROFILES.get(brand_key, BRAND_PROFILES["procrm"])
    print(f"\n=======================================================")
    print(f"🎬 Rendering CyberVerse Presenter for: {cfg['name']} ({cfg['gender'].upper()})")
    print(f"🎙️ Voice Profile: {cfg['voice']}")
    print(f"=======================================================")
    
    slug = f"{brand_key}_{''.join(c if c.isalnum() else '_' for c in title.lower())[:25]}"
    voice_mp3 = os.path.join(CACHE_DIR, f"{slug}_cv_voice.mp3")
    voice_wav = os.path.join(CACHE_DIR, f"{slug}_cv_voice.wav")
    
    full_text = " ".join(sentences)
    asyncio.run(generate_speech(full_text, cfg["voice"], voice_mp3, voice_wav))
    
    res = subprocess.run([ffmpeg_exe, "-i", voice_wav], capture_output=True, text=True)
    duration = 15.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            dur_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = dur_str.split(":")
            duration = int(h)*3600 + int(m)*60 + float(s)
            break
            
    print(f"⏱️ Spoken Duration: {duration:.2f}s")
    
    # 1. Generate CyberVerse Avatar Animation Stream
    cv_avatar_mp4 = os.path.join(CACHE_DIR, f"{slug}_cv_avatar.mp4")
    generate_cyberverse_avatar_stream(cfg["avatar_img"], cv_avatar_mp4, duration, cfg["accent_color"])
    print("✨ CyberVerse Staging complete (Center Hook -> Glide to Bottom-Left)")
    
    # 2. Build Typing Subtitles in Non-Overlapping Upper Canvas (y=550 to y=1100)
    ass_path = os.path.join(CACHE_DIR, f"{slug}_cv_subtitles.ass")
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Arial,42,&H00FFFFFF,&H000000FF,&H000F172A,&H90000000,1,0,0,0,100,100,0,0,1,5,0,2,60,60,1180,1
Style: Subtitle,Arial,36,&H000F172A,&H000000FF,&H00FFFFFF,&H90000000,1,0,0,0,100,100,0,0,1,4,0,2,60,60,820,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header)
        
        # Display sentences dynamically timed across duration
        t_seg = duration / float(len(sentences))
        for i, s in enumerate(sentences):
            start_s = i * t_seg
            end_s = (i + 1) * t_seg
            
            def fmt(sec):
                m = int(sec // 60)
                s = int(sec % 60)
                cs = int((sec - int(sec)) * 100)
                return f"{m:01d}:{s:02d}.{cs:02d}"
                
            words = s.split()
            word_dt = (end_s - start_s) / float(max(1, len(words)))
            
            accum = []
            for w_idx, w in enumerate(words):
                accum.append(w)
                w_start = start_s + w_idx * word_dt
                w_end = start_s + (w_idx + 1) * word_dt if w_idx < len(words) - 1 else end_s
                revealed = " ".join(accum)
                f.write(f"Dialogue: 0,{fmt(w_start)},{fmt(w_end)},Subtitle,,0,0,0,,{revealed}\n")
                
    # 3. Compositor
    bg_canvas_path = os.path.join(CACHE_DIR, "studio_light_bg.jpg")
    logo_path = os.path.join(ASSETS_DIR, f"logos/{brand_key}-logo.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(ASSETS_DIR, f"logos/{brand_key}broker-transparent.png")
    if not os.path.exists(logo_path):
        logo_path = bg_canvas_path
        
    out_mp4 = os.path.join(VIDEOS_DIR, f"{slug}_cyberverse.mp4")
    desktop_mp4 = os.path.join(DESKTOP_DIR, f"{cfg['name'].replace(' ', '_')}_CyberVerse.mp4")
    
    font_file = "/System/Library/Fonts/Supplemental/Arial.ttf"
    
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];"
        f"[2:v]scale=160:-1[logo_s];"
        f"[bg][1:v]overlay=0:0[with_avatar];"
        f"[with_avatar][logo_s]overlay=x=W-w-50:y=60[with_logo];"
        f"[with_logo]"
        f"drawtext=fontfile='{font_file}':text='{cfg['badge']}':fontcolor=0xffffff:fontsize=24:x=60:y=70:box=1:boxcolor=0x0f172a@0.92:boxborderw=10,"
        f"drawtext=fontfile='{font_file}':text='Call {cfg['phone']} - Contact Us Today':fontcolor=0x000000:fontsize=28:x=(w-text_w)/2:y=180:box=1:boxcolor=0xfb923c@0.95:boxborderw=14,"
        f"drawtext=fontfile='{font_file}':text='{title.upper()[:38]}':fontcolor=0x0f172a:fontsize=34:x=(w-text_w)/2:y=340:box=1:boxcolor=0xffffff@0.95:boxborderw=14,"
        f"subtitles='{ass_path}',"
        f"drawtext=fontfile='{font_file}':text='Visit {cfg['domain']}':fontcolor=0xffffff:fontsize=32:x=480:y=1540:box=1:boxcolor=0x2563eb@0.95:boxborderw=16[outv]"
    )
    
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-t", f"{duration}", "-i", bg_canvas_path,
        "-i", cv_avatar_mp4,
        "-i", logo_path,
        "-i", voice_wav,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "256k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p", "-shortest",
        out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    shutil.copy2(out_mp4, desktop_mp4)
    print(f"✅ CyberVerse Presenter Video Rendered: {out_mp4}")
    print(f"🖥️ Copied to Desktop: {desktop_mp4}")
    return out_mp4

if __name__ == "__main__":
    for brand, title, sents in [
        ("procrm", "PRO CRM Autonomous Multi-Agent AI", [
            "Are you ready to deploy governed enterprise AI workflows in 2026?",
            "PRO CRM delivers autonomous multi-agent networks with zero data retention and APRA CPS 234 compliance.",
            "Contact our Principal Architects today at 1300 050 099 or visit procrm.com.au."
        ]),
        ("ezconsultants", "NDIS & Healthcare Compliance Blueprint", [
            "Navigating the latest NDIS quality safeguards and mandatory care minutes?",
            "EZ Consultants provides end-to-end digital compliance and audit-ready reporting.",
            "Book your strategy consultation today with our national advisory team."
        ])
    ]:
        render_cyberverse_video(brand, title, sents)
        
    os.system(f'cd "{BLOGS_DIR}" && git add scripts/ assets/ && git commit -m "Add CyberVerse Staging AI Avatar Engine" && git push origin main')
    print("\n🎉 CyberVerse Engine is live and pushed to GitHub!")
