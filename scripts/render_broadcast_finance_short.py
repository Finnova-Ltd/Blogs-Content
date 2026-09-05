#!/usr/bin/env python3
"""
Broadcast-Grade Financial News Video Generator (Path A)
FINNOVA / EZMORTGAGE BROKERAGE • AUSTRALIAN FINANCIAL MEDIA ENGINE

Produces television-quality 1080x1920 (9:16) financial news shorts:
1. Dynamic full-screen motion visuals (Ken Burns pan/zoom over real Melbourne property assets).
2. Live-rendered Glassmorphic Rate Comparison Infographic (Sub-5.89% vs Big 4 6.45%).
3. Kinetic bold captions with word-level readability.
4. Broadcast-standard lower-third featuring R Bakshi (MFAA Accredited, CRN 538522).
5. Studio-mastered Australian neural voiceover.
Replaces low-quality static photo cutout mouth animations permanently.
"""

import os
import sys
import math
import asyncio
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime, timezone
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import imageio_ffmpeg
import edge_tts

AEST = ZoneInfo("Australia/Melbourne")
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
EZ_DIR = Path("/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker")
CACHE_DIR = BASE_DIR / "scripts" / "asset_cache"
FRAMES_DIR = CACHE_DIR / "broadcast_frames"

for d in [CACHE_DIR, FRAMES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# System Fonts
FONT_HEAVY = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_HEAVY):
    FONT_HEAVY = "/System/Library/Fonts/Helvetica.ttc"
if not os.path.exists(FONT_REGULAR):
    FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"

def get_current_date_str():
    return datetime.now(timezone.utc).astimezone(AEST).strftime("%d-%b-%Y")

async def generate_broadcast_voice(script_text, out_audio_path):
    """Synthesize high-fidelity Australian neural voiceover."""
    communicate = edge_tts.Communicate(script_text, "en-AU-WilliamNeural", rate="+4%")
    await communicate.save(out_audio_path)

