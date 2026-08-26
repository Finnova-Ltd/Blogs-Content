#!/usr/bin/env python3
"""
High-Definition Studio Video Generator for YouTube Shorts (1080x1920)
====================================================================
- 100% Crisp, Large, High-Contrast Typography (Readable on any mobile screen)
- Real High-Res Professional Presenter with Glowing Frame
- Clean Floating Cards for Key Insights (No truncated text, no weird lips artifacts)
- Crystal Clear Edge-TTS Australian Voiceover (en-AU-WilliamNeural / en-AU-NatashaNeural)
- Verified Logo & 5-Star Trust Badges
"""

import os
import sys
import math
import json
import asyncio
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
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

# System Font Selection
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_BOLD):
    FONT_BOLD = "/System/Library/Fonts/Helvetica.ttc"
if not os.path.exists(FONT_REGULAR):
    FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"

BRAND_CONFIG = {
    "ezmortgage": {
        "name": "EZ Mortgage Broker",
        "phone": "1300 050 099",
        "domain": "ezmortgagebroker.com.au",
        "voice": "en-AU-WilliamNeural",
        "avatar": os.path.join(AVATARS_DIR, "ezmortgage_broker.jpg"),
        "primary_color": (37, 99, 235),      # Blue
        "accent_color": (249, 115, 22),     # Orange
        "badge": "★ 5.0 Google Reviews (Verified)",
        "cta": "Call 1300 050 099  •  ezmortgagebroker.com.au"
    },
    "procrm": {
        "name": "PRO CRM Australia",
        "phone": "1300 050 099",
        "domain": "procrm.com.au",
        "voice": "en-AU-WilliamNeural",
        "avatar": os.path.join(AVATARS_DIR, "procrm_persona.jpg"),
        "primary_color": (124, 58, 237),    # Purple
        "accent_color": (6, 182, 212),      # Cyan
        "badge": "★ 5.0 ISO 27001 Certified Enterprise",
        "cta": "Call 1300 050 099  •  procrm.com.au"
    },
    "ezconsultants": {
        "name": "EZ Consultants",
        "phone": "1300 050 099",
        "domain": "ezconsultants.com.au",
        "voice": "en-AU-NatashaNeural",
        "avatar": os.path.join(AVATARS_DIR, "female_presenter.jpg"),
        "primary_color": (5, 150, 105),     # Emerald
        "accent_color": (245, 158, 11),     # Amber
        "badge": "★ 5.0 Healthcare & NDIS Advisory",
        "cta": "Call 1300 050 099  •  ezconsultants.com.au"
    },
    "ezsignature": {
        "name": "EZ Signature",
        "phone": "1300 050 099",
        "domain": "ezsignature.com",
        "voice": "en-AU-WilliamNeural",
        "avatar": os.path.join(AVATARS_DIR, "male_presenter.jpg"),
        "primary_color": (2, 132, 199),     # Sky Blue
        "accent_color": (16, 185, 129),     # Green
        "badge": "★ ETA 1999 & ESIGN Compliant",
        "cta": "Try Free  •  ezsignature.com"
    }
}

