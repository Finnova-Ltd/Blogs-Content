#!/usr/bin/env python3
"""
Professional YouTube Shorts / Reels Subtitle & Video Compositor
---------------------------------------------------------------
Uses ASS (Advanced SubStation Alpha) Subtitles for:
- Perfect TikTok/Shorts typography with zero escaping artifacts.
- Centered, glowing text with black outline and drop shadow.
- High-resolution background imagery with slow Ken-Burns panning motion.
- Overlaid brand logos and CTA buttons.
"""

import os
import subprocess
import imageio_ffmpeg
import edge_tts
import asyncio

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
OUTPUT_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/generated_videos"

def generate_ass_subtitles(sentences, seg_duration, ass_path):
    """Creates a stylized ASS subtitle file for TikTok/Shorts text styling."""
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,3,5,60,60,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for i, s in enumerate(sentences):
        t_start_s = i * seg_duration
        t_end_s = (i + 1) * seg_duration
        
        # Format HH:MM:SS.cs
        start_str = f"0:{int(t_start_s//60):02d}:{int(t_start_s%60):02d}.{int((t_start_s%1)*100):02d}"
        end_str = f"0:{int(t_end_s//60):02d}:{int(t_end_s%60):02d}.{int((t_end_s%1)*100):02d}"
        
        # Word wrap into 3-4 words per line with \N
        words = s.strip().split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(cur) >= 4:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))
        wrapped = "\\N".join(lines)
        
        events.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{wrapped}")
        
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
    return ass_path

def render_pro_short(
    title,
    sentences,
    brand_name,
    bg_image_path,
    website_url,
    output_mp4,
    voice="en-AU-NatashaNeural"
):
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    temp_audio = output_mp4.replace(".mp4", "_pro_audio.mp3")
    temp_ass = output_mp4.replace(".mp4", "_subs.ass")
    
    # 1. Voiceover
    full_text = " ".join(sentences)
    asyncio.run(edge_tts.Communicate(full_text, voice).save(temp_audio))
    
    # 2. Duration
    probe_cmd = [ffmpeg_exe, "-i", temp_audio]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    duration = 15.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            try:
                dur_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = dur_str.split(":")
                duration = int(h) * 3600 + int(m) * 60 + float(s)
                break
            except:
                pass
    print(f"⏱️ Audio duration: {duration:.2f}s")
    
    # 3. ASS Subtitles
    seg_dur = duration / max(len(sentences), 1)
    generate_ass_subtitles(sentences, seg_dur, temp_ass)
    
    # 4. Filter Complex
    total_frames = int(duration * 30)
    font_file = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    if not os.path.exists(font_file):
        font_file = "/System/Library/Fonts/Helvetica.ttc"
        
    clean_title = title.replace("'", "").replace(":", " -")[:35]
    domain = website_url.replace("https://", "").split("/")[0]
    
    # Use ASS subtitle filter for professional captions
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"zoompan=z='min(zoom+0.0008,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x1920:fps=30,"
        f"drawbox=y=0:color=black@0.45:width=iw:height=ih:t=fill,"
        f"drawtext=fontfile='{font_file}':text='{brand_name.upper()}':fontcolor=0x38bdf8:fontsize=40:x=(w-text_w)/2:y=180:box=1:boxcolor=0x0f172a@0.95:boxborderw=20,"
        f"drawtext=fontfile='{font_file}':text='{clean_title}':fontcolor=0xfacc15:fontsize=46:x=(w-text_w)/2:y=280:box=1:boxcolor=0x1e293b@0.95:boxborderw=22,"
        f"subtitles={temp_ass},"
        f"drawtext=fontfile='{font_file}':text='Visit {domain}':fontcolor=0xffffff:fontsize=42:x=(w-text_w)/2:y=1660:box=1:boxcolor=0x2563eb@0.95:boxborderw=26[outv]"
    )
    
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-i", bg_image_path,
        "-i", temp_audio,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-shortest",
        output_mp4
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    for p in [temp_audio, temp_ass]:
        if os.path.exists(p):
            os.remove(p)
    return output_mp4

if __name__ == "__main__":
    out_file = os.path.join(OUTPUT_DIR, "pro_youtube_short.mp4")
    print("🎬 Rendering Professional Short with ASS subtitles & Ken-Burns image...")
    render_pro_short(
        title="RBA Cash Rate Decision 2026",
        sentences=[
            "Did you know the latest Reserve Bank update could save you thousands on your home loan?",
            "Major Australian lenders are adjusting refinancing tiers right now.",
            "Compare your rate with accredited brokers to lock in your lowest monthly repayment."
        ],
        brand_name="EZ Mortgage Broker",
        bg_image_path="/Users/robinbakshi/Documents/GitHub/ezmortgagebroker/public/assets/luxury-home-refinance-hero-OeZc7gD4.webp",
        website_url="https://ezmortgagebroker.com.au/pages/blog/rba-cash-rate-decision-mortgage-repayments-2026.html",
        output_mp4=out_file
    )
    print("✅ Professional Short rendered at:", out_file)