def create_background_scene(width=1080, height=1920, zoom=1.0, pan_y=0):
    """
    Creates dynamic animated background using real Melbourne luxury property visual.
    """
    bg_path = ASSETS_DIR / "luxury-home-refinance-hero-OeZc7gD4.webp"
    if not bg_path.exists():
        bg_path = ASSETS_DIR / "tarneit-melbourne-property-hero-CcSqf1cE.webp"

    with Image.open(bg_path).convert("RGBA") as img:
        # Scale & center crop
        w, h = img.size
        target_w = int(width * zoom)
        target_h = int((target_w / w) * h)
        if target_h < height:
            target_h = int(height * zoom)
            target_w = int((target_h / h) * w)

        resized = img.resize((target_w, target_h), Image.Resampling.BILINEAR)
        left = max(0, (target_w - width) // 2)
        top = max(0, min(target_h - height, (target_h - height) // 2 + pan_y))
        cropped = resized.crop((left, top, left + width, top + height))

        # Add broadcast cinematic dark vignette overlay for readability
        overlay = Image.new("RGBA", (width, height), (10, 20, 35, 180))
        dimmed = Image.alpha_composite(cropped, overlay)
        return dimmed

def build_broadcast_frame(t, total_duration, script_words, width=1080, height=1920):
    """
    Composites one high-definition 1080x1920 television financial news frame.
    """
    # 1. Background with gentle Ken Burns motion
    zoom = 1.0 + 0.05 * math.sin((t / total_duration) * math.pi)
    pan_y = int(40 * math.sin((t / total_duration) * 2 * math.pi))
    canvas = create_background_scene(width, height, zoom=zoom, pan_y=pan_y)
    draw = ImageDraw.Draw(canvas)

    # 2. Top News Banner
    draw.rectangle([0, 0, width, 140], fill=(10, 37, 64, 240))
    # Red LIVE dot
    dot_color = (239, 68, 68) if int(t * 2) % 2 == 0 else (185, 28, 28)
    draw.ellipse([45, 52, 65, 72], fill=dot_color)
    
    font_top = ImageFont.truetype(FONT_HEAVY, 34)
    font_sub = ImageFont.truetype(FONT_REGULAR, 24)
    font_card_title = ImageFont.truetype(FONT_HEAVY, 36)
    font_card_sub = ImageFont.truetype(FONT_REGULAR, 26)
    font_rate = ImageFont.truetype(FONT_HEAVY, 54)
    font_caption = ImageFont.truetype(FONT_HEAVY, 46)

    draw.text((80, 44), "MELBOURNE FINANCIAL MARKET REPORT", font=font_top, fill=(255, 255, 255))
    draw.text((80, 88), f"RBA Cash Rate Outlook • Updated {get_current_date_str()} AEST", font=font_sub, fill=(0, 212, 170))

    # 3. Center Stage: High-Impact Rate Comparison Card (Glassmorphic)
    card_top = 260
    card_h = 720
    # Glass backdrop
    card_bg = Image.new("RGBA", (width - 100, card_h), (15, 23, 42, 220))
    canvas.paste(card_bg, (50, card_top), card_bg)

    # Card border
    draw.rectangle([50, card_top, width - 50, card_top + card_h], outline=(0, 135, 108), width=4)
    
    # Card Header
    draw.rectangle([50, card_top, width - 50, card_top + 90], fill=(0, 135, 108, 255))
    draw.text((80, card_top + 24), "📊 MELBOURNE LENDING COMPARISON", font=font_card_title, fill=(255, 255, 255))

    # Row 1: Variable Rate
    r1_y = card_top + 130
    draw.text((80, r1_y), "Owner Occupied Variable Loan (<80% LVR)", font=font_card_sub, fill=(203, 213, 225))
    draw.text((80, r1_y + 40), "EZ Panel Rate: 5.89% p.a.", font=font_rate, fill=(52, 211, 153))
    draw.text((700, r1_y + 50), "Big 4: 6.45%", font=font_card_title, fill=(239, 68, 68))
    draw.line([80, r1_y + 115, width - 80, r1_y + 115], fill=(51, 65, 85), width=2)

    # Row 2: First Home Buyer
    r2_y = card_top + 280
    draw.text((80, r2_y), "First Home Guarantee (5% Deposit • $0 LMI)", font=font_card_sub, fill=(203, 213, 225))
    draw.text((80, r2_y + 40), "Specialist Rate: 5.99% p.a.", font=font_rate, fill=(52, 211, 153))
    draw.text((700, r2_y + 50), "+ $10k Grant", font=font_card_title, fill=(250, 204, 21))
    draw.line([80, r2_y + 115, width - 80, r2_y + 115], fill=(51, 65, 85), width=2)

    # Row 3: Refinance Benefit
    r3_y = card_top + 430
    draw.text((80, r3_y), "Refinancing & Equity Cash-Out Opportunity", font=font_card_sub, fill=(203, 213, 225))
    draw.text((80, r3_y + 40), "Up to $3,000 Refinance Cashback", font=ImageFont.truetype(FONT_HEAVY, 42), fill=(255, 255, 255))
    draw.text((80, r3_y + 95), "Save an estimated $280+/month on an average $650k mortgage.", font=font_card_sub, fill=(148, 163, 184))

    # Lender Panel Badge
    draw.rectangle([80, card_top + 590, width - 80, card_top + 670], fill=(30, 41, 59, 255), outline=(71, 85, 105), width=2)
    draw.text((120, card_top + 614), "🏛️ Access Over 30+ Accredited Australian Lenders", font=ImageFont.truetype(FONT_HEAVY, 30), fill=(255, 255, 255))

    # 4. Kinetic Subtitles Stage (Dynamic Highlight)
    # Highlight word based on time progress
    words_count = len(script_words)
    current_word_idx = min(words_count - 1, int((t / total_duration) * words_count))
    # Slice a window of 6 words
    start_w = max(0, current_word_idx - 3)
    end_w = min(words_count, start_w + 6)
    snippet = " ".join(script_words[start_w:end_w])

    sub_box_y = 1040
    draw.rectangle([60, sub_box_y, width - 60, sub_box_y + 170], fill=(0, 0, 0, 200), outline=(234, 179, 8), width=3)
    draw.text((90, sub_box_y + 55), snippet, font=font_caption, fill=(254, 240, 138))

    # 5. Broadcast Lower-Third: Verified MFAA Broker Card (R Bakshi)
    lt_y = 1420
    lt_h = 420
    draw.rectangle([50, lt_y, width - 50, lt_y + lt_h], fill=(10, 37, 64, 245), outline=(0, 135, 108), width=3)

    # Broker Avatar
    avatar_path = EZ_DIR / "public" / "images" / "r-bakshi.jpeg"
    if not avatar_path.exists():
        avatar_path = Path("/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker/images/r-bakshi.jpeg")

    if avatar_path.exists():
        with Image.open(avatar_path).convert("RGBA") as a_img:
            a_cropped = a_img.resize((200, 200), Image.Resampling.LANCZOS)
            # Circular mask
            mask = Image.new("L", (200, 200), 0)
            m_draw = ImageDraw.Draw(mask)
            m_draw.ellipse((0, 0, 200, 200), fill=255)
            canvas.paste(a_cropped, (80, lt_y + 40), mask)
            draw.ellipse([76, lt_y + 36, 284, lt_y + 244], outline=(255, 255, 255), width=5)

    # Broker Credentials text
    draw.text((310, lt_y + 40), "R BAKSHI", font=ImageFont.truetype(FONT_HEAVY, 42), fill=(255, 255, 255))
    draw.text((310, lt_y + 90), "PRINCIPAL FINANCE BROKER (MFAA ACCREDITED)", font=ImageFont.truetype(FONT_HEAVY, 24), fill=(0, 212, 170))
    draw.text((310, lt_y + 125), "CRN: 538522  •  Aggregator: nMB  •  30+ Lenders", font=font_card_sub, fill=(203, 213, 225))
    draw.text((310, lt_y + 165), "Melbourne Residential & Commercial Property Specialist", font=ImageFont.truetype(FONT_REGULAR, 22), fill=(148, 163, 184))

    # CTA Buttons in lower third
    draw.rectangle([80, lt_y + 270, 520, lt_y + 360], fill=(0, 135, 108), outline=(255, 255, 255), width=2)
    draw.text((120, lt_y + 295), "📞 CALL 1300 050 099", font=ImageFont.truetype(FONT_HEAVY, 30), fill=(255, 255, 255))

    draw.rectangle([550, lt_y + 270, width - 80, lt_y + 360], fill=(30, 41, 59), outline=(255, 255, 255), width=2)
    draw.text((580, lt_y + 295), "🌐 ezmortgagebroker.com.au", font=ImageFont.truetype(FONT_HEAVY, 28), fill=(255, 255, 255))

    return canvas

def render_broadcast_video():
    """Generates the full broadcast-grade short video."""
    print("=== Rendering Broadcast-Grade Financial News Short (Path A) ===")
    
    script_text = (
        "G'day! This is your Melbourne mortgage and property finance market report. "
        "With current interest rate pressures, variable home loan rates on our accredited panel are starting from "
        "5.89% per annum, well below the big four bank average of 6.45%. "
        "First home buyers can access the 5% deposit guarantee scheme with zero lenders mortgage insurance, "
        "plus Victoria's $10,000 first home owner grant. "
        "If you are looking to refinance, lock in competitive rates, or calculate your maximum borrowing power, "
        "call R Bakshi on 1300 050 099 or visit ezmortgagebroker.com.au today."
    )
    script_words = script_text.split()

    audio_path = CACHE_DIR / "broadcast_voice.mp3"
    print("[1/4] Generating Australian neural voiceover...")
    asyncio.run(generate_broadcast_voice(script_text, str(audio_path)))

    # Get audio duration
    probe_cmd = [ffmpeg_exe, "-i", str(audio_path)]
    probe_res = subprocess.run(probe_cmd, stderr=subprocess.PIPE, text=True)
    duration = 24.0
    for line in probe_res.stderr.splitlines():
        if "Duration" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            duration = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
            break

    print(f"[2/4] Synthesizing video frames (Duration: {duration:.2f}s at 25 fps)...")
    fps = 25
    total_frames = int(duration * fps)

    # Clean old frames
    for f in FRAMES_DIR.glob("*.jpg"):
        f.unlink()

    # Step rendering (render 1 frame every 4 and use ffmpeg fps blend for high speed)
    # To keep generation fast and crisp, render keyframes and encode
    for i in range(total_frames):
        t = i / fps
        frame = build_broadcast_frame(t, duration, script_words)
        frame_path = FRAMES_DIR / f"frame_{i:05d}.jpg"
        frame.convert("RGB").save(frame_path, "JPEG", quality=90)
        if i % 100 == 0:
            print(f"  -> Processed frame {i}/{total_frames} ({int(i/total_frames*100)}%)")

    print("[3/4] Assembling MP4 with FFmpeg & AAC stereo audio...")
    raw_video = CACHE_DIR / "broadcast_raw.mp4"
    final_video = CACHE_DIR / "broadcast_final.mp4"

    compile_cmd = [
        ffmpeg_exe, "-y",
        "-framerate", f"{fps}",
        "-i", str(FRAMES_DIR / "frame_%05d.jpg"),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_video)
    ]
    subprocess.run(compile_cmd, check=True)

    print("[4/4] Publishing broadcast-grade video to ezmortgagebroker & Blogs-Content...")
    targets = [
        EZ_DIR / "public" / "assets" / "videos" / "ezmortgage_2026_rba_cash_rate___refi_live_talking_short.mp4",
        EZ_DIR / "public" / "assets" / "videos" / "ezmortgage_rba_cash_rate_outlook___r_digital_human_short.mp4",
        EZ_DIR / "assets" / "videos" / "ezmortgage_2026_rba_cash_rate___refi_live_talking_short.mp4",
        EZ_DIR / "assets" / "videos" / "ezmortgage_rba_cash_rate_outlook___r_digital_human_short.mp4",
        ASSETS_DIR / "videos" / "ezmortgage_2026_rba_cash_rate___refi_live_talking_short.mp4",
        ASSETS_DIR / "videos" / "ezmortgage_rba_cash_rate_outlook___r_digital_human_short.mp4"
    ]

    for t in targets:
        t.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", str(final_video), str(t)], check=True)

    print(f"✅ SUCCESS: Overwritten low-quality cutout puppet videos with Broadcast-Grade Financial Report!")
    return str(final_video)

if __name__ == "__main__":
    render_broadcast_video()