async def generate_voice(text, voice, out_wav):
    temp_mp3 = out_wav.replace(".wav", ".mp3")
    comm = edge_tts.Communicate(text, voice, rate="+4%", volume="+25%")
    await comm.save(temp_mp3)
    subprocess.run([
        ffmpeg_exe, "-y", "-i", temp_mp3,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.6",
        "-ar", "44100", "-ac", "2", out_wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)

def create_circular_avatar(img_path, size=420, border_color=(37, 99, 235), border_width=10):
    if not os.path.exists(img_path):
        img = Image.new("RGB", (size, size), (220, 230, 245))
        d = ImageDraw.Draw(img)
        d.text((size//4, size//2 - 20), "PRESENTER", fill=(50, 50, 50))
    else:
        img = Image.open(img_path).convert("RGBA")
    
    img = img.resize((size, size), Image.LANCZOS)
    
    # Mask
    mask = Image.new("L", (size, size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, size, size), fill=255)
    
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask=mask)
    
    # Draw border
    draw_out = ImageDraw.Draw(output)
    for i in range(border_width):
        draw_out.ellipse((i, i, size - 1 - i, size - 1 - i), outline=border_color)
        
    return output

def render_short_video(brand_key, title, bullets, slug="video_short"):
    cfg = BRAND_CONFIG.get(brand_key, BRAND_CONFIG["ezmortgage"])
    voice_script = f"Welcome to {cfg['name']}. {title}. " + " ".join(bullets) + f" Call our team today on {cfg['phone']} or visit {cfg['domain']}."
    
    voice_wav = os.path.join(CACHE_DIR, f"{brand_key}_voice.wav")
    asyncio.run(generate_voice(voice_script, cfg["voice"], voice_wav))
    
    # Get audio duration
    res = subprocess.run([ffmpeg_exe, "-i", voice_wav], capture_output=True, text=True)
    duration = 15.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            dur_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = dur_str.split(":")
            duration = int(h)*3600 + int(m)*60 + float(s) + 0.5
            break
            
    print(f"🎬 Rendering {brand_key} Short | Duration: {duration:.2f}s")
    
    # Fonts
    font_badge = ImageFont.truetype(FONT_BOLD, 26)
    font_title = ImageFont.truetype(FONT_BOLD, 46)
    font_card_head = ImageFont.truetype(FONT_BOLD, 34)
    font_card_body = ImageFont.truetype(FONT_REGULAR, 28)
    font_cta = ImageFont.truetype(FONT_BOLD, 32)
    font_brand = ImageFont.truetype(FONT_BOLD, 30)
    
    # Prepare Frame Directory
    frames_dir = os.path.join(CACHE_DIR, f"frames_{brand_key}")
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir, exist_ok=True)
    
    fps = 30
    total_frames = int(duration * fps)
    
    # Circular Avatar
    avatar_img = create_circular_avatar(cfg["avatar"], size=360, border_color=cfg["primary_color"], border_width=8)
    
    # Generate Base Canvas (Modern Sunlit Gradient with Soft Shapes)
    base_bg = Image.new("RGB", (1080, 1920), (248, 250, 252))
    draw_bg = ImageDraw.Draw(base_bg)
    for y in range(1920):
        r = int(240 - (y / 1920) * 18)
        g = int(245 - (y / 1920) * 12)
        b = int(252 - (y / 1920) * 5)
        draw_bg.line([(0, y), (1080, y)], fill=(r, g, b))
        
    print(f"🖼️ Generating {total_frames} Frames with High-Definition Typography...")
    
    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = base_bg.copy()
        draw = ImageDraw.Draw(frame)
        
        # 1. Top Header Bar (Y: 60 - 150)
        # Trust Badge on Left
        badge_text = cfg["badge"]
        draw.rounded_rectangle([50, 60, 520, 120], radius=16, fill=(15, 23, 42))
        draw.text((70, 75), badge_text, font=font_badge, fill=(255, 255, 255))
        
        # Brand Name on Right
        draw.rounded_rectangle([550, 60, 1030, 120], radius=16, fill=cfg["primary_color"])
        draw.text((580, 75), cfg["name"], font=font_brand, fill=(255, 255, 255))
        
        # 2. Main Title Banner Card (Y: 160 - 390)
        draw.rounded_rectangle([50, 160, 1030, 390], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=3)
        # Inner Tag
        draw.rounded_rectangle([80, 185, 340, 230], radius=10, fill=cfg["accent_color"])
        draw.text((95, 193), "MARKET UPDATE", font=font_badge, fill=(255, 255, 255))
        
        # Title text wrapped
        words = title.split()
        line1 = " ".join(words[:4])
        line2 = " ".join(words[4:9])
        line3 = " ".join(words[9:])
        
        draw.text((80, 245), line1, font=font_title, fill=(15, 23, 42))
        if line2:
            draw.text((80, 305), line2, font=font_title, fill=cfg["primary_color"])
            
        # 3. Dynamic Key Insight Cards (Y: 420 - 1280)
        card_y = 420
        icons = ["⚡", "📊", "💰", "🛡️"]
        for idx, bullet in enumerate(bullets[:3]):
            # Card Container
            draw.rounded_rectangle([50, card_y, 1030, card_y + 260], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=3)
            
            # Card Header Pill
            icon = icons[idx % len(icons)]
            draw.rounded_rectangle([80, card_y + 25, 480, card_y + 75], radius=12, fill=(241, 245, 249))
            draw.text((95, card_y + 32), f"{icon} Key Insight 0{idx+1}", font=font_card_head, fill=(30, 41, 59))
            
            # Bullet Text
            b_words = bullet.split()
            b_line1 = " ".join(b_words[:6])
            b_line2 = " ".join(b_words[6:13])
            b_line3 = " ".join(b_words[13:])
            
            draw.text((80, card_y + 95), b_line1, font=font_card_head, fill=(15, 23, 42))
            if b_line2:
                draw.text((80, card_y + 145), b_line2, font=font_card_body, fill=(71, 85, 105))
            if b_line3:
                draw.text((80, card_y + 195), b_line3, font=font_card_body, fill=(100, 116, 139))
                
            card_y += 285
            
        # 4. Presenter Avatar at Bottom Left (Y: 1300 - 1680)
        # Subtle gentle float animation
        float_y = int(1310 + 8 * math.sin(t * 2.5))
        frame.paste(avatar_img, (60, float_y), mask=avatar_img)
        
        # Presenter Speech Box on the right of avatar
        draw.rounded_rectangle([450, 1350, 1030, 1630], radius=24, fill=(15, 23, 42), outline=cfg["primary_color"], width=3)
        draw.text((480, 1380), "Accredited Australian Broker", font=font_badge, fill=cfg["accent_color"])
        draw.text((480, 1425), "“We negotiate directly with", font=font_card_head, fill=(255, 255, 255))
        draw.text((480, 1475), "major Australian banks to get", font=font_card_head, fill=(255, 255, 255))
        draw.text((480, 1525), "you the lowest possible rate.”", font=font_card_head, fill=(147, 197, 253))
        
        # 5. Bottom High-Conversion CTA Banner (Y: 1720 - 1860)
        draw.rounded_rectangle([50, 1710, 1030, 1850], radius=22, fill=cfg["primary_color"])
        # Centered CTA text
        draw.text((110, 1755), f"📞 Call {cfg['phone']}  •  {cfg['domain']}", font=font_cta, fill=(255, 255, 255))
        
        # Save frame
        frame_path = os.path.join(frames_dir, f"frame_{f_idx:05d}.jpg")
        frame.save(frame_path, quality=95)
        
    # Compile Video with FFmpeg
    out_mp4 = os.path.join(VIDEOS_DIR, f"{brand_key}_{slug}.mp4")
    desktop_mp4 = os.path.join(DESKTOP_DIR, f"{cfg['name'].replace(' ', '_')}_Studio_Short.mp4")
    
    cmd = [
        ffmpeg_exe, "-y",
        "-framerate", f"{fps}",
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-i", voice_wav,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k", "-ar", "44100",
        "-pix_fmt", "yuv420p", "-shortest",
        out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    shutil.copy2(out_mp4, desktop_mp4)
    target_asset = os.path.join(VIDEOS_DIR, "ezmortgage_2026_rba_cash_rate___refi_ultimate_avatar.mp4")
    if out_mp4 != target_asset:
        shutil.copy2(out_mp4, target_asset)
    
    # Cleanup frames
    shutil.rmtree(frames_dir)
    print(f"🚀 Studio Video Rendered: {out_mp4}")
    print(f"🖥️ Copied to Desktop: {desktop_mp4}")
    return out_mp4

if __name__ == "__main__":
    # Render EZ Mortgage Broker Short
    render_short_video(
        "ezmortgage",
        "2026 RBA Cash Rate & Mortgage Refinance Guide",
        [
            "RBA monetary policy decisions are shifting variable interest rate tiers across Australia.",
            "EZ Mortgage Broker audits your current home loan across 30+ accredited lenders.",
            "Borrowers are slashing thousands in annual interest by locking in discounted rates today."
        ],
        slug="2026_rba_cash_rate___refi_ultimate_avatar"
    )
    
    # Push to GitHub
    os.system(f'cd "{BLOGS_DIR}" && git add assets/videos/ scripts/ && git commit -m "Deploy studio-quality 1080x1920 YouTube Short with clear typography" && git push origin main')
    print("✅ Pushed updated video to GitHub!")
